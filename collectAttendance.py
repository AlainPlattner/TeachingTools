# Load all the files in "CompiledFixed", combine them, calculate their average,
# then put into a single file to upload

import os
import pandas as pd

GCfoldername = 'GC'
Compiledfoldername = 'CompiledFixed'

### Read in the current Blackboard grade center
for root, dirs, files in os.walk(GCfoldername):
    for filename in files:
        # Go through all to get the latest one?
        # Try not to have more than one 
        gc = pd.read_csv(os.path.join(root,filename))

        
### Create new pandas frame
completion = pd.DataFrame(columns = ['Username'])
completion['Username'] = gc['Username']

### Read all files in the folder Compiledfoldername
for root, dirs, files in os.walk(Compiledfoldername):
    for filename in files:
        record = pd.read_csv(os.path.join(Compiledfoldername,filename))

        # Create data frame with Username and completion
        # Create data frame with Username and completion
        lecture = pd.DataFrame(columns=['Username',filename])
        lecture['Username'] = record['UserName']
        lecture[filename] = record['Attended']

        completion = pd.merge(left=completion, right=lecture, how='left',
                              left_on='Username', right_on='Username')

### Order columns based on column name
completion = completion.sort_index(axis=1)
### Then put username first
cols = completion.columns.tolist()
completion = completion[cols[-1:] + cols[:-1]]
completion = completion.fillna(value=0) 

### Put average column at the end
# Don't use the Username column
# .loc is for column names, .iloc is for column indices
compls = completion.iloc[:, 1:]
completion['Average'] = compls.mean(axis=1)*100
# Also put first and last name:
completion['Last Name'] = gc['Last Name']
completion['First Name'] = gc['First Name']

# Save Completion
completion.to_csv('completion.csv',index=False)

# Determine GC column for attendance
attcol = [col for col in gc.columns if "Attendance" in col]
#gc.loc[:,attcol] = completion['Average']

# Create file with correct column name for uploading
uploadFile = pd.DataFrame(columns=['Username',attcol[0]])
uploadFile.loc[:,'Username'] = completion['Username']
uploadFile.loc[:,attcol[0]] = completion['Average']

# Save it
uploadFile.to_csv('uploadFile.csv',index=False)
