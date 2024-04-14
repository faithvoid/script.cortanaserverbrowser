import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import urllib2
import sys

def fetch_and_parse_rss(url):
    try:
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
        request.add_header('Referer', 'http://www.google.com')
        
        response = urllib2.urlopen(request)
        data = response.read().decode('utf-8')
        root = ET.fromstring(data.encode('utf-8'))
        return root
    except urllib2.HTTPError as e:
        xbmc.log("HTTP Error: {}".format(e.code), xbmc.LOGERROR)
        return None
    except urllib2.URLError as e:
        xbmc.log("URL Error: {}".format(e.reason), xbmc.LOGERROR)
        return None
    except Exception as e:
        xbmc.log("Failed to fetch or parse the feed: {}".format(str(e)), xbmc.LOGERROR)
        return None

def main():
    dialog = xbmcgui.Dialog()
    feeds = [
        (u"Insignia", "https://ogxbox.org/rss/insignia.xml"),
        (u"XLink Kai", "https://www.ogxbox.org/rss/xlinkkai"),
        ("Insignia Connection Test", "RunScript(Q:\scripts\Cortana Server Browser\InsigniaConnectTest.py)"),
        ("Insignia Notifier", "RunScript(Q:\scripts\Cortana Server Browser\notifier.py)"),
    ]
    
    feed_list = [name for name, _ in feeds]
    selected = dialog.select(u"Cortana Server Browser", feed_list)
    
    if selected >= 0:
        name, url = feeds[selected]
        if "RunScript" in url:
            xbmc.executebuiltin(url)
        else:
            root = fetch_and_parse_rss(url)
            if root is not None:
                channel = root.find('channel')
                if channel is not None:
                    items = []
                    for item in channel.findall('item'):
                        title_elem = item.find('title')
                        description_elem = item.find('')  # Ensure this is the correct tag in your XML
                        
                        item_title = title_elem.text if title_elem is not None else u"Not Available"
                        item_description = description_elem.text if description_elem is not None else u""
                        
                        items.append(u"{} {}".format(item_title, item_description))
                    
                    dialog.select(u"Cortana Server Browser - {}".format(name), items)
                else:
                    xbmc.log("No channel element found", xbmc.LOGERROR)
            else:
                xbmcgui.Dialog().ok("Error", "Failed to load server information!")
    else:
        xbmc.log("No server selected or dialog cancelled", xbmc.LOGERROR)

if __name__ == '__main__':
    main()
