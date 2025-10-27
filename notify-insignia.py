import xbmc
import xbmcgui
import time
import urllib2
import xml.etree.ElementTree as ET
import re
from collections import deque
import os

NOTIFY_FILE="Z:\\temp\\insignia.txt"

game_event_queue = deque()
regular_notification_queue = deque()

def clear_notifications_file():
    open(NOTIFY_FILE, "w").close()

def load_notifications():
    if os.path.exists(NOTIFY_FILE):
        with open(NOTIFY_FILE, "r") as f:
            return set(f.read().strip().split("\n"))
    return set()

def save_notifications(notifications):
    with open(NOTIFY_FILE, "w") as f:
        for notification in notifications:
            f.write("%s\n" % notification)

def clean_title(title):
    if not title:
        return ""
    
    title = re.sub(r'\s+', ' ', title.strip())
    
    title = title.replace("&amp;", "&")
    
    return title

def extract_game_id(link):
    if link:
        match = re.search(r'/games/(\w+)', link)
        if match:
            return match.group(1)
    return None

def get_game_thumbnail(game_id):
    if game_id and len(game_id) >= 4:
        game_id_upper = game_id.upper()
        folder = game_id_upper[:4]
        return "https://raw.githubusercontent.com/MobCat/MobCats-original-xbox-game-list/main/icon/{0}/{1}.png".format(folder, game_id_upper)
    return ""

def check_rss_only_once():
    current_notifications = load_notifications()
    new_notifications = set()
    try:
        url = 'http://ogxbox.org/rss/insignia.xml'
        req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib2.urlopen(req)
        data = response.read()
        root = ET.fromstring(data)

        for item in root.findall('.//item'):
            title_element = item.find('title')
            link_element = item.find('link')
            if title_element is None:
                continue

            title = title_element.text
            link = link_element.text if link_element is not None else None

            if title.startswith("Game Event - Today") or title.startswith("Game Event - Tomorrow"):
                clean_title_text = re.sub(r'^Game Event - ', '', title)
                clean_title_text = clean_title(clean_title_text)
                if clean_title_text not in current_notifications:
                    game_id = extract_game_id(link)
                    thumb_url = get_game_thumbnail(game_id)
                    game_event_queue.append(("Insignia - Event", clean_title_text, thumb_url))
                    new_notifications.add(clean_title_text)

        save_notifications(new_notifications)
    except Exception as e:
        error_msg = "RSS Error: " + str(e)
        regular_notification_queue.append(("RSS Feed Error", error_msg, ""))
        new_notifications.add(error_msg)

def check_rss_regular():
    current_notifications = load_notifications()
    new_notifications = set()
    try:
        url = 'http://ogxbox.org/rss/insignia.xml'
        req = urllib2.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        response = urllib2.urlopen(req)
        data = response.read()
        root = ET.fromstring(data)

        for item in root.findall('.//item'):
            title_element = item.find('title')
            link_element = item.find('link')
            if title_element is None:
                continue

            title = title_element.text
            link = link_element.text if link_element is not None else None

            if "(0 in 0 sessions)" in title:
                continue

            match = re.search(r'(\d+) players?', title)
            if match:
                players = int(match.group(1))
                if players > 0:
                    clean_title_text = clean_title(title)
                    new_notifications.add(clean_title_text)
                    if clean_title_text not in current_notifications:
                        game_id = extract_game_id(link)
                        thumb_url = get_game_thumbnail(game_id)
                        regular_notification_queue.append(("Insignia", clean_title_text, thumb_url))

        save_notifications(new_notifications)
    except Exception as e:
        error_msg = "RSS Error: " + str(e)
        regular_notification_queue.append(("RSS Feed Error", error_msg, ""))
        new_notifications.add(error_msg)

def process_notifications():
    while game_event_queue:
        header, message, thumb = game_event_queue.popleft()
        display_notification(header, message, thumb)

    while regular_notification_queue:
        header, message, thumb = regular_notification_queue.popleft()
        display_notification(header, message, thumb)

def display_notification(header, message, thumbnail):
    duration = 5000  # milliseconds
    if thumbnail:
        xbmc.executebuiltin('Notification("{}", "{}", {}, "{}")'.format(
            header, message, duration, thumbnail))
    else:
        xbmc.executebuiltin('Notification("{}", "{}", {})'.format(header, message, duration))
    
    time.sleep(duration / 1000.0)

clear_notifications_file()
check_rss_only_once()
process_notifications()

while True:
    check_rss_regular()
    process_notifications()
    time.sleep(60)
