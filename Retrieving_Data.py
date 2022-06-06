import urllib.request, urllib.parse, urllib.error
import json
import sqlite3
import ssl


# Ignore ssl certificate errors
ctx=ssl.create_default_context()
ctx.check_hostname=False
ctx.verify_mode=ssl.CERT_NONE

# Making Connection to the json file through url
url = 'https://data.cdc.gov/resource/n8mc-b4w4.json'
url_handle=urllib.request.urlopen(url, context=ctx)
data=url_handle.read().decode()

print("Retrieved", len(data), "characters")

json_handle=json.loads(data)
line_to_retrieve=int(input("How many rows you wanna retrieve ?"))

# Making connection with the database and creating Tables in Database
conn=sqlite3.connect('database1.sqlite')
cur=conn.cursor()

cur.execute('''DROP TABLE IF EXISTS Covid_Info''')

cur.execute('''CREATE TABLE IF NOT EXISTS Covid_Info
        (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,res_country TEXT, age_group TEXT, sex TEXT)''')


# Entering data into the tables in database1
for i in range(line_to_retrieve):
    age_group_v=json_handle[i]["age_group"]
    sex_v=json_handle[i]["sex"]
    res_country_v=json_handle[i]["res_county"]


    cur.execute('INSERT OR IGNORE INTO Covid_Info(age_group, res_country, sex) VALUES(?,?,?)', (age_group_v, res_country_v, sex_v, ))
conn.commit()
