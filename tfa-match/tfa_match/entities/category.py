from tfa_match.entities.bucket import Bucket

class Category(Bucket):
	def __init__(self, name, buckets, capacity, id_=""):
		self.name = name
		self.buckets = buckets
		super(Category, self).__init__(capacity, id_)
		# print(self.get_ruleset())
