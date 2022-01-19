import sqlite3
import json
      
#PART B
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
    '(2021)': 0,
    'TBD':0,
    'Opening on: 2021':0
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
                    link TEXT
                    )
               ''')
insert="INSERT INTO MonthDB (ID,Month) VALUES(?,?)"
for i in monthDict:
    #values=(i,monthDict[i])
    cur.execute(insert,(i,monthDict[i]))
    conn.commit()
    
    
    
insert="INSERT INTO MovieDB (name,director,actor1,actor2,actor3,actor4,actor5,actor6,actor7,actor8,actor9,actor10,actor11,Month,link) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
for i in file:
    cur.execute('SELECT Month FROM MonthDB WHERE ID=?',(i[4],))
    MonthID=cur.fetchone()[0]
    #print(type(MonthID))
    values=(i[1],i[2],i[3][0],i[3][1],i[3][2],i[3][3],i[3][4],i[3][5],i[3][6],i[3][7],i[3][8],i[3][9],i[3][10],MonthID,i[5])
    cur.execute(insert,values)
conn.commit() 
cur.close()
