#import glob, os
#os.chdir("python")
import os
n = 0
for root, dirs, files in os.walk("."):
    for file in files:
        path = os.path.join(root, file)
        if path.endswith((".py", ".html", ".js", ".css")) and (".bak" not in path):
             print(path)
             for t in open(path,"rb").readlines():
                 if t.strip()!=b"":n+=1


print("\n\nTOTAL LINES:", n)
