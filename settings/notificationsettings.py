import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import sys

def main():
    dialog = xbmcgui.Dialog()
    feeds = [
        ("...", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\settings.py)"),
        ("Enable Insignia Notifications On Startup", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\insigniastartup.py)"),
        ("Disable Insignia Notifications On Startup", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\noinsigniastartup.py)"),
        ("Enable XLink Kai Notifications On Startup", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\xlinkstartup.py)"),
        ("Disable XLink Kai Notifications On Startup", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\noxlinkstartup.py)"),
    ]
    
    feed_list = [name for name, _ in feeds]
    selected = dialog.select(u"Cortana Server Browser - Settings", feed_list)
    
    if selected >= 0:
        name, url = feeds[selected]
        if "RunScript" in url:
            xbmc.executebuiltin(url)

if __name__ == '__main__':
    main()
