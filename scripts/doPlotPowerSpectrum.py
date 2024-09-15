import sys
import argparse
import pickle
import numpy as np
import pandas as pd
import plotly.graph_objects as go

import aeon_behavior_spectral.signal_processing.spectral_analysis


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--fraction_start",
                        help="fraction of time series where to start",
                        type=float, default=0.0)
    parser.add_argument("--fraction_end",
                        help="fraction of time series where to end",
                        type=float, default=1.0)
    parser.add_argument("--Sxx_filename_pattern",
                        help="Sxx filename pattern", type=str,
                        default="../results/Sxx_from{:.02f}_to{:.02f}.pickle")
    parser.add_argument("--fig_filename_pattern",
                        help="fig filename pattern", type=str,
                        default="../figures/Sxx_from{:.02f}_to{:.02f}.{:s}")
    args = parser.parse_args()

    fraction_start = args.fraction_start
    fraction_end = args.fraction_end
    Sxx_filename_pattern = args.Sxx_filename_pattern
    fig_filename_pattern = args.fig_filename_pattern

    Sxx_filename = Sxx_filename_pattern.format(fraction_start, fraction_end)
    with open(Sxx_filename, "rb") as f:
        results = pickle.load(f)
    Sxx = results["Sxx"]
    freqs = results["freqs"]

    fig = go.Figure()
    trace = go.Scatter(x=freqs, y=10 * np.log10(Sxx/np.max(Sxx)))
    fig.add_trace(trace)
    fig.update_xaxes(title="Frequency (Hz)", type="log"),
    fig.update_yaxes(title="Power (dB)")
    fig.write_image(fig_filename_pattern.format(fraction_start, fraction_end,
                                                "png"))
    fig.write_html(fig_filename_pattern.format(fraction_start, fraction_end,
                                               "html"))
    fig.show()

    breakpoint()


if __name__ == "__main__":
    main(sys.argv)
