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
        ("News", "RunScript(Q:\\scripts\\Cortana Server Browser\\insignia\\news.py)"),
        ("Enable Notifications", "RunScript(Q:\\scripts\\Cortana Server Browser\\insignia\\Notify.py)"),
	("Disable Notifications", "StopScript(Q:\\scripts\\Cortana Server Browser\\insignia\\notify.py)"),
        ("Insignia Connection Test", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\insigniatest.py)"),
    ]
    
    feed_list = [name for name, _ in feeds]
    selected = dialog.select(u"Cortana Server Browser - Insignia", feed_list)
    
    if selected >= 0:
        name, url = feeds[selected]
        if "RunScript" in url:
            xbmc.executebuiltin(url)

def display_feed_items(dialog, channel, name):
    items = []
    for item in channel.findall('item'):
        title_elem = item.find('title')
        description_elem = item.find('description')  # Assuming description is the correct tag for item description
        
        item_title = title_elem.text if title_elem is not None else u"Not Available"
        item_description = description_elem.text if description_elem is not None else u""
        
        items.append(u"{} {}".format(item_title, item_description))
    
    dialog.select(u"Cortana Server Browser - {}".format(name), items)

if __name__ == '__main__':
    main()