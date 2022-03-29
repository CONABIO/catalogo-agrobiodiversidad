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
path_history y path_changelog
ya que ahí se lleva el seguimiento de los registros eliminados.
'''

import functions
import paths
import pandas as pd
from datetime import datetime,timedelta,date

def compareFiles(actual,anterior,path_history,path_changelog):
    '''
    Compara los archivos actual y anterior. Sobreescribe las diferencias
    en los archivos que se pasan como parámetros en path_history y path_changelog
    '''
    header = functions.getHeader(actual)
    divisor = '-------------------------------'

    history = open(path_history,'a')
    changelog = open(path_changelog,'a')
    hours = datetime.utcnow()-datetime.now()
    hours = str(hours).split(":")

    #Busca las diferencias entre los ids actuales y los anteriores
    for i in range(len(actual.index)):
        torf = actual.id[i] in anterior.id.values
        date = functions.getDate(actual.updatedAt[i],hours[0])

        #El id del archivo actual no existe en el archivo anterior
        if(torf == False):
            #Si la fecha de creación es igual a la de modificación, entonces se agregó un nuevo registro.
            #Agrega a history el nuevo registro y a changelog el id con la bandera de "nuevo registro"
            if(actual.createdAt[i] == actual.updatedAt[i]):
                info = functions.getInfo(actual,i)

                register = header + info
                
                res = '\n#### '+str(date)+'\n\n#### Se agregó el registro '+actual.id[i]+' por el usuario '+str(actual.usuario[i])+'\n'+'\n**Registro actual:**\n\n'+register+'\n'+divisor+'\n'
                history.write(res)

                res = '| '+str(date)+' | '+str(actual.id[i])+' | Nuevo registro | - | - | - | '+ str(actual.usuario[i]) +' |\n'
                changelog.write(res)

            #Si no, se modificó el registro
            else:
                existsTaxon = actual.taxon[i] in anterior.taxon.values
                
                #Si el id no existe y el taxon si, entonces se modificó el ID
                #Agrega a hsitory la modificación del registro y a changelog los cambios en los campos de ese registro con la bandera "editar registro"
                if(existsTaxon == True):

                    modTaxon = anterior[anterior['taxon'] == actual.taxon[i]].index.values
                    modTaxon = modTaxon[0]
                    infoAct = functions.getInfo(actual,i)
                    infoAnt = functions.getInfo(anterior,modTaxon)

                    register = header + infoAct
                    previous = header + infoAnt
                    
                    res = '\n#### '+str(date)+'\n\n#### Se actualizó el registro '+actual.id[i]+' por el usuario '+str(actual.usuario[i])+'\n\n'+'**Registro actual:**\n\n'+register+'\n\n**Registro anterior:**\n\n'+previous+'\n'+divisor+'\n'
                    history.write(res)

                    for j in list(actual.columns):
                        if j == 'createdAt' or j == 'updatedAt' or j == 'usuario':
                            continue
                        
                        if str(actual[j][i]) != str(anterior[j][modTaxon]):
                            res = '| '+str(date)+' | '+str(actual.id[i])+' | Editar registro | '+j+' | '+str(anterior[j][modTaxon])+' | '+str(actual[j][i])+' | '+ str(actual.usuario[i]) +' |\n'
                            changelog.write(res)

                #Si ninguno de los dos existe, se agregó un registro y se modificó en el mismo día
                #Agrega el registro a history y el id a changelog con la bandera "nuevo registro"
                else:

                    infoAct = functions.getInfo(actual,i)

                    register = header + infoAct

                    res = '\n#### '+str(date)+'\n\n#### Se agregó el registro '+actual.id[i]+' y se actualizó en el mismo día por el usuario '+str(actual.usuario[i])+'\n'+'\n**Registro actual:**\n\n'+register+'\n'+divisor+'\n'
                    history.write(res)

                    res = '| '+str(date)+' | '+str(actual.id[i])+' | Nuevo registro | - | - | - | '+ str(actual.usuario[i]) +' |\n'
                    changelog.write(res)

        if(torf == True):
            #El id del archivo actual existe en el archivo anterior
            modTaxon = anterior[anterior['id'] == actual.id[i]].index.values
            modTaxon = modTaxon[0]
            if(actual.createdAt[i] == actual.updatedAt[i]):
                res = "No hubo cambios"
            if(actual.updatedAt[i] == anterior.updatedAt[modTaxon]):
                res = "No hubo cambios"

            #Se actualizó el registro
            #Agrega a hsitory la modificación del registro y a changelog los cambios en los campos de ese registro con la bandera "editar registro"
            if(actual.createdAt[i] != actual.updatedAt[i] and actual.updatedAt[i] != anterior.updatedAt[modTaxon]):
                modTaxon = anterior[anterior['id']==actual.id[i]].index.values
                modTaxon = modTaxon[0]
                infoAnt = functions.getInfo(anterior,modTaxon)
                infoAct = functions.getInfo(actual,i)
                previous = header + infoAnt
                register = header + infoAct
                
                res = '\n#### '+str(date)+'\n\n#### Se actualizó el registro '+str(actual.id[i])+' por el usuario '+str(actual.usuario[i])+'\n'+'\n**Registro actual:**\n'+'\n'+register+'\n\n**Registro anterior:** \n\n'+previous+'\n'+divisor+'\n'
                history.write(res)

                for j in list(actual.columns):

                    if j == 'createdAt' or j == 'updatedAt' or j == 'usuario':
                        continue
                    
                    if str(actual[j][i]) != str(anterior[j][modTaxon]):
                        res = '| '+str(date)+' | '+str(actual.id[i])+' | Editar registro | '+j+' | '+str(anterior[j][modTaxon])+' | '+str(actual[j][i])+' | '+ str(actual.usuario[i]) +' |\n'
                        changelog.write(res)

    history.close()
    changelog.close()

def main():
    print("Leyendo archivos...")
    actual = pd.read_csv('agro_actual.csv')
    anterior = pd.read_csv('agro_anterior.csv')
    print("Comparando archivos...")
    compareFiles(actual,anterior,paths.path_history,paths.path_changelog)
    print("Termina comparación de archivos")
main()