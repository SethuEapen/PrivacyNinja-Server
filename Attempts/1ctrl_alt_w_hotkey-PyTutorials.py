#PyTutorials: https://www.youtube.com/watch?v=n_dfv5DLCGI
from pynput import keyboard
import os

COMBINATIONS = [
            {keyboard.Key.ctrl_l, keyboard.Key.alt_l,keyboard.KeyCode(char='w')},
            {keyboard.Key.ctrl_l, keyboard.Key.alt_l,keyboard.KeyCode(char='W')}
        ]

# The currently active modifiers
current = set()
            
def execute():
    #https://www.youtube.com/watch?v=IJm9m8kv7gU
    try:
        os.system("TASKKILL /F /IM firefox.exe")
    except Exception:
        print(Exception)
def on_press(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.add(key)
        if any(all(k in current for k in COMBO) for COMBO in COMBINATIONS):
            execute()

def on_release(key):
    if any([key in COMBO for COMBO in COMBINATIONS]):
        current.remove(key)

with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
            listener.join()
