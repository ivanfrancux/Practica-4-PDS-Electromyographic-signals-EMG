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

## Adquisición de la Señal

Para la adquisición de la señal electromiográfica (EMG), se utilizó un sistema de adquisición de datos (DAQ) con una frecuencia de muestreo de 1000 Hz. Esta frecuencia fue seleccionada para capturar con precisión los detalles de la señal EMG, ya que la mayor parte de la energía de estas señales se concentra entre 30 y 300 Hz (dialnet.unirioja.es). Según el teorema de Nyquist, la frecuencia de muestreo debe ser al menos el doble de la componente de frecuencia más alta que se desea registrar. Por lo tanto, una frecuencia de muestreo de 1000 Hz es adecuada para captar componentes de frecuencia de hasta 500 Hz, cubriendo el rango útil de la señal EMG.

Se empleó el módulo EMG AD8832, un dispositivo especializado diseñado para la amplificación y procesamiento de señales electromiográficas. Este módulo permite obtener mediciones de alta precisión y cuenta con filtros integrados para mejorar la calidad de la señal adquirida.

Para la captación de la actividad muscular, se usaron electrodos M3, que fueron colocados en el músculo del antebrazo. El movimiento analizado consistió en la realización de contracciones voluntarias de la muñeca, las cuales fueron realizadas contra la resistencia de una banda elástica. Esta resistencia adicional genera una mayor carga en el músculo, lo que puede inducir una fatiga más rápida (scielo.org.mx).

La señal fue registrada durante un período de 30 segundos, durante los cuales se realizaron un total de 23 contracciones musculares. La banda elástica proporcionó una resistencia constante al músculo, permitiendo un análisis más preciso de la actividad eléctrica generada durante las contracciones.

Para la alimentación del módulo EMG AD8832, se utilizó una fuente de alimentación en serie que proporcionó tanto valores positivos como negativos de voltaje. Esto fue necesario debido a los requerimientos del módulo, que necesita una alimentación simétrica para su correcto funcionamiento y procesamiento de la señal electromiográfica.

interfaz

![Imagen de WhatsApp 2025-03-27 a las 23 02 36_a2704f9d](https://github.com/user-attachments/assets/438fd1d6-625b-4719-9380-29adde8387a3)



### **Explicación del Código**
Este código implementa una interfaz gráfica en Python utilizando **PyQt5** para la adquisición de señales electromiográficas (EMG) con un dispositivo DAQ de National Instruments.


### **1. Importación de Librerías**
```python
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from nptdms import TdmsFile
import nidaqmx
from nidaqmx.system import System
from nidaqmx.constants import (
    AcquisitionType,
    LoggingMode,
    LoggingOperation,
)
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QComboBox, QMessageBox
```
Se importan varias librerías clave:
- `numpy`: Para manejar arreglos numéricos y cálculos matemáticos.
- `matplotlib.pyplot`: Para graficar la señal EMG.
- `pandas`: Para guardar los datos en un archivo CSV.
- `nptdms`: Para manipular archivos TDMS (aunque no se usa en este código).
- `nidaqmx`: Para comunicarse con el dispositivo DAQ.
- `PyQt5.QtWidgets`: Para construir la interfaz gráfica.


### **2. Creación de la Interfaz Gráfica**
```python
class EMGApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
```
Se define una clase `EMGApp` que hereda de `QWidget` (ventana de PyQt5). En el método `__init__`, se llama a `self.init_ui()`, que configura la interfaz.

```python
def init_ui(self):
    self.setWindowTitle("Adquisición de EMG con DAQ")
    self.layout = QVBoxLayout()
```
Aquí se establece el título de la ventana y se usa `QVBoxLayout` para organizar los elementos en una columna.

```python
self.label_puertos = QLabel("Dispositivos DAQ disponibles:")
self.layout.addWidget(self.label_puertos)
```
Se crea una etiqueta (`QLabel`) para mostrar los dispositivos DAQ disponibles.

```python
self.puertos_combo = QComboBox()
self.layout.addWidget(self.puertos_combo)
```
Se añade un `QComboBox` para seleccionar el dispositivo DAQ.

```python
self.boton_actualizar = QPushButton("Actualizar Puertos")
self.boton_actualizar.clicked.connect(self.actualizar_puertos)
self.layout.addWidget(self.boton_actualizar)
```
Se agrega un botón para actualizar los dispositivos DAQ detectados. Al hacer clic, se ejecuta el método `actualizar_puertos()`.

```python
self.boton_iniciar = QPushButton("Iniciar Adquisición (30s)")
self.boton_iniciar.clicked.connect(self.iniciar_adquisicion)
self.layout.addWidget(self.boton_iniciar)
```
Este botón inicia la adquisición de datos por 30 segundos.

```python
self.boton_guardar = QPushButton("Guardar Señal")
self.boton_guardar.clicked.connect(self.guardar_senal)
self.layout.addWidget(self.boton_guardar)
```
Este botón guarda los datos en un archivo CSV.

```python
self.boton_mostrar = QPushButton("Mostrar Gráfica")
self.boton_mostrar.clicked.connect(self.mostrar_grafica)
self.layout.addWidget(self.boton_mostrar)
```
Este botón grafica la señal EMG adquirida.


### **3. Detección de Dispositivos DAQ**
```python
def actualizar_puertos(self):
    self.puertos_combo.clear()
    try:
        system = System.local()
        dispositivos = system.devices
        if not dispositivos:
            QMessageBox.warning(self, "Error", "No se detectaron dispositivos DAQ.")
        else:
            for dispositivo in dispositivos:
                self.puertos_combo.addItem(dispositivo.name)
    except Exception as e:
        QMessageBox.critical(self, "Error", f"Error al obtener dispositivos DAQ:\n{e}")
```
Este método obtiene los dispositivos DAQ conectados al sistema y los muestra en el `QComboBox`.


### **4. Iniciar la Adquisición de Datos**
```python
def iniciar_adquisicion(self):
    device_name = self.puertos_combo.currentText()
    if not device_name:
        QMessageBox.warning(self, "Error", "Selecciona un dispositivo DAQ antes de iniciar la adquisición.")
        return
```
Verifica si se ha seleccionado un dispositivo DAQ.

```python
self.archivo_tdms = "TestData.tdms"
self.duracion = 30  # segundos
self.frecuencia_muestreo = 1000  # Hz
total_muestras = self.duracion * self.frecuencia_muestreo
```
Define la duración de la adquisición (30 segundos) y la frecuencia de muestreo (1000 Hz). Se calcula el número total de muestras.

```python
try:
    with nidaqmx.Task() as task:
        task.ai_channels.add_ai_voltage_chan(f"{device_name}/ai0")
        task.timing.cfg_samp_clk_timing(
            self.frecuencia_muestreo,
            sample_mode=AcquisitionType.FINITE,
            samps_per_chan=total_muestras,
            source="OnboardClock"
        )
```
- Se crea una tarea (`task`) de `nidaqmx`.
- Se agrega un canal analógico (`ai0`).
- Se configura la frecuencia de muestreo y el modo de adquisición (`FINITE`).

```python
task.start()
datos = task.read(number_of_samples_per_channel=total_muestras, timeout=nidaqmx.constants.WAIT_INFINITELY)
task.stop()
```
- Se inicia la adquisición de datos.
- Se leen los valores registrados.
- Se detiene la tarea.

```python
self.procesar_datos(datos)
```
Los datos se envían para su procesamiento.


### **5. Procesamiento de Datos**
```python
def procesar_datos(self, datos):
    self.tiempos = np.linspace(0, len(datos) / self.frecuencia_muestreo, len(datos))
    self.valores = np.array(datos)
    self.mostrar_grafica()
```
Convierte los datos en un arreglo de `numpy` y calcula el tiempo correspondiente a cada muestra.


### **6. Mostrar la Gráfica**
```python
def mostrar_grafica(self):
    if not hasattr(self, 'tiempos') or not hasattr(self, 'valores') or len(self.tiempos) == 0:
        QMessageBox.warning(self, "Error", "No hay datos para graficar. Realiza una adquisición primero.")
        return

    plt.figure(figsize=(10, 5))
    plt.plot(self.tiempos, self.valores, label="Señal EMG", color="b")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Voltaje (V)")
    plt.title("Señal EMG Adquirida")
    plt.legend()
    plt.grid(True)
    plt.show()
```
Si hay datos disponibles, se genera una gráfica de la señal EMG usando `matplotlib`.


### **7. Guardar la Señal en un Archivo CSV**
```python
def guardar_senal(self):
    if not hasattr(self, 'tiempos') or not hasattr(self, 'valores') or len(self.tiempos) == 0:
        QMessageBox.warning(self, "Error", "No hay datos para guardar. Realiza una adquisición primero.")
        return

    datos = pd.DataFrame({"Tiempo (s)": self.tiempos, "Voltaje (V)": self.valores})
    archivo_csv = "senal_emg.csv"
    datos.to_csv(archivo_csv, index=False)
    QMessageBox.information(self, "Guardado", f"Señal guardada en {archivo_csv}")
```
- Se guarda la señal en un archivo `CSV` con `pandas`.
- Se muestra un mensaje de confirmación.


### **8. Ejecución de la Aplicación**
```python
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = EMGApp()
    ventana.show()
    sys.exit(app.exec_())
```
Este bloque ejecuta la aplicación si el archivo se ejecuta como un script.



## **Carga y Lectura de la Señal EMG**  
El código permite al usuario abrir un archivo `.tdms` o `.csv` con datos de una señal EMG. Dependiendo del tipo de archivo, extrae la información relevante de tiempo y voltaje.  

### **Código Relacionado:**  
```python
def abrir_archivo(self):
    opciones = QFileDialog.Options()
    archivo, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo de Datos", "", "Archivos TDMS (*.tdms);;Archivos CSV (*.csv)", options=opciones)
    
    if archivo:
        try:
            if archivo.endswith(".tdms"):
                tdms_file = TdmsFile(archivo)
                self.tiempos = tdms_file["Tiempo"].data
                self.valores = tdms_file["Señal"].data
            elif archivo.endswith(".csv"):
                datos = pd.read_csv(archivo)
                self.tiempos = datos["Tiempo (s)"].values
                self.valores = datos["Voltaje (V)"].values
            
            # Determinar la frecuencia de muestreo
            fs = 1 / (self.tiempos[1] - self.tiempos[0]) if len(self.tiempos) > 1 else 1000

            # Aplicar el filtro pasabanda
            self.valores_filtrados = self.apply_bandpass_filter(self.valores, fs)
            self.mostrar_grafica()

        except Exception as e:
            self.label_info.setText(f"Error al abrir el archivo: {e}")
```
**Explicación:**  
- Se abre un cuadro de diálogo para seleccionar un archivo.  
- Se determina si el archivo es `.tdms` o `.csv` y se extraen los datos de tiempo y voltaje.  
- Se calcula la **frecuencia de muestreo (fs)** con la diferencia entre las dos primeras muestras de tiempo.  
- Se aplica el **filtro pasabanda (30 Hz - 300 Hz)** llamando a la función `apply_bandpass_filter()`.  
- Finalmente, se llama a `mostrar_grafica()` para visualizar la señal filtrada y sin filtrar.  

---

## **Filtrado de la Señal EMG**  
Se utiliza un **filtro pasabanda Butterworth** de cuarto orden con frecuencias de corte en **30 Hz y 300 Hz**.  

### **Código Relacionado:**  
```python
def butter_bandpass(self, lowcut, highcut, fs, order=4):
    nyquist = 0.5 * fs
    low = lowcut / nyquist
    high = highcut / nyquist
    b, a = butter(order, [low, high], btype='band', output='ba')
    return b, a

def apply_bandpass_filter(self, data, fs):
    b, a = self.butter_bandpass(30, 300, fs)
    return filtfilt(b, a, data)
```
**Explicación:**  
1. **`butter_bandpass()`**  
   - Calcula las frecuencias normalizadas (`low` y `high`) dividiendo entre la frecuencia de Nyquist.  
   - Genera los coeficientes del filtro Butterworth de cuarto orden (`b, a`).  

2. **`apply_bandpass_filter()`**  
   - Llama a `butter_bandpass()` para obtener los coeficientes del filtro.  
   - Aplica el filtro con `filtfilt()`, que **filtra en ambas direcciones** para evitar distorsiones en la señal.  

---

## **Visualización de la Señal EMG**  
El código genera una gráfica comparativa con la señal EMG antes y después del filtrado.  

### **Código Relacionado:**  
```python
def mostrar_grafica(self):
    plt.figure(figsize=(10, 5))
    plt.plot(self.tiempos, self.valores, label="Señal EMG sin filtrar", color="gray", alpha=0.5)
    plt.plot(self.tiempos, self.valores_filtrados, label="Señal EMG Filtrada", color="b")
    plt.xlabel("Tiempo (s)")
    plt.ylabel("Voltaje (V)")
    plt.title("Señal EMG - Comparación de Procesamiento")
    plt.legend()
    plt.grid(True)
    plt.show()
```
**Explicación:**  
- La señal **sin filtrar** se grafica en **gris** con opacidad (`alpha=0.5`) para visualizar el ruido presente.  
- La señal **filtrada** se grafica en **azul**, resaltando la actividad muscular sin interferencias.  
- Se incluyen etiquetas, título y leyenda para mejorar la interpretación.  

---
interfaz 

![image](https://github.com/user-attachments/assets/e59345a6-e8c2-4bb7-828c-7e4835159035)

señal 

![filtro](https://github.com/user-attachments/assets/f7ddd18d-bdc6-4254-8b26-abeb074c6484)

# Análisis del Filtrado de la Señal EMG y la Presencia de Valores Negativos


## **1. Eliminación de la Componente DC**  
La señal original (sin filtrar) suele tener una **componente de corriente continua (DC)**, que es un **desplazamiento positivo del voltaje**.  
- El filtro pasabanda con **30 Hz - 300 Hz** elimina **frecuencias por debajo de 30 Hz**, lo que incluye componentes de baja frecuencia y la DC.  
- Como resultado, la señal filtrada oscila alrededor de **0 V** en lugar de estar desplazada hacia valores positivos.  

### **Ejemplo Visual**  
Antes del filtrado (señal en gris), la señal puede estar desplazada hacia arriba por una componente DC.  
Después del filtrado (señal azul), la señal oscila alrededor del eje 0.  

---

## **2. Eliminación de Ruido de Baja Frecuencia (Inferior a 30 Hz)**  
Las señales EMG pueden contener **movimientos del electrodo** y artefactos de baja frecuencia (como el latido del corazón), que suelen estar por debajo de 30 Hz.  
- Estos artefactos suelen ser positivos y pueden contribuir a que la señal original no tenga valores negativos tan pronunciados.  
- Al eliminar estos artefactos, la señal filtrada **recupera su variabilidad natural**, lo que incluye valores negativos que representan la actividad real del músculo.  

---

## **3. El Filtro No Distingue Entre Valores Positivos y Negativos**  
El filtro pasabanda simplemente **permite el paso de frecuencias dentro del rango especificado (30 Hz - 300 Hz)** y elimina todo lo demás.  
- Como las señales EMG son **oscilatorias**, al eliminar ruido y componentes de baja frecuencia, la señal resultante **tendrá valores tanto positivos como negativos**.  
- Esto es completamente normal y no significa que la señal sea incorrecta.  

---

## **4. La Transformación del Filtro Digital**  
El filtrado se realiza con la función `filtfilt()`, que **aplica el filtro en ambas direcciones** para evitar desfases.  
```python
def apply_bandpass_filter(self, data, fs):
    b, a = self.butter_bandpass(30, 300, fs)
    return filtfilt(b, a, data)  # Filtro sin desfase
```
Esto significa que:  
- Se **eliminan tendencias de baja frecuencia**, lo que hace que la señal fluctúe más alrededor de cero.  
- La señal mantiene su forma original, pero ahora con valores más equilibrados entre positivos y negativos.  







