import xbmc
import xbmcgui
import os

# Define script paths
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
INSIGNIA = os.path.join(SCRIPT_DIR, "insignia.py")
XLINKKAI = os.path.join(SCRIPT_DIR, "xlinkkai.py")
INSTALLGAME = os.path.join(SCRIPT_DIR, "installgames.py")
NOTIFY_INSIGNIA = os.path.join(SCRIPT_DIR, "notify-insignia.py")
NOTIFY_XLINKKAI = os.path.join(SCRIPT_DIR, "notify-xlink.py")

# Show a dialog with main options
dialog = xbmcgui.Dialog()
choice = dialog.select("Select an option", ["Insignia", "XLink Kai", "Install Game(s)"])

# Execute the selected script
if choice == 0:
    xbmc.executebuiltin('RunScript("{}")'.format(INSIGNIA))
elif choice == 1:
    xbmc.executebuiltin('RunScript("{}")'.format(XLINKKAI))
elif choice == 2:
    xbmc.executebuiltin('RunScript("{}")'.format(INSTALLGAME))