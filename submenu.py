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
mode = sys.argv[4]

if mode == "video":
   files = [os.path.join(subdir, media, f) for f in files]
   file_list = [[f, ["./video.sh", f]] for f in files]

if mode == "audio":
   file_list = [[f, ["./musica.sh", os.path.join(subdir, media), f]] for f in files]

if mode == "image":
   file_list = [[f, ["./pictures.sh", os.path.join(subdir, media), f]] for f in files]


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
      def __init__(self, gui, file_index):
         btn = tk.Button(gui, text=file_list[file_index][APP_NAME], width = 30, command = self.startApp)
         btn.pack()
         self.app_cmd = file_list[file_index][APP_CMD]
      def startApp(self):
         print("APP_CDM: %s" % self.app_cmd)
         runApplicatinThread(self.app_cmd).start()
root = tk.Tk()
root.title("Submenu")
for index, app in enumerate(file_list):
   runApplicatinThread.appButtons(root, index)
root.mainloop()
