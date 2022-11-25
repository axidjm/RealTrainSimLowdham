import winsound
from time import sleep
import time

gap_period = 0.3

def bells_init():
    TrainOutOfSection("advance", "UP", "Test")
    pass

def peg(section, line, state):
    # section 'rear': do nothing
    # section 'advance: peg up

    # Line is UP or DOWN

    # state is 'LC', 'TOL' or 'NORMAL'

    if section == "advance":
        print(f"Pegging {state} on {line} (in {section})")
    else:
        print(f"Signalman should peg {state} on {line} (in {section})")


def up_bell():
    # winsound.Beep(2200, 50)
    winsound.PlaySound("ding2.wav", winsound.SND_FILENAME|winsound.SND_ASYNC)
    time.sleep(gap_period)

def down_bell():
    # winsound.Beep(1600, 50)
    winsound.PlaySound("ding3.wav", winsound.SND_FILENAME|winsound.SND_ASYNC)
    time.sleep(gap_period)

def bell_tapper():
    # winsound.Beep(400, 50)
    winsound.PlaySound("tap.wav", winsound.SND_FILENAME|winsound.SND_ASYNC)
    time.sleep(gap_period)



