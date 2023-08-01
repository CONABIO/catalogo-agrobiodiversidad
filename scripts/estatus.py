'''
Este script realiza la comparacion de lo que hay en nuestra base de datos local
contra lo que hay en Catalogo Conabio (CAT) via Zacatuche.
Si encuentra cambios entre las dos bases, realiza los respectivos cambios
en la base local directamente.
Si por alguna razon tenemos un ID que no se encuentre en Zacatuche
manda un correo a Alicia, Irene y Vivian para dar seguimiento.
Los logs del script se encuentran en logEstatus.txt
'''

import json
import pandas as pd
import requests
import smtplib 
import warnings
warnings.filterwarnings('ignore')

# local import
from paths import *

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

else:
    print("not successful")

def getInfoTaxon(record_id):
    '''
    Hace una consulta a zacatuche para obtener la informacion que se necesita de un id.
    Devuelve una pandas.Series con la informacion solicitada en la query.
    '''
    query = """query taxon{
                taxon(taxonID:"""+"\""+record_id+"\""+"""){
                            id
                            taxonomicStatus
                            scientificName
                            acceptedNameUsage{
                            id
                            scientificName
                            }
                        }
                        }"""
    #print(query)
    # renombrar las columnas
    New_col_names = {'acceptedNameUsage.id': 'id_valido',
                     'acceptedNameUsage.scientificName' : 'taxon_valido',
                     'taxonomicStatus': 'estatus',
                     'scientificName': 'taxon'
                    }

    r = session.post(path_zacatuche, json={'query': query}, verify=False)

    # TO DO: check that response.status = 200, else print error to log

    json_data = json.loads(r.text)
    #print(json_data)
    # case when id is not in CAT
    if json_data['data']['taxon'] is None:
        return None

    # case when there is no id_valido associated to id
    if json_data['data']['taxon']['acceptedNameUsage'] is None:
        df_data = (pd.json_normalize(json_data['data']['taxon'])
                     .rename(columns = New_col_names))
        df_data[['id_valido', 'taxon_valido']] = None, None
        df_data = df_data.fillna('')
        return df_data.loc[0]
    
    df_data = pd.json_normalize(json_data['data']['taxon'])
    df_data = (df_data.rename(columns = New_col_names)
                          .fillna(''))
    
    return df_data.loc[0]


def updateLocal(agrobd_id, New_values):
    '''
    Realiza las modificaciones en la instancia de catalogo-agrobiodiversidad
    de los campos que se le pasen como parametro.
    '''
    #print("estoy en update: ",agrobd_id)

    New_values['usuario'] = 'Bot validacion'
    
    # TO DO: ¿Como deben aparecer los valores vacios en mutation? 
    new_values = ''  
    for field in New_values:
        if New_values[field] is None:
            New_values[field] = ''
        if field == 'es_parientesilvestre' or field == 'es_domesticado' or field == 'es_quelite':
            if New_values[field] == 't':
                New_values[field] = 'true'
            if New_values[field] == 'f':
                New_values[field] = 'false'
            if New_values[field] == "":
                New_values[field] = "null"
            new_values += f'{field}: {New_values[field]} \n'
        else:
            new_values += f'{field}: \"{New_values[field]}\" \n'
        #new_values += f'{field}: \"{New_values[field]}\" \n'

    query = f'''mutation{{
                updateAgrobiodiversidad(
                    id:"{agrobd_id}"
                    {new_values}){{
                    id
                }}
                }}'''
    #print(query)
    session.post(path_siagro, json={'query': query}, verify=False)
    #print(res)


def is_synonym(record):  
    #print("estoy en is_synonym",record['id'])
    return (record['id_valido']) and (record['id'] != record['id_valido'])


def request_agrobd_review(record, check_previous_label=True):
    # if record doesn't have agrobd label, request review
    check = True
    if check_previous_label:
        check = record['categoria_agrobiodiversidad'] != 'Agrobiodiversidad'

    if check:
        try:
            note = record['comentarios_revision'] + ' - REVISAR ETIQUETA AGROBIODIVERSIDAD'

        except KeyError: # case when record not in local agrobd list
            note = 'REVISAR ETIQUETA AGROBIODIVERSIDAD'
        
        updateLocal(record['id'], {'comentarios_revision': note})

        


def delete_agrobd_label(record):
    # TO DO: also delete subcategoria_agrobiodiversidad
    # TO DO: como poner campos vacios    
    updateLocal(record['id'], {'categoria_agrobiodiversidad': '',
                                'es_parientesilvestre': "null",
                                'es_quelite': "null",
                                'es_domesticado': "null"})


def id_is_in_agrobd_list(record_id):
    return record_id in agrobd_list['id'].values


def add_record_to_agrobd_list(record):
    query = f'''mutation{{
                addAgrobiodiversidad(
                    id:"{record['id']}"
                    taxon:\"{record['taxon']}\"
                    estatus:\"{record['estatus']}\"
                    id_valido:"{record['id_valido']}"
                    taxon_valido:\"{record['taxon_valido']}\"
                    usuario:\"Bot validacion\"){{
                    id
                }}
                }}'''
    session.post(path_siagro, json={'query': query},verify=False)


def add_agrobd_label(record_id, agrobd):
    ''' 
    Agrega la etiqueta "Agrobiodiversidad" a un registro.
    Tambien agrega la subcategoria y las referencia que hereda del registro 
    cuyo estatus cambio de valido --> sinonimo.
    
    TO DO: Decidir que hacer en caso de que ya tenga la etiqueta y referencias.

    Recibe:
        record_id (string): nuevo id_valido del registro agrobd
        agrobd (pandas.Series): registro cuyo estatus cambio de valido -> sinonimo
    '''
    updateLocal(record_id, {'categoria_agrobiodiversidad': 'Agrobiodiversidad',
                            'referencia': agrobd['referencia'],
                            'es_parientesilvestre': agrobd['es_parientesilvestre'],
                            'es_domesticado': agrobd['es_domesticado'],
                            'es_quelite': agrobd['es_quelite']
                            })


def sendeMail(string):
    '''
    Envia un correo a las direcciones en "destinatario". 
    Recibe como parametro un string con los ids a los que se necesita dar seguimiento.
    '''
    remitente = "SIAgro <siagro@siagro.conabio.gob.mx>" 
    destinatario = ["Alicia <amastretta@conabio.gob.mx>","Oswaldo <oswaldo.oliveros@conabio.gob.mx>","Irma <ihernandez@conabio.gob.mx>"]
    asunto = "Aviso: no se encontro ID de taxon" 
    mensaje = """´En la validacion diaria de registros entre Zacatuche con nuestra base de datos de catalogo-agrobiodiversidad, se detecto que los siguientes IDs no se encontraron en Zacatuche. Favor de dar seguimiento a los casos. Para mas informacion sobre el script estatus.py favor de revisar https://github.com/CONABIO/catalogo-agrobiodiversidad#comparaci%C3%B3n-del-listado-contra-el-snib, o bien la seccion de monitoreo - Listado de agrobiodiversidad - Comparacion del listado contra el SNIB en la ruta J/USUARIOS/CARB/SIAgroBD/documentacion_servidores/documentacion.pdf

      ID       |      Taxon      

"""+string+"""
    
------------------------------------
Este correo ha sido enviado automaticamente. Favor de no responder.´"""
    email = 'Subject: {}\n\n{}'.format(asunto, mensaje)
    try: 
        smtp = smtplib.SMTP('localhost') 
        smtp.sendmail(remitente, destinatario, email.encode("utf8")) 
        print("Correo enviado")
    except: 
        print("""Error: el mensaje no pudo enviarse. 
        Compruebe que el mensaje no tenga acentos""")


def sendWarning(string, destinatario):
    """
    Envia un correo a las direcciones en "destinatario".
    """
    remitente = "SIAgro <siagro@siagro.conabio.gob.mx>"
    asunto = "ERROR EN COMPARACION LISTADO - ZACATUCHE"
    mensaje = ( """El archivo de """+string+""" que compara lo del listado contra lo que existe en Zacatuche no se actualizo. Favor de verificar. Para mas informacion sobre el script estatus.py favor de revisar https://github.com/CONABIO/catalogo-agrobiodiversidad#comparaci%C3%B3n-del-listado-contra-el-snib, o bien la seccion de monitoreo - Listado de agrobiodiversidad - Comparacion del listado contra el SNIB en la ruta J/USUARIOS/CARB/SIAgroBD/documentacion_servidores/documentacion.pdf
    
------------------------------------
Este correo no contiene acentos y ha sido enviado automaticamente. Favor de no responder."""
    )
    email = "Subject: {}\n\n{}".format(asunto, mensaje)
    try:
        smtp = smtplib.SMTP("localhost")
        smtp.sendmail(remitente, destinatario, email.encode("utf8"))
        print("Correo enviado")
    except:
        print(
            """Error: el mensaje no pudo enviarse. 
        Compruebe que el mensaje no tenga acentos"""
        )

def sync_status_and_agrobd_label(agrobd, catalog):
    '''
    Esta funcion actualiza los campos de estatus, id_valido, taxon_valido y
    categoria_agrobiodiversidad en la lista local si el registro `agrobd`
    tuvo un cambio de estatus en CAT. Los cambios dependen del tipo de 
    transicion que ocurrio para el estatus del registro. Ver detalles en README. 

    Recibe:
        agrobd (pandas.Series): Un registro de la lista local de agrobiodiversidad
        catalog (pandas.Series): Version de CAT Conabio del registro con mismo id que agrobd
    '''
    # sync estatus, id_valido, taxon_valido
    updateLocal(agrobd['id'], {'estatus': catalog['estatus'],
                               'id_valido': catalog['id_valido'],
                               'taxon_valido': catalog['taxon_valido']
                              })

    # sinonimo --> valido OR NA --> valido
    if agrobd['id'] == catalog['id_valido']:
        request_agrobd_review(agrobd)
    
    # valido --> NA
    elif (agrobd['id'] == agrobd['id_valido']) and (not catalog['id_valido']):
        delete_agrobd_label(agrobd) # TO DO: preguntar a CAT que hacer en este caso
    
    # sinonimo --> sinonimo
    elif is_synonym(agrobd) and is_synonym(catalog):
        if not id_is_in_agrobd_list(catalog['id_valido']):
            new_record = getInfoTaxon(catalog['id_valido'])
            add_record_to_agrobd_list(new_record)
            request_agrobd_review(new_record, check_previous_label=False)
    
    # valido --> sinonimo
    elif (agrobd['id'] == agrobd['id_valido']) and is_synonym(catalog):
        #print("valido a sinonimo",agrobd['id'])
        delete_agrobd_label(agrobd)
        if not id_is_in_agrobd_list(catalog['id_valido']):
            new_record = getInfoTaxon(catalog['id_valido']) # assumes id exists in CAT
            add_record_to_agrobd_list(new_record)
        # this is the only line that adds the agrobd label to a record
        add_agrobd_label(catalog['id_valido'], agrobd)
    

def sync_agrobd_to_catalog(agrobd_list):
    ''' Pipeline para sincronizar la lista local de agrobiodiversidad
    con el catalogo de Conabio (CAT). El script recorre la lista registro por registro;
    compara la version actual de la lista `agrobd_list` contra CAT mediante una consulta
    a zacatuche. Si cambio el estatus de un registro en CAT actualiza los campos
    y realiza los cambios necesarios en la categoria agrobiodiversidad.
    Envia un correo para advertir de ids que no estan en CAT, pues se trata
    de un error al que se le debe dar seguimiento.
    
    Recibe:
        agrobd_list(pandas.DataFrame): Tabla que contiene la version mas actual
        de la lista local de agrobd. 
    '''
    agroid_not_in_cat = []

    for i, agrobd in agrobd_list.iterrows():
        if 'pendiente' in agrobd['id']:
            continue

        catalog = getInfoTaxon(agrobd['id'])

        # case when agrobd is not in CAT
        if catalog is None:
            agroid_not_in_cat.append((agrobd['id'], agrobd['taxon']))
            continue
        
        # case when there was a change in taxonomic status
        if agrobd['id_valido'] != catalog['id_valido']:
            #print("cambia estatus",agrobd['id_valido'])
            sync_status_and_agrobd_label(agrobd, catalog)

        # case when there was a change in taxonomic name
        if agrobd['taxon'] != catalog['taxon']:
            updateLocal(agrobd['id'], {'taxon': catalog['taxon']})
    
    # format text for email
    # TO DO: add padding to align ids and taxons to fit in a table
    if len(agroid_not_in_cat) != 0:
        email = ''
        for agrobd_id, taxon in agroid_not_in_cat:

            email += f'   {agrobd_id}   |  {taxon} \n'

        sendeMail(email)


if __name__ == '__main__':
    try:
        print("Leyendo archivos...")
        agrobd_list = pd.read_csv(path_agrobd_list, keep_default_na=False)    
        print("Comparando archivos...")
        sync_agrobd_to_catalog(agrobd_list)
        print("Termina comparacion")

    except:
        print("Error al ejecutar script que compara el listado contra Zacatuche")
        destinatarios = ["Vicente <vicente.herrera@conabio.gob.mx>","Alicia <amastretta@conabio.gob.mx>","Oswaldo <oswaldo.oliveros@conabio.gob.mx>","Irma <ihernandez@conabio.gob.mx>"]
        sendWarning("estatus.py de compareZacatuche", destinatarios)