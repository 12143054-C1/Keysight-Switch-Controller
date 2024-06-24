#-------------------------------------------------------------------------------
# Name:        module2
# Purpose:
#
# Author:      mvhlab
#
# Created:     07/10/2021
# Copyright:   (c) mvhlab 2021
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from lunarlake.debug.domains.sio_dv.instruments import AgilentSwitchL8990D001 as switch
import sys, time, math, datetime, csv


def GetSwitchDict(switch_map=r"\\ger\ec\proj\ha\MVH_LAB\Groups\ATD_IO\LNL\PCIe5\LNL_Tx_Switch_Map.csv"):
    """ """
    did_titles = False
    dSwitchMap={}
    with open(switch_map) as map_file:
        reader = csv.reader(map_file, skipinitialspace=True)
        for row in reader:
            print(row)
            if did_titles == False:
                did_titles = True
            else:
                dSwitchMap[row[0]] = row[1]
    return dSwitchMap


def ConnectToSwitch():
    """ """
    ## dSwitchMap = GetSwitchDict()
    Switch_Module = switch
    switch1 = switch.fnConnect('169.254.44.16')
    return switch1
# end ConnectToScope

def getSwitchLink(ip='169.254.44.16'):
        """ """
        if ip == switch_ip_1:
            return switch1

def TerminateSwitchConnection(switch_tmp):
        """ """
        switch.fnDisconnect(switch_tmp)

def SwitchCloseRelay_P_N(txrx, nLane, Switch_Module , switch_tmp):
        """ Supported lanes are updated in Excel C:\pythonsv\raptorlake\debug\domains\hsio_dv\hsphy\test_flows\tx\Switch_Matrix\Tx_Switch_Map.csv
            {'LNL_TX_L0_P': {'169.254.44.16': '1111,1162'},
             'LNL_TX_L0_N': {'169.254.44.16': '1211,1262'},
             'LNL_TX_L1_P': {'169.254.44.16': '1112,1162'},
             'LNL_TX_L1_N': {'169.254.44.16': '1212,1262'},
             'LNL_TX_L2_P:  {'169.254.44.16': '1113,1162'},
             'LNL_TX_L2_N': {'169.254.44.16': '1213,1262'},
             'LNL_TX_L3_P': {'169.254.44.16': '1114,1162'},
             'LNL_TX_L3_N': {'169.254.44.16': '1214,1262'},
             'LNL_RX_L0_P': {'169.254.44.16': '1115'},
             'LNL_RX_L0_N': {'169.254.44.16': '1215'},
             'LNL_RX_L1_P': {'169.254.44.16': '1116'},
             'LNL_RX_L1_N': {'169.254.44.16': '1216'},
             'LNL_RX_L2_P': {'169.254.44.16': '1121'},
             'LNL_RX_L2_N': {'169.254.44.16': '1221'},
             'LNL_RX_L3_P': {'169.254.44.16': '1122'},
             'LNL_RX_L3_N': {'169.254.44.16': '1222'},
        """
        dSwitchMap = GetSwitchDict()

        P_Values = dSwitchMap["LNL"+"_"+str(txrx)+"_"+str(nLane)+"_P"]
        N_Values = dSwitchMap["LNL"+"_"+str(txrx)+"_"+str(nLane)+"_N"]


##        P_Values = "1123, 1103"
##        N_Values = "1113, 1113"

        #switch_tmp = getSwitchLink(str(switch_ip))
        Switch_Module.fnCloseRelay(switch_tmp, P_Values)

        #switch_tmp = getSwitchLink(str(switch_ip))
        Switch_Module.fnCloseRelay(switch_tmp, N_Values)

   # end TerminateScopeConnection

##        Switch_Module.fnCloseRelay(1156, 1133)
##        Switch_Module.fnCloseRelay(1253, 1233)



if __name__ == '__main__':
    ## switchDict = GetSwitchDict()
    ######## getSwitchLink = getSwitchLink()
    switchConnection = ConnectToSwitch()
    SwitchCloseRelay_P_N(txrx = 'RX', nLane = 'L0', Switch_Module = switch , switch_tmp = switchConnection)
    SwitchCloseRelay_P_N(txrx = 'TX', nLane = 'L0', Switch_Module = switch , switch_tmp = switchConnection)

    # In Order to see the signal on scope - please un comment the below:
##    switch.fnCloseRelay(switchConnection, "1142")
##    switch.fnCloseRelay(switchConnection, "1242")
##    switch.fnCloseRelay(switchConnection, "1165")
##    switch.fnCloseRelay(switchConnection, "1265")

    TerminateSwitchConnection(switch_tmp = switchConnection)


    pass

