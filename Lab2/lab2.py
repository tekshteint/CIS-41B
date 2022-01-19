'''
Tom Ekshtein
Lab2.py File handles the GUI, and converting all colleges.py matplotlib methods to work in GUI windows of Tkinter.
'''
import matplotlib
matplotlib.use("TkAgg")
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from tkinter import messagebox
import colleges
    
COLUMN=[] #Used for plotting by Data

class mainWindow(tk.Tk):
    '''Main Window That displays mean values and standard deviations found in colleges.py as well as buttons for the User to Interact with'''
    def __init__(self):
        super().__init__()
        self.TOPNUM=15
        try:
            colObj=colleges.Colleges()
        except FileNotFoundError as errorMessage:
            self.withdraw()
            messagebox.showerror("Error",str(errorMessage))
            raise SystemExit()        
        self.colleges=colObj
        
    def closeProgram(self):
        '''For the exit program button'''
        self.destroy()

    def mathDisplay(self):
        return self.colleges.Math()
    
    def newDialogueWin(self):
        '''Hides main window and also calls Dialogue Window class. 
        Will also allow the user to close the dialogue window but keep the main window open in the background'''
        self.iconify()
        test=dialogueWindow()
        
    def exit(self):
        '''Shutdown the program'''
        self.quit()
        
        
class dialogueWindow(mainWindow):
    '''Dialogue Window class. Will open window with radio buttons of the header.csv file and allow
    the user to decide which graph they'd like to see.'''
    def __init__(self):
        super().__init__()
        self.rbCV=tk.IntVar(self)
        for i in self.colleges.headerList:
            tk.Radiobutton(self,text=i,variable=self.rbCV,value=self.colleges.headerList.index(i)).grid()#,command=lambda: self.value_changed(self.rbCV.get())).grid()
        ok=tk.Button(self,text="OK",command=lambda:self.closeDialogue()).grid()
       
    def closeDialogue(self):
        '''Gets ready to graph user choice by appending the radiobutton's value to the COLUMN list and also destroys 
        the current window.'''
        COLUMN.append(self.rbCV.get())
        self.destroy()
        dialoguePlotter()
        
        
class plotWindow(mainWindow):
    '''Plot Window class. Handles all of the plotting and 'handshake' between tkinter and pyplot'''
    def __init__(self,UI,):
        self.UI=UI
        super().__init__()
        self.switch(UI)
        
    def switch(self,UI):
        '''Based off of the button choice this will select the correct method to use.'''
        menuDict={
            1: lambda:self.byCost(),
            2: lambda:self.bySalary(self.TOPNUM),
            3: lambda:self.byData()
            }
        switcher=menuDict.get(UI,lambda:"")
        switcher()
    
    def byCost(self):
        '''Plots method plotAnnual in colleges.py. Part 1C'''
        fig=plt.figure(figsize=(7,7))
        self.title("By Cost")        
        self.colleges.plotAnnual()
        plt.scatter(self.colleges.rank,self.colleges.allAnnuals)
        canvas=FigureCanvasTkAgg(fig,master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()
    
    def bySalary(self,num):
        '''Plots method topAlumniSalaryPlot in colleges.py. Part 1E'''
        fig=plt.figure(figsize=(7,7))
        self.title("By Salary")        
        self.colleges.topAlumniSalaryPlot(num)
        plt.bar(self.colleges.sortedLabelList,self.colleges.sortedPlotList)
        canvas=FigureCanvasTkAgg(fig,master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()
    
    def byData(self):
        '''Plots method plotColumn in colleges.py. Part 1D'''
        fig=plt.figure(figsize=(7,7))
        self.title("By Data",)     
        self.colleges.plotColumn(COLUMN[-1])
        plt.scatter(self.colleges.rank,self.colleges.columns)
        canvas=FigureCanvasTkAgg(fig,master=self)
        canvas.get_tk_widget().grid()
        canvas.draw()
    
    
win=mainWindow()

def dialoguePlotter():
    ''' 'In between' phase of the plotting for 'By Data'. This allows the child class to work with the parent class as needed by
    the lab requirements'''
    plotWindow(3)

def main():
    '''Main function. Creates main window object'''
    win.title("Top Colleges")
    win.minsize(250,200)
    header=tk.Label(win,text="College Lookup",fg="blue",font=15)
    header.grid(row=0,column=2)     
    costButton=tk.Button(win,text="By Cost",width=8, command=lambda : plotWindow(1))
    dataButton=tk.Button(win,text="By Data",width=8, command=lambda : win.newDialogueWin())
    salaryButton=tk.Button(win,text="By Salary",width=8, command=lambda : plotWindow(2))
    quitButton=tk.Button(win,text="Quit Program",width=15, command=lambda : win.exit())
    
    texter=tk.StringVar()
    texter.set(win.mathDisplay())
    textDisplay=tk.Label(win,text=texter.get(),fg="black")
    
    
    costButton.grid(row=1,column=1,padx=5,)
    dataButton.grid(row=1,column=2,padx=5)
    salaryButton.grid(row=1,column=3,padx=12)
    quitButton.grid(row=2,column=2)
    
    textDisplay.grid(row=3,column=0,columnspan=5)
    win.mainloop()
    
if __name__=="__main__":
    main()

'''
Extra Credit Questions:
1)For the most part there is not a strong correlation between rank and student population.
2)Yes, for the most part as the rank decreases so does the total annual cost of the college.
3)Yes, for the most part as the rank decreases, the alumni salary decreases almost exponentially.
4)Yes, for the most part as the rank decreases, the acceptance rate increases. 
5)
    SAT)Yes, as the rank increases the average SAT Upper and Lower scores increase as well.
    ACT)Yes, as the rank increases the average ACT Upper and Lower scores increase as well.
'''