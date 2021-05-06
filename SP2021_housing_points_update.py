import pandas as pd
from pandas import ExcelWriter, ExcelFile
import numpy as np
import csv

# initialize this to store the 'headers' and numerical point categories for housing point spreadsheet
headers = []
point_categories = []

# get the substituent dataframes (make sure you use the appropriate filepath for your directory; here I use mine)
df_govt = pd.read_csv('sp2021_govt_points.xlsx')
df_res = pd.read_csv('sp2021_residency_points.xlsx')
df_fa2021 = pd.read_csv('fa2021_roster.xlsx')  # incoming residents, STILL BEING UPDATED by HRS
df_sp2020 = pd.read_csv('current.csv - Shortcut.lnk')  # previous housing points, from Spring 2020
df_sp2021 = pd.read_csv('sp2021_roster.xlsx')

# to create a full input spreadsheet, we'll include a broad list of people and update everyone's points regardless
semesters = [df_sp2020, df_sp2021, df_fa2021]

kerbs_list = [df['Kerberos'] for df in semesters]
new_kerbs = np.unique(np.concatenate(arr for arr in kerbs_list))
headers.append(new_kerbs)

# COMPILING PREVIOUS POINTS
prev_kerbs = df_sp2020['Kerberos']
prev_totals = df_sp2020['Total']
prev_points = {prev_kerbs[i]: prev_totals[i] for i in range(len(prev_totals))}

for item in new_kerbs:
    if item not in prev_kerbs:
        prev_points[item] = '0'

fa2021_prev_points = np.array([j for j in prev_points.values()])
fa2021_all_kerbs = np.array([k for k in prev_points.keys()])
point_categories.append(fa2021_prev_points)

# COMPILING SENIOR POINTS
gradyear_sp2021 = {'Freshman': '2024', 'Sophomore': '2023', 'Junior': '2022', 'Senior': '2021'}
gradyear_fa2021 = {'Freshman': '2025', 'Sophomore': '2024', 'Junior': '2023', 'Senior': '2022'}


def grad_year(arr, term):
    # assigns numerical graduation year to class name (e.g. 'Senior' --> 2022, 'Junior' --> 2023, etc.); depends on
    # reference year ['term']
    if term == 'fa2021':
        num_yr = [gradyear_fa2021[i] for i in arr]
    elif term == 'sp2021':
        num_yr = [gradyear_sp2021r_sp2021[i] for i in arr]
    return np.array(num_yr)


raw_year_fa2021 = df_fa2021['Year (RAW)']
year_fa2021 = grad_year(raw_year_fa2021, 'fa2021')
classes_fa2021 = {df_fa2021['Kerberos'][i]: year_fa2021[i] for i in range(len(prev_totals))}

raw_year_sp2021 = df_sp2021['Year (RAW)']
year_sp2021 = grad_year(raw_year_sp2021, 'sp2021')
classes_sp2021 = {df_sp2021['Kerberos'][i]: year_sp2021[i] for i in range(len(prev_totals))}

year_sp2020 = df_sp2020['Year']
classes_sp2020 = {df_sp2020['Kerberos'][i]: year_sp2020[i] for i in range(len(prev_totals))}

fa2021_all_classes = classes_sp2020.update(classes_sp2021.update(classes_fa2021))
fa2021_years = np.array([fa2021_all_classes[i] for i in fa2021_all_kerbs])
headers.append(fa2021_years)

sen_year = np.full((year.shape[0], 1), '2022')  # <--change this to grad year of upcoming seniors; senior identifier


def is_senior(year) -> arr:
    return np.equal(year, sen_year)


fa2021_sen_pts = 40 * is_senior(fa2021_years)
point_categories.append(fa2021_sen_pts)

# COMPILING COMMITTEE POINTS
'''
(Optionally) Need to add something to check that if a name appears twice (i.e. someone volunteered for multiple things),
must add the points and put them under one name. otherwise check for redundancies by hand
'''
df_comm = pd.read_csv('sp2021_committee_points.xlsx')

comm_kerbs = df_comm['Kerberos']
comm_pts = df_comm['Committee Points']
sp2021_comm_pts = {comm_kerbs[i]: comm_pts[i] for i in range(len(comm_kerbs))}

for kerb in fa2021_all_kerbs:
    if kerb not in comm_kerbs:
        sp2021_comm_pts[kerb] = '0'

fa2021_comm_pts = np.array([sp2021_comm_pts[i] for i in fa2021_all_kerbs])
point_categories.append(fa2021_comm_pts)

# COMPILING RESIDENT POINTS
'''
Basically need to check that the Spring 2021 roster lines up with the entire housing points roster.
The residents in the intersection of both matrices are the ones who receive 20 resident points for living in Maseeh.
'''
sp2021_res_points = {}
for kerb in fa2021_all_kerbs:
    if kerb in df_sp2021['Kerberos']:
        sp2021_res_points[kerb] = '20'
    else:
        sp2021_res_points[kerb] = '0'

fa2021_res_pts = np.array([sp2021_res_points[i] for i in fa2021_all_kerbs])
point_categories.append(fa2021_res_pts)

# COMPILING GOVERNMENT POINTS
govt_pts = df_govt['Government Points']
govt_kerbs = df_govt['Kerberos']
sp2021_govt_pts = {govt_kerbs[i]: govt_pts[i] for i in range(len(govt_kerbs))}
for kerb in fa2021_all_kerbs:
    if kerb not in govt_kerbs:
        sp2021_govt_pts[kerb] = '0'

fa2021_govt_pts = np.array(sp2021_govt_pts[i] for i in fa2021_all_kerbs)
point_categories.append(fa2021_govt_pts)

# PRINT TO NEW CSV
fa2021_total_pts = sum(point_categories)
point_categories.append(fa2021_total_pts)
for cat in point_categories:
    headers.append(cat)

df = pd.DataFrame(headers, columns=['Kerberos', 'Year', 'Previous Points', 'Senior Points', 'Committee Points',
                                    'Residency Points', 'Government Points', 'Total Points'])
df.to_csv(path, index=False, header=True)
