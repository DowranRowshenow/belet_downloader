import os
import sys
import yt_dlp
import requests
import urllib3
from dotenv import load_dotenv
from http.cookies import SimpleCookie


# Define a dictionary of default values to check against
DEFAULT_CONFIG = {
    "DEBUG": "False",
    "DNS_RESOLVE": "False",
    "CHECK_CERTIFICATE": "True",
    "ARIA2C": "False",
    "SAVE_PATH": "None",
    "FINGERPRINT": "web84b041g6ekl5ce4a19",
    "AUTHORIZATION_TOKEN": "None",
    "REFRESH_TOKEN": "None",
}


def debugPrint(debugMessage, message=None):
    try:
        debug_mode = DEBUG
    except NameError:
        debug_mode = False

    if debug_mode:
        print(debugMessage)
    elif message:
        print(message)


def updateEnv(key, value):
    """
    Updates or adds a key-value pair in a .env file.
    If the key exists, its value is updated. If not, the pair is added.
    """
    # Check if the .env file exists
    if not os.path.exists(DOTENV_PATH):
        with open(DOTENV_PATH, "w") as f:
            f.write(f"{key}={value}\n")
        return
    lines = []
    found = False
    with open(DOTENV_PATH, "r") as f:
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
    with open(DOTENV_PATH, "w") as f:
        f.writelines(lines)
    debugPrint(f"Updated .env file: \n{key}: {value}")


# Create default .env file before attempting to load it
def create_default_env():
    global ENV, DOTENV_PATH, BIN_DIR
    # Get the directory where the executable is running
    if getattr(sys, "frozen", False):
        # Running from a PyInstaller bundle
        application_path = os.path.dirname(sys.executable)
        BIN_DIR = os.path.join(sys._MEIPASS, "bin")
        ENV = "PyInstaller"
        DOTENV_PATH = os.path.join(application_path, ".env")
    elif "__compiled__" in globals():
        # Running from a Nuitka bundle
        application_path = os.path.dirname(os.path.abspath(__file__))
        BIN_DIR = os.path.join(application_path, "bin")
        ENV = "Nuitka"
        DOTENV_PATH = os.path.join(os.path.dirname(sys.executable), ".env")
    else:
        # Running as a standard Python script (development)
        application_path = os.path.dirname(os.path.abspath(__file__))
        BIN_DIR = os.path.join(application_path, "bin")
        ENV = "Script"
        DOTENV_PATH = os.path.join(application_path, ".env")

    # Check if the .env file exists; if not, create it with all defaults
    if not os.path.exists(DOTENV_PATH):
        print("Configuration file not found. Creating a default file.")
        with open(DOTENV_PATH, "w") as f:
            f.write("# === Configuration ===\n")
            for key, value in DEFAULT_CONFIG.items():
                f.write(f"{key}={value}\n")
        load_dotenv(dotenv_path=DOTENV_PATH)
    else:
        # If the file exists, load it and check for missing keys
        load_dotenv(dotenv_path=DOTENV_PATH)
        for key, value in DEFAULT_CONFIG.items():
            # If the key is not in the environment variables, add it to the file
            if os.getenv(key) is None:
                updateEnv(key, value)
                print(f"Added missing configuration key: {key}")


def getDotEnv(key):
    return os.getenv(key, DEFAULT_CONFIG[key])


create_default_env()
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
# --- Configuration ---
FFMPEG_PATH = os.path.join(BIN_DIR, "ffmpeg.exe").__str__() if os.path.exists(os.path.join(BIN_DIR, "ffmpeg.exe")) else "ffmpeg"
ARIA2C_PATH = os.path.join(BIN_DIR, "aria2c.exe").__str__() if os.path.exists(os.path.join(BIN_DIR, "aria2c.exe")) else "aria2c"
VERSION = "1.0.1"
DEBUG = getDotEnv("DEBUG").lower() in ("true")
DNS_RESOLVE = getDotEnv("DNS_RESOLVE").lower() in ("true")
CHECK_CERTIFICATE = False if DNS_RESOLVE else getDotEnv("CHECK_CERTIFICATE").lower() in ("true")
ARIA2C = getDotEnv("ARIA2C").lower() in ("true")
SAVE_PATH = getDotEnv("SAVE_PATH")
SAVE_PATH = os.path.join(os.path.expanduser("~"), "Desktop", "Belet") if SAVE_PATH.lower() == "none" else SAVE_PATH
FINGERPRINT = getDotEnv("FINGERPRINT")
AUTHORIZATION_TOKEN = getDotEnv("AUTHORIZATION_TOKEN")
REFRESH_TOKEN = getDotEnv("REFRESH_TOKEN")

FILM_BELETAPIS = "film.beletapis.com"
FILM_BELET = "film.belet.tm"
API_BELET = "api.belet.tm"
VIDEOFILM_BELET = "videofilm.belet.me"
DOWNLOADFILM_BELET = "downloadfilm.belet.me"

MAIN_URLS = {
    FILM_BELET: ["119.235.120.106", "119.235.120.103", "119.235.120.105", "119.235.120.107", "119.235.120.100", "119.235.120.101"],
    FILM_BELETAPIS: ["95.85.127.156", "119.235.120.118", "119.235.120.119", "119.235.120.123", "95.85.127.157"],
    API_BELET: ["119.235.120.118", "95.85.127.156", "119.235.120.119", "119.235.120.123", "95.85.127.157"],
    DOWNLOADFILM_BELET: ["119.235.120.106", "119.235.120.107", "119.235.120.100", "119.235.120.103", "119.235.120.105", "119.235.120.101"],
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
        "Cookie": f"fingerprint={FINGERPRINT};",
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


class Episode:

    def __init__(self, last_watch, sources, id, type_id, parent_id, name, duration, image):
        self.last_watch = last_watch
        self.sources = sources
        self.id = id
        self.type_id = type_id
        self.parent_id = parent_id
        self.name = name
        self.duration = duration
        self.image = image

    @classmethod
    def fromMap(cls, episode_map, sources_list):
        return cls(
            last_watch=episode_map.get("last_watch"),
            sources=sources_list,
            id=episode_map.get("id"),
            type_id=episode_map.get("type_id"),
            parent_id=episode_map.get("parent_id"),
            name=episode_map.get("name"),
            duration=episode_map.get("duration"),
            image=episode_map.get("image"),
        )


class Source:

    def __init__(self, filename, download_url, type, quality):
        self.filename = filename
        self.download_url = download_url
        self.type = type
        self.quality = quality

    @classmethod
    def fromMap(cls, source_map):
        return cls(
            filename=source_map.get("filename"),
            download_url=source_map.get("download_url"),
            type=source_map.get("type"),
            quality=source_map.get("quality"),
        )


def resolveHost(host):
    return MAIN_URLS[host][0] if DNS_RESOLVE else host


def resolveUrl(url):
    return url
    """
    This lines are deprecated for now
    host = urlparse(url).netloc
    return url.replace(host, resolveHost(host))
    """


def login():
    url = f"https://{resolveHost(API_BELET)}/api/v1/auth/sign-in?sign_in_type=1"
    headers = HEADERS_LOGIN
    print("Enter phone number to login")
    phone = input("Phone number: +993-")
    payload = {"phone": int("993" + phone)}
    try:
        response = requests.post(url, headers=headers, json=payload, verify=CHECK_CERTIFICATE)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return check(response.json()["token"])
    except requests.exceptions.RequestException as e:
        debugPrint(f"Error login: {e}", "Something went wrong trying again")
        login()
        return None


def check(token):
    global AUTHORIZATION_TOKEN, REFRESH_TOKEN
    url = f"https://{resolveHost(API_BELET)}/api/v1/auth/check-code"
    headers = HEADERS_CHECK
    print("Enter 5 digit verification code")
    code = input("Code: ")
    payload = {"code": code, "token": token}
    try:
        response = requests.post(url, headers=headers, json=payload, verify=CHECK_CERTIFICATE)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        AUTHORIZATION_TOKEN = response.json()["token"]
        updateEnv("AUTHORIZATION_TOKEN", AUTHORIZATION_TOKEN)
        set_cookie_headers = response.headers.get("Set-Cookie")
        if set_cookie_headers:
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
        debugPrint(f"Error check code: {e}", "Something went wrong trying again")
        check(token)
        return None


def refreshToken():
    """Obtains a new authorization token from the API."""
    debugPrint("Obtaining new Token...")
    url = f"https://{resolveHost(API_BELET)}/api/v1/auth/refresh"
    headers = HEADERS_TOKEN
    token = REFRESH_TOKEN if REFRESH_TOKEN or str(REFRESH_TOKEN).lower() != "none" else AUTHORIZATION_TOKEN
    headers["Cookie"] = f"RefreshToken={token}; fingerprint={FINGERPRINT};"
    try:
        response = requests.post(url, headers=headers, verify=CHECK_CERTIFICATE)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        token = response.json()["token"]
        updateEnv("AUTHORIZATION_TOKEN", token)
        return token
    except requests.exceptions.RequestException as e:
        debugPrint(f"Error obtaining token: {e}")
        login()
        return None


def welcomeMessage():
    """Prints a welcome banner and information about the downloader."""
    print("=======================================")
    print("       Belet Film Video Downloader       ")
    print("=======================================")
    print("🚀 This script downloads videos from film.belet.tm")
    print("It automatically handles video, audio, and subtitle streams.")
    print(f"Running on console version: {VERSION}")
    print("=======================================")


def initDir():
    debugPrint(f"Running on {ENV}")
    debugPrint(f"BIN_DIR: {BIN_DIR}")
    debugPrint(f"EXE_DIR: {os.path.dirname(sys.executable)}")
    debugPrint(f"FFMPEG: {FFMPEG_PATH}")
    debugPrint(f"ARIA2C: {ARIA2C_PATH}")
    debugPrint(f"DOTENV: {DOTENV_PATH}")
    if not os.path.exists(SAVE_PATH):
        debugPrint(f"Creating download directory: {SAVE_PATH}")
        os.makedirs(SAVE_PATH)
    else:
        debugPrint(f"Download directory already exists: {SAVE_PATH}")


def initCredentials():
    global AUTHORIZATION_TOKEN
    if not FINGERPRINT:
        print("Set FINGERPRINT in .env file. Aborting")
        return
    if not REFRESH_TOKEN or str(REFRESH_TOKEN).lower() == "none":
        debugPrint("REFRESH_TOKEN: " + str(REFRESH_TOKEN))
        login()
    if not AUTHORIZATION_TOKEN or str(AUTHORIZATION_TOKEN).lower() == "none":
        debugPrint("AUTHORIZATION_TOKEN: " + AUTHORIZATION_TOKEN)
        AUTHORIZATION_TOKEN = refreshToken()


def download(url, output_file, save_path=SAVE_PATH, main=True):
    print("Download started...")

    def progress_hook(d):
        if d["status"] == "downloading":
            downloaded = d["_downloaded_bytes_str"]
            print(f"Downloaded: {downloaded}", end="\r")
        elif d["status"] == "finished":
            print("\nDownload finished.")

    headers = HEADERS
    headers["authorization"] = AUTHORIZATION_TOKEN

    ydl_opts = {
        "allow_multiple_audio_streams": True,
        "merge_output_format": "mp4",
        "outtmpl": os.path.join(save_path, output_file),
        "quiet": not DEBUG,
        "writedescription": False,
        "writethumbnail": False,
        "writesubtitles": True,
        "writeautomaticsub": True,
        "subtitleslangs": ["all"],
        "fragment_retries": 10**10,
        "retries": 10**10,
        "socket_timeout": 60 * 60 * 24,
        "no_check_certificate": CHECK_CERTIFICATE,
        "postprocessors": [{"key": "FFmpegEmbedSubtitle"}],
        "progress_hooks": [progress_hook] if DEBUG else [],
        "http_headers": headers,
        "ffmpeg_location": FFMPEG_PATH,
    }
    if main:
        ydl_opts.update({"format": "bestvideo+mergeall[vcodec=none]"})
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
                    "--timeout=300",
                    f"--check-certificate={CHECK_CERTIFICATE.__str__().lower()}",
                ],
            }
        )
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([resolveUrl(url)])
        print("\n🎉 Download successful!")
        print(f"File saved to: {os.path.join(save_path, output_file)}")
    except yt_dlp.utils.DownloadError as e:
        debugPrint(f"\n❌ Error during download: {e}")
        if "Requested format is not available" in str(e):
            debugPrint("Trying with main=False")
            download(url, output_file, save_path=save_path, main=False)
    except Exception as e:
        debugPrint(f"\n❌ An unexpected error occurred: {e}", "\n❌ An unexpected error occurred cannot download")


def getSources(videoId, typ=1):
    url = f"https://{resolveHost(FILM_BELETAPIS)}/api/v3/files/{videoId}?type={typ}"
    headers = HEADERS_SOURCE
    headers["authorization"] = AUTHORIZATION_TOKEN
    response = requests.get(url, headers=headers, verify=CHECK_CERTIFICATE)
    if response.status_code == 200:
        data = response.json()
        sources = []
        for source in data["sources"]:
            print(source)
            sources.append(Source.fromMap(source))
        return sources
    else:
        debugPrint(f"ERROR: Get Source Response Fail. Status code: {response.status_code}")
        debugPrint(f"Raw response: {response.text}")
        refreshToken()
        return None


def getEpisodes(season_id):
    url = f"https://{resolveHost(FILM_BELETAPIS)}/api/v2/episodes?seasonId={season_id}"
    headers = HEADERS_SOURCE
    headers["authorization"] = AUTHORIZATION_TOKEN
    try:
        response = requests.get(url, headers=headers, verify=CHECK_CERTIFICATE)
        if response.status_code == 200:
            data = response.json()
            episodes = []
            for episode in data["episodes"]:
                sources = []
                for source in episode["sources"]:
                    sources.append(Source.fromMap(source))
                episodes.append(Episode.fromMap(episode, sources))
            return episodes
        else:
            debugPrint(f"ERROR: Get Season Response Fail. Status code: {response.status_code}")
            debugPrint(f"Raw response: {response.text}")
            refreshToken()
    except Exception as e:
        debugPrint(f"Error: {e}")
    return None


def inputOption():
    print("Enter download option")
    print("0: Episode")
    print("1: Season")
    option = input("Option: ")
    if option == "1":
        return 1
    return 0


def inputQuality(sources):
    qualities = []
    for source in sources:
        qualities.append(source.quality)
    if not qualities:
        print("No qualities available for this video.")
        return None
    print("\nAvailable qualities:")
    for i, quality in enumerate(qualities):
        print(f"{i}: {quality}")
    try:
        inp = input(f"Enter quality index. Leave empty if {qualities[0]}: ").strip()
        index = int(inp) if inp != "" else 0
        if 0 <= index < len(qualities):
            return qualities[index]
        else:
            print("Invalid index. Please enter a number from the list.")
            return inputQuality(sources)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return inputQuality(sources)
    except Exception as e:
        debugPrint(f"ERROR in inputQuality: {e}")
        return None


def getUrlFromSources(quality, sources):
    for source in sources:
        if quality == source.quality:
            debugPrint(f"Found desired quality: {quality}")
            return source.filename
    if len(sources) > 0:
        debugPrint(f"Desired quality not found using: {sources[0].quality}")
        return sources[0].filename
    debugPrint("Not source found")
    return None


def main():
    if inputOption() == 1:
        seasonId = input("Enter season number: ")
        episodes = getEpisodes(seasonId)
        if episodes:
            quality = inputQuality(episodes[0].sources)
            for episode in episodes:
                try:
                    download(
                        url=getUrlFromSources(quality, episode.sources),
                        save_path=os.path.join(SAVE_PATH, "Seasons", f"{seasonId}"),
                        output_file=f"{episode.name}_{quality}.mp4",
                    )
                except Exception as e:
                    debugPrint(f"Error downloading {episode.name}.\n{e}", f"Something went wrong while downloading {episode.name}. Skipping")
        else:
            print("Something went wrong! Episodes not found.")
    else:
        videoId = input("Enter video number: ")
        sources = getSources(videoId)
        if sources:
            quality = inputQuality(sources)
            try:
                download(
                    url=getUrlFromSources(quality, sources),
                    save_path=os.path.join(SAVE_PATH, "Videos", f"{videoId}"),
                    output_file=f"{videoId}_{quality}.mp4",
                )
            except Exception as e:
                debugPrint(f"Error downloading {videoId}\n{e}", f"Something went wrong while downloading {videoId}. Skipping")
        else:
            debugPrint("Failed to retrieve sources or no sources available.")
    main()


# The main execution block also needs a small change
if __name__ == "__main__":
    welcomeMessage()
    initDir()
    initCredentials()
    main()
