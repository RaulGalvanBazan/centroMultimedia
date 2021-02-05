#! /usr/bin/python3
# menu.py
import tkinter as tk
from subprocess import call
import threading
import os
import mimetypes

mimetypes.init()

#Se revisa si hay una usb conectada usando la biblioteca os
#se listan los subdirectorios en /media/pi que es
#en donde se hace el montaje de los dispositivos usb
media = "/media/pi"
subDirs = [dir.name for dir in os.scandir(media) if dir.is_dir()]
usb = []

#Definiendo las aplicaciones
#["Nombre de App", "comando"]
#netflix = ["Netflix", ["./start.sh", "www.netflix.com"]]
#amazonPrime = ["Amazon", ["./start.sh", "www.primevideo.com"]]
mubi = ["Mubi", ["./start.sh", "www.mubi.com"]]
spotify = ["Spotify", ["./start.sh", "http://open.spotify.com"]]
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
      if len(mediaType) == 1 and mediaType[0] == 'audio':
         usb.append(["USB-" + name, ["./musica.sh", subdir]])
      elif len(mediaType) == 1 and mediaType[0] == 'video':
         files = [f.name for f in files]
         usb.append(["USB-" + name, ["./submenu.py", media, name, " ".join(files), "video"]])
      elif len(mediaType) == 1 and mediaType[0] == 'image':
         files = [f.name for f in files]
         usb.append(["USB-" + name, ["./pictures.sh", subdir, " ".join(files)]])
      elif len(mediaType) > 1:
         files = [f.name for f in files]
         usb.append(["USB-" + name, ["./submenuMixed.py", media, name, " ".join(files), " ".join(fileTypes)]])
else:
   usb.append(["Scan USB", ["./restart.sh"]])

app_list = [mubi, spotify] + usb

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
         btn = tk.Button(gui, text=app_list[app_index][APP_NAME], width = 30, command = self.startApp)
         btn.pack()
         self.app_cmd = app_list[app_index][APP_CMD]
      def startApp(self):
         print("APP_CDM: %s" % self.app_cmd)
         runApplicatinThread(self.app_cmd).start()
root = tk.Tk()
root.title("Menu")
for index, app in enumerate(app_list):
   runApplicatinThread.appButtons(root, index)
root.mainloop()
