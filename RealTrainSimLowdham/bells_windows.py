import time
import winsound

# from time import sleep

gap_period = 0.5


def up_bell():
    # winsound.Beep(2200, 50)
    winsound.PlaySound(None, 0)
    winsound.PlaySound("/sigbox/sounds/up-bell.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    time.sleep(gap_period)


def down_bell():
    # winsound.Beep(1600, 50)
    winsound.PlaySound(None, 0)
    winsound.PlaySound("/sigbox/sounds/down-bell.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    time.sleep(gap_period)


def up_tap():
    # winsound.Beep(400, 50)
    winsound.PlaySound(None, 0)
    winsound.PlaySound("/sigbox/sounds/up-tap.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    time.sleep(gap_period)


def down_tap():
    # winsound.Beep(400, 50)
    winsound.PlaySound(None, 0)
    winsound.PlaySound("/sigbox/sounds/down-tap.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    time.sleep(gap_period)
