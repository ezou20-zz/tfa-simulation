import py_school_match as psm
import random
import csv
from collections import defaultdict

schools_per_region_by_size = {"S": 20, "M": 60, "L": 100}
total_cap = 0
regions = defaultdict(list)

def create_schools():
    global total_cap, regions
    schools = []
    with open('../data/schools.csv', newline='') as regions:
        filereader = csv.reader(regions, delimiter=',')
        for row in filereader:
            print(row)
            region = row[0] 
            size = row[1]
            for i in range(schools_per_region_by_size[size]):
                capacity = random.randint(1,5)
                school = psm.School(capacity)
                school.category = region
                schools.append(school)
                total_cap += capacity
                regions[region].append(school)
    return schools

def create_students():
    pass
    # create/set student.category_preferences to random order over regions.keys()
    # for each region in order, randomly sort region's schools and add to student.global_preferences


    st0 = psm.Student()
    st1 = psm.Student()
    st2 = psm.Student()

    st0.preferences = [sc0, sc1, sc2]
    st1.preferences = [sc0, sc2, sc1]
    st2.preferences = [sc2, sc1, sc0]

def compare_matchings(matching1, matching2):
    pass


def run_simulation():
    random.seed(42)

    psm.Student.reset_ids()
    psm.School.reset_ids()
    
    students = create_students()
    schools = create_schools()
    print(total_cap)


    planner = psm.SocialPlanner(students, schools, psm.RuleSet())

def test_dastb():
    planner.run_matching(psm.DASTB())
    assertEqual(st0.assigned_school.id, 0)
    assertEqual(st1.assigned_school.id, 1)
    assertEqual(st2.assigned_school.id, 2)


run_simulation()