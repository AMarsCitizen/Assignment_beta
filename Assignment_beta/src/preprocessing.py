# -*- coding: utf-8 -*-
""" Preprocessing the pandas.DataFrame objects (df) to creat the right input for the solver s"""

def preProcessMajor(df): 
    """ Normalise the names of the Majors in dfStudents 'HCE' 'ASI' 'SGB' 'GEE' 'NEW' ... """
    rows,columns = df.shape
    for i in range(rows):
        if df['Master_program'].values[i] == 'GEE (Alternance)':
            df['Master_program'].values[i] = 'GEE'
        else:
            strr = str(df['Master_program'].values[i][-3:]) #take the last three leters of the string to get rid of any unncessary information
            df['Master_program'].values[i] = strr
    return df

def preProcessStudents(df): 
    """" Drop all students that didn't give their preference list in dfStudents"""
    rows,columns = df.shape
    todeleteList = []
    for row in df.itertuples(): #Loop to save the row index of every student that didn't give a preference list
        if row.choice_1 == 'xx':
            todeleteList.append(row.Index)
    df = df.drop(todeleteList) #Delete the list of the unwanted students
    df = df.reset_index(drop=True) #reset the index so any future transformation of the dataframe won't cause any confusion index wise
    return df

def preProcessProjects(df): 
    """ Normalise the names of the projects in dfStudents so it's just "Pi" where i is a number, i in [1,number_of_projects]"""
    for row in df.itertuples():
        for i in range(10):
            if row[i+5] != 0: #is ther any prefered project ?
                strr = row[i+5][:3] #take the first three leters of the string to get rid of any unncessary information
                if strr[-1:] == '-': #get rid of the"-" if there is one
                    strr = strr[:2]
                df.iat[row.Index,i+4] = strr
    return df
            
def creatname_dict(df):
    """ Creat a dictionarry of students IDs 'S25' & the students name 'Firsy' + 'Last' """
    name_dict = {}
    for row in df.itertuples():
        name_dict[row.Student_ID] = row.Last_Name +' '+ row.First_Name
    return name_dict
    
    
    
    