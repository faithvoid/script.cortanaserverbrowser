import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import sys

def main():
    dialog = xbmcgui.Dialog()
    feeds = [
        ("...", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\settings.py)"),
        ("Enable / Disable Insignia Notifications On Startup", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\startup\\autoexec-insignia.py)"),
        ("Enable / Disable XLink Kai Notifications On Startup", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\startup\\autoexec-xlinkkai.py)"),
    ]
    
    feed_list = [name for name, _ in feeds]
    selected = dialog.select(u"Cortana Server Browser - Settings", feed_list)
    
    if selected >= 0:
        name, url = feeds[selected]
        if "RunScript" in url:
            xbmc.executebuiltin(url)

if __name__ == '__main__':
    main()
