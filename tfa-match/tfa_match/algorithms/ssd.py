"""This module implements the *Simple Serial Dictatorship* algorithm.
"""

from tfa_match.algorithms.abstract_matching_algorithm import AbstractMatchingAlgorithm


class SSD(AbstractMatchingAlgorithm):
    """This class implements the *Simple Serial Deictatorship* algorithm.
    
    This takes a list of students, a list of buckets and a ruleset
    (which is used to calculate priorities).
    This works by 'proposing' students to their most preferred
    (and available) bucket. buckets, on the other hand, accept
    or reject these students based on their priority.
    """

    def run(self, students, buckets, preference_type):
        """Runs the *Deferred Acceptance* algorithm.

        :param students: List of students.
        :type students: list
        :param buckets: List of bucket.
        :type buckets: list
        :param ruleset: Set of rules used.
        :type ruleset: Ruleset
        """

        for student in students:
            student_preferences = student.preferences
            if preference_type == "category":
                student_preferences = student.category_preferences
            if preference_type == "regional":
                student_preferences = student.regional_preferences
            for pref in student_preferences:
                if pref.capacity > len(pref.assignation):
                    SSD.assign_student(student, pref)
                    break

    @staticmethod
    def assign_student(student, bucket):
        """Assigns a student to a bucket."""
        student.assigned_bucket = bucket
        bucket.assignation.append(student)
