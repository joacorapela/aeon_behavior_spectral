import sys
import argparse
import pickle
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
    parser.add_argument("--time_series_filename", help="time series filename",
                        type=str,
                        default="../data/simulated.parquet.gzip")
    parser.add_argument("--results_filename_pattern",
                        help="results filename pattern", type=str,
                        default="../results/Sxx_from{:.02f}_to{:.02f}.pickle")
    args = parser.parse_args()

    fraction_start = args.fraction_start
    fraction_end = args.fraction_end
    time_series_filename = args.time_series_filename
    results_filename_pattern = args.results_filename_pattern

    df = pd.read_parquet(time_series_filename)
    pos_start = int(fraction_start * df.shape[0])
    pos_end = int(fraction_end * df.shape[0])
    dates = df["dates"][pos_start:pos_end, ]
    x = df["x"][pos_start:pos_end, ]
    dt = (dates.iloc[1] - dates.iloc[0]).total_seconds()
    T = (dates.iloc[-1] - dates.iloc[0]).total_seconds()

    Sxx, freqs = aeon_behavior_spectral.signal_processing.spectral_analysis.estimate_power_spectrum(
        x=x, fs=1/dt, T=T)

    result = {"Sxx": Sxx, "freqs": freqs}
    results_filename = results_filename_pattern.format(fraction_start,
                                                       fraction_end)
    with open(results_filename, "wb") as f:
        pickle.dump(result, f)
    print(f"Results save to {results_filename}")

    fig = go.Figure()
    trace = go.Scatter(x=freqs, y=Sxx)
    fig.add_trace(trace)
    fig.update_xaxes(title="Frequency (Hz)"),
    fig.update_yaxes(title=r"$Sxx \mu V^2$/Hz$")
    fig.write_image(fig_filename_pattern.format(fraction_start, fraction_end,
                                                "png"))
    fig.write_html(fig_filename_pattern.format(fraction_start, fraction_end,
                                               "html"))

    fig.show()

    breakpoint()


if __name__ == "__main__":
    main(sys.argv)
