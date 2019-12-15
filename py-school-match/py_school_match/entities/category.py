from py_school_match.entities.school import School

class Category(School):
	def __init__(self, name, schools, capacity, id_=""):
		self.name = name
		self.schools = schools
		super(Category, self).__init__(capacity, id_)
		print("Category ID", self.id)
		# print(self.get_ruleset())
