import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import sys

def main():
    dialog = xbmcgui.Dialog()
    feeds = [
        ("...", "RunScript(Q:\\scripts\\Cortana Server Browser\\default.py)"),
        ("Xbox Dashboard", "RunXBE(E:\\Apps\\MS Xbox Dashboard\\default.xbe)"),
        ("Dashboard Network Settings", "RunXBE(E:\\Apps\\MS Online Dashboard\\default.xbe)"),
        ("Internet Connection Test", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\internettest.py)"),
        ("Notification Settings", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\notificationsettings.py)"),
        ("XBMC4Gamers Scripts", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\x4g.py)"),
#       ("Update Cortana", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\update.py)"),
    ]
    
    feed_list = [name for name, _ in feeds]
    selected = dialog.select(u"Cortana Server Browser - Settings", feed_list)
    
    if selected >= 0:
        name, url = feeds[selected]
        if "RunScript" in url:
            xbmc.executebuiltin(url)

if __name__ == '__main__':
    main()
