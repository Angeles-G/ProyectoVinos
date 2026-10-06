# Mas que Vino

📋 Descripción del Proyecto
"Más que vino" es un producto web interactivo de storytelling visual y análisis de datos centrado en la industria del vino orgánico certificado argentino y sus dinámicas de exportación.

A través de una narrativa estructurada en capítulos interactivos, mapas geoespaciales y simulaciones de escenarios comerciales, el proyecto analiza la relación entre el volumen físico exportado (litros) y el valor económico capturado (USD FOB) por mercado internacional y provincia depositaria originaria.

El foco principal está en demostrar que la oportunidad estratégica reside en el incremento de valor agregado y posicionamiento de precio, más allá del simple crecimiento en volumen físico de litros.

## 🎯 Objetivos Principales
* Visualizar la concentración de mercado: Analizar qué países absorben el mayor volumen de litros exportados y cuáles representan nichos de mayor valor unitario.

* Determinar la brecha de precio (Techo P75): Evaluar el margen de crecimiento analizando la diferencia entre el precio mediano por litro y el percentil 75 (P75) dentro de cada mercado de destino.

* Mapeo Geoespacial: Representar geográficamente los principales destinos de exportación y la distribución por provincias depositarias en Argentina.

* Simulación de Escenarios: Ofrecer una herramienta dinámica e interactiva que calcula el impacto económico potencial (USD FOB) si los exportadores capturan un porcentaje de la brecha hacia el P75 de precio.

## 🚀 Características Clave
* Hero & Key Performance Indicators (KPIs): Indicadores clave animados que muestran totales de litros, mercados destino, embarques y valor FOB general.

* ### Narrativa Interactiva por Capítulos:

* Capítulo 1: Distribución y concentración de volumen (litros y embarques por país).

* Capítulo 2: Relación Volumen vs. Precio Mediano (gráfico de burbujas dinámico con escala logarítmica).

* Capítulo 3: Análisis del techo de precio (rango entre precio mediano y P75).

* Capítulo 4: Desglose por provincias depositarias argentinas (participación y precio promedio).

* Capítulo 5: Simulador de escenario comercial interactivo en tiempo real.

* Mapa Geoespacial Interactivo: Integrado con Leaflet.js sobre cartografía oscura (ESRI World Dark Gray), con conmutación entre Destinos Internacionales y Provincias Depositarias.

* Conexión Bi-direccional Gráfico-Mapa: Al hacer clic en un país o barra de un gráfico, el mapa realiza una transición fluida (flyTo) hacia la ubicación geográfica correspondiente marcando los datos puntuales.

## 🛠️ Tecnologías Utilizadas
* Frontend HTML5 / CSS3: Maquetación responsiva personalizada, variables de estilo, animaciones SVG/CSS y diseño adaptativo.

* Bootstrap 5: Sistema de grillas y componentes base.

* JavaScript (ES6+): Lógica del storytelling, procesamiento dinámico de JSON, animaciones numéricas e interactividad.

* Chart.js (v4): Visualización de datos interactivos (gráficos de barras, burbujas dinámicas, doughnut y rangos).
  
## 📊 Dataset y Origen de Datos
Los datos provienen de datos abiertos del gobierno, mas precisamente de " Datos de agricultura, ganadería y pesca - Padrón de Operadores Orgánicos", analizados para la competencia Contar con Datos 2026 (Universidad de San Andrés), procesados previamente en Python (Pandas / NumPy) para estructurar métricas agregadas por mercado (mediana, percentiles, volúmenes, embarques) y generar el archivo estático datos_completos.json.

## 👩‍💻 Autora
Lupe Malbec/ Angeles Belén García — Desarrollo, Análisis de Datos y Diseño UI/UX

### Proyecto presentado para Contar con Datos 2026 — Universidad de San Andrés.
Leaflet.js: Renderización de mapas interactivos y popups geoespaciales.

FontAwesome: Iconografía técnica e intuitiva.
