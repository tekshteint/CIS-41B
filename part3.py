'''
Tom Ekshtein
Lab file with multithreading
Weather API project
'''
import requests
import json
import tkinter as tk
import time
import threading
import tkinter.messagebox as tkmb
import tkinter.filedialog
import os
        
class mainWindow(tk.Tk):
    '''
    Main window class
    '''
    def __init__(self):
        '''Init sets up main window'''
        super().__init__()
        self.savedData=[]        
        self.selectedCities=[]
        self.cities=["Berkeley",'Buttonwillow',"Chico","Davis","Irvine","Los Angeles","Merced","Monterey","Riverside","San Diego","San Jose","Santa Barbara","Santa Cruz"]        
        self.citiesAndColleges={
            "Berkeley":"(UCB)",
            "Buttonwillow":"BW",
            "Chico":"(CSU Chico)",
            "Davis":"(UCD)",
            "Irvine":"(UCI)",
            "Los Angeles":"(UCLA)",
            "Merced":"(UCM)",
            "Monterey":"(CSU MB)",
            "Riverside":"(UCR)",
            "San Diego":"(UCSD)",
            "San Jose":"(SJSU)",
            "Santa Barbara":"(UCSB)",
            "Santa Cruz":"(UCSC)",}
        self.importedData={}
        '''
        Loop from part 1
        The rest of the programs are relatively the same
        so self.API_get works for all of them
        
        for i in self.cities:
            self.API_get(i)
        '''

        self.title("Movies")
        self.minsize(300,150)
        self.title("Welcome to the Weather App")
        tk.Label(self,text="Weather app for Tom's 12 favorite CA college cities",fg="blue",font=15).grid(row=0,column=0,padx=50,pady=20,columnspan=4)
        tk.Button(self,text="Choose a city",command= lambda:self.newDialogueWin()).grid(row=1,column=0)
        self.frame=tk.Frame(self)
        self.frame.grid()
        self.canvas=tk.Canvas(self.frame)
        self.canvas.grid()
        self.scrollBar=tk.Scrollbar(self.frame,orient="vertical",command=self.canvas.yview)
        self.scrollBar.grid(row=0,column=2,sticky="NS",columnspan=2)
        self.listBox=tk.Listbox(self.canvas,yscrollcommand=self.scrollBar.set,height=12,width=100)
        self.scrollBar.config(command=self.listBox.yview)
        
        start=time.time()        
        self.threads=[]
        for i in range(len(self.cities)):
            t=threading.Thread(target=self.API_get, args=(self.cities[i],))
            self.threads.append(t)
            t.start()
        for i in self.threads:
            t.join()
        end=time.time()
        print("Seconds taken = ",end-start)
    
    def exit(self):
        ''' Exit function called when the main window is exited'''        
        if len(self.selectedCities)>0:
            if tkmb.askokcancel("Save","Save your search in a directory of your choice?",parent=self):
                self.saveFile()
        self.destroy()    
        
    def writeFile(self,filename,contents):
        '''Writes contents into the weather.txt file'''
        file=open(filename,'w')
        for i in contents:
            file.write(i)
        tkmb.showinfo("File Saved",f"File weather.txt has been saved to {self.d}",parent=self)
    
    def saveFile(self):
        '''finds filepath that the user wants and calls the writeFile method'''        
        self.d=tk.filedialog.askdirectory(initialdir='.')
        self.writeFile(os.path.join(self.d,"weather.txt"),self.savedData)
        
    
    def API_get(self,cityName):
        '''Handles API calls'''
        API_Key="44beb371e8fa40677793ab21fba51bb6"
        url=f"http://api.openweathermap.org/data/2.5/weather?q={cityName}&APPID={API_Key}&units=Imperial"
        page=json.loads(requests.get(url).text)
        self.importedData[cityName]=[page['weather'][0]['description'],page['main']['temp']]        
        
    def newDialogueWin(self):
        '''Creates the dialogue window and updates the main window's listbox'''
        self.withdraw()
        dialogueObj=dialogueWin(self.citiesAndColleges)
        dialogueObj.CityListBox()
        self.wait_window(dialogueObj)
        if dialogueObj.cityChoice!="zzz":
            self.selectedCities.append(dialogueObj.cityChoice)
            for i in self.importedData:
                txt=(f"City:{i} Description: {self.importedData[i][0]} Temperature in Degrees Fahrenheit: {self.importedData[i][1]}")                
                if self.selectedCities[-1] in i: 
                    self.listBox.insert("end",txt)
                    self.savedData.append(txt)                        

        self.listBox.grid()
        self.deiconify()
    
class dialogueWin(tk.Toplevel):
    '''Dialogue Window class'''    
    def __init__(self,cities):
        '''init inititalizes the dialogue window'''
        super().__init__()
        self.cities=cities
        self.rbChoice=tk.StringVar(self)
        self.cityChoice="zzz"
        
    def CityListBox(self):
        '''Handles the radiobuttons for each city in the dialogue window'''
        self.minsize(200,200)
        label=tk.Label(self,text="Click on a city to select",fg="black",font=8).grid(row=0,column=0)
        for i in self.cities:
            self.rbChoice.set("abc")
            txt=(f"{i} {self.cities[i]}")
            radio=tk.Radiobutton(self,text=txt,variable=self.rbChoice,value=i).grid(sticky="W")
        tk.Button(self,text="Confirm City",command=lambda : self.confirmCity()).grid()
        
    def confirmCity(self):
        '''"Saves" the user's choice of city and destroys the dialogue window'''        
        self.cityChoice=self.rbChoice.get()
        self.destroy()

if __name__=="__main__":
    main=mainWindow()
    main.protocol('WM_DELETE_WINDOW',main.exit)
    
    main.mainloop()
