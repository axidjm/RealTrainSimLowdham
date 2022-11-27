import RPi.GPIO as GPIO
from time import sleep
import time

# GPIO pins
tap_pin=21 # appr_bell/tap
tc4601_out=20
lh_bj_bell=16
lh_bj_lc=12
lh_bj_tol=25
lh_th_lc=24
lh_th_tol=23
lh_th_bell=18

pulse_period = 0.15
gap_period = 0.25

def bells_init():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    pulse_output(lh_bj_bell)
    time.sleep(gap_period)
    pulse_output(lh_th_bell)
    time.sleep(1.0)

    set_output(tap_pin)
    time.sleep(2.0)
    clr_output(tap_pin)
    time.sleep(1.0)

    tc4601("CLEAR")
    time.sleep(2.0)
    tc4601("OCCUPIED")
    time.sleep(1.0)
    tc4601("CLEAR")      # Leave TC 'clear'

    set_output(lh_bj_lc)
    time.sleep(2.0)
    clr_output(lh_bj_lc)
    time.sleep(1.0)

    set_output(lh_bj_tol)
    time.sleep(2.0)
    clr_output(lh_bj_tol)
    time.sleep(1.0)

    set_output(lh_th_lc)
    time.sleep(2.0)
    clr_output(lh_th_lc)
    time.sleep(1.0)

    set_output(lh_th_tol)
    time.sleep(2.0)
    clr_output(lh_th_tol)
    time.sleep(1.0)

def peg(section, line, state):
    # section 'rear': do nothing
    # section 'advance: peg up

    # Line is UP or DOWN

    # state is 'LC', 'TOL' or 'NORMAL'

    if section == "advance":
        print(f"Pegging {state} on {line} (in {section})")
        match line:
            case "UP":
                lc_pin = lh_bj_lc
                tol_pin = lh_bj_tol
            case "DOWN":
                lc_pin = lh_th_lc
                tol_pin = lh_th_tol

        match state:
            case "LC":
                set_output(lc_pin)
                clr_output(tol_pin)
            case "TOL":
                clr_output(lc_pin)
                set_output(tol_pin)
            case "NORMAL":
                clr_output(lc_pin)
                clr_output(tol_pin)
    else:
        print(f"Signalman should peg {state} on {line} (in {section})")

def up_bell():
    pulse_output(lh_bj_bell)

def down_bell():
    pulse_output(lh_th_bell)

def bell_tapper():
    pulse_output(tap_pin)

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

