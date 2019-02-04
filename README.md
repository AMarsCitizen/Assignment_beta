# Assignment_beta

The goal here is to assign students to projects given their preferences.

# The algorithm : Gale-Shapley 1962

This is an implementation of the capacitated Gale-Shapley algorithm. The algorithm is as follows :

0 - Assign all suitors and reviewers to be unmatched
1 - Take any unmatched suitor, s, that is still up for consideration,and go to 2.
If there are no such suitors, end.
2 - If the preference list of s is empty, remove them from consideration and go to 1. Otherwise, consider their most preferred reviewer, r. Go to 3.
3 -  If s is not ranked by r, remove r from the preference list of s and go to 2. Otherwise, if r has space, match s to r and go to 1. If not, go to 4.
4 - Consider r’s current matching, and particular their least preferable current matching, s’. If r prefers s to s’, then unmatch s’ from r, match s to r, and go to 1. Otherwise, leave s unmatched, remove s from the preference list of r and r from the preference list of s, and go to 2.

