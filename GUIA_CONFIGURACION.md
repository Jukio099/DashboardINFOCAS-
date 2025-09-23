# 🚀 Guía de Configuración del Entorno - Dashboard de Competitividad

## Configuración Inicial del Proyecto

### Paso 1: Crear Entorno Virtual
```bash
# Crear el entorno virtual
python -m venv venv
```

### Paso 2: Activar el Entorno Virtual
```bash
# En Windows
.\venv\Scripts\activate

# En macOS/Linux
source venv/bin/activate
```

### Paso 3: Instalar Dependencias
```bash
# Instalar las librerías necesarias
pip install -r requirements.txt
```

### Paso 4: Ejecutar la Aplicación
```bash
# Iniciar el dashboard
streamlit run Dashboard.py
```

### Estructura del Proyecto
```
dashboard/
├── Dashboard.py              # Punto de entrada principal
├── requirements.txt          # Dependencias del proyecto
├── utils/                    # Módulos de utilidades
│   ├── loader.py            # Funciones de carga de datos
│   └── plotting.py          # Funciones de visualización
├── pages/                    # Páginas de la aplicación
│   ├── 1_📊_Perfil_Económico.py
│   └── 2_🏢_Tejido_Empresarial.py
└── venv/                     # Entorno virtual (generado)
```

## Comandos Útiles

### Desactivar Entorno Virtual
```bash
deactivate
```

### Actualizar Dependencias
```bash
pip freeze > requirements.txt
```

### Verificar Instalación
```bash
pip list
```

## Archivos CSV Requeridos

Asegúrate de que los siguientes archivos estén en la carpeta raíz del proyecto:

- `Indicadores generalidades  - Generalidades.csv`
- `Indicadores generalidades  - Sector Economico.csv`
- `Indicadores generalidades  - Empresarial.csv`
- `Indicadores generalidades  - Numero de empresas por municipio.csv`

## Solución de Problemas

### Error: "No se encontró el archivo CSV"
- Verifica que los archivos CSV estén en la misma carpeta que `Dashboard.py`
- Revisa que los nombres de archivo coincidan exactamente

### Error de Importación
- Asegúrate de que las carpetas `utils` y `pages` existan
- Verifica que el entorno virtual esté activado

### Error de Dependencias
- Ejecuta `pip install -r requirements.txt` nuevamente
- Verifica tu versión de Python (recomendado: 3.8+)

## Navegación del Dashboard

Una vez ejecutado, el dashboard tendrá tres secciones principales:

1. **Resumen General** - Indicadores clave y rankings de competitividad
2. **📊 Perfil Económico** - Composición del PIB por sectores
3. **🏢 Tejido Empresarial** - Distribución de empresas por tamaño y municipio

La navegación se realiza automáticamente a través de la barra lateral de Streamlit.

## Mejoras Implementadas

✅ **Arquitectura Modular**: Código separado en módulos especializados  
✅ **Cache de Datos**: Carga optimizada con `@st.cache_data`  
✅ **Manejo de Errores**: Validación robusta de datos y archivos  
✅ **Documentación**: Código bien comentado y documentado  
✅ **Escalabilidad**: Fácil agregar nuevas páginas y funcionalidades  
✅ **Profesional**: Sigue mejores prácticas de desarrollo Python
