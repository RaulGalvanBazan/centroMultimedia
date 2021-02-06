#! /usr/bin/python3
# menu.py
import tkinter as tk
from subprocess import call
import threading
import os
import mimetypes
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
   #no exista, por tal motivo se usa un try
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
      for name in subDirs:
         subdir = os.path.join(media, name)
         files = [f for f in os.scandir(subdir) if f.is_file()]
         mediaType = []
         fileTypes= []
         for f in files:
            fileType = mimetypes.guess_type(os.path.join(subdir, f))[0]
            if fileType != None:
               fileType = fileType.split("/")[0]
               fileTypes.append(fileType)
               mediaType.append(fileType) if fileType not in mediaType else mediaType
         
         files = [f.name for f in files]
         if len(mediaType) == 1 and mediaType[0] == 'audio':
            usb.append(["USB-" + name, ["./action.sh", subdir, "audio", " ".join(files)]])
         elif len(mediaType) == 1 and mediaType[0] == 'video':
            usb.append(["USB-" + name, ["./submenu.sh", subdir, " ".join(files), "video", "listFiles"]])
         elif len(mediaType) == 1 and mediaType[0] == 'image':
            usb.append(["USB-" + name, ["./action.sh", subdir, "image", " ".join(files)]])
         elif len(mediaType) > 1:
            usb.append(["USB-" + name, ["./submenuMixed.sh", subdir, " ".join(files), " ".join(fileTypes)]])
   else:
      usb.append(["Scan USB", ["./restart.sh"]])
   
   menuName = "Menú Principal"
   action_list = [mubi, spotify] + usb

elif (len(sys.argv)) == 4:

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
   menuName = "Elige la accion"

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


elif (len(sys.argv)) == 5:
   subdir = sys.argv[1]
   files = sys.argv[2].split(" ")
   mode = sys.argv[3]

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

class runApplicatinThread(threading.Thread):
   def __init__(self, app_cmd):
      threading.Thread.__init__(self)
      self.cmd = app_cmd
   def run(self):
      try:
      	cmd = call(self.cmd)
      except:
         print("No se puede correr: %s" % self.cmd)

   class appButtons:
      def __init__(self, gui, app_index):
         btn = tk.Button(gui, text=action_list[app_index][APP_NAME], width = 30, command = self.startApp)
         btn.pack()
         self.app_cmd = action_list[app_index][APP_CMD]
      def startApp(self):
         print("APP_CDM: %s" % self.app_cmd)
         runApplicatinThread(self.app_cmd).start()
root = tk.Tk()
root.title(menuName)
for index, app in enumerate(action_list):
   runApplicatinThread.appButtons(root, index)
root.mainloop()
