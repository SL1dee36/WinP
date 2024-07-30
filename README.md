
# WinP: File and System Utility

WinP is a user-friendly application built with Python and customtkinter, providing tools for file archiving, conversion, system optimization, and more. It's designed for ease of use and aims to simplify common file and system tasks.

## Features

* **Archiving:** Compress files and folders into archives with optional password protection. Supports extraction from .zis, .zip, and .7zip archives.
* **Conversion:** Convert between different file formats, including:
    * **Images:** PNG, JPG, JPEG, GIF, ICO
    * **Videos:** MP4, AVI, MOV
    * **Audios:** MP3, WAV, OGG
    * **Documents:** TXT 
* **Optimization:** 
    * Cleans up temporary files.
    * Provides options to check and manage registry entries (implementation in progress).
    * Optimizes system performance by freeing up RAM.
* **File Information and Editing:** View detailed file information and edit basic attributes (name, dates, read-only).
* **Context Menu Integration:** Access WinP's archiving and extraction functions directly from your file explorer's right-click menu.
* **Drag and Drop:** Easily select files and folders for archiving and conversion using drag and drop. 
* **Multilingual Support:** User interface available in English and Russian.
* **Cross-Platform Compatibility:** Developed with portability in mind, aiming for future compatibility with multiple operating systems.
* **System Tray Integration:** Minimize WinP to the system tray for easy access.
* **Real-Time System Monitoring:**  Displays a live graph of RAM usage.

## Getting Started

1. **Prerequisites:** Make sure you have Python installed on your system. WinP requires the following packages:
    - `customtkinter`
    - `CTkMessagebox`
    - `Pillow`
    - `moviepy`
    - `pydub`
    - `win32com` (For Windows context menu integration)
    - `pystray` (For System Tray Icon)
    - `pywinstyles` (For Drag & Drop)
    - `psutil` (For System Monitoring)
    - `matplotlib` (For RAM usage graph)

2. **Clone or Download:** Get the WinP repository from GitHub:

   ```bash 
   git clone https://github.com/sl1dee36/winp.git 
   ```

3. **Install Dependencies:** Navigate to the project directory and install the required packages:

   ```bash
   pip install -r requirements.txt
   ```

4. **Run WinP:** Execute the main script:

   ```bash
   python winp.py
   ```

## Usage

### Archiving

1. **Select File/Folder:** 
    * Drag and drop the file or folder onto the designated area. 
    * Click "Select" and choose the file or folder you want to archive.
2. **Set Options:** 
    - Choose between "File" or "Folder" compression type.
    - Check "Use Password?" and enter a password if desired.
3. **Archive/Extract:** 
    * Click "Archive" to compress.
    * Click "Extract" to decompress supported archive types.

### Conversion

1. **Select File:**  
    * Drag and drop the file onto the designated area.
    * Click "Select File" and choose the file you want to convert. File information will be displayed.
2. **Choose Category:**  Use the segmented buttons (Image, Video, Audio, Document) to select the appropriate category.
3. **Select Output Format:**  Choose the desired output format from the dropdown menu.
4. **Convert:**  Click "Convert" to start the conversion process. The converted file will be saved in your Downloads folder.

### Optimization

* **Clear Temp Folder:** Click "Clear Temp Folder" to remove temporary files.
* **Check Registry:** This feature is under development.
* **Free Up RAM:** Click "Free Up RAM" to attempt to clear unused RAM.

### Settings

* **Context Menu:** Enable or disable WinP's context menu integration.
* **Language:** Switch between available languages.
* **Run on Windows Startup:** Choose whether to launch WinP automatically when Windows starts.

## Context Menu Integration

On Windows, enable context menu integration during the first run or in the Settings. This adds options to right-click on files and folders to:

* **"Archive File/Folder with WinP":** Directly compress the selected item.
* **"Extract with WinP":**  Extract files from supported archive formats (.zis, .zip, .7zip).

## Contributing

Contributions to WinP are welcome! Here's how you can contribute:

* **Report Bugs:** Submit issues on the GitHub repository for any bugs or errors encountered.
* **Suggest Features:**  Propose new features or improvements by creating a new issue and describing your idea.
* **Code Contributions:** Fork the repository, make your changes, and submit a pull request for review.

## License

This project is licensed under the MIT License.

## Contact

* **GitHub:** [Nazaryan Artem @Sl1dee36](https://github.com/Sl1dee36)
* **Telegram:** @slide36 
