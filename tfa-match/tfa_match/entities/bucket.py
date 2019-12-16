"""This module defines a bucket."""

from itertools import count

class Bucket:
    """This class defines bucket."""

    __id_counter = count(0)
    """This is used to generate an incremental id."""

    def __init__(self, capacity, id_=""):
        """Initializes a bucket.

        :param capacity: The maximum number of students.
        :type capacity: int.
        :param id_: Any unique identifier.
        :type id_: Any.
        """
        self.id = id_ if id_ else next(Bucket.__id_counter)
        self.capacity = capacity
        self.category = None
        self.assignation = []

    def reset_assignation(self):
        """Resets the assignations of the bucket."""
        self.assignation = []

    @staticmethod
    def reset_ids():
        """Resets the incremental id."""
        Bucket.__id_counter = count(0)
