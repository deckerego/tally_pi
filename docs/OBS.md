# OBS Script

TallyPi was created to work with [OBS](https://obsproject.com/) as a script
that fires whenever a video input source switches from program, preview,
or idle modes.


## Installing Python for OBS

Currently OBS requires Python 3.7 shared libraries in order to execute
Python scripts. On Windows this can be done using a Python 3.7 installer,
and on MacOS or Linux this can be most easily managed through `pyenv`.

To install `pyenv` on MacOS I recommend first installing
[Homebrew](https://brew.sh/), and then installing `pyenv` via:

    brew update
    brew install pyenv

On MacOS and Linux you can ask `pyenv` to generate the shared libraries with:

    CONFIGURE_OPTS=--enable-shared pyenv install 3.7.8

Once Python is installed, point OBS to the installation path by opening
OBS and navigating to Tools -> Scripts -> Python Settings

![OBS Python settings](./images/obs_python.png)


## Installing the TallyPi Script

Download the latest OBS Python script for TallyPi from the release page
at https://github.com/deckerego/tally_pi/releases

Store the script wherever you like, then add the script to OBS by navigating
to Tools -> Scripts and adding the `obs_tally_light.py` script
that you just downloaded.


## Configuring the TallyPi Script

Once the script is installed, you can use the settings interface to specify
colors for idle/preview/program cameras, and map each camera source to an
IP address or hostname that corresponds to a tally light.

![OBS script settings](./imags/obs_settings.png)
