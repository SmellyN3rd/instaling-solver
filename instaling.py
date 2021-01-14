from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sys import argv, exit
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, \
    UnexpectedAlertPresentException, NoSuchElementException
import geckodriver_autoinstaller

__author__ = "SmellyN3rd"


def webdriver_generate():
    geckodriver_autoinstaller.install()
    profile = webdriver.FirefoxProfile()
    profile.set_preference("media.volume_scale", "0.0")
    return webdriver.Firefox(firefox_profile=profile)


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
    if driver.find_element_by_id("check").is_displayed() and driver.find_element_by_id("question").is_displayed():
        for text in driver.find_element_by_id('question').text.split('\n'):
            if '_' not in text:
                break
        return text


def session_end(driver):
    driver.find_element_by_id("return_mainpage").click()
    while True:
        try:
            driver.find_element_by_id("session_button").click()
            break
        except UnexpectedAlertPresentException or NoSuchElementException:
            continue


def learn(driver):
    if question(driver) not in questions:
        questions.append(question(driver))
        while driver.find_element_by_id("check").is_displayed():
            driver.find_element_by_id("check").click()
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, "word")))
        if driver.find_element_by_id("word").is_displayed():
            answers.append(driver.find_element_by_id("word").text)
        else:
            del questions[-1]
        while driver.find_element_by_id("next_word").is_displayed():
            driver.find_element_by_id("next_word").click()


def answer(driver):
    if driver.find_element_by_id("dont_know_new").is_displayed():
        driver.find_element_by_id("dont_know_new").click()
        driver.find_element_by_id("skip").click()
    if driver.find_element_by_id("start_session_button").is_displayed():
        driver.find_element_by_id("start_session_button").click()

    if question(driver) in questions:
        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, "answer")))
        if driver.find_element_by_id("answer").is_displayed() and question(driver) in questions:
            print(question(driver) + ' - ' + answers[questions.index(question(driver))])
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
        learn(driver)


if __name__ == "__main__":
    global questions
    global answers
    username = " "
    password = " "
    questions = ['język niemiecki']
    answers = ['Deutsch']
    sessions_to_do = 1
    file = "instaling.words"

    print("instaling solver by " + __author__)

    for argument in argv:
        if "--user=" in argument:
            username = argument.replace("--user=", "")
        if "--password=" in argument:
            password = argument.replace("--password=", "")
        if "--sessions=" in argument:
            sessions_to_do = int(argument.replace("--sessions=", ""))
        if "--file=" in argument:
            file = argument.replace("--file=", "")
        if "--minimize" in argument:
            webdriver.minimize_window()
        if "--help" in argument:
            print("usage: " + argv[0] + " [options]\n")
            print("options:")
            print("--user=      your instaling username")
            print("--password=  yor instaling password")
            print("--sessions=  desired number of instaling sessions to complete")
            print("--file=      file with the saved instaling words")
            print("--minimize   start the program minimized")
            print("--help       display this help message")
            exit()

    try:
        lists = open(file, 'r').read().split('\n')
        questions = lists[0].split(';')
        answers = lists[1].split(';')
        del questions[-1]
        del answers[-1]
        print("read " + str(len(questions)) + " words from file " + file)
    except IOError:
        pass
    webdriver = webdriver_generate()
    login(webdriver, username, password)

    while True:
        if webdriver.find_element_by_id("return_mainpage").is_displayed():
            sessions_to_do = sessions_to_do - 1
            if sessions_to_do == 0:
                print("completed all sesions")
                open('geckodriver.log', 'w')
                open(file, 'w')
                for i in questions:
                    open(file, 'a').write(str(i) + ';')
                open(file, 'a').write('\n')
                for j in answers:
                    open(file, 'a').write(str(j) + ';')
                webdriver.close()
                exit()
            print(str(sessions_to_do) + " sessions left\n")
            session_end(webdriver)

        answer(webdriver)
