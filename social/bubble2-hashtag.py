#this is needed to convert the source code to a list with the texts
input_texts = open("C:/Users/Nicolette/djangogirls/django101/social/htmlcode.txt", "r").readlines()
#input_texts = open("C:/Users/Laura/Dropbox/Studie spullen/Master/Social Web/htmlcode.txt", "r").readlines()
texts = []
text = ""
post = False
date_found = False
dates = []

MONTHS = ['january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']

def create_date(line):
    parted = line.strip().split(',')
    month = parted[0].split()[2]
    for i in range(len(MONTHS)):
        if MONTHS[i] == str(month).lower():
            month = i + 1
    day = int(parted[0].split()[3])
    year = int(parted[1].strip())
    dates.append([month, day, year])
    
for line in input_texts:
    if line.find("<p class='lead'>") != -1:
        post = True
        text = ""
    if post:
        stripped_line = line.strip().replace("<p class='lead'>", "").replace("</p>", "")
        text += stripped_line
    if line.find("</p>") != -1 and post:
        post = False
        texts.append(text)
    if line.find("<h4 class='small'>") != -1:
        date_found = True
    elif date_found:
        create_date(line)
        date_found = False

#here we create a csv file with the output of sentiment analysis
import csv
import subprocess
import json

c = open("C:/Users/Nicolette/djangogirls/django101/social/static/social/data-hashtag.csv", "wb")
csv = csv.writer(c)
csv.writerow(["Hashtag", "Positive", "Negative", "Neutral", "Day", "Month", "Year"])

#extract hashtags and texts
counter = 0
for text in texts:
    hashtags = []
    message = ""
    for word in text.split():
        if word[0] == "#":
            str = word.lower()
            if str.endswith(",") or str.endswith("!") or str.endswith("."):
                str = str[:-1]
            hashtags.append(str)
        else:
            message += word + " "
    
    #sentiment analysis on text
    command = 'curl -d "text=%s" http://text-processing.com/api/sentiment/' %message
    output = subprocess.check_output(command, shell=True)
    output2 = json.loads(output)
    results = output2.get('probability')
    for hashtag in hashtags:
        csv.writerow([hashtag, results.get('pos'), results.get('neg'), results.get('neutral'), dates[counter][1], dates[counter][0], dates[counter][2]])
    
    counter += 1

c.close()
    
   
        
    
