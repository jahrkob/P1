import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, filedialog

def load_multiple_datasets():
    root = Tk()
    root.withdraw()

    file_paths = filedialog.askopenfilenames(
        title="Select one or more CSV files",
        filetypes=[("CSV files", "*.csv")]
    )

    if not file_paths:
        print("No files selected.")
        return []

    datasets = []

    for path in file_paths:
        try:
            df = pd.read_csv(
                path,
                skiprows=[1],                # Skip the second “fake header” row
                names=['x-axis', 'F1'],
                header=0
            )

            df['x-axis'] = pd.to_numeric(df['x-axis'], errors='coerce')
            df['F1'] = pd.to_numeric(df['F1'], errors='coerce')
            df = df.dropna()

            # Convert seconds to microseconds
            df['x-axis'] = df['x-axis'] * 1e6

            # Normalize time axis to start at zero
            df['x-axis'] = df['x-axis'] - df['x-axis'].min()

            datasets.append((df['x-axis'].tolist(), df['F1'].tolist(), path))

        except Exception as e:
            print(f"Error loading {path}: {e}")

    return datasets


def plot_multiple(datasets, title="Power consumption comparison"):
    if not datasets:
        print("No datasets to plot.")
        return

    plt.figure(figsize=(12, 6))

    for seconds, voltage, filename in datasets:
        label = filename.split("/")[-1]  # Use file name as legend label
        plt.plot(seconds, voltage, linewidth=1, label=label)

    plt.title(title)
    plt.xlabel("Microseconds (µs)")
    plt.ylabel("Voltage")
    plt.grid(True, linestyle="--", alpha=0.5)

    plt.locator_params(axis='x', nbins=10)
    plt.locator_params(axis='y', nbins=10)

    plt.legend()
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    datasets = load_multiple_datasets()
    plot_multiple(datasets)
