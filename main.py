from pathlib import Path

from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage
import tkinter as tk
import threading
import pyautogui
import time
import cv2
from pytesseract import *
from PIL import Image
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
ser = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=ser)
from selenium.webdriver.common.by import By
import mss
import mss.tools

pytesseract.tesseract_cmd = r'...AppData/Local/Programs/Tesseract-OCR/tesseract.exe' # Download pytesseract and link PATH here

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / Path("./assets")

def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)

if __name__ == "__main__":
    
    window = tk.Tk()
    window.geometry("431x550")
    window.configure(bg = "#ECECEC")
    window.title("HUSKYEL1TE'S WZ STATS BOT")
    window.iconbitmap("icon.ico")
    
    run = False
    lock = threading.Lock()
    monitor = threading.Condition(lock)
    
    def webscrape(username, original):
        t = time.time()
    
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options=options)
        driver.get(f'https://cod.tracker.gg/warzone/profile/atvi/{username}/overview')
        page_title = driver.find_elements(By.CLASS_NAME, 'lead')
        
        if not page_title or page_title[0] == "WARZONE STATS NOT FOUND":
            print("WARZONE STATS NOT FOUND - Private profile")
            usernameBox.delete(0, tk.END)
            usernameBox.insert(0, "WARZONE STATS NOT FOUND - Private profile")
        
        else:
            usernameBox.delete(0, tk.END)
            usernameBox.insert(0, original)
            search = driver.find_elements(By.CLASS_NAME, 'value')
            
            if len(search) > 4:
                print("Wins:", search[0].text)
                winsBox.delete(0, tk.END)
                winsBox.insert(0, search[0].text)
                
                print("Win %:", search[1].text)
                winPercentageBox.delete(0, tk.END)
                winPercentageBox.insert(0, search[1].text)
                
                print("Kills:", search[2].text)
                killsBox.delete(0, tk.END)
                killsBox.insert(0, search[2].text)
                
                print("K/D:", search[3].text)
                KD_Box.delete(0, tk.END)
                KD_Box.insert(0, search[3].text)
    
                print("Score/min:", search[4].text)
                scoreMinBox.delete(0, tk.END)
                scoreMinBox.insert(0, search[4].text)
                
            else:
                print("Incorrect name or private profile")
                
                usernameBox.delete(0, tk.END)
                usernameBox.insert(0, original)
                
                winsBox.delete(0, tk.END)
                winsBox.insert(0, "-----")
                
                winPercentageBox.delete(0, tk.END)
                winPercentageBox.insert(0, "-----")
                
                killsBox.delete(0, tk.END)
                killsBox.insert(0, "-----")
                
                KD_Box.delete(0, tk.END)
                KD_Box.insert(0, "-----")
                
                scoreMinBox.delete(0, tk.END)
                scoreMinBox.insert(0, "-----")
                
        elapsed = time.time() - t
        print(elapsed, "Time to webscrape")
        webscrapeBox.delete(0, tk.END)
        webscrapeBox.insert(0, str(round(elapsed, 2)) + " seconds")
        
        driver.close() 
        driver.quit()
    
    def runBot():
        global run
        global lock
        global monitor
        print("Waiting for lock")
        lock.acquire()
        monitor.wait()
        lock.release()
        print("Acquired the lock!")
        
        time.sleep(0.5)
        
        while run:
            coords = pyautogui.locateOnScreen('1ex.png', confidence = 0.24, grayscale = True, region = (696, 938, 339, 36))
            coords1 = pyautogui.locateOnScreen('2ex.png', confidence = 0.24, grayscale = True, region = (696, 938, 339, 36))
            coords2 = pyautogui.locateOnScreen('3ex.png', confidence = 0.24, grayscale = True, region = (696, 938, 339, 36))
            coords3 = pyautogui.locateOnScreen('6ex.png', confidence = 0.24, grayscale = True, region = (696, 938, 339, 36))
    
            if coords or coords1 or coords2 or coords3:
                with mss.mss() as sct:
                    # The screen part to capture
                    region = {'top': 938, 'left': 696, 'width': 339, 'height': 35}
                
                    # Grab the data
                    img = sct.grab(region)
                
                    # Save to the picture file
                    mss.tools.to_png(img.rgb, img.size, output='screenshot.png')
                
                # Enlarge image for more accurate results
                img = cv2.imread('screenshot.png')
                img = cv2.resize(img, dsize=(526, 66), interpolation=cv2.INTER_CUBIC)
                
                # Save image and remove any extra spaces
                cv2.imwrite('screenshot.png', img)
                result = pytesseract.image_to_string(img) # Result variable is what the program thinks the username is after conversion to string
                result = result.rstrip()
                
                # If the username is empty or doesn't have a hashtag, keep scanning/try again
                if result == '' or '#' not in result:
                    continue
                    
                # Special condition for when the username has a clantag, remove the clantag
                if ']' in result:
                    slicing = result.find(']')
                    newUsername = result[slicing+1:]
                    newUsername = newUsername.replace('#', '%')
                    
                    # cod tracker adds a '23' to the links after the percent sign, do the same here
                    pcent = newUsername.index('%')
                    newUsername = newUsername[:pcent+1] + '23' + newUsername[pcent+1:]
                    
                    webscrape(newUsername, result)
                
                # If username doesn't have clantag then it's ready for webscraping
                elif ']' not in result:
                    newUsername = result.replace('#', '%')
                    
                    # cod tracker adds a '23' to the links after the percent sign, do the same here
                    pcent = newUsername.index('%')
                    newUsername = newUsername[:pcent+1] + '23' + newUsername[pcent+1:]
                    
                    webscrape(newUsername, result)
                    
            else:
                continue
            
    threading.Thread(target=runBot).start()
        
    def stopBot():
        global run
        run = False
        
    def startBot():
        global run
        global lock
        global monitor
        print("Starting the bot!")
        run = True
        lock.acquire()
        monitor.notify()
        lock.release()

    canvas = Canvas(
        window,
        bg = "#ECECEC",
        height = 550,
        width = 431,
        bd = 0,
        highlightthickness = 0,
        relief = "ridge"
    )
    
    canvas.place(x = 0, y = 0)
    button_image_1 = PhotoImage(
        file=relative_to_assets("button_1.png"))
    stopButton = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=stopBot,
        relief="flat"
    )
    stopButton.place(
        x=171.0,
        y=440.0,
        width=90.0,
        height=40.0
    )
    
    button_image_2 = PhotoImage(
        file=relative_to_assets("button_2.png"))
    runButton = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=startBot,
        relief="flat"
    )
    runButton.place(
        x=62.0,
        y=440.0,
        width=90.0,
        height=40.0
    )
    
    button_image_3 = PhotoImage(
        file=relative_to_assets("button_3.png"))
    historyButton = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=lambda: print("button_3 clicked"),
        relief="flat"
    )
    historyButton.place(
        x=280.0,
        y=440.0,
        width=90.0,
        height=40.0
    )
    
    canvas.create_text(
        100.0,
        508.0,
        anchor="nw",
        text="Created by marcosmaciel.tech",
        fill="#000000",
        font=("Roboto", 16 * -1)
    )
    
    entry_image_1 = PhotoImage(
        file=relative_to_assets("entry_1.png"))
    entry_bg_1 = canvas.create_image(
        216.0,
        132.5,
        image=entry_image_1
    )
    usernameBox = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    usernameBox.place(
        x=57.0,
        y=111.0,
        width=318.0,
        height=41.0
    )
    
    entry_image_2 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_2 = canvas.create_image(
        121.0,
        215.5,
        image=entry_image_2
    )
    winsBox = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    winsBox.place(
        x=57.0,
        y=194.0,
        width=128.0,
        height=41.0
    )
    
    entry_image_3 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_3 = canvas.create_image(
        121.0,
        298.0,
        image=entry_image_3
    )
    killsBox = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    killsBox.place(
        x=57.0,
        y=276.0,
        width=128.0,
        height=42.0
    )
    
    entry_image_4 = PhotoImage(
        file=relative_to_assets("entry_4.png"))
    entry_bg_4 = canvas.create_image(
        312.0,
        215.5,
        image=entry_image_4
    )
    winPercentageBox = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    winPercentageBox.place(
        x=249.0,
        y=194.0,
        width=126.0,
        height=41.0
    )
    
    entry_image_5 = PhotoImage(
        file=relative_to_assets("entry_5.png"))
    entry_bg_5 = canvas.create_image(
        121.0,
        383.0,
        image=entry_image_5
    )
    scoreMinBox = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    scoreMinBox.place(
        x=57.0,
        y=361.0,
        width=128.0,
        height=42.0
    )
    
    entry_image_6 = PhotoImage(
        file=relative_to_assets("entry_6.png"))
    entry_bg_6 = canvas.create_image(
        312.0,
        383.0,
        image=entry_image_6
    )
    webscrapeBox = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    webscrapeBox.place(
        x=249.0,
        y=361.0,
        width=126.0,
        height=42.0
    )
    
    entry_image_7 = PhotoImage(
        file=relative_to_assets("entry_7.png"))
    entry_bg_7 = canvas.create_image(
        312.0,
        298.0,
        image=entry_image_7
    )
    KD_Box = Entry(
        bd=0,
        bg="#FFFFFF",
        highlightthickness=0
    )
    KD_Box.place(
        x=249.0,
        y=276.0,
        width=126.0,
        height=42.0
    )
    
    canvas.create_text(
        53.0,
        94.0,
        anchor="nw",
        text="Username",
        fill="#000000",
        font=("Arial BoldMT", 13 * -1)
    )
    
    canvas.create_text(
        53.0,
        258.0,
        anchor="nw",
        text="Number of Kills",
        fill="#000000",
        font=("Arial BoldMT", 13 * -1)
    )
    
    canvas.create_text(
        53.0,
        176.0,
        anchor="nw",
        text="Wins",
        fill="#000000",
        font=("Arial BoldMT", 13 * -1)
    )
    
    canvas.create_text(
        246.0,
        259.0,
        anchor="nw",
        text="K/D",
        fill="#000000",
        font=("Arial BoldMT", 13 * -1)
    )
    
    canvas.create_text(
        246.0,
        342.0,
        anchor="nw",
        text="Time to Webscrape",
        fill="#000000",
        font=("Arial BoldMT", 13 * -1)
    )
    
    canvas.create_text(
        246.0,
        176.0,
        anchor="nw",
        text="Win %",
        fill="#000000",
        font=("Arial BoldMT", 13 * -1)
    )
    
    canvas.create_text(
        53.0,
        342.0,
        anchor="nw",
        text="Score/Min",
        fill="#000000",
        font=("Arial BoldMT", 13 * -1)
    )
    
    canvas.create_text(
        70.0,
        36.0,
        anchor="nw",
        text="HUSKYEL1TE'S WZ STATS BOT",
        fill="#000000",
        font=("RobotoRoman Regular", 20 * -1)
    )
    window.resizable(False, False)
    window.mainloop()
