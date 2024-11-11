import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import sys

def main():
    dialog = xbmcgui.Dialog()
    feeds = [
        ("...", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\settings.py)"),
        ("480p Game Loaders", "RunScript(Q:\\scripts\\Cortana Server Browser\\Settings\\x4g\\480p Game Loaders\\default.py)"),
        ("Clean Program Thumbs", "RunScript(Q:\\scripts\\Cortana Server Browser\\Settings\\x4g\\Clean Program Thumbs\\default.py)"),
        ("DVD2Xbox", "RunScript(Q:\\scripts\\Cortana Server Browser\\Settings\\x4g\\DVD2Xbox\\default.py)"),
        ("File Patcher", "RunScript(Q:\\scripts\\Cortana Server Browser\\Settings\\x4g\\File Patcher\\default.py)"),
        ("Generate Favourites", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\x4g\\Generate Favourites\\default.py)"),
        ("Remove Empty Save Folders", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\x4g\\Remove Empty Save Folders\\default.py)"),
        ("XISO to HDD Installer", "RunScript(Q:\\scripts\\Cortana Server Browser\\settings\\x4g\\XISO to HDD Installer\\default.py)"),
    ]
    
    feed_list = [name for name, _ in feeds]
    selected = dialog.select(u"Cortana Server Browser - Settings", feed_list)
    
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
