import serial
import numpy as np
import matplotlib.pyplot as plt
import scipy as sp

import tkinter as tk
from tkinter import ttk
from RangeSlider.RangeSlider import RangeSliderH, RangeSliderV
from datetime import datetime
import time
import pygame



class experiment():

    def __init__(self):
        self.GUI()
        self.callibrationSequence()
        self.experiment_loop()
        self.analyse()
        self.displayResult()


    def GUI(self):
        
        """Interface garphique"""

        self.window = tk.Tk()
        self.window.title("Estimateurs de paramètre du modèle de moteur à induction")

        frame = tk.Frame(self.window)
        frame.pack()

        COM_info_frame =tk.LabelFrame(frame, text="Paramètres de communication")
        COM_info_frame.grid(row= 0, column=0, padx=20, pady=10)
        
        baud_label = tk.Label(COM_info_frame, text="Baudrate")
        baud_label.grid(row=0, column=0)
        self.baud_combobox = ttk.Combobox(COM_info_frame, values=[9600, 19200, 2880, 38400, 5700, 76800, 115200, 230400, 460800, 576000, 921600])
        self.baud_combobox.current(10)
        self.baud_combobox.grid(row=0, column=1)
            
        port_label = tk.Label(COM_info_frame, text="Port")
        port_label.grid(row=1, column=0)
        self.port_entry = tk.Entry(COM_info_frame, width=10)
        self.port_entry.insert(0, "COM3")
        self.port_entry.grid(row=1, column=1)

        for widget in COM_info_frame.winfo_children(): #espace entre les trucs
            widget.grid_configure(padx=90, pady=10)


        acquisition_info_frame =tk.LabelFrame(frame, text="Paramètres d'acquisition")
        acquisition_info_frame.grid(row= 1, column=0, padx=20, pady=10)

        temps_label = tk.Label(acquisition_info_frame, text= "Durée d'acquisition par point (s)")
        temps_label.grid(row=0, column=0)
        self.temps_entry = tk.Entry(acquisition_info_frame, width=5, justify="center")
        self.temps_entry.insert(0, 1)
        self.temps_entry.grid(row=0, column=1)


        freq_label = tk.Label(acquisition_info_frame, text="Plage de fréquences d'excitation(Hz)")
        freq_label.grid(row=1, column=0)
        hLeft = tk.DoubleVar(value=10)
        hRight = tk.DoubleVar(value=150)
        self.freq_rangeSlider = RangeSliderH(acquisition_info_frame, [hLeft, hRight], padX=20, min_val=0,
                                            max_val=300, Width=350, Height=40, bar_radius=5, font_size=11, 
                                                font_family="TkDefaultFont", bgColor=self.window.cget('bg'))
        self.freq_rangeSlider.grid(row=1, column=1)

        Npts_label = tk.Label(acquisition_info_frame, text="Nombres de points")
        Npts_label.grid(row=2,column=0)
        Npts_var = tk.DoubleVar(value=10)
        self.Npts_spinbox = tk.Spinbox(acquisition_info_frame, from_=1, to="infinity", textvariable=Npts_var, width=5)
        self.Npts_spinbox.grid(row=2, column=1)

        freq_acquisition_label = tk.Label(acquisition_info_frame, text="Fréquence d'échantillonage (Hz)")
        freq_acquisition_label.grid(row=3, column=0)
        self.freq_acquisition_entry = tk.Entry(acquisition_info_frame)
        self.freq_acquisition_entry.insert(0, 6000)
        self.freq_acquisition_entry.grid(row=3, column=1)
        
        
        for widget in acquisition_info_frame.winfo_children(): #espace entre les trucs
            widget.grid_configure(padx=10, pady=10)


        export_info_frame = tk.LabelFrame(frame)
        export_info_frame.grid(row=2, column=0)

        fich_frame = tk.Frame(export_info_frame)
        fich_frame.grid(row=0, column=0)


        fich_label = tk.Label(fich_frame, text="Nom du fichier:")
        fich_label.grid(row=0, column=0)
        self.fich_entry = tk.Entry(fich_frame, width=50, justify="center")
        self.fich_entry.insert(0, datetime.now().strftime("Data/exp_du_%m-%d-%Y_%Hh%M.txt"))
        self.fich_entry.grid(row=0, column=1)

        button = tk.Button(export_info_frame, text="Démarrer l'échantillonage", command=self.setValues, width=40,)
        button.grid(row=1, column=0)

        for widget in export_info_frame.winfo_children(): #espace entre les trucs
            widget.grid_configure(padx=90, pady=10)

        self.window.mainloop()

    def setValues(self):
        self.baudrate = self.baud_combobox.get()
        self.time = float(self.temps_entry.get())
        self.port = self.port_entry.get()
        self.freq_range = self.freq_rangeSlider.getValues()
        self.file_name = self.fich_entry.get()
        self.Npts = int(self.Npts_spinbox.get())
        self.samplingRate = float(self.freq_acquisition_entry.get())
        self.window.destroy()

    def callibrationSequence(self):
        print("Callibration...", end='')
        
        n = 10
        # for i in range(n):
        #     self.generateSound()

        
        time.sleep(0.5)
        print('\r                            \r', end="") 
        pass

    def experiment_loop(self):
        self.freqs = np.linspace(*self.freq_range, self.Npts)
        
        self.ser = serial.Serial(
        port=self.port,
        baudrate=self.baudrate,
        timeout=1)
        
        with open(self.file_name, 'a') as file:
                file.write(f"Baudrate: {self.baudrate}\nPort: {self.port}\nDuree par point: {self.time}\nPalge de frequences: {self.freq_range}\nNombre de points: {self.Npts}\nSamplingRate: {self.samplingRate}\n")

        for i, freq in enumerate(self.freqs):
            freq = int(freq)
            
            with open(self.file_name, 'a') as file:
                file.write(f'\n\nFrequence #{i+1}: {freq} Hz\n')
            
            self.sourceInstruction(freq)
            #self.generateSound(freq, self.time + 0.5)
            print(f"Test {i+1} sur {self.Npts}. Fréquence: {freq:.1f} Hz                  \r", end="")

            samplingBytesNumber = int(self.samplingRate*self.time*16)#14 = num de char par ligne

            self.ser.flush() # CLEAR SERIAL BUFFER
            with open(self.file_name, 'ab') as file:
                while samplingBytesNumber > 0:
                    t1 = time.time()

                    inWaiting = self.ser.inWaiting()
                    if (inWaiting > 0):
                        file.write(self.ser.read(self.ser.inWaiting()) )
                        samplingBytesNumber -= inWaiting
            self.check_saturation()
            #self.sound.stop()
            time.sleep(1)
        self.ser.close()

    def generateSound(self, freq, duration):
        
        """Pour un générateur de fonction basé sur un système audio."""

        sampleRate = 44100
        pygame.mixer.init(sampleRate,-16,1,2**16)
        arr = np.array([4096 * np.sin(2.0 * np.pi * freq * x / sampleRate) for x in range(0, int(sampleRate*self.time+1))]).astype(np.int16)
        arr2 = np.c_[arr,arr]
        #plt.plot(arr)
        #plt.show()
        self.sound = pygame.sndarray.make_sound(arr2)
        self.sound.play(-1)

    def sourceInstruction(self, freq):

        """ Pour un générateur de fonction nécessitant une intervention humaine. """


        self.instructionWindow = tk.Tk()
        self.instructionWindow.title("Instructions")
        
        frame = tk.Frame(self.instructionWindow)
        frame.pack()

        instruction_label = tk.Label(frame, text=f"Veuillez régler le générateur de fonction à {freq} Hz.", font=("TkDefaultFont", 18))
        instruction_label.grid(row=0, column=0)
        button = tk.Button(frame, text="Poursuivre l'échantillonage", command=self.instructionWindow.destroy, width=40, height=5, bg='white')
        button.grid(row=1, column=0)


        for widget in frame.winfo_children(): #espace entre les trucs
            widget.grid_configure(padx=20, pady=30)
        
        self.instructionWindow.mainloop()

    def check_saturation(self):
        pass

    def analyse(self):
        """ Analyse les données et trouve: courbes d'impédance, paramètres du modèle, courbes de couple/puissance/efficacité"""
        pass

    def displayResult(self):
        """ affiche les résultats de l'expérience en cours ou d'une expérience passée"""
        pass


experiment()