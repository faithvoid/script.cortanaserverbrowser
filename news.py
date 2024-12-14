import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import urllib2
import textwrap
import re
import HTMLParser  # Use HTMLParser for decoding HTML entities in Python 2.x

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

def show_news_articles(url=None):
    dialog = xbmcgui.Dialog()
    news_menu = [
        ("Cortana", "https://lain.ftp.sh/cortana/news.xml"),
        ("Insignia", "https://mas.to/@insignia.rss"),
        ("Xbox-Scene", "https://feeds.feedburner.com/XboxScene"),
        ("The Usual Places Modcast", "https://anchor.fm/s/f5e086d4/podcast/rss"),
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

        # Clean and strip HTML tags from title and description
        title = clean_text(title)
        description = clean_text(description)

        # If the URL is for the Insignia feed, use description as title
        if url == "https://mas.to/@insignia.rss":
            items.append(description)
        else:
            items.append(title)
        
        wrapped_description = wrap_text(description)
        descriptions.append(wrapped_description)

    selected = dialog.select("Articles", items)
    if selected >= 0:
        # Display multiple dialog boxes if the description is too long
        wrapped_description = descriptions[selected]
        page = 0
        while page * 3 < len(wrapped_description):
            # Prepare the text for the current page (up to 3 lines)
            dialog_lines = [
                wrapped_description[page * 3] if page * 3 < len(wrapped_description) else '',
                wrapped_description[page * 3 + 1] if page * 3 + 1 < len(wrapped_description) else '',
                wrapped_description[page * 3 + 2] if page * 3 + 2 < len(wrapped_description) else ''
            ]
            
            # Remove any empty lines to avoid gaps
            dialog_lines = [line for line in dialog_lines if line.strip() != '']

            # Display the current page without user prompts
            dialog_response = dialog.ok(
                items[selected],  # Article title
                *dialog_lines  # The wrapped description lines
            )
            
            # Handle forward and backward navigation
            if dialog_response == 1:  # "OK" button pressed (A), go forward
                page += 1
            elif dialog_response == 0:  # "Back" button pressed (B), go backward
                if page > 0:
                    page -= 1
                else:
                    break  # If we're at the first page, exit the loop
            else:
                break  # If the dialog is closed, exit the loop

        # After exiting the article view, return to the article list
        display_news_items(dialog, root, url)  # Go back to the article list

    else:
        # If the user exits from the article list, return to the source menu
        show_news_articles()  # Go back to the source selection menu

if __name__ == '__main__':
    show_news_articles()
