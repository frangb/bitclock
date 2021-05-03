# bitclock
bitclock is a project to display bitcoin-related information on a raspberry Pi zero W with an e-ink display.

<img src="https://github.com/frangb/bitclock/blob/master/raspi-blockclock.jpg" alt="bitclock" width="300"/>


## Shopping list
We will need the following material. I leave the Aliexpress links of what I have bought, but actually you can buy it wherever you want (amazon, ...)
- 1 x Raspberry Pi Zero W, with pre-welded header [link](https://es.aliexpress.com/item/4000693620101.html?spm=a2g0s.9042311.0.0.5d5363c0IMK1H6)
- 1 x micro hdmi to hdmi cable (or micro hdmi to hdmi adaptor, if you already have a hdmi cable) [link](https://es.aliexpress.com/item/10000404075798.html?spm=a2g0s.9042311.0.0.5d5363c0IMK1H6)
- 1 x power supply for raspberry pi zero (only if you need it. In case you have a power strip to connect it via USB with 5V output it would not be necessary).
- 1 x 2'13 inches waveshare e-ink screen [link](https://es.aliexpress.com/item/4001261285356.html?spm=a2g0s.9042311.0.0.5d5363c0IMK1H6)
- 1 x USB keyboard (puedes usar cualquier teclado que tengas por casa, ya que va a ser solo un momento) and one USB to mini-USB adaptor [link](https://es.aliexpress.com/item/1005001894830612.html?spm=a2g0o.productlist.0.0.3e52645fcWv8zN&algo_pvid=e53fb4cd-43b2-458f-9b1c-6b3fcd091c48&algo_expid=e53fb4cd-43b2-458f-9b1c-6b3fcd091c48-4&btsid=2100bde116178130299921634edfcd&ws_ab_test=searchweb0_0,searchweb201602_,searchweb201603_)
- 1 x tarjeta microSD de 8 GB o superior

## Assembly
If we have purchased the Raspberry Pi Zero w with the header pin already welded, there will be no complications. We will simply fit the screen in the GPIO port of the Raspberry and that's it.

## Operating system for the raspberry pi zero
Download the Raspberry Pi OS Lite operating system from the following official address
https://www.raspberrypi.org/software/operating-systems/

We must install the Operating System on a SD card large enough (a small one of 1 GB should be enough). To burn the image I personally use the Etcher application. It is multiplatform and you can download it [here](https://www.balena.io/etcher/)

## Configuration and first steps
Insert the SD card into the raspberry pi zero, connect the hdmi cable to the monitor, a keyboard and connect to the power.
Log in with `user: pi` and `password: raspberry`, and run the following command:
```
sudo raspi-config
```
In the configuration menu you should make the following changes:

**wifi setup**
    System options / Wireless LAN: setup your home wifi (SSID and password)

**activate SSH**
    Interface options / SSH / enable

**activate SPI**
    Interface options / SPI / enable

Once this is done, we could in theory disconnect the monitor and keyboard of our Raspberry Pi and continue the whole process opening an SSH terminal from a computer in the same local network. To do this we first need to obtain the IP address of the Raspberry Pi:
```
ifconfig
```
after executing this command we will get something like this:

```
lo: flags=73<UP,LOOPBACK,RUNNING>  mtu 65536
        inet 127.0.0.1  netmask 255.0.0.0
        inet6 ::1  prefixlen 128  scopeid 0x10<host>
        loop  txqueuelen 1000  (Local Loopback)
        RX packets 0  bytes 0 (0.0 B)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 0  bytes 0 (0.0 B)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0

wlan0: flags=4163<UP,BROADCAST,RUNNING,MULTICAST>  mtu 1500
        inet 192.168.1.136  netmask 255.255.255.0  broadcast 192.168.1.255
        inet6 fe80::a21:977c:c3f5:8fee  prefixlen 64  scopeid 0x20<link>
        ether b8:27:eb:ec:d7:d8  txqueuelen 1000  (Ethernet)
        RX packets 22986  bytes 17167770 (16.3 MiB)
        RX errors 0  dropped 0  overruns 0  frame 0
        TX packets 7194  bytes 1042225 (1017.7 KiB)
        TX errors 0  dropped 0 overruns 0  carrier 0  collisions 0
```
We must write down the address that appears in the interface wlan0, in the case of the example it would be ```inet 192.168.1.136```

Now, to connect to our Raspberry Pi from any other computer that is on the local network, just open a terminal on that computer (In windows, with the cmd command, on Mac and linux by opening a terminal) and run:
```
ssh pi@<raspberry pi ip address>
```
The system will ask for the user's password. Write ```raspberry```

## Install tools and dependencies
```
sudo apt-get update
sudo apt-get install git
sudo apt-get install python3-pip
sudo apt-get install python3-pil
sudo apt-get install libatlas-base-dev
```

## Download bitclock code
Download the project from github
```
git clone https://github.com/frangb/bitclock
```
Install the required packages
```
cd bitclock
sudo pip3 install -r requirements.txt
```

## Script execution
Usage:
```
python3 btc_ticker.py [-h] [-t TIME] [-c {USD,EUR}] [-d {PRICE,BLOCK,PRCBLK}] [-tz TIMEZONE]
```

The following optional arguments are available:

**-h, --help**: Displays a help message explaining the use of each of the optional parameters.

**-t, --time**: refresh time (in seconds) after which we want the price to update. I recommend you not to use a very short interval as the page from where you get the data could block your IP. An interval of 5 (300 s) or 10 (600 s) minutes should work fine. If nothing is indicated, by default 60 seconds will be taken.

**-c, --currency**: USD or EUR depending on the currency you want to use. If nothing is indicated, by default it will be shown in USD.

**-d, --display**: information to be displayed on the screen. write PRICE if you only want to show the price, BLOCK if you want to show the current block height and the estimated fees for immediate / 30 min / 1 hour confirmation, or PRCBLK if you want to toggle between both modes. If nothing is specified, by default the price will be displayed.

**-tz, --timezone**: this is used to correctly display the time of the last update at the top of the screen. You can check the available time zones [here](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones). Choose one of the zones in the "TZ database name" column, for example "Europe/Madrid". If nothing is specified, the "Europe/Madrid" zone will be used by default..

a) In case you want to start the script automatically after turning the Raspberry Pi Zero on, you must add the following line to the rc.local file
```
sudo nano /etc/rc.local
```
At the end of the file, before the line ````exit 0```, add the following command:
```
python3 /home/pi/bitclock/btc_ticker.py -t 300 -c USD -d PRICE -tz Europe/Madrid &
```
*In this example I have used as refresh interval 5 minutes (300 seconds) and as time zone Europe/Madrid, but you can change these parameters at your convenience*.

b) To manually start the script, run it as follows, so that the process does not stop after you close the SSH session:
```
nohup python3 /home/pi/bitclock/btc_ticker.py -t 300 -c USD -d PRICE -tz Europe/Madrid
```

## Optional
If you want to turn the green LED light on the Raspberry Pi Zero W off, you can do it with the following command:
```
echo none | sudo tee /sys/class/leds/led0/trigger
```
This line can also be added in rc.local if desired, so that the light is always turned off when restarting the Raspberry Pi Zero

## ¿How to update?
If the project has undergone any change and you need to update it, you only have to access via ssh to your raspberry pi zero, delete the application directory using the command:
```
rm -rf bitclock
```

and then redownload the repository using the command:
```
git clone https://github.com/frangb/bitclock
```