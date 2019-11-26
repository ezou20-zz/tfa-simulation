from py_school_match.entities.school import School

class Category(School):
	def __init__(self, name, schools, capacity, id_=""):
		self.name = name
		self.schools = schools
		self.capacity = capacity
		School.__init__(self, capacity, id_="")
