"""
Script para corregir los nombres de columnas en los CSVs
y actualizar el código para usar los nombres correctos
"""

import pandas as pd
import os
from pathlib import Path

def corregir_nombres_columnas():
    """Corrige los nombres de columnas en los CSVs"""
    data_dir = Path("data/clean")
    
    print("🔧 CORRIGIENDO NOMBRES DE COLUMNAS")
    print("=" * 50)
    
    # Mapeo de nombres incorrectos a correctos
    correcciones = {
        'sector_economico.csv': {
            'sector_econ_mico': 'sector_economico',
            'participaci_n_porcentual': 'participacion_porcentual',
            'valor_aproximado_cop_billones': 'valor_aproximado_cop_billones'
        },
        'empresarial.csv': {
            'tama_o_de_empresa': 'tamaño_de_empresa',
            'n_mero_de_empresas': 'numero_de_empresas',
            'porcentaje_del_total': 'porcentaje_del_total'
        },
        'graduados_profesion.csv': {
            'rea_de_conocimiento': 'area_de_conocimiento',
            'n_mero_de_graduados': 'numero_de_graduados',
            'porcentaje_del_total': 'porcentaje_del_total'
        },
        'numero_de_empresas_por_municipi.csv': {
            'municipio': 'municipio',
            'n_mero_de_empresas': 'numero_de_empresas'
        }
    }
    
    for archivo, mapeo in correcciones.items():
        ruta_archivo = data_dir / archivo
        if ruta_archivo.exists():
            try:
                df = pd.read_csv(ruta_archivo)
                df_original = df.copy()
                
                # Renombrar columnas
                df = df.rename(columns=mapeo)
                
                # Guardar archivo corregido
                df.to_csv(ruta_archivo, index=False)
                print(f"✅ {archivo} - Columnas corregidas")
                print(f"   Antes: {list(df_original.columns)}")
                print(f"   Después: {list(df.columns)}")
                
            except Exception as e:
                print(f"❌ Error procesando {archivo}: {e}")
        else:
            print(f"⚠️  {archivo} - No encontrado")

def verificar_correcciones():
    """Verifica que las correcciones se aplicaron correctamente"""
    data_dir = Path("data/clean")
    
    print("\n🔍 VERIFICANDO CORRECCIONES")
    print("=" * 50)
    
    archivos_verificar = [
        'sector_economico.csv',
        'empresarial.csv', 
        'graduados_profesion.csv',
        'numero_de_empresas_por_municipi.csv'
    ]
    
    for archivo in archivos_verificar:
        ruta_archivo = data_dir / archivo
        if ruta_archivo.exists():
            df = pd.read_csv(ruta_archivo)
            print(f"✅ {archivo}: {list(df.columns)}")
        else:
            print(f"❌ {archivo}: No encontrado")

if __name__ == "__main__":
    corregir_nombres_columnas()
    verificar_correcciones()
    print("\n🎉 ¡Corrección completada!")
