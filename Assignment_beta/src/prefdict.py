# -*- coding: utf-8 -*-
""" creat students_pref_dic & projects_pref_dict """

import random
from src.preprocessing import preProcessMajor

def creatExceptions_dict():
    """ Lists the exceptions : if the student is from major so he has access to exceptions_dict[major] projects """
    exceptions_dict = {
            'SGB' : ['IEE', 'HCE'],
            'GEE' : ['ASI'],
            'NEW' : ['ASI'],
            'HCE' : ['HOE'],
            'IEN' : ['ASI', 'HCE'],
            'SEM' : ['ASI', 'HCE']
            }
    return exceptions_dict
   
def creatStudentprefsdict(df): 
    """ Creat students_pref_dict that lists the projects prefered by each student"""
    student_pref_dict = {}
    exceptions_dict = creatExceptions_dict()
    for row in df.itertuples():
        listt = [] #list of prefered projects
        for i in range(10): #iterat on the choices
            if df.iat[row.Index,i+4] != 0:
                projectID = df.iat[row.Index, i+4] +'_'+ row.Master_program #add the master_program name to the project name P1_ASI
                listt.append(projectID) # add project_Student'sMAJOR to list
                """ the exceptions"""
                for major in exceptions_dict.keys():
                    if major == row.Master_program : #if the student is from one of the majors to wich the exceptions apply
                        for j in range(len(exceptions_dict[major])):
                            projectID = df.iat[row.Index, i+4] + '_' + exceptions_dict[major][j]
                            listt.append(projectID)
                        break
        student_pref_dict[row.Student_ID] = listt #add the list of wanted projects for the student at hand
    return student_pref_dict


def creatStudentslistsdict(df): 
    """ Creat a dictionnary to list students by major """
    students_lists_by_major_dict = {}
    g = df.groupby('Master_program') 
    for major, major_df in g:
        data = g.get_group(major)['Student_ID']
        listt = data.tolist()
        students_lists_by_major_dict[major] = listt
    
    return students_lists_by_major_dict


def optimisestudentslist_rank(listt, student_pref_dict, projectID):
    """ delete students that didn't rank the project """
    return [
            student
            for student in listt 
            if projectID in student_pref_dict[student]
            ]



def creatProjectsprefs_capacitiesdict(df,dfS2): #dfS2 preprocessed dfStudents
    """ Creat project_pref_dict that lists the students prefered by a project expl : {'P1_ASI':['S12','S67', ...], 'P15_IEE' : [. . . ], ... } """
    project_pref_dict = {}
    capacities_dict = {} #the capacities of each project/ how many students the project can take
    exceptions_dict = creatExceptions_dict()
    studentslist_dict = creatStudentslistsdict(preProcessMajor(dfS2))
    student_pref_dict = creatStudentprefsdict(dfS2)
    for row in df.itertuples():
        for i in range(8): #iterate on the majors in dfProjects => df 
            projectID = row.Project_ID
            if df.iat[row.Index,3+i] != 0: #if project capacitie isn't equal to zero
                projectMajor = df.keys()[3+i]
                projectID = projectID + '_' + projectMajor #add the name of the major to the project name 'P1_ASI'
                listt = studentslist_dict[projectMajor] # project accepts students  from the same major expl: "P1_ASI" accepts "ASI" students
                listt = random.sample(listt,len(listt)) #randomise the list of students from the same major as the project
                """ the exceptions """
                studentMajors_toaddlist = [studentMajor for studentMajor in exceptions_dict.keys() if projectMajor in exceptions_dict[studentMajor]  ] # list of majors that the project should accept besides it's own major
                for j in range(len(studentMajors_toaddlist)):
                    listt = listt + random.sample(studentslist_dict[studentMajors_toaddlist[j]],len(studentslist_dict[studentMajors_toaddlist[j]])) # add students list from the majors that are suposed to be added
                listt = optimisestudentslist_rank(listt, student_pref_dict , projectID) #delete the students that didn't rank the project
                project_pref_dict[projectID] = random.sample(listt,len(listt)) #randomise the lists
                capacities_dict[projectID] = df.iat[row.Index,3+i] #add the list of wanted students for the project at hand
    return project_pref_dict,capacities_dict


def optimiseStudentpref_dict(df, dfS2):
    """ Delete all projects that don't exist from student_pref_dict aka that aren't in project_pref_dict """
    student_pref_dict = creatStudentprefsdict(dfS2)
    project_pref_dict, capacities_dict = creatProjectsprefs_capacitiesdict(df,dfS2)
    
    for student in student_pref_dict.keys():
        indexlist_todelete = [] #list of all porjects that should be deleted
        for project in student_pref_dict[student]: #all project the student ranked
            if project not in project_pref_dict.keys(): #if the project doesn't exist
                indexlist_todelete.append(project) # add it to the list to delete
        for project in indexlist_todelete:
            student_pref_dict[student].remove(project)
    return student_pref_dict