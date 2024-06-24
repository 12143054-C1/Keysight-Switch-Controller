import AgilentSwitchL8990D001 as switch

class Switch_Class():
    def __init__(self, ip="") -> None:
        if ip == "":
            print("No Switch IP provided!")
        else:
            self.switch_obj = switch.fnConnect(ip)
            #self.switch_obj.timeout = 5000  # Set timeout to 5 seconds

    def CloseRelay(self, relay_num):
        switch.fnCloseRelay(self.switch_obj, relay_num)

    def disconnect(self):
        switch.fnDisconnect(self.switch_obj)
        print("Disconnected from switch :)")

    def get_individual_relay_status(self, relay_num):
        try:
            # Replace 'RELAY:STATUS?' with the actual command to get the status of a specific relay
            status = self.switch_obj.ask(f'RELAY{relay_num}:STATUS?')
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

if __name__ == "__main__":
    ip_address = "169.254.44.15"
    my_switch = Switch_Class(ip_address)

    # List of relay numbers to check, update according to your setup
    #relay_numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    #my_switch.get_all_relay_statuses(relay_numbers)
    my_switch.disconnect()
