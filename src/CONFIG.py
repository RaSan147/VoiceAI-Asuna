import os


class Config:
	def __init__(self):
		self.disable_lib_check = False
		self.file_dir = os.path.dirname(os.path.realpath(__file__))
		self.ftp_dir = os.path.join(self.file_dir, 'page')
		self.main_data_dir = os.path.join(self.file_dir, "Asuna_data/")
		self.user_data_dir = os.path.join(self.main_data_dir, "Users/")
		self.app_data_dir = os.path.join(self.main_data_dir, "server/")
		self.log_unknown = os.path.join(self.main_data_dir, "server/unknown query.txt")
		self.log_location = os.path.join(self.main_data_dir, "server/")  # fallback log_location = "./"
		self.temp_file = os.path.join(self.main_data_dir, "temp/")
		self.audio_file = os.path.join(self.temp_file, "audio/")

		self.cached_webpages_dir = self.temp_file + "cached_webpages/"

		self.allow_dl_data = True


appConfig = Config()
