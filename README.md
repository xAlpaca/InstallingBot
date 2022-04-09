# InstallingBot
#### (installing.pl)

## What does this bot do?
- Autocoplete every question that appears in the quize.
- Self-learning, after running the script, you don't have to worry about new questions that might appear. 
- Adjustable amount of series per run.

## How do I use it?
- You need to [Download Python](https://www.python.org/downloads/release/python-3912/) and install it.
- Then, open cmd and type: ```python -m pip install selenium```

You have just installed python, and setupped the libraries. Now it is time to download WebdDriver, it dipend on browser that you have on your computer. 
- For Chrome: you should check your browser verison after that go to [ChromeDriver Website](https://chromedriver.chromium.org/downloads) and download an exe matching your browser version. 
- After all, create an empty folder and UnZip your ChromeDriver and clone installingBot.py into directory. 

## Setup for easier usage
- All you need is modify line 10 and 11 
### installingBot.py
```python 
7 driver = webdriver.Chrome("./chromedriver.exe")
8 driver.get("https://instaling.pl/teacher.php?page=login")
9 
10 username = "Your installing.py username"  <---
11 password = "Your installing.py password"  <---
12 
13 
14 def start_session():
```
