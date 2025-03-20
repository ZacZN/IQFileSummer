from iqtools import *
import argparse
import numpy as np

LFRAMES = 1024

def parse_dataset(dataset):
    data_arr = []
    with open(dataset, "r") as f:
        for line in f:
            val = line.splitlines()
            data_arr.append(val)

    return data_arr

def process_loop(dataset, path, output_name):
    zz = np.array([])
    for filename in dataset:
        fullpath = path + filename[0]
        print(f"Processing {filename}")
        iq = get_iq_object(fullpath)
        iq.read_samples(1)
        lframes = LFRAMES
        nframes = int(iq.nsamples_total / lframes)
        iq.read_samples(nframes * lframes)
        z = get_cplx_spectrogram(
            iq.data_array, lframes=lframes, nframes=nframes
        )
        if np.shape(zz)[0] == 0:
            zz.resize((nframes, lframes))
            zz += np.abs(z)
        else:
            zz += np.abs(z)

    print(f"Plotting to {output_name}.png")
    xx, yy, _ = iq.get_power_spectrogram(lframes=lframes, nframes=nframes)
    plot_spectrogram(xx, yy, np.abs(np.fft.fftshift(zz, axes=1)), filename=output_name, cen=iq.center,
                     dbm=False, title=output_name)

def main():

    # Parse text file containing the names of the data files, and the path to those files
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dataset", type=str, required=True, help=".txt file containing names of data files - 1 file per line"
    )

    parser.add_argument(
        "--path", type=str, required=True, help="Path to the data files"
    )

    parser.add_argument(
        "--outputname", required=True, help="Name for output files"
    )

    args = parser.parse_args()
    dataset = args.dataset
    path = args.path
    output_name = args.outputname

    data_arr = parse_dataset(dataset)

    process_loop(dataset=data_arr, path=path, output_name=output_name)

if __name__ == "__main__":
    main()

