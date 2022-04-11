# Warzone-Bot-V1.0 (Python)
This is a bot created for Warzone that reads the screen and detects the people you kill/get killed by and it webscrapes their stats from cod.tracker.gg. This can be used to help you identify a cheater. This is an updated launch with a GUI.

What libraries does it use?
* PyAuto GUI
* CV2
* Time
* Pytesseract
* PIL
* Selenium
* MSS

How to run it? 
Main file is: Warzone Scanning Bot.py
What you want to make sure you do is have the correct version of chromedriver. 
To do this, go to Google Chrome's about page and check which version you have of Chrome, for example I have 97.

![image](https://user-images.githubusercontent.com/47039827/150620152-56ea6a67-d0fb-4c15-8448-01ccdc3a7ac8.png)
![image](https://user-images.githubusercontent.com/47039827/150620192-f350a8c3-c8e7-45b1-92af-8925171f1d9c.png)

Then, you want to go here (https://chromedriver.chromium.org/downloads) and download the appropriate version for your chrome browser. 
Extract the file and replace the chromedriver.exe in the repo for your appropriate version. My advice is to update Chrome before doing this. 

You also need to download pytesseract and include the path in the code. Just copy it and paste the path under line 21. 

How does the bot work?
I gave it a few examples to use as comparison. I turned them to grayscale to try to reduce the time it takes for it to compare and increase accuracy. Using PyAuto GUI it analyzes the bottom of the screen where usernames appear when you kill or get killed by a player. Once it finds something similar it will screenshot it with mss (very fast) and using a little bit of image processing with cv2 to enlarge the image, it uses pytesseract to convert the image to string. Once converted to string it tries to remove the clan tag from the username. It does this by removing any [clan]* combination between brackets. It then removes the hashtag and adds a percent sign and adds the number 23 to the right of it like the cod.tracker.gg website does. It then uses the built website link with the extracted username in selenium where it webscrapes the stats from cod.tracker.gg. (See image below) **The first time the bot runs it takes about 9-10s to fetch stats, after that it only takes 2s per player.**

![image](https://user-images.githubusercontent.com/47039827/162818479-eae5ec8e-b938-4ceb-9b68-5f3ad1fb06af.png)
