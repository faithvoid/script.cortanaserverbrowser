import xbmc
import xbmcgui
import socket
import urllib2

def get_local_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0)
        try:
            # Use loopback IP to initialize the interface
            s.connect(('127.0.0.1', 1))
            IP = s.getsockname()[0]
        except Exception:
            IP = 'N/A'
        finally:
            s.close()
    except socket.error:
        IP = 'N/A'
    return IP

def get_external_ip():
    try:
        response = urllib2.urlopen('http://httpbin.org/ip', timeout=5)
        result = response.read()
        external_ip = eval(result)['origin']
    except:
        external_ip = 'N/A'
    return external_ip

def check_insignia_connection():
    hostname = "macs.xboxlive.com"
    target_ip1 = "46.101.64.175"
    target_ip2 = "49.13.57.101"

    try:
        # Resolve the hostname to an IP address
        ip_address = socket.gethostbyname(hostname)
        # Determine connection status
        if ip_address == target_ip1 or ip_address == target_ip2:
            return "Success", "Connected to Insignia!"
        else:
            return "Failure", "You are NOT conneted to Insignia!"
    except socket.gaierror:
        return "Error", "Failed to resolve hostname."

if __name__ == '__main__':
    local_ip = get_local_ip()
    external_ip = get_external_ip()

    # Check Insignia connection status
    insignia_status, insignia_message = check_insignia_connection()

    # Build and display the final dialog
    if external_ip == 'N/A':
        xbmcgui.Dialog().ok(
            "Connection Failed!",
            "Local IP: " + local_ip,
            "Internet IP: N/A",
            "Check your network settings and try again."
        )
    else:
        xbmcgui.Dialog().ok(
            "Network Status",
            "Local IP: " + local_ip,
            "Internet IP: " + external_ip,
            insignia_message
        )
