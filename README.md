![](https://img.shields.io/pypi/status/instaling-solver)
![](https://img.shields.io/github/license/smellyn3rd/instaling-solver)

## About the project
instaling-solver is a small project that automates the process of answering [instaling.pl](https://instaling.pl/) questions.

## Prerequisites
- [Firefox](https://www.mozilla.org/firefox/new/) or [Chromium](https://www.chromium.org/getting-involved/download-chromium/) based browser
- [Geckodriver](https://github.com/mozilla/geckodriver/releases) (For Firefox) or [Chromedriver](https://chromedriver.chromium.org/downloads) (For Chromium)

## Dependencies
- [Selenium](https://pypi.org/project/selenium/)

## Installation
Download a webdriver for your browser and copy it to path (for example `C:\Windows` or `/bin`)

`pip install instaling-solver`

## Usage
`python -m instaling-solver [options]`

## Options

option        | description
------------- | -------------
--user    -u        | your instaling username
--password    -p    | your instaling password
--sessions -s    | desired number of instaling sessions to complete
--file    -f        | file with the saved instaling words
--delay    -d        | delay in seconds before answering each question
--headless    -h    | toogle headless mode (without browser gui)
