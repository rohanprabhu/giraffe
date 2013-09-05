from lib.data.datastore import DataStore
from lib.dividely.dividelymanager import DividelyManager
from lib.dividely.credentials import Credentials

class GiraffeHandler:
	ds = None
	dividely = None

	@classmethod
	def __init__(self):
		self.ds = DataStore()
		self.dividely = DividelyManager()
		self.ds.connect()

	@classmethod
	def add_expense(self, user, title, bills, date):
		username, password = self.ds.get_credentials(user)

		if(username == None or password == None):
			return False

		credentials = Credentials(username, password)
		short_codes = [x[1] for x in bills]
		_x = [x for x in self.ds.get_friends_list(user, short_codes)]
		emails = {x["short_code"]: x["email"] for x in self.ds.get_friends_list(user, short_codes)}

		bill_objects = []

		for bill in bills:
			bill_objects.append((bill[0], emails[bill[1]]))

		print bill_objects

		self.dividely.add_expense(credentials, title, bills, datetime.date.today().strftime("%m/%d/%Y"))
		return True

	@classmethod
	def get_accounts(self, user):
		username, password = self.ds.get_credentials(user)

		return self.dividely.get_accounts(Credentials(username, password))

	@classmethod
	def __del__(self):
		try:
			self.ds.disconnect()
		except:
			pass

