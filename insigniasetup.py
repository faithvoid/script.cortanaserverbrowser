import xbmc
import xbmcgui
import urllib

download_url = "https://github.com/insignia-live/setup-assistant-release/releases/download/2025-01-19/default.xbe"
target_path = "Z:\\insignia.xbe"

def main():
    setup = xbmcgui.Dialog().yesno("Insignia", "Is your Xbox already registered for Insignia?")
    
    if not setup:
        download = xbmcgui.Dialog().yesno("Insignia", 
                                                   "Would you like to download and run the Insignia Setup Utility?")
        if not download:
            return
    
    try:
        urllib.urlretrieve(download_url, target_path)
    except Exception as e:
        xbmcgui.Dialog().ok("Insignia", "An error occurred: %s" % str(e))
        return
    
    try:
        xbmc.executebuiltin('XBMC.RunXBE(%s)' % target_path)
    except Exception as e:
        xbmcgui.Dialog().ok("Setup Failed", "Could not launch Insignia Setup Assistant: %s" % str(e))

if __name__ == "__main__":
    main()
