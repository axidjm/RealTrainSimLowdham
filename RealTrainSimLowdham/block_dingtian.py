# from time import sleep

import time

import httpx

debug = 0
relay_board_ip = "192.168.2.102"


def pulse_output(relay):
    send(f"type=1&relay={relay}&on=1&time=1")


def pulse_output2(relay, pulse_period, gap_period):
    set_output(relay)
    time.sleep(pulse_period)
    clr_output(relay)
    time.sleep(gap_period)


def set_output(relay):
    send(f"type=0&relay={relay}&on=1&time=0")


def clr_output(relay):
    send(f"type=0&relay={relay}&on=0&time=0")


def send(args):
    url = f"http://{relay_board_ip}/relay_cgi.cgi?{args}&pwd=0"
    if debug:
        print(f"Sending {url}")
        return

    try:
        # http_client = httpx.AsyncClient()
        _CLIENT = httpx.Client(timeout=httpx.Timeout(5, pool=5))
        response = _CLIENT.get(
            url=url,
            headers={"Content-Type": "application/json", "Accept": "text/plain"},
        )
    except httpx.ConnectTimeout:
        print(f"Connection timed out to {url}")
        return

    if response.status_code == httpx.codes.OK:
        # print(f"Success: got 200 from {response.request}")
        pass
    else:
        print(f"Failed: got {response.status_code} from {response.request}")
