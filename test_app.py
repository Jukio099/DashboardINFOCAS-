#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba para verificar que la aplicación funciona correctamente.
"""

import sys
import os

# Agregar el directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Prueba que todas las importaciones funcionen."""
    try:
        print("🔍 Probando importaciones...")
        
        # Probar importación de pandas
        import pandas as pd
        print("✅ pandas importado correctamente")
        
        # Probar importación de streamlit
        import streamlit as st
        print("✅ streamlit importado correctamente")
        
        # Probar importación de plotly
        import plotly.express as px
        print("✅ plotly importado correctamente")
        
        # Probar importación de nuestros módulos
        from utils.loader import load_all_data, get_kpi_values, get_ranking_data
        print("✅ módulos locales importados correctamente")
        
        return True
        
    except ImportError as e:
        print(f"❌ Error de importación: {e}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def test_data_loading():
    """Prueba que la carga de datos funcione."""
    try:
        print("\n📊 Probando carga de datos...")
        
        from utils.loader import load_all_data
        
        # Cargar datos
        data = load_all_data()
        
        if not data:
            print("❌ No se pudieron cargar los datos")
            return False
            
        print(f"✅ Datos cargados correctamente:")
        print(f"   - Secciones disponibles: {list(data.keys())}")
        print(f"   - Datos generales: {len(data.get('general', []))} filas")
        print(f"   - Datos de sectores: {len(data.get('sector', []))} filas")
        print(f"   - Datos empresariales: {len(data.get('empresarial', []))} filas")
        print(f"   - Datos de municipios: {len(data.get('municipios', []))} filas")
        
        # Probar KPIs
        from utils.loader import get_kpi_values
        kpis = get_kpi_values(data.get('general'))
        print(f"✅ KPIs extraídos: {len(kpis)} indicadores")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en carga de datos: {e}")
        return False

def test_plotting():
    """Prueba que las funciones de plotting funcionen."""
    try:
        print("\n📈 Probando funciones de plotting...")
        
        from utils.plotting import plot_ranking_bars
        import pandas as pd
        
        # Crear datos de prueba
        test_data = pd.DataFrame({
            'Indicador': ['Test 1', 'Test 2'],
            'Valor': [7.5, 8.2]
        })
        
        # Probar función de plotting
        fig = plot_ranking_bars(test_data)
        print("✅ Funciones de plotting funcionan correctamente")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en plotting: {e}")
        return False

def main():
    """Función principal de prueba."""
    print("🚀 Iniciando pruebas de la aplicación...")
    print("=" * 50)
    
    # Ejecutar pruebas
    tests = [
        ("Importaciones", test_imports),
        ("Carga de datos", test_data_loading),
        ("Plotting", test_plotting)
    ]
    
    results = []
    for test_name, test_func in tests:
        result = test_func()
        results.append((test_name, result))
    
    # Resumen de resultados
    print("\n" + "=" * 50)
    print("📋 RESUMEN DE PRUEBAS:")
    print("=" * 50)
    
    all_passed = True
    for test_name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{test_name}: {status}")
        if not result:
            all_passed = False
    
    print("=" * 50)
    if all_passed:
        print("🎉 ¡TODAS LAS PRUEBAS PASARON! La aplicación está lista para ejecutarse.")
        print("\nPara ejecutar la aplicación:")
        print("1. Activar el entorno virtual: .\\venv\\Scripts\\Activate.ps1")
        print("2. Ejecutar: streamlit run Dashboard.py")
    else:
        print("⚠️  Algunas pruebas fallaron. Revisa los errores arriba.")
    
    return all_passed

if __name__ == "__main__":
    main()
