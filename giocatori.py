# Import giocatori SERIE A dal sito ufficiale "http://www.legaseriea.it
# Created by Marco Plescia...

#Recupero i paramentri di connessione al DB dal config.json e restituisco la stringa di connessione
def ReadConnectionParamsDB():
    import json
    with open('config.json') as json_data_file:
        data = json.load(json_data_file)

    stringconnection = ("Driver={SQL Server};"
                  "Server=" + data['mssql']['host'] + ";"
                  "Database=" + data['mssql']['db'] + ";"
                  "UID=" + data['mssql']['user'] + ";"
                  "PWD=" + data['mssql']['passwd'] + ";")

    return stringconnection

def giocatori(url, squadra):
    import requests
    import urllib.request
    from bs4 import BeautifulSoup
    import pyodbc 
    cnxn = pyodbc.connect(ReadConnectionParamsDB())
    cursor = cnxn.cursor()

    # Set the URL you want to webscrape from
    #url = 'http://www.legaseriea.it/it/serie-a/squadre/inter/squadra'

    # Connect to the URL
    response = requests.get(url)

    # Parse HTML and save to BeautifulSoup object
    soup = BeautifulSoup(response.text, "html.parser")

    righe = []
    tabella = []
    giocatori = soup.find('table',{'class':'tabella colonne9'})

    num_record = 0
    rows = giocatori.find_all('tr')
    for row in rows:
        cols = row.find_all('td')
        righe = []
        num_record += 1
        num_colonne = 0
        for col in cols :
            num_colonne += 1
            if num_colonne == 7: #Gestione gol subiti per i portieri
                if col.text.strip().isdecimal() == False:
                    chars_to_remove = {40 : None, 41 : None} #caratteri da rimuovere "("  ")"
                    tmp = col.text.strip().translate(chars_to_remove).split(" ")
                    righe.append(tmp[0])
                    righe.append(tmp[1])
                else:
                    righe.append(col.text.strip())
                    righe.append('0')
                num_colonne += 1
            else:
                if col.find('img') is not None:
                    righe.append(col.find('img')['title'])
                else:
                    righe.append(col.text.strip())
        tabella.append(righe)

    # Ricavo il massimo dalla tabella        
    cursor.execute('SELECT CASE WHEN MAX(gi_id) IS NULL THEN 0 ELSE MAX(gi_id) END FROM giocatori')
    for row in cursor:
        codice = row[0]


    for k in range(1,num_record):
        sqlquery = "INSERT INTO giocatori (gi_id, gi_nrmaglia, gi_nome, gi_datanascita, gi_ruolo, gi_nazionalita, \
            gi_partitegiocate, gi_golfatti, gi_golsubiti, gi_ammonizioni, gi_ammespu, gi_espulsioni, gi_squadra) VALUES ("
        codice += 1
        sqlquery = sqlquery + str(codice) + ","
        for i in range(num_colonne):
            if tabella[k][i].isdecimal() == False:
                sqlquery = sqlquery + "'" + str(tabella[k][i]).replace("'","''") + "'"
            else:
                sqlquery = sqlquery + str(tabella[k][i])
            sqlquery = sqlquery + ","
        sqlquery = sqlquery+ "'"+ squadra + "')"
        #print(sqlquery)
        cursor.execute(sqlquery)
        cnxn.commit()


 # Programma principale       
squadre = ['Atalanta','Bologna','Cagliari','Chievo Verona', 'Empoli', 'Fiorentina', 
    'Frosinone', 'Genoa', 'Inter', 'Juventus', 'Lazio', 'Milan', 'Napoli', 'Parma', 
    'Roma ', 'Sampdoria', 'Sassuolo', 'Spal', 'Torino', 'Udinese']

for i in range(0, len(squadre)):
    url = "http://www.legaseriea.it/it/serie-a/squadre/"+ str(squadre[i]).lower().replace(" ","") +"/squadra"
    giocatori(url, squadre[i])