# -*- coding: utf-8 -*-
""" test the assignment_beta V0.9.2 """

import time
start = time.time()


import pandas as pd
import src.preprocessing  as pre
import src.prefdict as pref
import src.solvers as sv
import src.query as qe

#Load the data files
dfProjects = pd.read_excel("C:\\Users\\hamza\\Desktop\\Ense3\\Ense3 2A b\\Optimisation\\Assignment project\\Test_DATA\TEST_2017\\Projects_TEST_2017.xlsx","Sheet2")
dfStudents = pd.read_excel("C:\\Users\\hamza\\Desktop\\Ense3\\Ense3 2A b\\Optimisation\\Assignment project\\Test_DATA\TEST_2017\\voeux_TEST_2017.xlsx","PI_Choix_Etudiants")
#Preprocess the data using Pandas
dfS = pre.preProcessMajor(dfStudents)
dfS1 = pre.preProcessStudents(dfS)
dfS2 = pre.preProcessProjects(dfS1)
name_dict = pre.creatname_dict(dfS2)
#Creat student & project pref dictionnary 
project_pref_dict,capacities_dict = pref.creatProjectsprefs_capacitiesdict(dfProjects,dfS2)
student_pref_dict = pref.optimiseStudentpref_dict(dfProjects,dfS2)
#Solve the assignment problem using Gale-Shapley
matching, resident_prefs, hospital_prefs = sv.resident_hospital(capacities_dict,student_pref_dict,project_pref_dict)
end = time.time()
print('Time to preprocess + creat project&student pref dict + do the actual matching',end - start)
#Results of the match
unmatchedStudentlist = qe.get_unmatched_residents(student_pref_dict, matching)
print('Percentage of students who are assigned',(len(student_pref_dict)-len(unmatchedStudentlist))/len(student_pref_dict))
unmatchedProjectslist = qe.get_unmatched_projects(project_pref_dict, matching, capacities_dict)
print('Percentage of project that are full',(len(project_pref_dict)-len(unmatchedProjectslist))/len(project_pref_dict))
student_pref_dict = pref.creatStudentprefsdict(dfS2)
count,sigma = qe.getResult(matching, student_pref_dict, dfS2)
print('Percentage of happily matched students(1st, 2nd or 3rd choice)', count/len(resident_prefs))
print('Percentage of unhappily matched students (4th, 5th 6th choice)', sigma/len(resident_prefs))
print('Percentage of really unhappily matched students (7th, 8th choice or worst)',(len(resident_prefs) - sigma- count)/len(resident_prefs))
#Normalise projects names 'P1_ASI' --> 'P1'
new_matching = qe.normaliseprojectname_matching(matching, dfS2)
#Export the results to excel
exceldf = pd.DataFrame.from_dict(new_matching, orient='index')
exceldf.to_excel("C:\\Users\\hamza\\Desktop\\matching_results.xlsx")