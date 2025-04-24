import os     
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import butter, filtfilt, windows, convolve, find_peaks
from scipy.fftpack import fft, fftfreq
from nptdms import TdmsFile
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QFileDialog

class EMGApp(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        self.setWindowTitle("Análisis de EMG")
        self.layout = QVBoxLayout()
        
        self.boton_abrir = QPushButton("Abrir Archivo de Datos")
        self.boton_abrir.clicked.connect(self.abrir_archivo)
        self.layout.addWidget(self.boton_abrir)
        
        self.label_info = QLabel("Información de la señal EMG aparecerá aquí después de abrir un archivo.")
        self.layout.addWidget(self.label_info)
        
        self.setLayout(self.layout)

    def apply_hamming_window(self, data):
        window_size = min(len(data), 101)  # Tamaño de la ventana
        window = windows.hamming(window_size)
        window /= np.sum(window)
        return convolve(data, window, mode='same')
    
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
                
                fs = 1 / (self.tiempos[1] - self.tiempos[0]) if len(self.tiempos) > 1 else 1000
                self.valores_ventana = self.apply_hamming_window(self.valores)
                self.identificar_contracciones(fs)
                
            except Exception as e:
                self.label_info.setText(f"Error al abrir el archivo: {e}")
    
    def identificar_contracciones(self, fs):
        duracion_minima = int(0.6 * fs)  # Cambiado a 0.5 segundos
        picos, _ = find_peaks(self.valores, height=2.5, distance=duracion_minima)
        
        self.contracciones = []
        self.tiempos_contracciones = []
        for p in picos:
            inicio = max(0, p - duracion_minima // 2)
            fin = min(len(self.valores), p + duracion_minima // 2)
            self.contracciones.append(self.valores_ventana[inicio:fin])
            self.tiempos_contracciones.append((self.tiempos[inicio], self.tiempos[fin]))
        
        self.analizar_frecuencia(fs)
    
    def analizar_frecuencia(self, fs):
        total_contracciones = len(self.contracciones)
        for i in range(0, total_contracciones, 6):
            fig, axs = plt.subplots(2, 3, figsize=(15, 10))
            axs = axs.flatten()
            
            for j, (contraccion, (t_inicio, t_fin)) in enumerate(zip(self.contracciones[i:i+6], self.tiempos_contracciones[i:i+6])):
                n = len(contraccion)
                frecuencia = fftfreq(n, d=1/fs)
                espectro = np.abs(fft(contraccion))
                
                frecuencia_dominante = np.sum(frecuencia * espectro) / np.sum(espectro)
                frecuencia_media = np.sum(frecuencia * espectro) / np.sum(espectro)
                desviacion_estandar = np.sqrt(np.sum((frecuencia - frecuencia_media)**2 * espectro) / np.sum(espectro))
                
                print(f"Contracción {i+j+1} (Tiempo: {t_inicio:.2f}s - {t_fin:.2f}s):")
                print(f"  Frecuencia Dominante: {frecuencia_dominante:.2f} Hz")
                print(f"  Frecuencia Media: {frecuencia_media:.2f} Hz")
                print(f"  Desviación Estándar: {desviacion_estandar:.2f} Hz")
                
                axs[j].plot(frecuencia[:n//2], espectro[:n//2])
                axs[j].set_xscale("log")
                axs[j].set_xlabel("Frecuencia (Hz)")
                axs[j].set_ylabel("Amplitud")
                axs[j].set_title(f"Contracción {i+j+1}")
                axs[j].grid(True)
            
            plt.tight_layout()
            plt.show()

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ventana = EMGApp()
    ventana.show()
    sys.exit(app.exec_())

    sys.exit(app.exec_())
