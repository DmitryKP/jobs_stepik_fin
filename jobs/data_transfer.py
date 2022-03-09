import sqlite3
import pandas as pd
from job_service.data import jobs, companies, specialties

sqlite_connection = sqlite3.connect('db.sqlite3')
cursor = sqlite_connection.cursor()

df_jobs = pd.DataFrame(jobs).drop('id', 1)[['title', 'skills', 'description',
                                            'salary_from', 'salary_to', 'posted',
                                            'company', 'specialty']]

selector = '''
INSERT INTO job_service_vacancy(title, skills, description, salary_min, salary_max, published_at, company_id, specialty_id)
VALUES (?,?,?,?,?,?,?,?);
'''
cursor.executemany(selector, [tuple(x) for x in df_jobs.values])
sqlite_connection.commit()

df_companies = pd.DataFrame(companies).drop('id', 1)[['title', 'location', 'logo', 'description', 'employee_count']]
selector = '''
INSERT INTO job_service_company(name, location, logo, description, employee_count)
VALUES (?,?,?,?,?);
'''
cursor.executemany(selector, [tuple(x) for x in df_companies.values])
sqlite_connection.commit()

cursor.execute("UPDATE job_service_company SET logo='https://place-hold.it/100x60'")
sqlite_connection.commit()

df_specialties = pd.DataFrame(specialties).assign(picture='https://place-hold.it/100x60')
selector = '''
INSERT INTO job_service_specialty(code, title, picture)
VALUES (?,?,?);
'''
cursor.executemany(selector, [tuple(x) for x in df_specialties.values])
sqlite_connection.commit()
