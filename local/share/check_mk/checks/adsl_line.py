#!/usr/bin/python

# Description: Check-MK plugin for monitoring adsl lines
# File: adsl_line.py
# Version: 1.1 (requires check_mk 2.0)
# Author: Ulrich Baumann <check_mk@uli-baumann.de>
#
# https://www.draytek.com/support/knowledge-base/5517
# supported ADSL-LINE-MIB OIDs in Draytek Vigor Routers
# (ADSL and VDSL are using same OIDs)
# 1.3.6.1.2.1.10.94.1.1.1.1.1 adslLineCoding
# 1.3.6.1.2.1.10.94.1.1.1.1.2 adslLineType
# 1.3.6.1.2.1.10.94.1.1.1.1.3 adslLineSpecific
# 1.3.6.1.2.1.10.94.1.1.1.1.4 adslLineConfProfile
# 1.3.6.1.2.1.10.94.1.1.1.1.5 adslLineAlarmConfProfile
# 1.3.6.1.2.1.10.94.1.1.3.1.1 adslAturInvSerialNumber
# 1.3.6.1.2.1.10.94.1.1.3.1.2 adslAturInvVendorID
# 1.3.6.1.2.1.10.94.1.1.3.1.3 adslAturInvVersionNumber
# 1.3.6.1.2.1.10.94.1.1.3.1.4 adslAturCurrSnrMgn
# 1.3.6.1.2.1.10.94.1.1.3.1.5 adslAturCurrAtn
# 1.3.6.1.2.1.10.94.1.1.3.1.6 adslAturCurrStatus
# 1.3.6.1.2.1.10.94.1.1.3.1.7 adslAturCurrOutputPwr
# 1.3.6.1.2.1.10.94.1.1.3.1.8 adslAturCurrAttainableRate
# 1.3.6.1.2.1.10.94.1.1.4.1.2 adslAtucChanCurrTxRate (DSL router's Rx Rate)
# 1.3.6.1.2.1.10.94.1.1.5.1.1 adslAturChanInterleaveDelay
# 1.3.6.1.2.1.10.94.1.1.5.1.2 adslAturChanCurrTxRate (DSL router's Tx rate)
# 1.3.6.1.2.1.10.94.1.1.5.1.3 adslAturChanPrevTxRate
# 1.3.6.1.2.1.10.94.1.1.5.1.4 adslAturChanCrcBlockLength

from .agent_based_api.v1 import *
from .utils.interfaces import cleanup_if_strings
from cmk.base.check_api import get_nic_speed_human_readable


# helper function for combining states
def worst(old,new):
    if (new==State.CRIT) or (old==State.CRIT):
      return State.CRIT
    elif (new==State.WARN) or (old==State.WARN):
      return State.WARN
    else: return State.OK

# discovery function
def discover_adsl_line(section):
    for oid_end,adslLineCoding, adslLineType, adslLineSpecific, \
        adslAturInvSerialNumber, adslAturInvVendorID, adslAturInvVersionNumber, \
        adslAturCurrSnrMgn, adslAturCurrAtn, adslAturCurrStatus, adslAturCurrOutputPwr, \
        adslAturCurrAttainableRate, adslAtucChanCurrTxRate, adslAturChanCurrTxRate \
    in section:
        yield Service(item=oid_end)  # item name follows oid enumeration

# check function
def check_adsl_line(item, params, section):
    # constants from ADSL-LINE-MIB
    adslLineCodings = { 1: "other", 2: "dmt", 3: "cap", 4: "qam" }
    adslLineTypes =   { 1: "noChannel", 2: "fastOnly", 3: "interleavedOnly", \
                        4: "fastOrInterleaved", 5: "fastAndInterleaved" }
    # iterate ADSL Lines
    for oid_end,adslLineCoding, adslLineType, adslLineSpecific, \
        adslAturInvSerialNumber, adslAturInvVendorID, adslAturInvVersionNumber, \
        adslAturCurrSnrMgn, adslAturCurrAtn, adslAturCurrStatus, adslAturCurrOutputPwr, \
        adslAturCurrAttainableRate, adslAtucChanCurrTxRate, adslAturChanCurrTxRate \
    in section:
        if (item != oid_end): continue
        status = State.OK
        statusString = ''
        perfData = []
        # check link status
        adslAturCurrStatus=cleanup_if_strings(adslAturCurrStatus)
        statusString += adslAturCurrStatus
        if adslAturCurrStatus != "SHOWTIME":
            status = worst(status, State.CRIT)
        # check upstream
        statusString += ', Up: '+get_nic_speed_human_readable(adslAturChanCurrTxRate)
        if 'upstream_params' in params:
            upstream_warn,upstream_crit = params['upstream_params']
            upstream_warn=int(upstream_warn)*10**6
            upstream_crit=int(upstream_crit)*10**6
            if int(adslAturChanCurrTxRate) < upstream_crit:
                status = worst(status, State.CRIT)
                statusString += ' (CRIT at '+get_nic_speed_human_readable(upstream_crit)+')'
            elif int(adslAturChanCurrTxRate) < upstream_warn:
                status = worst(status, State.WARN)
                statusString += ' (WARN at '+get_nic_speed_human_readable(upstream_warn)+')'
        else: upstream_warn,upstream_crit=None,None
        yield Metric("adsl_up_rate",int(adslAturChanCurrTxRate), levels=(upstream_warn,upstream_crit))
        # check downstream
        statusString += ', Down: '+get_nic_speed_human_readable(adslAtucChanCurrTxRate)
        if 'downstream_params' in params:
            downstream_warn,downstream_crit = params['downstream_params']
            downstream_warn=downstream_warn*10**6
            downstream_crit=downstream_crit*10**6
            if int(adslAtucChanCurrTxRate) < downstream_crit:
                status = worst(status, State.CRIT)
                statusString += ' (CRIT at '+get_nic_speed_human_readable(downstream_crit)+')'
            elif int(adslAtucChanCurrTxRate) < downstream_warn:
                status = worst(status, State.WARN)
                statusString += ' (WARN at '+get_nic_speed_human_readable(downstream_warn)+')'
        else: downstream_warn,downstream_crit=None,None
        yield Metric("adsl_down_rate",int(adslAtucChanCurrTxRate),levels=(downstream_warn,downstream_crit))

        # attainable data rate
        statusString += ', Attainable: '+get_nic_speed_human_readable(adslAturCurrAttainableRate)
        yield Metric("adsl_attainable",int(adslAturCurrAttainableRate))

        # check snr_margin
        statusString += ', SNR Margin: ' + adslAturCurrSnrMgn+' dB'
        if 'snr_margin_params' in params:
            snr_margin_warn,snr_margin_crit = params['snr_margin_params']
            if int(adslAturCurrSnrMgn) < snr_margin_crit:
                status = worst(status, State.CRIT)
                statusString += ' (CRIT at '+str(snr_margin_crit)+' dB)'
            elif int(adslAturCurrSnrMgn) < snr_margin_warn:
                status = worst(status, State.WARN)
                statusString += ' (WARN at '+str(snr_margin_warn)+' dB)'
        else: snr_margin_warn,snr_margin_crit=None,None
        yield Metric("adsl_snr_margin",int(adslAturCurrSnrMgn),levels=(snr_margin_warn,snr_margin_crit))

        # check attenuation
        statusString += ', Attenuation: ' + adslAturCurrAtn+' dB'
        if 'attenuation_params' in params:
            attenuation_warn,attenuation_crit = params['attenuation_params']
            if int(adslAturCurrAtn) > attenuation_crit:
                status = worst(status, State.CRIT)
                statusString += ' (CRIT at '+str(attenuation_crit)+' dB)'
            elif int(adslAturCurrAtn) > attenuation_warn:
                status = worst(status, State.WARN)
                statusString += ' (WARN at '+str(attenuation_warn)+' dB)'
        else: attenuation_warn,attenuation_crit=None,None
        yield Metric("adsl_attenuation",int(adslAturCurrAtn),levels=(attenuation_warn,attenuation_crit))

        # additional info for status string
        statusString +=  ', '+\
        'Output Power: '+adslAturCurrOutputPwr+' db, '+\
        'Line Coding: '+adslLineCodings.get(int(adslLineCoding),"unknown")+', '+\
        'Line Type: '+adslLineTypes.get(int(adslLineType),"unknown")
        yield Metric("adsl_output_power",int(adslAturCurrOutputPwr))

        yield Result(state=status,summary=f"{statusString}")


register.snmp_section(
    name = "adsl_line",
    detect = matches(".1.3.6.1.2.1.1.1.0", ".*Vigor(130|165).*"),
    fetch = SNMPTree(
      base = '.1.3.6.1.2.1.10.94.1.1',
      oids = [
       OIDEnd(), # interface number
       "1.1.1", # adslLineCoding
       "1.1.2", # adslLineType
       "1.1.3", # adslLineSpecific
       "3.1.1", # adslAturInvSerialNumber
       "3.1.2", # adslAturInvVendorID
       "3.1.3", # adslAturInvVersionNumber
       "3.1.4", # adslAturCurrSnrMgn
       "3.1.5", # adslAturCurrAtn
       "3.1.6", # adslAturCurrStatus
       "3.1.7", # adslAturCurrOutputPwr
       "3.1.8", # adslAturCurrAttainableRate
       "4.1.2", # adslAtucChanCurrTxRate
       "5.1.2", # adslAtucChanCurrTxRate
       ] ),
) 

CHECK_DEFAULT_PARAMETERS = {
  'downstream_params': (0,0),
  'upstream_params': (0,0),
  'attenuation_params': (30,45),
  'snr_margin_params': (10,6),
}

register.check_plugin(
    name = "adsl_line",
    service_name = "ADSL Interface %s",
    discovery_function = discover_adsl_line,
    check_function = check_adsl_line,
    check_ruleset_name="adsl_line",
    check_default_parameters=CHECK_DEFAULT_PARAMETERS,
)
