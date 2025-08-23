import os
import requests
import urllib3
import yt_dlp
from dotenv import load_dotenv
from http.cookies import SimpleCookie
import sys


# Get the directory where the executable is running
if getattr(sys, "frozen", False):
    application_path = os.path.dirname(sys.executable)
    # Running from a PyInstaller bundle
    BUNDLE_ROOT = sys._MEIPASS
    BIN_DIR = os.path.join(BUNDLE_ROOT, "bin")
else:
    application_path = os.path.dirname(os.path.abspath(__file__))
    # Running as a standard Python script (development)
    # You can set a specific bin directory here or rely on system PATH
    BUNDLE_ROOT = os.path.dirname(os.path.abspath(__file__))
    BIN_DIR = os.path.join(BUNDLE_ROOT, "bin")  # Or an empty string to rely on PATH

# Explicitly set the paths to the bundled executables
# If they don't exist in BIN_DIR (e.g., in dev env), fallback to just the command name
FFMPEG_PATH = os.path.join(BIN_DIR, "ffmpeg.exe").__str__() if os.path.exists(os.path.join(BIN_DIR, "ffmpeg.exe")) else "ffmpeg"
ARIA2C_PATH = os.path.join(BIN_DIR, "aria2c.exe").__str__() if os.path.exists(os.path.join(BIN_DIR, "aria2c.exe")) else "aria2c"
# Now tell load_dotenv() to look for the .env file in that specific directory
dotenv_path = os.path.join(application_path, ".env")


# Create default .env file before attempting to load it
def create_default_env(path):
    """
    Creates a .env file with default values if it does not exist.
    """
    if not os.path.exists(path):
        print("'.env' file not found. Creating a default file.")
        default_content = """# === Configuration ===
DEBUG=False # Enable for logging
DNS_RESOLVE=True # Resolve dns if ip fails
ARIA2C=False # Try aria2c for faster downloads
# SAVE_PATH=C:// # Download location
FINGERPRINT=web96b793f8dcb6bf3c20 # Fake Fingerprint
AUTHORIZATION_TOKEN=None # Authorization token
REFRESH_TOKEN=None # Refresh token
"""
        with open(path, "w") as f:
            f.write(default_content)


create_default_env(dotenv_path)
load_dotenv()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


# --- Configuration ---
VERSION = "1.0.0"
DEBUG = os.getenv("DEBUG", False).lower() in ("true")
DNS_RESOLVE = os.getenv("DNS_RESOLVE", True).lower() in ("true")
ARIA2C = os.getenv("ARIA2C", True).lower() in ("true")
SAVE_PATH = os.getenv("SAVE_PATH", os.path.join(os.path.expanduser("~"), "Desktop", "Belet"))
FINGERPRINT = os.getenv("FINGERPRINT", "web96b793f8dcb6bf3c20")
AUTHORIZATION_TOKEN = os.getenv("AUTHORIZATION_TOKEN", None)
REFRESH_TOKEN = os.getenv("REFRESH_TOKEN", None)

FILM_BELETAPIS = "film.beletapis.com"
FILM_BELET = "film.belet.tm"
API_BELET = "api.belet.tm"
VIDEOFILM_BELET = "videofilm.belet.me"
DOWNLOADFILM_BELET = "downloadfilm.belet.me"

MAIN_URLS = {
    FILM_BELET: [
        "119.235.120.106",
        "119.235.120.103",
        "119.235.120.105",
        "119.235.120.107",
        "119.235.120.100",
        "119.235.120.101",
    ],
    FILM_BELETAPIS: [
        "95.85.127.156",
        "119.235.120.118",
        "119.235.120.119",
        "119.235.120.123",
        "95.85.127.157",
    ],
    API_BELET: [
        "119.235.120.118",
        "95.85.127.156",
        "119.235.120.119",
        "119.235.120.123",
        "95.85.127.157",
    ],
    DOWNLOADFILM_BELET: [
        "119.235.120.106",
        "119.235.120.107",
        "119.235.120.100",
        "119.235.120.103",
        "119.235.120.105",
        "119.235.120.101",
    ],
}

BASE_HEADER = {
    "Accept": "application/json, text/plain, */*",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-GB,en;q=0.9,ru;q=0.8,en-US;q=0.7,tr;q=0.6",
    "Connection": "keep-alive",
    "DNT": "1",
    "sec-ch-ua-mobile": "?0",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "sec-ch-ua-platform": '"Windows"',
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
}

HEADERS = {
    **BASE_HEADER,
    **{
        "access-control-request-headers": "authorization,fingerprint",
        "access-control-request-method": "GET",
        "host": VIDEOFILM_BELET,
        "origin": f"https://{FILM_BELET}",
        "referer": f"https://{FILM_BELET}/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "cross-site",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "authorization": AUTHORIZATION_TOKEN,
    },
}


HEADERS_LOGIN = {
    **BASE_HEADER,
    **{
        "Content-Length": "21",
        "Content-Type": "application/json",
        "Host": API_BELET,
        "Lang": "ru",
        "Origin": f"https://{FILM_BELET}",
        "Referer": f"https://{FILM_BELET}/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "X-Platform": "Web",
    },
}

HEADERS_CHECK = {
    **BASE_HEADER,
    **{
        "Content-Length": "174",
        "Content-Type": "application/json",
        "Cookie": f"fingerprint={FINGERPRINT};",  # _ga=GA1.1.1541636591.1753466221; ph_phc_q0IYU1JS8LgRvdYL8vORaCjj8izJSvsydRqILHXqYSH_posthog=%7B%22distinct_id%22%3A%22345289%22%2C%22%24sesid%22%3A%5Bnull%2Cnull%2Cnull%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22u%22%3A%22https%3A%2F%2Ffilm.belet.tm%2Flogin%3FbackUrl%3D%252F%22%7D%7D; _ga_SE5MHC8KCY=GS2.1.s1755854145$o17$g1$t1755854213$j60$l0$h0",
        "Host": API_BELET,
        "Lang": "ru",
        "Origin": f"https://{FILM_BELET}",
        "Referer": f"https://{FILM_BELET}/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "X-Platform": "Web",
    },
}

HEADERS_TOKEN = {
    **BASE_HEADER,
    **{
        "Host": API_BELET,
        "Origin": f"https://{FILM_BELET}",
        "Referer": f"https://{FILM_BELET}/",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
        "X-Platform": "Web",
    },
}

HEADERS_SOURCE = {
    **BASE_HEADER,
    **{
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "authorization": AUTHORIZATION_TOKEN,
        "cache-control": "max-age=0",
        "Host": FILM_BELETAPIS,
        "fingerprint": FINGERPRINT,
        "priority": "u=0, i",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
    },
}


class Source:
    def __init__(self):
        self.videos = {}

    def addVideo(self, quality, url):
        self.videos[quality] = url

    def get_qualities(self):
        return list(self.videos.keys())

    def get_url_by_quality(self, quality):
        return self.videos.get(quality)


def welcomeMessage():
    """Prints a welcome banner and information about the downloader."""
    print("=======================================")
    print("       Belet Film Video Downloader       ")
    print("=======================================")
    print("🚀 This script downloads videos from film.belet.tm")
    print("It automatically handles video, audio, and subtitle streams.")
    print(f"Running on console version: {VERSION}")
    print("=======================================\n")


def updateEnv(key, value):
    """
    Updates or adds a key-value pair in a .env file.
    If the key exists, its value is updated. If not, the pair is added.
    """
    env_path = ".env"
    # Check if the .env file exists
    if not os.path.exists(env_path):
        with open(env_path, "w") as f:
            f.write(f"{key}={value}\n")
        return
    lines = []
    found = False
    with open(env_path, "r") as f:
        for line in f:
            if line.strip().startswith(f"{key}="):
                # Update the line if the key is found
                lines.append(f"{key}={value}\n")
                found = True
            else:
                lines.append(line)
    # If the key was not found, add it to the end
    if not found:
        lines.append(f"{key}={value}\n")
    # Write all the content back to the file
    with open(env_path, "w") as f:
        f.writelines(lines)
    debugPrint(f"Updated .env file: \n{key}: {value}")


def getUrl(host):
    if DNS_RESOLVE:
        return MAIN_URLS[host][0]
    return host


def check(token):
    global AUTHORIZATION_TOKEN
    global REFRESH_TOKEN
    url = f"https://{getUrl(API_BELET)}/api/v1/auth/check-code"
    headers = HEADERS_CHECK
    print("Enter 5 digit verification code")
    code = input("Code: ")
    payload = {"code": code, "token": token}
    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        AUTHORIZATION_TOKEN = response.json()["token"]
        updateEnv("AUTHORIZATION_TOKEN", AUTHORIZATION_TOKEN)
        set_cookie_headers = response.headers.get("Set-Cookie")
        if set_cookie_headers:
            # You might need to parse the string to extract specific cookies like RefreshToken
            # Libraries like 'http.cookies' can be helpful for more complex parsing
            cookies_parser = SimpleCookie()
            cookies_parser.load(set_cookie_headers)
            if "RefreshToken" in cookies_parser:
                refresh_token_cookie = cookies_parser["RefreshToken"]
                REFRESH_TOKEN = refresh_token_cookie.value
                updateEnv("REFRESH_TOKEN", REFRESH_TOKEN)
        else:
            debugPrint("No Set-Cookie header found in the response.")
        return AUTHORIZATION_TOKEN
    except requests.exceptions.RequestException as e:
        debugPrint(f"Error check code: {e}")
        print("Something went wrong trying again")
        check(token)
        return None


def login():
    url = f"https://{getUrl(API_BELET)}/api/v1/auth/sign-in?sign_in_type=1"
    headers = HEADERS_LOGIN
    print("Enter phone number to login")
    phone = input("Phone number: +993-")
    payload = {"phone": int("993" + phone)}
    try:
        response = requests.post(url, headers=headers, json=payload, verify=False)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return check(response.json()["token"])
    except requests.exceptions.RequestException as e:
        debugPrint(f"Error login: {e}")
        print("Something went wrong trying again")
        login()
        return None


def obtainNewToken():
    """Obtains a new authorization token from the API."""
    debugPrint("Obtaining new Token...")
    url = f"https://{getUrl(API_BELET)}/api/v1/auth/refresh"
    headers = HEADERS_TOKEN
    token = REFRESH_TOKEN if REFRESH_TOKEN else AUTHORIZATION_TOKEN
    headers["Cookie"] = f"RefreshToken={token}; fingerprint={FINGERPRINT};"  # _ga=GA1.1.1541636591.1753466221; ph_phc_q0IYU1JS8LgRvdYL8vORaCjj8izJSvsydRqILHXqYSH_posthog=%7B%22distinct_id%22%3A%22345289%22%2C%22%24sesid%22%3A%5Bnull%2Cnull%2Cnull%5D%2C%22%24epp%22%3Atrue%2C%22%24initial_person_info%22%3A%7B%22r%22%3A%22https%3A%2F%2Fwww.google.com%2F%22%2C%22u%22%3A%22https%3A%2F%2Ffilm.belet.tm%2Flogin%3FbackUrl%3D%252F%22%7D%7D; _ga_SE5MHC8KCY=GS2.1.s1755777900$o13$g0$t1755777900$j60$l0$h0"
    try:
        response = requests.post(url, headers=headers, verify=False)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        token = response.json()["token"]
        updateEnv("AUTHORIZATION_TOKEN", token)
        return token
    except requests.exceptions.RequestException as e:
        debugPrint(f"Error obtaining token: {e}")
        login()
        return None


# Updated `download` function
def download(
    url,
    output_file,
    save_path=SAVE_PATH,
):
    print("\nDownload started...")

    def progress_hook(d):
        if d["status"] == "downloading":
            downloaded = d["_downloaded_bytes_str"]
            print(f"Downloaded: {downloaded}", end="\r")
        elif d["status"] == "finished":
            print("\n")
            print("Download finished.")

    ydl_opts = {
        # This format string is designed to work with yt-dlp's merging logic
        "format": "bestvideo+mergeall[vcodec=none]",
        "allow_multiple_audio_streams": True,  # This flag is crucial for downloading all audio tracks
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(save_path, output_file),
        "quiet": not DEBUG,
        "writedescription": False,
        "writethumbnail": False,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["all"],
        "no_check_certificate": True,
        "postprocessors": [
            {
                "key": "FFmpegEmbedSubtitle",
            },
        ],
        "progress_hooks": [progress_hook] if DEBUG else [],
        "http_headers": HEADERS,
        "ffmpeg_location": FFMPEG_PATH,
    }
    if ARIA2C:
        ydl_opts.update(
            {
                "external_downloader": ARIA2C_PATH,
                "external_downloader_args": [
                    "-x",
                    "16",
                    "-s",
                    "16",
                    "-k",
                    "1M",
                    "--check-certificate=false",
                ],
            }
        )

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("\n🎉 Download successful!")
        print(f"File saved to: {os.path.join(save_path, output_file)}")

    except yt_dlp.utils.DownloadError as e:
        print(f"\n❌ Error during download: {e}")
        print("This often means the URL is invalid or the token has expired.")
    except Exception as e:
        print(f"\n❌ An unexpected error occurred: {e}")


def getSources(video, typ=1):
    url = f"https://{getUrl(FILM_BELETAPIS)}/api/v3/files/{video}?type={typ}"
    headers = HEADERS_SOURCE
    headers["authorization"] = AUTHORIZATION_TOKEN
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        data = response.json()
        video_sources = Source()
        for video_info in data.get("sources", []):
            quality = video_info.get("quality")
            filename = video_info.get("filename")
            if quality and filename:
                video_sources.addVideo(quality, filename)
                debugPrint(f"Found source: {quality} at {filename}")
        return video_sources
    else:
        debugPrint(f"ERROR: Get Source Response Fail. Status code: {response.status_code}")
        debugPrint(f"Raw response: {response.text}")
        obtainNewToken()
        return None


def initDir():
    if not os.path.exists(SAVE_PATH):
        debugPrint(f"Creating download directory: {SAVE_PATH}")
        os.makedirs(SAVE_PATH)
    else:
        debugPrint(f"Download directory already exists: {SAVE_PATH}")


def debugPrint(s):
    if DEBUG:
        print(s)


# Updated `inputQuality` function
def inputQuality(source):
    qualities = list(source.videos.keys())
    if not qualities:
        print("No qualities available for this video.")
        return None, None  # Return both URL and quality string
    print("\nAvailable qualities:")
    for i, quality in enumerate(qualities):
        print(f"{i}: {quality}")
    try:
        inp = input("Enter quality index. Leave empty if 480p: ").strip()
        index = int(inp) if inp != "" else 0
        if 0 <= index < len(qualities):
            selected_quality = qualities[index]
            url = source.videos[selected_quality]
            # Return both the URL and the selected quality string
            return url, selected_quality
        else:
            print("Invalid index. Please enter a number from the list.")
            return inputQuality(source)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return inputQuality(source)
    except Exception as e:
        debugPrint(f"ERROR in inputQuality: {e}")
        return None, None


def main():
    global AUTHORIZATION_TOKEN
    if not FINGERPRINT:
        print("Set FINGERPRINT in .env. Aborting")
        return
    if not REFRESH_TOKEN:
        debugPrint("REFRESH_TOKEN: " + REFRESH_TOKEN)
        login()
    if not AUTHORIZATION_TOKEN:
        debugPrint("AUTHORIZATION_TOKEN: " + AUTHORIZATION_TOKEN)
        AUTHORIZATION_TOKEN = obtainNewToken()
    video = input("Enter video number: ")
    source = getSources(video)
    if source and source.videos:
        # Get both the url and the quality string from the function
        url, quality_string = inputQuality(source)
        if url and quality_string:
            debugPrint(f"Selected URL: {url}")
            dynamic_output_file = f"{video}_{quality_string}.mp4"
            download(
                url=url,
                save_path=os.path.join(SAVE_PATH, f"{video}_{quality_string}"),
                output_file=dynamic_output_file,
            )
        else:
            print("No URL selected. Exiting.")
    else:
        debugPrint("Failed to retrieve sources or no sources available.")
    main()


# The main execution block also needs a small change
if __name__ == "__main__":
    welcomeMessage()
    initDir()
    main()
