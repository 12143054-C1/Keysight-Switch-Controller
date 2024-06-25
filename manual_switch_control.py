import pyvisa
import time
import AgilentSwitchL8990D001 as switch

def fnCheckRelayStatus(CommObj, sRelayInfo, bPrint=True):
    """Check status of Agilent Switch
    Args:
        CommObj        -- visa object
        sRelayInfo     -- Relay info comma separated
        bPrint         -- Prints log message to console
    """
    query_command = "ROUTE:OPEN? (@%s)" % sRelayInfo

    if bPrint:
        print("%s %s" % (CommObj.resource_name, query_command))

    CommObj.write(query_command)
    time.sleep(0.05)

    response = CommObj.read()

    return response

class Switch_Class:
    def __init__(self,):
        self.switch_obj = None

    def connect(self, ip=""):
        self.ip = ip
        try:
            self.switch_obj = switch.fnConnect(self.ip)
            return True
        except:
            print("Connection to switch failed!")
            self.switch_obj = None
            return False

    def close_relay(self, relay_num):
        switch.fnCloseRelay(self.switch_obj, relay_num)

    def disconnect(self):
        if self.switch_obj != None:
            switch.fnDisconnect(self.switch_obj)
            print("Disconnected from switch :)")
        else:
            print("No connected switch. Exiting.")

    def get_individual_relay_status(self, relay_num):
        try:
            status = self.query_relay_status(self.ip, relay_num)
            print(f"Relay {relay_num} status response: {status}")
            return status
        except Exception as e:
            print(f"Error querying relay {relay_num} status: {e}")
            return None

    def get_all_relay_statuses(self, relay_numbers):
        closed_relays = []
        for relay_num in relay_numbers:
            status = self.get_individual_relay_status(relay_num)
            if status and 'Closed' in status:
                closed_relays.append(relay_num)
        print(f"Closed relays: {closed_relays}")
        return closed_relays

    def query_relay_status(self, ip_address, sRelayInfo):
        # rm = pyvisa.ResourceManager()
        # resource = f'TCPIP0::{ip_address}::INSTR'
        # instrument = rm.open_resource(resource)

        # # Increase the timeout to 10 seconds
        # instrument.timeout = 10000  # Timeout in milliseconds

        try:
            relay_status = fnCheckRelayStatus(self.switch_obj, sRelayInfo)
            return relay_status
        except pyvisa.errors.VisaIOError as e:
            print(f"An error occurred: {e}")
            return None
        finally:
            # instrument.close()
            pass

if __name__ == "__main__":
    ip_address = "169.254.44.15"
    my_switch = Switch_Class(ip_address)

    if my_switch.connect():
        # List of relay numbers to check, update according to your setup
        relay_numbers = [   1111,
                            1112,
                            1113,
                            1114,
                            1115,
                            1116]
        my_switch.get_all_relay_statuses(relay_numbers)
        my_switch.disconnect()
