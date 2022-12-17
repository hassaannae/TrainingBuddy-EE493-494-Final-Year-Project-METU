import os
import shutil
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--path", type=str)
ap.add_argument("--filetype", type=str, help="folder or file")
args = vars(ap.parse_args())


path = args["path"]
if args["filetype"] == "folder" and path in os.listdir():
    shutil.rmtree(os.getcwd()+"/{}".format(args["path"]))


elif args["filetype"] == "file" and path in os.listdir():
    os.remove(os.getcwd()+"/{}".format(args["path"]))