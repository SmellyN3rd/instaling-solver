from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from sys import argv, exit
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException
from selenium.webdriver.firefox.options import Options
import geckodriver_autoinstaller
from time import sleep


def argument_parse():
    parsed = {
        "username": "",
        "password": "",
        "file": "instaling.words",
        "sessions_to_do": 1,
        "headless": False,
        "delay": 0,
    }

    if "--help" in argv:
        print("usage: " + argv[0] + " [options]\n")
        print("options:")
        print("--user       -f      Your instaling username")
        print("--password   -p      Your instaling password")
        print("--sessions   -s      desired number of instaling sessions to complete")
        print("--file       -f      file with the saved instaling words")
        print("--delay      -d      delay in seconds before answering each question")
        print("--headless   -h      start the program without browser gui")
        print("--help               display this help message")
        exit()

    for argument in range(len(argv)):
        if "--user" == argv[argument] or "-u" == argv[argument]:
            parsed["username"] = argv[argument + 1]
        if "--password" == argv[argument] or "-p" == argv[argument]:
            parsed["password"] = argv[argument + 1]
        if "--sessions" == argv[argument] or "-s" == argv[argument]:
            parsed["sessions_to_do"] = int(argv[argument + 1])
        if "--file" == argv[argument] or "-f" == argv[argument]:
            parsed["file"] = argv[argument + 1]
        if "--delay" == argv[argument] or "-d" == argv[argument]:
            parsed["delay"] = int(argv[argument + 1])
        if "--headless" == argv[argument] or "-h" == argv[argument]:
            if not parsed["headless"]:
                parsed["headless"] = True
            else:
                parsed["headless"] = False

    if parsed["username"] == "":
        parsed["username"] = input("Username: ")

    if parsed["password"] == "":
        parsed["password"] = input("Password: ")
        print()
    return parsed


def webdriver_generate(headless):
    geckodriver_autoinstaller.install()
    options = Options()
    options.headless = headless
    options.set_preference("media.volume_scale", "0.0")
    return webdriver.Firefox(options=options)


def read_words(file):
    try:
        lists = open(file, "r").read().split("\n\n")
        questions = lists[0].split(" :|: ")
        answers = lists[1].split(" :|: ")
        del questions[-1]
        del answers[-1]
        print("Read " + str(len(questions)) + " words from file " + file)
    except IOError:
        questions = [""]
        answers = [""]
    return {"questions": questions, "answers": answers}


def write_words(questions, answers, file):
    open(file, "w")
    for i in questions:
        open(file, "a").write(str(i) + " :|: ")
    open(file, "a").write("\n\n")
    for j in answers:
        open(file, "a").write(str(j) + " :|: ")


def login(driver, username, password):
    driver.get("https://instaling.pl/login")
    driver.find_element(By.ID, "log_email").send_keys(username)
    driver.find_element(By.ID, "log_password").send_keys(password)
    driver.find_element(By.ID, "log_password").send_keys(Keys.ENTER)
    try:
        WebDriverWait(driver, 5).until(
            ec.presence_of_element_located((By.CLASS_NAME, "btn-session"))
        )
        driver.find_element(By.CLASS_NAME, "btn-session").click()
    except TimeoutException:
        driver.close()
        print("Wrong password")
        exit()
    WebDriverWait(driver, 5).until(
        ec.presence_of_element_located((By.CLASS_NAME, "big_button"))
    )
    if driver.find_element(By.ID, "start_session_button").is_displayed():
        driver.find_element(By.ID, "start_session_button").click()
    if driver.find_element(By.ID, "continue_session_button").is_displayed():
        driver.find_element(By.ID, "continue_session_button").click()
    print("Logged in as " + username + "\n")


def question(driver):
    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, "question")))
    return driver.find_element(By.ID, "question").text


def dismiss_popup(driver):
    if driver.find_element(By.ID, "dont_know_new").is_displayed():
        driver.find_element(By.ID, "dont_know_new").click()
        driver.find_element(By.ID, "skip").click()
    if driver.find_element(By.ID, "start_session_button").is_displayed():
        driver.find_element(By.ID, "start_session_button").click()


def session_end(driver, sessions_to_do, file, questions, answers):
    sessions_to_do = sessions_to_do - 1
    if sessions_to_do == 0:
        write_words(questions, answers, file)
        webdriver.close()
        exit()
    print(str(sessions_to_do) + " sessions left\n")
    driver.find_element(By.ID, "return_mainpage").click()
    WebDriverWait(driver, 8).until(
        ec.presence_of_element_located((By.CLASS_NAME, "btn-session"))
    )
    driver.find_element(By.CLASS_NAME, "btn-session").click()
    return sessions_to_do


def learn(driver, questions, answers):
    question_text = question(driver)
    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, "check")))
    driver.find_element(By.ID, "check").click()
    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, "word")))
    answer = driver.find_element(By.ID, "word").text
    driver.find_element(By.ID, "next_word").click()
    answers.append(answer)
    questions.append(question_text)
    print("Learnt a new word: " + question_text.replace("\n", " ") + "-    " + answer)
    return {"questions": questions, "answers": answers}


def get_index(questions, question):
    for i in range(len(questions)):
        if questions[i] == question:
            return i
    return False


def answer(driver, questions, answers, answer_delay):
    WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, "answer")))
    question_text = question(driver)
    answer_index = get_index(questions, question_text)

    sleep(answer_delay)
    if answer_index:
        print(
            "Answered: "
            + question_text.replace("\n", " ")
            + "-    "
            + answers[answer_index]
        )
        for letter in answers[answer_index]:
            if letter == "ä":
                driver.find_elements(By.CLASS_NAME, "special_character_button")[
                    0
                ].click()
                continue
            if letter == "ö":
                driver.find_elements(By.CLASS_NAME, "special_character_button")[
                    1
                ].click()
                continue
            if letter == "ü":
                driver.find_elements(By.CLASS_NAME, "special_character_button")[
                    2
                ].click()
                continue
            if letter == "ß":
                driver.find_elements(By.CLASS_NAME, "special_character_button")[
                    3
                ].click()
                continue
            if letter == "Ä":
                driver.find_elements(By.CLASS_NAME, "special_character_button")[
                    4
                ].click()
                continue
            if letter == "Ö":
                driver.find_elements(By.CLASS_NAME, "special_character_button")[
                    5
                ].click()
                continue
            if letter == "Ü":
                driver.find_elements(By.CLASS_NAME, "special_character_button")[
                    6
                ].click()
                continue
            driver.find_element(By.ID, "answer").send_keys(letter)

        WebDriverWait(driver, 5).until(ec.presence_of_element_located((By.ID, "check")))
        driver.find_element(By.ID, "check").click()
        WebDriverWait(driver, 5).until(ec.element_to_be_clickable((By.ID, "nextword")))
        driver.find_element(By.ID, "nextword").click()
    else:
        return learn(driver, questions, answers)
    return {"questions": questions, "answers": answers}


if __name__ == "__main__":
    settings = argument_parse()
    webdriver = webdriver_generate(settings["headless"])
    lists = read_words(settings["file"])
    login(webdriver, settings["username"], settings["password"])
    while True:
        try:
            lists = answer(
                webdriver, lists["questions"], lists["answers"], settings["delay"]
            )
        except (ElementNotInteractableException, TimeoutException):
            dismiss_popup(webdriver)
            if webdriver.find_element(By.ID, "return_mainpage").is_displayed():
                settings["sessions_to_do"] = session_end(
                    webdriver,
                    settings["sessions_to_do"],
                    settings["file"],
                    lists["questions"],
                    lists["answers"],
                )
