#! /usr/bin/python3
# submenu.py
import tkinter as tk
from subprocess import call
import threading
import os
import sys
import mimetypes

mimetypes.init()
subdir = sys.argv[0]
media = sys.argv[1]

#Se listan todos los archivos de video
files = [f for f in os.scandir(os.path.join(subdir, media)) if f.is_file()]
file_list = [[f.name, ["./video.sh", os.path.join(subdir, f)]] for f in files]

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
