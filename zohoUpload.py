import requests
import os
import time
import zipfile
from pathlib import Path

# 🔐 REQUIRED TOKENS
CLIENT_ID = "1000.2LTPU2XUA2PHYU47JMTUQUKA4PJD8I"
CLIENT_SECRET = "aaf42acb022c1009f2b1f45a54fe595646d01a6c8f"
REFRESH_TOKEN = "1000.0c3a68c31e498bb3439a7fc8de0b4d69.1253f9f99948797dd319ec364f3590f6"

# 📁 Your target WorkDrive folder (inside a Team Folder)
PARENT_FOLDER_ID = "c4osde78db44bfe9d4f4d878b95db3317cf7e"
# ⏳ Store token in memory
access_token_data = {
    "token": None,
    "expires_at": 0
}


def get_access_token():
    if time.time() < access_token_data["expires_at"]:
        return access_token_data["token"]

    print("🔄 Refreshing access token...")
    url = "https://accounts.zoho.com/oauth/v2/token"
    payload = {
        "refresh_token": REFRESH_TOKEN,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "refresh_token"
    }

    response = requests.post(url, data=payload)
    if response.status_code != 200:
        raise Exception(f"❌ Failed to refresh access token: {response.text}")

    data = response.json()
    access_token_data["token"] = data["access_token"]
    access_token_data["expires_at"] = time.time() + int(data["expires_in"]) - 60
    print("✅ Access token refreshed.")
    return access_token_data["token"]


def zip_folder(folder_path):
    """Zips the contents of a folder and returns the path to the zip file."""
    folder = Path(folder_path)
    if not folder.is_dir():
        raise NotADirectoryError(f"❌ Not a directory: {folder_path}")

    zip_path = folder.with_suffix('.zip')

    print(f"🗜️ Zipping folder '{folder_path}' to '{zip_path}'...")
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, start=folder_path)
                zipf.write(file_path, arcname)

    print("✅ Folder zipped.")
    return zip_path


def upload_file_to_workdrive(folder_path):
    """Zips the given folder and uploads it to Zoho WorkDrive."""
    # First zip the folder
    zipped_file_path = zip_folder(folder_path)

    if not os.path.isfile(zipped_file_path):
        raise FileNotFoundError(f"❌ Zipped file not found: {zipped_file_path}")

    access_token = get_access_token()
    upload_url = "https://www.zohoapis.com/workdrive/api/v1/upload"
    headers = {
        "Authorization": f"Zoho-oauthtoken {access_token}"
    }

    files = {
        "content": open(zipped_file_path, "rb")
    }

    data = {
        "parent_id": PARENT_FOLDER_ID
    }

    print(f"📤 Uploading '{zipped_file_path}' to WorkDrive...")
    response = requests.post(upload_url, headers=headers, files=files, data=data)

    if response.status_code == 201 or response.status_code == 200:
        print("✅ File uploaded successfully.")
        print("📄 Response:", response.json())
    else:
        print("❌ Upload failed!")
        print("🔴 Status:", response.status_code)
        print("🪵 Response:", response.text)


# ✅ Call like this:
