pyinstaller downloader.py --onefile --name "BeletDownloader" --add-binary "bin/aria2c.exe;bin" --add-binary "bin/ffmpeg.exe;bin"

https://www.gyan.dev/ffmpeg/builds/
https://www.gyan.dev/ffmpeg/builds/packages/ffmpeg-2025-08-20-git-4d7c609be3-essentials_build.7z

https://github.com/aria2/aria2/releases/

# Belet.tm Video Downloader

A robust Python script to download videos from the Belet.tm streaming platform. It automates the authentication process and handles the complex task of downloading multi-stream content (all available video, audio, and subtitle tracks) into a single file.

This tool is designed to provide a seamless downloading experience, ensuring you get the highest quality content with all language tracks included.

---

## 🚀 Key Features

* **Automated Authentication**: Handles login and token refreshing with an easy-to-use `.env` file configuration.

* **Multi-Stream Download**: Automatically detects and downloads **all available audio and subtitle streams** along with the best quality video, merging them into a single `.mp4` file.

* **Quality Selection**: Allows you to choose your preferred video quality (e.g., 480p, 1080p) from available options.

* **Fast & Efficient**: Leverages `yt-dlp` and `aria2c` to maximize download speed and manage multiple connections.

* **User-Friendly Progress**: Displays a clean, single-line progress bar showing downloaded data.

* **Customizable Settings**: All key configurations are managed via a simple `.env` file, including debug mode and save path.

* **Single Executable**: Can be bundled into a single `.exe` file for easy distribution without requiring Python to be installed (requires separate FFmpeg and aria2c executables to be bundled).

---

## ⚙️ How to Use

### Prerequisites

You need to have `FFmpeg` and `aria2c` installed on your system. These are external tools that `yt-dlp` uses for merging streams and accelerating downloads. Make sure they are in your system's PATH.

### Installation

1.  **Clone the Repository**:

    ```
    git clone [https://github.com/your-username/your-repo.git](https://github.com/your-username/your-repo.git)
    cd your-repo


    ```

2.  **Install Python Dependencies**:

    ```
    pip install -r requirements.txt


    ```

    *(Create a `requirements.txt` file by running `pip freeze > requirements.txt`)*

3.  **Create `.env` File**:
    The script will automatically create a `.env` file with default values if it doesn't exist when you run it for the first time. You should edit this file to configure your settings.

    ```
    # === Configuration ===
    DEBUG=False
    DNS_RESOLVE=True
    ARIA2C=True
    SAVE_PATH="/path/to/your/download/folder" # e.g., C:\Users\YourUser\Desktop\Belet
    FINGERPRINT= # Your Belet.tm fingerprint (leave empty to prompt for login)
    AUTHORIZATION_TOKEN= # Automatically updated after login
    REFRESH_TOKEN= # Automatically updated after login


    ```

    * **`FINGERPRINT`**: This is a unique identifier for your device. If left empty, the script will prompt you to log in via phone number to obtain one.

    * **`SAVE_PATH`**: The directory where downloaded videos will be saved.

    * **`DEBUG`**: Set to `True` for verbose output and to enable the download progress hook.

    * **`DNS_RESOLVE`**: Set to `True` to use the pre-defined IP addresses for Belet.tm domains.

    * **`ARIA2C`**: Set to `True` to enable `aria2c` as the external downloader for faster downloads.

### Running the Script

1.  **Run from Source**:

    ```
    python downloader.py


    ```

    The script will guide you through the login process if `AUTHORIZATION_TOKEN` is not set or expired, and then allow you to select the video and quality.

### Building an Executable (.exe)

You can create a standalone `.exe` file for easier distribution. This will bundle your script and its Python dependencies. However, you must include `ffmpeg.exe` and `aria2c.exe` manually.

1.  **Install PyInstaller**:

    ```
    pip install pyinstaller


    ```

2.  **Build the Executable**:
    Run the following command in your project's root directory. **Remember to replace the paths to `aria2c.exe` and `ffmpeg.exe` with their actual locations on your system.**

    ```
    pyinstaller downloader.py --onefile --name "BeletDownloader" ^
    --add-binary "C:\path\to\aria2c\aria2c.exe;." ^
    --add-binary "C:\path\to\ffmpeg\ffmpeg.exe;."


    ```

    * **`--onefile`**: Creates a single `.exe` file.

    * **`--name "BeletDownloader"`**: Sets the name of the output executable.

    * **`--add-binary "C:\path\to\aria2c\aria2c.exe;."`**: Includes `aria2c.exe` in the bundle.

    * **`--add-binary "C:\path\to\ffmpeg\ffmpeg.exe;."`**: Includes `ffmpeg.exe` in the bundle.

    This will create the `BeletDownloader.exe` in the `dist` folder. You will then place your `.env` file in the same directory as this `exe` when distributing it.

---

## ⚠️ Important Notes

* **SSL Certificate Errors**: If you encounter SSL/TLS handshake errors, the script includes `--no-check-certificate` for `yt-dlp` and `requests` to bypass these. Use this with caution and only with trusted sources.

* **FFmpeg Requirement**: FFmpeg is crucial for merging video, audio, and embedding subtitles. Ensure it's correctly bundled or available in your system's PATH.

* **`.env` File**: Keep your `.env` file secure as it contains authentication tokens.