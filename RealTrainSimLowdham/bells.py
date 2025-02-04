import time

if True:
    print("Importing bells_dingtian")
    from bells_dingtian import bells_init, set_output, clr_output, pulse_output
#elif os.name == "posix":
    # RPi
    #print("Importing bells_gpio")
    #from bells_gpio import bells_init, set_output, clr_output, pulse_output
#elif os.name == "nt":
    # windows
    #print("Importing bells_windows")
    #from bells_windows import bells_init, set_output, clr_output, pulse_output

# Relays
tap_relay = 0  # appr_bell/tap
tc4601_out = 1
lh_bj_bell = 2
lh_bj_lc = 3
lh_bj_tol = 4
lh_th_lc = 5
lh_th_tol = 6
lh_th_bell = 7

# Times
pause_period = 0.5
pause2_period = 1.0
long_period = 2.5

pulse_period = 0.15
gap_period = 0.25

def bells_test():
    bells_init()

    print("Testing Bells\n")
    print("BJ Bell")
    pulse_output(lh_bj_bell)
    time.sleep(gap_period)
    print("Thur Bell")
    pulse_output(lh_th_bell)
    time.sleep(1.0)

    print("tap relay")
    set_output(tap_relay)
    time.sleep(2.0)
    clr_output(tap_relay)
    time.sleep(1.0)

    tc4601("CLEAR")
    time.sleep(2.0)
    tc4601("OCCUPIED")
    time.sleep(1.0)
    tc4601("CLEAR")  # Leave TC 'clear'

    print("BJ line clear")
    set_output(lh_bj_lc)
    time.sleep(2.0)
    clr_output(lh_bj_lc)
    time.sleep(1.0)

    print("BJ Train on Line")
    set_output(lh_bj_tol)
    time.sleep(2.0)
    clr_output(lh_bj_tol)
    time.sleep(1.0)

    print("Thur line clear")
    set_output(lh_th_lc)
    time.sleep(2.0)
    clr_output(lh_th_lc)
    time.sleep(1.0)

    print("Thur Train on Line")
    set_output(lh_th_tol)
    time.sleep(2.0)
    clr_output(lh_th_tol)
    time.sleep(1.0)


def IsLineClear(section, line, description):
    trainClass = description[0]
    # trainClass 1: 4
    # trainClass 2: 3-1
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
            print(" ding (2-3)")
            ding(section, line)
            ding(section, line)
            pause()
            ding(section, line)
            ding(section, line)
            ding(section, line)
            pause2()
            print("tap (2-3)")
            tap(section, line)
            tap(section, line)
            pause()
            tap(section, line)
            tap(section, line)
            tap(section, line)

        case "1":
            print(" ding (4)")
            ding(section, line)
            ding(section, line)
            ding(section, line)
            ding(section, line)
            pause2()
            print("tap (4)")
            tap(section, line)
            tap(section, line)
            tap(section, line)
            tap(section, line)

        case "2":
            print(" ding (3-1)")
            ding(section, line)
            ding(section, line)
            ding(section, line)
            pause()
            ding(section, line)
            pause2()
            print("tap (3-1)")
            tap(section, line)
            tap(section, line)
            tap(section, line)
            pause()
            tap(section, line)

        case "3":
            print(" ding (3-4-1)")  # RHTT
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
            print("tap (3-4-1)")
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
            print(" ding (2-2-1)")
            ding(section, line)
            ding(section, line)
            pause()
            ding(section, line)
            ding(section, line)
            pause()
            ding(section, line)
            pause2()
            print("tap (2-2-1)")
            tap(section, line)
            tap(section, line)
            pause()
            tap(section, line)
            tap(section, line)
            pause()
            tap(section, line)

        case "6":
            print(" ding (1-4)")
            ding(section, line)
            pause()
            ding(section, line)
            ding(section, line)
            ding(section, line)
            ding(section, line)
            pause2()
            print("tap (1-4)")
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
        bell_tapper()


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
        bell_tapper()


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
    # section 'rear': do nothing
    # section 'advance: peg up

    # Line is UP or DOWN

    # state is 'LC', 'TOL' or 'NORMAL'

    if section == "advance":
        print(f"Pegging {state} on {line} (in {section})")
        lc_relay = 0
        tol_relay = 0
        match line:
            case "UP":
                lc_relay = lh_bj_lc
                tol_relay = lh_bj_tol
            case "DOWN":
                lc_relay = lh_th_lc
                tol_relay = lh_th_tol

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
    else:
        print(f"Signalman should peg {state} on {line} (in {section})")


def up_bell():
    pulse_output(lh_bj_bell)


def down_bell():
    pulse_output(lh_th_bell)


def bell_tapper():
    pulse_output(tap_relay)


def tc4601(state):
    print(f"Track Circuit {state}")
    match state:
        case "OCCUPIED":
            clr_output(tc4601_out)

        case "CLEAR":
            set_output(tc4601_out)

        case _:
            print("Unknown TC state {state}")
