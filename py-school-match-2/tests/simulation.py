from . import py_school_match as psm
import random

def run_simulation():
    random.seed(42)

    psm.Student.reset_ids()
    psm.School.reset_ids()

    st0 = psm.Student()
    st1 = psm.Student()
    st2 = psm.Student()

    schools = []
    schools_per_region_by_size = {"S": 25, "M": 75, "L": 125}
    students = []
    total_cap = 0
    create_schools()
    print(total_cap)

    def create_schools():
        with open('data/schools.csv', newline='') as regions:
            filereader = csv.reader(regions, delimiter=',')
            for row in filereader:
                region = row[0] 
                size = row[1]
                for i in range(schools_per_region_by_size[size]):
                    school = psm.School()
                    school.category = region
                    school.capacity = random.randint(1,5)
                    schools.append(school)
                    total_cap += school.capacity


    # def create_students():


    st0.preferences = [sc0, sc1, sc2]
    st1.preferences = [sc0, sc2, sc1]
    st2.preferences = [sc2, sc1, sc0]

    planner = psm.SocialPlanner(students, schools, psm.RuleSet())

def test_dastb():
    planner.run_matching(psm.DASTB())
    assertEqual(st0.assigned_school.id, 0)
    assertEqual(st1.assigned_school.id, 1)
    assertEqual(st2.assigned_school.id, 2)

run_simulation()