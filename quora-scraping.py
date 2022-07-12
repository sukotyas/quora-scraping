from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import time
from datetime import datetime

driver = webdriver.Chrome("C:\jupyter\webdrivers\chromedriver.exe")

#specify which topics to grab
topics = ["literasidansastra", "seputarduniapendidikan", "yukbahasbuku", "curhatanmahasiswa", "mistisdanlegendaurban", "siswaambis", "richdadmindset", "ilmubaruhariini", "tipsdantrikkehidupan", "ruangpsikologianak", "ruangdokter", "mindandselfcontrol", "belajar-dari-indonesia-dan-dunia", "semuatentangsejarah", "kkyt", "psikologicinta", "komunitasliterasicerdas", "ceritaaku", "matamatika"]


for topic in topics:

    #initiate empty arrays to store questions, links, and number of answer for the question
    questions = []
    links = []
    answers = []

    #open designated URL based on the topics
    driver.get("https://"+topic+".quora.com/questions")

    #wait for 5 seconds for the automated browsers to load the whole contents including the javascripts.
    #this depends on your internet connection, you can reduce the value if you have faster internet connection
    time.sleep(5)

    #specify waiting time before scrolling again
    #again, you can reduce the following value if you have faster internet connection
    waiting_time = 5 #in seconds
    prev_height = 0

    continue_scroll = 1
    while(continue_scroll == 1):
        #perform scrolling action to bottom of the page
        driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        #get the window height after the scroll
        height = int(driver.execute_script("return document.documentElement.scrollHeight"))

        #if the current height is different than the previous height, it means there are new questions displayed
        #if they are the same, means the window has reached the maximum displayed contents. therefore stop scrolling and grab the data
        if(prev_height != height):
            prev_height = height
            continue_scroll = 1
        else:
            continue_scroll = 0

        #wait for the contents to be displayed in the window
        time.sleep(waiting_time)

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    for a in soup.findAll('a', href = True, attrs = {'target':'_blank'}):
        q = a.find('span', attrs = {'class': 'q-box qu-userSelect--text'})
        questions.append(q)
        links.append(a.get('href'))
        answers.append(a.text)

df = pd.DataFrame({'Questions':questions,'Links':links, 'Answers:':answers}) 
#df.to_csv('export\questions-'+topic+'-'+str(datetime.now().hour)+'-'+str(datetime.now().minute)+'.csv', index=False, encoding='utf-8')
df.to_csv('export\questions-'+str(datetime.now().hour)+'-'+str(datetime.now().minute)+'.csv', index=False, encoding='utf-8')
