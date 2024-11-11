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

if __name__ == '__main__':
    local_ip = get_local_ip()
    external_ip = get_external_ip()
    dialog = xbmcgui.Dialog()

    if external_ip == 'N/A':
        # Display a connection error message if the external IP cannot be fetched
        dialog.ok("Connection Failed!", "Local IP: {}".format(local_ip), "Internet IP: N/A", "Check your network settings/cables and try again.")
	xbmc.executebuiltin('RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\settings.py)')
    else:
        # Display both local and internet IP addresses if the external IP is fetched successfully
        dialog.ok("Success!", "Local IP: {}".format(local_ip), "Internet IP: {}".format(external_ip), "Your Xbox is connected to the internet!")
	xbmc.executebuiltin('RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\settings.py)')
