# OBS Script

TallyPi was created to work with [OBS](https://obsproject.com/forum/resources/tallypi-push-scene-changes-to-wifi-enabled-tally-lights.1082/) as a script
that fires whenever a video input source switches from program, preview,
or idle modes.

Starting with version 26 OBS no longer supports Python scripts on MacOS, so
now there are two options: invoke `curl` using a Lua script or call
your lights directly over HTTP with a Python script.


## Installing the Lua Script

Download the latest OBS Lua script for TallyPi from the release page
at https://github.com/deckerego/tally_pi/releases

Store the script wherever you like, then add the script to OBS by navigating
to Tools -> Scripts and adding the `obs_tally_light.lua` script
that you just downloaded.

Note that you must have `curl` installed on your machine for the script
to function. Rather than calling HTTP endpoints directly, the script has
to make a system call to the `curl` command line tool.


## Installing the Python Script

Installing the Python version of the script requires a specific version
of Python 3.7 with shared libraries installed, and then installing the
Python script itself.

### Installing Python for OBS

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


### Installing the TallyPi Python Script

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

If you are having trouble finding your lights by hostname, you can use either
the [HTML dashboard page](../scripts/dashboard.html) or
[find_lights.sh](../scripts/find_lights.sh) command-line script to search
your network for available lights. Either option will provide you with an IPv4
address for each light found which can be used to setup the OBS plugin.
