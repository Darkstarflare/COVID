#!/usr/bin/python
import numpy as np
import pandas as pd
import random
import config

from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.types import String, Integer
from collections import defaultdict 
import mysql.connector
from uszipcode import SearchEngine

Faker.seed(42)
np.random.seed(42)
fake = Faker()

def get_city_db():
    engine = SearchEngine()
    city_db = defaultdict(list)

    for zipcode in list(engine.by_state(sort_by='population', ascending=False, state="california", returns=10)) + list(engine.by_state(sort_by='population', ascending=False,  state="new york", returns=10)):
        city_db['zipcode'].append(zipcode.zipcode)
        city_db['major_city'].append(zipcode.major_city)
        city_db['county'].append(zipcode.county)
        city_db['state'].append(zipcode.state)
        city_db['population'].append(int(zipcode.population))

    return pd.DataFrame(city_db).drop_duplicates()

def get_user_db():
    user_db = defaultdict(list)

    for _ in range(100):
        user_db['email'].append(fake.email())
        user_db['name'].append(fake.name())
        user_db['user_name'].append(user_db['email'][-1].split('@')[0])
        user_db['password'].append(fake.password())
        user_db['dob'].append(fake.date_of_birth())
        user_db['country'].append(fake.country())

    return pd.DataFrame(user_db).drop_duplicates()

def get_subscription_db(df_user_db, df_city_db):
    emails = sorted(set(df_user_db['email'].tolist()))
    zipcodes = sorted(set(df_city_db['zipcode'].tolist()))
    subscription_db = defaultdict(list)
    for email in emails:
        for _ in range(np.random.randint(1, 4)):
            subscription_db['email'].append(email)

    subscription_db['zipcode'] = np.random.choice(zipcodes, len(subscription_db['email']), replace=True)
    return pd.DataFrame(subscription_db).drop_duplicates()

df_city_db = get_city_db()
df_user_db = get_user_db()
subscription_db = get_subscription_db(df_user_db, df_city_db)

my_conn = create_engine(config.SQLALCHEMY_DATABASE_URI)

subscription_db.to_sql(con=my_conn, name='subscription_db', if_exists='replace', index=False, dtype={'email': String(256), 'zipcode': Integer()})
df_user_db.to_sql(con=my_conn, name='user_db', if_exists='replace', index=False, dtype={'email': String(256), 'country': String(256)})
df_city_db.to_sql(con=my_conn, name='city_db', if_exists='replace', index=False, dtype={'zipcode': Integer(), 'major_city': String(256), 'county': String(256), 'state': String(10), 'population': Integer()})

my_conn.execute('ALTER TABLE `city_db` ADD PRIMARY KEY (`zipcode`);')
my_conn.execute('ALTER TABLE `user_db` ADD PRIMARY KEY (`email`);')
my_conn.execute('ALTER TABLE `user_db` MODIFY `name` VARCHAR(255) NOT NULL;')
my_conn.execute('ALTER TABLE `user_db` MODIFY `user_name` VARCHAR(30) NOT NULL;')
my_conn.execute('ALTER TABLE `user_db` MODIFY `password` VARCHAR(255) NOT NULL;')
my_conn.execute('ALTER TABLE `subscription_db` ADD PRIMARY KEY (`email`, `zipcode`);')
my_conn.execute('ALTER TABLE `subscription_db` ADD FOREIGN KEY (zipcode) REFERENCES city_db(zipcode);')
my_conn.execute('ALTER TABLE `subscription_db` ADD FOREIGN KEY (email) REFERENCES user_db(email);')