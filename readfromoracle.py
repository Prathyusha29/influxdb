import pyodbc
import json
import collections
import cx_Oracle
from influxdb import InfluxDBClient
import ast

con = cx_Oracle.connect('deploy/dep123@10.252.8.203:1909/citestha.webex.com')
#connstr = 'DRIVER={SQL Server};SERVER=10.252.8.203;DATABASE=citestha.webex.com;User ID=deploy;Password=dep123;'
#conn = pyodbc.connect(connstr)
cursor = con.cursor()
cursor.execute("SELECT dbtype,major_number,minor_number FROM IDENTITYDB.wbxdatabaseversion")
rows = cursor.fetchall()
objects_list = []

for row in rows:
    d = collections.OrderedDict()
    d['dbtype'] = row[0]
    d['major_number'] = row[1]
    d['minor_number'] = row[2]
    objects_list.append(d)
    print(d)

j = json.dumps(objects_list)
oracle_data = json.loads(j)
#data=j.loads(ob)
#jsonlist = ast.literal_eval(j)
#print(type(j1[0]))
print(oracle_data)
con.close()

client = InfluxDBClient('sdtsj1jks005.webex.com', '8086', 'admin', 'km', 'db_ci_version')

json_body =[{
    "measurement": "TEST",
    "tags": {
        "location": "SJC"
    },
    "fields": {
        "db_name": "db_ci_version",
        "patch_major": "30164",
        "patch_minor": "1",
        "patch_type": "DDL"
    }
},
    {
    "measurement": "TEST",
    "tags": {
        "location": "SJC"
    },
    "fields": {
        "db_name": "db_ci_version",
        "patch_major": "30164",
        "patch_minor": "0",
        "patch_type": "DML"
    }
}]


json_body[0]["fields"]['patch_type'] = oracle_data[0]['dbtype']
json_body[0]["fields"]['patch_major'] = oracle_data[0]['major_number']
json_body[0]["fields"]['patch_minor'] = str(oracle_data[0]['minor_number'])

json_body[1]["fields"]['patch_type'] = oracle_data[1]['dbtype']
json_body[1]["fields"]['patch_major'] = oracle_data[1]['major_number']
json_body[1]["fields"]['patch_minor'] = str(oracle_data[1]['minor_number'])

print(json_body)

client.write_points(json_body)