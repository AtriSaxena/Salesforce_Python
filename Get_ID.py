
from simple_salesforce import Salesforce
import pandas as pd
from auth import * 
import argparse

sf = Salesforce(
        username=username, 
        password=password, 
        security_token=security_token,
        instance_url = instance_url)

parser = argparse.ArgumentParser(description ='RUN SOQL Query for Salesforce')
parser.add_argument('--object',type=str, help='Salesforce Object Name')
parser.add_argument('--columns',type=str, help = 'Salesforce Object Columns')
parser.add_argument('--where_field', type=str, help='Where Column')
parser.add_argument('--csv_file',type=str,help='csv file')
parser.add_argument('--csv_field_map',type=str,help='CSV Mapped Field')
args = parser.parse_args()

## Example Argument Passing
import math
# python Get_ID.py --object Object1 --columns "Id, col1, col2, col3" 
# --where_field Name --csv_file myfile.csv --csv_field_map NameofPerson

def SOQL_Query():
    data = pd.read_csv(args.csv_file)
    data.head()
    j=0
    for i in range(len(data)):
        fieldmap = str(data[args.csv_field_map][i]).split(',')
        
        print("Running Query:")
        for f in fieldmap:
            SOQL = 'SELECT ' + args.columns + " FROM " + args.object + ' WHERE ' + args.where_field + '=' + "'" + str(f) + "'"
            #print(SOQL)
            qryResult = sf.query(SOQL)
            isDone = qryResult['done']
            #print(qryResult['records'])
            
            if isDone == True:
                if j == 0:
                    if len(qryResult['records']) > 0:
                        df = pd.DataFrame(qryResult['records'])
                        j+=1
                else:
                    if len(qryResult['records']) > 0:
                        df = df.append(pd.DataFrame(qryResult['records']))

                
    df = df.drop('attributes',axis=1)
    df.to_csv('output.csv')
    print("Data saved to output.csv") 



print(SOQL_Query())
            