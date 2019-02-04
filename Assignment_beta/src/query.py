# -*- coding: utf-8 -*-
""" Get results of the matching """

from src.prefdict import creatStudentprefsdict
import src.preprocessing as preprocessing
#import pandas as pd
   
def get_unmatched_residents(resident_prefs, matching):
    """ Return a list of all residents who are currently unmatched """
    return [
        resident
        for resident in resident_prefs
        if not any([resident in match for match in matching.values()])
    ]
    
def get_matched_residents(resident_prefs, matching):
    """ Return a list of all residents who are currently unmatched """
    return [
        resident
        for resident in resident_prefs
        if any([resident in match for match in matching.values()])
    ]
    
def get_unmatched_projects(hospital_prefs, matching, capacities_dict):
    """ Return a list of all hospitals who are currently not full """
    return [
            hospital
            for hospital in hospital_prefs
            if len(matching[hospital]) < capacities_dict[hospital]
            ]

def getResult(matching,resident_prefs,dfS2):
    """ Get number of students who got 1st,2nd,3th choice : count
        Get number of students who got 4th,5th,6th choice : sigma"""
    count = 0
    sigma = 0
    mathced_list = get_matched_residents(resident_prefs, matching)
    student_pref_dict = creatStudentprefsdict(dfS2)
    for resident in mathced_list: #True if resident is matched 
        for i in range(3):
            try:
                hospitalpref = student_pref_dict[resident][i] #most preferred hospital
            except IndexError:
                break
            hospitalpref = student_pref_dict[resident][i]
            index_matchedHospital = [resident in match for match in matching.values()].index(True)
            hospitalmatched = list(matching)[index_matchedHospital] #hospital he got
            if hospitalpref == hospitalmatched:
                count = count + 1
                break
        for j in range(3):
            try:
                hospitalpref = student_pref_dict[resident][j+3] #most preferred hospital
            except IndexError:
                break
            hospitalpref = student_pref_dict[resident][j+3]
            index_matchedHospital = [resident in match for match in matching.values()].index(True)
            hospitalmatched = list(matching)[index_matchedHospital] #hospital he got
            if hospitalpref == hospitalmatched:
                sigma = sigma + 1
                break
    return  count, sigma

def normaliseprojectname_matching(matching, df):
    """ Normalise the names of the projects to go from P1_ASI to simply P1
        Change students IDs in matching to their names
        """
    name_dict = preprocessing.creatname_dict(df) #dict of student IDs and their corresponding names
    hospital_list = []
    for hospital in matching:
        #Normalise the name of the project
        strr = hospital[:3] #take the first three letters
        if strr[-1:] == '_': #if the string ends with '_'
            strr = strr[:2] #keep only the first two characters
        if strr not in hospital_list: #if the normalised name of the project isn't added yet
            hospital_list.append(strr) #add it to the list of projects names
    
    new_matching = {hospital: [] for hospital in hospital_list} #creat the new matching dictionnary
    
    for hospital in matching:
        strr = hospital[:3]
        if strr[-1:] == '_':
            strr = strr[:2]
        #Get the students
        for student in matching[hospital]:
            student_name = name_dict[student] #get the name of the student
            new_matching[strr].append(student_name) #add the name of the student in stead of the students ID ('S45')
    return new_matching 



