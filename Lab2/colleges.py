'''
Tom Ekshtein
Colleges class file. Handles the setup to plot methods and 
imports/reads/manipulates data from csv files as needed
'''
import csv
import numpy as np
import matplotlib.pyplot as plt
import sys
np.set_printoptions(threshold=sys.maxsize)
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib
matplotlib.use("TkAgg")

def returner(func):
    '''Decorator that prints return values'''
    def wrapper(*args,**kwargs):
        rv=func(*args,**kwargs)
        return print(rv)
    return wrapper
                
class Colleges:
    '''Colleges class'''
    def __init__(self):
        self.headerList=[]
        with open("header.csv","r") as header:
            headerReader=csv.reader(header)
            self.headerList=next(headerReader)
            
        with open("scores.csv","r") as scores:
            scoresReader=csv.reader(scores)
            scoresList=list(scoresReader)
            self.scoreArray=np.array(scoresList).astype(int)
                
        with open("colleges.csv","r") as colleges:
            collegeReader=csv.reader(colleges)
            collegeList=list(collegeReader)
            self.collegeArray=np.array(collegeList)
                
    #part B
    def Math(self):
        '''Handles all math needed for Mean values and Standard Deviations'''
        meanTAC=[]
        meanSAT=[]
        meanACT=[]
        
        stdTAC=[]
        stdSAT=[]
        stdACT=[]
                
        for i in range(len(self.scoreArray)):
            if self.scoreArray[i][5]!=-1:
                meanTAC.append(self.scoreArray[i][5])
                stdTAC.append(self.scoreArray[i][5])

            if self.scoreArray[i][8]!=-1:
                meanSAT.append(self.scoreArray[i][8])
                stdSAT.append((self.scoreArray[i][8]))
                
            if self.scoreArray[i][10]!=-1:
                meanACT.append(self.scoreArray[i][10])
                stdACT.append(self.scoreArray[i][10])
                
        return("Mean Total Annual Cost: "+str(int(np.mean(meanTAC).round()))+", Standard Deviation: "+str(int(np.std(stdTAC).round()))+"\nMean SAT Lower: "+str(int(np.mean(meanSAT).round()))+", Standard Deviation "+str(int(np.std(stdSAT).round()))+"\nMean ACT Lower: "+str(int(np.mean(meanACT).round()))+", Standard Deviation: "+str(int(np.std(stdACT).round())))
        
    #part C
    @returner
    def plotAnnual(self):
        '''Plots the annual cost of all colleges with avaliable data'''
        allAnnuals=[i[5] for i in self.scoreArray]
        rank=[i for i in range(len(allAnnuals))]
        self.allAnnuals=allAnnuals
        self.rank=rank
        plt.title("Annual Cost of the Top 650 Colleges")
        plt.xlabel("College by Rank (0-650)")
        plt.ylabel("Annual Cost in Dollars")
        return min(allAnnuals),max(allAnnuals)
        
        
    #Part D
    @returner
    def plotColumn(self,column):
        '''Plots data as top colleges vs header category of the user's choice for all available data'''
        plotList=[i[column] for i in self.scoreArray if i[column]!=-1]
        rank=[i for i in range(len(plotList))]
        plotArr=np.array(plotList)
        self.rank=rank
        self.columns=plotArr
        plt.title(self.headerList[column]+" plotted from maximum value to lowest value")
        plt.xlabel("650 of the Top Colleges")
        plt.ylabel(self.headerList[column])
        return min(plotArr),max(plotArr)
    
    #Part E
    @returner
    def topAlumniSalaryPlot(self,number):
        '''Plots the alumni salaries of the top colleges up to X number where the user picks X
        sorted by the salary from highest to lowest.'''
        #Data Set creation
        numRange=[i for i in range(number)]
        plotList=[] #Plotlists are numbers
        labelList=[] #LabelLists are college names
        plotListFull=[i[6] for i in self.scoreArray]
        labelListFull=[i[1] for i in self.collegeArray]
        for i in range(number):
            plotList.append(plotListFull[i])
            labelList.append(labelListFull[i])
        #Sorting of lists
        zippedLists=zip(plotList,labelList)
        sortedZip=sorted(zippedLists)
        
        sortedLabelList=[i for j,i in sortedZip]
        sortedPlotList=[i for i,j in sortedZip]
        
        sortedPlotList.reverse()
        self.sortedPlotList=sortedPlotList
        self.sortedLabelList=sortedLabelList
        
        #Graphing
        plt.bar(sortedLabelList,sortedPlotList)
        plt.xticks(numRange,labelList,fontsize=8,rotation=90)
        plt.title("Top Alumni Salaries from the first "+str(number)+" schools")
        plt.xlabel("Schools")
        plt.ylabel("Average Alumni Salary in Dollars")
        plt.tight_layout()
        plt.axis(ymin=100000)        
        return min(sortedPlotList),max(sortedPlotList)
        
