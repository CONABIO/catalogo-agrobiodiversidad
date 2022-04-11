
'''
Este script compara el archivo `anterior.csv` contra `actual.csv`.
Ambos archivos csv contienen las mismas columnas. 
Los ids de los registros (columna `id`) en cada csv son únicos.

El script identifica los registros borrados, agregados y editados.

Por último, el script guarda un registro de los cambios en los 
archivos `changelog.csv` y `history.md`. Estos archivos
deben existir en las rutas `path_changelog` y `path_history`.
La primera línea del archivo `changelog.csv` es el header y 
contiene las columnas de la lista `changelog_cols`.
'''

from datetime import datetime
import pandas as pd

from paths import *

def save_new_or_deleted_to_changelog(idx, tipo_cambio, path):
    '''
    Agrega los registros nuevos o borrados a un csv. 
    La columna `Usuario` sólo se llena para registros nuevos.

    Recibe:
        idx (list): Lista u otro objeto iterable de ids que tuvieron cambios
        tipo_cambio (str): `new` para registros nuevos y `del` para registros borrados.
        path (str): ruta del csv donde se guardan los cambios
    '''
    Opciones_cambios = {'new' : 'Registro nuevo',
                        'del' : 'Registro borrado'}
    
    cambios = pd.DataFrame(columns=changelog_cols)
    cambios['ID'] = idx
    cambios[['Fecha', 'Tipo cambio']] = datetime.now().strftime('%Y-%m-%d'), Opciones_cambios[tipo_cambio]
    
    if tipo_cambio == 'new':
        cambios['Usuario'] = actual.loc[idx_new_records, 'usuario'].values

    cambios.to_csv(path, mode='a', index=False, header=False)


def save_edited_to_changelog(idx_edited, path):
    '''
    Itera sobre registros y columnas para identificar
    los cambios entre los dataframes `actual` y `anterior`,
    solamente considerando las columnas en `cols_comparacion`.
    Agrega a changelog los registros editados.

    Recibe:
        idx_edited (lista): Lista u otro objeto iterable de ids que tuvieron cambios
        path (str): Ruta del csv donde se guardan los cambios
    '''

    cols_comparacion = ['taxon',
                         'estatus',
                         'id_valido',
                         'taxon_valido',
                         'referencia',
                         'categoria_agrobiodiversidad',
                         'subcategoria_agrobiodiversidad',
                         'justificacion_subcategoria',
                         'comentarios_revision']

    cambios = pd.DataFrame(columns=changelog_cols)
    
    for idx, row in actual.loc[idx_edited].iterrows():
        for col in cols_comparacion:
            if row[col] != anterior.loc[idx, col]:
                cambios = cambios.append({
                                'ID': idx,
                                'Campo': col,
                                'Valor anterior': anterior.loc[idx, col],
                                'Valor actual': row[col],
                                'Usuario': row['usuario']},
                                ignore_index=True)
    
    cambios[['Fecha', 'Tipo cambio']] = datetime.now().strftime('%Y-%m-%d'), 'Registro editado'
    cambios.to_csv(path, mode='a', index=False, header=False)


def list_to_markdown(lista_campos):
    '''
    Dar formato a los elementos de una lista para que
    aparezcan como una fila de una tabla en markdown.

    Recibe: 
        lista_campos (lista): Lista u otro objeto iterable de strings. Cada elemento se colocará en una columna aparte.
    Regresa:
        String con el formato de una fila de una tabla en markdown

    Ejemplo:
    lista_campos = [item1, item2, item3]
    list_to_markdown(lista_campos) = '| item1 | item2 | item3 |'
    '''

    md = ''
    for campo in lista_campos:
        md += f'| {campo} '
    
    return md + '|'


def history_templates(idx, tipo_cambio):
    '''
    Genera un string con el formato acordado para guardar 
    los cambios de un registro con id `idx` en `history.md`.
    
    El formato del string depende del tipo de cambio.
    '''
    header = list_to_markdown(actual.columns)
    divisor = list_to_markdown(['---'] * len(actual.columns))
    date = datetime.now().strftime('%Y-%m-%d')

    if tipo_cambio == 'new': 
        template = (
            f"\n### {date}\n"
            f"**Se agregó el registro {idx}:**\n\n"
            f"{header}\n"
            f"{divisor}\n"
            f"{list_to_markdown(actual.loc[idx])}\n"
        )

    if tipo_cambio == 'del':
        template = (
            f"\n### {date}\n"
            f"**Se borró el registro {idx}:**\n\n"
            f"{header}\n"
            f"{divisor}\n"
            f"{list_to_markdown(anterior.loc[idx])}\n"
        )

    if tipo_cambio == 'edit':
        template = (
            f"\n### {date}\n"
            f"**Se editó el registro {idx}.**\n\n"
            f"**Registro actual:**\n"
            f"{header}\n"
            f"{divisor}\n"
            f"{list_to_markdown(actual.loc[idx])}\n\n"
            f"**Registro anterior:**\n"
            f"{header}\n"
            f"{divisor}\n"
            f"{list_to_markdown(anterior.loc[idx])}\n"
        )
    
    return template


def print_to_history(idx_cambios, tipo_cambio, path):
    '''
    Guarda los cambios de una lista de registros con ids `idx_cambios` en `history.md`
    '''
    with open(path, 'a') as output:
        for idx in idx_cambios:
            output.write(history_templates(idx, tipo_cambio))


if __name__ == '__main__':
    changelog_cols = ['Fecha',
                      'ID',
                      'Tipo cambio',
                      'Campo',
                      'Valor anterior',
                      'Valor actual',
                      'Usuario']
        
    actual = pd.read_csv(path_actual, index_col='id', keep_default_na=False)
    anterior = pd.read_csv(path_anterior, index_col='id', keep_default_na=False)

    # los registros nuevos corresponden a los ids
    # que se encuentran en `actual` pero no en `anterior`
    idx_new_records = list(set(actual.index) - set(anterior.index))

    # los registros borrados corresponden a los ids
    # que se encuentran en `anterior` pero no en `actual`
    idx_deleted_records = list(set(anterior.index) - set(actual.index))

    # los registros editados corresponden a los ids que existen 
    # tanto en `anterior` como en `actual`,
    # y donde cambió el valor `updatedAt` --- ¿Qué estamos asumiendo aquí?
    # ¿Podemos asumir que todos los registros tienen un valor en `updatedAt`? 
    idx_intersect = set(actual.index) & set(anterior.index)

    # Esta comparación regresa True en registros donde `updatedAt` == nan, aunque no se hayan editado
    # Por eso los csv se leen con la opción keep_default_na=False
    edited = actual.loc[idx_intersect, 'updatedAt'] != anterior.loc[idx_intersect, 'updatedAt']
    idx_edited_records = (actual.loc[idx_intersect]
                                .loc[edited]
                                .index)

    save_new_or_deleted_to_changelog(idx_new_records, 'new', path_changelog)
    save_new_or_deleted_to_changelog(idx_deleted_records, 'del', path_changelog)
    save_edited_to_changelog(idx_edited_records, path_changelog)

    print_to_history(idx_new_records, 'new', path_history)
    print_to_history(idx_deleted_records, 'del', path_history)
    print_to_history(idx_edited_records, 'edit', path_history)