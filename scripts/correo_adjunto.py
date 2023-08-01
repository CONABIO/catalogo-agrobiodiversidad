import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

def mailAdjunto():
    # Iniciamos los parámetros del script
    remitente = 'siagro@siagro.conabio.gob.mx'
    destinatarios = ["Alicia <amastretta@conabio.gob.mx>","Oswaldo <oswaldo.oliveros@conabio.gob.mx>","Irma <ihernandez@conabio.gob.mx>"]
    asunto = 'Revisar etiquetas con Oswa y Mao'
    cuerpo = """Verifica si en los logs hay sinonimos con etiquetas que necesiten revisarse con Oswa y Mao.

Para mas informacion sobre el script check_sinonimos.py favor de revisar https://github.com/CONABIO/catalogo-agrobiodiversidad/tree/main#revisi%C3%B3n-de-taxones-marcados-como-sin%C3%B3nimos, o bien la seccion de monitoreo - Listado de agrobiodiversidad - Revision de taxones marcados como sinonimos, en la ruta J/USUARIOS/CARB/SIAgroBD/documentacion_servidores/documentacion.pdf
        
------------------------------------
Este correo no contiene acentos y ha sido enviado automaticamente. Favor de no responder."""
    ruta_adjunto = 'scripts/check_sinonimos.txt'
    nombre_adjunto = 'check_sinonimos.txt'

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


if __name__ == '__main__':
    mailAdjunto()


    