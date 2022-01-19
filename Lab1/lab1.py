'''
Tom Ekshtein
Description: Main file for the program. Contains methods that take the data from topColleges and further manipulates them into being readable and useful data.
'''
import topColleges
import college

PRINTNUM=10

class UI:
    
    def __init__(self):
        TC=topColleges.TopCollege()
        self.topColleges=TC
        if TC.errorRaised==True: #Error handling in case the csv file is not found
            print("Sorry, there was an issue finding the file:",TC.defaultName,"and the program will now close.")
            raise SystemExit()
    
    #part 1B        
    def printTopCollegeStates(self):
        '''Creates an array of state abbreviations including Washington DC. The array is PRINTNUM units wide and enough units tall to satisfy that condition. '''
        finalList=[]
        a=0
        bigList=[i for i in self.topColleges.getAbbreviations()]
        if(len(bigList)%PRINTNUM!=1):
            height=0 
        else:
            height=1
        for i in range((len(bigList)//PRINTNUM)+height):
            littleList=[]
            for j in range(PRINTNUM):
                if a< len(bigList):                
                    littleList.append(bigList[(i*PRINTNUM)+(j)])
                    j+=1
                    a+=1
            finalList.append(littleList)
        for k in finalList:
            print(*k)
            
    #part 1C
    def printSchoolType(self):
        '''Takes a user input of either private or public and returns schools that are of that type using the generator from topColleges.py.'''
        while True:
            try:
                typeChoice=int(input("1. Public\n2. Private\nEnter your choice: "))
                if typeChoice==1 or typeChoice==2:
                    break
            except ValueError:
                print("Please input either 1 for Public or 2 for Private")
        if typeChoice==1:
            generator=(self.topColleges.getType("Public"))
        elif typeChoice==2:
            generator=(self.topColleges.getType("Private"))
        for i in range(PRINTNUM):
            print(f"{i+1}. {next(generator)}")
        while True:
            try:
                stopChoice=input(f"Press the enter key for the next {PRINTNUM} schools or anything else to quit:")
                if stopChoice=="":
                    for i in range(PRINTNUM):
                        print(f"{i+1}. {next(generator)}")
                else:
                    break
            except StopIteration:
                if typeChoice==1:
                    print("You've seen all of the Public colleges in the country.")
                else:
                    print("You've seen all of the Private colleges in the country.")
                break
            
        
    
    #part 1D
    def printAlumniSalary(self):
        '''Takes a user input for a minimum filter for average alumni salary and returns schools that meat that search using the generator from topColleges.py.'''
        while True:
            try:
                salary=int(input("Enter the lowest salary to filter by:\n"))
                break
            except ValueError:
                print("Please enter a valid salary\n") 
        generator=self.topColleges.getAlumniSalary(salary)
        print("Name{:>35} Cost{:>5} Salary".format("","",""))
        blank=""
        counter=0
        while counter<=(len(self.topColleges.rankedList)):
            try:
                line=[(*next(generator))]
                if len(line[1])!=1:
                    print("{:39s} ${:} {:>4}{:}".format(line[0],line[1],"$",line[2]))
                else:
                    print("{:39s} ${:} {:>8}{:}".format(line[0],line[1],"$",line[2]))
            except StopIteration:
                break            
    #part 1E
    def printMatcher(self):
        '''Takes user input for either/or name and state abbreviation(s) and returns schools that fit the criteria using the list returned from topColleges.py.'''
        nameInput=str(input("Please type a name to search for, or press enter to not enter a name\n"))
        stateInput=str(input("Please input state abbreviations. You can enter none or as many as you'd like separated by spaces.\n"))
        listOfStates=stateInput.upper().split(" ")
        if nameInput=="": #Just name is empty
            output=(self.topColleges.matcher(stateList=listOfStates))
            for i in output:
                print(i,"\n")
        elif listOfStates==[""] and nameInput!="": #Just states is empty
            output=(self.topColleges.matcher(Name=nameInput))
            for i in output:
                print(i,"\n")
        else: #neither is empty
            output=(self.topColleges.matcher(Name=nameInput,stateList=listOfStates))
            for i in output:
                print(i,"\n")
        
    def quit(self):
        '''Allows for the user to exit the program through the Main Menu.'''
        print("Exiting program now...")
        raise SystemExit()
    
    def switch(self,choice):
        '''Handles the user's input to the main menu and runs whichever method needs to be ran for that input.'''
        menuDict={
            1:lambda:UI().printTopCollegeStates(),
            2:lambda:UI().printSchoolType(),
            3:lambda:UI().printAlumniSalary(),
            4:lambda:UI().printMatcher(),
            5:lambda:UI().quit()
            }        
        switcher=menuDict.get(choice,lambda:"")
        switcher()
                    
    #part 1F
    def run(self):
        '''Main menu and loop for the user to interact with.'''
        menu=("MAIN MENU - WRITTEN BY TOM EKSHTEIN\n1. States by number of top colleges\n2. Schools by rank and type\n3. Schools by alumni salary\n4. Schools by name and/or state\n5. Quit")
        while True:
            try:
                print(menu)
                choice=int(input("Select an option from the menu: "))                   
                UI().switch(choice)                
            except ValueError:
                print("Please try a valid input 1-5")


def main():
    UI().run()

if __name__=="__main__":
    main()
