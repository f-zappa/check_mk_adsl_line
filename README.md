⚠️ Sorry, but I won't put more effort into this plugin. FTTH is coming to our village, we already have the empty tube in our house and are waiting for the actual fibre which should come within the rest of the year. After that, we don't need DSL anymore.

# Check-MK plugin for monitoring adsl lines
This Check checks status of an ADSL line via the SNMP ADSL-LINE-MIB. Written for and tested with a DrayTek Vigor165, should work on other DrayTek ADSL routers/modems and probably with other hardware (feedback is welcome). 

If want to try this with other Hardware than Vigor165/160/130, you will need to adjust the snmp_scan_function.

The ADSL line is usually on interface #4, although this should be autodiscovered by the plugin.

New Version (>1.1) requires CMK >2.0.0! If you use an older version, look in the v0.7 branch (but be warned, this code is really ugly).
