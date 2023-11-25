
# Importar librerias básicas
from PyQt5.QtWidgets import  QApplication,QMainWindow, QDialog, QMessageBox, QFileDialog, QWidget
from PyQt5 import QtWidgets
from PyQt5.uic import loadUi;
from PyQt5.QtGui import QIntValidator, QRegExpValidator
from PyQt5.QtCore import Qt,QRegExp
from PyQt5.QtGui import QPixmap, QImage
import sys
import numpy as np
import os
import pydicom
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class VentanaPrincipal(QMainWindow):
    #constructor
    def __init__(self, ppal=None):
        super(VentanaPrincipal,self).__init__(ppal)
        loadUi('VentanaLogin.ui',self)
        self.setup()
    #metodo para configurar las senales-slots y otros de la interfaz
    def setup(self):
        #se programa la senal para el boton
        self.boton_ingresar.clicked.connect(self.accion_ingresar)

    def asignarControlador(self,c):
        self.__controlador = c

    def abrirVentImagen(self):
        ventana_imagen=VentanaImagen(self)
        self.hide()
        ventana_imagen.show()


    def accion_ingresar(self):
        usuario = self.campo_usuario.text()
        password = self.campo_password.text()
        #esta informacion la debemos pasar al controlador
        resultado = self.__controlador.validar_usuario(usuario,password)
        
        #se selecciona el resultado de acuerdo al resultado de la operacion
        if resultado == True:
            self.abrirVentImagen()
        else:
            #se crea la ventana de resultado
            msg = QMessageBox(self)
            msg.setIcon(QMessageBox.Information)
            msg.setWindowTitle("Ingreso")
            msg.setText("Usuario no Valido")
            #se muestra la ventana
            msg.show()

    
class VentanaImagen(QDialog):
    def __init__(self, ppal=None):
        super().__init__(ppal)
        loadUi('Imagen.ui',self)
        self.__VentanaPadre = ppal
        self.setup()
    
    def setup(self):
        self.canvas = FigureCanvas(plt.Figure())
        self.verticalLayout.addWidget(self.canvas)
        self.abrirCarpeta.clicked.connect(self.seleccionar_carpeta)
        self.sliderImagen.valueChanged.connect(self.actualizar_imagen)
        self.imagenes_dicom = []
        self.salirB.clicked.connect(self.salir)

    def seleccionar_carpeta(self):
        carpeta_seleccionada = QFileDialog.getExistingDirectory(self, 'Seleccionar Carpeta de Imágenes DICOM')
        self.imagenes_dicom = [os.path.join(carpeta_seleccionada, archivo) for archivo in os.listdir(carpeta_seleccionada) if archivo.lower().endswith('.dcm')]
        
        if self.imagenes_dicom:
            self.sliderImagen.setRange(0, len(self.imagenes_dicom) - 1)
            self.sliderImagen.setValue(0)
            self.actualizar_imagen()

    def actualizar_imagen(self):
        indice = self.sliderImagen.value()
        if 0 <= indice < len(self.imagenes_dicom):
            imagen_dicom_path = self.imagenes_dicom[indice]
            dataset = pydicom.dcmread(imagen_dicom_path)
            
            # Convertir la imagen DICOM a formato numpy
        imagen_array = dataset.pixel_array
        self.canvas.figure.clf()
        ax = self.canvas.figure.add_subplot(111)
        ax.imshow(imagen_array, cmap='gray')
        ax.axis("off")
        self.canvas.draw()

        #Sacamos la información y creamos el label
        nombre_Pac = dataset[0x0010,0x0010].value
        id = dataset[0x0010,0x0020].value
        sex = dataset[0x0010,0x0040].value
        modalidad= dataset[0x0008,0x0060].value
        desc= dataset[0x0008,0x1030].value
        self.infoimagen.setText(f'''
                                Nombre: {nombre_Pac}
                                Id: {id}
                                Sexo: {sex}
                                Modalidad: {modalidad}
                                Descripción del estudio: {desc}''')
    def salir(self):
        self.__VentanaPadre.campo_password.clear()
        self.__VentanaPadre.campo_usuario.clear()
        self.close() 
        self.__VentanaPadre.show()    
            


    
    
       
    
    
    
    
    
    

        

        
        