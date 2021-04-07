![](https://img.shields.io/pypi/status/instaling-solver)
![](https://img.shields.io/github/license/smellyn3rd/instaling-solver)

## About the project
instaling-solver is a small project that automates the process of answering [instaling.pl](https://instaling.pl/) questions.


## dependencies
- [geckodriver-autoinstaller](https://pypi.org/project/geckodriver-autoinstaller/)
- [selenium](https://pypi.org/project/selenium/)
- [firefox](https://www.mozilla.org/firefox/new/)

## Installation
`pip install instaling-solver`</br></br>

or</br></br>

`git clone https://github.com/SmellyN3rd/instaling-solver`</br></br>
`cd instaling-solver`</br></br>
`python setup.py install`</br></br>

## Usage
`python -m instaling-solver [options]`</br></br>

## Options

option        | description
------------- | -------------
--user    -u        | specify the instaling account to use
--password    -p    | password for the given account
--sessions -s    | specify the amount of sessions to complete
--file    -f        | specify the file to which to read/write the known words
--headless    -h    | toogle headless mode (without browser gui)
--config    -c    | dump all settings into a file which will be loaded automaticly in the future

# Showcase
<img src="https://media.giphy.com/media/njjiYq0zcxNpkfeV02/giphy.gif" >
