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
            for index, value in enumerate(hay):
                if(cell == value or cell in value):
                    return index + 1
            return 0
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


data['eval_possible_cause'] = data.apply(lambda x: evaluate_column(x['Possible_Cause'], [
    ['Undetermined', 'Unintentional, cause undetermined', 'Other'],
    ['Improperly Discarded', 'Other unintentional cause, not classified'],
    ['Improper handling of ignition source or ignited material', 'Routine maintenance deficiency, eg creosote, lint, grease buildup'],
    ['Electrical Failure', 'Design/Construction/Installation/Maintenance Deficiency'],
    ['Unattended', 'Used or Placed too close to combustibles'],
    ]), axis=1)

data['eval_sofoa'] = data.apply(lambda x: evaluate_column(x['Status_of_Fire_On_Arrival'], [
['Fire extinguished prior to arrival', 'Unclassified'],
['Fire with no evidence from street', 'Fire with smoke showing only - including vehicle, outdoor fires'],
'Flames showing from small area (one storey or less, part of a vehicle, outdoor)',
'Flames showing from large area (more than one storey, large area outdoors)',
['Exposure involved', 'Fully involved (total structure, vehicle, spreading outdoor fire)'],
    ]), axis=1)

data['eval_faso'] = data.apply(lambda x: evaluate_column(x['Fire_Alarm_System_Operation'], [
    'Fire alarm system operated',
    'Fire alarm system operation undetermined',
    ['Not applicable (no system)', 'Fire alarm system did not operate']
    ]), axis=1)


from pandas_profiling import ProfileReport
profile = ProfileReport(data, title="Pandas Profiling Report")
profile.to_file("your_report.html")
