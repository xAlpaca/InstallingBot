import asyncio
import aiofiles
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
import os

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_experimental_option('excludeSwitches', ['enable-logging'])

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

username = ""
password = ""


data = [["", ""],]
amount_of_sessions = 1


async def start_session():
    start_session_btn_1 = driver.find_element(By.XPATH, '//*[@id="student_panel"]/p[1]/a')
    start_session_btn_1.click()

    driver.implicitly_wait(1)

    try:
        start_session_btn_2 = driver.find_element(By.XPATH, '//*[@id="start_session_button"]/h4')
        start_session_btn_2.click()
    except:
        start_session_btn_3 = driver.find_element(By.XPATH, '//*[@id="continue_session_button"]/h4')
        start_session_btn_3.click()


async def log_in(_username, _password):
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

    task = asyncio.create_task(start_session())
    await task


async def answer_question():

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

            continue_btn = driver.find_element(By.XPATH, '//*[@id="skip"]')
            continue_btn.click()

        except:
            pass
        pass


    question = driver.find_element(By.XPATH, '//*[@id="question"]/div[1]')
    input_field = driver.find_element(By.XPATH, '//*[@id="answer"]')
    submit_answer = driver.find_element(By.XPATH, '//*[@id="check"]/h4')

    q_text = question.text




    dict_file = open("dict.json")
    data = json.load(dict_file)
    dict_file.close()



    if q_text in data:
        # Answer is in JSON

        input_field.send_keys(str(data[q_text]))
        submit_answer.click()

    else:
        # Add answer to JSON
        submit_answer.click()
        right_answer = driver.find_element(By.XPATH, '//*[@id="word"]')

        if right_answer.text != "" and q_text != "":
            task = asyncio.create_task(write_fo_file(q_text, right_answer.text))
            await task

        await asyncio.sleep(0.5)

    next_question = driver.find_element(By.XPATH, '//*[@id="next_word"]')
    next_question.click()

    return None


async def perform_session(_amount_of_sessions):

    for session in range(_amount_of_sessions):
        print(f"Session {session + 1} started")
        response = None
        while response is None:
            try:
                response = await answer_question()
            except:
                pass


        if session < _amount_of_sessions-1:

            task = asyncio.create_task(start_session())
            await task


async def write_fo_file(q, a):
    async with aiofiles.open("dict.json", "r") as file:
        data = await file.read()
        data = json.loads(data)
        data[str(q)] = str(a)
    async with aiofiles.open("dict.json", "w") as file:
        await file.write("{\n")
        id = 0
        for i in data:
            await file.write(f'"{i}": "{data[i]}"')
            id += 1
            if id < len(data):
                await file.write(",\n")
            else:
                await file.write("\n")
        await file.write("}")


async def main(data_):
    driver.get("https://instaling.pl/teacher.php?page=login")

    for i in data_:

        if i[0] != "" and i[1] != "":
            await log_in(i[0], i[1])
        else:
            i[0] = input("Your username:\n")
            i[1] = input("Your password:\n")

            await log_in(i[0], i[1])

        await perform_session(amount_of_sessions)

        driver.find_element(By.XPATH, '//*[@id="student_panel"]/p[9]/a').click()
        driver.find_element(By.XPATH, '/html/body/div/div[2]/a/img').click()
        driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/p[10]/a').click()

    print("Done")
    driver.close()
    exit()


if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    a = loop.run_until_complete(main(data))

