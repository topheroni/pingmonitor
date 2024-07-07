import argparse
import logging
import platform
import re
import subprocess
from datetime import datetime as dt
from time import sleep

from plotting import make_plot

expr = re.compile(r"time=[0-9]{1,}ms")
file = "data.json"


def main(
    host: str,
    interval: int,
    amount: int,
):
    ping_values = []
    ping_timestamps = []
    count = amount
    ping_time = 0
    if platform.system().lower() == "windows":
        flag = "/n"
    else:
        flag = "-c"
    amount_str = f"{amount} times" if amount != 0 else ""
    logging.info(f"pinging host {host} every {interval} seconds {amount_str}")
    while amount is None or count < amount:
        try:
            timestamp = dt.now()
            output = subprocess.check_output(
                ["ping", flag, "1", host], stderr=subprocess.STDOUT
            ).decode()
            ping_time_match = expr.search(output)
            if ping_time_match:
                ping_time = int(ping_time_match[0].split("=")[1].replace("ms", ""))
                ping_timestamps.append(timestamp)
                ping_values.append(ping_time)
        except (subprocess.CalledProcessError, TypeError):
            logging.error("Host potentially unreachable.")
        count += 1
        if count == amount:
            break
        if ping_time < interval:
            sleep(interval - (ping_time / 1000))
        else:
            sleep(interval)
    make_plot(ping_timestamps, ping_values, host)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="optional arguments for the ping command"
    )
    parser.add_argument(
        "--host", help="the host to ping. google.com by default", default="google.com"
    )
    parser.add_argument(
        "--interval",
        metavar="int",
        type=int,
        help="the time in seconds between pings. must be a positive integer. 1 second by default",
        default=1,
    )
    parser.add_argument(
        "--amount",
        type=int,
        help="the number of times to ping before completing execution. must be a positive integer. runs indefinitely by default",
        default=0,
    )
    args = parser.parse_args()
    if args.interval <= 0:
        raise ValueError
    main(args.host, args.interval, args.amount)
