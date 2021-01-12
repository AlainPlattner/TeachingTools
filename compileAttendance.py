# Creates one compiled attendance file for a specific Lecture

# Provide lecture name as command line input

import sys
import os
import pandas as pd
#import numpy as np

lecture = sys.argv[1]


Zoomfolder='Zoom'
Panoptofolder='Panopto'
InPersonfolder='InPerson'
GCfolder='GC'

outfolder='Compiled'

##### Load all three Lectures, create one file with all last names, first names, user names, and if they attended in any way (1 for yes, 0 for no)

compiled = pd.DataFrame(columns = ['LastName','FirstName','UserName','Attended'])

# First read in Blackboard GC to get the name lists 
### Read in the current Blackboard grade center
for root, dirs, files in os.walk(GCfolder):
    for filename in files:
        # Go through all to get the latest one?
        # Try not to have more than one
        gc = pd.read_csv(os.path.join(root,filename))

if len(files)>1:
    print('Error!!! You either have more than one grade center file in the folder, or you are editing the grade center file.')
      
compiled['LastName'] = gc['Last Name']
compiled['FirstName'] = gc['First Name']
compiled['UserName'] = gc['Username']
compiled['Attended'] = 0
        
########### Read Zoom ##########
zoom = pd.read_csv(os.path.join(Zoomfolder,lecture+'.csv'))
# Extract User Name: Remove last 15 characters from string
uname = zoom["User Email"].str[:-15]
splitname = zoom["Name (Original Name)"].str.split(" ", n = 1, expand = True) 
fname = splitname[0]
lname = splitname[1]

# Now check if the username can be found in the Attended list.
# If yes: set "Attended" to 1.
idx = compiled['UserName'].isin(uname)
compiled.loc[idx,'Attended']=1

# Then check if first and last name can be found.
# If yes, then set "Attended" to 1
idx = compiled['LastName'].isin(lname) & compiled['FirstName'].isin(fname)
compiled.loc[idx,'Attended']=1

# Now identify the ones you couldn't find. First and last name
idx1 = uname.isin(compiled['UserName'] )
idx2 = fname.isin(compiled['FirstName']) & lname.isin(compiled['LastName'])
idx = ~(idx1 | idx2)

notFound = pd.concat([fname[idx],lname[idx],uname[idx]], axis=1)
notFound.to_csv('notFound_Zoom'+lecture+'.csv',index=False)


########### Read Panopto ##########
panopto = pd.read_csv(os.path.join(Panoptofolder,lecture+'.csv'))
#unameTest = panopto["Email"].str[:-15]
uname = panopto["UserName"].str[11:]
#print(uname.equals(unameTest))
#splitname = panopto["Name"].str.split(" ", n = 1, expand = True) 
#fname = splitname[0]
#lname = splitname[1]
# This list should contain the usernames correctly
idx = compiled['UserName'].isin(uname)
compiled.loc[idx,'Attended']=1
# There shouldn't be any unknown students as this is linked with Blackboard


########### Read In-Person ##########
inPerson = pd.read_csv(os.path.join(InPersonfolder,lecture+'.csv'))
# This list should contain the usernames correctly
idx = compiled['UserName'].isin(inPerson['User Name'])
compiled.loc[idx,'Attended']=1
# There shouldn't be any unknown students as this is linked with Blackboard



########### Write out Compiled ###############
compiled.to_csv(os.path.join(outfolder,lecture+'.csv'))






