import xbmc
import xbmcgui
import socket

def check_ip():
    hostname = "macs.xboxlive.com"
    target_ip1 = "46.101.64.175"
    target_ip2 = "49.13.57.101"
    
    try:
        # Resolve the hostname to an IP address
        ip_address = socket.gethostbyname(hostname)
        # Compare the resolved IP with the target IPs
        if ip_address == target_ip1:
            xbmcgui.Dialog().ok("Success!", "Success, you're connected to Insignia! Frag on, soldier!")
        elif ip_address == target_ip2:
            xbmcgui.Dialog().ok("Connection Test Successful!", "Xbox Live IP address reported back as " + ip_address, "which means you're connected to Insignia!", "Frag on, soldier!")
        else:
            xbmcgui.Dialog().ok("Failed to connect to Insignia", "Xbox Live IP address reported back as " + ip_address, "which means your DNS isn't being redirected!")
    except socket.gaierror:
        xbmcgui.Dialog().ok("Insignia Connection Test", "Failed to resolve hostname.")

if __name__ == "__main__":
    check_ip()
