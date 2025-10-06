import pandas as pd
from pathlib import Path
import re
import logging
from typing import Any

# --- Configuración ---
EXCEL_FILE = Path("Indicadores generalidades oficial.xlsx")
OUTPUT_DIR = Path("data/clean")
LOG_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"

# Configurar logging
logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
logger = logging.getLogger(__name__)

def _sanitize_string(text: str) -> str:
    """Convierte un texto a formato snake_case."""
    if not isinstance(text, str):
        text = str(text)
    # Reemplazar caracteres no alfanuméricos con guiones bajos
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    # Reemplazar espacios y guiones repetidos con un solo guion bajo
    text = re.sub(r'[\s-]+', '_', text).strip('_')
    return text.lower()

def _clean_value(value: Any) -> Any:
    """
    Limpia un valor individual, manejando strings que parecen números y
    fechas erróneas de Excel.
    """
    # Si Pandas leyó una fecha, probablemente es un número mal formateado.
    if isinstance(value, pd.Timestamp):
        logger.debug(f"Valor de fecha encontrado y descartado: {value}")
        return None

    # Si es un string, intentamos convertirlo a número.
    if isinstance(value, str):
        cleaned_value = value.strip()
        
        # Si está vacío después de limpiar, es nulo
        if not cleaned_value:
            return None
            
        # Intentar convertir a numérico directamente
        # `errors='coerce'` es ideal para esto, convierte lo no numérico en NaT/NaN
        numeric_value = pd.to_numeric(cleaned_value, errors='coerce')

        # Si la conversión fue exitosa, devolvemos el número
        if pd.notna(numeric_value):
            return numeric_value

        # Si no, devolvemos el string limpio original
        return cleaned_value

    # Si ya es un número o nulo, lo devolvemos tal cual.
    return value

def process_sheet(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica el preprocesamiento completo a una hoja de cálculo (DataFrame).
    - Limpia los nombres de las columnas.
    - Limpia los valores en cada celda.
    - Elimina filas completamente vacías.
    """
    # 1. Limpiar nombres de columnas
    df.columns = [_sanitize_string(col) for col in df.columns]

    # 2. Limpiar valores en todo el dataframe para corregir errores de tipo (ej. fechas)
    df = df.map(_clean_value)

    # 3. Eliminar filas que son completamente nulas
    df.dropna(how='all', inplace=True)

    return df

def main():
    """
    Función principal que orquesta el pipeline de preparación de datos.
    Lee un archivo Excel, procesa cada hoja y la guarda como un archivo CSV
    limpio en el directorio de salida.
    """
    logger.info("🚀 Iniciando el pipeline de preparación de datos...")

    if not EXCEL_FILE.exists():
        logger.error(f"❌ Archivo no encontrado: '{EXCEL_FILE}'. Asegúrate de que exista.")
        return

    # Crear directorio de salida si no existe
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    logger.info(f"📂 Directorio de salida: '{OUTPUT_DIR}'")

    try:
        xls = pd.ExcelFile(EXCEL_FILE)
        sheet_names = xls.sheet_names
        logger.info(f"📄 Encontradas {len(sheet_names)} hojas en el archivo Excel.")

        for sheet_name in sheet_names:
            logger.info(f"  - Procesando hoja: '{sheet_name}'...")

            df = pd.read_excel(xls, sheet_name=sheet_name)
            
            if df.empty:
                logger.warning(f"    ⚠️ La hoja '{sheet_name}' está vacía. Se omitirá.")
                continue

            df_processed = process_sheet(df.copy())
            
            # Sanitizar nombre de hoja para usar como nombre de archivo
            clean_filename = f"{_sanitize_string(sheet_name)}.csv"
            output_path = OUTPUT_DIR / clean_filename
            
            df_processed.to_csv(output_path, index=False, decimal='.')
            logger.info(f"    ✅ Hoja procesada y guardada en: '{output_path}'")

        logger.info("\n🎉 ¡Pipeline de datos completado exitosamente!")
        logger.info(f"Los archivos CSV limpios están listos en '{OUTPUT_DIR}'.")

    except Exception as e:
        logger.error(f"❌ Ocurrió un error inesperado durante el procesamiento: {e}", exc_info=True)

if __name__ == '__main__':
    main()