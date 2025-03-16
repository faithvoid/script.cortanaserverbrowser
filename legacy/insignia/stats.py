import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import urllib2
import re

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

def clean_html(text):
    """ Remove HTML tags and line breaks from text. """
    # Remove common HTML tags
    clean_text = re.sub(r'<[^>]+>', '', text)
    # Remove line breaks and excessive whitespace
    clean_text = re.sub(r'\s+', ' ', clean_text).strip()
    return clean_text

def display_stats(dialog, channel):
    stats = ['...']  # Inserting the '...' at the beginning of the list
    for item in channel.findall('item'):
        title_elem = item.find('title')
        if title_elem is not None:
            title_text = title_elem.text.strip()
            if any(prefix in title_text for prefix in ["Users Online", "Registered Users", "Games Supported", "Active Games"]):
                description_elem = item.find('description')
                description = clean_html(description_elem.text) if description_elem is not None else "No description available"
                stats.append(title_text)

    selected = dialog.select("Stats", stats)
    if selected == 0:  # Check if '...' was selected
        xbmc.executebuiltin('RunScript(Q:\\scripts\\Cortana Server Browser\\insignia\\insignia.py)')
    elif selected > 0:  # If any actual stat is selected
        xbmcgui.Dialog().ok("Statistics", stats[selected])
    else:
        xbmc.log("No statistic selected or dialog cancelled", xbmc.LOGERROR)

def main():
    dialog = xbmcgui.Dialog()
    url = "https://ogxbox.org/rss/insignia.xml"

    root = fetch_and_parse_rss(url)
    if root is not None:
        channel = root.find('channel')
        if channel is not None:
            display_stats(dialog, channel)
        else:
            xbmc.log("No channel element found", xbmc.LOGERROR)
    else:
        xbmcgui.Dialog().ok("Error", "Failed to load stats information!")

if __name__ == '__main__':
    main()
