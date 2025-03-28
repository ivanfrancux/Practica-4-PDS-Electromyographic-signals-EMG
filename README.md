# Practica-4-PDS-Electromyographic-signals-EMG

## 1. Introducción
El presente informe documento la adquisición, procesamiento y análisis de la señal electromiográfica (EMG) obtenida durante un experimento sobre la fatiga muscular. El objetivo principal es evaluar la respuesta del músculo del antebrazo durante la flexión de la muñeca bajo condiciones normales y de fatiga inducida mediante una banda elástica de baja dureza.

Para ello, se implementaron técnicas de adquisición, filtrado y análisis espectral de la señal EMG con el fin de extraer información relevante sobre la frecuencia de activación muscular y la evolución de la fatiga. Además, se aplicaron herramientas estadísticas para evaluar los cambios en la respuesta muscular y validar los resultados obtenidos, siguiendo los criterios establecidos en la rúbrica de calificación.

## 2. Objetivos
- Adquirir y analizar la señal EMG del músculo del antebrazo durante la flexión de la muñeca.
- Aplicar filtros para mejorar la calidad de la señal y eliminar ruido.
- Evaluar la respuesta muscular a través del análisis espectral y estadístico.
- Comparar la actividad muscular en condiciones normales y de fatiga.
- Seguir la estructura y requerimientos de la rúbrica de calificación para obtener un análisis completo y bien documentado.

## 3. Metodología
La metodología seguida en este experimento consta de las siguientes etapas:

- **Adquisición de la señal:** Se utilizó un módulo de electromiografía con electrodos de superficie colocados en el antebrazo para captar la actividad EMG durante la flexión de la muñeca.
- **Filtrado de la señal:** Se diseñó un filtro digital basado en los parámetros estudiados en clase para eliminar artefactos y ruido.
- **Aplicación de ventanas:** Se segmentó la señal en diferentes contracciones musculares mediante ventanas temporales adecuadas.
- **Análisis espectral:** Se transformó la señal al dominio de la frecuencia para identificar componentes relevantes como la frecuencia dominante y la variabilidad espectral.
- **Análisis estadístico:** Se realizaron pruebas de comparación de medias para evaluar diferencias significativas en la actividad muscular en presencia de fatiga.

# Adquisición de la Señal

Para la adquisición de la señal electromiográfica (EMG), se utilizó un sistema de adquisición de datos (DAQ) con una frecuencia de muestreo de 1000 Hz. Esta frecuencia fue seleccionada para capturar con precisión los detalles de la señal EMG, ya que la mayor parte de la energía de estas señales se concentra entre 30 y 300 Hz (dialnet.unirioja.es). Según el teorema de Nyquist, la frecuencia de muestreo debe ser al menos el doble de la componente de frecuencia más alta que se desea registrar. Por lo tanto, una frecuencia de muestreo de 1000 Hz es adecuada para captar componentes de frecuencia de hasta 500 Hz, cubriendo el rango útil de la señal EMG.

Se empleó el módulo EMG AD8832, un dispositivo especializado diseñado para la amplificación y procesamiento de señales electromiográficas. Este módulo permite obtener mediciones de alta precisión y cuenta con filtros integrados para mejorar la calidad de la señal adquirida.

Para la captación de la actividad muscular, se usaron electrodos M3, que fueron colocados en el músculo del antebrazo. El movimiento analizado consistió en la realización de contracciones voluntarias de la muñeca, las cuales fueron realizadas contra la resistencia de una banda elástica. Esta resistencia adicional genera una mayor carga en el músculo, lo que puede inducir una fatiga más rápida (scielo.org.mx).

La señal fue registrada durante un período de 30 segundos, durante los cuales se realizaron un total de 23 contracciones musculares. La banda elástica proporcionó una resistencia constante al músculo, permitiendo un análisis más preciso de la actividad eléctrica generada durante las contracciones.

Para la alimentación del módulo EMG AD8832, se utilizó una fuente de alimentación en serie que proporcionó tanto valores positivos como negativos de voltaje. Esto fue necesario debido a los requerimientos del módulo, que necesita una alimentación simétrica para su correcto funcionamiento y procesamiento de la señal electromiográfica.
