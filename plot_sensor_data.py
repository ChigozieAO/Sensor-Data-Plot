"""
plot_sensor_data.py
-------------------
Reads sensor data from 'sensor_data.csv' and plots voltage, current,
and temperature as time-series subplots.
"""

import argparse
import csv
import sys
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# ── Colour palette ──────────────────────────────────────────────────────────
COLORS = {
    "voltage": "#2196F3",  # blue
    "current": "#FF5722",  # deep orange
    "temperature": "#4CAF50",  # green
    "background": "#0F1923",  # dark navy
    "grid": "#1E2D3D",
    "text": "#E0E6ED",
    "axes_bg": "#131F2B",
}


def load_csv(filepath: str):
    """
    Load sensor data from a CSV file.

    Returns:
        timestamps  : list of datetime objects
        voltage     : list of floats
        current     : list of floats
        temperature : list of floats
    """
    timestamps, voltage, current, temperature = [], [], [], []

    try:
        with open(filepath, newline="") as f:
            reader = csv.DictReader(f)
            required = {"timestamp", "voltage", "current", "temperature"}

            if not required.issubset(set(reader.fieldnames or [])):
                missing = required - set(reader.fieldnames or [])
                print(f"[✗] CSV is missing columns: {missing}")
                sys.exit(1)

            for row in reader:
                timestamps.append(
                    datetime.strptime(row["timestamp"], "%Y-%m-%d %H:%M:%S")
                )
                voltage.append(float(row["voltage"]))
                current.append(float(row["current"]))
                temperature.append(float(row["temperature"]))

    except FileNotFoundError:
        print(f"[✗] File not found: '{filepath}'")
        print("    Run 'python generate_data.py' first to create sample data.")
        sys.exit(1)

    print(f"[✓] Loaded {len(timestamps)} records from '{filepath}'")
    return timestamps, voltage, current, temperature


def plot(
    timestamps,
    voltage,
    current,
    temperature,
    save: bool = False,
    output: str = "sensor_plot.png",
):
    """Render a 3-panel time-series plot for the three sensor channels."""

    # ── Figure setup ────────────────────────────────────────────────────────
    fig, axes = plt.subplots(3, 1, figsize=(14, 9), sharex=True)
    fig.patch.set_facecolor(COLORS["background"])
    fig.suptitle(
        "Sensor Data Dashboard",
        fontsize=18,
        fontweight="bold",
        color=COLORS["text"],
        y=0.98,
    )

    channels = [
        ("Voltage (V)", voltage, COLORS["voltage"], "V"),
        ("Current (A)", current, COLORS["current"], "A"),
        ("Temperature (°C)", temperature, COLORS["temperature"], "°C"),
    ]

    for ax, (label, data, color, unit) in zip(axes, channels):
        # Background & spines
        ax.set_facecolor(COLORS["axes_bg"])
        for spine in ax.spines.values():
            spine.set_edgecolor(COLORS["grid"])

        # Plot line + shaded area under curve
        ax.plot(timestamps, data, color=color, linewidth=1.6, alpha=0.95, label=label)
        ax.fill_between(timestamps, data, alpha=0.12, color=color)

        # Labels & ticks
        ax.set_ylabel(label, color=COLORS["text"], fontsize=11)
        ax.tick_params(colors=COLORS["text"], labelsize=9)
        ax.yaxis.label.set_color(COLORS["text"])

        # Grid
        ax.grid(True, color=COLORS["grid"], linewidth=0.7, linestyle="--", alpha=0.6)
        ax.set_axisbelow(True)

        # Stats annotation (min / max / avg)
        mn, mx, avg = min(data), max(data), sum(data) / len(data)
        ax.annotate(
            f"min {mn:.2f}{unit}  |  avg {avg:.2f}{unit}  |  max {mx:.2f}{unit}",
            xy=(0.01, 0.88),
            xycoords="axes fraction",
            fontsize=8.5,
            color=COLORS["text"],
            alpha=0.75,
        )

    # ── X-axis: format timestamps ────────────────────────────────────────────
    axes[-1].xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
    axes[-1].xaxis.set_major_locator(mdates.AutoDateLocator())
    axes[-1].set_xlabel("Time", color=COLORS["text"], fontsize=11)
    axes[-1].tick_params(axis="x", colors=COLORS["text"], labelsize=9)

    fig.autofmt_xdate(rotation=30, ha="right")
    plt.tight_layout(rect=[0, 0, 1, 0.96])

    # ── Output ───────────────────────────────────────────────────────────────
    if save:
        fig.savefig(output, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
        print(f"[✓] Plot saved to '{output}'")
    else:
        plt.show()


def parse_args():
    parser = argparse.ArgumentParser(description="Plot sensor data from a CSV file.")
    parser.add_argument(
        "--file",
        default="sensor_data.csv",
        help="Path to the CSV file (default: sensor_data.csv)",
    )
    parser.add_argument(
        "--save",
        action="store_true",
        help="Save the plot as a PNG instead of displaying it",
    )
    parser.add_argument(
        "--output",
        default="sensor_plot.png",
        help="Output filename when --save is used (default: sensor_plot.png)",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    ts, v, c, t = load_csv(args.file)
    plot(ts, v, c, t, save=args.save, output=args.output)
