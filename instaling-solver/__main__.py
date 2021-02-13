from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sys import argv, exit
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, \
    UnexpectedAlertPresentException, NoSuchElementException
import geckodriver_autoinstaller
import configparser
from selenium.webdriver.firefox.options import Options

__author__ = "SmellyN3rd"


def argument_parse():
    parsed = {"username": "", "password": "", "file": "instaling.words", "sessions_to_do": 1, "headless": False}

    if "--help" in argv:
        print("usage: " + argv[0] + " [options]\n")
        print("options:")
        print("--user       -f      your instaling username")
        print("--password   -p      yor instaling password")
        print("--sessions   -s      desired number of instaling sessions to complete")
        print("--file       -f      file with the saved instaling words")
        print("--headless   -h      start the program without browser gui")
        print("--help               display this help message")
        exit()
    try:
        config = configparser.ConfigParser()
        config.read("config.ini")
        if "username" in config["settings"]:
            parsed["username"] = config["settings"]["username"]
        if "password" in config["settings"]:
            parsed["password"] = config["settings"]["password"]
        if "sessions_to_do" in config["settings"]:
            parsed["sessions_to_do"] = int(config["settings"]["sessions_to_do"])
        if "file" in config["settings"]:
            parsed["file"] = config["settings"]["file"]
    except KeyError:
        pass

    for argument in range(len(argv)):
        if "--user" == argv[argument] or "-u" == argv[argument]:
            parsed["username"] = argv[argument + 1]
        if "--password" == argv[argument] or "-p" == argv[argument]:
            parsed["password"] = argv[argument + 1]
        if "--sessions" == argv[argument] or "-s" == argv[argument]:
            parsed["sessions_to_do"] = int(argv[argument + 1])
        if "--file" == argv[argument] or "-f" == argv[argument]:
            parsed["file"] = argv[argument + 1]
        if "--headless" == argv[argument] or "-h" == argv[argument]:
            parsed["headless"] = True

    if parsed["username"] == "":
        print("please specify what user to use")
        exit()
    if parsed["password"] == "":
        print("please type the password for the user " + parsed["username"])
        exit()
    return parsed


def webdriver_generate(headless):
    geckodriver_autoinstaller.install()
    profile = webdriver.FirefoxProfile()
    options = Options()
    options.headless = headless
    profile.set_preference("media.volume_scale", "0.0")
    return webdriver.Firefox(firefox_profile=profile, options=options)


def read_words(file):
    try:
        lists = open(file, 'r').read().split('\n')
        questions = lists[0].split('|')
        answers = lists[1].split('|')
        del questions[-1]
        del answers[-1]
        print("read " + str(len(questions)) + " words from file " + file)
    except IOError:
        questions = ['null']
        answers = ['null']
    return {"questions": questions, "answers": answers}


def write_fiile(questions, answers, file):
    open('geckodriver.log', 'w')
    open(file, 'w')
    for i in questions:
        open(file, 'a').write(str(i) + '|')
    open(file, 'a').write('\n')
    for j in answers:
        open(file, 'a').write(str(j) + '|')


def login(driver, username, password):
    driver.get('https://instaling.pl/login')
    driver.find_element_by_id("log_email").send_keys(username)
    driver.find_element_by_id("log_password").send_keys(password)
    driver.find_element_by_id("log_password").send_keys(Keys.ENTER)
    try:
        WebDriverWait(driver, 8).until(ec.presence_of_element_located((By.ID, "session_button")))
        driver.find_element_by_id("session_button").click()
    except TimeoutException:
        driver.close()
        print("wrong password")
        exit()
    try:
        for i in driver.find_elements_by_class_name("big_button"):
            i.click()
    except ElementNotInteractableException:
        pass

    try:
        driver.find_elements_by_class_name("big_button")[2].click()
    except ElementNotInteractableException:
        pass

    print("logged in as " + username + "\n")


def question(driver):
    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, "question")))
    if driver.find_element_by_id("check").is_displayed() and driver.find_element_by_id("question").is_displayed():
        for text in driver.find_element_by_id('question').text.split('\n'):
            if '_' not in text:
                break
        return text


def dismiss_popup(driver):
    if driver.find_element_by_id("dont_know_new").is_displayed():
        driver.find_element_by_id("dont_know_new").click()
        driver.find_element_by_id("skip").click()
        print("dismissed a popup")
    if driver.find_element_by_id("start_session_button").is_displayed():
        driver.find_element_by_id("start_session_button").click()


def session_end(driver, sessions_to_do, file, questions, answers):
    if webdriver.find_element_by_id("return_mainpage").is_displayed():
        WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.ID, "return_mainpage")))
        sessions_to_do = sessions_to_do - 1
        if sessions_to_do == 0:
            print("completed all sesions")
            write_fiile(questions, answers, file)
            webdriver.close()
            exit()
        print(str(sessions_to_do) + " sessions left\n")
        driver.find_element_by_id("return_mainpage").click()
        while True:
            try:
                driver.find_element_by_id("session_button").click()
                break
            except UnexpectedAlertPresentException or NoSuchElementException:
                continue
    return sessions_to_do


def learn(driver, questions, answers):
    if question(driver) not in questions:
        tmp = [question(driver)]
        while driver.find_element_by_id("check").is_displayed():
            driver.find_element_by_id("check").click()
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, "word")))
        if driver.find_element_by_id("word").is_displayed():
            tmp.append(driver.find_element_by_id("word").text)
        while driver.find_element_by_id("next_word").is_displayed():
            driver.find_element_by_id("next_word").click()
        try:
            if None not in tmp:
                answers.append(tmp[1])
                questions.append(tmp[0])
                print("learnt a new word: " + tmp[0] + " - " + tmp[1])
        except IndexError:
            pass
    return {"questions": questions, "answers": answers}


def answer(driver, questions, answers):
    dismiss_popup(driver)

    questions = list(dict.fromkeys(questions))
    answers = list(dict.fromkeys(answers))

    if question(driver) in questions and driver.find_element_by_id("answer").is_displayed():
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, "answer")))
        if driver.find_element_by_id("answer").is_displayed() and question(driver) in questions:
            print("answered: " + question(driver) + ' - ' + answers[questions.index(question(driver))])
            for letter in answers[questions.index(question(driver))]:
                if letter == 'ä':
                    driver.find_elements_by_class_name("special_character_button")[0].click()
                    continue
                if letter == 'ö':
                    driver.find_elements_by_class_name("special_character_button")[1].click()
                    continue
                if letter == 'ü':
                    driver.find_elements_by_class_name("special_character_button")[2].click()
                    continue
                if letter == 'ß':
                    driver.find_elements_by_class_name("special_character_button")[3].click()
                    continue
                if letter == 'Ä':
                    driver.find_elements_by_class_name("special_character_button")[4].click()
                    continue
                if letter == 'Ö':
                    driver.find_elements_by_class_name("special_character_button")[5].click()
                    continue
                if letter == 'Ü':
                    driver.find_elements_by_class_name("special_character_button")[6].click()
                    continue
                driver.find_element_by_id("answer").send_keys(letter)
        while driver.find_element_by_id("check").is_displayed():
            driver.find_element_by_id("check").click()
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, "next_word")))
        while driver.find_element_by_id("next_word").is_displayed():
            driver.find_element_by_id("next_word").click()
    else:
        return learn(driver, questions, answers)
    return {"questions": questions, "answers": answers}


if __name__ == "__main__":
    settings = argument_parse()
    webdriver = webdriver_generate(settings["headless"])
    print("instaling solver by " + __author__)
    lists = read_words(settings["file"])
    login(webdriver, settings["username"], settings["password"])
    while True:
        lists = answer(webdriver, lists["questions"], lists["answers"])
        settings["sessions_to_do"] = session_end(webdriver, settings["sessions_to_do"], settings["file"],
                                                 lists["questions"], lists["answers"])
