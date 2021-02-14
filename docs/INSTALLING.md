# Installing the TallyPi Service

The TallyPi service runs on the
[Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
and allows for remote control of an
[Pimoroni Unicorn pHat](https://shop.pimoroni.com/products/unicorn-phat).
This requires preparing your Raspberry Pi OS image,
installing the libraries from Pimoroni, some Python libraries,
and the TallyPi service itself.


## WiFi Setup for the Raspberry Pi OS

If you have loaded the stock
[Raspberry Pi OS](https://www.raspberrypi.org/downloads/raspberry-pi-os/), you
can set up wireless access for your Pi before it even boots. When you insert
the SD card into your main Windows/Linux/MacOS computer. You should see two
partitions or disk mounts appear - one of them will be labelled "BOOT":

![Mounting the boot partition](./images/boot_part.png)

Within this boot partition we need to create a file named "wpa_supplicant.conf".
Use a text editor (like Notepad or TextEdit or vim) to create a new
wpa_supplicant.conf on this partition of the SD card. You can generate the
contents of this file by using Steve Edson's fantastic Config Generator,
or by modifying this sample [wpa_supplicant.conf](./wpa_supplicant.conf).

Finally, create an empty file in the same mount point simply named "ssh" -
nothing needs to be inside the file. When the Raspberry Pi starts up,
it should see this file and automatically enable SSH connections.

Once you have generated your configuration and saved the file to your SD card,
eject both partitions from your computer and insert the SD card back
into the Raspberry Pi.

After you boot your Raspberry Pi with this configuration file saved in the
BOOT partition, it should connect to your wireless network! If you haven't
changed the hostname of your Raspberry Pi, the default should be "raspberrypi".
Assuming you haven't change your Pi's name, and if your wireless access point
is also your router and DHCP server, within a few minutes you should soon be
able to SSH into your Raspberry Pi using `ssh pi@raspberrypi`.


## Setting Up Your Pi Zero W

There are a few steps you can take to prepare your Pi and make it last
for longer use... especially for studio use.

The first thing you want to do once the Pi is connected to your network is
set a new password, set your hostname, and possibly expand your filesystem
using `sudo raspi-config`.



I would also recommend you set up Uncomplicated Firewall using:

    sudo apt-get install ufw
    sudo ufw allow 7413
    sudo ufw enable

This will start a basic firewall, and open the HTTP port used by the
PiTally service.

You can also reduce the wear & tear on your SD card by moving your logs
to the in-memory tmpfs filesystem and disabling swap memory. To create
mount points for logging you can modify `/etc/fstab` to include:

    tmpfs           /var/tmp        tmpfs   size=10M,nodev,nosuid     0       0
    tmpfs           /var/cache/samba tmpfs   size=5M,nodev,nosuid     0       0

And then modifying `/etc/rsyslog.conf` to point the logging targets to the
tmp filesystem. As an example, you can moving the auth logging to:

    auth,authpriv.*                 /var/tmp/log/auth.log

You can also disable swap using:

    sudo dphys-swapfile swapoff
    sudo systemctl disable dphys-swapfile.service

To be safe, I also usually modify `/etc/dphys-swapfile` likewise to set:

    CONF_SWAPSIZE=0


## Installing the Unicorn pHat Libraries

To install the Unicorn pHat Libraries on your Pi, run the following from
an SSH session:

    sudo apt-get update
    sudo apt-get dist-upgrade
    sudo apt-get clean
    curl https://get.pimoroni.com/unicornhat  | bash


## Installing the TallyPi Service

To install the TallyPi software, first install Python requirements from an
SSH session on your Pi:

    apt-get install python-bottle python-paste

Next, use wget to get the latest package of TallyPi from the release page
at https://github.com/deckerego/tally_pi/releases. For example:

    wget https://github.com/deckerego/tally_pi/releases/download/0.3.1/python-tallypi_0.3.1-1_all.deb

After downloading the package, install it using:

    dpkg -i python-tallypi_0.3.1-1_all.deb

Once the software is installed, you can enable it with:

    sudo systemctl enable tallypi

Then reboot your Pi for everything to kick off!


## Testing the TallyPi Service

If you know the hostname of your Raspberry Pi, open up a web browser and
see if you can load the status URL to test it out. For example, if your
Pi is named `raspberrypi`, try loading the following:

    http://raspberrypi:7413/status

It should reply back with:

    { "red": 0, "green": 0, "blue": 0, "brightness": 0.0 }

You can try turning your LEDs blue with:

    http://raspberrypi:7413/set?color=0000FF&brightness=0.5

This should turn your LEDs blue at 50% brightness.

If you do not know what your Pi's hostname or IP address is, you can use the
[find_lights.sh](../scripts/find_lights.sh) shell script to search your network
for any available TallyPi lights. If your wireless network is on the subnet
192.168.1.1/24, you could search by downloading the script and running:

    find_lights.sh 192.168.1

The script will then crawl across your network, looking for an
open 7413 port.


## Troubleshooting WiFi Issues

The tally lights require a consistent wireless connection to work. Following are some known issues with wireless and Raspbian with the Raspberry Pi Zero W.

### WiFi Adapter Power Saving

Raspbian on the Raspberry Pi Zero W _should_ disable power management on the build-in wireless network interface... but for some reason it seems to switch itself back on every so often. You can confirm this by running `dmesg` and finding the following lines:

    [   28.567231] brcmfmac: brcmf_cfg80211_set_power_mgmt: power save enabled
    [   30.082015] IPv6: ADDRCONF(NETDEV_CHANGE): wlan0: link becomes ready

You can confirm if power saving is on for the default wireless module by running & reviewing:

    pi@tally01:~ $ sudo iwconfig wlan0
    wlan0     IEEE 802.11  ESSID:"YourWifi"  
      Mode:Managed  Frequency:2.462 GHz  Access Point: FE:ED:FA:CE:BE:EF   
      Bit Rate=24 Mb/s   Tx-Power=31 dBm   
      Retry short limit:7   RTS thr:off   Fragment thr:off
      Encryption key:off
      Power Management:on

Note the line `Power Management: on`. This indicates that power management is enabled for the device, even though the Raspbian kernel was supposed to have disabled that.

You can disable power management for a running system using:

    sudo iw wlan0 set power_save off

Your best option to disable power management is to update Raspbian and make sure you are on the latest version - current releases should have this disabled. _However_, if your latest build of Raspbian still does work, you can add the following lines to `/etc/rc.local`:

    # Don't let the default wireless interface go to sleep
    iw wlan0 set power_save off

Note I've attempted to add `wireless-power off` to the interfaces config, but the setting doesn't seem to be properly obeyed in some Raspbian builds.

You can then reboot your tally light and confirm power management is disabled:

    pi@tally01:~ $ sudo iwconfig wlan0
    wlan0     IEEE 802.11  ESSID:"YourWifi"  
      Mode:Managed  Frequency:2.462 GHz  Access Point: FE:ED:FA:CE:BE:EF   
      Bit Rate=24 Mb/s   Tx-Power=31 dBm   
      Retry short limit:7   RTS thr:off   Fragment thr:off
      Encryption key:off
      Power Management:off
