import json
from numpy import true_divide
import pandas as pd
import requests
import smtplib 
import warnings
warnings.filterwarnings('ignore')
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# local import
from paths import *

def loginListado():

    # credential for login to zendro
    auth = {
        "username": username,
        "password": password,
        "client_id": client_id,
        "grant_type": grant_type
    }

    # make a post to a zendro-keycloak endpoint to retrieve session token
    login = requests.post(
        listado_token,
        verify=False,
        data=auth
    )

    # if status code in the response is 200, then the request was successful and we have
    # the session token we need in the login response
    if login.status_code == 200:
        
        # we create a session object to use it for the requests to zendro api
        session = requests.Session()

        # and store the token we receive in the 'Authorization' header as a Bearer token
        session.headers.update({
            "Authorization": "Bearer " + login.json()["access_token"]
        })
        
        print("Successful login")
        return session


def get_pendientes():
    query = """{
            agrobiodiversidads(pagination:{limit:5000} search:{field:id, value:"%pendiente%", operator:like}){
                id
                taxon
                categoria_agrobiodiversidad
                es_parientesilvestre
                es_domesticado
                es_quelite
                comentarios_revision

            }
            }"""

    r = session.post(path_siagro, json={'query': query}, verify=False)
    json_data = json.loads(r.text)
    json_data = json_data['data']['agrobiodiversidads']
    actual=pd.read_csv(path_actual, keep_default_na=False)   
    anterior=pd.read_csv(path_anterior, keep_default_na=False)   
    #print(json_data['data']['agrobiodiversidads'])
    aux=[]
    for i in range (len(json_data)):
        #print(json_data[i]['taxon'])
        res=search_taxon(json_data[i],actual,anterior)
        if len(res) != 0:
            for j in range(len(res)):
                #print(res[j])
                aux.append(res[j])

    
    if len(aux) != 0:

        #sendeMail(aux)   
        pdData = pd.DataFrame(aux,columns=["ID pendiente", "Taxon pendiente", "ID coincidencia", "Taxon coincidencia", "Comentarios"])
        #print(aux[0])
        pdData.to_csv('check_pendiente.csv',index=False) 
        mailAdjunto()


def is_equal(info,json_data):
    if (info['taxon'] == json_data['taxon']) and (info['categoria_agrobiodiversidad'] == json_data['categoria_agrobiodiversidad']) and (info['es_parientesilvestre'] == json_data['es_parientesilvestre']) and (info['es_domesticado'] == json_data['es_domesticado']) and (info['es_quelite'] == json_data['es_quelite']):
        return True
    else:
        return False


def delete_pendiente(id):
    print("borrar: ", id)
    query = f'''mutation{{
                deleteAgrobiodiversidad(id:"{id}")
                }}'''
    #print(query)
    session.post(path_siagro, json={'query': query}, verify=False)

def mailAdjunto():
    # Iniciamos los parámetros del script
    remitente = 'siagro@siagro.conabio.gob.mx'
    #["Vivian <vbass@conabio.gob.mx>", "Oswaldo <ooliver@conabio.gob.mx>", "Mao <morjuela@conabio.gob.mx>"]
    destinatarios = ["Vivian <vbass@conabio.gob.mx>"]
    asunto = 'Revisar taxones con id pendiente'
    cuerpo = """La lista adjunta de taxones pendientes tiene similitudes con los taxones indicados, favor de revisar los campos categoria_agrobiodiversidad, es_parientesilvestre, es_domesticado y es_quelite.

Este es el aviso mensual, favor de hacer caso omiso si el registro ya se reviso y tiene comentarios. Si el registro ya se reviso y no tiene comentarios, favor de agregarlos.
    
------------------------------------
Este correo no contiene acentos y ha sido enviado automaticamente. Favor de no responder."""
    ruta_adjunto = 'check_pendiente.csv'
    nombre_adjunto = 'check_pendiente.csv'

    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()
    
    # Establecemos los atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = ", ".join(destinatarios)
    mensaje['Subject'] = asunto
    
    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))
    
    # Abrimos el archivo que vamos a adjuntar
    archivo_adjunto = open(ruta_adjunto, 'rb')
    
    # Creamos un objeto MIME base
    adjunto_MIME = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto
    adjunto_MIME.set_payload((archivo_adjunto).read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME)
    # Agregamos una cabecera al objeto
    adjunto_MIME.add_header('Content-Disposition', "attachment; filename= %s" % nombre_adjunto)
    # Y finalmente lo agregamos al mensaje
    mensaje.attach(adjunto_MIME)
    
    # Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    
    smtp = smtplib.SMTP('localhost') 
    smtp.sendmail(remitente, destinatarios, mensaje.as_string()) 


def is_new(id,actual,anterior):
    if (actual['id'].isin([id]).any()) and (anterior['id'].isin([id]).any() == False):
        return True
    else:
        return False

def search_taxon(info,actual,anterior):
    #print("taxon:", taxon)
    taxon_split=info['taxon'].split(' ')
    #print("taxon array:", taxon)
    taxon_p = "%"

    for i in taxon_split:
        taxon_p =  taxon_p + i + "%"
    
    #print("taxon_p:", taxon_p)
    query = """{
            agrobiodiversidads(pagination:{limit:50} search:{operator:and search:[{field:taxon, value:"""+"\""+taxon_p+"\""+""", operator:like}, {field:id value:"%pendiente%" operator:notLike}]}){
                id
                taxon
                categoria_agrobiodiversidad
                es_parientesilvestre
                es_domesticado
                es_quelite
                comentarios_revision
            }
        }"""

    #print(query)
    r = session.post(path_siagro, json={'query': query}, verify=False)
    json_data = json.loads(r.text)
    json_data = json_data['data']['agrobiodiversidads']
    formail=""
    arrFormail=[]
    

    if len(json_data) > 0 :
        
        for x in info:
            #print(info[x])
            if info[x] is None:
                info[x] = ''

        
        #print(info)
        for i in range(len(json_data)):
            
            #print(json_data[0]['taxon'])
            if is_equal(info,json_data[i]):
                delete_pendiente(info['id'])

            else:
                
                formail=info['id'] + "," + info['taxon'] + ","+ json_data[i]['id'] + ","+ json_data[i]['taxon'] + ","+ info['comentarios_revision']
                formail=formail.split(',')
                #print(formail)
                arrFormail.append(formail) 

    return arrFormail            

if __name__ == '__main__':
    print("Empieza check_pendiente archivos...")
    session=loginListado()
    get_pendientes()


    