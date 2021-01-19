# -*- coding: utf-8 -*-
"""
Created on Tue Jan 19 13:15:18 2021

@author: AhMeD DaWooD
"""

import pandas as pd 
df = pd.read_csv("glassdoor_jobs.csv")

# Salary Prasing 

df['hourley'] = df['Salary Estimate'].apply(lambda x: 1 if 'per hour' in x.lower() else 0)
df['employer_provided'] = df['Salary Estimate'].apply(lambda x: 1 if 'employer provided salary:' in x.lower() else 0)

df = df[df["Salary Estimate"] != "-1"] #put -1 in qautes bec the field is not numeric 
salary = df['Salary Estimate'].apply(lambda x: x.split('(')[0])
salary_minus_KD = salary.apply(lambda x: x.replace('K','').replace('$', ''))
salary_minus_hour = salary_minus_KD.apply(lambda x: x.lower().replace('per hour','').replace('employer provided salary:',''))

min_salary = salary_minus_hour.apply(lambda x: int(x.split('-')[0]))
max_salary = salary_minus_hour.apply(lambda x: int(x.split('-')[1]))

df['min_salary'] = min_salary
df['max_salary'] = max_salary
df['avg_salary'] = (df.min_salary + df.max_salary)/2

# Clean Company Name 
df['company text'] = df.apply(lambda x: x['Company Name'] if x['Rating'] < 0 else x['Company Name'][:-3], axis = 1)

#Stae / Location
df['job_state'] = df['Location'].apply(lambda x: x.split(',')[1])
print(df.job_state.describe())
print(df.job_state.value_counts())


df['same state'] = df.apply(lambda x: 1 if x.Location == x.Headquarters else 0, axis = 1)

## Year of establish 
df['age'] = df.Founded.apply(lambda x: x if x == -1 else 2020 - x)

#job Description 
print(df['Job Description'][0])

#python
df['python_yn'] = df['Job Description'].apply(lambda x: 1 if 'python' in x.lower() else 0)
print(df.python_yn.value_counts())

#r studio
df['R_yn'] = df['Job Description'].apply(lambda x: 1 if 'r studio' in x.lower() or  'r-studio' in x.lower() else 0)
print(df.R_yn.value_counts())

#spark
df['spark_yn'] = df['Job Description'].apply(lambda x: 1 if 'spark' in x.lower() else 0)
print(df.spark_yn.value_counts())

#aws
df['aws_yn'] = df['Job Description'].apply(lambda x: 1 if 'aws' in x.lower() else 0)
print(df.aws_yn.value_counts())

#excel
df['excel_yn'] = df['Job Description'].apply(lambda x: 1 if 'excel' in x.lower() else 0)
print(df.excel_yn.value_counts())

#tableau
df['tableau_yn'] = df['Job Description'].apply(lambda x: 1 if 'tableau' in x.lower() else 0)
print(df.tableau_yn.value_counts())

#power pi
df['power_yn'] = df['Job Description'].apply(lambda x: 1 if 'power pi' in x.lower() or 'power-pi' in x.lower() else 0)
print(df.power_yn.value_counts())

print(df.columns)
df_out = df.drop(['Unnamed: 0'], axis = 1)

df_out.to_csv('salary_data_cleaned.csv', index = False)
