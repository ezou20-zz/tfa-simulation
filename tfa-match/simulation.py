import tfa_match as tm
import random
import math
import csv
from collections import defaultdict
import matplotlib.pyplot as plt

fig_dir = "figures/"

# S: 0-50
# M: 50-100
# L: 100-200
buckets_per_region_by_size = {"S": (1, 5), "M": (5, 10), "L": (10, 20)}

region_size = 10

def print_matches(students):
    for student in students:
        if student.assigned_bucket is not None:
            print("Student {} was assigned to bucket {}".format(student.id, student.assigned_bucket.id))
        else:
            print("Student {} was not assigned to any bucket".format(student.id))

def create_buckets():
    buckets, regions = [], []
    total_capacity = 0

    # get region names and sizes from data file
    with open('../data/regions_small.csv', newline='') as datafile:
        filereader = csv.reader(datafile, delimiter=',')
        for row in filereader:
            [region_name, size] = row
            lower, upper = buckets_per_region_by_size[size]
            region_buckets = []
            region_capacity = 0

            # iterate through # of "buckets" in region and create buckets w/ random caps
            for _ in range(region_size):
                bucket_capacity = random.randint(lower, upper)
                bucket = tm.Bucket(bucket_capacity)
                bucket.category = region_name
                buckets.append(bucket)
                region_buckets.append(bucket)
                region_capacity += bucket_capacity
                total_capacity += bucket_capacity
                # region_capacity += bucket_capacity

            # initialize region as Category object with list of buckets
            region = tm.Category(region_name, region_buckets, region_capacity)
            for bucket in region_buckets:
                bucket.category = region
            regions.append(region)

    print("TOTAL CAPACITY:", total_capacity)
    print("TOTAL bucketS: ", len(buckets))
    print("TOTAL REGIONS: ", len(regions))
    return regions, buckets, total_capacity

def create_students(regions, buckets, total_capacity):
    students = []
    num_students = int(total_capacity * 0.8)

    # set student.category_preferences to random order over regions
    # for each region in order, randomly sort region's buckets and add to student.preferences
    for i in range(num_students):
        student = tm.Student()
        bucket_prefs = []
        region_prefs = [region for region in regions]
        random.shuffle(region_prefs)
        student.category_preferences = region_prefs

        for region in region_prefs:
            region_bucket_prefs = [i for i in region.buckets]
            random.shuffle(region_bucket_prefs)
            bucket_prefs.extend(region_bucket_prefs)

        student.preferences = bucket_prefs.copy()
        student.original_preferences = bucket_prefs.copy()
        students.append(student)

    print("TOTAL STUDENTS: ", len(students))
    return students

def permute_preferences(students, k_array):
    # for each student i, randomly swap k_array[i] times within student.preferences
    # using array allows for different degrees of randomness between students
    for i in range(len(students)):
        student = students[i]
        lst = student.original_preferences.copy()
        num_buckets = len(lst)
        for _ in range(k_array[i]):
            i1,i2 = random.sample(range(num_buckets), 2)
            lst[i1], lst[i2] = lst[i2], lst[i1]
        student.preferences = lst
    return 

def compare_matchings(students, matching1, matching2):
    # total utilities of matcing1 and matching2
    matching1_utility = 0
    matching2_utility = 0

    # total number of students better off in matching 1
    total_better = 0

    # total number of students with same matching
    total_same = 0

    # total number of students worse off in matching 1
    total_worse = 0

    # total change in utility (based on rank of buckets matched per student) from matching 1 to 2
    delta_rank_utility = 0
    for student in students:
        prefs = student.preferences
        s_id = student.id
        bucket1_rank = prefs.index(matching1[s_id])
        matching1_utility -= bucket1_rank
        bucket2_rank = prefs.index(matching2[s_id])
        matching2_utility -= bucket2_rank
        delta_rank_utility += bucket1_rank - bucket2_rank
        if bucket1_rank > bucket2_rank: total_better += 1
        elif bucket1_rank == bucket2_rank: total_same += 1
        else: total_worse += 1

    return {
        "better": total_better,
        "same": total_same,
        "worse": total_worse,
        "delta": delta_rank_utility,
        "matching1_utility": matching1_utility,
        "matching2_utility": matching2_utility,
    }


def get_matchings(k_array, regions, buckets, students):
    one_stage_matches = {} # dict mapping student id to bucket (objects)
    two_stage_matches = {} # same

    # reset all assignments
    for student in students:
        student.assigned_bucket = None
    for bucket in buckets:
        bucket.reset_assignation()
    for region in regions:
        region.reset_assignation()

    print("Permuting preferences...")
    permute_preferences(students, k_array)

    print("Starting one-stage")
    # ONE-STAGE MATCHING
    one_stage_planner = tm.SocialPlanner(students, buckets)
    one_stage_planner.run_matching(tm.SSD())
    for student in students:
        one_stage_matches[student.id] = student.assigned_bucket

    for student in students:
        student.assigned_bucket = None
    for bucket in buckets:
        bucket.reset_assignation()

    # TWO-STAGE MATCHING
    print("Starting two-stage")
    print("Starting stage 1")

    # stage 1: match between students and regions
    two_stage_planner = tm.SocialPlanner(students, regions)
    two_stage_planner.run_matching(tm.SSD(), preference_type="category")
    
    print("Starting stage 2")

    # stage 2: iterate through each region and match within
    for region in regions:
        region_students = region.assignation
        region_buckets = region.buckets

        # reset student assignments, not sure if necessary
        for student in region_students:
            student.regional_preferences = [bucket for bucket in student.preferences if bucket.category.id == student.assigned_bucket.id]
            student.assigned_bucket = None

        # match between region's students and buckets in region
        two_stage_planner = tm.SocialPlanner(region_students, region_buckets)
        two_stage_planner.run_matching(tm.SSD(), preference_type="regional")

        for student in region_students:
            two_stage_matches[student.id] = student.assigned_bucket

    # print("ONE-STAGE RESULT:", {k:v.id for k, v in one_stage_matches.items()})
    # print("TWO-STAGE RESULT:", {k:v.id for k, v in two_stage_matches.items()})
    return one_stage_matches, two_stage_matches

def print_buckets(buckets):
    for bucket in buckets:
        print("bucket " + str(bucket.id))
        print("Capacity: ", bucket.capacity)
        print("Category: ", bucket.category)
        print("Assignation: ", [student.id for student in bucket.assignation])
        print()

def print_students(students):
    for student in students:
        print("STUDENT " + str(student.id))
        print("bucket Prefs: ", [bucket.id for bucket in student.preferences])
        print("Region Prefs: ", [region.id for region in student.category_preferences])
        print("bucket Assignment: ", student.assigned_bucket.id if student.assigned_bucket else None)
        print()

def graph_results(ks, results):
    deltas = [r["delta"] for r in results]
    matching1_utilities = [r["matching1_utility"] for r in results]
    matching2_utilities = [r["matching2_utility"] for r in results]
    print("*************************RESULTS*************************")
    print("Ks: ", ks)
    print("Deltas: ", deltas)
    print("Matching1 Utility: ", matching1_utilities)
    print("Matching2 Utility: ", matching2_utilities)

    f = plt.figure()
    plt.plot(ks, deltas, marker='o')
    plt.ylabel("Change in Utility")
    plt.xlabel("K")
    plt.title("Change in Total Welfare from One-Stage to Two-Stage")
    f.savefig(fig_dir + "delta-utility-1stage-2stage.png", bbox_inches='tight')
    f.clear()
    plt.close(f)

    f = plt.figure()
    plt.plot(ks, matching1_utilities, marker='o')
    plt.ylabel("Utility")
    plt.xlabel("K")
    plt.title("One-Stage Matching Utilities")
    f.savefig(fig_dir + "1stage-utility.png", bbox_inches='tight')
    f.clear()
    plt.close(f)

    f = plt.figure()
    plt.plot(ks, matching2_utilities, marker='o')
    plt.ylabel("Utility")
    plt.xlabel("K")
    plt.title("Two-Stage Matching Utilities")
    f.savefig(fig_dir + "2stage-utility.png", bbox_inches='tight')
    f.clear()
    plt.close(f)

def run_simulation():
    random.seed(42)
    print("Starting simulation...")
    # tm.Student.reset_ids()
    # tm.Bucket.reset_ids()
    print("creating buckets....")
    regions, buckets, total_capacity = create_buckets()
    print("creating students....")
    students = create_students(regions, buckets, total_capacity)

    # eventually loop for different k_arrays
    # using array allows for different degrees of randomness between students
    # eg. first half completely parameterized by region, second half very random

    print("************** Varying K *****************")
    results = []
    ks = [i for i in range(0, 100, 10)] + [i for i in range(100, 1000, 50)] + [i for i in range(1000, 2000, 100)]
    for k in ks:
        print("********** K = " + str(k) + " ************")
        k_array = [k] * len(students)
        print("Get Matchings: k = " + str(k))
        one_stage_matches, two_stage_matches = get_matchings(k_array, regions, buckets, students)
        
        match_results = compare_matchings(students, one_stage_matches, two_stage_matches)
        print(match_results)
        results.append(match_results)
        
    graph_results(ks, results)

    print("**************** Varying Proportion that are Random ******************")
    proportions = [i for i in range(0, len(students), 150)]
    for k in [50, 100, 250, 500, 1000]:
        print("************* K = " + str(k) + " ******************")
        different_randomness_results = []
        for i in proportions:
            print("*************** proportion: " + str(round((i/len(students))*100, 2)) + " ****************")
            k_array = [0] * (len(students) - i) + [k] * i
            one_stage_matches, two_stage_matches = get_matchings(k_array, regions, buckets, students)
        
            match_results = compare_matchings(students, one_stage_matches, two_stage_matches)
            print(match_results)
            different_randomness_results.append(match_results)

        x_vals = [round((i/len(students))*100, 2) for i in proportions]
        f = plt.figure()
        plt.plot(x_vals, [m["delta"] for m in different_randomness_results], marker='o')
        plt.ylabel("Utility")
        plt.xlabel("Proportion with Randomness (%)")
        plt.title("Change in Welfare with Varying Proportion of Teachers with Random Preferences (K = " + str(k) + ")")
        f.savefig(fig_dir + "proportions-k-" + str(k) + ".png", bbox_inches='tight')
        f.clear()
        plt.close(f)

run_simulation()


