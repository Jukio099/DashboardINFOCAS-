#!/usr/bin/env python3
"""
Script de verificación para asegurar que el dashboard use EXCLUSIVAMENTE datos de CSVs
"""

import pandas as pd
import os
from pathlib import Path

def verificar_archivos_csv():
    """Verifica que todos los archivos CSV necesarios existan"""
    data_dir = Path("data/clean")
    archivos_requeridos = [
        "generalidades.csv",
        "sector_economico.csv", 
        "empresarial.csv",
        "numero_de_empresas_por_municipi.csv",
        "ciclo_vital.csv",
        "graduados_profesion.csv",
        "tasa_desercion_sector_oficial.csv",
        "morbilidad1.csv",
        "calidad_del_agua.csv",
        "seguridad.csv",
        "estructura_demografica.csv"
    ]
    
    print("🔍 VERIFICACIÓN DE ARCHIVOS CSV")
    print("=" * 50)
    
    archivos_faltantes = []
    archivos_existentes = []
    
    for archivo in archivos_requeridos:
        ruta_archivo = data_dir / archivo
        if ruta_archivo.exists():
            archivos_existentes.append(archivo)
            print(f"✅ {archivo} - ENCONTRADO")
        else:
            archivos_faltantes.append(archivo)
            print(f"❌ {archivo} - NO ENCONTRADO")
    
    print("\n" + "=" * 50)
    print(f"📊 RESUMEN: {len(archivos_existentes)}/{len(archivos_requeridos)} archivos encontrados")
    
    if archivos_faltantes:
        print(f"⚠️  Archivos faltantes: {', '.join(archivos_faltantes)}")
        return False
    else:
        print("🎉 ¡Todos los archivos CSV están presentes!")
        return True

def verificar_contenido_csv():
    """Verifica que los CSVs tengan contenido válido"""
    data_dir = Path("data/clean")
    
    print("\n🔍 VERIFICACIÓN DE CONTENIDO CSV")
    print("=" * 50)
    
    archivos_verificados = []
    
    for archivo in data_dir.glob("*.csv"):
        try:
            df = pd.read_csv(archivo)
            if not df.empty:
                archivos_verificados.append(archivo.name)
                print(f"✅ {archivo.name} - {len(df)} filas, {len(df.columns)} columnas")
            else:
                print(f"⚠️  {archivo.name} - ARCHIVO VACÍO")
        except Exception as e:
            print(f"❌ {archivo.name} - ERROR: {e}")
    
    print(f"\n📊 Archivos con contenido válido: {len(archivos_verificados)}")
    return len(archivos_verificados) > 0

def verificar_loader_sin_hardcode():
    """Verifica que el loader.py no tenga valores hardcodeados"""
    print("\n🔍 VERIFICACIÓN DE CÓDIGO SIN VALORES HARDCODEADOS")
    print("=" * 50)
    
    with open("utils/loader.py", "r", encoding="utf-8") as f:
        contenido = f.read()
    
    # Buscar valores hardcodeados sospechosos
    valores_sospechosos = [
        "481938", "23082000", "5.01", "17", "76.2", "8.9", "45.7", "5.5", "4850"
    ]
    
    valores_encontrados = []
    for valor in valores_sospechosos:
        if valor in contenido:
            valores_encontrados.append(valor)
    
    if valores_encontrados:
        print(f"⚠️  Valores hardcodeados encontrados: {', '.join(valores_encontrados)}")
        return False
    else:
        print("✅ No se encontraron valores hardcodeados sospechosos")
        return True

def main():
    """Función principal de verificación"""
    print("🚀 VERIFICACIÓN COMPLETA DEL DASHBOARD")
    print("=" * 60)
    
    # Verificar archivos CSV
    csv_ok = verificar_archivos_csv()
    
    # Verificar contenido
    contenido_ok = verificar_contenido_csv()
    
    # Verificar código
    codigo_ok = verificar_loader_sin_hardcode()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN FINAL")
    print("=" * 60)
    
    if csv_ok and contenido_ok and codigo_ok:
        print("🎉 ¡VERIFICACIÓN EXITOSA!")
        print("✅ Todos los archivos CSV están presentes")
        print("✅ Los archivos tienen contenido válido")
        print("✅ El código no tiene valores hardcodeados")
        print("\n🚀 El dashboard está listo para usar EXCLUSIVAMENTE datos de CSVs")
    else:
        print("❌ VERIFICACIÓN FALLIDA")
        if not csv_ok:
            print("❌ Faltan archivos CSV")
        if not contenido_ok:
            print("❌ Los archivos CSV están vacíos o corruptos")
        if not codigo_ok:
            print("❌ El código tiene valores hardcodeados")
        print("\n🔧 Ejecute 'python preparar_datos.py' para generar los CSVs")

if __name__ == "__main__":
    main()
