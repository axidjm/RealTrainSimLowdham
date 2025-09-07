import time

from bells_windows import down_bell, down_tap, up_bell, up_tap
from block_dingtian import clr_output, pulse_output2, set_output

# Relays

# These relays enable the remote signalman to peg up
lh_bj_lc = 3
lh_bj_tol = 4
lh_th_lc = 7
lh_th_tol = 8

# These relays override the local galvo on the pegging instrument
lh_bj_lc2 = 1
lh_bj_tol2 = 2
lh_th_lc2 = 5
lh_th_tol2 = 6

lamp1_out = 9
lamp2_out = 10
lamp3_out = 11
lamp4_out = 12

tc4601_out = 13
approach_bell = 14
platform_bell = 15
normal_standby = 16

# Times
pause_period = 0.4
pause2_period = 1.0
long_period = 2.5

pulse_period = 0.15
gap_period = 0.25


def bells_test():
    print("Testing Bells\n")
    print("BJ Bell")
    up_bell()
    time.sleep(pause_period)
    up_bell()
    time.sleep(pause2_period)
    up_bell()
    time.sleep(long_period)
    print("Thur Bell")
    down_bell()
    time.sleep(pause_period)
    down_bell()
    time.sleep(pause2_period)
    down_bell()
    time.sleep(long_period)

    TrainOutOfSection("advance", "UP", "Test advance")
    TrainOutOfSection("rear", "UP", "Test rear")

    BlockTest("advance", "UP")
    BlockTest("rear", "UP")
    BlockTest("advance", "DOWN")
    BlockTest("rear", "DOWN")

    pulse_output2(lamp1_out, 1.5, 0.5)
    pulse_output2(lamp2_out, 1.5, 0.5)
    pulse_output2(lamp3_out, 1.5, 0.5)
    pulse_output2(lamp4_out, 1.5, 0.5)

    tc4601("OCCUPIED")
    time.sleep(1.0)
    tc4601("CLEAR")  # Leave TC 'clear'

    pulse_output2(approach_bell, 1.5, 0.5)
    pulse_output2(platform_bell, 1.5, 0.5)
    set_output(normal_standby)


def BlockTest(section, line):
    peg(section, line, "LC")
    time.sleep(1.5)
    peg(section, line, "TOL")
    time.sleep(1.5)
    peg(section, line, "NORMAL")
    print("")
    time.sleep(0.5)


def IsLineClear(section, line, description):
    trainClass = description[0]
    # trainClass 0: 2-3
    # trainClass 1: 4
    # trainClass 2: 3-1
    # trainClass 3: 3-4-1
    # trainClass 5: 2-2-1
    # trainClass 6: 1-4

    # section 'rear': Train is belled to us, we tap reply and peg up
    # section 'advance: We tap the code, and the reply is belled

    # Line is UP or DOWN

    print(f"Call Attention on {line} (in {section})")
    ding(section, line)
    long_pause()
    tap(section, line)
    pause2()
    print(f"Is Line Clear for {description} on {line} (in {section})", end="")

    match trainClass:
        case "0":
            print(" ding (2-3)", end="")
            ding(section, line)
            ding(section, line)
            pause()
            ding(section, line)
            ding(section, line)
            ding(section, line)
            pause2()
            print(" tap (2-3)")
            tap(section, line)
            tap(section, line)
            pause()
            tap(section, line)
            tap(section, line)
            tap(section, line)

        case "1":
            print(" ding (4)", end="")
            ding(section, line)
            ding(section, line)
            ding(section, line)
            ding(section, line)
            pause2()
            print(" tap (4)")
            tap(section, line)
            tap(section, line)
            tap(section, line)
            tap(section, line)

        case "2":
            print(" ding (3-1)", end="")
            ding(section, line)
            ding(section, line)
            ding(section, line)
            pause()
            ding(section, line)
            pause2()
            print(" tap (3-1)")
            tap(section, line)
            tap(section, line)
            tap(section, line)
            pause()
            tap(section, line)

        case "3":
            print(" ding (3-4-1)", end="")  # RHTT
            ding(section, line)
            ding(section, line)
            ding(section, line)
            pause()
            ding(section, line)
            ding(section, line)
            ding(section, line)
            ding(section, line)
            pause()
            ding(section, line)
            pause2()
            print(" tap (3-4-1)")
            tap(section, line)
            tap(section, line)
            tap(section, line)
            pause()
            tap(section, line)
            tap(section, line)
            tap(section, line)
            tap(section, line)
            pause()
            tap(section, line)

        case "5":
            print(" ding (2-2-1)", end="")
            ding(section, line)
            ding(section, line)
            pause()
            ding(section, line)
            ding(section, line)
            pause()
            ding(section, line)
            pause2()
            print(" tap (2-2-1)")
            tap(section, line)
            tap(section, line)
            pause()
            tap(section, line)
            tap(section, line)
            pause()
            tap(section, line)

        case "6":
            print(" ding (1-4)", end="")
            ding(section, line)
            pause()
            ding(section, line)
            ding(section, line)
            ding(section, line)
            ding(section, line)
            pause2()
            print(" tap (1-4)")
            tap(section, line)
            pause()
            tap(section, line)
            tap(section, line)
            tap(section, line)
            tap(section, line)

        case _:
            print(f" (unknown class {trainClass})")

    pause2()
    peg(section, line, "LC")


def TrainEnteringSection(section, line, description):
    # section 'rear': Train is belled to us, we tap reply and peg up
    # section 'advance: We tap the code, and the reply is belled

    # Line is UP or DOWN

    print(f"Train {description} Entering Section (2) on {line} (in {section})")
    ding(section, line)
    time.sleep(0.2)  # Don't know why the pause in the 'ding()' isn't enough...
    ding(section, line)
    long_pause()
    tap(section, line)
    time.sleep(0.2)  # Don't know why the pause in the 'ding()' isn't enough...
    tap(section, line)
    pause2()
    peg(section, line, "TOL")


def TrainOutOfSection(section, line, description):
    # section 'rear': Train is belled to us, we tap reply and peg up
    # section 'advance: We tap the code, and the reply is belled

    # Line is UP or DOWN

    print(f"Call Attention on {line} (in {section})")
    tap(section, line)
    long_pause()
    ding(section, line)
    pause2()

    print(f"Train {description} Out Of Section (2-1) on {line} (in {section})")
    tap(section, line)
    tap(section, line)
    pause()
    tap(section, line)
    pause2()
    ding(section, line)
    ding(section, line)
    pause()
    ding(section, line)
    pause2()
    peg(section, line, "NORMAL")


def ding(section, line):
    # section 'rear': Ring the bell
    # section 'advance: Tap the tapper

    # Line is UP or DOWN
    if section == "rear":
        if line == "UP":
            down_bell()
        else:
            up_bell()
    else:
        if line == "UP":
            up_tap()
        else:
            down_tap()


def tap(section, line):
    # section 'rear': Tap the tapper
    # section 'advance: Ring the bell

    # Line is UP or DOWN
    if section == "advance":
        if line == "UP":
            up_bell()
        else:
            down_bell()
    else:
        if line == "UP":
            up_tap()
        else:
            down_tap()


def pause():
    # short pause between taps, 300ms
    time.sleep(pause_period)


def pause2():
    # Longer pause, say 1 second
    time.sleep(pause2_period)


def long_pause():
    # Time for signalman to get to the bell, say 3 seconds
    time.sleep(long_period)


def peg(section, line, state):
    # section 'rear': override the galvo on the pegging instrument
    # section 'advance: The remote signalman pegs up
    # Line is UP or DOWN
    # state is 'LC', 'TOL' or 'NORMAL'

    lc_relay = 0
    tol_relay = 0

    print(f"Pegging {state} on {line} (in {section})")

    if section == "advance":
        match line:
            case "UP":
                lc_relay = lh_bj_lc
                tol_relay = lh_bj_tol
            case "DOWN":
                lc_relay = lh_th_lc
                tol_relay = lh_th_tol

    else:
        print(f"Signalman should peg {state} on {line} (in {section})")
        match line:
            case "UP":
                lc_relay = lh_bj_lc2
                tol_relay = lh_bj_tol2
            case "DOWN":
                lc_relay = lh_th_lc2
                tol_relay = lh_th_tol2

    match state:
        case "LC":
            set_output(lc_relay)
            clr_output(tol_relay)
        case "TOL":
            clr_output(lc_relay)
            set_output(tol_relay)
        case "NORMAL":
            clr_output(lc_relay)
            clr_output(tol_relay)


def tc4601(state):
    print(f"Track Circuit {state}")
    match state:
        case "OCCUPIED":
            set_output(tc4601_out)

        case "CLEAR":
            clr_output(tc4601_out)

        case _:
            print("Unknown TC state {state}")
