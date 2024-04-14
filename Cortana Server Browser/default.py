import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import urllib2
import sys

ddef fetch_and_parse_rss(url):
    try:
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3')
        request.add_header('Referer', 'http://www.google.com')
        
        response = urllib2.urlopen(request)
        # Ensure the data read is treated as UTF-8
        data = response.read().decode('utf-8')
        root = ET.fromstring(data.encode('utf-8'))  # Re-encode it to UTF-8 if necessary for XML parsing
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
    ]
    
    feed_list = [name for name, _ in feeds]
    selected = dialog.select(u"Choose a feed", feed_list)
    
    if selected >= 0:
        name, url = feeds[selected]
        root = fetch_and_parse_rss(url)
        if root is not None:
            channel = root.find('channel')
            if channel is not None:
                items = []
                for item in channel.findall('item'):
                    title_elem = item.find('title')
                    description_elem = item.find('description')
                    
                    item_title = title_elem.text if title_elem is not None else u"No title available"
                    item_description = description_elem.text if description_elem is not None else u"No description available"

                    # Ensure both parts of the format are Unicode
                    items.append(u"{} - {}".format(item_title, item_description).encode('utf-8'))
                
                dialog.select(u"Items in {}".format(name), items)
            else:
                xbmc.log("No channel element found", xbmc.LOGERROR)
        else:
            xbmcgui.Dialog().ok("Error", "Failed to load the RSS feed.")
    else:
        xbmc.log("No feed selected or dialog cancelled", xbmc.LOGERROR)

if __name__ == '__main__':
    main()
