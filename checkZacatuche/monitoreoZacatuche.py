import requests
import smtplib
from paths import path_zacatuche


def sendeMail(string, destinatario):
    """
    Envía un correo a las direcciones en "destinatario".
    """
    remitente = "SIAgro <siagro@siagro.conabio.gob.mx>"
    asunto = "Monitoreo Zacatuche"
    mensaje = (
        string
        + """
    
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


queryOc = """query searchOccurrence{
        searchOccurrence(q:"projectID:(FY001 OR FZ001 OR FZ002 OR FZ003 OR FZ007 OR FZ014 OR FZ015 OR FZ016 OR FZ018 OR FZ023 OR Z003 OR Z004 OR Z005 OR Z006 OR NM003 OR NM002)"){
                    edges{
                    node{
                        id
                        proyecto: projectId
                        procedencia: basisOfRecord
                        fecha_colecta_observacion: eventDate
                        numero_colecta_observacion: recordNumber
                        colector_observador: recordedBy
                        coleccion: collectionCode
                        numero_catalogo: catalogNumber
                        individuos_copias: individualCount
                        preparacion: preparations
                        sexo: sex
                        fecha_determinacion: dateIdentified
                        determinador: identifiedBy
                        calificador_determinacion: identificationQualifier
                        determinacion_tipo: typeStatus
                        licencia_uso: license
                        referencias: references
                        forma_citar: bibliographicCitation
                        autorizacion_informacion: accessRights
                        taxon{
                            taxon_id: id
                        }
                    }
                    cursor
                }
                pageInfo{
                    endCursor
                    hasNextPage
                }
                }
            }"""

queryTaxon = """query searchTaxon{
                    searchTaxon(q:"id:(1057FUNGI OR 13375MOLUS OR 135278AVES OR  14345ANGIO OR 1630LEPID OR 18214ANGIO OR 18435ANGIO OR 19204ANGIO OR 19210ANGIO OR 19216ANGIO OR 19549MAMIF OR 20104PECES OR 20142HEMIP OR 20318HEMIP OR 20333HEMIP OR 20341HEMIP OR 2204FUNGI OR 222854DIPTE OR 227909DIPTE OR 2539FUNGI OR 26213ANGIO OR 2664FUNGI OR 26895ANGIO OR 26919ANGIO OR 2723FUNGI OR 27376ANGIO OR 27770ANGIO OR 2813FUNGI OR 29438ANGIO OR 32455HYMEN OR 3315FUNGI OR 33251ANGIO OR 33255ANGIO OR 33901HYMEN OR 33940HYMEN OR 33941HYMEN OR 33963HYMEN OR 34473ANGIO OR 35039ANGIO OR 35136ANGIO OR 35797ANGIO OR 35997ANGIO OR 36197ANGIO OR 36260ANGIO OR 36262ANGIO OR 36330ANGIO OR 36748ANGIO OR 37909ANGIO OR 38025ANGIO OR 3889ANGIO OR 40309ANGIO OR 42021ANGIO OR 42022ANGIO OR 43526ANGIO OR 45226COLEO OR 46977HYMEN OR 47139ANGIO OR 49164ANGIO OR 51124ANGIO OR 52326ANGIO OR 52575ANGIO OR 52576ANGIO OR 53190ANGIO OR 5593LEPID OR 57733ORTHO OR 57861ORTHO OR 58086ORTHO OR 58235ANGIO OR 58855ORTHO OR 6074PECES OR 60800HEMIP OR 60806HEMIP OR 60807HEMIP OR 60811ANGIO OR 60968ANGIO OR 61070LEPID OR 6211PECES OR 6222PECES OR 6278PECES OR 6297PECES OR 6461PECES OR 6642PECES OR 6682PECES OR 6708PECES OR 7622PECES OR 7629PECES OR 8076ANGIO OR 8117PECES OR 8292PECES OR 8339PECES OR 8453PECES OR 9192ANGIO)" first:500 ){ 
                    totalCount           
                    edges{
                    node{
                        id,
                        taxon: scientificName,
                        categoria: taxonRank,
                        estatus:taxonomicStatus,
                        fuente:nameAccordingTo,
                        nombre_autoridad:scientificNameAuthorship,
                        cites:appendixCITES,
                        iucn:threatStatus
                    }
                        cursor
                    }
                    pageInfo{
                        endCursor
                        hasNextPage
                    }
                    }
                }"""

try:
    r = requests.post(path_zacatuche, json={"query": queryOc}, timeout=10)

    #print(path_zacatuche)
    json_data = r.json()
    code = r.status_code
    response_json_len = len(json_data["data"]["searchOccurrence"]["edges"])
    #print(response_json_len)
    if code != 200:
        msg = f"EXISTE UN ERROR EN EL SERVIDOR. CODIGO DE ERROR: {code}"
        destinatarios = [
            "Vivian <vbass@conabio.gob.mx>",
            "Juan <jbarrios@conabio.gob.mx>"
        ]
        print(msg)
        sendeMail(msg, destinatarios)

    if response_json_len == 0:
        msg = (
            f"NO SE OBTUVIERON RESULTADOS DE LA CONSULTA. LA CONSULTA QUE "
            f"SE REALIZO ES \n {queryOc}"
        )
        destinatarios = [
            "Vivian <vbass@conabio.gob.mx>",
            "Juan <jbarrios@conabio.gob.mx>"
        ]
        print(msg)
        sendeMail(msg, destinatarios)

    if response_json_len > 0:
        string = (
            f"Todo esta bien, se encontraron {response_json_len} registros "
            f"en la consulta."
        )
        destinatarios = ["Vivian <vbass@conabio.gob.mx>"]
        print(string)
        sendeMail(string, destinatarios)

except requests.Timeout as err:
    #print("ERROR TIMEOUT:",err)
    try:
        r = requests.post(path_zacatuche, json={"query": queryTaxon}, timeout=10)

        #print(path_zacatuche)
        json_data = r.json()
        code = r.status_code
        response_json_len = len(json_data["data"]["searchTaxon"]["edges"])
        #print(response_json_len)
        if code != 200:
            msg = f"EXISTE UN ERROR EN EL SERVIDOR. CODIGO DE ERROR: {code}"
            destinatarios = ["Vivian <vbass@conabio.gob.mx>", "Juan <jbarrios@conabio.gob.mx>"]
            print(msg)
            sendeMail(msg, destinatarios)

        if response_json_len == 0:
            msg = (
                f"NO SE OBTUVIERON RESULTADOS DE LA CONSULTA. LA CONSULTA QUE "
                f"SE REALIZO ES \n {queryTaxon}"
            )
            destinatarios = ["Vivian <vbass@conabio.gob.mx>", "Juan <jbarrios@conabio.gob.mx>"]
            print(msg)
            sendeMail(msg, destinatarios)

        if response_json_len > 0:
            string = (
                f"LAS CONSULTAS DE OCCURRENCE NO RESPONDEN PERO LAS DE TAXON SI RESPONDEN."
               
            )
            destinatarios = ["Vivian <vbass@conabio.gob.mx>", "Juan <jbarrios@conabio.gob.mx>"]            
            print(string)
            sendeMail(string, destinatarios)

    except requests.Timeout as err:
        msg = f"ZACATUCHE ESTA TARDANDO MAS DE 10 SEGUNDOS EN RESPONDER LAS PETICIONES TANTO DE OCCURRENCE COMO DE TAXON"
        destinatarios = ["Vivian <vbass@conabio.gob.mx>", "Juan <jbarrios@conabio.gob.mx>"]        
        print(msg)
        sendeMail(msg, destinatarios)

    except requests.ConnectionError:
        msg = f"EXISTE UN ERROR DE CONEXION CON ZACATUCHE AL INTENTAR HACER UNA QUERY EN TAXON. EL SERVIDOR NO CONTESTA"
        destinatarios = ["Vivian <vbass@conabio.gob.mx>", "Juan <jbarrios@conabio.gob.mx>"]
        print(msg)
        sendeMail(msg, destinatarios)


except requests.ConnectionError:
    msg = f"EXISTE UN ERROR DE CONEXION CON ZACATUCHE. EL SERVIDOR NO CONTESTA"
    destinatarios = ["Vivian <vbass@conabio.gob.mx>", "Juan <jbarrios@conabio.gob.mx>"]
    print(msg)
    sendeMail(msg, destinatarios)
