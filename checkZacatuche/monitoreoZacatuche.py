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
                searchTaxon(q:"isAgrobiodiversity:true" first:5){      
                edges{
                    node{
                    id,
                    acceptedNameUsage{
                        scientificName
                    }
                    appendixCITES
                    establishmentMeans{
                        region
                    }
                    isFreshWater
                    isMarine
                    isTerrestial
                    lifeform
                    nameAccordingTo
                    scientificNameAuthorship
                    taxonRankSort
                    threatStatus
                    vernacularNames{
                        language
                        region
                        vernacularName
                    }
                    taxon: scientificName,
                    categoria: taxonRank,
                    higherClassification{
                        edges{
                        node{
                            id
                            scientificName
                            taxonRank
                        }
                        }
                    }
                    estatus:taxonomicStatus,
                    fuente:nameAccordingTo,
                    nombre_autoridad:scientificNameAuthorship,
                    cites:appendixCITES,
                    iucn:threatStatus,
                    agrobiodiversityInfo{
                        es_parientesilvestre,
                        es_domesticado,
                        es_quelite
                    }
                    }
                    }
                }
                }"""

try:
    r = requests.post(path_zacatuche, json={"query": queryOc})
    #print(path_zacatuche)
    json_data = r.json()
    code = r.status_code
    response_json_len = len(json_data["data"]["searchOccurrence"]["edges"])
    #print(response_json_len)
    if code != 200:
        msg = f"EXISTE UN ERROR EN EL SERVIDOR. CODIGO DE ERROR: {code}"
        destinatarios = [
            "Vivian <vbass@conabio.gob.mx>",
            "Juan <jbarrios@conabio.gob.mx>",
            "Vivian <vivbass4@gmail.com"
        ]
        sendeMail(msg, destinatarios)

    if response_json_len == 0:
        msg = (
            f"NO SE OBTUVIERON RESULTADOS DE LA CONSULTA. LA CONSULTA QUE "
            f"SE REALIZO ES \n {queryOc}"
        )
        destinatarios = [
            "Vivian <vbass@conabio.gob.mx>",
            "Juan <jbarrios@conabio.gob.mx>",
            "Vivian <vivbass4@gmail.com"
        ]
        sendeMail(msg, destinatarios)

    if response_json_len > 0:
        string = (
            f"Todo esta bien, se encontraron {response_json_len} registros "
            f"en la consulta."
        )
        destinatarios = ["Vivian <vbass@conabio.gob.mx>", "Vivian <vivbass4@gmail.com"]
        sendeMail(string, destinatarios)

except requests.ConnectionError:
    msg = f"EXISTE UN ERROR DE CONEXION CON ZACATUCHE. EL SERVIDOR NO CONTESTA"
    destinatarios = ["Vivian <vbass@conabio.gob.mx>", "Juan <jbarrios@conabio.gob.mx>", "Vivian <vivbass4@gmail.com"]
    sendeMail(msg, destinatarios)
