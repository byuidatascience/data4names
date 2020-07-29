#%%
# import packages
# pip instal xlrd
import pandas as pd
import numpy as np
import seaborn as sns
from pathlib import Path
import us

# https://github.com/appeler/ethnicolr
# Handling file paths
# https://treyhunner.com/2018/12/why-you-should-be-using-pathlib/


#%%
# Read in data for gender and race probabilities
dat_gender = pd.read_csv("data/name_gender.csv", delimiter = ",")
dat_race = pd.read_excel("data/firstnames_race.xlsx", sheet_name="Data")


#%%
# Now to read through all state files in folder and then append.
counts_folder = Path.cwd() / "data" / "names_state" 
files = counts_folder.glob("*.TXT")

colnames = ['state', 'gender', 'year', 'name', "count"]
# What is the difference between these two lines
#df_states = (pd.read_csv(f, names = colnames , header = None) for f in files)
df_states = [pd.read_csv(f, names = colnames , header = None) for f in files]
# https://pandas.pydata.org/pandas-docs/stable/user_guide/merging.html
# https://pandas.pydata.org/pandas-docs/stable/getting_started/comparison/comparison_with_sql.html#compare-with-sql-join

# http://jonathansoma.com/lede/foundations-2017/classes/working-with-many-files/class/
# https://stmorse.github.io/journal/tidyverse-style-pandas.html
dat_state_year = pd.concat(df_states, ignore_index=True)


# Now move all the data for merging

# 
#%%
# Create data sets for year gender and then to merge with prob data

dat_year = (dat_state_year
    .groupby(["name", "gender", "year"])
    .agg(sum = ("count", "sum")).reset_index())

dat_mf = (dat_state_year
    .groupby(["name", "gender"])
    .agg(sum = ("count", "sum")).reset_index())

dat_state = (dat_state_year
    .groupby(["name", "gender", "state"])
    .agg(
        sum = ("count", "sum"),
        mean = ("count", "mean"),
        max = ("count", "max"),
        min = ("count", "min"),
    ).reset_index())
   


#%%
# Make one data set with gender, race, and state to totals
# https://gist.github.com/conormm/fd8b1980c28dd21cfaf6975c86c74d07
# https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.rename.html
# df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
# df.rename(columns={"A": "a", "B": "c"})
gender_count_merge = (pd.pivot_table(dat_mf, 
                            index = "name", 
                            columns = "gender", 
                            values="sum", fill_value=0)
                      .rename(columns={"M": "number_male", "F": "number_female"}))

gender_prob_merge = (pd.pivot_table(dat_gender, 
                            index = 'name', 
                            columns='gender', 
                            values='probability', 
                            fill_value=0)
                     .rename(columns={"M": "prob_male", "F": "prob_female"}))

state_merge = pd.pivot_table(dat_state, 
                            index = "name", 
                            columns = "state", 
                            values = "sum", 
                            fill_value=0)

# https://www.shanelynn.ie/merge-join-dataframes-python-pandas-index-1/
# https://www.coursera.org/lecture/python-data-analysis/merging-dataframes-08sf6

m1 = pd.merge(gender_count_merge, gender_prob_merge, on='name', how='left')
dat_out = pd.merge(m1, state_merge, on="name", how="left").reset_index()


dat_out.to_csv("derived_data/baby_names_gender_state.csv")


#%%
# save yearly data as on file with state information beyond the abbreviation
# https://github.com/unitedstates/python-us

# create new columns
# https://cmdlinetips.com/2019/01/3-ways-to-add-new-columns-to-pandas-dataframe/
# gapminder.assign(pop_in_millions=lambda x: x['pop']/1e6,
#                pop_in_billions=lambda x: x['pop_in_millions']/1e3).head()

# https://mode.com/python-tutorial/defining-python-functions

# https://stackoverflow.com/questions/35414625/pandas-how-to-run-a-pivot-with-a-multi-index

# remove names with less than 'count_remove' ever
count_remove = 500
bnames = dat_out[(dat_out['number_male'] > count_remove) | (dat_out['number_female'] > count_remove)]['name']


dat_sy_wide = (dat_state_year.pivot_table(
    index = ["name", "year"], 
    columns = "state", 
    values = "count", fill_value=0).
    assign(
        Total = lambda x: x.sum(axis = 1)
    ).reset_index().
    query('name in @bnames'))

dat_sy_wide.to_csv("derived_data/baby_names_state_year.csv")

