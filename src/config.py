from pynput.mouse import Button, Controller
import pynput.keyboard
# import screen_brightness_control as sbc


OKTime = None
SwipeTime = 0
ActionList = ["Open Palm", "Fist", "Index Finger", "Double Index Finger", "Spider-Man", "OK", "Telephone"]
keyboard = pynput.keyboard.Controller()
Key = pynput.keyboard.Key
mouse = Controller()
IsBeingClicked = False
Username = "Guest"
SwipeList = []


def VolumeUp():
    keyboard.press(Key.media_volume_up)
    keyboard.release(Key.media_volume_up)


def VolumeDown():
    keyboard.press(Key.media_volume_down)
    keyboard.release(Key.media_volume_down)

def ScrollDown():
    mouse.scroll(0, -.5)

def ScrollUp():
    mouse.scroll(0, .5)
Exit = False