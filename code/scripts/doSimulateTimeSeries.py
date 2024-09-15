import sys
import argparse
import pandas as pd
import numpy as np


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("--start_datetime", help="start datetime", type=str,
                        default="2024-02-05T15:00:00")
    parser.add_argument("--end_datetime", help="start datetime", type=str,
                        default="2024-02-08T15:00:00")
    parser.add_argument("--datetime_format", help="datetime format", type=str,
                        default="%Y-%m-%dT%H:%M:%S")
    parser.add_argument("--fs", help="sample frequency (Hz)", type=float,
                        default=50)
    parser.add_argument("--freqs", help="frequencies (Hz)", type=str,
                        default="[.00001157407407407407,1.0,3.0]")
    parser.add_argument("--ampls", help="amplitudes (V)", type=str,
                        default="[1.0,0.1,0.01]")
    parser.add_argument("--phases", help="phases (radians)", type=str,
                        default="[0.0,0.0,0.0]")
    parser.add_argument("--rel_starts", help="fraction where component starts",
                        type=str, default="[0.0,0.0,0.0]")
    parser.add_argument("--rel_ends", help="fraction where component ends",
                        type=str, default="[1.0,1.0,0.3]")
    parser.add_argument("--save_filename", help="save filename", type=str,
                        default="../../data/simulated.parquet.gzip")
    args = parser.parse_args()

    start_datetime_str = args.start_datetime
    end_datetime_str = args.end_datetime
    datetime_format = args.datetime_format
    fs = args.fs
    freqs = [float(freq) for freq in args.freqs[1:-1].split(",")]
    ampls = [float(ampl) for ampl in args.ampls[1:-1].split(",")]
    phases = [float(phase) for phase in args.phases[1:-1].split(",")]
    rel_starts = [float(rel_start)
                  for rel_start in args.rel_starts[1:-1].split(",")]
    rel_ends = [float(rel_end) for rel_end in args.rel_ends[1:-1].split(",")]
    save_filename = args.save_filename

    start_datetime = pd.to_datetime(start_datetime_str, format=datetime_format)
    end_datetime = pd.to_datetime(end_datetime_str, format=datetime_format)
    date_range = pd.date_range(start=start_datetime, end=end_datetime,
                               freq=f"{int(1000.0/fs)}ms")

    t = (date_range - start_datetime).total_seconds()
    x = np.zeros(len(t))
    for i in range(len(freqs)):
        freq = freqs[i]
        ampl = ampls[i]
        phase = phases[i]
        rel_start = rel_starts[i]
        rel_end = rel_ends[i]

        start_index = int(rel_start * len(t))
        end_index = int(rel_end * len(t))
        t_in_range = t[start_index:(end_index+1)]
        x[start_index:(end_index+1)] += \
            ampl * np.sin(2*np.pi*freq*t_in_range+phase)
    df = pd.DataFrame({"dates": date_range, "x": x})
    df.to_parquet(save_filename, compression="gzip")

    breakpoint()


if __name__ == "__main__":
    main(sys.argv)
