import pandas as pd
import numpy as np
from datetime import datetime

def datetime_from_format(datestring):
    return datetime.strptime(datestring, '%Y-%m-%dT%H:%M:%S')


def datetime_from_timestamp(timestamp):
    return datetime.fromtimestamp(timestamp).strftime('00:%M:%S')


data = pd.read_csv('./Fire-Incidents.csv')

data = data.drop([
    'Area_of_Origin',
    'Count_of_Persons_Rescued',
    'Estimated_Dollar_Loss',
    'Ext_agent_app_or_defer_time',
    'Fire_Alarm_System_Impact_on_Evacuation',
    'Incident_Station_Area',
    'Incident_Ward',
    'Last_TFS_Unit_Clear_Time',
    'Latitude',
    'Longitude',
    'Method_Of_Fire_Control',
    'Property_Use',
    'Smoke_Alarm_at_Fire_Origin_Alarm_Failure',
    'Smoke_Alarm_at_Fire_Origin_Alarm_Type',
    'Fire_Under_Control_Time',
    'Ignition_Source',
    'Material_First_Ignited',
], axis=1) 

def op_time(row):
    alarm = datetime_from_format(row['TFS_Alarm_Time'])
    arrival = datetime_from_format(row['TFS_Arrival_Time'])

    return (arrival - alarm).total_seconds()

def eval_business_impact(row):
    business_impact = row['Business_Impact']
    
    if(business_impact == "May resume operations within a week"):
        return 1
    elif(business_impact == "May resume operations within a month"):
        return 2
    elif(business_impact == "May resume operations within a year"):
        return 3
    elif(business_impact == "May not resume operations"):
        return 4
    else:
        return 0


def eval_extent_of_fire(row):
    extent: str = row['Extent_Of_Fire']
    
    if('Confined' in extent):
        return 1
    elif('Spread' in extent):
        return 2
    elif('Entire' in extent):
        return 3
    else:
        return 0


data['Operation_time'] = data.apply(lambda x: op_time(x), axis=1)
data['eval_bi'] = data.apply(lambda x: eval_business_impact(x), axis=1)
data['eval_eof'] = data.apply(lambda x: eval_extent_of_fire(x), axis=1)


from pandas_profiling import ProfileReport
profile = ProfileReport(data, title="Pandas Profiling Report")
profile.to_file("your_report.html")
