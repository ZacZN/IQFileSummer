from iqtools import tools
import numpy as np
import toml

with open("config.toml", "r") as f:
    config = toml.load(f)

def parse_dataset(dataset):
    data_arr = []
    with open(dataset, "r") as f:
        for line in f:
            val = line.splitlines()
            data_arr.append(val)

    return data_arr


def data_summer(dataset, path, output_location):

    zz = np.array([])
    ref_pos = None
    for filename in dataset:
        fullpath = path + filename[0]
        print(f"Processing {filename}")
        iq = tools.get_iq_object(fullpath)
        iq.read_samples(1)
        nframes = int(iq.nsamples_total / lframes)
        iq.read_samples(nframes * lframes)
        xx, yy, _ = iq.get_power_spectrogram(lframes=lframes, nframes=nframes)
        z = tools.get_cplx_spectrogram(
            iq.data_array,
            lframes=lframes,
            nframes=nframes
        )

        z_real = np.abs(z)

        sly = slice(0, np.shape(yy)[0])

        proj_spec = np.sum(z_real[sly,:], axis=0)
        max_bin = np.argmax(proj_spec)

        if f_shift_tracking == "True":
            if ref_pos is None:
                ref_pos = max_bin
                shift = 0
            else:
                shift = max_bin - ref_pos

            print(f"Ref. pos.: {ref_pos}, Cur. pos.: {max_bin}")
            z_real = np.roll(z_real, shift=-shift, axis=1)

        if np.shape(zz)[0] == 0:
            zz.resize((nframes, lframes))
            zz += z_real
        else:
            zz += z_real

    output_name = f"{experiment_name}_{t_start}-{t_end}_{lframes}lframes-{nframes}nframes"

    print(f"Saving data to file {output_name}.npz in location {output_location}")
    np.savez(output_location + output_name + ".npz", xx+iq.center, yy, np.abs(np.fft.fftshift(zz, axes=1)))

t_start = config["settings"]["t_start"]
t_end = config["settings"]["t_end"]
lframes = config["settings"]["lframes"]
lframes = int(lframes)
experiment_name = config["settings"]["experiment_name"]
output_location = config["settings"]["output_location"]
f_shift_tracking = config["settings"]["f_shift_tracking"]

file_list = config["settings"]["file_list"]
file_path = config["settings"]["file_path"]

def main():

    dataset = parse_dataset(file_list)

    data_summer(dataset=dataset, path=file_path, output_location=output_location)

if __name__ == "__main__":
    main()