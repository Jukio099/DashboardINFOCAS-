# 🏛️ Dashboard de Competitividad de Casanare (Versión 2.0)

Dashboard interactivo de élite, desarrollado con **Dash** y **Altair**, para visualizar y analizar los indicadores de competitividad del departamento de Casanare, Colombia. Esta versión representa una refactorización completa del proyecto original, enfocada en la robustez, mantenibilidad y una experiencia de usuario superior.

## 🎯 Características Principales

- **Arquitectura Moderna**: Aplicación de una sola página (SPA) con navegación fluida a través de un sidebar fijo.
- **Visualizaciones Impactantes**: Gráficos interactivos y estéticamente agradables construidos con Altair, diseñados para "contar una historia".
- **Pipeline de Datos Robusto**: Proceso de ETL automatizado y fiable que limpia y prepara los datos desde un archivo Excel.
- **Rendimiento Optimizado**: Carga de datos centralizada y en caché para una experiencia de usuario rápida y receptiva.
- **Código de Alta Calidad**: Estructura modular, código documentado y siguiendo las mejores prácticas de desarrollo.

## 🚀 Tecnologías Utilizadas

- **Dash**: Framework principal para la construcción de la aplicación web analítica.
- **Dash Bootstrap Components**: Para un diseño profesional y responsivo.
- **Altair**: Para la creación de visualizaciones declarativas e interactivas.
- **Pandas**: Para la manipulación y procesamiento de datos.
- **OpenPyXL**: Para la lectura del archivo Excel fuente.

## 📁 Nueva Estructura del Proyecto

El proyecto ha sido consolidado para eliminar redundancias y mejorar la claridad:

```
Dashboard-Casanare/
├── dashboard.py                           # Aplicación principal de Dash
├── utils/                                 # Módulos utilitarios
│   ├── __init__.py
│   ├── loader.py                          # Módulo de carga de datos optimizado
│   └── plotting.py                        # Módulo de creación de gráficos
├── data/
│   └── clean/                             # Datos CSV limpios y procesados
├── preparar_datos.py                      # Script para el pipeline de ETL
├── requirements.txt                       # Dependencias del proyecto
├── Indicadores generalidades oficial.xlsx # Archivo de datos fuente
└── README.md                              # Esta documentación
```

## 🛠️ Instalación y Configuración

Sigue estos pasos para ejecutar el dashboard en tu entorno local:

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd Dashboard-Casanare
```

### 2. (Recomendado) Crear y activar un entorno virtual
```bash
# Crear el entorno
python -m venv venv

# Activar en Windows
venv\Scripts\activate

# Activar en Linux/Mac
source venv/bin/activate
```

### 3. Instalar las dependencias
Asegúrate de tener todas las librerías necesarias con un solo comando:
```bash
pip install -r requirements.txt
```

### 4. Preparar los datos
Este es un paso **crucial**. Ejecuta el script de preprocesamiento para generar los archivos CSV limpios que la aplicación necesita:
```bash
python preparar_datos.py
```
Verás un log en la consola indicando el progreso.

### 5. Ejecutar la aplicación
Lanza el dashboard con el siguiente comando:
```bash
python dashboard.py
```
Abre tu navegador y ve a la dirección `http://127.0.0.1:8057`.

## 🔧 Arquitectura del Código Refactorizado

### `preparar_datos.py`
- **Orquestador ETL**: Lee el archivo `Indicadores generalidades oficial.xlsx`.
- **Limpieza Automática**: Sanitiza los nombres de las hojas y las columnas a formato `snake_case`.
- **Procesamiento Robusto**: Convierte tipos de datos, maneja valores nulos y errores de formato de manera segura.
- **Salida Estandarizada**: Genera archivos CSV limpios en la carpeta `data/clean/`.

### `utils/loader.py`
- **Carga Centralizada**: `DataLoader` carga todos los CSV necesarios una sola vez.
- **Cache Inteligente**: Los datos se guardan en memoria (`_cache`) para evitar lecturas repetidas del disco.
- **Optimización**: Aplica conversiones de tipo y optimizaciones a los DataFrames al cargarlos.
- **API de Acceso a Datos**: Proporciona métodos claros (`get_dengue_data`, `get_sectores_economicos`, etc.) para que la aplicación acceda a los datos.

### `utils/plotting.py`
- **Fábrica de Gráficos**: Contiene funciones dedicadas para cada visualización del dashboard (`create_sectores_chart`, etc.).
- **Estilo Unificado**: Utiliza una paleta de colores y un tema de Altair personalizados para mantener la consistencia visual.
- **Visualizaciones Declarativas**: Define los gráficos con Altair, resultando en un código más legible y mantenible.

## 🎯 Mejores Prácticas Implementadas

- **Modularidad**: Separación clara de responsabilidades (app, carga de datos, visualización).
- **Código Limpio**: Uso de type hints, docstrings y un estilo de código consistente.
- **Gestión de Dependencias**: Un `requirements.txt` completo y bien organizado.
- **Logging**: El script de preparación de datos utiliza `logging` para un feedback claro y profesional.
- **Mantenibilidad**: La nueva estructura facilita la actualización de datos, la modificación de gráficos y la extensión de la aplicación.

---

*Este dashboard fue refactorizado para impulsar la toma de decisiones basada en datos en el departamento de Casanare con una herramienta moderna, robusta y eficiente.* 🏛️