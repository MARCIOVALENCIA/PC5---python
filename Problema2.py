import pandas as pd
import sqlite3

# Cargar el archivo CSV
data_wine = pd.read_csv('data/winemag-data-130k-v2.csv')

# 1. Renombrar columnas
data_wine.rename(columns={
    'country': 'pais',
    'description': 'descripcion',
    'points': 'puntuacion',
    'price': 'precio'
}, inplace=True)

# 2. Crear nuevas columnas
# Columna 'rango_precio' clasifica los vinos por el precio
data_wine['rango_precio'] = pd.cut(data_wine['precio'], bins=[0, 20, 50, 100, 200, 1000], labels=['Bajo', 'Medio', 'Alto', 'Premium', 'Lujoso'], right=False)

# Columna 'puntuacion_clasificacion' clasifica los vinos por la puntuación
data_wine['puntuacion_clasificacion'] = pd.cut(data_wine['puntuacion'], bins=[0, 85, 90, 95, 100], labels=['Regular', 'Bueno', 'Excelente', 'Sobresaliente'], right=False)

# Columna 'continente' basada en el país
def asignar_continente(pais):
    if pais in ['Italy', 'France', 'Spain', 'Portugal', 'Germany']:
        return 'Europa'
    elif pais in ['US', 'Canada']:
        return 'América del Norte'
    elif pais in ['Argentina', 'Chile']:
        return 'América del Sur'
    elif pais in ['Australia', 'New Zealand']:
        return 'Oceanía'
    elif pais in ['South Africa']:
        return 'África'
    else:
        return 'Desconocido'

data_wine['continente'] = data_wine['pais'].apply(asignar_continente)

# 3. Generar 4 reportes distintos
# Reporte 1: Vinos mejor puntuados por continente
reporte_1 = data_wine.groupby('continente').apply(lambda x: x.nlargest(1, 'puntuacion'))[['pais', 'puntuacion', 'variety', 'winery']]
reporte_1.to_csv('reporte_1_mejores_puntuaciones.csv', index=False)

# Reporte 2: Promedio de precio de vino y cantidad de reviews por país, ordenado de mayor a menor
reporte_2 = data_wine.groupby('pais').agg({'precio': 'mean'}).sort_values(by='precio', ascending=False)
reporte_2.to_excel('reporte_2_precio_promedio_reviews.xlsx')

# Reporte 3: Vinos clasificados por rango de precio
reporte_3 = data_wine.groupby('rango_precio').size().reset_index(name='cantidad_vinos')
reporte_3.to_json('reporte_3_vinos_por_rango_precio.json')

# Reporte 4: Vinos por tipo de uva, ordenado por cantidad
reporte_4 = data_wine['variety'].value_counts().reset_index(name='cantidad').rename(columns={'index': 'variety'})
conn = sqlite3.connect('reporte_4_variedades.sqlite')
reporte_4.to_sql('varieties', conn, if_exists='replace', index=False)
conn.close()

# 4. Exportar los 4 reportes en formatos diferentes
# Ya hemos exportado a CSV, Excel, JSON, y SQLite en los pasos anteriores.

# Mensaje indicando que los reportes han sido guardados
print("Los 4 reportes han sido guardados en sus respectivos formatos.")

