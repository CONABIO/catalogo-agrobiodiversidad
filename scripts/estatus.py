'''
Este programa realiza la comparación de lo que hay en nuestra base de datos
contra lo que hay en Zacatuche.
Si encuentra cambios entre las dos bases realiza los respectivos cambios
en nuestra base directamente.
Si por alguna razón tenemos un ID que no se encuentre en Zacatuche
manda un correo a Alicia, Irene y Vivian para dar seguimiento.
Los logs del script se encuentran en logEstatus.txt
'''

import functions
import numpy as np
import pandas as pd

def compareRows(agro_actual):
    #Revisa línea por línea del csv
    for i in range(len(agro_actual.index)):

        #Query a Zacatuche
        df_data = functions.getInfoTaxon(agro_actual.id[i])
        
        #Existe ID en zacatuche?
        #Si sí, sigue validando, si no, manda un correo a Alicia, Irene y Vivian para hacer seguimiento.
        if df_data!=None:
            if df_data['acceptedNameUsage']==None:
                print(agro_actual.id[i])
            #Cambia el estatus?
            #Si sí, sigue validando, si no, se verifica que el nombre del taxon sea igual.
            if str(agro_actual.estatus[i]) != str(df_data['taxonomicStatus']):
                if str(df_data['taxonomicStatus'])!='Sinónimo':
                    #Cambia a válido
                    #Cambia en la base el estatus, el id válido, el taxón válido y la categoria_agrobiodiversidad = Agrobiodiversidad
                    functions.updateLocal(id=str(agro_actual.id[i]),estatus=str(df_data['taxonomicStatus']), id_valido=str(df_data['acceptedNameUsage']['id']),taxon_valido=str(df_data['acceptedNameUsage']['scientificName']),categoria_agrobiodiversidad="Agrobiodiversidad")
                    
                else:
                    #Cambia a sinónimo
                    #Si el registro no tiene taxon id válido relacionado sólo actualiza estatus y categoria_agrobiodiversidad=NULL
                    if(df_data['acceptedNameUsage']==None):
                        functions.updateLocal(id=str(agro_actual.id[i]),estatus=str(df_data['taxonomicStatus']), categoria_agrobiodiversidad="NULL")
                    
                    #Si sí tiene taxon id valido relacionado y el taxon existe en nuestra base, se actualiza su estatus, id_valido, taxon_valido y categoria_agrobiodiversidad=NULL del taxon que se está revisando. 
                    #Si el taxon no existe en nuestra base, se agrega.
                    else:

                        exists = df_data['acceptedNameUsage']['id'] in agro_actual.id.values
                        if exists:
                            functions.updateLocal(id=str(agro_actual.id[i]),estatus=str(df_data['taxonomicStatus']), id_valido=str(df_data['acceptedNameUsage']['id']),taxon_valido=str(df_data['acceptedNameUsage']['scientificName']),categoria_agrobiodiversidad="NULL")

                        else:
                            df_data_new = functions.getInfoTaxon(str(df_data['acceptedNameUsage']['id']))
                            functions.addLocal(id=str(df_data_new['id']),taxon=str(df_data_new['scientificName']),estatus=str(df_data_new['taxonomicStatus']),id_valido=str(df_data_new['id']),taxon_valido=str(df_data_new['scientificName']),categoria_agrobiodiversidad="Agrobiodiversidad")
                

            #Cambió el scientificName?
            if df_data['scientificName'] != agro_actual['taxon'][i]:
                functions.updateLocal(id=str(agro_actual.id[i]),taxon=str(df_data['scientificName']))

        else:
            print("ID no existe en Zacatuche --- mandar correo",agro_actual.id[i])
            #functions.sendeMail(agro_actual.id[i])


def main():
    print("Leyendo archivos...")
    agro_actual =  pd.read_csv('comparaZacatuche.csv')
    print("Comparando archivos...")
    compareRows(agro_actual)
    print("Termina comparación de archivos")


main()
