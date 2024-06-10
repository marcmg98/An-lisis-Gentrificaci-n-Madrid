import pandas as pd
import json
from pyproj import Transformer

# Ruta del archivo JSON
json_file_path = r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Actividad Economica\actividadeconomica202405.json'

# Leer el archivo JSON
with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Crear un DataFrame a partir del JSON
df = pd.DataFrame(data)

# Filtrar por desc_seccion "HOSTELERÍA"
df_filtered = df[df['desc_seccion'] == 'HOSTELERÍA']

# Seleccionar y renombrar las columnas necesarias
df_selected = df_filtered[['id_local', 'desc_distrito_local', 'coordenada_x_local', 'coordenada_y_local', 'desc_division']].copy()
df_selected.columns = ['id', 'barrio', 'coordenada_x', 'coordenada_y', 'tipo_servicio']

# Limpiar y formatear los nombres de los barrios
df_selected.loc[:, 'barrio'] = df_selected['barrio'].str.strip().str.title()

# Eliminar duplicados basados en 'id'
df_selected.drop_duplicates(subset='id', inplace=True)

# Definir el proyector para la zona UTM específica (por ejemplo, zona 30T para España)
transformer = Transformer.from_crs("epsg:32630", "epsg:4326")  # 32630 es el código EPSG para UTM zona 30N, 4326 es el código EPSG para WGS84

# Función para convertir UTM a lat/lon
def utm_to_latlon(x, y):
    lon, lat = transformer.transform(x, y)
    return lat, lon

# Aplicar la conversión a las coordenadas
df_selected[['longitud', 'latitud']] = df_selected.apply(
    lambda row: utm_to_latlon(row['coordenada_x'], row['coordenada_y']), axis=1, result_type='expand'
)

# Eliminar las columnas de coordenadas UTM
df_selected.drop(columns=['coordenada_x', 'coordenada_y'], inplace=True)

# Guardar el DataFrame en un archivo CSV
output_csv_path = r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Actividad Economica\output.csv'
df_selected.to_csv(output_csv_path, index=False)

print(f'Archivo CSV guardado en: {output_csv_path}')