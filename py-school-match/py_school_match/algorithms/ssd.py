"""This module implements the *Simple Serial Dictatorship* algorithm.
"""

from py_school_match.algorithms.abstract_matching_algorithm import AbstractMatchingAlgorithm


class SSD(AbstractMatchingAlgorithm):
    """This class implements the *Simple Serial Deictatorship* algorithm.
    
    This takes a list of students, a list of schools and a ruleset
    (which is used to calculate priorities).
    This works by 'proposing' students to their most preferred
    (and available) school. Schools, on the other hand, accept
    or reject these students based on their priority.
    """

    def run(self, students, schools, preference_type):
        """Runs the *Deferred Acceptance* algorithm.

        :param students: List of students.
        :type students: list
        :param schools: List of school.
        :type schools: list
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
    def assign_student(student, school):
        """Assigns a student to a school."""
        student.assigned_school = school
        school.assignation.append(student)
