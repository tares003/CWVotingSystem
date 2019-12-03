import csv
import random

from faker import Faker

fake = Faker()

user_registered = [True, False]
faculties = ["fa1", "fa2", "fa3", "fa4"]


def getRandomDetails():
    person = dict()

    if not i % 2 == 0:
        person["name"] = fake.first_name_male() + " " + fake.last_name_male()
    else:
        person["name"] = fake.first_name_female() + " " + fake.last_name_female()

    person["Registered"] = random.choice(user_registered)
    person["dob"] = "".join(
        map(str, [random.randint(1, 30), "/", random.randint(1, 12), "/", random.randint(1940, 2001)]))
    person["id"] = "".join(map(str, [person["name"].split()[0], random.randint(0, 50000)]))
    person["faculty"] = random.choice(faculties)
    return person


with open("RandomStudents.csv", "w", newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["name", "Registered", "dob", "id", "faculty"], quoting=csv.QUOTE_ALL)
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

with open("RandomStudents.csv", "r") as students_details_file:
    csv_reader = csv.DictReader(students_details_file)
    all_Students = []
    for row in csv_reader:
        all_Students.append(dict(row))

    for key, val in postions.items():  # Each position
        for i in range(val * 4):  # 4 candadates per position
            unique = False
            while not unique:
                choice = random.choice(all_Students)
                if choice not in random_choice_candadates:
                    choice["position"] = key
                    random_choice_candadates.append(choice)
                    unique = True
                else:
                    continue
with open("RandomCandidates.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "Registered", "dob", "id", "position", 'faculty'],
                            quoting=csv.QUOTE_ALL)
    header_written = False
    for i in random_choice_candadates:
        if not header_written:
            writer.writeheader()
            header_written = True
        writer.writerow(i)
