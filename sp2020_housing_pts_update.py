import pandas as pd
import numpy as np

'''
Script for updating housing points for residents at end of Spring 2020. 
Written by Octavio Vega, MHEC President, Spring 2021
'''

roster = pd.read_csv('current') #the dataframe; use correct filepath

#identifiers
kerbs = roster['Kerberos'] #WITHOUT '@MIT.EDU'
year = roster['Year'] 

#point columns:
res_pts = roster['Residency Points']
sen_pts = roster['Senior Points'] 
govt_pts = roster['Government Points']

#senior identifier function
sen_year = np.full((year.shape[0],1),'2021') #change this to be graduation year of upcoming seniors
def is_senior():
    return np.equal(year, sen_year)
#add Senior points (ONLY in Spring updates!): upcoming seniors get 40 points
sen_pts += 40*is_senior()

#add committee points
#### FILL IN LATER-- was done manually this semester#####

#add resident points
###get rosters on a semesterly basis to confirm

#add government points
###DONE Manually###
