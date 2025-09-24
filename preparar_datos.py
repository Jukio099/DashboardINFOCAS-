# preparar_datos.py
import pandas as pd
import os
import re
import datetime

def limpiar_valor(valor):
    """
    Limpia un valor individual de forma robusta, con manejo especial para
    el problema de "números interpretados como fechas" de Excel.
    """
    # Si el valor es un objeto de fecha/hora (el problema principal)
    if isinstance(valor, datetime.datetime):
        # Esta es la corrección clave: si Pandas leyó una fecha, es muy probable
        # que sea un error de formato de Excel. Lo tratamos como NaN (nulo)
        # para que no contamine los cálculos. Podríamos intentar extraer
        # un número, pero es más seguro invalidarlo y revisar el Excel original si es necesario.
        return None

    # Si es un string, intentamos limpiarlo y convertirlo a número
    if isinstance(valor, str):
        s = valor.strip().replace('$', '').replace('%', '')
        # Manejar números con comas como decimales
        s = s.replace(',', '.')
        # Si hay múltiples puntos, probablemente son separadores de miles. Los quitamos.
        if s.count('.') > 1:
            s = s.replace('.', '', s.count('.') - 1)
        
        # Intentar la conversión final a número
        try:
            return pd.to_numeric(s)
        except (ValueError, TypeError):
            # Si después de todo no es un número, devolvemos el string limpio
            return valor
            
    # Si ya es un número o nulo, lo devolvemos
    return valor

def procesar_hoja(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica la limpieza a un DataFrame completo."""
    df.columns = [re.sub(r'[^a-zA-Z0-9]+', '_', str(col)).lower().strip('_') for col in df.columns]
    df = df.map(limpiar_valor)
    df.dropna(how='all', inplace=True)
    return df

def main():
    """Función principal para procesar el archivo Excel."""
    ruta_excel = 'Indicadores generalidades oficial.xlsx'
    directorio_salida = 'data/clean'
    
    if not os.path.exists(directorio_salida):
        os.makedirs(directorio_salida)
        
    print("🚀 Iniciando el pipeline de limpieza de datos...")
    
    try:
        xls = pd.ExcelFile(ruta_excel)
        for nombre_hoja in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=nombre_hoja)
            df_limpio = procesar_hoja(df)
            
            nombre_archivo_limpio = re.sub(r'[^a-zA-Z0-9]+', '_', nombre_hoja).lower().strip('_')
            ruta_salida = os.path.join(directorio_salida, f"{nombre_archivo_limpio}.csv")
            
            df_limpio.to_csv(ruta_salida, index=False, decimal='.')
            print(f"  ✅ Hoja '{nombre_hoja}' procesada y guardada correctamente.")
            
        print("\n🎉 ¡Pipeline de datos completado! Los archivos en 'data/clean/' están actualizados y son fiables.")
    except FileNotFoundError:
        print(f"❌ ERROR: No se encontró '{ruta_excel}'. Asegúrate de que esté en la carpeta raíz.")
    except Exception as e:
        print(f"❌ Ocurrió un error inesperado: {e}")

if __name__ == '__main__':
    main()