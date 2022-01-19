'''
Tom Ekshtein
Description: College class file
'''
class College:
    def __init__(self,name,state,schoolType,cost,alumniSalary):
        self.name=name
        self.state=state
        self.schoolType=schoolType
        self.cost=cost
        if alumniSalary==None or alumniSalary=="":
            self.alumniSalary=0
        else:
            self.alumniSalary=alumniSalary            
        
    def getName(self):
        return self.name
    
    def getState(self):
        return self.state
    
    def getSchoolType(self):
        return self.schoolType
    
    def getCost(self):
        return int(self.cost)
   
    def getAlumniSalary(self):
        return int(self.alumniSalary)
   
    def __str__(self):
        '''returns college objects as readable strings'''
        output1=f"Name: {College.getName(self)}, {College.getState(self)}"
        output2=f"School Type: {College.getSchoolType(self)}"
        output3=f"Cost: ${College.getCost(self):,}"
        output4=f"Alumni Salary: ${College.getAlumniSalary(self):,}"
        newLine=" \n "
        return (output1+newLine+output2+newLine+output3+newLine+output4)
    
