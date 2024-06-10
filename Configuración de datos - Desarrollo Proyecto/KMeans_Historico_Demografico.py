import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd

# Ruta de la carpeta con los archivos CSV
folder_path = r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Históricos Demográficos'

# Leer el archivo combinado
combined_file_path = os.path.join(folder_path, 'combined_output.csv')
df = pd.read_csv(combined_file_path, delimiter=',')

# Preprocesamiento de datos
# Convertir columnas numéricas que están en formato string a float
for col in df.columns:
    if df[col].dtype == 'object':
        try:
            df[col] = df[col].str.replace(',', '.', regex=False).astype(float)
        except ValueError:
            pass

# Calcular la variación de cada variable numérica de un año respecto al año anterior
df_variations = df.groupby('Nombre Barrio').diff()

# Añadir la representación de las variaciones al dataframe original
df_variations.columns = [f'{col}_Variation' for col in df_variations.columns]
df = pd.concat([df, df_variations], axis=1)

# Eliminar filas con valores faltantes
df = df.dropna()

# Seleccionar las columnas relevantes para el clustering
features = df.drop(columns=['Número Barrio', 'Nombre Barrio', 'Año'])

# Estandarizar los datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(features)

# Determinación del número óptimo de clusters con el método del codo y el análisis de la silueta
inertia = []
silhouette_scores = []
range_n_clusters = range(2, 21)

for n in range_n_clusters:
    kmeans = KMeans(n_clusters=n, random_state=42)
    cluster_labels = kmeans.fit_predict(X_scaled)
    inertia.append(kmeans.inertia_)
    silhouette_avg = silhouette_score(X_scaled, cluster_labels)
    silhouette_scores.append(silhouette_avg)

# Ajustar el modelo K-Means con el número óptimo de clusters
optimal_clusters = 4  # Cambiar el número de clusters a 4
kmeans = KMeans(n_clusters=optimal_clusters, random_state=42)
clusters = kmeans.fit_predict(X_scaled)

# Añadir los clusters al dataframe original
df['Cluster'] = clusters

# Añadir etiquetas de gentrificación descriptivas
gentrification_labels = {0: 'Cluster 1 - Áreas No Gentrificadas', 
                         1: 'Cluster 2 - Áreas Poco Gentrificadas', 
                         2: 'Cluster 3 - Áreas Gentrificadas',
                         3: 'Cluster 4 - Áreas Muy Gentrificadas'}

df['Estado de Gentrificación'] = df['Cluster'].map(gentrification_labels)

# Cargar archivo geoespacial con geometría de los barrios
geo_path = r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Actividad Economica\Distritos.shp'
gdf = gpd.read_file(geo_path)

# Método del codo
plt.figure(figsize=(10, 6))
plt.plot(range_n_clusters, inertia, marker='o')
plt.title('Método del codo para encontrar el número óptimo de clusters')
plt.xlabel('Número de clusters')
plt.ylabel('Inercia')
plt.show()

# Análisis de la silueta
plt.figure(figsize=(10, 6))
plt.plot(range_n_clusters, silhouette_scores, marker='o')
plt.title('Análisis de la silueta para encontrar el número óptimo de clusters')
plt.xlabel('Número de clusters')
plt.ylabel('Puntuación de la silueta')
plt.show()

# Análisis de importancia de características
# Crear y ajustar el modelo de Random Forest
rf = RandomForestClassifier(n_estimators=1000, random_state=42)
rf.fit(features, clusters)

# Obtener la importancia de todas las características
feature_importances = rf.feature_importances_
feature_names = features.columns

# Crear un dataframe con las importancias
importance_df = pd.DataFrame({
    'Característica': feature_names,
    'Importancia': feature_importances
})

# Ordenar las características por importancia
importance_df = importance_df.sort_values(by='Importancia', ascending=False)

# Seleccionar solo las 10 características más importantes
top_10_importance = importance_df.head(10)

# Visualizar el top 10 de las características más importantes
plt.figure(figsize=(12, 8))
sns.barplot(x='Importancia', y='Característica', data=top_10_importance)
plt.title('Top 10 de las características más importantes según Random Forest')
plt.xlabel('Importancia')
plt.ylabel('Característica')
plt.show()

# Iterar sobre cada año
for year in df['Año'].unique():
    # Filtrar datos por año
    df_year = df[df['Año'] == year]
    gdf_year = gdf.merge(df_year, left_on='NOMBRE', right_on='Nombre Barrio', how='left')
    
    # Crear un mapa para visualizar el estado de gentrificación
    fig, ax = plt.subplots(1, 1, figsize=(15, 10))
    gdf_year.plot(column='Estado de Gentrificación', ax=ax, legend=True, cmap='viridis')

    # Ajustar la leyenda manualmente
    legend = ax.get_legend()
    legend.set_bbox_to_anchor((1, 0.5))
    legend.set_title("Estado de Gentrificación")

    # Añadir nombres de los barrios al mapa
    for x, y, label in zip(gdf_year.geometry.centroid.x, gdf_year.geometry.centroid.y, gdf_year['Nombre Barrio']):
        ax.text(x, y, label, fontsize=8, ha='center', va='center')

    plt.title(f'Estado de Gentrificación por Barrios - Año {year}')
    plt.show()

# Identificar las 5 características de variación más importantes
variation_features = [col for col in importance_df['Característica'].tolist() if col.endswith('_Variation')]
top_5_variation_columns = variation_features[:5]

# Crear gráficas de líneas para observar la evolución de las 5 características de variación más importantes por barrio
for barrio in df['Nombre Barrio'].unique():
    df_barrio = df[df['Nombre Barrio'] == barrio]
    plt.figure(figsize=(12, 8))
    for col in top_5_variation_columns:
        if col in df_barrio.columns:
            plt.plot(df_barrio['Año'], df_barrio[col], marker='o', label=col)
    
    plt.title(f'Evolución de las 5 Variaciones Más Importantes - Barrio {barrio}')
    plt.xlabel('Año')
    plt.ylabel('Variación')
    plt.legend()
    plt.show()

# Ruta para guardar el archivo de salida
output_csv_path = os.path.join(folder_path, 'output_gentrification.csv')

# Guardar el dataframe con las variaciones y los estados de gentrificación en un archivo CSV
df.to_csv(output_csv_path, index=False, decimal=',')
print(f'Archivo de salida guardado en: {output_csv_path}')