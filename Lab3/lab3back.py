'''
Tom Ekshtein, Backend file of Lab3
'''
#Part A
# https://editorial.rottentomatoes.com/article/most-anticipated-movies-of-2021/
import requests
from bs4 import BeautifulSoup
import json
import re
from string import digits
import sqlite3

page=requests.get("https://editorial.rottentomatoes.com/article/most-anticipated-movies-of-2021/")
#page=requests.get("https://python.org/")

soup= BeautifulSoup(page.content,"lxml")
monthL=['January','February','March','April','May','June','July','August','September','October','November','December']

def webScraper(): 
   '''Main chunk of program. Handles all web-scraping and deals with each unique case/ prepares information from the web for the JSON file. 
   Also uploads to the JSON'''
   found=(soup.body.find("div",class_="articleContentBody"))
   tagLists=[]
   directorKeyWords=["Directed by:","Director:"]
   counter=0
   removeNonAlpha=(re.compile('[^a-zA-Z]'))
   #Creates List of lists containing movie info
   for tag in found.find_all("p"):
      #Checks for movies after website update
      if (tag.find("p")):
         if "Directed by:" in tag.text:
            tagLists.append(list(str(tag.text).replace("\xa0"," ").split("\n")))
            del(tagLists[counter][0],tagLists[counter][0],tagLists[counter][1],tagLists[counter][1])
            tagLists[counter].append(tag.strong.a.get("href"))
            tagLists[counter].append(counter)            
            counter+=1
            
      elif "Directed by:" in tag.text or "Director:" in tag.text:
         tagLists.append(list(str(tag.text).replace("\xa0"," ").split("\n")))
         try:
            tagLists[counter].append(tag.strong.a.get("href"))
         except AttributeError:
            tagLists[counter].append(None)
         counter+=1
   #Changes movie release date to contain only month
   for i in monthL:
      for j in range(0,len(tagLists)):
         if i in tagLists[j][3]:
            tagLists[j][3]=i
         elif "TBD" in tagLists[j][3]:
            tagLists[j][3]="TBD"
   maxActorCount=0            
   #removes directed by or director from list and removes starring from actor list
   #Also converts actor list to tuple
   #Also removes non letters from movie title
   for i in range(0,len(tagLists)):
      for j in directorKeyWords:
         if j in tagLists[i][1]:
            tagLists[i][1]=tagLists[i][1].replace(j,"").strip()
      tagLists[i][2]=tagLists[i][2].replace("Starring:","")
      tagLists[i][2]=list(tagLists[i][2].split(","))
      tagLists[i][0]=str(tagLists[i][0]).translate({ord(k):None for k in digits}).replace("(","").replace(")","").rstrip("%") 
      tagLists[i].append(i)
      actorLen=len(tagLists[i][2])
      if actorLen>maxActorCount:
         maxActorCount=actorLen
      #this adds None to the actor list if there aren't as many as the max
      if len(tagLists[i][2])<11:
         appendCount=11-len(tagLists[i][2])
         for j in range(appendCount):
            tagLists[i][2].append(None)
   #Special names
   tagLists[9][0]="Coming 2 America"
   tagLists[30][0]="F9"
   tagLists[34][0]="Escape Room 2"
   tagLists[61][0]="Jackass 4"
   tagLists[74][0]="The Matrix 4"
   tagLists[75][0]="Sing 2"
   tagLists[76][0]="Downtown Abbey 2"
   tagLists[78][0]="Sherlock Holmes 3"
         
   
   with open("lab3backJSON.json",'w') as file:
      jsonMovie=[]
      for i in range(len(tagLists)):
         jsonMovie.append([tagLists[i][5],tagLists[i][0],tagLists[i][1],tagLists[i][2],tagLists[i][3],tagLists[i][4]])
      json.dump(jsonMovie,file,indent=3)


#PART B
def dbCreator():
   '''
   Handles all SQL programming needed to create the DB and both tables.
   '''
   file=json.load(open("lab3backJSON.json"))
   conn=sqlite3.connect("MovieSQL.db")
   conn.execute("PRAGMA foreign_keys=1")
   cur=conn.cursor()
   cur.execute("DROP TABLE IF EXISTS MovieDB")
   cur.execute("DROP TABLE IF EXISTS MonthDB")
   monthDict={
      'January' :1,
       'February' :2,
       'March' :3,
       'April' :4,
       'May' :5,
       'June' :6,
       'July' :7,
       'August':8 ,
       'September':9 ,
       'October': 10,
       'November': 11,
       'December': 12,
       '(2021)': 13,
       'TBD':13,
       'Opening on: 2021':13
   }
   
   cur.execute('''CREATE TABLE MonthDB(
                   ID VARCHAR PRIMARY KEY,
                   Month INTEGER
               )''')
   #insert="INSERT INTO MonthDB (January,February,March,April,May,June,July,August,September,October,November,December) VALUES(?,?,?,?,?,?,?,?,?,?,?,?)"
   
   cur.execute('''CREATE TABLE MovieDB(
                       name VARCHAR PRIMARY KEY,
                       director TEXT,
                       actor1 TEXT,
                       actor2 TEXT,
                       actor3 TEXT,
                       actor4 TEXT,
                       actor5 TEXT,
                       actor6 TEXT,
                       actor7 TEXT,
                       actor8 TEXT,
                       actor9 TEXT,
                       actor10 TEXT,
                       actor11 TEXT,
                       Month VARCHAR,
                       link TEXT,
                       id INTEGER
                       )
                  ''')
   insert="INSERT INTO MonthDB (ID,Month) VALUES(?,?)"
   for i in monthDict:
      #values=(i,monthDict[i])
      cur.execute(insert,(i,monthDict[i]))
      conn.commit()
   
   
   
   insert="INSERT INTO MovieDB (name,director,actor1,actor2,actor3,actor4,actor5,actor6,actor7,actor8,actor9,actor10,actor11,Month,link,id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
   for i in file:
      cur.execute('SELECT Month FROM MonthDB WHERE ID=?',(i[4],))
      MonthID=cur.fetchone()[0]
      values=(i[1],i[2],i[3][0],i[3][1],i[3][2],i[3][3],i[3][4],i[3][5],i[3][6],i[3][7],i[3][8],i[3][9],i[3][10],MonthID,i[5],i[0])
      cur.execute(insert,values)
   conn.commit() 
   cur.close()

if __name__=="__main__":
   webScraper()
   dbCreator()