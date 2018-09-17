import requests
from bs4 import BeautifulSoup
from firebase import firebase
import random
firebase = firebase.FirebaseApplication('https://pesdatabase-d2d99.firebaseio.com/')

def player_scrap(link):
    url = link
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, "html.parser")
    playerMainTable = soup.find('table',{'class':'player'})
    tr1 = playerMainTable.findAll('tr')
    #td1 = tr1[0].find_all('td')
    allTables = tr1[0].find_all('table')
    #print(allTables)
    '''
    table_td = td1[0].find('table')
    allRowsTable = table_td.find_all('tr')    
    for i in allRowsTable:
        try:
            lable = i.find('th')
            value = i.find('td')
            print(lable.text, " ", value.text)
        except:
            break
    '''
    main_dict = {}
    for tables in allTables:
        dict = {}
        all_rows = tables.find_all('tr')
        for i in all_rows:
            try:
                lable = i.find('th')
                value = i.find('td')
                print(lable.text, " ", value.text)
                dict[lable.text] = value.text
                #result = firebase.put('/'+unique_num,lable.text,value.text)
            except:
                break
            main_dict.update(dict)

    result = firebase.post('/players',main_dict)
    print(result)


url = 'http://pesdb.net/pes2019/'
source_code = requests.get(url)
plain_text = source_code.text
soup = BeautifulSoup(plain_text, "html.parser")

tables = soup.find('table',{'class': 'players'})

tr = tables.find_all("tr")
for t in tr:
    td = t.find_all("td")
    #row = [i.text for i in td]
    row = []
    c = 0
    for i in td:
        row.append(i.text)
        if (c == 1):
            link = i.a.get('href')[1:]
            player_scrap("http://pesdb.net/pes2019"+link)
        c = c + 1
    print(row)


