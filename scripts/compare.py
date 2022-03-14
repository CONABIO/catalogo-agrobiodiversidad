import pandas as pd
import numpy as np
from datetime import datetime

df1 = pd.read_csv('agro_actual.csv')
df2 = pd.read_csv('agro_anterior.csv')

array1 = np.array(df1) 
array2 = np.array(df2)

df_CSV_1 = pd.DataFrame(array1, columns=['id','createdAt','updatedAt','taxon','referencia','categoria_agrobiodiversidad','subcategoria_agrobiodiversidad','justificacion_subcategoria','comentarios_revision'])
df_CSV_2 = pd.DataFrame(array2, columns=['id','createdAt','updatedAt','taxon','referencia','categoria_agrobiodiversidad','subcategoria_agrobiodiversidad','justificacion_subcategoria','comentarios_revision'])

f = open ('history.txt','a')

#Busca las diferencias entre los ids actuales y los anteriores
for i in range(len(df_CSV_1.index)):
    torf=df_CSV_1.id[i] in df_CSV_2.id.values
    if(torf==False):
        if(df_CSV_1.createdAt[i]==df_CSV_1.updatedAt[i]):
            #print("Se agregó un nuevo registro")
            actual=str(df_CSV_1.id[i])+' | '+str(df_CSV_1.taxon[i])+' | '+str(df_CSV_1.referencia[i])+' | '+str(df_CSV_1.categoria_agrobiodiversidad[i])+' | '+str(df_CSV_1.subcategoria_agrobiodiversidad[i])+' | '+str(df_CSV_1.justificacion_subcategoria[i])+' | '+str(df_CSV_1.comentarios_revision[i])
            actual=df_CSV_1.columns[0]+' | '+df_CSV_1.columns[3]+' | '+df_CSV_1.columns[4]+' | '+df_CSV_1.columns[5]+' | '+df_CSV_1.columns[6]+' | '+df_CSV_1.columns[7]+' | '+df_CSV_1.columns[8]+'\n'+actual
            res=df_CSV_1.updatedAt[i]+'\nSe agregó el registro '+df_CSV_1.id[i]+'\n'+'\nRegistro actual:\n'+actual+'\n'+'-------------------------------'+'\n'
            f.write(res)

        else:
            existsTaxon=df_CSV_1.taxon[i] in df_CSV_2.taxon.values
            if(existsTaxon==True):
                modTaxon=df_CSV_2[df_CSV_2['taxon']==df_CSV_1.taxon[i]].index.values
                modTaxon=modTaxon[0]
                #print("Se actualizó el taxon ID")
                actual=str(df_CSV_1.id[i])+' | '+str(df_CSV_1.taxon[i])+' | '+str(df_CSV_1.referencia[i])+' | '+str(df_CSV_1.categoria_agrobiodiversidad[i])+' | '+str(df_CSV_1.subcategoria_agrobiodiversidad[i])+' | '+str(df_CSV_1.justificacion_subcategoria[i])+' | '+str(df_CSV_1.comentarios_revision[i])
                actual=df_CSV_1.columns[0]+' | '+df_CSV_1.columns[3]+' | '+df_CSV_1.columns[4]+' | '+df_CSV_1.columns[5]+' | '+df_CSV_1.columns[6]+' | '+df_CSV_1.columns[7]+' | '+df_CSV_1.columns[8]+'\n'+actual
                anterior=str(df_CSV_2.id[modTaxon])+' | '+str(df_CSV_2.taxon[modTaxon])+' | '+str(df_CSV_2.referencia[modTaxon])+' | '+str(df_CSV_2.categoria_agrobiodiversidad[modTaxon])+' | '+str(df_CSV_2.subcategoria_agrobiodiversidad[modTaxon])+' | '+str(df_CSV_2.justificacion_subcategoria[modTaxon])+' | '+str(df_CSV_2.comentarios_revision[modTaxon])
                res=df_CSV_1.updatedAt[i]+'\nSe actualizó el registro '+df_CSV_1.id[i]+'\n'+'Registro actual:\n'+actual+'\nRegistro anterior:\n'+anterior+'\n-------------------------------'+'\n'
                f.write(res)
            else:
                #print("Se actualizó el registro. Caso de que se agregue un registro y el mismo día se modifique")
                actual=str(df_CSV_1.id[i])+' | '+str(df_CSV_1.taxon[i])+' | '+str(df_CSV_1.referencia[i])+' | '+str(df_CSV_1.categoria_agrobiodiversidad[i])+' | '+str(df_CSV_1.subcategoria_agrobiodiversidad[i])+' | '+str(df_CSV_1.justificacion_subcategoria[i])+' | '+str(df_CSV_1.comentarios_revision[i])
                actual=df_CSV_1.columns[0]+' | '+df_CSV_1.columns[3]+' | '+df_CSV_1.columns[4]+' | '+df_CSV_1.columns[5]+' | '+df_CSV_1.columns[6]+' | '+df_CSV_1.columns[7]+' | '+df_CSV_1.columns[8]+'\n'+actual
                res=df_CSV_1.updatedAt[i]+'\nSe agregó el registro '+df_CSV_1.id[i]+' y se actualizó en el mismo día.\n'+'\nRegistro actual:\n'+actual+'\n'+'-------------------------------'+'\n'
                f.write(res)
    if(torf==True):
        modTaxon=df_CSV_2[df_CSV_2['id']==df_CSV_1.id[i]].index.values
        modTaxon=modTaxon[0]
        if(df_CSV_1.createdAt[i]==df_CSV_1.updatedAt[i]):
            res="No hubo cambios"
        if(df_CSV_1.updatedAt[i]==df_CSV_2.updatedAt[modTaxon]):
            res="No hubo cambios"
        if(df_CSV_1.createdAt[i]!=df_CSV_1.updatedAt[i] and df_CSV_1.updatedAt[i]!=df_CSV_2.updatedAt[modTaxon]):
            modTaxon=df_CSV_2[df_CSV_2['id']==df_CSV_1.id[i]].index.values
            modTaxon=modTaxon[0]
            anterior=df_CSV_1.columns[0]+' | '+df_CSV_1.columns[3]+' | '+df_CSV_1.columns[4]+' | '+df_CSV_1.columns[5]+' | '+df_CSV_1.columns[6]+' | '+df_CSV_1.columns[7]+' | '+df_CSV_1.columns[8]+'\n'+str(df_CSV_2.id[modTaxon])+' | '+str(df_CSV_2.taxon[modTaxon])+' | '+str(df_CSV_2.referencia[modTaxon])+' | '+str(df_CSV_2.categoria_agrobiodiversidad[modTaxon])+' | '+str(df_CSV_2.subcategoria_agrobiodiversidad[modTaxon])+' | '+str(df_CSV_2.justificacion_subcategoria[modTaxon])+' | '+str(df_CSV_2.comentarios_revision[modTaxon])
            actual=str(df_CSV_1.id[i])+' | '+str(df_CSV_1.taxon[i])+' | '+str(df_CSV_1.referencia[i])+' | '+str(df_CSV_1.categoria_agrobiodiversidad[i])+' | '+str(df_CSV_1.subcategoria_agrobiodiversidad[i])+' | '+str(df_CSV_1.justificacion_subcategoria[i])+' | '+str(df_CSV_1.comentarios_revision[i])
            actual=df_CSV_1.columns[0]+' | '+df_CSV_1.columns[3]+' | '+df_CSV_1.columns[4]+' | '+df_CSV_1.columns[5]+' | '+df_CSV_1.columns[6]+' | '+df_CSV_1.columns[7]+' | '+df_CSV_1.columns[8]+'\n'+actual
            res=df_CSV_1.updatedAt[i]+'\nSe actualizó el registro '+df_CSV_1.id[i]+'\n'+'\nRegistro actual:'+'\n'+actual+'\n\nRegistro anterior: \n'+anterior+'\n-------------------------------'+'\n'
            f.write(res)

#Busca las diferencias entre los ids anteriores y los actuales
now = datetime.now()

for i in range(len(df_CSV_2.index)):
    res=df_CSV_2.id[i] in df_CSV_1.id.values
    if(res==False):
        #print("Se elminó el registro")
        anterior=df_CSV_2.columns[0]+' | '+df_CSV_2.columns[3]+' | '+df_CSV_2.columns[4]+' | '+df_CSV_2.columns[5]+' | '+df_CSV_2.columns[6]+' | '+df_CSV_2.columns[7]+' | '+df_CSV_2.columns[8]+'\n'+str(df_CSV_2.id[i])+' | '+str(df_CSV_2.taxon[i])+' | '+str(df_CSV_2.referencia[i])+' | '+str(df_CSV_2.categoria_agrobiodiversidad[i])+' | '+str(df_CSV_2.subcategoria_agrobiodiversidad[i])+' | '+str(df_CSV_2.justificacion_subcategoria[i])+' | '+str(df_CSV_2.comentarios_revision[i])
        res=now.strftime("%d/%m/%Y")+'\nSe eliminó el registro '+df_CSV_2.id[i]+'\n'+'\nRegistro anterior: \n'+anterior+'\n-------------------------------'+'\n'
        f.write(res)





f.close()
