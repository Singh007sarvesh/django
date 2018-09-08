import json

employee_record = []


def setData(file):
    dataStore = json.loads(file)
    jsonRecords = dataStore["employee"]
    for records in jsonRecords:
        row = [records["first_name"], records["last_name"], records["date_of_birth"], 
        records["aadahr_id"], records["gender"], records["email"], 
        records["username"], records["password"]]
        employee_record.append(row)
        return employee_record
