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
--user    -u        | Your instaling username
--password    -p    | Your instaling password
--sessions -s    | desired number of instaling sessions to complete
--file    -f        | file with the saved instaling words
--delay    -d        | delay in seconds before answering each question
--headless    -h    | toogle headless mode (without browser gui)

# Showcase
![instaling](https://user-images.githubusercontent.com/70511617/115993222-2ce74000-a5d2-11eb-842d-13b63abee105.gif)

