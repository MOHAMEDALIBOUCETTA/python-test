import json
from pymongo import MongoClient
import datetime
import pandas as pd
import matplotlib.pyplot as plt
mongo_uri = "mongodb://127.0.0.1:27017"
data_path = "data.json.codechallenge.janv22.RHOBS.json"
N = 60
job = "expert automobile"
def collection(uri=mongo_uri):
    client = MongoClient(uri)
    database = client["rhobs"]
    collection = database["people"]
    return collection


def load(uri=mongo_uri, datapath=data_path):
    coll = collection(uri=uri)
    with open(datapath, "r") as fp:
        data = json.load(fp)

        for person in data:
            coll.insert_one(person)

def count_genders(uri=mongo_uri):
    data = collection(uri)
    print(len(list((data).find())))
    nb_hommes = data.count_documents({"sex":'M'})
    nb_femmes = data.count_documents({"sex":'F'})
    return {
        "nombre d'hommes":nb_hommes,
        "nombre de femmes":nb_femmes
    }

def filter_companies(uri=mongo_uri ,n = N):
    data = collection(uri)
    filtered_employees = data.find()
    companies_list = data.distinct("company")
    companies_dict = {company: 0 for company in companies_list}
    final_list = []
    for emp in filtered_employees : 
        companies_dict[emp['company']]+=1
    for comp in companies_list : 
        if companies_dict[comp] > N :
            final_list.append(comp)
    print(final_list)
       
def ages_by_job(uri=mongo_uri, job=job):
    data = collection(uri)
    filtered_employees = data.find({"job": job})
    current_year = datetime.date.today().year
    
    age_range = ['0-9', '10-19', '20-29', '30-39', '40-49', '50-59', '60-69', '70-79', '80-89', '90+']
    
    df = pd.DataFrame({'Age': age_range, 'Male': [0]*10, 'Female': [0]*10})
    
    for emp in filtered_employees:
        age = current_year - int(emp['birthdate'][:4])
        if emp["sex"] == 'M':
            df.loc[df['Age'] == f'{age//10*10}-{age//10*10+9}', 'Male'] += 1
        else:
            df.loc[df['Age'] == f'{age//10*10}-{age//10*10+9}', 'Female'] += 1
    y = range(0, len(df))
    x_male = df['Male']
    x_female = df['Female']
    fig, axes = plt.subplots(ncols=2, sharey=True, figsize=(9, 6))
    plt.figtext(.5,.9,"Age Pyramid ", fontsize=15, ha='center')
    axes[0].barh(y, x_male, align='center', color='royalblue')
    axes[0].set(title='Males')
    axes[1].barh(y, x_female, align='center', color='lightpink')
    axes[1].set(title='Females')

    axes[1].grid()
    axes[0].set(yticks=y, yticklabels=df['Age'])
    axes[0].invert_xaxis()
    axes[0].grid()
    plt.show()

ages_by_job()
