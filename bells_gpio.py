import RPi.GPIO as GPIO
from time import sleep

# GPIO pins
tap_pin=21 # appr_bell/tap
lh_bj_bell=16
lh_bj_lc=12
lh_bj_tol=25
lh_th_lc=24
lh_th_tol=23
lh_th_bell=18

pulse_period = 0.15
gap_period = 0.25

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
                set_output(lc_pin)
                clr_output(tol_pin)


def up_bell():
    pulse_output(lh_bj_bell)

def down_bell():
    pulse_output(lh_th_bell)

def bell_tapper():
    pulse_output(tap)

def pulse_output(pin):
    set_output(pin)
    time.sleep(pulse_period)
    clr_output(pin)
    time.sleep(gap_period)

def set_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)

def clr_output(pin):
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

