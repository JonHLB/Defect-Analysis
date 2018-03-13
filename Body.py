import pandas as pd
import numpy as np

defectdf = pd.read_csv("assemblytest3.csv")
moduleNamedf = pd.read_csv("ModuleName.csv")

defectdf['WeekEnding'] = pd.to_datetime(defectdf.WeekEnding)
defectdf2 = defectdf.dropna(how='any', axis=0)
#newTable = pd.DataFrame(columns = defectdf.columns)
defectnp = defectdf.values #make pandas df to numpy array
moduleNamesnp = moduleNamedf.values # make pandas df to numpy array

defectnp2 = defectdf2.values
#______________________________________________________
"""
Reference Designator Loop Parsing
    -pass individual values from np array of defects
    -find how many elements to loop through by seeing shape of matrix
    -find how many components in reference designator (space separated)
    -create nested loop for # of elements and # of components per entry
    -select useful columns for new data set/structure (optional)
    -close loop and return new np array with separated/parsed reference designators
"""

defectdf2lastelem = moduleNamesnp.shape[0]
array1 = []
array2 = []
lastelem2 = defectnp2.shape[0]

for x in range (0, lastelem2): #loop for each row entry in dataset
    strcount = defectnp2[x, 12].count(' ')
    for y in range (0, strcount+1): #loop for each reference designator found
        
        splitstr = defectnp2[x, 12].split(' ')
        array2.append([defectnp2[x, 0], defectnp2[x, 1], defectnp2[x, 2], 
                      defectnp2[x, 3], defectnp2[x, 7], defectnp2[x, 9],
                      defectnp2[x, 10], defectnp2[x, 11], splitstr[y],
                      defectnp2[x, 13]])

array2[1]

#__________________________________________________________

"""
Make a dataframe with peeling defects based on individual reference designators parsed out of the 'defectdf' dataframe
    -create data structure by defining column names column names
    -create defectdf by using np parsed array2
    -replace any blank space/null values with NaN
    -dropna with pandas
    -filter and create dataframe with only peeling defects --> peeldf
"""


columns = ['ID', 'ProductionModuleID', 'Module', 'SerialNo', 'Weekending', 'DefectCategory', 'DefectDescription', 'Comment', 'RefDesig', 'Source']

defectdf2 = pd.DataFrame(data = array2, columns=columns)
defectdf2['RefDesig'].replace('', np.nan, inplace=True)
defectdf2.dropna(subset=['RefDesig'], inplace=True)

peeldf = defectdf2[(defectdf2['DefectDescription'] == 'Peeling Pad')]

peeldf

#____________________________________________________________
"""
Data Visualization
Using seaborn, create heatmap of quantity or DPU for peeling on certain productline
Display pareto top 5 productlines
Break down 5 productlines parts into 5 individual graphs of components

Troubles, pivot table has multiple index objects, two level indexes, 
need to go down to 1st series(Comments)
then sort by another 2nd series (Peeling Pad)
"""

df_table = peeldf.pivot_table(index='Module', columns='DefectDescription', aggfunc='count')
df_table

peelseries = df_table.Comment.sort_values(by=['Peeling Pad'], axis = 0, ascending = False)
peelseries.head()

#_____________________________________________________________

"""
Create Peeling Pad breakdown
pivot table must select module name from top 5
#####NEED TO LINK PN TO REFERENCE DESIGNATORS FROM BOM --> RELATIONAL DATABASE######
"""

#call index of top peeling series aggregation
#moduleNames: peelseries.index[0]
#filter: pivot_table(index = 'RefDesig', columns='Source', aggfunc='count').Comment.sort_values(by=['Bonding'], axis=0, ascending = False) 

#fil = pivot_table(index = 'RefDesig', columns='DefectCategory', aggfunc='count').Comment.sort_values(by=['Bonding'], axis=0, ascending = False) 


peel1df = peeldf[(peeldf['Module'] == peelseries.index[0])]
peel2df = peeldf[(peeldf['Module'] == peelseries.index[1])]
peel3df = peeldf[(peeldf['Module'] == peelseries.index[2])]
peel4df = peeldf[(peeldf['Module'] == peelseries.index[3])]
peel5df = peeldf[(peeldf['Module'] == peelseries.index[4])]

peeeldf = peel1df.pivot_table(index = 'RefDesig', columns='DefectCategory', aggfunc='count').Comment.sort_values(by=['Bonding'], axis=0, ascending = False) 

peeeldf

# peeeldf1 = peeeldf.reset_index()

# peeeldf1

#____________________________________________________________________

"""
Link to PN Reference Designator From BOM 
Relational Database using dictionary replacement from two datasets: peel1df & testbomdf
BOM is TESTBOM.xlsx
Problems: 
tried using merge, joins but those added columns
tried using map but only returned series and did not map inplace for the original series/df

next to try: df.to_dict(arg)
"""
from pandas import ExcelWriter
from pandas import ExcelFile

testbomdf = pd.read_excel('TESTBOM.xlsx', sheetname='Sheet1')
dict1 = testbomdf.set_index('RefDesig')
testbomnp = testbomdf.values
testbomnp

x = peeldf[(peeldf['Module'] == 'SFM')]

x

