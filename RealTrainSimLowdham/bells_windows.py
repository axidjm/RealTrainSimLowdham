import time
import winsound

# from time import sleep

gap_period = 0.6


def up_bell():
    # winsound.Beep(2200, 50)
    winsound.PlaySound("/sigbox/sounds/ding2.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    time.sleep(gap_period)


def down_bell():
    # winsound.Beep(1600, 50)
    winsound.PlaySound("/sigbox/sounds/ding3.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    time.sleep(gap_period)


def bell_tapper():
    # winsound.Beep(400, 50)
    winsound.PlaySound("/sigbox/sounds/tap.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
    time.sleep(gap_period)
