from datetime import datetime
import pyaudio
import wave

class AudioStream:
	def __init__(self, chunk = None, format = None, channels = None, rate = None, record_seconds = None, output_filename = None):
		if chunk == None:
			self.chunk = 1024 # Declare blocks of data to collect
		else:
			self.chunk = chunk
		if format == None:
			self.format = pyaudio.paInt16 # Declare format
		else:
			self.format = format
		if channels == None:
			self.channels = 1 # Declare number of channels
		else:
			self.channels = channels
		if rate == None:
			self.rate = 48000 # Declare sample per second
		else:
			self.rate = rate
		if record_seconds == None:
			self.record_seconds = 20 # Declare how many seconds to record
		else:
			self.record_records = record_seconds
		if output_filename == None:
			self.output_filename = "output.wav" # Declare output filename
		else:
			self.output_filename = output_filename

	def record(self):
		print("PyAudio recording '" + self.output_filename + "' started - "  + self.time())
		try:
			while True:
				p = pyaudio.PyAudio() # Declare pyaudio instance

				stream = p.open(format=self.format,
				                channels=self.channels,
				                rate=self.rate,
				                input=True,
								output=True,
				                frames_per_buffer=self.chunk,
								input_device_index=2) # Start audio stream of computer and audio

				self.frames = [] # Declare frame hold
				for i in range(0, int(self.rate / self.chunk * self.record_seconds)): # For each
					data = stream.read(self.chunk) # Read in a frame
					self.frames.append(data) # Append frame - Not sure if we actually need this considering zoom record
					# Do stuff
		except KeyboardInterrupt:
			stream.stop_stream()
			stream.close()
			p.terminate()
			print("PyAudio recording '" + self.output_filename + "' stopped - " + self.time())
			print(len(self.frames), " frames recorded...\n")
			print('Reformatting audio file to .wav...')
			wf = wave.open(self.output_filename, 'wb') # Format output
			wf.setnchannels(self.channels)
			wf.setsampwidth(p.get_sample_size(self.format))
			wf.setframerate(self.rate)
			wf.writeframes(b''.join(self.frames))
			wf.close()
			print('Reformatting complete, audio file successfully saved')

	def time(self):
		return datetime.now().strftime("%m/%d/%Y %H:%M:%S")

	def attributes(self):
		print(self.__dict__)
