import sys
import argparse
import pandas as pd
import plotly.graph_objects as go


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--fraction_start",
                        help="fraction of time series where to start",
                        type=float, default=0.0)
    parser.add_argument("--fraction_end",
                        help="fraction of time series where to end",
                        type=float, default=0.5)
    parser.add_argument("--time_series_filename", help="time series filename",
                        type=str,
                        default="../../data/simulated.parquet.gzip")
    parser.add_argument("--fig_filename_pattern",
                        help="figure filename pattern", type=str,
                        default="../../figures/simulated_from{:.02f}_to{:.02f}.{:s}")
    args = parser.parse_args()

    fraction_start = args.fraction_start
    fraction_end = args.fraction_end
    time_series_filename = args.time_series_filename
    fig_filename_pattern = args.fig_filename_pattern

    df = pd.read_parquet(time_series_filename)
    pos_start = int(fraction_start * df.shape[0])
    pos_end = int(fraction_end * df.shape[0])
    fig = go.Figure()
    trace = go.Scatter(x=df["dates"][pos_start:pos_end, ],
                       y=df["x"][pos_start:pos_end, ])
    fig.add_trace(trace)
    fig.update_xaxes(rangeslider_visible=True)

    fig.write_image(fig_filename_pattern.format(fraction_start, fraction_end,
                                                "png"))
    fig.write_html(fig_filename_pattern.format(fraction_start, fraction_end,
                                               "html"))

    fig.show()

    breakpoint()


if __name__ == "__main__":
    main(sys.argv)
