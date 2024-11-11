import xbmc
import xbmcgui
import xml.etree.ElementTree as ET
import urllib2
import os
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

def clean_game_name(game_name):
    # Regex to match and remove the pattern ": number player(s)" and anything that follows
    pattern = r':\s*\d+\s*players?.*$'
    # Using regex to search and replace the part that matches the pattern with an empty string
    clean_name = re.sub(pattern, '', game_name, flags=re.IGNORECASE)
    return clean_name.strip()

def load_game(game_name):
    filtered_game_name = clean_game_name(game_name)
    if os.path.exists("Q:\\scripts\\Cortana Server Browser\\games.txt"):
        with open("Q:\\scripts\\Cortana Server Browser\\games.txt", "r") as file:
            for line in file:
                line = line.strip()
                name, path = line[1:-1].split('", "')
                if name == filtered_game_name:
                    return path
    return None

def save_game(game_name, game_path):
    filtered_game_name = clean_game_name(game_name)
    with open("Q:\\scripts\\Cortana Server Browser\\games.txt", "a") as file:
        file.write('"{}", "{}"\n'.format(filtered_game_name, game_path))

def display_feed_items(dialog, channel):
    regular_items = ['...']
    excluded_titles = ["Users Online", "Users Today", "Server Status", "Supported Games", "Total Users", "Orbital Server", "Orbital Mesh", "Game Traffic", "Team XLink", "Game Event"]
    for item in channel.findall('item'):
        title_elem = item.find('title')
        if title_elem is not None:
            title = title_elem.text
            if not any(title.startswith(excluded) for excluded in excluded_titles):
                game_name = clean_game_name(title.split(' - ')[0])
                game_path = load_game(game_name)
                description = "Installed - " + game_path if game_path else "Not Installed"
                regular_items.append(title + " - " + description)

    selected_game = dialog.select("Cortana Server Browser - XLink Kai", regular_items)
    if selected_game == 0:
        xbmc.executebuiltin('RunScript(Q:\\scripts\\Cortana Server Browser\\XLink\\XLinkKai.py)')
    else:
        process_game_selection(dialog, regular_items, selected_game)

def process_game_selection(dialog, items, selected):
    if selected != -1:
        selected_item = items[selected].split(' - ')[0]
        game_path = load_game(selected_item)
        if not game_path:
            game_path = dialog.browse(1, "Select Game Path", 'files', '.xbe', False, False, '')
            if game_path:
                save_game(selected_item, game_path)
                launch = dialog.yesno("Launch Game", "Do you want to launch the game now?")
                if launch:
                    xbmc.executebuiltin('XBMC.RunXBE({})'.format(game_path))
                else:
                    xbmc.executebuiltin('RunScript(Q:\\scripts\\Cortana Server Browser\\xlink\\browser.py)')
            else:
                xbmcgui.Dialog().ok("Error", "No game path selected!")
        else:
            xbmc.executebuiltin('XBMC.RunXBE({})'.format(game_path))

def main():
    dialog = xbmcgui.Dialog()
    url = "https://ogxbox.org/rss/xlinkkai"  # Updated URL for XLink Kai
    root = fetch_and_parse_rss(url)
    if root is not None:
        channel = root.find('channel')
        if channel is not None:
            display_feed_items(dialog, channel)
        else:
            xbmc.log("No channel element found", xbmc.LOGERROR)
    else:
        xbmcgui.Dialog().ok("Error", "Failed to load server information!")

if __name__ == '__main__':
    main()
