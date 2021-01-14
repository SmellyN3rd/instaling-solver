## About the project
instaling-solver is a small project that automates the process of answering [instaling.pl](https://instaling.pl/) questions.


## dependencies
- [geckodriver-autoinstaller](https://pypi.org/project/geckodriver-autoinstaller/)
- [selenium](https://pypi.org/project/selenium/)
- [firefox](https://www.mozilla.org/firefox/new/)


## Usage

`git clone https://github.com/SmellyN3rd/instaling-solver`</br></br>
`cd instaling-solver`</br></br>
`pip install -r requirements.txt`</br></br>
`python instaling.py [options]`</br></br>

## Options

--user=                          specify the instaling account to use
--password=                        password for the given account
--sessions=                        specify the amount of sessions to complete
--file=                           specify the file to which to read/write to
--minimize                         start the program with a minimized browser
