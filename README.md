# Web Browser Application

## Overview
This project is a simple web browser application developed using PyQt5 and QWebEngineView. It includes core browser features such as tabbed browsing, history management, dark mode support, and private browsing.

## Features
- **Tab Support**: Open and close multiple tabs.
- **History Management**: Save and view the history of visited sites (stores the last 100 entries).
- **Private Browsing**: Browse without saving history.
- **Dark Mode**: Support for dark mode in both the interface and web pages.
- **Toolbar**: Basic navigation tools including back, forward, refresh, home, and URL bar.
- **Persistent Cookies**: Cookies are stored persistently.

## Requirements
- Python 3.x
- PyQt5
- PyQtWebEngine

## Installation
1. Install the required libraries:
   ```bash
   pip install PyQt5 PyQtWebEngine
   ```

2. Download or copy the project file (`browser.py`).

3. Run the application:
   ```bash
   python browser.py
   ```

## Usage
- **Open New Tab**: Click the `+` button on the toolbar.
- **Open Private Tab**: Click the "Private" button on the toolbar.
- **Navigate to URL**: Enter an address in the URL bar and press Enter.
- **View History**: Select "History" from the menu button (☰).
- **Dark Mode**: Toggle dark mode by checking/unchecking "Dark Mode" in the menu.
- **Clear History**: Select "Clear History" from the menu to delete history records.

## Code Structure
- **BrowserTab**: Manages tab functionality. Each tab is a `QWebEngineView` instance and includes history management and private browsing features.
- **Browser**: The main application window. Manages the toolbar, tabs, and settings.
- **Dark Mode**: Applies dark mode to web pages via CSS injection and to the interface via `QStyleSheet`.
- **History**: Visited sites are saved in JSON format and stored persistently using `QSettings`.

## Notes
- The application opens Google by default.
- Private tabs do not save history and are displayed in gray.
- Dark mode affects both the interface and visited web pages.
- History is limited to the last 100 entries.

## License
This project is distributed under the [MIT License](#mit-license). See the license details below.

## MIT License
The MIT License is an open-source software license that allows users to use, copy, modify, merge, publish, distribute, sublicense, and/or sell the software. It is provided "as is" without any warranty. The full license text is below:

```
MIT License

Copyright (c) 2025 Alper Samur

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```
