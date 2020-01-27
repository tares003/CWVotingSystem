import csv
import random
import string

from faker import Faker

fake = Faker()

user_registered = [True, False]
faculties = ["fa1", "fa2", "fa3", "fa4"]
NUMBER_OF_DATA_TO_GENETRATE = 1000


def getRandomDetails():
    person = dict()

    #for generating mix of male and female
    if not i % 2 == 0:
        person["name"] = fake.first_name_male() + " " + fake.last_name_male()
    else:
        person["name"] = fake.first_name_female() + " " + fake.last_name_female()

    person["Registered"] = random.choice(user_registered)
    person["dob"] = "".join(
        map(str, [random.randint(1, 30), "/", random.randint(1, 12), "/", random.randint(1940, 2001)]))
    person["id"] = "".join(map(str, [person["name"].split()[0], random.randint(0, 50000)]))
    person["faculty"] = random.choice(faculties)
    person["password"] = "".join([random.choice(string.ascii_letters) for d in range(5)] + [random.choice(string.digits) for d in range(2)])  #for random password
    return person

#generating the random Student
with open("RandomStudents.csv", "w", newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["name", "Registered", "dob", "id", "faculty", "password"], quoting=csv.QUOTE_ALL)
    header_written = False
    for i in range(1000):
        if not header_written:
            writer.writeheader()
            header_written = True
        student = getRandomDetails()
        writer.writerow(student)

random_choice_candadates = list()
postions = {"GSU Officers": 3,
            "President": 1,
            "Faculty Officer": 16
            }
#reading again from the text file
with open("RandomStudents.csv", "r") as students_details_file:
    csv_reader = csv.DictReader(students_details_file)
    all_Students = []
    for row in csv_reader:
        all_Students.append(dict(row))

    gsu_position = dict()

    #creating unique position for GSU officer
    # for i in range(1,postions['GSU Officers']+1):
    #     gsu_position['Position '+postions]=0 #setting 0 to all all the positon


    first_run = True
    faculty_groups = {}

    # counter = 1
    # for i in range(1, (postions['Faculty Officer'] * 4) + 1):
    #     if i % 4 != 0:
    #
    #         pass
    #     elif i% 4 == 0:
    #         faculty_groups['group %s' % counter] = 0

    done_faculty = {'fa1': 0, 'fa2': 0, 'fa3': 0, 'fa4': 0 }
    for key, val in postions.items():  # Each position
        for i in range(1, val * 4+1):  # 4 candadates per position
            #for unique candidates
            unique = False
            while not unique:
                choice = random.choice(all_Students)
                # max 16 candidates per faculty
                # print(key, val, i)
                # print(choice['faculty'])
                # print(all_Students[0]['faculty'])
                # TODO: Make it so it restricted to studen't GSU Position

                # only 16 candidates for the each Faculty
                if key == "Faculty Officer" and len(list(filter(lambda x: x['faculty'] == choice['faculty']
                                                                          and x['position'] == "Faculty Officer",
                                                                random_choice_candadates))) >= 16:
                    continue

                #
                # if key == "Faculty Officer":
                #
                #
                if choice not in random_choice_candadates:
                    print(i)
                    if i % 4 == 0 or first_run:  # every 4th candidate put it in a group

                        if key == "Faculty Officer":
                            current_group_gsu_val = key + ' group {}'.format(val)
                            pass
                        # else:

                        current_group_gsu_val = key + ' group {}'.format(val)  # name of the group
                        first_run = False
                        val -= 1
                    choice["group"] = current_group_gsu_val
                    choice["position"] = key
                    choice['campaign'] = fake.text()[:random.randint(5,20)]
                    choice['promises'] = fake.text()
                    choice['logoref'] = None # TODO: GENERATE RANDOM PROFILE IMAGES
                    unique = True
                    random_choice_candadates.append(choice)
                else:
                    continue
with open("RandomCandidates.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "Registered", "dob", "id", "position", "group",'faculty', "password", 'campaign', 'promises', 'logoref'],
                            quoting=csv.QUOTE_ALL)
    header_written = False
    for i in random_choice_candadates:
        if not header_written:
            writer.writeheader()
            header_written = True
        writer.writerow(i)
