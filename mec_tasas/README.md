# **Script mec_tasas - Extracción de Datos Educativos**

Este script procesa datos del archivo **"Evolución_2011-2024.xlsx"**, proveniente de:  
📂 [OneDrive - Ministerio de Educación](https://mecgob-my.sharepoint.com/personal/andres_espinola_mec_gob_ar/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fandres_espinola_mec_gob_ar%2FDocuments%2FMinisterio%2FBases%2FDatos_MEC_PowerBI&ga=1)  

## **📌 Objetivo**
El script extrae y estructura los datos de tasas educativas de Argentina desde el archivo de Excel proporcionado por el Ministerio de Educación.

## **🛠️ Instalación y Dependencias**
Asegúrate de tener Python instalado y ejecuta:  
```bash
pip install pandas openpyxl
```

## **📂 Uso**
1️⃣ Coloca el archivo **"Evolución_2011-2024.xlsx"** en la carpeta `files/`.  
2️⃣ Ejecuta el script:  
```bash
python read_excel_tasas.py
```

## **📊 Estructura de los Datos**
El script toma datos de la hoja **"Tasas 2011-2024"**, omitiendo la primera fila (encabezados).  
Las columnas procesadas incluyen:
- `tasas`
- `ra_ano`
- `div_geografica`
- `sector`
- `nivel`
- `total`
- `1er_ano`, `2do_ano`, `3er_ano`, `4to_ano`, `5to_ano`, `6to_ano`

## **📌 Notas**
🔹 Si el archivo no se encuentra en `files/`, el script no podrá ejecutarse.  
🔹 `NaN` en datos numéricos se convierten a `0` para evitar errores de base de datos.  

