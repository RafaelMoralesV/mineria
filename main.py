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

def evaluate_column(cell, hay, exact = True):
    try:
        if(exact):
            return hay.index(cell) + 1
        else:
            for index, word in enumerate(hay):
                if(word in cell):
                    return index + 1
    except:
        return 0


data['Operation_time'] = data.apply(lambda x: op_time(x), axis=1)
data['eval_bi'] = data.apply(lambda x: evaluate_column(x['Business_Impact'], [
            "May resume operations within a week",
            "May resume operations within a month",
            "May resume operations within a year",
            "May not resume operations",
        ]), axis=1)
data['eval_eof'] = data.apply(lambda x: evaluate_column(x['Extent_Of_Fire'], [
    'Confined',
    'Spread',
    'Entire',
    ], exact=False), axis=1)


from pandas_profiling import ProfileReport
profile = ProfileReport(data, title="Pandas Profiling Report")
profile.to_file("your_report.html")
