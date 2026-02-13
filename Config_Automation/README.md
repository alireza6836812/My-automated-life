## Overview
the focus of this project is on crating an automation for making the internet connection stable and usable via using proxies. The project has three stages whihc each of them have theirs own files:

#### 1- Config Scrapper
This part woking on scrapping proxies via different sources. right now there are two sources provided in this part:
1- Telegram Channels:
in this part you have to create a .session file based on the information of your telegram account.
first you need to visit https://my.telegram.org/ and get your api id and api hash and then put them in the text file called Info.txt.
(if you are an Iranian user, maybe this part needs to be done by someone outside the country, because the iranian ip is filtered and also the site dont let people with proxy longging in)
after giving needed information to the code like your phone number, code and login password, you can create your session and use it to scrape data from Telegram.
2- Config Provider Servers
these servers are created by other people using othe ways to scrape configs. right now there is just one server which is trusted and safe.
3- Costum Configs
you can put the link of your costum configs to use them as another source for connection.
after scarraping all the neesed configs, they will be saved in excel file called 1)Scrapped_VMESS_Configs.xlsx
in the next step the json format of those links will be created to use by other applications like xray.
the json format of files will be saved in a excel file called 2)Scrapped_VMESS_Configs_json.xlsx

#### 2- Config Test
in this part the scrapped configs will be test in two state, fist tcp config to seperate valid and unvalid configs from eachother and second full test on these websites:
youtube
telegram
instagram
chatgpt
these websites are the ones which is neccesary for most of the people, so if a proxy can open them maybe it can open other websites too.
after testing the vmess configs, they will be saved in a excel file called 

#### 3- Conifg Connection
in the last part the best config will be choose and make a connection to it by using xray and redsocks.
warnning: before running this part make sure the scripts in code has no sideeffect on your system and other tools which you are using.

## Requirenments
1- Python
2- Redsocks
3- xray
4- pandas
5- Requests
6- socks
7- re
9- telethon
10- base64
11- json
12- urllib
13- json
14- socket
15- time
16- asyncio
17- subprocess
18- tempfile
19- copy
20- playwright
21- Linux Distribution(Ubuntu)

## How to use
first create .session file described in the previous parts.
second put all of the codes in a time cyle to run automaticly, for this part I used Cron. you can use whatever you want.
then enjoy.
for stoping the process and restarting the network setting there is another code whihc you can run and disable past settings.
## Lmitations
1- rihgt now only vmess configs are available
2- the code is developed to use on ubuntu
3- low speed, I need to work on its preformance which can be suitable for phones too
4- for the first time you need to use a proxy or other vpn to scrape data from telegram channel. other times there is no need for this part/.
## current stage and furute developments
if you have an ubuntu and telegram account and internet connection, everything works well.
for phones you can Install Termux and use the codes.
also in future developments we will have:
1- other type of configs like vless, trojan and ...
2- better performance
