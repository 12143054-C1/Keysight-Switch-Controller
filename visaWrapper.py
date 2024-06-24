from __future__ import print_function
############################################################################
# INTEL CONFIDENTIAL
# Copyright 2005 2006 2007 Intel Corporation All Rights Reserved.
#
# The source code contained or described herein and all documents related
# to the source code ("Material") are owned by Intel Corporation or its
# suppliers or licensors. Title to the Material remains with Intel Corp-
# oration or its suppliers and licensors. The Material may contain trade
# secrets and proprietary and confidential information of Intel Corpor-
# ation and its suppliers and licensors, and is protected by worldwide
# copyright and trade secret laws and treaty provisions. No part of the
# Material may be used, copied, reproduced, modified, published, uploaded,
# posted, transmitted, distributed, or disclosed in any way without
# Intel's prior express written permission.
#
# No license under any patent, copyright, trade secret or other intellect-
# ual property right is granted to or conferred upon you by disclosure or
# delivery of the Materials, either expressly, by implication, inducement,
# estoppel or otherwise. Any license under such intellectual property
# rights must be express and approved by Intel in writing.
#
# visaWrapper.py
#
#
# Created on:      09-Dec-2015
# Original author: Garrett Twogood
# Edited by gtwogood 14-Jan-2016
#
# This is the visa wrapper that allows you to use any version of pyvisa without having
# to modify your instrument code commands.
#
#
############################################################################

from builtins import object
import pyvisa as visa

class PyvisaWrapper(object):
    """
    This wrapper allows you to be able to use any version of pyVisa.  < 1.5 used diffent methods to write
    to the instruments.  You can look at the documentation at https://pyvisa.readthedocs.org/en/stable/migrating.html

    Attributes:
        visaVersion : The visa version that is installed on the host
        timeout : Allows user to create a custom timeout time instead of the default one
        visaWrapper : The visa object instrument object
    """
    def __init__(self, bStubMode = False, bVerbose=False, bErrChk = False):
        """
        Figures out which version of visa is installed on the host.  Based on this it will know which commands to use
        params:
          bStubMode (bool): When True, instrument communication will not be done.  query commands will return empty string values
          bVerbose (bool): when True, each command and query result will be printed to the console
          bErrChk (bool): When True, each write() call will query for errors and raise an exception if any exist.
                          note: calling user must set the fnCheckErrors method to use
        """
        self.StubMode = bStubMode
        self.Verbose = bVerbose
        self.ErrChk = bErrChk
        if hasattr(visa, '__version__'):
            if visa.__version__ == "1.5":
                self._visaVersion = 'Legacy'
            else:
                self._visaVersion = visa.__version__
        else:
            self._visaVersion = 'Legacy'

    @property
    def visaVersion(self):
        return self._visaVersion

    @visaVersion.setter
    def visaVersion(self, version):
        self._visaVersion = version

    @property
    def timeout(self):
        return self._timeout

    @property
    def resource_name(self):
        return self.visaWrapper.resource_name

    @timeout.setter
    def timeout(self, timeout):

        if self.visaVersion == "Legacy":
            self._timeout = timeout
        else:
            self._timeout = timeout * 1000
        if self.StubMode:    return
        self.visaWrapper.timeout = self._timeout

    def instrument(self, sInstrument):
        """
            connects to the instrument given the information from the instrument sript
            @Args
                sInstrument - The SCPI connection string.  It can be in any format that the instrument allows
        """
        if self.StubMode:
            return
        if self.visaVersion == "Legacy":
            self.visaWrapper = visa.instrument(sInstrument)
        else:
            rm = visa.ResourceManager()
            self.visaWrapper = rm.open_resource(sInstrument)

    def write(self, sSCPI):
        """
            This function sends the SCPI command that you want to execute to the correct version
            @Args
                sSCPI - SCPI string you want executed
        """
        if self.Verbose:    print("visaWrapper.write(%s)" % sSCPI)
        if self.StubMode:    return
        self.visaWrapper.write(sSCPI)
        if self.ErrChk:
            e = self.fnCheckErrors()
            if len(e) > 0:
                raise Exception("WARNING: errors generated after write(%s) to instrument.  Please verify hardware:\n%s" % (sSCPI, e))

    def fnCheckErrors(self):
        ''' place holder function for checking instrument errors
        Developer note: the calling instrument must assign this method, for example:
        inst = PyvisaWrapper()
        inst.fnCheckErrors = fnCheckErrors()
        '''
        raise NotImplementedError("User must assign this function in the calling instrument.  Please read visawrapper comments for more information.")
    def ask(self, sSCPI):
        """
            This function asks(send and receives) the SCPI command that you want to execute to the correct version.
            It will return the result from the command.
            @Args
                sSCPI - SCPI string you want executed
        """
        if self.Verbose:    print("visaWrapper.ask(%s)" % sSCPI)
        if self.StubMode:    return ""
        try:
            if self.visaVersion == 'Legacy':
                r = self.visaWrapper.ask(sSCPI)
            else:
                r = self.visaWrapper.query(sSCPI)
            if self.Verbose:    print(r)
            return r
        except:
            print("exception after instrument query command: %s.  (timeout = %s)" % (sSCPI, self._timeout )) # tell the user a bit more about where this issue occurred
            raise

    def read(self):
        """
            This function reads the SCPI command that you want to get back.
        """
        return self.visaWrapper.read()

    def visaLockQ(self):
        """
            Instrument lock checking when using multiple connections to the instrument.  This is mostly used when
            using threading with an instrument
        """
        self.lock_excl()
        if self.StubMode:
            esr = 0
        else:
            esr = int(self.visaWrapper.query("*ESR?").strip("\n")) # Event Status Register query
        if (esr != 0):
            print()
            print()
            print("***** visa query error")
            print("instrument: %s" % self.visaWrapper.resource_name)
            print("command: %s" % sSCPI)
            print("result: %s" % result)
            print("*ESR? %d" % esr)
            print(":SYST:ERR?")
            print(self.visaLockErrorQ())
            print()
        self.unlock()

    def visaLockErrorQ(self):
        """
            Instrument error checking when using multiple connections to the instrument.  This is mostly used when
            using threading with an instrument
        """
        self.lock_excl()
        retVal = ""
        while True:
            if self.StubMode:
                s = "NO ERROR"
            else:
                s = self.visaWrapper.query(":SYST:ERR?") # read entire error queue from oldest to newest
            if "NO ERROR" not in s.upper():
                retVal += s
            else:
                break
        self.unlock()
        return retVal

    def lock_excl(self):
        """
            Establish an exclusive lock to the resource. Only used in 1.6 >=
        """
        if self.StubMode:    return
        if not self.visaVersion == 'Legacy':
            self.visaWrapper.lock_excl()

    def unlock(self):
        """
            Relinquishes a lock for the specified resource. Only used in 1.6 >=
        """
        if self.StubMode:    return
        if not self.visaVersion == 'Legacy':
            self.visaWrapper.unlock()

    def close(self):
        """
            Closes the connection to the instrument
        """
        if self.StubMode:    return
        self.visaWrapper.close()

    def delay(self, delay):
        """
            Sets the delay in seconds between write and read operations.
            @Args
                delay - delay in seconds
        """
        if self.StubMode:    return
        if hasattr(self.visaWrapper, 'delay'):         #Pyvisa <= 1.4
            self.visaWrapper.delay = delay
        elif hasattr(self.visaWrapper, 'ask_delay'):     #Pyvisa >= 1.5
            self.visaWrapper.ask_delay = delay
        elif hasattr(self.visaWrapper, 'query_delay'):   #Pyvisa >= 1.6
            self.visaWrapper.query_delay = delay


if __name__ == '__main__':
    stubMode = True
    print("Testing Stub Mode: %s" % stubMode)
    Instrument = PyvisaWrapper(bStubMode=stubMode)
    sConnectionString = ""
    Instrument.instrument(sConnectionString)
    Instrument.timeout = 20
    print("checking errors...")
    Instrument.visaLockErrorQ()
    print("establishing lock...")
    Instrument.visaLockQ()
    print("IDN = %s" % Instrument.ask("*IDN?"))
    print("visaVersion = %s" % Instrument.visaVersion)
    print("timeout = %s" % Instrument.timeout)

    Instrument.close()
