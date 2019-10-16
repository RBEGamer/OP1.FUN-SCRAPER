import os
import shutil
from zipfile import ZipFile
from distutils.dir_util import copy_tree

ZIP_FILES_PATH = "/Users/path/to/the/zip/folders/...."
UNPACK_TO = "/Users/paths/to/unpack/folder/...."

if not os.path.exists(UNPACK_TO):
    os.makedirs(UNPACK_TO)
    os.makedirs(os.path.join(UNPACK_TO, "drum"))
    os.makedirs(os.path.join(UNPACK_TO, "synth"))
    os.system("sudo chmod 0777 -R " + UNPACK_TO)
if not os.path.exists(ZIP_FILES_PATH):
    os.makedirs(ZIP_FILES_PATH)
    os.system("sudo chmod 0777 -R " + ZIP_FILES_PATH)

homeDirLst = os.listdir(ZIP_FILES_PATH)
zipLst = []
for i in homeDirLst:
    if ".zip" in i:
        zipLst.append(i)

print("=============================")
for i in zipLst:
    print(i)
print("=============================")
print("Found ---" + str(len(zipLst)) + "--- Pack Zips")
print("Do you want to continue? (Y/N) ")
userInput = input().lower()
if userInput == "y":
    for i in zipLst:
        print("Unpacking: " + str(i))
        tempUnpackPath = os.path.join(UNPACK_TO, "temp")
        with ZipFile(os.path.join(ZIP_FILES_PATH, i), 'r') as zipObj:
            zipObj.extractall(tempUnpackPath)

        if "drum" in os.listdir(tempUnpackPath) and "synth" in os.listdir(tempUnpackPath):
            c = os.path.join(tempUnpackPath, "drum")
            s = os.path.join(tempUnpackPath, "drum")
            cl = os.listdir(c)
            for i in cl:
                if i.startswith("."):
                    cl.remove(i)
            dP = os.path.join(c, cl[0])
            sP = os.path.join(s, cl[0])
            try:
                copy_tree(dP, os.path.join(os.path.join(UNPACK_TO, "drum"), cl[0]))
                copy_tree(sP, os.path.join(os.path.join(UNPACK_TO, "synth"), cl[0]))
            except IOError:
                print("Unpack Error")

        elif "drum" in os.listdir(tempUnpackPath):
            c = os.path.join(tempUnpackPath, "drum")
            cl = os.listdir(c)
            for i in cl:
                if i.startswith("."):
                    cl.remove(i)
            try:
                p = os.path.join(c, cl[0])
                copy_tree(p, os.path.join(os.path.join(UNPACK_TO, "drum"), cl[0]))
            except IOError:
                print("Unpack Error")

        elif "synth" in os.listdir(tempUnpackPath):
            c = os.path.join(tempUnpackPath, "synth")
            cl = os.listdir(c)
            for i in cl:
                if i.startswith("."):
                    cl.remove(i)
            try:
                p = os.path.join(c, cl[0])
                copy_tree(p, os.path.join(os.path.join(UNPACK_TO, "synth"), cl[0]))
            except IOError:
                print("Unpack Error")

        shutil.rmtree(tempUnpackPath)

print("Done")
