import py_school_match as psm
import random
import csv
from collections import defaultdict
from py_school_match.entities.student_queue import StudentQueue

schools_per_region_by_size = {"S": 10, "M": 30, "L": 50}

def print_matches(students):
    for student in students:
        if student.assigned_school is not None:
            print("Student {} was assigned to School {}".format(student.id, student.assigned_school.id))
        else:
            print("Student {} was not assigned to any school".format(student.id))

def create_schools():
    schools, regions = [], []
    total_capacity = 0

    # get region names and sizes from data file
    with open('../data/schools.csv', newline='') as datafile:
        filereader = csv.reader(datafile, delimiter=',')
        for row in filereader:
            [region_name, size] = row
            region_capacity = 0
            region_schools = []
            region_size = schools_per_region_by_size[size]

            # iterate through # of schools in region and create schools w/ random caps
            for i in range(region_size):
                capacity = random.randint(1,5)
                school = psm.School(capacity)
                school.category = region_name
                schools.append(school)
                region_schools.append(school)

                total_capacity += capacity
                region_capacity += capacity
            region = psm.Category(region_name, region_schools, region_capacity)
            regions.append(region)
    print("TOTAL CAPACITY:", total_capacity)
    return regions, schools

def create_students(regions, schools):
    students = []
    # set student.category_preferences to random order over regions
    # for each region in order, randomly sort region's schools and add to student.preferences
    return students

    # EXAMPLES
    # sc0 = psm.School(1)
    # sc1 = psm.School(1)
    # sc2 = psm.School(1)

    # st0 = psm.Student()
    # st1 = psm.Student()
    # st2 = psm.Student()

    # st0.preferences = [sc0, sc1, sc2]
    # st1.preferences = [sc0, sc2, sc1]
    # st2.preferences = [sc2, sc1, sc0]

def permute_preferences(students, k):
    # for each student, randomly swap k times within student.preferences
    return 

def compare_matchings(matching1, matching2):
    pass

def get_k_matchings(k, regions, schools, students):
    one_stage_matches = {} # dict mapping student id to School (objects)
    two_stage_matches = {} # same

    permute_preferences(students, k)
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

    # print("TWO-STAGE RESULT:", two_stage_matches)
    # print("ONE-STAGE RESULT:", one_stage_matches)
    return one_stage_matches, two_stage_matches

def run_simulation():
    random.seed(42)

    psm.Student.reset_ids()
    psm.School.reset_ids()
    
    regions, schools = create_schools()
    students = create_students(regions, schools)

    # eventually loop for different k
    k = 0
    one_stage_matches, two_stage_matches = get_k_matchings(k, regions, schools, students)
    compare_matchings(one_stage_matches, two_stage_matches)


run_simulation()