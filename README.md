# IQFileSummer
Sums the data from several IQ datafiles and saves it in .npz format.

Not guaranteed to work yet!

### Requirements
Requires numpy and [IQTools](https://github.com/xaratustrah/iqtools). Check the installation instructions under the IQTools repo.

### Use
Set the desired settings in the config file, then run the script:

    python IQFileSummer.py

### config.toml

The different settings in the config file are as follows:

    * `file_list` - the list of data files to sum together. Format is a text file with the name of each file on a new line. Type: str
    * `file_path` - path to the data files. Type: str
    * `output_location` - location where you want to save the .npz output file. Type: str
    * `lframes` - frame length, _i.e._ the number of frequency bins. This then determines the value of nframes (number of time bins). Type: int
    * `t_start` - time of the first data file, used to generate the name of the .npz file. Type: str
    * `t_end` - time of the last data file, also used for name generation. Type: str
    * `experiment_name` - name of the experiment, also for name generation. Type: str
