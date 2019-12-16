"""This module defines an abstract class for other algorithms."""

from abc import ABCMeta, abstractmethod


class AbstractMatchingAlgorithm(metaclass=ABCMeta):
    """Abstract class for matching algorithms.
    Defined, using ABCMeta.
    """

    @abstractmethod
    def run(self, teachers, buckets, ruleset):
        """
        Abstract method algorithms should implement.
        
        :param teachers: List of teachers.
        :type teachers: list
        :param buckets: List of buckets.
        :type buckets: list
        :param ruleset: The ruleset to be used.
        :type ruleset: Ruleset
        """
        pass


