from database_methods import DatabaseMethods
import routefindingalgorithm
import demo
db = DatabaseMethods()
print(db.getNodeFromLocation("Harrison Building"))
print(db.getNodeFromLocation("HMP Exeter"))


#Input the name of the location into the text box 
#get the route ID from the 