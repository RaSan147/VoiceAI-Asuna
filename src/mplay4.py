from os import name as os_name
import random
from sys	import getfilesystemencoding

if os_name == 'nt':
	#from .windows import AudioClip as _PlatformSpecificAudioClip
	from ctypes import windll, c_buffer
	class PlaysoundException(Exception):
		pass

	def _ignore_playsound_exception(func):
		"""Decorator to ignore PlaysoundException."""
		def wrapper(*args, **kwargs):
			try:
				func(*args, **kwargs)
			except PlaysoundException:
				pass
		return wrapper

	# TODO: detect errors in all mci calls
	class _PlatformSpecificAudioClip(object):
		
		def directsend(self, command):
			buf = c_buffer(255)
			command = ''.join(command).encode(getfilesystemencoding())
			# command = ''.join(command)
			errorCode = int(windll.winmm.mciSendStringA(command, buf, 254, 0))
			if errorCode:
				errorBuffer = c_buffer(255)
				windll.winmm.mciGetErrorStringA(errorCode, errorBuffer, 254)
				exceptionMessage = ('\n	Error ' + str(errorCode) + ' for command:'
									'\n		' + command.decode() +
									'\n	' + errorBuffer.value.decode())

				if self.error:	raise PlaysoundException(exceptionMessage)
			return buf.value

		def __init__(self, filename, error=True):
			self.error = error
			#filename = filename.replace('/', '\\')
			self.filename = filename
			self._alias = 'yui_' + str(random.random())
			# print(self._alias)

			self.directsend('open "'+filename+'" alias ' +self._alias )
			self.directsend('set %s time format milliseconds' % self._alias)
			
			self._length_ms = int(self.directsend('status %s length' % self._alias).decode())
			#print(self._length_ms)
			#self.directsend('play %s from %d to %d'% (self._alias, 0, self._length_ms) )
		def volume(self, level):
			"""Sets the volume between 0 and 100."""
			assert level >=0 and level <= 100
			self.directsend('setaudio %s volume to %d' %
					(self._alias, level * 10) )
		def isvolume(self):
			return self.directsend('status %s volume' % self._alias) 

		def play(self, start_ms=None, end_ms=None):
			start_ms = 0 if not start_ms else start_ms
			end_ms = self._length_ms if not end_ms else end_ms
			buf=self.directsend('play %s from %d to %d' % (self._alias, start_ms, end_ms) )
			#print(buf)
			print(self._length_ms)
			return buf
		def _mode(self):
			# returns binary
			#print(self.directsend('status %s mode' % self._alias))
			return self.directsend('status %s mode' % self._alias) 
		
		def isrunning(self):
			return self._mode() == b'playing' or self._mode() == b'paused'
			
		def isplaying(self):
			return self._mode() == b'playing'


		def pause(self):
			self.directsend('pause %s' % self._alias)

		def resume(self):
			self.directsend('resume %s' % self._alias)

		def ispaused(self):
			return self._mode() == b'paused'

		def stop(self):
			self.directsend('stop %s' % self._alias)
			self.directsend('seek %s to start' % self._alias)

		def replay(self):
			self.directsend('stop %s' % self._alias)
			self.play()

		# TODO: this closes the file even if we're still playing.
		# no good.  detect isplaying(), and don't die till then!
		def close(self):
			self.directsend('close %s' % self._alias)
		def __del__(self):
			self.close()
else:
	raise Exception("mp3play can't run on your operating system.")


class AudioClip:

	def __init__(self, filename, error="all"):
		"""Create an AudioClip for the given filename."""
		self._error = error != "ignore"
		self._clip = _PlatformSpecificAudioClip(filename, self._error)

	def show_error(self):
		self._clip.error = True
		self._error = True # show all errors

	def play(self, start_ms=None, end_ms=None):
		"""
		Start playing the audio clip, and return immediately. Play from
		start_ms to end_ms if either is specified; defaults to beginning
		and end of the clip.  Returns immediately.  If end_ms is specified
		as smaller than start_ms, nothing happens.
		"""

		if end_ms != None and end_ms < start_ms:
			return
		else:
			return self._clip.play(start_ms, end_ms)

	def volume(self, level):
		"""Sets the volume between 0 and 100."""
		assert level >=0 and level <= 100
		return self._clip.volume(level)

	def isplaying(self):
		"""Returns True if the clip is currently playing.  Note that if a
		clip is paused, or if you called play() on a clip and playing has
		completed, this returns False."""
		return self._clip.isplaying()

	def pause(self):
		"""Pause the clip if it is currently playing."""
		return self._clip.pause()

	def resume(self):
		"""Unpause the clip if it is currently paused."""
		return self._clip.resume()

	def replay(self):
		return self._clip.replay()

	def isrunning(self):
		return self._clip.isrunning()

	def ispaused(self):
		"""Returns True if the clip is currently paused."""
		return self._clip.ispaused()

	def stop(self):
		"""Stop the audio clip if it is playing."""
		return self._clip.stop()

	def close(self):
		self._clip.close()

	def seconds(self):
		"""
		Returns the length in seconds of the audio clip, rounded to the
		nearest second.
		"""
		return int(round(float(self.milliseconds()) / 1000))

	def milliseconds(self):
		"""Returns the length in milliseconds of the audio clip."""
		return self._clip._length_ms
	def duration(self):
		return self.seconds()

	def is_volume(self):
		return self._clip.isvolume()

	
def load(filename, error="all"):
	"""Return an AudioClip for the given filename."""
	return AudioClip(filename, error)

if __name__=='__main__':
        x= load('songs/Date.m4a')
        x.play()
        print(x.is_volume())

