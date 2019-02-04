# -*- coding: utf-8 -*-

def get_worst_idx(hospital, hospital_prefs, matching):
    """ Find the index of the worst resident currently assigned to `hospital` according to their preferences. """

    return max(
        [
            hospital_prefs[hospital].index(resident)
            for resident in matching[hospital]
        ]
    )
    
def get_free_residents(resident_prefs, matching):
    """ Return a list of all residents who are currently unmatched but have a non-empty preference list. """

    return [
        resident
        for resident in resident_prefs
        if resident_prefs[resident]
        and not any([resident in match for match in matching.values()])
    ]


def resident_hospital(capacities,resident_prefs,hospital_prefs):
    """ Provide a stable, resident-optimal matching for the given instance of HR using the algorithm set out in [Gale, Shapley 1962]. """
# 0 - Assign all suitors and reviewers to be unmatched
    matching = {hospital: [] for hospital in hospital_prefs}
# 1 - Take any unmatched suitor, s, that is still up for consideration,
# and go to 2
# if there are no such suitors end
    free_residents = get_free_residents(resident_prefs, matching)
    while free_residents: # if there are no such suitors end
        #free_residents = get_free_residents(resident_prefs, matching)
        resident = free_residents[0]
# 2 - If the preference list of s is empty, remove them from consideration
# and go to 1
        while resident_prefs[resident]: 
            #free_residents = get_free_residents(resident_prefs, matching)
            hospital = resident_prefs[resident][0] # most preferred reviewer
        # Since we already did this in optimise student pref
#            if hospital not in hospital_prefs.keys():
#                resident_prefs[resident].remove(hospital)
#                break
# 3 -  If s is not ranked by r, remove r from the preference list of s
# and go to 2
            matching[hospital].append(resident) 
            if resident not in hospital_prefs[hospital]:
                resident_prefs[resident].remove(hospital)
                matching[hospital].remove(resident)
                free_residents = get_free_residents(resident_prefs, matching)
            elif len(matching[hospital]) > capacities[hospital]: # r has no space
                worstiD = get_worst_idx(hospital, hospital_prefs, matching)
                worst = hospital_prefs[hospital][worstiD]
                if worst != resident:
                    matching[hospital].remove(worst)
                    hospital_prefs[hospital].remove(worst)
                    resident_prefs[worst].remove(hospital)
                    free_residents = get_free_residents(resident_prefs, matching)
                    break
                else:
                    matching[hospital].remove(resident)
                    hospital_prefs[hospital].remove(resident)
                    resident_prefs[resident].remove(hospital)
                    free_residents = get_free_residents(resident_prefs, matching)
# Use the code above to speed up the algorithm
#            elif len(matching[hospital]) == capacities[hospital]:
#                worstiD = get_worst_idx(hospital, hospital_prefs, matching)
#                successors = hospital_prefs[hospital][worstiD + 1 :]                  
#                if successors :
#                    for r in successors:
#                        hospital_prefs[hospital].remove(r)
#                        if hospital in resident_prefs[r]:
#                            resident_prefs[r].remove(hospital)
                
            else:
                free_residents = get_free_residents(resident_prefs, matching)
                break
        #free_residents = get_free_residents(resident_prefs, matching)
    return matching, resident_prefs, hospital_prefs