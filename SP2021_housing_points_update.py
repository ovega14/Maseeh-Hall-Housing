import numpy as np
import pandas as pd

# initialize lists to store  'headers' and numerical point categories for spreadsheet
headers = []
point_categories = []

# get the substituent dataframes (make sure you use the appropriate filepath for your directory; here I use mine)
df_govt = pd.read_excel('sp2021_govt_points.xlsx')
df_fa2021 = pd.read_excel('fa2021_roster.xlsx')  # incoming residents, STILL BEING UPDATED by HRS
df_sp2020 = pd.read_excel('previous_sp2020.xlsx')  # previous housing points, from Spring 2020
df_sp2021 = pd.read_excel('sp2021_roster.xlsx')

# to create a full input spreadsheet, include a broad list of people and update everyone's points
semesters = [df_sp2020, df_sp2021, df_fa2021]

kerbs_list = [df['Kerberos'] for df in semesters]
kerbs_seq = [arr for arr in kerbs_list]

new_kerbs_raw = np.unique(np.concatenate(kerbs_seq))
new_kerbs = np.array([new_kerbs_raw]).T
headers.append(new_kerbs)

# COMPILING PREVIOUS POINTS
prev_kerbs = df_sp2020['Kerberos']
prev_totals = df_sp2020['Total']
prev_points = {prev_kerbs[i]: prev_totals[i] for i in range(len(prev_totals))}

for item in new_kerbs_raw:
    if item not in prev_points.keys():
        prev_points[item] = 0
    elif item in prev_points.keys():
        pass

fa2021_all_kerbs_raw = np.array([k for k in prev_points.keys()])
fa2021_prev_points_raw = np.array([prev_points[j] for j in new_kerbs_raw])
fa2021_prev_points = np.array([fa2021_prev_points_raw]).T
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
        num_yr = [gradyear_sp2021[i] for i in arr]
    return np.array(num_yr)


# convert the raw year as text into a numerical year string
raw_year_fa2021 = df_fa2021['Year (RAW)']
year_fa2021 = grad_year(raw_year_fa2021, 'fa2021')
classes_fa2021 = {df_fa2021['Kerberos'][i]: year_fa2021[i] for i in range(len(year_fa2021))}

raw_year_sp2021 = df_sp2021['Year (RAW)']
year_sp2021 = grad_year(raw_year_sp2021, 'sp2021')
classes_sp2021 = {df_sp2021['Kerberos'][i]: year_sp2021[i] for i in range(len(year_sp2021))}

year_sp2020 = df_sp2020['Year']
classes_sp2020 = {df_sp2020['Kerberos'][i]: year_sp2020[i] for i in range(len(prev_totals))}

fa2021_all_classes = {}
years_dict = [classes_sp2020, classes_sp2021, classes_fa2021]

for x in years_dict:
    fa2021_all_classes.update(x)

fa2021_years_raw = np.array([fa2021_all_classes[i] for i in new_kerbs_raw])
fa2021_years = np.array([fa2021_years_raw]).T
headers.append(fa2021_years)

sen_year = np.full((fa2021_years.shape[0], 1),
                   '2022')  # <--change this to grad year of upcoming seniors; senior identifier


def is_senior(year):
    return year == sen_year


fa2021_sen_pts = 40 * is_senior(fa2021_years)
point_categories.append(fa2021_sen_pts)

# COMPILING COMMITTEE POINTS
'''
(Optionally) Need to add something to check that if a name appears twice (i.e. someone volunteered for multiple things),
must add the points and put them under one name. otherwise check for redundancies by hand
'''
df_comm = pd.read_excel('sp2021_committee_points.xlsx')

comm_kerbs = df_comm['Kerberos']
comm_pts = df_comm['Committee Points']
sp2021_comm_pts = {comm_kerbs[i]: comm_pts[i] for i in range(len(comm_kerbs))}

for kerb in new_kerbs_raw:
    if kerb not in sp2021_comm_pts.keys():
        sp2021_comm_pts[kerb] = 0
    elif kerb in sp2021_comm_pts.keys():
        pass

fa2021_comm_pts_raw = np.array([sp2021_comm_pts[i] for i in new_kerbs_raw])
fa2021_comm_pts = np.array([fa2021_comm_pts_raw]).T
point_categories.append(fa2021_comm_pts)

# COMPILING RESIDENT POINTS
'''
Basically need to check that the Spring 2021 roster lines up with the entire housing points roster.
The residents in the intersection of both matrices are the ones who receive 20 resident points for living in Maseeh.
'''
res_kerbs = df_sp2021['Kerberos']
sp2021_res_pts = {res_kerbs[i]: 0 for i in range(len(res_kerbs))}

for kerb in new_kerbs_raw:
    if kerb not in sp2021_res_pts.keys():
        sp2021_res_pts[kerb] = 0
    elif kerb in sp2021_res_pts.keys():
        sp2021_res_pts[kerb] = 20

fa2021_res_pts_raw = np.array([sp2021_res_pts[i] for i in new_kerbs_raw])
fa2021_res_pts = np.array([fa2021_res_pts_raw]).T
point_categories.append(fa2021_res_pts)

# COMPILING GOVERNMENT POINTS
govt_pts = df_govt['Government Points']
govt_kerbs = df_govt['Kerberos']
sp2021_govt_pts = {govt_kerbs[i]: govt_pts[i] for i in range(len(govt_kerbs))}

for kerb in new_kerbs_raw:
    if kerb not in sp2021_govt_pts.keys():
        sp2021_govt_pts[kerb] = 0
    elif kerb in sp2021_govt_pts.keys():
        pass

fa2021_govt_pts_raw = np.array([sp2021_govt_pts[i] for i in new_kerbs_raw])
fa2021_govt_pts = np.array([fa2021_govt_pts_raw]).T
point_categories.append(fa2021_govt_pts)

# Write to a CSV file
for cat in point_categories:
    headers.append(cat)

out_cols = np.stack(headers)
labels = ['Kerberos', 'Year', 'Previous Points', 'Senior Points', 'Committee Points',
          'Residency Points', 'Government Points']
head_cols = np.array([[col] for col in labels])

refined_cols = out_cols.reshape(7, 1132, )  # get rid of the extra 3rd dim from np.stack

df = pd.DataFrame(data=refined_cols.T, index=None, columns=head_cols)

df.to_csv('insert_filepath/sheet_name.csv', index=False, header=True)

