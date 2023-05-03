import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QTableWidget, QTableWidgetItem,QHeaderView
from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtCore import QThread , pyqtSignal, QDateTime , QObject
import requests
import json
from time import sleep
from datetime import datetime
import subprocess
from threading import Thread
import pandas as pd
 
## CLASE PARA ACCION DEL THREAD ##
class BackendThread(QObject):
    refresh = pyqtSignal(list,bool)
    ip_api= 'http://localhost:5000/'
    list_all_envios: list
    server: bool

    def run(self):
        
        while True:
            
            try:
                all_datos = requests.get(f'{self.ip_api}videos',timeout=4)
                server = True
            except (requests.exceptions.ConnectionError):
                print('Server INACTIVO...Conectando...')
                list_all_datos=[]
                server = False
                self.refresh.emit(list_all_datos,server)
                continue
                
            if server==True:
                server = True
                json_all_datos = all_datos.json()
                list_all_datos = [dict(id_item) for id_item in json_all_datos]
                self.refresh.emit(list_all_datos,server)
                self.respuesta_server=False
                sleep(1)
            else:
                info_server = ' '
                server = False
                list_all_datos.append(info_server)
                self.refresh.emit(list_all_datos,server)
                list_all_datos= []
                sleep(1)
                
   

## CLASE PARA CREAR Y EJECUTAR INTERFAZ GRAFICA (GUI)
class gui_video(QMainWindow):
    ip_api= 'http://localhost:5000/'
    
    def __init__(self):
        super().__init__()
        uic.loadUi("gui_video.ui",self)
        
        ## NOMBRE VENTANA ##
        self.setWindowTitle('Servidor Camara Seguridad')
        

        ## LOGO ##
        pixmap1 = QPixmap('logo.png')
        self.logo.setPixmap(pixmap1)

        ## LOGO ##
        pixmap2 = QPixmap('img_fondo.jpg')
        self.fondo.setPixmap(pixmap2)

        ## THREAD ## 
        self.backend = BackendThread() 
        self.backend.refresh.connect(self.visualizar)
        self.thread = QThread()
        self.backend.moveToThread(self.thread)
        self.thread.started.connect(self.backend.run)
        self.thread.start()

        ## SELECCION LISTADO ##
        self.list_categorias = ['Vacio']    
        self.list_categorias.sort()
        self.cbox_listado.addItems(self.list_categorias)
        #self.cbox_listado.activated.connect(self.seleccion_categoria)

        ## VARIABLES AUXILIARES ##
        self.list_categorias = []
        self.listado_datos = []
        self.categoria_seleccionada = str
        self.envio_datos = {}
    
    ## FECHA ACTUAL ##
    def fecha_actual(self):
        ahora = datetime.now()
        formato = "%d-%m-%Y %H:%M"
        fecha_hora_actual = ahora.strftime(formato)
        return fecha_hora_actual

    #def seleccion_categoria(self,listado_datos):
        
        
    ## VISUALIZAR DE BdD A GUI ##
    def visualizar(self,list_all_datos,server):
        fecha = self.fecha_actual()
        self.out_fecha.setText(fecha)
        
        self.listado_datos = []
        self.cbox_listado.clear()
        for n in range(0,len(list_all_datos)):
            self.listado_datos.append(list_all_datos[n]['video'])
        print(f'Listado de datos {self.listado_datos}')
        self.listado_datos.sort()
        self.cbox_listado.addItems(self.listado_datos)



def run_gui():
    app = QApplication(sys.argv)
    GUI = gui_video()
    GUI.show()
    sys.exit(app.exec_()) 

if __name__ == '__main__':
    run_gui()
    