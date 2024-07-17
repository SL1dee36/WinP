# WinP: File and System Utility

WinP is a user-friendly application built with Python and customtkinter, providing tools for file archiving, conversion, system optimization, and more. It's designed for ease of use and aims to simplify common file and system tasks.

## Features

* **Archiving:** Compress files and folders into archives with optional password protection. Supports extraction from various archive formats.
* **Conversion:** Convert between different file formats, including images, videos, audios, and documents.
* **Optimization (Planned):** Clean up temporary files, manage registry entries, and optimize system performance.
* **Context Menu Integration:** Access WinP's archiving and extraction functions directly from your file explorer's right-click menu.
* **Multilingual Support:** User interface available in English and Russian.
* **Cross-Platform Compatibility:** Developed with portability in mind, aiming for future compatibility with multiple operating systems.

## Getting Started

1. **Prerequisites:** Make sure you have Python installed on your system. WinP requires the following packages:
    - `customtkinter`
    - `CTkMessagebox`
    - `Pillow`
    - `moviepy`
    - `pydub`
    - `win32com` (For Windows context menu integration)

2. **Clone or Download:** Get the WinP repository from GitHub:

   ```bash
   git clone https://github.com/your-username/winp.git 
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

1. **Select File/Folder:** Click "Select" and choose the file or folder you want to archive.
2. **Set Options:** 
    - Select "File" or "Folder" compression type.
    - Check "Use Password?" and enter a password if desired.
3. **Archive/Extract:** Click "Archive" to compress or "Extract" to decompress.

### Conversion

1. **Select File:**  Click "Select File" and choose the file you want to convert. File information will be displayed.
2. **Choose Category:**  Use the segmented buttons (Image, Video, Audio, Document) to select the appropriate category.
3. **Select Output Format:**  Choose the desired output format from the dropdown menu.
4. **Convert:**  Click "Convert" to start the conversion process.

### Settings

* **Context Menu:** Enable or disable WinP's context menu integration for quick access to archiving and extraction.
* **Language:** Switch between English and Russian language options.

## Context Menu Integration

On Windows, you can enable context menu integration during the first run of WinP. This adds options to right-click on files and folders to:

* **"Archive File/Folder with WinP":** Directly compress the selected item.
* **"Extract with WinP":**  Extract files from supported archive formats.

## Contributing

Contributions to WinP are welcome! Here's how you can contribute:

* **Report Bugs:** Submit issues on the GitHub repository for any bugs or errors encountered.
* **Suggest Features:**  Propose new features or improvements by creating a new issue and describing your idea.
* **Code Contributions:** Fork the repository, make your changes, and submit a pull request for review.

## License

This project is licensed under the MIT License.

## Contact

* **GitHub:** [Nazaryan Artem @Sl1dee36](https://github.com/Sl1dee36)

---
