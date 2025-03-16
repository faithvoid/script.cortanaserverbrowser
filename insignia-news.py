import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import urllib2
import textwrap
import re
import HTMLParser  # Use HTMLParser for decoding HTML entities in Python 2.x

def show_news_articles():
    url = "https://bsky.app/profile/insignia.live/rss"
    root = fetch_and_parse_rss(url)
    if root:
        display_news_items(xbmcgui.Dialog(), root, url)

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
    return textwrap.wrap(text, width)

def clean_text(text):
    if not text:
        return ""
    text = re.sub(r'<[^>]*>', '', text)
    html_parser = HTMLParser.HTMLParser()
    text = html_parser.unescape(text)
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def display_news_items(dialog, root, url):
    if root.tag == 'rss':
        channel = root.find('channel')
        if not channel:
            xbmc.log("No channel element found in the RSS feed", xbmc.LOGERROR)
            return
        items = []
        descriptions = []
        for item in channel.findall('item'):
            title = clean_text(item.find('title').text if item.find('title') is not None else "")
            description = clean_text(item.find('description').text if item.find('description') is not None else "No Description")
            if not title.strip():
                title = description
            items.append(title)
            descriptions.append(wrap_text(description))
    elif root.tag == 'feed':
        items = []
        descriptions = []
        for entry in root.findall('entry'):
            title = clean_text(entry.find('title').text if entry.find('title') is not None else "No Title")
            description = clean_text(entry.find('summary').text if entry.find('summary') is not None else "No Description")
            items.append(title)
            descriptions.append(wrap_text(description))
    else:
        xbmc.log("Unrecognized feed format", xbmc.LOGERROR)
        return
    while True:
        selected = dialog.select("News - Insignia", items)
        if selected < 0:
            return  # Exit if user cancels selection
        wrapped_description = descriptions[selected]
        page = 0
        while page * 3 < len(wrapped_description):
            dialog_lines = [wrapped_description[i] for i in range(page * 3, min((page + 1) * 3, len(wrapped_description)))]
            dialog_response = dialog.ok(items[selected], *dialog_lines)
            if dialog_response == 1:
                page += 1
            else:
                break
if __name__ == '__main__':
    show_news_articles()
