class Config:
	def __init__(self):
		self.disable_lib_check = False
		self.user_data_dir = "./Asuna_data/Users/"
		self.app_data_dir = "./Asuna_data/server/"
		self.log_unknown = "./Asuna_data/server/unknown query.txt"
		self.log_location = "./"  # fallback log_location = "./"
		self.temp_file = "Asuna_data/temp/"

		self.cached_webpages_dir = self.temp_file + "cached_webpages/"


appConfig = Config()
