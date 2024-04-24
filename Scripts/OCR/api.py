import requests

base_url = "http://minmahawlms.cmkl.ai"
token = '212d242c1123f154a0c849fa7e9c68e5'
course_id = 4
URL = base_url + '/webservice/rest/server.php'


def get_name_list():
    params = {
        'wstoken': token,
        'wsfunction': 'core_enrol_get_enrolled_users',
        'courseid': course_id,
        'moodlewsrestformat': 'json'
    }
    response = requests.post(URL, params=params)
    users = response.json()
    name_dict = {}
    for user in users:
        name_dict[user['fullname']] = user['id']
    return name_dict

def get_cmid():
    params = {
        'wstoken': token,
        'wsfunction': 'mod_assign_get_assignments',
        'courseids[0]': course_id,
        'moodlewsrestformat': 'json'
    }
    response = requests.get(URL, params=params)
    assignments = response.json()['courses'][0]['assignments']

    params = {
        'wstoken': token,
        'wsfunction': 'gradereport_user_get_grade_items',
        'courseid': course_id,
        'userid': 7,
        'moodlewsrestformat': 'json'
    }

    response = requests.get(URL, params=params)
    grade_items = response.json()['usergrades'][0]['gradeitems']

    cmid_dict = {}
    for grade_item in grade_items:
        item_instance = grade_item['iteminstance']
        for assignment in assignments:
            if assignment['id'] == item_instance:
                cmid_dict[grade_item['itemname']] = assignment['cmid']
                break

    return cmid_dict
    

def update_api(user_id, cmid, new_grade):
    params = {
        'wstoken': token,
        'wsfunction': 'core_grades_update_grades',
        'source': 'api',
        'courseid': course_id,
        'component': 'mod_assign',  # Replace with the appropriate component
        'activityid': cmid,  # Replace with the appropriate activity ID
        'itemnumber': 0,
        'moodlewsrestformat': 'json',
        'grades[0][studentid]': user_id,
        'grades[0][grade]': new_grade,
    }
    response = requests.post(URL, params=params)
    print(response.json())

def update_grade(name, assignment, grade):
    name_dict = get_name_list()
    cmid_dict = get_cmid()

    if name in name_dict and assignment in cmid_dict:
        user_id = name_dict[name]
        cmid = cmid_dict[assignment]
        update_api(user_id, cmid, grade)
    else:
        print("User or assignment not found.")

def print_uid_cmid():
    name_dict = get_name_list()
    cmid_dict = get_cmid()
    print(name_dict)
    print(cmid_dict)

if __name__ == "__main__":
    print_uid_cmid()
    update_grade("Kunanont Taechaaukarakul", "Assignment 2", 80)
