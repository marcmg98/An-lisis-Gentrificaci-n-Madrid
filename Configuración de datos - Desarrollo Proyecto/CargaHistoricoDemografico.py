import os
import pandas as pd

# Ruta de la carpeta con los archivos CSV
folder_path = r'C:\Users\ANALMA\Desktop\MÁSTER\FEB 24 - JUNIO 24 (TFM)\TFM\Fuentes de datos\Históricos Demográficos'

# Lista para almacenar los dataframes
dataframes = []

# Leer cada archivo CSV en la carpeta
for filename in os.listdir(folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(folder_path, filename)
        
        # Leer el archivo CSV con delimitador de punto y coma como strings
        df = pd.read_csv(file_path, delimiter=';', dtype=str)
        
        # Obtener el nombre del archivo hasta el primer "_"
        base_name = filename.split('_')[0]
        
        # Comprobar y renombrar columnas si es necesario
        if 'Categorías;Barrios;2018;2019;2020;2021;2022' in df.columns:
            df.columns = ['Categorías', 'Barrios', '2018', '2019', '2020', '2021', '2022']
        elif 'Barrios;2018;2019;2020;2021;2022' in df.columns:
            df.columns = ['Barrios', '2018', '2019', '2020', '2021', '2022']
        
        # Verificar si la columna 'Barrios' existe
        if 'Barrios' in df.columns:
            try:
                # Separar la columna 'Barrios' en 'Número Barrio' y 'Nombre Barrio'
                df[['Número Barrio', 'Nombre Barrio']] = df['Barrios'].str.split('.', n=1, expand=True)
                df['Número Barrio'] = df['Número Barrio'].str.strip()
                df['Nombre Barrio'] = df['Nombre Barrio'].str.strip()
            except ValueError as e:
                print(f"Error al dividir la columna 'Barrios' en el archivo {filename}: {e}")
                continue
        else:
            print(f"Advertencia: La columna 'Barrios' no se encontró en el archivo {filename}. Columnas disponibles: {df.columns}")
            continue  # Saltar este archivo si 'Barrios' no está presente

        # Manejar la columna 'Categorías' si existe
        if 'Categorías' in df.columns:
            df_melted = pd.melt(df, id_vars=['Categorías', 'Número Barrio', 'Nombre Barrio'], 
                                value_vars=[str(year) for year in range(2018, 2023)], 
                                var_name='Año', 
                                value_name='Valor')
            df_pivot = df_melted.pivot_table(index=['Número Barrio', 'Nombre Barrio', 'Año'], 
                                             columns='Categorías', 
                                             values='Valor', 
                                             aggfunc='first')
            df_pivot.columns = [f'{base_name} - {cat}' for cat in df_pivot.columns]
            df_pivot.reset_index(inplace=True)
            dataframes.append(df_pivot)
        else:
            df_melted = pd.melt(df, id_vars=['Número Barrio', 'Nombre Barrio'], 
                                value_vars=[str(year) for year in range(2018, 2023)], 
                                var_name='Año', 
                                value_name=base_name)
            dataframes.append(df_melted)

# Combinar todos los dataframes en uno solo
if dataframes:
    final_df = pd.concat(dataframes, axis=0, ignore_index=True)
    # Pivotar el dataframe combinado para asegurar que cada combinación única tenga una fila
    final_df = final_df.pivot_table(index=['Número Barrio', 'Nombre Barrio', 'Año'], 
                                    aggfunc='first').reset_index()

    # Convertir valores numéricos a float conservando precisión y sin notación científica
    for col in final_df.columns:
        if final_df[col].dtype == 'object':
            try:
                final_df[col] = final_df[col].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
                final_df[col] = final_df[col].map(lambda x: f'{x:.10g}')  # Formato para evitar notación científica
                final_df[col] = final_df[col].str.replace('.', ',', regex=False)  # Revertir el punto a coma decimal
            except ValueError:
                pass

    # Guardar el dataframe final en un archivo CSV
    output_path = os.path.join(folder_path, 'combined_output.csv')
    final_df.to_csv(output_path, index=False, float_format='%.2f')
    print(f'Archivo combinado guardado en: {output_path}')
else:
    print("No se encontraron archivos con la columna 'Barrios'.")
