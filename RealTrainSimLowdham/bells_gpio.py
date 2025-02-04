import time

import RPi.GPIO as GPIO

# from time import sleep


# GPIO pins
tap_pin = 21  # appr_bell/tap
tc4601_out = 20
lh_bj_bell = 16
lh_bj_lc = 12
lh_bj_tol = 25
lh_th_lc = 24
lh_th_tol = 23
lh_th_bell = 18

pulse_period = 0.15
gap_period = 0.25


def bells_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)


def pulse_output(pin):
    set_output(pin)
    time.sleep(pulse_period)
    clr_output(pin)
    time.sleep(gap_period)


def set_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)


def clr_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)


def tc4601(state):
    print(f"Track Circuit {state}")
    match state:
        case "OCCUPIED":
            clr_output(tc4601_out)

        case "CLEAR":
            set_output(tc4601_out)

        case _:
            print("Unknown TC state {state}")
