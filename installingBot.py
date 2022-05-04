from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import json
import os

driver = webdriver.Chrome("./chromedriver.exe")
driver.get("https://instaling.pl/teacher.php?page=login")

username = ""
password = ""
amount_of_sessions = 3


def start_session():
    start_session_btn_1 = driver.find_element(By.XPATH, '//*[@id="student_panel"]/p[1]/a')
    start_session_btn_1.click()

    driver.implicitly_wait(1)

    try:
        start_session_btn_2 = driver.find_element(By.XPATH, '//*[@id="start_session_button"]/h4')
        start_session_btn_2.click()
    except:
        start_session_btn_3 = driver.find_element(By.XPATH, '//*[@id="continue_session_button"]/h4')
        start_session_btn_3.click()


def log_in(_username, _password):
    if not os.path.isfile("dict.json"):
        f = open("dict.json", "a")
        f.write('{\n"none": "none"\n}')
        f.close()

    username_field = driver.find_element(By.ID, "log_email")
    password_field = driver.find_element(By.ID, "log_password")
    login_button = driver.find_element(By.XPATH, '//*[@id="main-container"]/div[3]/form/div/div[3]/button')

    username_field.send_keys(str(_username))
    password_field.send_keys(str(_password))

    login_button.click()

    time.sleep(1)

    start_session()


def answer_question():
    try:
        # Final message?
        return_to_menu = driver.find_element(By.XPATH, '//*[@id="return_mainpage"]/h4')
        return_to_menu.click()
        return "Session performed"

    except:
        try:
            # Installing.pl may sometimes ask you if you want to add a new word to dictionary,
            # you must click "No", unless you have a premium.
            new_word = driver.find_element(By.XPATH, '//*[@id="dont_know_new"]/h4')
            new_word.click()

            time.sleep(1)

            continue_btn = driver.find_element(By.XPATH, '//*[@id="skip"]')
            continue_btn.click()

        except:
            pass
        pass

    dict_file = open("dict.json")
    data = json.load(dict_file)
    dict_file.close()

    question = driver.find_element(By.XPATH, '//*[@id="question"]/div[1]')
    input_field = driver.find_element(By.XPATH, '//*[@id="answer"]')
    submit_answer = driver.find_element(By.XPATH, '//*[@id="check"]/h4')

    q_text = question.text

    if q_text in data:
        # Answer is in JSON
        input_field.send_keys(str(data[q_text]))
        submit_answer.click()

    else:
        # Add answer to JSON
        submit_answer.click()

        driver.implicitly_wait(0.5)
        right_answer = driver.find_element(By.XPATH, '//*[@id="word"]')
        if right_answer.text != "" and q_text != "":
            with open("dict.json", "r+") as file:
                # Write to file
                data = json.load(file)
                data[q_text] = right_answer.text
                file.seek(0)
                json.dump(data, file, indent=4)
                # time.sleep(0.25)
                # driver.implicitly_wait(0.25)
                file.truncate()

    driver.implicitly_wait(0.5)

    next_question = driver.find_element(By.XPATH, '//*[@id="next_word"]')
    next_question.click()

    return None


def perform_session(_amount_of_sessions):
    for session in range(_amount_of_sessions):
        print(f"Session {session + 1} started")
        response = None
        while response is None:
            try:
                response = answer_question()
            except:
                pass
        driver.implicitly_wait(1)

        start_session()

    exit()


if __name__ == "__main__":
    if username != "" and password != "":
        log_in(username, password)
    else:
        username = input("Your username:\n")
        password = input("Your password:\n")
        log_in(username, password)
    perform_session(amount_of_sessions)
