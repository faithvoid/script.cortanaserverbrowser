import os
import xbmcgui
import zipfile
import requests

def download_file(url, dest):
    try:
        response = requests.get(url, stream=True, verify=False)
        response.raise_for_status()

        with open(dest, 'wb') as f:
            dialog = xbmcgui.DialogProgress()
            dialog.create('Download Progress', 'Downloading update...')
            file_size = int(response.headers.get('content-length', 0))
            file_size_dl = 0
            block_sz = 8192

            for buffer in response.iter_content(block_sz):
                if not buffer:
                    break

                file_size_dl += len(buffer)
                f.write(buffer)
                percent = file_size_dl * 100. / file_size
                dialog.update(int(percent))

                if dialog.iscanceled():
                    f.close()
                    dialog.close()
                    os.remove(dest)
                    return False

            dialog.close()
            return True
    except Exception as e:
        dialog = xbmcgui.Dialog()
        dialog.ok('Cortana Updater - Error', 'Failed to download file: ' + str(e))
        return False

def check_version(remote_version_url, local_version_path):
    try:
        response = requests.get(remote_version_url, verify=False)
        response.raise_for_status()
        remote_version = response.text.strip()
        response.close()

        if os.path.exists(local_version_path):
            with open(local_version_path, 'r') as f:
                local_version = f.read().strip()
                return float(remote_version) > float(local_version)
        else:
            return True
    except Exception as e:
        dialog = xbmcgui.Dialog()
        dialog.ok('Cortana Updater - Error', 'Failed to check version: ' + str(e))
        return False

def extract_zip(zip_file, extract_path):
    try:
        with zipfile.ZipFile(zip_file, 'r') as zip_ref:
            zip_ref.extractall(extract_path)
        return True
    except Exception as e:
        dialog = xbmcgui.Dialog()
        dialog.ok('Cortana Updater - Error', 'Failed to extract ZIP file: ' + str(e))
        return False

# Example use
def main():
    remote_version_url = 'https://github.com/faithvoid/script.cortanaserverbrowser/raw/refs/heads/main/release/version.txt'
    local_version_path = 'Q:\\scripts\\Cortana Server Browser\\version.txt'
    url = 'https://github.com/faithvoid/script.cortanaserverbrowser/raw/refs/heads/main/release/update.zip'
    destination_path = 'Q:\\scripts\\Cortana Server Browser\\update.zip'
    extract_path = 'Q:\\scripts\\Cortana Server Browser'

    if not os.path.exists(extract_path):
        os.makedirs(extract_path)

    if check_version(remote_version_url, local_version_path):
        print("New version available. Downloading...")
        if download_file(url, destination_path):
            print("Download successful")
            if extract_zip(destination_path, extract_path):
                print("Extraction successful")
            else:
                print("Extraction failed")
        else:
            print("Download failed")
    else:
        dialog = xbmcgui.Dialog()
        dialog.ok('Cortana Updater - Error', 'You already have the latest version.')

if __name__ == '__main__':
    main()
