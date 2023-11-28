import pyaudio
import wave
import time


class AudioFile:
    chunk = 1024

    # Init audio stream
    def __init__(self, file):
        self.wf = wave.open(file, 'rb')
        self.p = pyaudio.PyAudio()
        # self.stream = self.p.open(
        #     format = self.p.get_format_from_width(self.wf.getsampwidth()), 
        #     channels = self.wf.getnchannels(), 
        #     rate = self.wf.getframerate(), 
        #     output = True
        #     )
        self.stream = self.p.open(
            format=8,
            channels=2,
            rate=44100,
            output=True
        )

    def get_stream(self):
        return self.wf

    def get_reader(self):
        return self.stream

    def get_object(self) -> pyaudio.PyAudio:
        return self.p

    # Play the entire file
    def play(self):
        # Read data by chunks so 1024 bytes at a time
        data = self.wf.readframes(self.chunk)
        while data != b'':
            self.stream.write(data)
            data = self.wf.readframes(self.chunk)

    # Shutdown the stream
    def close(self):
        self.stream.close()
        self.p.terminate()

    # if __name__ == '__main__':
    #     a = AudioFile("sample.wav")
    #     a.play()
    #     a.close()

    """-----------------------------Old Code-----------------------------------"""
    # location = "./sample.wav"

    # with wave.open(location, 'rb') as wf:
    #     # Define callback for playback (1)
    #     def callback(in_data, frame_count, time_info, status):
    #         data = wf.readframes(frame_count)
    #         # If len(data) is less than requested frame_count, PyAudio automatically
    #         # assumes the stream is finished, and the stream stops.
    #         return (data, pyaudio.paContinue)

    #     # Instantiate PyAudio and initialize PortAudio system resources (2)
    #     p = pyaudio.PyAudio()

    #     # Open stream using callback (3)
    #     stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
    #                     channels=wf.getnchannels(),
    #                     rate=wf.getframerate(),
    #                     output=True,
    #                     stream_callback=callback)

    #     # Wait for stream to finish (4)
    #     while stream.is_active():
    #         time.sleep(0.1)

    #     # Close the stream (5)
    #     stream.close()

    #     # Release PortAudio system resources (6)
    #     p.terminate()
    """----------------------------------------------------------------------------"""
