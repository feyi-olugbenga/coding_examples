import pandas as pd
import sqlite3

# import os
# import boto3

# session = boto3.Session(
#     region_name=os.environ['region_name'],
#     aws_access_key_id=os.environ['aws_access_key_id'],
#     aws_secret_access_key=os.environ['aws_secret_access_key'],
# )
#
# s3 = session.resource('s3')
# for bucket in s3.buckets.all():
#     print(bucket.name)

# s3 = session.client('s3')
# obj = s3.get_object(Bucket= "bucket", Key='07-07-2023 Oklahoma Human Services.csv')
# oklahoma_hs = pd.read_csv(obj['Body'])

oklahoma_hs = pd.read_csv('datasets/07-07-2023 Oklahoma Human Services.csv', nrows=49)
texas_dhhs = pd.read_csv('datasets/07-07-2023 Texas DHHS.csv')
nevada_dpbh = pd.read_csv('datasets/07-07-2023 Nevada Dept of Public _ Behavioral Health.csv', encoding='cp1252')


def split_name(entry):

    entry_list = entry.split('\r\n')
    person_name = entry_list[0].split(' ')

    return person_name[0], person_name[1], entry_list[1]


oklahoma_hs['Accepts Subsidy'] = oklahoma_hs['Accepts Subsidy'].map({'Accepts Subsidy': True}).fillna(False)
oklahoma_hs['first_name'], oklahoma_hs['last_name'], oklahoma_hs['title'] = zip(*oklahoma_hs['Primary Caregiver'].map(split_name))
oklahoma_hs['license_type'] = oklahoma_hs['Type License'].str.split(' - ').str[0].str.title()
oklahoma_hs['license_number'] = oklahoma_hs['Type License'].str.split(' - ').str[1]
oklahoma_hs['max_age'] = oklahoma_hs["AA4"].fillna(oklahoma_hs["AA3"]).fillna(oklahoma_hs["AA2"]).fillna(oklahoma_hs["Ages Accepted 1"])
oklahoma_hs['ages_served'] = oklahoma_hs['Ages Accepted 1'].astype(str) + ' to ' + oklahoma_hs['max_age']

oklahoma_hs = oklahoma_hs.rename(columns={'Accepts Subsidy': 'accepts_financial_aid',
                                          'Total Cap': 'capacity',
                                          'City': 'city',
                                          'Address1': 'address1',
                                          'Address2': 'address2',
                                          'Company': 'company',
                                          'Phone': 'phone',
                                          'Email': 'email',
                                          'License Monitoring Since': 'license_issued',
                                          'Ages Accepted 1': 'min_age',
                                          'State': 'state',
                                          'Zip': 'zip'
                                          })

non_oklahoma_columns = ['certificate_expiration_date',
                        'phone2',
                        'county',
                        'curriculum_type',
                        'language',
                        'license_status',
                        'license_renewed',
                        'license_name',
                        'operator',
                        'provider_id',
                        'language',
                        'schedule',
                        'website_address',
                        'facility_type']

for col_name in non_oklahoma_columns:
    oklahoma_hs[col_name] = None

oklahoma_hs.drop(['Type License', 'Year Round', 'Daytime Hours', 'Star Level',
                  'Mon', 'Tues', 'Wed', 'Thurs', 'Friday', 'Saturday', 'Sunday', 'Primary Caregiver',
                  'Subsidy Contract Number', 'AA2', 'AA3', 'AA4', 'School Year Only', 'Evening Hours'],
                 axis=1, inplace=True)

conn = sqlite3.connect('/Users/feyi/PycharmProjects/coding_examples/testDB.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS school_services (
        accepts_financial_aid character varying,
        ages_served character varying,
        capacity numeric,
        certificate_expiration_date date,
        city character varying,
        address1 character varying,
        address2 character varying,
        company character varying,
        phone character varying,
        phone2 character varying,
        county character varying,
        curriculum_type character varying,
        email character varying,
        first_name character varying,
        language character varying,
        last_name character varying,
        license_status character varying,
        license_issued date,
        license_number numeric,
        license_renewed date,
        license_type character varying,
        license_name character varying,
        max_age numeric,
        min_age numeric,
        operator character varying,
        provider_id character varying,
        schedule character varying,
        state character varying,
        title character varying,
        website_address character varying,
        zip character varying,
        facility_type character varying
)""")

oklahoma_hs.to_sql(name='school_services', con=conn, if_exists='replace', index=False)
conn.commit()
conn.close()
