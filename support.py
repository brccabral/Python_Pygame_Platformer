from os import walk
from os.path import join
import sys

def resource_path(relative):
    if hasattr(sys, "_MEIPASS"):
        return join(sys._MEIPASS, relative)
    return join(relative)

def import_folder(path):
    for _,__,img_files in walk(path):
        print(img_files)

import_folder('assets/graphics/character/run')