# 🏛️ Dashboard de Competitividad de Casanare

Dashboard interactivo desarrollado con Streamlit para visualizar y analizar los indicadores de competitividad del departamento de Casanare, Colombia.

## 🎯 Características Principales

- **Página Principal**: Panorama general con KPIs clave y visualizaciones principales
- **Perfil Económico**: Análisis de sectores económicos con treemap interactivo
- **Tejido Empresarial**: Distribución de empresas por tamaño y municipio
- **Seguridad Ciudadana**: Indicadores de seguridad y convivencia
- **Salud Pública**: Análisis de morbilidad, calidad del agua y demografía
- **Educación**: Graduados por área y deserción escolar

## 🚀 Tecnologías Utilizadas

- **Streamlit**: Framework para aplicaciones web de datos
- **Plotly Express**: Visualizaciones interactivas modernas
- **Pandas**: Procesamiento y análisis de datos
- **NumPy**: Operaciones numéricas
- **OpenPyXL**: Lectura de archivos Excel

## 📁 Estructura del Proyecto

```
DashboardINFOCAS-/
├── Dashboard.py                           # Página principal
├── pages/                                 # Páginas de la aplicación
│   ├── 1_📊_Perfil_Económico.py
│   ├── 2_🏢_Tejido_Empresarial.py
│   ├── 3_🛡️_Seguridad_Ciudadana.py
│   ├── 4_🩺_Salud.py
│   └── 5_🎓_Educación.py
├── utils/                                 # Módulos utilitarios
│   ├── loader.py                          # Carga de datos
│   └── plotting.py                        # Funciones de visualización
├── data/                                  # Datos procesados
│   └── clean/                             # Datos limpios en CSV
├── preparar_datos.py                      # Script de preprocesamiento
├── requirements.txt                       # Dependencias
└── README.md                              # Documentación
```

## 🛠️ Instalación y Configuración

### 1. Clonar el repositorio
```bash
git clone <url-del-repositorio>
cd DashboardINFOCAS-
```

### 2. Crear entorno virtual
```bash
python -m venv venv
```

### 3. Activar entorno virtual

**Windows:**
```bash
venv\Scripts\activate
```

**Linux/Mac:**
```bash
source venv/bin/activate
```

### 4. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 5. Preparar los datos (opcional)
```bash
python preparar_datos.py
```

### 6. Ejecutar la aplicación
```bash
streamlit run Dashboard.py
```

## 📊 Fuente de Datos

El dashboard utiliza datos del archivo `Indicadores generalidades oficial.xlsx` que contiene información oficial de:

- Indicadores de competitividad departamental
- Datos económicos y empresariales
- Estadísticas de seguridad ciudadana
- Indicadores de salud pública
- Datos del sistema educativo

## 🎨 Características de Diseño

- **Interfaz moderna**: Diseño limpio con gradientes y colores corporativos
- **Responsive**: Adaptado para diferentes tamaños de pantalla
- **Interactividad**: Gráficos interactivos con Plotly
- **Navegación intuitiva**: Sidebar con acceso a todas las secciones
- **Métricas visuales**: KPIs destacados con `st.metric`

## 📈 Funcionalidades por Página

### Dashboard Principal
- KPIs principales del departamento
- Treemap de sectores económicos
- Gráfico de dona de distribución poblacional
- Análisis empresarial y territorial

### Perfil Económico
- Treemap interactivo de participación sectorial
- Análisis de concentración económica
- Estrategias por sector
- Datos detallados con tablas interactivas

### Tejido Empresarial
- Distribución por tamaño de empresa
- Ranking de municipios empresariales
- Análisis de concentración territorial
- Insights y recomendaciones estratégicas

### Seguridad Ciudadana
- Indicadores de criminalidad
- Análisis de tendencias
- Comparativo nacional
- Estrategias de prevención

### Salud Pública
- KPIs de salud poblacional
- Vigilancia epidemiológica
- Calidad del agua
- Estructura demográfica

### Educación
- Graduados por área de conocimiento
- Deserción escolar municipal
- Análisis comparativo
- Recomendaciones estratégicas

## 🔧 Arquitectura del Código

### Módulo de Carga (`utils/loader.py`)
- Funciones específicas para cada dataset
- Cache de datos con `@st.cache_data`
- Manejo de errores y validaciones
- Extracción de KPIs calculados

### Módulo de Visualización (`utils/plotting.py`)
- Funciones de Plotly personalizadas
- Estilos corporativos consistentes
- Gráficos responsivos y accesibles
- Paleta de colores unificada

### Preprocesamiento de Datos (`preparar_datos.py`)
- Limpieza automática de datos Excel
- Conversión a formato snake_case
- Normalización de valores numéricos
- Generación de CSVs limpios

## 🎯 Mejores Prácticas Implementadas

- **Código limpio**: Comentarios y documentación completa
- **Modularidad**: Separación de responsabilidades
- **Performance**: Cache de datos y optimizaciones
- **UX/UI**: Diseño centrado en el usuario
- **Mantenibilidad**: Estructura escalable y organizad

## 📋 Próximas Mejoras

- [ ] Integración con APIs en tiempo real
- [ ] Exportación de reportes en PDF
- [ ] Filtros temporales avanzados
- [ ] Dashboard de administración
- [ ] Alertas automáticas por umbrales

## 👥 Contribución

Para contribuir al proyecto:

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit tus cambios (`git commit -am 'Agregar nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crea un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo `LICENSE` para más detalles.

## 📞 Contacto

**Gobernación de Casanare**
- Website: [www.casanare.gov.co](https://www.casanare.gov.co)
- Email: info@casanare.gov.co

---

*Dashboard desarrollado para impulsar la toma de decisiones basada en datos en el departamento de Casanare* 🏛️
