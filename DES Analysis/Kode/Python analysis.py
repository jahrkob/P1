import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

def load_list():
    root = Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select the CSV file",
        filetypes=[("CSV files", "*.csv")]
    )

    if not file_path:
        print("No file selected.")
        return [], []

    # Load CSV correctly
    df = pd.read_csv(
        file_path,
        skiprows=[1],                # Skip the second “fake header” row
        names=['x-axis', 'F1'],
        header=0
    )

    df['x-axis'] = pd.to_numeric(df['x-axis'], errors='coerce')
    df['F1'] = pd.to_numeric(df['F1'], errors='coerce')
    df = df.dropna()

    # Convert seconds to microseconds for easier visual scaling
    df['x-axis'] = df['x-axis'] * 1e6

    # Start at zero
    df['x-axis'] = df['x-axis'] - df['x-axis'].min()


    return df['x-axis'].tolist(), df['F1'].tolist()


def plot_voltage(seconds, voltage, title="Power consumption over Time"):
    if not seconds or not voltage:
        print("Nothing to plot: empty data.")
        return

    plt.figure(figsize=(12, 6))
    plt.plot(seconds, voltage, color="steelblue", linewidth=1)

    plt.title(title)
    plt.xlabel("Microseconds (µs)")
    plt.ylabel("Voltage")
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.locator_params(axis='x', nbins=10)
    plt.locator_params(axis='y', nbins=10)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    seconds, voltage = load_list()
    plot_voltage(seconds, voltage)
