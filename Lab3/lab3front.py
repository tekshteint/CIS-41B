'''
Tom Ekshtein, frontend file of Lab3
'''

import tkinter as tk
import sqlite3
import json
import webbrowser

class mainWindow(tk.Tk):
    '''
    Main window class
    '''
    def __init__(self):
        '''Init sets up main window'''
        super().__init__()
        self.title("Movies")
        self.minsize(300,150)
        tk.Label(self,text="Most Anticipated Movies of 2021",fg="blue",font=15).grid(row=0,column=0,padx=50,pady=20,columnspan=4)
        tk.Label(self,text="Search by:",fg="black",font=10).grid(row=1,column=0,sticky="W")
        tk.Button(self,text="Webpage",fg="blue",font=8,command=lambda:self.webButton()).grid(row=1,column=1,pady=20)
        tk.Button(self,text="Main Actor",fg="blue",font=8,command=lambda:self.actorButton()).grid(row=1,column=2)
        tk.Button(self,text="Month",fg="blue",font=8,command=lambda:self.monthButton()).grid(row=1,column=3)
        
        self.mainloop()
    
    def webButton(self):
        '''Handles web search button and it's duties'''
        self.withdraw()
        dialougeObj=dialougeWin(self)
        dialougeObj.byWeb()
        self.wait_window(dialougeObj)
        choice=dialougeObj.movieID
        conn=sqlite3.connect("MovieSQL.db")
        cur=conn.cursor()
        movieNames=[i for i in cur.execute(""" SELECT name,id,link FROM MovieDB ORDER BY name ASC;""")]
        cur.close()
        for i in movieNames:
            if i[1] == choice:
                webbrowser.open(i[2])
            else:
                pass
        self.deiconify()
    
    def actorButton(self):
        '''Handles actor search button and it's duties'''
        self.withdraw()
        dialougeObj=dialougeWin(self)
        dialougeObj.byActor()
        self.wait_window(dialougeObj)
        choice=dialougeObj.movieID
        conn=sqlite3.connect("MovieSQL.db")
        cur=conn.cursor()
        movieNames=[i for i in cur.execute(""" SELECT id,name,director,actor1,actor2,actor3,actor4,actor5,actor6,actor7,actor8,actor9,actor10,actor11 FROM MovieDB ORDER BY id ASC;""")]
        cur.close()
        passableList=[]
        for i in movieNames:
            if i[0] == choice:
                passableList.append(list(movieNames[choice]))
                displayObj=displayWindow(passableList)
                self.wait_window(displayObj)                
            else:
                pass
                          
        self.deiconify()
        
    def monthButton(self):
        '''Handles month search button and it's duties'''
        self.withdraw()
        dialougeObj=dialougeWin(self)
        dialougeObj.byMonth()
        self.wait_window(dialougeObj)
        choice=dialougeObj.movieID
        conn=sqlite3.connect("MovieSQL.db")
        cur=conn.cursor()
        movieNames=[i for i in cur.execute(""" SELECT id,name,director,actor1,actor2,actor3,actor4,actor5,actor6,actor7,actor8,actor9,actor10,actor11,month FROM MovieDB ORDER BY id ASC;""")]
        cur.close()
        monthPrintout=[]
        for i in range(len(movieNames)):
            if int(movieNames[i][-1])==choice:
                monthPrintout.append(list(movieNames[i]))                
            else:
                pass
        if len(monthPrintout)>1:
            displayObj=displayWindow(monthPrintout)
            self.wait_window(displayObj)        
                
        self.deiconify()    
        
        
class dialougeWin(tk.Toplevel):
    '''
    Dialouge Window class
    '''
    def __init__(self,master):
        '''
        Init creates SQL DB link and lists of data from the DB
        '''
        super().__init__()
        self.movieID=99999
        conn=sqlite3.connect("MovieSQL.db")
        cur=conn.cursor()
        self.movieNames=[i for i in cur.execute(""" SELECT name,id FROM MovieDB ORDER BY name ASC;""")]
        self.actorNames=[i for i in cur.execute(""" SELECT actor1,id FROM MovieDB ORDER BY actor1 ASC;""")]
        self.months=[i for i in cur.execute(""" SELECT ID,Month FROM MonthDB ORDER BY Month ASC;""")]
        print(self.actorNames[0][1])
        cur.close()        
        
    def byWeb(self):
        '''Handles websearch dialogue window'''
        self.minsize(200,200)
        frame=tk.Frame(self)
        frame.grid()
        canvas=tk.Canvas(frame)
        canvas.grid()
        label=tk.Label(canvas,text="Click on a movie to select",fg="black",font=8).grid(row=0,column=0)
        scrollBar=tk.Scrollbar(frame,orient="vertical",command=canvas.yview)
        scrollBar.grid(row=0,column=2,sticky="NS",columnspan=2)
        listBox=tk.Listbox(canvas,yscrollcommand=scrollBar.set,height=12,width=50)
        scrollBar.config(command=listBox.yview)
        for j in range(len(self.movieNames)):
            listBox.insert(j,self.movieNames[j][0])

        listBox.bind("<<ListboxSelect>>",lambda x: self.getMovieID(listBox.curselection()))
        listBox.grid()
        
    def byActor(self):
        '''Handles Actor searchdialogue window'''
        self.minsize(200,200)
        frame=tk.Frame(self)
        frame.grid()
        canvas=tk.Canvas(frame)
        canvas.grid()
        label=tk.Label(canvas,text="Click on an actor to select",fg="black",font=8).grid(row=0,column=0)
        scrollBar=tk.Scrollbar(frame,orient="vertical",command=canvas.yview)
        scrollBar.grid(row=0,column=2,sticky="NS",columnspan=2)
        listBox=tk.Listbox(canvas,yscrollcommand=scrollBar.set,height=12,width=50)
        scrollBar.config(command=listBox.yview)
        for j in range(len(self.actorNames)):
            listBox.insert(j,self.actorNames[j][0])

        listBox.bind("<<ListboxSelect>>",lambda x: self.getActorID(listBox.curselection()))
        listBox.grid() 
        
    def byMonth(self):
        '''Handles month search dialogue window'''
        self.minsize(200,200)
        frame=tk.Frame(self)
        frame.grid()
        canvas=tk.Canvas(frame)
        canvas.grid()
        label=tk.Label(canvas,text="Click on a month to select",fg="black",font=8).grid(row=0,column=0)
        scrollBar=tk.Scrollbar(frame,orient="vertical",command=canvas.yview)
        scrollBar.grid(row=0,column=2,sticky="NS",columnspan=2)
        listBox=tk.Listbox(canvas,yscrollcommand=scrollBar.set,height=12,width=50)
        scrollBar.config(command=listBox.yview)
        for j in range(0,12):
            listBox.insert(j,self.months[j][0])

        listBox.bind("<<ListboxSelect>>",lambda x: self.getMonthID(listBox.curselection()))
        listBox.grid()        
    
        
    def getMovieID(self,selection):
        self.movieID=(self.movieNames[selection[0]][1])
        self.destroy()
    def getActorID(self,selection):
        self.movieID=(self.actorNames[selection[0]][1])
        self.destroy()    
    def getMonthID(self,selection):
        self.movieID=(self.months[selection[0]][1])
        self.destroy()
        
class displayWindow(tk.Toplevel):
    '''
    Display Window class 
    '''
    def __init__(self,movie):
        '''Init handles entire class'''
        super().__init__()
        self.movie=list(movie)
        frame=tk.Frame(self)
        frame.grid()
        canvas=tk.Canvas(frame)
        canvas.grid() 
        scrollBar=tk.Scrollbar(frame,orient="vertical",command=canvas.yview)
        scrollBar.grid(row=0,column=2,sticky="NS",columnspan=2)        
        movieList=tk.Listbox(canvas,yscrollcommand=scrollBar.set,height=12,width=50)
        scrollBar.config(command=movieList.yview)
        for i in range(len(self.movie)):
            self.movie[i].insert(0,"Movie:")
            del(self.movie[i][1])
            self.movie[i].insert(2,"Director:")
            self.movie[i].insert(4,"Actors:")
            del(self.movie[i][-1])
            for j in self.movie[i]:
                movieList.insert(tk.END,j)
        
        movieList.grid()
        
        
def main():
    mainWindow()
        
        
if __name__=="__main__":
    main()