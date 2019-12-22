Features
--------

* Configure and switch a G-Homa power plug
* No external dependencies
* No javascript

Requirements
------------

* Python 3

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

Some more information from here could be used:

* https://github.com/poldy79/ghoma2mqtt

Vendor webpage:

* http://www.g-homa.com/index.php/en
