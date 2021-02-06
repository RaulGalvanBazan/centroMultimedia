#! /usr/bin/python3
# menu.py
'''
Crea una interfaz con diferentes opciones:
--Al inicio se muestran opciones para acceder a servicios de streaming
  y para acceder a una usb conectada. 
  +-Si no hay una usb conectada al inicio del programa, el botón de la
    usb hará primero un escaneo a la ruta de montaje de los dispositivos 
    usb. Si encuentra un dispositivo, se reinicia la interfaz y el botón
    de la usb ahora accede a nuevas opciones
  +-Si existe una usb conectada al inicio del programal el escaneo es 
    automático.

--Las opciones para la usb varían dependiendo del tipo de archivos que 
  se encuentren en ella. Este programa solo toma en cuenta los archivos 
  de audio, video e imagen. El programa no explora subcarpetas.
  +-Si la usb contiene solo archivos de audio, se reproducen todas las pistas.
  +-Si la usb contien solo archivos de video, se despliega un nuevo menú
    en donde se puede elegir el video para ser reproducido.
  +-Si la usb contiene solo archivos de imagen, se reproducen todas las
    imágenes.
  +-Si la usb contiene archivos de diferentes tipos, se despliega un nuevo
    menú donde se puede elegir la acción a realizar.
  +-Se puede elegir el botón de "Atrás" para regresar al menú principal.

--Para reproducir cualquier tipo de contenido, el programa se apoya en 
  scripts de bash para lanzar la aplicación correspondiente. Los servicios
  de streaming se reproducen en el navegador Firefox, mientras que los
  archivos multimedia se reproducen en la aplicación vlc.

Autores:
  Fernández Mora JosÉ Enrique
  Galván Bazán Raúl
  Sánchez Castillo Paola

Licencia: MIT

'''
#Biblioteca para crear la interfaz gráfica
import tkinter as tk
#Función para correr un comando 
from subprocess import call
#Módulo para crear hilos
import threading
#Módulo para interactuar con el sistema operativo
import os
#Módulo para obtener el tipo de archivo
import mimetypes
#Módulo para acceder a las variables del intérprete
import sys

mimetypes.init()

#Si se recibe un solo argumento significa que se quiere lanzar
#el menú principal
if (len(sys.argv)) == 1:
   #Se revisa si hay una usb conectada usando la biblioteca os
   #se listan los subdirectorios en /media/pi que es
   #en donde se hace el montaje de los dispositivos usb
   media = "/media/pi"
   #Si no se ha conectado una usb es posible que la ruta /media/pi
   #no exista, por tal motivo se usa un bloque try
   try:
      subDirs = [dir.name for dir in os.scandir(media) if dir.is_dir()]
   except:
      subDirs = []
   usb = []

   #Definiendo las aplicaciones que se pueden utilizar
   #["Nombre de App", "comando"]
   #Algunos ejemplos de los servicios de streaming que se pueden usar:
   #netflix = ["Netflix", ["./start.sh", "www.netflix.com"]]
   #amazonPrime = ["Amazon", ["./start.sh", "www.primevideo.com"]]
   mubi = ["Mubi", ["./start.sh", "www.mubi.com"]]
   spotify = ["Spotify", ["./start.sh", "http://open.spotify.com"]]
   #Si se encontró al menos un subdirectorio en /media/pi significa que 
   #hay al menos una usb conectada. En este caso el código está hecho para
   #reconocer solo una usb pero se puede adaptar para más
   if len(subDirs) > 0:
      #Se obtiene el nombre de la usb
      for name in subDirs:
         subdir = os.path.join(media, name)
         #Se obtienen los archivos en la usb
         files = [f for f in os.scandir(subdir) if f.is_file()]
         mediaType = []
         fileTypes= []
         #Se obtiene el tipo de archivo para cada archivo
         for f in files:
            fileType = mimetypes.guess_type(os.path.join(subdir, f))[0]
            if fileType != None:
               fileType = fileType.split("/")[0]
               fileTypes.append(fileType)
               mediaType.append(fileType) if fileType not in mediaType else mediaType
         
         #Se crean nuevas opciones para el menú dependiendo del tipo de archivo
         files = [f.name for f in files]
         if len(mediaType) == 1 and mediaType[0] == 'audio':
            usb.append(["USB-" + name, ["./action.sh", subdir, "audio", " ".join(files)]])
         elif len(mediaType) == 1 and mediaType[0] == 'video':
            usb.append(["USB-" + name, ["./submenu.sh", subdir, " ".join(files), "video", "listFiles"]])
         elif len(mediaType) == 1 and mediaType[0] == 'image':
            usb.append(["USB-" + name, ["./action.sh", subdir, "image", " ".join(files)]])
         elif len(mediaType) > 1:
            usb.append(["USB-" + name, ["./submenuMixed.sh", subdir, " ".join(files), " ".join(fileTypes)]])
   #Si no hay una usb conectada, se agrega la opción para escanear la ruta nuevamente
   else:
      usb.append(["Scan USB", ["./restart.sh"]])

   menuName = "Menú Principal"
   #Lista de las opciones de streaming + las usb
   action_list = [mubi, spotify] + usb

#Crea un nuevo menú dependiendo de los archivos que se encuentren en la usb
#Este menú se despliega cuando la usb tiene archivos de tipos diferentes.
elif (len(sys.argv)) == 4:
   #Se obtienen los argumentos
   subdir = sys.argv[1]
   files = sys.argv[2].split(" ")
   mediaType = sys.argv[3].split(" ")

   #Se separan los archivos por tipo:
   videoFiles = []
   audioFiles = []
   imageFiles = []
   for i in range(len(files)):
      videoFiles.append(files[i]) if mediaType[i] == "video" else \
      audioFiles.append(files[i]) if mediaType[i] == "audio" else \
      imageFiles.append(files[i]) if mediaType[i] == "image" else None
   
   action_list = []
   #Se crean las opciones de la interfaz dependiendo del tipo de los
   #archivos que se encuentren en la usb
   if videoFiles: 
      action_list.append(["Reproducir Videos", \
      ["./submenu.sh", subdir, " ".join(videoFiles), "video", "listFiles"]])
      
   if audioFiles:
      print(audioFiles)
      action_list.append(["Reproducir toda la música", \
      ["./action.sh", subdir, "audio", " ".join(audioFiles)]])
      action_list.append(["Seleccionar canción", \
      ["./submenu.sh", subdir," ".join(audioFiles), "audio", "listFiles"]])
      
   if imageFiles:
      action_list.append(["Reproducir todas las imágenes", \
      ["./action.sh", subdir, "image", " ".join(imageFiles)]])
      
      action_list.append(["Seleccionar la imagen", \
      ["./submenu.sh", subdir, " ".join(imageFiles), "image", "listFiles"]])
      
   action_list.append(["Atrás", ["./action.sh", "kill"]])
   menuName = "Elige la accion"


#Si se recibien 5 argumentos se enlistan los archivos multimedia 
#para seleccionarlos uno a uno.
#Este menú se despliega cuando la usb tiene solo archivos de video
#o si se selecciona la opción para elegir el archivo a reproducir
elif (len(sys.argv)) == 5:
   subdir = sys.argv[1]
   files = sys.argv[2].split(" ")
   mode = sys.argv[3]
   
   #Se enlistan los archivos multimedia dependiendo del tipo
   if mode == "video":
      action_list = [[f, ["./action.sh", subdir, "video", f]] for f in files]

   if mode == "audio":
      action_list = [[f, ["./action.sh", subdir, "audio", f]] for f in files]

   if mode == "image":
      action_list = [[f, ["./action.sh", subdir, "image", f]] for f in files]
   
   action_list.append(["Atrás", ["./action.sh", "kill"]])
   
   menuName = "Elige el archivo"


APP_NAME = 0
APP_CMD = 1
'''
Clase que hereda las características de threading.Thread para 
ejecutar las funciones en nuevos hilos de ejecución.
Este está basado en la sección "Using Python for Automation and
Productivity" del libro "Raspberry Pi Cookbook for Python Programmers"
de Tim Cox
'''
class runApplicatinThread(threading.Thread):
   def __init__(self, app_cmd):
      threading.Thread.__init__(self)
      self.cmd = app_cmd
   def run(self):
      try:
      	cmd = call(self.cmd)
      except:
         print("No se puede correr: %s" % self.cmd)
   '''
   Se crea una nueva clase que sirve como base para la creación de los
   botones de la interfaz. Cada item en el menu se compone de:
   -Nombre de la acción: APP_NAME
   -Acción a realizar: APP_CMD
   Ambos campos se encuentran almacenados en la lista action_list, creada
   en alguno de los campos anteriores
   '''
   class appButtons:
      def __init__(self, gui, app_index):
         btn = tk.Button(gui, text=action_list[app_index][APP_NAME], width = 30, command = self.startApp)
         btn.pack()
         self.app_cmd = action_list[app_index][APP_CMD]
      '''
      Este método se encarga de ejecutar la acción para cada opción
      en un nuevo hilo
      '''   
      def startApp(self):
         print("APP_CDM: %s" % self.app_cmd)
         runApplicatinThread(self.app_cmd).start()
root = tk.Tk()
root.title(menuName)
for index, app in enumerate(action_list):
   runApplicatinThread.appButtons(root, index)
root.mainloop()
