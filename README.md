# audiobooks-downloader
Скрипты для загрузки аудиокниг в формате mp3.
Поддерживается:
* audioknigi.club
* audioknigi.online
* audioknigi.ru
* knigavuhe.org

----------------------------------------------------
## Pre-requisites

* Python3 (https://www.python.org/downloads)
* pip (https://pip.pypa.io/en/stable/installing/)
* virtualenv (https://pypi.python.org/pypi/virtualenv)
* git client (https://git-scm.com/download/gui/windows)
* Chrome web browser.

## Installation (Windows)

* Create a virtual environment, clone the code:
```
virtualenv downloader
cd downloader
git clone https://github.com/mrsrvman/audiobooks-downloader.git src
```

* Install dependencies:
```
scripts\pip install -r src\requirements.txt
```
* Download [Chromedriver](https://chromedriver.chromium.org/downloads), extract to your current working directory.
* Make sure you have the recent version of  Chrome installed.
* Run the app:
```
cd src
scripts\python app.py -h
```
## Enjoy!
