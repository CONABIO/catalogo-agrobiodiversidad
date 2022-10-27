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


def getInfoZacatuche(record_id):
    '''
    Hace una consulta a zacatuche para obtener la información que se necesita de un id.
    Devuelve una pandas.Series con la información solicitada en la query.
    '''
    query = """query taxon{
                taxon(taxonID:"""+"\""+record_id+"\""+"""){
                            id
                            taxon: scientificName
                            estatus: taxonomicStatus
                            acceptedNameUsage{
                                id_valido: id
                                taxon_valido: scientificName
                            }
                            agrobiodiversityInfo{
                                es_parientesilvestre
                                es_domesticado
                                es_quelite
                                referencia
                            }
                        }
                        }"""

    r = session.post(path_zacatuche, json={'query': query}, verify=False)
    json_data = json.loads(r.text)
    json_data = json_data['data']['taxon']

    return json_data


def is_in_listado(id):
    query = """{
                countAgrobiodiversidads(search:{field:id, value:"""+"\""+id+"\""+""", operator:eq})
            }"""

    #print(query)
    r = session.post(path_siagro, json={'query': query}, verify=False)
    json_data = json.loads(r.text)
    #print(json_data)
    json_data = json_data['data']['countAgrobiodiversidads']

    if json_data > 0:
        return True
    else:
        return False

def change_valid(json_data,zacatuche):
    query = """
            mutation{
            updateAgrobiodiversidad(id:"""+"\""+json_data['id']+"\""+""" id_valido:"""+"\""+zacatuche['acceptedNameUsage']['id_valido']+"\""+""" taxon_valido:"""+"\""+zacatuche['acceptedNameUsage']['taxon_valido']+"\""+"""){
                id
            }
            }"""
    
    session.post(path_siagro, json={'query': query}, verify=False)

def add_new_valid(json_data,zacatuche):

    zacatuche = getInfoZacatuche(zacatuche['acceptedNameUsage']['id_valido'])

    if json_data['es_parientesilvestre'] is None:
        json_data['es_parientesilvestre']="null"
    if json_data['es_domesticado'] is None:
        json_data['es_domesticado']="null"
    if json_data['es_quelite'] is None:
        json_data['es_quelite']="null"

    query = """
            mutation{
            addAgrobiodiversidad(id:"""+"\""+zacatuche['acceptedNameUsage']['id_valido']+"\""+""" id_valido:"""+"\""+zacatuche['acceptedNameUsage']['id_valido']+"\""+""" taxon_valido:"""+"\""+zacatuche['acceptedNameUsage']['taxon_valido']+"\""+""" taxon:"""+"\""+zacatuche['taxon']+"\""+""" estatus:"""+"\""+zacatuche['estatus']+"\""+""" referencia:"""+"\""+json_data['referencia']+"\""+""" categoria_agrobiodiversidad:"Agrobiodiversidad" es_parientesilvestre:"""+str(json_data['es_parientesilvestre']).lower()+""" es_domesticado:"""+str(json_data['es_domesticado']).lower()+""" es_quelite:"""+str(json_data['es_quelite']).lower()+""" usuario:"Bot check sinónimo" ){
                id
            }
            }"""
    #print(query)
    session.post(path_siagro, json={'query': query}, verify=False) 


def delete_labels_pendiente(id):
    query = """
            mutation{
            updateAgrobiodiversidad(id:"""+"\""+id+"\""+"""categoria_agrobiodiversidad:null es_parientesilvestre: null es_domesticado:null es_quelite:null usuario:"Bot check sinónimo" ){
                id
            }
            }"""
    #print(query)
    session.post(path_siagro, json={'query': query}, verify=False)


def verify_labels(json_data,zacatuche):
    #print(json_data)
    zacatuche = getInfoZacatuche(zacatuche['acceptedNameUsage']['id_valido'])
    
    if (json_data['es_parientesilvestre']==zacatuche['agrobiodiversityInfo']['es_parientesilvestre']) and (json_data['es_domesticado']==zacatuche['agrobiodiversityInfo']['es_domesticado']) and (json_data['es_quelite']==zacatuche['agrobiodiversityInfo']['es_quelite']):
        delete_labels_pendiente(json_data['id'])
    if (zacatuche['agrobiodiversityInfo']['es_parientesilvestre'] is None) and (zacatuche['agrobiodiversityInfo']['es_domesticado'] is None) and (zacatuche['agrobiodiversityInfo']['es_quelite'] is None):
        print("Las etiquetas estan vacias, se eliminaran las etiquetas del sinonimo y se heredaran a las del id valido")
        auxMutation=""
        if json_data['es_parientesilvestre'] is None:
            json_data['es_parientesilvestre']="null"
        if json_data['es_domesticado'] is None:
            json_data['es_domesticado']="null"
        if json_data['es_quelite'] is None:
            json_data['es_quelite']="null"
        if zacatuche['agrobiodiversityInfo']['referencia']=="":
            auxMutation="referencia: \""+ json_data['referencia']+"\""

        query = """
            mutation{
            updateAgrobiodiversidad(id:"""+"\""+zacatuche['id']+"\" "+ auxMutation + """ categoria_agrobiodiversidad:"Agrobiodiversidad" es_parientesilvestre: """+str(json_data['es_parientesilvestre']).lower()+""" es_domesticado:"""+str(json_data['es_domesticado']).lower()+""" es_quelite:"""+str(json_data['es_quelite']).lower()+""" usuario:"Bot check sinónimo" ){
                id
            }
            }"""
        #print(query)
        session.post(path_siagro, json={'query': query}, verify=False)
        delete_labels_pendiente(json_data['id'])
    else:
        print("VALIDAR CON OSWA Y MAO")
        print("Sinonimo: |",json_data['id']," | ",json_data['taxon']," | ",json_data['es_parientesilvestre']," | ",json_data['es_domesticado']," | ",json_data["es_quelite"])
        print("Valido: |",zacatuche['id']," | ",zacatuche['taxon']," | ",zacatuche['agrobiodiversityInfo']['es_parientesilvestre']," | ",zacatuche['agrobiodiversityInfo']['es_domesticado']," | ",zacatuche['agrobiodiversityInfo']['es_quelite'])
        print("\n")


def get_sinonimos():
    query = """{
            agrobiodiversidads(pagination:{limit:5000} search:{field:estatus, value:"%Sinónimo%", operator:like}){
                id
                taxon
                estatus
                id_valido
                taxon_valido
                referencia
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
    
    aux=[]
    for i in range (len(json_data)):

        zacatuche=getInfoZacatuche(json_data[i]['id'])

        #Si tanto en zacatuche como en el listado el estatus es sinónimo
        #hay que revisar primero que su id_valido sea igual, Si no,
        #hay que cambiar el id valido del registro en el listado.
        #Hay que verificar que el id valido esté en el listado, si no
        # hay que agregarlo y heredar etiquetas. Si si, se verifican etiquetas.
        #
        #Si el estatus es distinto en zacatuche y en el listado, se verificará en el script
        #estatus.py
        if zacatuche['estatus'] == json_data[i]['estatus']:
            if zacatuche['acceptedNameUsage'] is not None:
                if zacatuche['acceptedNameUsage']['id_valido']!=json_data[i]['id_valido']:
                    print("cambiar id_valido del taxon: ",json_data[i])
                    change_valid(json_data[i],zacatuche)
                    
                if is_in_listado(zacatuche['acceptedNameUsage']['id_valido']):
                    print("compara etiquetas")
                    
                    if (json_data[i]['categoria_agrobiodiversidad'] is None or json_data[i]['categoria_agrobiodiversidad'] == "") and (json_data[i]['es_domesticado'] is None) and (json_data[i]['es_quelite'] is None) and (json_data[i]['es_parientesilvestre'] is None):
                        #print(json_data[i])
                        print("El sinonimo ", json_data[i]['id']," ya no tiene etiquetas")
                    else:
                        verify_labels(json_data[i],zacatuche)
                    
                else:
                    print("agrega valido y elimina etiquetas")
                    add_new_valid(json_data[i],zacatuche)
                    delete_labels_pendiente(json_data[i]['id'])
                    
            else:
                print("El id ",json_data[i]['id']," tiene un id_valido None")
        print("\n")
    

if __name__ == '__main__':
    print("Empieza check_pendiente archivos...")
    session=loginListado()
    get_sinonimos()


    