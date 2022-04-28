import requests
import time
import re
import sys
import os.path

file = open("./token", "r")
TOKEN = file.read()
file.close()
if not os.path.exists('./seen'):
        file = open("./seen", "w")
        file.write("title,text,sentiment\n")
        file.close()
file = open("./seen", "r")
seen = []
for line in file:
        seen.append(line.rstrip('\n'))
file.close()
headers = {'User-Agent': 'Python:wsbsentiment:v0.0.9004 (by /u/kim3-sudo)'}
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

while True:
        # while the token is valid (~2 hours) we just add headers=headers to our requests
        response = requests.get("https://oauth.reddit.com/r/wallstreetbets/random", headers = headers)
        #print(response.json()[0]['data']['children'][0]['data'])

        title = response.json()[0]['data']['children'][0]['data']['title']
        title = title.replace('",', '')
        title = re.sub(r"[^\d\w\s$'\.]", '', title)
        text = response.json()[0]['data']['children'][0]['data']['selftext']
        text = re.sub(r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)", '', text)
        text = text.replace('",', '')
        text = text.replace('\n', ' ')
        text = re.sub(r"[^\d\w\s$'\.]", '', text)
        flair = response.json()[0]['data']['children'][0]['data']['link_flair_richtext'][0]['t']
        flair = re.sub(r"[^\w]", '', flair).lower()[:4]
        if title in seen:
                print("Post already seen. Passing...")
                time.sleep(1.2)
        elif flair == 'meme':
                print('Autoranking based on flair')
                seen.append(title)
                file = open("./seen", 'a')
                file.write('\n' + title)
                file.close()
                time.sleep(1.2)
        elif flair == 'gain':
                print('Autoranking based on flair')
                file = open("./wsbsentiment.csv", 'a')
                file.write('"' + title + '","' + text + '","positive"\n')
                file.close()
                seen.append(title)
                file = open("./seen", 'a')
                file.write('\n' + title)
                file.close()
                time.sleep(1.2)
        elif flair == 'loss':
                print('Autoranking based on flair')
                file = open("./wsbsentiment.csv", 'a')
                file.write('"' + title + '","' + text + '","negative"\n')
                file.close()
                seen.append(title)
                file = open("./seen", 'a')
                file.write('\n' + title)
                file.close()
                time.sleep(1.2)
        else:
                print('Title: ' + title)
                print('Text: ' + text)
                print('Flair: ' + flair)
                rank = str(input('Rank the post:\n1-3 or `n`\tNegative\n4-6 or `k`\tNeutral\n7-9 or `p`\tPositive\n0 or space\tSkip\nx\t\tExit\n>>> '))
                if rank in ['1', '2', '3', 'n']:
                        file = open("./wsbsentiment.csv", 'a')
                        file.write('"' + title + '","' + text + '","negative"\n')
                        file.close()
                        seen.append(title)
                        file = open("./seen", 'a')
                        file.write('\n' + title)
                        file.close()
                elif rank in ['4', '5', '6', 'k']:
                        file = open("./wsbsentiment.csv", 'a')
                        file.write('"' + title + '","' + text + '","neutral"\n')
                        file.close()
                        seen.append(title)
                        file = open("./seen", 'a')
                        file.write('\n' + title)
                        file.close()
                elif rank in ['7', '8', '9', 'p']:
                        file = open("./wsbsentiment.csv", 'a')
                        file.write('"' + title + '","' + text + '","positive"\n')
                        file.close()
                        seen.append(title)
                        file = open("./seen", 'a')
                        file.write('\n' + title)
                        file.close()
                elif rank in [' ', '0']:
                        seen.append(title)
                        file = open("./seen", 'a')
                        file.write('\n' + title)
                        file.close()
                elif rank in ['x']:
                        sys.exit()
                time.sleep(1)