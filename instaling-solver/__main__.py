import time
import getpass
import json
import sys
import selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, WebDriverException


def webdriver(headless):
    try:
        options = selenium.webdriver.firefox.options.Options()
        options.headless = headless
        options.set_preference("media.volume_scale", "0.0")
        return selenium.webdriver.Firefox(options=options)
    except WebDriverException:
        pass

    try:
        options = selenium.webdriver.chrome.options.Options()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--mute-audio")
        return selenium.webdriver.Chrome(options=options)
    except WebDriverException:
        pass
    print("Failed to find a suitable browser. Did you forget to install the webdriver?")
    exit(2)


class Settings:
    def __init__(self):
        self.username = None
        self.password = None
        self.file = "instaling.words"
        self.sessions_to_do = 1
        self.headless = False
        self.delay = 0

        if "--help" in sys.argv:
            print("Usage: " + sys.argv[0] + " [options]\n")
            print("Options:")
            print("--user       -u      your instaling username")
            print("--password   -p      your instaling password")
            print(
                "--sessions   -s      desired number of instaling sessions to complete"
            )
            print("--file       -f      file with the saved instaling words")
            print(
                "--delay      -d      delay in seconds before answering each question"
            )
            print("--headless   -h      start the program without browser gui")
            print("--help               display this help message")
            exit()

        for argument in range(len(sys.argv)):
            if "--user" == sys.argv[argument] or "-u" == sys.argv[argument]:
                self.username = sys.argv[argument + 1]
            if "--password" == sys.argv[argument] or "-p" == sys.argv[argument]:
                self.password = sys.argv[argument + 1]
            if "--sessions" == sys.argv[argument] or "-s" == sys.argv[argument]:
                self.sessions_to_do = int(sys.argv[argument + 1])
            if "--file" == sys.argv[argument] or "-f" == sys.argv[argument]:
                self.file = sys.argv[argument + 1]
            if "--delay" == sys.argv[argument] or "-d" == sys.argv[argument]:
                self.delay = int(sys.argv[argument + 1])
            if "--headless" == sys.argv[argument] or "-h" == sys.argv[argument]:
                self.headless = True

        if not self.username:
            self.username = input("Username: ")
        if not self.password:
            self.password = getpass.getpass("Password: ")


class Solver(Settings):
    def __init__(self):
        Settings.__init__(self)
        self.driver = webdriver(self.headless)
        try:
            self.questions, self.answers = json.load(open(self.file, "r"))
            print("Read " + str(len(self.questions)) + " words from file " + self.file)
        except (FileNotFoundError, json.JSONDecodeError):
            self.questions = []
            self.answers = []

    def login(self):
        self.driver.get("https://instaling.pl/login")
        self.driver.find_element(By.ID, "log_email").send_keys(self.username)
        self.driver.find_element(By.ID, "log_password").send_keys(self.password)
        self.driver.find_element(By.ID, "log_password").send_keys(Keys.ENTER)

        try:
            WebDriverWait(self.driver, 5).until(
                ec.element_to_be_clickable((By.CLASS_NAME, "btn-session"))
            )
        except TimeoutException:
            print("Login failed")
            exit(1)
        self.driver.find_element(By.CLASS_NAME, "btn-session").click()

        WebDriverWait(self.driver, float("inf")).until(
            ec.visibility_of_element_located((By.ID, "allpage"))
        )
        while True:
            if self.driver.find_element(By.ID, "start_session_button").is_displayed():
                self.driver.find_element(By.ID, "start_session_button").click()
                break
            if self.driver.find_element(
                By.ID, "continue_session_button"
            ).is_displayed():
                self.driver.find_element(By.ID, "continue_session_button").click()
                break
        print("Logged in as " + self.username + "\n")

    def session_end(self):
        self.sessions_to_do = self.sessions_to_do - 1
        if self.sessions_to_do == 0:
            json.dump(
                [self.questions, self.answers],
                open(self.file, "w"),
                indent=4,
                ensure_ascii=False,
            )
            exit()
        else:
            print(str(self.sessions_to_do) + " sessions left\n")
            self.driver.find_element(By.ID, "return_mainpage").click()
            WebDriverWait(self.driver, float("inf")).until(
                ec.element_to_be_clickable((By.CLASS_NAME, "btn-session"))
            )
            self.driver.find_element(By.CLASS_NAME, "btn-session").click()
            WebDriverWait(self.driver, float("inf")).until(
                ec.element_to_be_clickable((By.ID, "start_session_button"))
            )
            self.driver.find_element(By.ID, "start_session_button").click()

    def learn(self, question):
        self.driver.find_element(By.ID, "check").click()
        WebDriverWait(self.driver, float("inf")).until(
            ec.presence_of_element_located((By.ID, "word"))
        )
        answer = self.driver.find_element(By.ID, "word").text
        self.driver.find_element(By.ID, "next_word").click()
        self.answers.append(answer)
        self.questions.append(question)
        print("Learned a new word: " + question.replace("\n", " ") + "-    " + answer)

    def answer(self):
        time.sleep(self.delay)
        if self.driver.find_element(By.ID, "return_mainpage").is_displayed():
            self.session_end()

        if self.driver.find_element(By.ID, "know_new").is_displayed():
            self.driver.find_element(By.ID, "know_new").click()
            self.driver.find_element(By.ID, "skip").click()

        if self.driver.find_element(By.ID, "answer").is_displayed():
            question = self.driver.find_element(By.ID, "question").text
            if question in self.questions:
                answer_index = self.questions.index(question)
                print(
                    "Answered: "
                    + question.replace("\n", " ")
                    + "-    "
                    + self.answers[answer_index]
                )
                self.driver.find_element(By.ID, "answer").send_keys(
                    self.answers[answer_index]
                )
                WebDriverWait(self.driver, float("inf")).until(
                    ec.presence_of_element_located((By.ID, "check"))
                )
                self.driver.find_element(By.ID, "check").click()
                WebDriverWait(self.driver, float("inf")).until(
                    ec.element_to_be_clickable((By.ID, "nextword"))
                )
                self.driver.find_element(By.ID, "nextword").click()
            else:
                self.learn(question)

    def __del__(self):
        try:
            self.driver.close()
        except AttributeError:
            pass


if __name__ == "__main__":
    solver = Solver()
    solver.login()
    while True:
        solver.answer()
