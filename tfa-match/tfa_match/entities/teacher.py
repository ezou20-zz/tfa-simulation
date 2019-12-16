"""This module defines a teacher."""

from collections import defaultdict
from itertools import count


class Teacher:
    """This class defines a teacher."""

    __id_counter = count(0)
    """This is used to generate an incremental id."""

    def __init__(self, id_=""):
        """Initializes a teacher.

        :param id_: Any unique identifier.
        :type id_: Any.
        """
        self._id = id_ if id_ else next(Teacher.__id_counter)
        self.original_preferences = []
        self.preferences = []
        self.category_preferences = []
        self.regional_preferences = []

        # self.__characteristics = defaultdict(list)

        self.assigned_bucket = None

    @property
    def id(self):
        return self._id

    @staticmethod
    def reset_ids():
        """Resets the incremental id."""
        Teacher.__id_counter = count(0)
