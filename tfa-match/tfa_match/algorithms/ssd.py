"""This module implements the *Simple Serial Dictatorship* algorithm.
"""

from tfa_match.algorithms.abstract_matching_algorithm import AbstractMatchingAlgorithm


class SSD(AbstractMatchingAlgorithm):
    """This class implements the *Simple Serial Deictatorship* algorithm.
    
    This takes a list of teachers, a list of buckets and a ruleset
    (which is used to calculate priorities).
    This works by 'proposing' teachers to their most preferred
    (and available) bucket. buckets, on the other hand, accept
    or reject these teachers based on their priority.
    """

    def run(self, teachers, buckets, preference_type):
        """Runs the *Deferred Acceptance* algorithm.

        :param teachers: List of teachers.
        :type teachers: list
        :param buckets: List of bucket.
        :type buckets: list
        :param ruleset: Set of rules used.
        :type ruleset: Ruleset
        """

        for teacher in teachers:
            teacher_preferences = teacher.preferences
            if preference_type == "category":
                teacher_preferences = teacher.category_preferences
            if preference_type == "regional":
                teacher_preferences = teacher.regional_preferences
            for pref in teacher_preferences:
                if pref.capacity > len(pref.assignation):
                    SSD.assign_teacher(teacher, pref)
                    break

    @staticmethod
    def assign_teacher(teacher, bucket):
        """Assigns a teacher to a bucket."""
        teacher.assigned_bucket = bucket
        bucket.assignation.append(teacher)
