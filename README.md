# TallyPi

A network controlled tally light for cameras, intended for control by OBS.

Currently this is offered as alpha - we still have a bit of a way to go
before this is stable.

## Hardware

TallyPi is built for the Raspberry Pi and Pimoroni Unicorn pHat. It also
supports hardware buttons/switches to shutdown the Pi and wake it back up.

## Software

Software was built to expose the Unicorn pHat through an HTTP interface and
an OBS script that maps preview/program/idle status to AV input sources.

### Unicorn HTTP Interface

An HTTP interface is provided that allows for color control and brightness
to be specified remotely. As an example:

    http://192.168.1.1:7413/set?color=AA22FF&brightness=0.3

Would set the Unicorn pHat to purple across all LEDs, at 30% brightness.

The status of the Unicorn pHat is available as:

    http://192.168.1.1:7413/status

### OBS Script

Once added to OBS, the obs_tally_light script will allow you to map AV input
sources to IP addresses that correspond to Unicorn HTTP interfaces. Colors are
assigned to program/preview/idle status in OBS, along with brightness.
