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
pause_period = 0.6
pause2_period = 1.2
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
    up_tap()
    time.sleep(long_period)

    print("Thur Bell")
    down_bell()
    time.sleep(pause_period)
    down_bell()
    time.sleep(pause2_period)
    down_bell()
    time.sleep(long_period)
    down_tap()
    time.sleep(long_period)


def all_block_tests():
    block_test("advance", "UP")
    block_test("rear", "UP")
    block_test("advance", "DOWN")
    block_test("rear", "DOWN")

    print("-------------------------")
    print("Lamp 1 test")
    pulse_output2(lamp1_out, 1.5, 1.5)
    print("Lamp 2 test")
    pulse_output2(lamp2_out, 1.5, 1.5)
    print("Lamp 3 test")
    pulse_output2(lamp3_out, 1.5, 1.5)
    print("Lamp 4 test")
    pulse_output2(lamp4_out, 1.5, 1.5)

    tc4601("OCCUPIED")
    time.sleep(1.0)
    tc4601("CLEAR")  # Leave TC 'clear'

    print("approach bell")
    pulse_output2(approach_bell, 1.0, 0.5)
    print("platform bell")
    pulse_output2(platform_bell, 1.0, 0.5)
    print("normal")
    pulse_output2(normal_standby, 1.0, 0.5)
    print("End of test")


def block_test(section, line):
    print("-------------------------")
    print(f"Block test {section} {line}")
    peg(section, line, "LC")
    time.sleep(2.5)
    peg(section, line, "TOL")
    time.sleep(2.5)
    peg(section, line, "NORMAL")
    print("")
    time.sleep(3.5)


def trains_test():
    train_test("rear", "UP", "0A11")
    train_test("advance", "UP", "0A11")
    train_test("rear", "DOWN", "2B22")
    train_test("advance", "DOWN", "2B22")


def train_test(section, line, description):
    print("-------------------------")
    print(f"Train test: {section} {line} {description}")
    IsLineClear(section, line, description)
    time.sleep(5.0)
    TrainEnteringSection(section, line, description)
    time.sleep(5.0)
    TrainOutOfSection(section, line, description)
    time.sleep(5.0)


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
            ding2(section, line)
            pause()
            ding3(section, line)
            pause2()
            print(" tap (2-3)")
            tap2(section, line)
            pause()
            tap3(section, line)

        case "1":
            print(" ding (4)", end="")
            ding4(section, line)
            pause2()
            print(" tap (4)")
            tap4(section, line)

        case "2":
            print(" ding (3-1)", end="")
            ding3(section, line)
            pause()
            ding(section, line)
            pause2()
            print(" tap (3-1)")
            tap3(section, line)
            pause()
            tap(section, line)

        case "3":
            print(" ding (3-4-1)", end="")  # RHTT
            ding3(section, line)
            pause()
            ding4(section, line)
            pause()
            ding(section, line)
            pause2()
            print(" tap (3-4-1)")
            tap3(section, line)
            pause()
            tap4(section, line)
            pause()
            tap(section, line)

        case "5":
            print(" ding (2-2-1)", end="")
            ding2(section, line)
            pause()
            ding2(section, line)
            pause()
            ding(section, line)
            pause2()
            print(" tap (2-2-1)")
            tap2(section, line)
            pause()
            tap2(section, line)
            pause()
            tap(section, line)

        case "6":
            print(" ding (1-4)", end="")
            ding(section, line)
            pause()
            ding4(section, line)
            pause2()
            print(" tap (1-4)")
            tap(section, line)
            pause()
            tap4(section, line)

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
    time.sleep(0.3)  # Don't know why the pause in the 'ding()' isn't enough...
    ding(section, line)
    long_pause()
    tap(section, line)
    time.sleep(0.3)  # Don't know why the pause in the 'ding()' isn't enough...
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
    tap2(section, line)
    pause()
    tap(section, line)
    pause2()
    ding2(section, line)
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


def ding2(section, line):
    ding(section, line)
    ding(section, line)


def ding3(section, line):
    ding2(section, line)
    ding(section, line)


def ding4(section, line):
    ding2(section, line)
    ding2(section, line)


def tap2(section, line):
    tap(section, line)
    tap(section, line)


def tap3(section, line):
    tap2(section, line)
    tap(section, line)


def tap4(section, line):
    tap2(section, line)
    tap2(section, line)


def pause():
    # short pause between taps, 300ms
    time.sleep(pause_period)


def pause2():
    # Longer pause, say 1 second
    time.sleep(pause2_period)


def long_pause():
    # Time for signalman to get to the bell, say 3 seconds
    time.sleep(long_period)


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
            down_tap()
        else:
            up_tap()


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
            case "DOWN":
                lc_relay = lh_bj_lc2
                tol_relay = lh_bj_tol2
            case "UP":
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
