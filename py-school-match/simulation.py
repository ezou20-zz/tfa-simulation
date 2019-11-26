import py_school_match as psm
import random
import csv
from collections import defaultdict
from py_school_match.entities.student_queue import StudentQueue

schools_per_region_by_size = {"S": 20, "M": 60, "L": 100}
total_cap = 0

def print_matches(students):
    for student in students:
    if student.assigned_school is not None:
        print("Student {} was assigned to School {}".format(student.id, student.assigned_school.id))
    else:
        print("Student {} was not assigned to any school".format(student.id))

def create_schools():
    global total_cap, regions
    schools, regions = [], []
    with open('../data/schools.csv', newline='') as regions:
        filereader = csv.reader(regions, delimiter=',')
        for row in filereader:
            print(row)
            [region_name, size] = row
            region_cap = 0
            region_schools = []
            for i in range(schools_per_region_by_size[size]):
                capacity = random.randint(1,5)
                school = psm.School(capacity)
                school.category = region_name
                schools.append(school)
                region_schools.append(school)

                total_cap += capacity
                region_cap += capacity
            region = psm.Category(region_name, region_schools, region_cap)
            regions.append(region)
    print("TOTAL CAPACITY:", total_cap)
    return regions, schools

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
    regions, schools = create_schools()
    one_stage_matches = {} # dict mapping student id to School (objects)
    two_stage_matches = {} # same

    # TWO-STAGE MATCHING
    # stage 1: match between students and regions
    two_stage_planner = psm.SocialPlanner(students, regions, psm.RuleSet())
    two_stage_planner.run_matching(psm.DASTB(), preference_type="category")
    
    # stage 2: iterate through each region and match within
    for region in regions:
        region_students = region.assignation.get_all_students()
        region_schools = region.schools

        # reset student assignments, not sure if necessary
        for student in region_students:
            student.assigned_school = None

        # match between region's students and schools in region
        two_stage_planner = psm.SocialPlanner(region_students, region_schools, psm.RuleSet())
        two_stage_planner.run_matching(psm.DASTB())

        for student in region_students:
            two_stage_matches[student.id] = student.assigned_school

    # ONE-STAGE MATCHING
    one_stage_planner = psm.SocialPlanner(students, schools, psm.RuleSet())
    one_stage_planner.run_matching(psm.DASTB())
    for student in students:
        one_stage_matches[student.id] = student.assigned_school

    print("TWO-STAGE RESULT:", two_stage_matches)
    print("ONE-STAGE RESULT:", one_stage_matches)
    compare_matchings(one_stage_matches, two_stage_matches)




    planner = psm.SocialPlanner(students, schools, psm.RuleSet())

def test_dastb():
    planner.run_matching(psm.DASTB())
    assertEqual(st0.assigned_school.id, 0)
    assertEqual(st1.assigned_school.id, 1)
    assertEqual(st2.assigned_school.id, 2)


run_simulation()