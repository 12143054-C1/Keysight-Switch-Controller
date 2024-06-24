from __future__ import print_function
#-------------------------------------------------------------------------
# Intel Corporation
# Copyright 2011 - All Rights Reserved
# Department  : MDO
# Written by  : Supriya Kilambi
# Modified by : Garrett Twogood
# Date        : 03/09/2016
# Description : Library for controlling the Agilent N6705B.
#-------------------------------------------------------------------------
import os
from visaWrapper import PyvisaWrapper as visaClass
import time
import string


def fnConnect(PortInfo, VisaAlias=""):
    """
        Connect to device via TCPIP
        @Args
            PortInfo : could be full connection string or TCPIP info
            VisaAlias : Alias created for visa insrument
        @Returns
            CommObj : visa object
    """
    print("Connecting to CommObj TCPIP(%s)..."%(PortInfo))
    global CommObj
    CommObj = visaClass()
    try:
        if(VisaAlias != ""):
            CommObj.instrument(VisaAlias)
        else:
            if(PortInfo.upper().startswith("T")==True):
                #Raw Connection String
                CommObj.instrument(PortInfo)
            else:
                #TCPIP IP#
                CommObj.instrument("TCPIP::%s::INSTR"%PortInfo)
        CommObj.timeout = 30
        print("Connected to %s"%(CommObj.ask("*IDN?")))
        return(CommObj)
    except:
        ## print(traceback.format_exc())
        print("Unable to connect to CommObj %s\n"%PortInfo)
        raise Exception("Unable to connect to CommObj %s\n"%PortInfo)

def fnDisconnect(CommObj):
    """
    Disconnect from instrument
    @Args
        CommObj : visa object
    """
    CommObj.close()
    print("Agilent N6705B Communication Port Closed")


def fnOpenRelay(CommObj,sRelayInfo,bPrint=True):
    """Disconnect Agilent Switch
    Args:
        CommObj        -- visa object
        sRelayInfo     -- Relay info comma separated
        bPrint         -- Prints log message to console
    """
    if(bPrint):
        print("%s ROUTE:OPEN (@%s)"%(CommObj.resource_name,sRelayInfo))
    CommObj.write("ROUTE:OPEN (@%s)"%(sRelayInfo))
    time.sleep(0.1)

def fnCloseRelay(CommObj,sRelayInfo,bPrint=True):
    """Disconnect Agilent Switch
    Args:
        CommObj        -- visa object
        sRelayInfo     -- Relay info comma separated
        bPrint         -- Prints log message to console
    """
    if(bPrint):
        print("%s ROUTE:CLOSE (@%s)"%(CommObj.resource_name,sRelayInfo))
    CommObj.write("ROUTE:CLOSE (@%s)"%(sRelayInfo))
    time.sleep(0.1)

def fnGetErrorMessage(CommObj):
    """
    ##>>> CommObj.ask("SYSTem:ERRor?")
    ##'+949,"Open operation not valid for this channel configuration; Chan 1146"\n'
    """
    return CommObj.ask("SYSTem:ERRor?")

def fnGetDeviceInfoIDN(CommObj):
    """
    ##>>> CommObj.ask("SYSTem:ERRor?")
    ##'+949,"Open operation not valid for this channel configuration; Chan 1146"\n'
    """
    return CommObj.ask("*IDN?")


