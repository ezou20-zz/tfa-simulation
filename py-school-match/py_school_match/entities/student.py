"""This module defines a student."""

from collections import defaultdict
from itertools import count


class Student:
    """This class defines a student."""

    __id_counter = count(0)
    """This is used to generate an incremental id."""

    def __init__(self, id_=""):
        """Initializes a student.

        :param id_: Any unique identifier.
        :type id_: Any.
        """
        self._id = id_ if id_ else next(Student.__id_counter)
        self.preferences = []
        self.category_preferences = []
        self.regional_preferences = []

        # self.__characteristics = defaultdict(list)

        self.assigned_school = None

    @property
    def id(self):
        return self._id

    @staticmethod
    def reset_ids():
        """Resets the incremental id."""
        Student.__id_counter = count(0)
