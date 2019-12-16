"""This module defines a social planner."""

class SocialPlanner:
    """This class defines a social planner. 
    A social planner is used to run a algorithm
    using a group of teachers, a group of buckets
    and a set of rules.
    """

    def __init__(self, teachers, buckets):
        """Initializes a slot.
        :param teachers: A list of teachers.
        :type teachers: list.
        :param buckets: A list of bucket
        :type buckets: list.
        :param ruleset: The set of rules. By default, it uses the
        same ruleset in every bucket.
        :type ruleset: :class:`.Ruleset`.
        """
        self.teachers = teachers
        self.buckets = buckets
        # self.preference_type = preference_type
        # self.ruleset = ruleset if ruleset else RuleSet()

        # self.assign_same_ruleset()  # By default it assigns the same ruleset to every bucket.            

    # def assign_same_ruleset(self):
    #     """Assigns the same ruleset to every bucket."""
    #     for bucket in self.buckets:
    #         bucket.set_ruleset_n_reset(self.ruleset)  # ToDo: The assignation should update itself!

    def run_matching(self, algorithm, preference_type = None):
        """Run the algorithm."""
        algorithm.run(self.teachers, self.buckets, preference_type)

    # @staticmethod
    # def change_ruleset(bucket, ruleset):
    #     """Changes the ruleset used in a bucket."""
    #     bucket.ruleset = ruleset
    #     bucket.reset_assignation()