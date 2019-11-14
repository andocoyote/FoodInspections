import sqlite3
import pandas as pd

# Create the table used to cache the inspection data
conn = sqlite3.connect('inspections.sqlite')
cur = conn.cursor()
cur.executescript('''CREATE TABLE IF NOT EXISTS Inspections (
                    id INTEGER PRIMARY KEY,
                    name TEXT,
                    program_identifier TEXT,
                    inspection_date TEXT,
                    description TEXT,
                    address TEXT,
                    city TEXT,
                    zip_code TEXT,
                    phone TEXT,
                    longitude TEXT,
                    latitude TEXT,
                    inspection_business_name TEXT,
                    inspection_type TEXT,
                    inspection_score INTEGER,
                    inspection_result TEXT,
                    inspection_closed_business TEXT,
                    violation_points INTEGER,
                    business_id TEXT,
                    inspection_serial_num TEXT,
                    grade INTEGER,
                    violation_type TEXT,
                    violation_description TEXT,
                    violation_record_id TEXT )
                    ''')
                    
# Read the inspection data from inspections.csv
df_inspections = pd.read_csv('inspections.csv')

# Write each inspection with its index to the database
for id, inspection in df_inspections.iterrows():

    cur.execute('''INSERT OR IGNORE INTO Inspections (
                id,
                name,
                program_identifier,
                inspection_date,
                description,
                address,
                city,
                zip_code,
                phone,
                longitude,
                latitude,
                inspection_business_name,
                inspection_type,
                inspection_score,
                inspection_result,
                inspection_closed_business,
                violation_points,
                business_id,
                inspection_serial_num,
                grade,
                violation_type,
                violation_description,
                violation_record_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
                id,
                inspection['name'],
                inspection['program_identifier'],
                inspection['inspection_date'],
                inspection['description'],
                inspection['address'],
                inspection['city'],
                inspection['zip_code'],
                inspection['phone'],
                inspection['longitude'],
                inspection['latitude'],
                inspection['inspection_business_name'],
                inspection['inspection_type'],
                inspection['inspection_score'],
                inspection['inspection_result'],
                inspection['inspection_closed_business'],
                inspection['violation_points'],
                inspection['business_id'],
                inspection['inspection_serial_num'],
                inspection['grade'],
                inspection['violation_type'],
                inspection['violation_description'],
                inspection['violation_record_id']) )

conn.commit()
conn.close()