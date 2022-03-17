'''
Este programa realiza la comparación de 2 archivos csv 
(lo que hay en la instancia el día de hoy contra lo que
había en la instancia el día de ayer) y sobreescribe 2 archivos .md:
* El primero (history.md) contiene el histórico a detalle de todos 
  los cambios que se realizan en la instancia.
* El segundo (changelog.md) contiene el resumen de esos cambios.
Este script sólo detecta las diferencias si se agrega un registro o
se modifica un registro. 
La eliminación de registros se lleva a cabo directamente en el script 
que realiza el delete. Por esa razón se utilizan los archivos
<> y
<>
ya que ahí se lleva el seguimiento de los registros eliminados.
'''

import pandas as pd
import numpy as np
from datetime import datetime,timedelta

def readFile(filename):
    '''
    Lee archivo csv y devuelve un dataframe
    '''
    df = pd.read_csv(filename)
    return df


def getDate(date):
    '''
    Convierte la fecha de la base de datos de zendro a nuestra zona horaria
    '''
    date = date.split(".")
    date = datetime.strptime(date[0], "%Y-%m-%d %H:%M:%S" )
    date = date-timedelta(hours = 6)
    date = str(date.year) + '-'+ str(date.month) + '-'+ str(date.day)
    return date


def getHeader(df):
    '''
    Obtiene el header para el history.md dependiendo el dataframe que se reciba.
    Se eliminan las columnas createdAt y updatedAt y se devuelve el header completo de la tabla.    
    '''
    header = ' | '.join(df.columns)
    header = '| '+header+' |'
    header = header.replace("| createdAt ","")
    header = header.replace("| updatedAt ","")

    separator = '| -- |'
    for i in range(len(df.columns)-3):
        separator = separator + ' -- |'

    header = header + '\n' + separator + '\n'

    return header 


def compareFiles(df_CSV_1,df_CSV_2,path_history,path_changelog):
    '''
    Compara los archivos df_CSV_1 y df_CSV_2. Sobreescribe las diferencias
    en los archivos que se pasan como parámetros en path_history y path_changelog
    '''
    header = getHeader(df_CSV_1)
    divisor = '-------------------------------'

    history = open(path_history,'a')
    changelog = open(path_changelog,'a')

    #Busca las diferencias entre los ids actuales y los anteriores
    for i in range(len(df_CSV_1.index)):
        torf = df_CSV_1.id[i] in df_CSV_2.id.values
        date = getDate(df_CSV_1.updatedAt[i])

        #El id del archivo actual no existe en el archivo anterior
        if(torf == False):
            #Si la fecha de creación es igual a la de modificación, entonces se agregó un nuevo registro
            if(df_CSV_1.createdAt[i] == df_CSV_1.updatedAt[i]):
                actual = header + '| '+str(df_CSV_1.id[i])+' | '+str(df_CSV_1.taxon[i])+' | '+str(df_CSV_1.estatus[i])+' | '+str(df_CSV_1.id_valido[i])+' | '+str(df_CSV_1.taxon_valido[i])+' | '+str(df_CSV_1.referencia[i])+' | '+str(df_CSV_1.categoria_agrobiodiversidad[i])+' | '+str(df_CSV_1.subcategoria_agrobiodiversidad[i])+' | '+str(df_CSV_1.justificacion_subcategoria[i])+' | '+str(df_CSV_1.comentarios_revision[i])+' | '+str(df_CSV_1.usuario[i])+' | '
                
                res = '\n#### '+str(date)+'\n\n#### Se agregó el registro '+df_CSV_1.id[i]+' por el usuario '+str(df_CSV_1.usuario[i])+'\n'+'\n**Registro actual:**\n\n'+actual+'\n'+divisor+'\n'
                history.write(res)

                res = '| '+str(date)+' | '+str(df_CSV_1.id[i])+' | Nuevo registro | - | - | - | '+ str(df_CSV_1.usuario[i]) +' |\n'
                changelog.write(res)

            #Si no, se modificó el registro
            else:
                existsTaxon = df_CSV_1.taxon[i] in df_CSV_2.taxon.values
                
                #Si el id no existe y el taxon si, entonces se modificó el ID
                if(existsTaxon == True):
                    modTaxon = df_CSV_2[df_CSV_2['taxon'] == df_CSV_1.taxon[i]].index.values
                    modTaxon = modTaxon[0]
                    actual = header + '| '+str(df_CSV_1.id[i])+' | '+str(df_CSV_1.taxon[i])+' | '+str(df_CSV_1.estatus[i])+' | '+str(df_CSV_1.id_valido[i])+' | '+str(df_CSV_1.taxon_valido[i])+' | '+str(df_CSV_1.referencia[i])+' | '+str(df_CSV_1.categoria_agrobiodiversidad[i])+' | '+str(df_CSV_1.subcategoria_agrobiodiversidad[i])+' | '+str(df_CSV_1.justificacion_subcategoria[i])+' | '+str(df_CSV_1.comentarios_revision[i])+' | '+str(df_CSV_1.usuario[i])+' | '
                    previous = header + '| '+str(df_CSV_2.id[modTaxon])+' | '+str(df_CSV_2.taxon[modTaxon])+' | '+str(df_CSV_2.estatus[modTaxon])+' | '+str(df_CSV_2.id_valido[modTaxon])+' | '+str(df_CSV_2.taxon_valido[modTaxon])+' | '+str(df_CSV_2.referencia[modTaxon])+' | '+str(df_CSV_2.categoria_agrobiodiversidad[modTaxon])+' | '+str(df_CSV_2.subcategoria_agrobiodiversidad[modTaxon])+' | '+str(df_CSV_2.justificacion_subcategoria[modTaxon])+' | '+str(df_CSV_2.comentarios_revision[modTaxon])+' | '+str(df_CSV_2.usuario[modTaxon])+' | '
                    
                    res = '\n#### '+str(date)+'\n\n#### Se actualizó el registro '+df_CSV_1.id[i]+' por el usuario '+str(df_CSV_1.usuario[i])+'\n\n'+'**Registro actual:**\n\n'+actual+'\n\n**Registro anterior:**\n\n'+previous+'\n'+divisor+'\n'
                    history.write(res)
                #Si ninguno de los dos existe, se agregó un registro y se modificó en el mismo día
                else:
                    actual = header + '| '+str(df_CSV_1.id[i])+' | '+str(df_CSV_1.taxon[i])+' | '+str(df_CSV_1.estatus[i])+' | '+str(df_CSV_1.id_valido[i])+' | '+str(df_CSV_1.taxon_valido[i])+' | '+str(df_CSV_1.referencia[i])+' | '+str(df_CSV_1.categoria_agrobiodiversidad[i])+' | '+str(df_CSV_1.subcategoria_agrobiodiversidad[i])+' | '+str(df_CSV_1.justificacion_subcategoria[i])+' | '+str(df_CSV_1.comentarios_revision[i]) + ' | '+str(df_CSV_1.usuario[i]) + ' | '

                    res = '\n#### '+str(date)+'\n\n#### Se agregó el registro '+df_CSV_1.id[i]+' y se actualizó en el mismo día por el usuario '+str(df_CSV_1.usuario[i])+'\n'+'\n**Registro actual:**\n\n'+actual+'\n'+divisor+'\n'
                    history.write(res)

                    res = '| '+str(date)+' | '+str(df_CSV_1.id[i])+' | Nuevo registro | - | - | - | '+ str(df_CSV_1.usuario[i]) +' |\n'
                    changelog.write(res)

        if(torf == True):
            #El id del archivo actual existe en el archivo anterior
            modTaxon = df_CSV_2[df_CSV_2['id'] == df_CSV_1.id[i]].index.values
            modTaxon = modTaxon[0]
            if(df_CSV_1.createdAt[i] == df_CSV_1.updatedAt[i]):
                res = "No hubo cambios"
            if(df_CSV_1.updatedAt[i] == df_CSV_2.updatedAt[modTaxon]):
                res = "No hubo cambios"
            if(df_CSV_1.createdAt[i] != df_CSV_1.updatedAt[i] and df_CSV_1.updatedAt[i] != df_CSV_2.updatedAt[modTaxon]):
                #Se actualizó el registro
                modTaxon = df_CSV_2[df_CSV_2['id']==df_CSV_1.id[i]].index.values
                modTaxon = modTaxon[0]
                previous = header+'| '+str(df_CSV_2.id[modTaxon])+' | '+str(df_CSV_2.taxon[modTaxon])+' | '+str(df_CSV_2.estatus[modTaxon])+' | '+str(df_CSV_2.id_valido[modTaxon])+' | '+str(df_CSV_2.taxon_valido[modTaxon])+' | '+str(df_CSV_2.referencia[modTaxon])+' | '+str(df_CSV_2.categoria_agrobiodiversidad[modTaxon])+' | '+str(df_CSV_2.subcategoria_agrobiodiversidad[modTaxon])+' | '+str(df_CSV_2.justificacion_subcategoria[modTaxon])+' | '+str(df_CSV_2.comentarios_revision[modTaxon])+' | '+str(df_CSV_2.usuario[modTaxon])+' | '
                actual = header+'| '+str(df_CSV_1.id[i])+' | '+str(df_CSV_1.taxon[i])+' | '+str(df_CSV_1.estatus[i])+' | '+str(df_CSV_1.id_valido[i])+' | '+str(df_CSV_1.taxon_valido[i])+' | '+str(df_CSV_1.referencia[i])+' | '+str(df_CSV_1.categoria_agrobiodiversidad[i])+' | '+str(df_CSV_1.subcategoria_agrobiodiversidad[i])+' | '+str(df_CSV_1.justificacion_subcategoria[i])+' | '+str(df_CSV_1.comentarios_revision[i])+' | '+str(df_CSV_1.usuario[i]) + ' | '
                
                res = '\n#### '+str(date)+'\n\n#### Se actualizó el registro '+df_CSV_1.id[i]+' por el usuario '+str(df_CSV_1.usuario[i])+'\n'+'\n**Registro actual:**\n'+'\n'+actual+'\n\n**Registro anterior:** \n\n'+previous+'\n'+divisor+'\n'
                history.write(res)

                for j in list(df_CSV_1.columns):
                    if j == 'createdAt' or j == 'updatedAt' or j == 'usuario':
                        continue
                    
                    if str(df_CSV_1[j][i]) != str(df_CSV_2[j][modTaxon]):
                        res = '| '+str(date)+' | '+str(df_CSV_1.id[i])+' | Editar registro | '+j+' | '+str(df_CSV_2[j][modTaxon])+' | '+str(df_CSV_1[j][i])+' | '+ str(df_CSV_1.usuario[i]) +' |\n'
                        changelog.write(res)

    history.close()
    changelog.close()

def main():
    print("Leyendo archivos...")
    df_CSV_1 = readFile('agro_actual.csv')
    df_CSV_2 = readFile('agro_anterior.csv')
    print("Comparando archivos...")
    compareFiles(df_CSV_1,df_CSV_2,'<filename1>','<filename2>')
    print("Termina comparación de archivos")


main()