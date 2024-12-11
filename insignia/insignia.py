import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import sys

def main():
    dialog = xbmcgui.Dialog()
    feeds = [
        ("...", "RunScript(Q:\\scripts\\Cortana Server Browser\\default.py)"),
        ("Sessions", "RunScript(Q:\\scripts\\Cortana Server Browser\\insignia\\browser.py)"),
        ("Statistics", "RunScript(Q:\\scripts\\Cortana Server Browser\\insignia\\stats.py)"),
        ("Events", "RunScript(Q:\\scripts\\Cortana Server Browser\\insignia\\events.py)"),
        ("Enable Notifications", "RunScript(Q:\\scripts\\Cortana Server Browser\\insignia\\notify.py)"),
	("Disable Notifications", "StopScript(Q:\\scripts\\Cortana Server Browser\\insignia\\notify.py)"),
        ("Insignia Connection Test", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\internettest.py)"),
    ]
    
    feed_list = [name for name, _ in feeds]
    selected = dialog.select(u"Cortana Server Browser - Insignia", feed_list)
    
    if selected >= 0:
        name, url = feeds[selected]
        if "RunScript" in url:
            xbmc.executebuiltin(url)

if __name__ == '__main__':
    main()
