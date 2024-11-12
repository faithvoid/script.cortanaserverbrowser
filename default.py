import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import sys

def main():
    dialog = xbmcgui.Dialog()
    feeds = [
        ("Insignia", "RunScript(Q:\\scripts\\Cortana Server Browser\\insignia\\insignia.py)"),
        ("XLink Kai", "RunScript(Q:\\scripts\\Cortana Server Browser\\xlink\\xlinkkai.py)"),
        ("Cortana News", "RunScript(Q:\\scripts\\Cortana Server Browser\\news.py)"),
    ]
    
    feed_list = [name for name, _ in feeds]
    selected = dialog.select(u"Cortana Server Browser", feed_list)
    
    if selected >= 0:
        name, url = feeds[selected]
        if "RunScript" in url:
            xbmc.executebuiltin(url)

if __name__ == '__main__':
    main()
