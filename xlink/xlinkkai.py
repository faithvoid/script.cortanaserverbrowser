import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import sys

def main():
    dialog = xbmcgui.Dialog()
    feeds = [
        ("...", "RunScript(Q:\\scripts\\Cortana Server Browser\\default.py)"),
        ("Sessions", "RunScript(Q:\\scripts\\Cortana Server Browser\\xlink\\browser.py)"),
        ("Statistics", "RunScript(Q:\\scripts\\Cortana Server Browser\\xlink\\stats.py)"),
        ("Events", "RunScript(Q:\\scripts\\Cortana Server Browser\\xlink\\events.py)"),
        ("News", "RunScript(Q:\\scripts\\Cortana Server Browser\\xlink\\news.py)"),
        ("Enable Notifications", "RunScript(Q:\\scripts\\Cortana Server Browser\\xlink\\notify.py)"),
	("Disable Notifications", "StopScript(Q:\\scripts\\Cortana Server Browser\\xlink\\notify.py)"),
    ]
    
    feed_list = [name for name, _ in feeds]
    selected = dialog.select(u"Cortana Server Browser - XLink Kai", feed_list)
    
    if selected >= 0:
        name, url = feeds[selected]
        if "RunScript" in url:
            xbmc.executebuiltin(url)

if __name__ == '__main__':
    main()
