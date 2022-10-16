import requests
import os

url = "https://lim95.pythonanywhere.com/nextshell/"

try:
    os.mkdir("audio")
except FileExistsError:
    pass

files_to_download = ["update", "config", "error_wav"]
filenames = ["nextshell.py", "config.yml", "audio/error.wav"]

for i in range(len(files_to_download)):
    file = url + files_to_download[i]

    with open(filenames[i], "wb") as file_:
        file_.write(requests.get(file).content)
    

print("Updated successfully. Run nextshell.py to start.")