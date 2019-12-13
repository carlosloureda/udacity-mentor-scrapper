from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import json
import time
from datetime import datetime
from bs4 import BeautifulSoup

# TODO: Let's think on how to do this dynamic

PROGRAM_INFO = {
    "REACT": {
        "TOTAL_LESSONS": "10",
        "TOTAL_PROJECTS": "5",
    }
}
PROGRAM = "REACT"


def get_credentials():
    with open("./credentials.json") as json_data_file:
        return json.load(json_data_file)
    return None


def init_selenium():
    webdriver_name = "chromedriver"
    driver = webdriver.Chrome(webdriver_name)
    return driver


def authenticate(driver):
    credentials = get_credentials()
    driver.get(
        "https://auth.udacity.com/sign-in?next=https://classroom.udacity.com/authenticated")

    elem = driver.find_element(By.XPATH, "//input[@data-cy='signin-email']")
    elem.click()
    elem.send_keys(credentials["udacity"]["username"])

    elem = driver.find_element(By.XPATH, "//input[@data-cy='signin-password']")
    elem.click()
    elem.send_keys(credentials["udacity"]["password"])

    elem = driver.find_element_by_class_name(
        "button_primary__1qhjh")
    elem.click()

    # TODO: wait for something to appear on window instead of sleep
    time.sleep(10)
    # driver.implicitly_wait(10)
    return driver


def get_students_info_from_dashboard(driver):
    driver.get(
        "https://mentor-dashboard.udacity.com/mentorship/overview")
    time.sleep(10)
    soup = BeautifulSoup(driver.page_source, 'html5lib')
    all_rows = soup.find_all("tr", {"class": 'rc-table-row'})
    students = []
    for student_row in all_rows:
        columns = student_row.find_all('td')
        students.append(list(map((lambda column: column.text), columns)))
    return students


"""
Get all the data from the dashboard. Just global helpers to be used
"""
POSITIONS = {
    "STUDENT": 0,
    "PROGRAM": 1,
    "FIRST_PAYMENT": 2,
    "SUBSCRIPTION_END": 3,
    "LESSONS_COMPLETED": 4,
    "PROJECTS_COMPLETED": 5,
    "ACTIONS": 6
}


def filter_by_lessons_completed(students, number_of_lessons, filter=None):
    """- Number of lessons completed: Dashboard"""
    filtered_students = []
    for student in students:
        if student[POSITIONS["LESSONS_COMPLETED"]] == str(number_of_lessons) + "/" + PROGRAM_INFO[PROGRAM]["TOTAL_LESSONS"]:
            filtered_students.append(student)

    return filtered_students


def filter_by_projects_completed(students, number_of_projects, filter=None):
    """- Number of projects completed: Dashboard"""
    filtered_students = []
    for student in students:
        if student[POSITIONS["PROJECTS_COMPLETED"]] == str(number_of_projects) + "/" + PROGRAM_INFO[PROGRAM]["TOTAL_PROJECTS"]:
            filtered_students.append(student)

    return filtered_students


def filter_by_since_first_week(students, days_off):
    """ Filters the students by the maximum {days_off}  since their initial date at udacity"""
    today = datetime.now()
    filtered_students = []
    for student in students:
        first_payment_date = parse_date_from_dashboard(
            student[POSITIONS["FIRST_PAYMENT"]])
        diff = today - first_payment_date

        if diff.days < days_off:
            filtered_students.append(student)
    return filtered_students


def filter_by_renewal_in_days(students, days_for_renewal):
    """ Filters the students by the maximum {days_for_renewal}  days for their next renewal date"""
    today = datetime.now()
    filtered_students = []
    for student in students:
        first_payment_date = parse_date_from_dashboard(
            student[POSITIONS["SUBSCRIPTION_END"]])
        diff = first_payment_date - today

        if diff.days < days_for_renewal:
            filtered_students.append(student)
    return filtered_students


"""
Dates helpers
"""


def parse_date_from_dashboard(date):
    """On dashboard the dates are on different format and want to parse them
    into the datetime.now() format"""
    return datetime.strptime(date,  '%b %d, %Y')


def get_students_names(students):
    names = []
    for student in students:
        names.append(student[0])
    return names


def main():
    driver = init_selenium()
    driver = authenticate(driver)
    students = get_students_info_from_dashboard(driver)
    print(f'--> You have a total of {len(students)} students')
    # Get students graduating in less than a week
    close_to_graduate = filter_by_renewal_in_days(students, 7)
    if (len(close_to_graduate)):
        names = get_students_names(close_to_graduate)
        print(
            f'## You have {len(close_to_graduate)} students graduating this week: ', names)

    # Get students registered less than a week ago
    first_week = filter_by_since_first_week(students, 7)
    if (len(first_week)):
        names = get_students_names(first_week)
        print(
            f'## You have {len(first_week)} students on their first week: ', names)


main()
