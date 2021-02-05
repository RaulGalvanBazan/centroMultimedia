#! /usr/bin/python3
# submenu.py
import tkinter as tk
from subprocess import call
import threading
import os
import sys
import mimetypes

mimetypes.init()
subdir = sys.argv[1]
media = sys.argv[2]
files = sys.argv[3].split(" ")
mediaType = sys.argv[4].split(" ")

print(files)
print(mediaType)

def guessType(path):
   fileType = mimetypes.guess_type(path)[0]
   if fileType != None:
            return fileType.split("/")[0]

#Se enlistan todos los archivos
#media = os.path.join(subdir, media)
#files = [f for f in os.scandir(media) if f.is_file()]
#Se obtiene el tipo de archivo para cada archivo
#fileTypes = [guessType(f) for in in files]
#Se separan los archivos por tipo:

videoFiles = []
audioFiles = []
imageFiles = []
for i in range(len(files)):
   videoFiles.append(files[i]) if mediaType[i] == "video" else \
   audioFiles.append(files[i]) if mediaType[i] == "audio" else \
   imageFiles.append(files[i]) if mediaType[i] == "audio" else None

action_list = []

if videoFiles: 
   action_list.append(["Reproducir Videos", \
   ["./submenu.py", subdir, media, " ".join(videoFiles), "video"]])
if audioFiles:
   action_list.append(["Reproducir Musica", \
   ["./submenu.py", subdir, media, " ".join(audioFiles), "audio"]])
if imageFiles:
   action_list.append(["Reproducir Imagenes", \
   ["./submenu.py", subdir, media, " ".join(imageFiles), "image"]])



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
root.title("SubmenuMix")
for index, app in enumerate(action_list):
   runApplicatinThread.appButtons(root, index)
root.mainloop()
