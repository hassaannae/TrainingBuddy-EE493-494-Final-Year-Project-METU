import os
import shutil
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("--path", type=str)
ap.add_argument("--filetype", type=str, help="folder or file")
args = vars(ap.parse_args())

if args["filetype"] == "folder":
    shutil.rmtree(os.getcwd()+"/{}".format(args["path"]))

elif args["filetype"] == "file":
    os.remove(os.getcwd()+"/{}".format(args["path"]))