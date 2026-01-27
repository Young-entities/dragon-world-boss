import glob
import os
import datetime

def list_files():
    files = glob.glob("../*.png") + glob.glob("../*.jpg")
    files.sort(key=os.path.getmtime, reverse=True)
    
    with open("file_list.txt", "w") as f:
        f.write("Recent Files:\n")
        for file in files[:15]:
            ts = os.path.getmtime(file)
            dt = datetime.datetime.fromtimestamp(ts)
            name = os.path.basename(file)
            f.write(f"{dt} | {name}\n")

list_files()
