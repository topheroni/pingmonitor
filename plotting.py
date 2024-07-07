from datetime import datetime as dt

import matplotlib.dates as mdates
import matplotlib.pyplot as plt

THRESHOLD_YELLOW = 50
THRESHOLD_RED = 150


def make_plot(
    timestamps: list[dt],
    values: list[int],
    host: str,
):
    """Generate the line plot of ping records.

    Args:
        timestamps (list[str]): list of timestamps
        values (list[int]): list of corresponding ping values
    """
    x_floats = mdates.date2num(timestamps)
    xmin = x_floats[0]
    xmax = x_floats[-1]
    ax = plt.subplot()
    ax.plot(x_floats, values, marker="o")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M:%S"))
    ax.xaxis.set_major_locator(mdates.SecondLocator(interval=300))
    ax.xaxis.set_minor_locator(mdates.SecondLocator(interval=60))
    graph_bottom = -max(values) * 0.02
    graph_top = max(values) * 1.05
    ax.axhspan(
        ymin=graph_bottom,
        ymax=THRESHOLD_YELLOW,
        color="green",
        alpha=0.25,
    )
    ax.axhspan(
        ymin=THRESHOLD_YELLOW,
        ymax=THRESHOLD_RED,
        color="yellow",
        alpha=0.25,
    )
    ax.axhspan(
        ymin=THRESHOLD_RED,
        ymax=graph_top,
        color="red",
        alpha=0.25,
    )
    ax.set_xlim(xmin, xmax)
    ax.set_ylim(graph_bottom, graph_top)
    plt.title(f"Ping results to {host}")
    plt.xlabel("Timestamp")
    plt.ylabel("Ping (ms)")
    plt.show()
