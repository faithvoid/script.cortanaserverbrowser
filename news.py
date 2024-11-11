import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import urllib2
import textwrap
import re

def fetch_and_parse_rss(url):
    try:
        request = urllib2.Request(url)
        request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
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

def wrap_text(text, width=64):
    """Wrap text to the specified width."""
    return textwrap.wrap(text, width)

def show_news_articles():
    dialog = xbmcgui.Dialog()
    news_menu = [
        ("Cortana", "http://lain.ftp.sh/cortana/news.xml"),
        ("Insignia", "https://mas.to/@insignia.rss"),
        ("Xbox-Scene", "http://feeds.feedburner.com/XboxScene"),
    ]

    titles = [item[0] for item in news_menu]
    selected = dialog.select("Cortana News", titles)

    if selected >= 0:
        _, url = news_menu[selected]
        root = fetch_and_parse_rss(url)
        if root:
            display_news_items(dialog, root,url)

def strip_tags(html):
    return re.sub(r'<[^>]*>', '', html)

def display_news_items(dialog, root, url):
    channel = root.find('channel')
    if not channel:
        xbmc.log("No channel element found in the feed", xbmc.LOGERROR)
        return

    items = []
    descriptions = []
    for item in channel.findall('item'):
        title = item.find('title').text if item.find('title') is not None else "No Title"
        description = item.find('description').text if item.find('description') is not None else "No Description"
        # If the URL is for the Insignia feed, use description as title
        if url == "https://mas.to/@insignia.rss":
	    description = strip_tags(description)
            items.append(description)
        else:
            items.append(title)
        wrapped_description = wrap_text(description)
        descriptions.append(wrapped_description)

    selected = dialog.select("Articles:", items)
    if selected >= 0:
        # Display multiple dialog boxes if the description is too long
        wrapped_description = descriptions[selected]
        for i in range(0, len(wrapped_description), 3):
            response = dialog.ok(items[selected], 
                          wrapped_description[i] if i < len(wrapped_description) else '', 
                          wrapped_description[i+1] if i+1 < len(wrapped_description) else '', 
                          wrapped_description[i+2] if i+2 < len(wrapped_description) else '')
            if not response:  # If "No" is selected
                break

if __name__ == '__main__':
    show_news_articles()
