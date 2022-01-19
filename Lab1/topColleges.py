'''
Tom Ekshtein
Description: topColleges class file. Handles data collection and manipulation as needed so objects can be used as needed.
'''
def lenTest(func):
    '''Decorator method. Used to check length of other methods.'''
    def wrapper(*args,**kwargs):
        rv=func(*args,**kwargs)
        try:
            print(len(rv),"{:>30}#Printed by Decorator".format(""))
            return rv
        except TypeError:
            print("0{:>30}#Printed by Decorator".format(""))
            return rv
    return wrapper    

import csv
import college

class TopCollege:
    defaultName ="topcolleges.csv"
  
   #part 1b
    def __init__(self,filename=defaultName):
        '''Init creates needed data structures for entire program, along with opening the csv file and reading it.'''
        self.rankedList=[] #College names ordered by rank (so decending the file)        
        self.statesDict={} #State abbreviations as keys, values are list of colleges in each state
        self.errorRaised=False #Will be used to handle FileNotFoundError
        self.sortedStatesDict=[] #Will be used to sort self.statesDict for the getter method
        try:
            with open(filename,"r") as file:
                fileReader=csv.reader(file)
                next(fileReader,None)
                for row in fileReader:
                    collegeObj=college.College(row[1],row[3],row[4],row[9],row[10])
                    self.rankedList.append(collegeObj)
                    if row[3] not in self.statesDict:
                        self.statesDict[row[3]]=[]
                    self.statesDict[row[3]].append(collegeObj)
        except FileNotFoundError:
            self.errorRaised=True
        for i in sorted(self.statesDict, key=lambda i: len(self.statesDict[i]), reverse=True):
            self.sortedStatesDict.append(i)        
            
    #part 1c
    @lenTest
    def getAbbreviations(self): 
        '''Returns the sorted states dictionary to be used later.'''
        return self.sortedStatesDict
    
    #part 1d
    @lenTest
    def getType(self,schoolType):
        '''creates and returns a generator of schools being either private or public.'''
        generator= (self.rankedList[colObj].name for colObj in range(len(self.rankedList)) if schoolType == self.rankedList[colObj].schoolType)
        return generator
            
    
    #part 1e                   
    @lenTest
    def getAlumniSalary(self,alumniSalary):
        '''creates and returns a generator of schools with the info being school name, average annual cost, and average alumni salary'''
        generator= ([self.rankedList[colObj].name,self.rankedList[colObj].cost,self.rankedList[colObj].alumniSalary] for colObj in range(len(self.rankedList)) if alumniSalary <= int(self.rankedList[colObj].alumniSalary))
        
        return generator
    
    #part 1f
    @lenTest
    def matcher(self, Name="xx",stateList=None):
        '''Takes user input and finds schools that match the criteria. Checks for either school names containing X, schools in state Y, or a combination of both.'''
        if not stateList: stateList=["None"]
        output=[]
        for j in self.rankedList:
            for k in stateList:
                if k in j.state and Name=="xx": #Deals with just stateList
                    output.append(j)
                elif k in j.state and Name.upper() in str(j.name).upper(): #Deals with both Name and State
                    output.append(j)
                elif Name.upper() in str(j.name).upper() and k=="None": #Deals with just Name
                    output.append(j)
        return (output)

                    
