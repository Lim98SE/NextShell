import yaml as yml
try:
    import simpleaudio
except ImportError:
    print("Simpleaudio could not be installed. Please note that some parts of the software may not work or not work properly.")
import sys
import os
import time
import requests

audio_files = []
version = 0.5

website = "website"

def send_error(error, isCritical : bool, soundID = 0):
    print(f"ERROR: {error}. Go to {website} to get help.")

    if isCritical:
        print("NextShell cannot continue and will be terminated.")
        sys.exit(0)

try:
    os.chdir("audio")

    for i in os.listdir():
        audio_files.append(f"{os.getcwd()}/{i}")

    os.chdir("..")

except Exception as e:
    send_error(f"An error occured while finding audio files: {e}", True)

try:
    with open("config.yml") as config_yml:
        loader = yml.Loader
        config = yml.load(config_yml, loader)
except FileNotFoundError as e:
    send_error(e, True, 0)
    sys.exit(0)

time.sleep(0.5)

# the duplicated function is intentional

if config["sound"]:
    def playsound(soundID):
        play = simpleaudio.WaveObject.from_wave_file(audio_files[soundID]).play()

        play.wait_done()

    def send_error(error, isCritical : bool, soundID = 0):
        print(f"ERROR: {error}. Go to {website} to get help.")

        playsound(soundID)

        if isCritical:
            print("NextShell cannot continue and will be terminated.")
            sys.exit(0)

if config["color"]:
    from colorit import *
    init_colorit()

pallate = config["pallate"]

def cprint(text, clr):
    if config["color"]:
        text = color(text, pallate[clr])

    print(text)

def bprint(text, clr):
    if config["color"]:
        text = background(text, pallate[clr])

    print(text)

cprint(f"Loading NextShell {version}...", 4)

running = True

def run(command):
    global playing_audio
    args = command.split()
    command = command.lower().split()

    if len(command) < 1:
        return True

    if command[0] == "dir":
        if len(command) >= 2:
            query = command[1]
        else:
            query = ""

        for x in os.listdir():
            if query in x:
                cprint(x, 2 if os.path.isfile(x) else 4 if os.path.isdir(x) else 5)

    if command[0] == "cd":
        if len(command) < 2:
            send_error("Please provide a directory.", False, 0)
            return True

        try:
            os.chdir(" ".join(args[1:]))
        except Exception as e:
            send_error(f"An error occured while preforming this command: {e}", False, 0)
            return True

    if command[0] == "exit":
        return False

    if command[0] == "play":
        if len(command) < 2:
            send_error("Please provide a valid .wav file.", False, 0)
            return True

        try:
            with open(" ".join(args[1:]), "rb") as file:
                playing_audio = simpleaudio.WaveObject.from_wave_file(file).play()
        except Exception as e:
            send_error(f"An error occured while preforming this command: {e}", False, 0)
            return True

    if command[0] == "stop":
        try:
            playing_audio.stop()
        except Exception as e:
            send_error(f"An error occured while preforming this command: {e}", False, 0)
            return True

    if command[0] == "read":
        if len(command) < 2:
            send_error("Please provide a file.", False, 0)
            return True

        try:
            try:
                with open(" ".join(args[1:])) as file:
                    print(file.read())
            except UnicodeError:
                with open(" ".join(args[1:]), "rb") as file:
                    print(file.read())
        except Exception as e:
            send_error(f"An error occured while preforming this command: {e}", False, 0)
            return True

    if command[0] == "echo":
        print(" ".join(args[1:]))

    if command[0] == "typewrite":
        if len(command) < 3:
            send_error("Please provide text and time between characters.", False, 0)
            return True

        text = " ".join(args[2:])
        speed = float(args[1])

        for i in text:
            sys.stdout.write(i)
            sys.stdout.flush()
            time.sleep(speed)

        print("")

    if command[0] == "batch":
        if len(command) < 2:
            send_error("Please provide a file.", False, 0)
            return True

        try:
            with open(" ".join(args[1:])) as batch_file:
                commands = batch_file.read().split("\n")
                for i in commands:
                    if i == "\n":
                        return True
                    run(i.strip())
        except Exception as e:
            send_error(f"An error occured while preforming this command: {e}", False, 0)
            return True

    if command[0] == "run":
        if len(command) < 2:
            send_error("Please provide a Python file.", False, 0)
            return True

        try:
            with open(" ".join(args[1:])) as code:
                exec(code.read())
        except Exception as e:
            send_error(f"An error occured while preforming this command: {e}", False, 0)
            return True

    if command[0] == "delay":
        if len(command) < 2:
            send_error("Please provide a float (for seconds).", False, 0)
            return True

        try:
            time.sleep(float(args[1]))
        except Exception as e:
            send_error(f"An error occured while preforming this command: {e}", False, 0)
            return True

    if command[0] == "waitforsound":
        try:
            playing_audio.wait_done()
        except Exception as e:
            send_error(f"An error occured while preforming this command: {e}", False, 0)
            return True

    if command[0] == "download":
        if len(command) < 2:
            send_error("Please provide a URL.", False, 0)

        arg = " ".join(args[1:])

        paths = (arg.strip().split(","))

        for i in range(len(paths)):
            paths[i] = paths[i].strip()

        if len(paths) == 1:
            with open("download.txt", "wb") as download:
                download.write(requests.get(paths[0]).content)

        else:
            with open(paths[1], "wb") as download:
                download.write(requests.get(paths[0]).content)

    return True

while running:
    running = run(input(color(">", pallate[5]) if config["color"] else ">"))