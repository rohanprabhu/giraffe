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

	@classmethod
	def add_expense(self, user, title, bills, date):
		username, password = ds.get_credentials(user)
		credentials = Credentials(username, password)

		self.dividely.add_expense(credentials, title, bills, datetime.date.today().strftime("%m/%d/%Y"))
