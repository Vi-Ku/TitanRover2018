# Oled board Schematic 
Audstanley Oled Board.fzb
is the fritzing file for manufacturing.  This board consists of an ethernet connector on the board,
and a custom cable will need to be made with an ethernet on one end, and four usb to serial devices on the other end.

I used the CP2102 chip serial to usb by: Silabs.
These CP2102 can be flashed with a serial number using the USBxpress Dev Software from Silabs' website.

It's important to flash unique serial numbers to the CP2102 chips, so our linux computers can assign a symlink
to the /dev/someCustomName device, otherwise on startup, our python scripts will not know which serial device is which
and our scripts will fail. By applying a serial number, I have created: 
/etc/udev/rules.d/99-usb-serial.rules
and applied the following to that file:

```
SUBSYSTEM=="tty",
ATTRS{idVendor}=="Silicon Labs",
ATTRS{idProduct}=="titan rover",
ATTRS{serial}=="1000",
SYMLINK+="oled1"
SUBSYSTEM=="tty",
ATTRS{idVendor}=="Silicon Labs",
ATTRS{idProduct}=="titan rover",
ATTRS{serial}=="1001",
SYMLINK+="oled2"
SUBSYSTEM=="tty",
ATTRS{idVendor}=="Silicon Labs",
ATTRS{idProduct}=="titan rover",
ATTRS{serial}=="1002",
SYMLINK+="oled3"
SUBSYSTEM=="tty",
ATTRS{idVendor}=="Silicon Labs",
ATTRS{idProduct}=="titan rover",
ATTRS{serial}=="1003",
SYMLINK+="oled4"
```

Now whenever the oleds are attached to linux, oLed#.py  can attach to either 
/dev/oled1
/dev/oled2
/dev/oled3
/dev/oled4

The idProduct was also changed in the flashing process of the CP2102 to: titan rover
in the USBxpress software, idProduct, can be found under the Product ID field.


Here is the result of the circuit board:

## Top of the board:
![circuit board top]()


## Bottom of the board:
![circuit board bottom]()