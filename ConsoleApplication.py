import json
import copy
from datetime import datetime
import re
from calendar import monthrange


# function to calculate one month from a given date
def add_one_month(input_date):
    month = input_date.month + 1
    year = input_date.year
    if month > 12:
        month = 1
        year = year + 1
    last_day_next_month = monthrange(year, month)[1]
    next_day = min(input_date.day, last_day_next_month)
    next_month = datetime(year, month, next_day)
    return next_month


#############task1 function starts####################
def user_count_of_completed_trainings(input_data):
    course_count = {}
    for record in input_data:
        for training in record['completions']:
            if training["name"] in course_count:
                course_count[training["name"]].add(record["name"])
            else:
                course_count[training["name"]] = {record["name"]}
    # structuring  the output data
    lst = []
    for key, value in course_count.items():
        output1_dict1 = {}
        output1_dict1["training_name"] = key
        output1_dict1["user_count"] = len(value)
        lst.append(output1_dict1)
    # dumping the data to json file
    o1 = 'output_task1.json'
    with open(o1, 'w') as json_file:
        json.dump(lst, json_file, indent=4)
    print(
        "###########Task 1 completed: output_task1.json file generated#####################\n")


###################task1 function completed#################

############task2 function starts##############################

def trainings_by_fiscal_year(sorted_input_data):
    # getting list of Trainings from user
    print("For Task2 enter the required inputs:")
    while True:
        print('Enter list of Trainings (comma-separated strings enclosed in double quotes only. e.g: "X-Ray Safety", "Laboratory Safety Training" ): ')
        user_input = input()
        if user_input.count('"') % 2 != 0:
            print("Error: Mismatched quotes. Please ensure that all strings are enclosed in double quotes.")
            continue
        pattern = r'"([^"]+)"'
        matches = re.findall(pattern, user_input)
        if len(matches) > 0:
            trainings = {match.strip().lower() for match in matches}
            break
        else:
            print("Error: Invalid format. Ensure all inputs are enclosed in double quotes and try again.")

    # getting fiscal year from user
    while True:
        print()
        year_value = input("Enter the fiscal year (YYYY): ")
        if re.match(r'^\d{4}$', year_value):
            break
        else:
            print("Error: Please enter a valid fiscal year in the format YYYY.")

    # calculating fiscal year range
    start_date = datetime(int(year_value) - 1, 7, 1)
    end_date = datetime(int(year_value), 6, 30)
    # finding the users who completed the given trainings in the specified fiscal year
    lst = []
    second_output = {}
    for i in sorted_input_data:
        for k in i["completions"]:

            if k["name"].lower() in trainings:
                completion_date = datetime.strptime(k["timestamp"], "%m/%d/%Y")

                if k["name"] not in second_output:
                    second_output[k["name"]] = []

                if (completion_date >= start_date and completion_date <= end_date):

                    if k["name"] in second_output:
                        second_output[k["name"]].append(i["name"])
    # giving proper keys to the data
    for k, v in second_output.items():
        temp = {"training_name": k, "users": v}
        lst.append(temp)
    # dumping output data to json file
    o2 = 'output_task2.json'
    with open(o2, 'w') as json_file:
        json.dump(lst, json_file, indent=4)
    print("###########Task 2 completed: output_task2.json file generated###########\n")



##############task2 function completed###############################


############task3 function starts##############################
def get_trainings_status_for_given_date(obj1):
    # getting the date input from user and validating it
    print("For Task3 enter required input:")
    while True:
        print("Enter a date to check expiration status of Trainings (Example: oct 21, 2023 or oct 21st, 2023): ")
        date_input = input()
        date_input = re.sub(r'(\d+)(st|nd|rd|th)', r'\1', date_input.strip())
        date_input = re.sub(r',\s*', ', ', date_input)
        date_formats = ["%b %d, %Y", "%Y-%m-%d", "%m/%d/%Y", "%B %d, %Y"]
        user_given_date = None
        for i in date_formats:
            try:
                user_given_date = datetime.strptime(date_input, i)
                break
            except ValueError:
                continue

        if user_given_date:

            break
        else:
            print("Please enter a valid date in one of the following formats: Oct 21st, 2023 or Oct 21, 2023 ")

    userdate_plus_onemonth = add_one_month(user_given_date)
    # finding the expiration status of the trainings for the given date
    lst = []
    third_output = {}
    for i in obj1:
        for j in i["completions"]:

            if j["expires"] is not None:
                course_expire_date = datetime.strptime(j["expires"], "%m/%d/%Y")
                if course_expire_date < userdate_plus_onemonth:
                    dict1 = {"name": j["name"]}
                    if course_expire_date >= user_given_date and course_expire_date < userdate_plus_onemonth:
                        dict1["expiration_status"] = "expires soon"
                    else:
                        dict1["expiration_status"] = "expired"

                    if i["name"] in third_output:
                        third_output[i["name"]].append(dict1)
                    else:
                        third_output[i["name"]] = [dict1]
    # structuring the output
    for k, v in third_output.items():
        temp = {"user_name": k, "trainings": v}
        lst.append(temp)
    # dumping output data to json file
    o3 = 'output_task3.json'
    with open(o3, 'w') as json_file:
        json.dump(lst, json_file, indent=4)

    print("###########Task 3 completed: output_task3.json file generated###########")


###############task3 function completed#########################


def main():


    try:
        file_name = input("Please enter the input data file name (with .json extension): ")
        print()
        # Open the input data file and read the JSON data
        with open(file_name, 'r') as jsonfile:
            data = json.load(jsonfile)

        # calling task1 function
        user_count_of_completed_trainings(data)

        # creating a copy
        obj1 = copy.deepcopy(data)
        # filtering the obj1 to eliminate duplicate courses and consider most recent course only if duplicates are there
        for i in obj1:
            latest_completions = {}
            for entry in i["completions"]:

                y = datetime.strptime(entry["timestamp"], "%m/%d/%Y")

                if entry["name"] not in latest_completions:

                    latest_completions[entry["name"]] = entry
                elif entry["name"] in latest_completions:
                    already_y = datetime.strptime(latest_completions[entry["name"]]["timestamp"], "%m/%d/%Y")
                    if y > already_y:
                        latest_completions[entry["name"]] = entry

            i["completions"] = list(latest_completions.values())

        # calling  task2 function
        trainings_by_fiscal_year(obj1)

        # calling  task3 function
        get_trainings_status_for_given_date(obj1)
    except FileNotFoundError:
        print(f"Error: The file '{file_name}' was not found.")
    except json.JSONDecodeError:
        print("Error: The file is not a valid JSON.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    except KeyboardInterrupt:
        print("\n Program exited.")


if __name__ == "__main__":
    main()
