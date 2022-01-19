import requests
import json
import tkinter as tk
import time
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
        self.cities=["Berkeley","Chico","Davis","Irvine","Los Angeles","Merced","Monterey","Riverside","San Diego","San Jose","Santa Barbara","Santa Cruz"]        
        self.citiesAndColleges={
            "Berkeley":"(UCB)",
            "Chico":"(CSU-Chico)",
            "Davis":"(UCD)",
            "Irvine":"(UCI)",
            "Los Angeles":"(UCLA)",
            "Merced":"(UCM)",
            "Monterey":"(CSU-MB)",
            "Riverside":"(UCR)",
            "San Diego":"(UCSD)",
            "San Jose":"(SJSU)",
            "Santa Barbara":"(UCSB)",
            "Santa Cruz":"(UCSC)",}
        self.importedData={}        
        #API Portion
        start=time.time()        
        for i in self.cities:
            self.API_get(i)
        
        end=time.time()
        print("Seconds taken = ",end-start)
        #End API
        
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
    
    def API_get(self,cityName):
        API_Key="44beb371e8fa40677793ab21fba51bb6"
        url=f"http://api.openweathermap.org/data/2.5/weather?q={cityName}&APPID={API_Key}&units=Imperial"
        page=json.loads(requests.get(url).text)
        self.importedData[cityName]=[page['weather'][0]['description'],page['main']['temp']]        
        
    def exit(self):
        if len(self.selectedCities)>0:
            if tkmb.askokcancel("Save","Save your search in a directory of your choice?",parent=self):
                self.saveFile()
        self.destroy()
        
    def writeFile(self,filename,contents):
        file=open(filename,'w')
        for i in contents:
            file.write("City: ")
            file.write(i[0])
            file.write(" Description: ")
            file.write(i[1][0])
            file.write(" Temperature in Degrees Fahrenheit: ")
            file.write(str(i[1][1]))
            file.write("\n")
        file.close()
        tkmb.showinfo("File Saved",f"File weather.txt has been saved to {self.d}",parent=self)
    
    def saveFile(self):
        self.d=tk.filedialog.askdirectory(initialdir='.')
        self.writeFile(os.path.join(self.d,"weather.txt"),self.savedData)
                
    def newDialogueWin(self):
        self.withdraw()
        dialogueObj=dialogueWin(self.citiesAndColleges)
        dialogueObj.CityListBox()
        self.wait_window(dialogueObj)
        if dialogueObj.cityChoice!="zzz":
            self.selectedCities.append(dialogueObj.cityChoice)
            for i in self.importedData:
                if self.selectedCities[-1] in i:
                    self.listBox.insert("end",(i,self.importedData[i]))
                    self.savedData.append([i,self.importedData[i]])                
        
        self.listBox.grid()
        self.deiconify()
    
class dialogueWin(tk.Toplevel):
    def __init__(self,cities):
        super().__init__()
        self.cities=cities
        self.rbChoice=tk.StringVar(self)
        self.cityChoice="zzz"
        
    def CityListBox(self):
        self.minsize(200,200)
        label=tk.Label(self,text="Click on a city to select",fg="black",font=8).grid(row=0,column=0)
        for i in self.cities:
            self.rbChoice.set("abc")
            txt=i,self.cities[i]
            radio=tk.Radiobutton(self,text=txt,variable=self.rbChoice,value=i).grid()
        tk.Button(self,text="Confirm City",command=lambda : self.confirmCity()).grid()
        
    def confirmCity(self):
        self.cityChoice=self.rbChoice.get()
        self.destroy()

if __name__=="__main__":
    main=mainWindow()
    main.protocol('WM_DELETE_WINDOW',main.exit)
    
    main.mainloop()
