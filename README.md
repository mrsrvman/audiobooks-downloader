# audiobooks-downloader
Скрипты для загрузки аудиокниг в формате mp3.
Поддерживается:
audioknigi.club
audioknigi.online
audioknigi.ru
knigavuhe.org

Pre-requisites
Python3 (https://www.python.org/downloads)
pip (https://pip.pypa.io/en/stable/installing/)
virtualenv (https://pypi.python.org/pypi/virtualenv)
git client (https://git-scm.com/download/gui/windows)
Ghrome web browser.
Installation (Windows)
Create a virtual environment, clone the code:
virtualenv downloader
cd downloader
git clone https://github.com/mrsrvman/audiobooks-downloader.git src
Install dependencies:
scripts\pip install -r src\requirements.txt
Download Chromedriver, extract to your current working directory.
Make sure you have the recent version of Firefox installed.
Run the app:
cd src
scripts\python app.py
Or build a single-file executable:
cd src
pyinstaller app.spec --onefile
