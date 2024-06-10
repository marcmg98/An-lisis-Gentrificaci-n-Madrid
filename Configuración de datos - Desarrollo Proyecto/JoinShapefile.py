import pandas as pd
import geopandas as gpd

# Rutas de los archivos CSV
ruta_servicios = r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Actividad Economica\output.csv'
ruta_ubicaciones = r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Actividad Economica\datos_salida.csv'

# Ruta del archivo shapefile
ruta_shapefile = r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Actividad Economica\Distritos.shp'

# Leer archivos CSV
df_servicios = pd.read_csv(ruta_servicios)
df_ubicaciones = pd.read_csv(ruta_ubicaciones)

# Leer shapefile con información geográfica de distritos
gdf_distritos = gpd.read_file(ruta_shapefile)

# Asegurarse de que los nombres de los barrios coincidan en los archivos CSV y shapefile
df_servicios['barrio'] = df_servicios['barrio'].str.strip().str.title()
df_ubicaciones['Barrio'] = df_ubicaciones['Barrio'].str.strip().str.title()
gdf_distritos['NOMBRE'] = gdf_distritos['NOMBRE'].str.strip().str.title()

# Crear GeoDataFrame para servicios
gdf_servicios = gpd.GeoDataFrame(
    df_servicios,
    geometry=gpd.points_from_xy(df_servicios.longitud, df_servicios.latitud),
    crs="EPSG:4326"
)

# Crear GeoDataFrame para ubicaciones
gdf_ubicaciones = gpd.GeoDataFrame(
    df_ubicaciones,
    geometry=gpd.points_from_xy(df_ubicaciones.Longitud, df_ubicaciones.Latitud),
    crs="EPSG:4326"
)

# Unir información de servicios con distritos
gdf_servicios_distritos = gpd.sjoin(gdf_servicios, gdf_distritos, how='left', op='within')
gdf_ubicaciones_distritos = gpd.sjoin(gdf_ubicaciones, gdf_distritos, how='left', op='within')

# Rutas de salida para los nuevos archivos CSV
ruta_salida_servicios = r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Actividad Economica\servicios_con_distritos.csv'
ruta_salida_ubicaciones = r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Actividad Economica\ubicaciones_con_distritos.csv'

# Guardar los resultados en nuevos archivos CSV
gdf_servicios_distritos.to_csv(ruta_salida_servicios, index=False)
gdf_ubicaciones_distritos.to_csv(ruta_salida_ubicaciones, index=False)

print(f'Archivos CSV guardados en: {ruta_salida_servicios} y {ruta_salida_ubicaciones}')
