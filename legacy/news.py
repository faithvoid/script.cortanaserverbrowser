import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import urllib2
import textwrap
import re
import HTMLParser  # Use HTMLParser for decoding HTML entities in Python 2.x

def show_news_articles(url=None):
    dialog = xbmcgui.Dialog()
    news_menu = [
        ("Cortana", "https://lain.ftp.sh/cortana/news.xml"),
        ("Insignia (Mastodon)", "https://mas.to/@insignia.rss"),
        ("Xbox-Scene", "https://feeds.feedburner.com/XboxScene"),
        ("The Usual Places Modcast", "https://anchor.fm/s/f5e086d4/podcast/rss"),
        ("Original Xbox (Reddit)", "https://www.ogxbox.org/rss/originalxboxreddit"),
    ]

    titles = [item[0] for item in news_menu]
    
    # If url is provided, skip menu selection and directly fetch the feed
    if url is None:
        selected = dialog.select("Cortana News", titles)
        if selected >= 0:
            _, url = news_menu[selected]
    
    if url:
        root = fetch_and_parse_rss(url)
        if root:
            display_news_items(dialog, root, url)

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

def clean_text(text):
    """Clean up unwanted symbols, characters, and HTML entities from the text."""
    if not text:
        return ""  # Return an empty string if text is None or empty
    
    # Remove HTML tags
    text = re.sub(r'<[^>]*>', '', text)
    
    # Decode HTML entities like &amp;, &lt;, &gt;, etc.
    html_parser = HTMLParser.HTMLParser()
    text = html_parser.unescape(text)
    
    # Remove non-ASCII characters (if any), and replace them with space
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)
    
    # Replace multiple spaces with a single space
    text = re.sub(r'\s+', ' ', text)
    
    # Strip leading and trailing whitespace
    text = text.strip()
    
    return text


def display_news_items(dialog, root, url):
    # Check if it's an RSS or Atom feed
    if root.tag == 'rss':
        channel = root.find('channel')
        if not channel:
            xbmc.log("No channel element found in the RSS feed", xbmc.LOGERROR)
            return

        # Handle RSS items
        items = []
        descriptions = []
        for item in channel.findall('item'):
            title = item.find('title').text if item.find('title') is not None else "No Title"
            description = item.find('description').text if item.find('description') is not None else "No Description"

            title = clean_text(title)
            description = clean_text(description)

            items.append(title)
            wrapped_description = wrap_text(description)
            descriptions.append(wrapped_description)

    elif root.tag == 'feed':
        # Handle Atom feed
        items = []
        descriptions = []
        for entry in root.findall('entry'):
            title = entry.find('title').text if entry.find('title') is not None else "No Title"
            description = entry.find('summary').text if entry.find('summary') is not None else "No Description"
            
            title = clean_text(title)
            description = clean_text(description)

            items.append(title)
            wrapped_description = wrap_text(description)
            descriptions.append(wrapped_description)

    else:
        xbmc.log("Unrecognized feed format", xbmc.LOGERROR)
        return

    selected = dialog.select("Articles", items)
    if selected >= 0:
        # Display multiple dialog boxes if the description is too long
        wrapped_description = descriptions[selected]
        page = 0
        while page * 3 < len(wrapped_description):
            dialog_lines = [
                wrapped_description[page * 3] if page * 3 < len(wrapped_description) else '',
                wrapped_description[page * 3 + 1] if page * 3 + 1 < len(wrapped_description) else '',
                wrapped_description[page * 3 + 2] if page * 3 + 2 < len(wrapped_description) else ''
            ]
            
            dialog_lines = [line for line in dialog_lines if line.strip() != '']

            dialog_response = dialog.ok(
                items[selected], 
                *dialog_lines
            )
            
            if dialog_response == 1:  # "OK" button pressed (A), go forward
                page += 1
            elif dialog_response == 0:  # "Back" button pressed (B), go backward
                if page > 0:
                    page -= 1
                else:
                    break  # If we're at the first page, exit the loop
            else:
                break  # If the dialog is closed, exit the loop

        display_news_items(dialog, root, url)  # Go back to the article list if exiting the article view

    else:
        show_news_articles()  # Go back to the source selection menu if exiting the article list

if __name__ == '__main__':
    show_news_articles()
