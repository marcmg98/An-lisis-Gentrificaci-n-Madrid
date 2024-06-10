import os
import json
import csv

def obtener_info(address_id, type):
    barrio = address_id.split('/')[-1]
    tipo_ubicacion = type.split('/')[-1].replace('entidadesYorganismos', '').replace('_', ' ').strip()
    return barrio, tipo_ubicacion

def limpiar_nombre(nombre):
    nombre_sin_extension = os.path.splitext(nombre)[0]  # Elimina la extensión .json
    nombre_limpio = ''.join(filter(str.isalpha, nombre_sin_extension)).replace('_', ' ')
    return nombre_limpio

ruta_carpeta = r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\JSON Tipo Ubicaciones'
datos_procesados = []

for archivo in os.listdir(ruta_carpeta):
    if archivo.endswith('.json'):
        ruta_archivo = os.path.join(ruta_carpeta, archivo)
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if '@graph' in data:
                for entry in data['@graph']:
                    id = entry.get('id', '')
                    title = entry.get('title', '')
                    latitude = entry.get('location', {}).get('latitude', '')
                    longitude = entry.get('location', {}).get('longitude', '')
                    adress_id = entry.get('address', {}).get('district', {}).get('@id', '')
                    type = entry.get('@type', '')
                    barrio, tipo_ubicacion = obtener_info(adress_id, type)
                    categoria = limpiar_nombre(archivo)
                    datos_procesados.append([id, title, latitude, longitude, barrio, tipo_ubicacion, categoria])

ruta_salida_csv = 'datos_salida.csv'
with open(ruta_salida_csv, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ID', 'Nombre', 'Latitud', 'Longitud', 'Barrio', 'Tipo de Ubicación', 'Categoría'])
    writer.writerows(datos_procesados)

print("Proceso completado. Los datos se han guardado en", ruta_salida_csv)
