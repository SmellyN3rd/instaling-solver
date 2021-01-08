from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from sys import argv, exit


#getting the login information from user
try:
    login= argv[1]
    password= argv[2]
    sessions_to_do= int(argv[3])
    open('geckodriver.log', 'w')
except:
    print('Usage: '+argv[0]+' [login] [password] [number of sessions]')
    exit()

sessions_done= 0
unknown_countdown=0
print('Instaling solver by SmellyN3rd\n')


#trying to load a wordlist file
try:
    words = open('instaling.words','r')
    for list in words.readlines():
        exec(list)
    print('Read '+str(len(questions))+ ' words from file instaling.words')
except:
    questions=['język niemiecki']
    answers=['Deutsch']
    print('No wordlist file found. Using fallback wordlist')


#login script
profile = webdriver.FirefoxProfile()
profile.set_preference("media.volume_scale", "0.0")
driver = webdriver.Firefox(firefox_profile=profile)
driver.get('https://instaling.pl/login')

driver.find_element_by_id("log_email").send_keys(login)
driver.find_element_by_id("log_password").send_keys(password)
sleep(0.1)
driver.find_element_by_id("log_password").send_keys(Keys.ENTER)
sleep(0.4)
try:
    driver.find_element_by_id("session_button").click()
except:
    print('Wrong password. Try again')
    driver.close()
    exit()
sleep(0.1)

try:
    driver.find_element_by_id("continue_session_button").click()
except:
    driver.find_element_by_id("start_session_button").click()

print('Logged in as '+login)
print('Preparing to do '+str(sessions_to_do)+' sessions \n')




#the main event loop
while(True):

    #dismisses any unwanted popups
    try:
        driver.find_element_by_id("dont_know_new").click()
        sleep(0.1)
        driver.find_element_by_id("skip").click()
        sleep(0.1)
    except:
        pass


    #finding the question
    for question in range(len(questions)):

        try:
            driver.find_element_by_id('question').text
        except:
            words = open('instaling.words', 'w')
            words.write('questions=' +str(questions)+'\nanswers=' + str(answers))
            print('\nCompleted all sessions. Exiting')
            exit()

        for text in driver.find_element_by_id('question').text.split('\n'):
            if '_' not in text:
                break


    #learning unknown words
        unknown_countdown=unknown_countdown+1
        if unknown_countdown >= len(questions)*2:
            sleep(0.2)
            try:
                if text not in questions:
                    questions.append(text)
                else:
                    raise Exception(text+' already in memory')
                sleep(0.2)
                driver.find_element_by_id("check").click()
                sleep(0.5)
                answers.append(driver.find_element_by_id("word").text)
                print('Learnt new word: '+text+' - '+driver.find_element_by_id("word").text)
                driver.find_element_by_id("next_word").click()
                unknown_countdown=0
                sleep(0.2)
            except:
                try:
                    driver.find_element_by_id("dont_know_new").click()
                    sleep(0.1)
                    driver.find_element_by_id("skip").click()
                    del questions[len(questions)-1]
                except:
                    pass


        #finding the answer
        try:
            if questions[question] == text:
                unknown_countdown=0
                for letter in answers[question]:
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

                try:
                    while(True):
                        driver.find_element_by_id("check").click()
                        break
                except:
                    continue
                sleep(0.1)
                try:
                    while(True):
                        driver.find_element_by_id("next_word").click()
                        break
                except:
                    continue

                print(answers[question] + ' - ' + text)
        except:
            pass


    #checking if the current session is complete
    try:
        driver.find_element_by_id("return_mainpage").click()
        sleep(0.2)
        driver.find_element_by_id("session_button").click()
        sleep(0.2)
        driver.find_element_by_id("start_session_button").click()
        sessions_done= sessions_done+1
        print('Completed '+str(sessions_done)+' sessions ('+str(sessions_to_do-sessions_done)+' sessions left)\n')
        if sessions_done == sessions_to_do:
            driver.close()
            exit()
    except:
        pass
