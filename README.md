Python scripts to configure and control a G-Homa WiFi plug

Files
-----

* configure.py: Use to set the plug to use your host as control server
* do.py: Control script to switch the plug

Setup
-----

* Set up the plug via the G-Homa app (iOS or Android)
* Configure the plug to use your local host as control server
  * Edit the file and adjust the values for `dev`, `ctrl`, and `port` to your situation
  * Run the script: `./configure.py`

Usage
-----

* Read the switch status

  `do.py`

* Switch plug on

  `do.py on`

* Switch plug off

  `do.py off`

Caveats
-------

* only a single plug is supported for now
* when the control program is not running, the plug LED will blink

Acknowledgments
---------------

A lot of information was found here:

* https://github.com/rodney42/node-ghoma
* https://seclists.org/fulldisclosure/2015/May/45
* https://wiki.fhem.de/wiki/G-Homa

