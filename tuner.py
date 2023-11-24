import pyaudio
import random
import numpy as np
from scipy.fftpack import fft
from colorama import Fore, Style


note_freq = {
    "E1": {
        "E": 82.41,
        "F": 87.31,
        "F#": 92.50,
        "G": 98.00,
        "G#": 103.83,
        "A": 110.00,
        "Bb": 116.54,
        "B": 123.47,
        "C": 130.81,
        "C#": 138.59,
        "D": 146.83,
        "D#": 155.56
    },
    "A": {
        "A": 110.00,
        "Bb": 116.54,
        "B": 123.47,
        "C": 130.81,
        "C#": 138.59,
        "D": 146.83,
        "D#": 155.56,
        "E": 164.81,
        "F": 174.61,
        "F#": 185.00,
        "G": 196.00,
        "G#": 207.65
    },
    "D": {
        "D": 146.83,
        "D#": 155.56,
        "E": 164.81,
        "F": 174.61,
        "F#": 185.00,
        "G": 196.00,
        "G#": 207.65,
        "A": 220.00,
        "Bb": 233.08,
        "B": 246.94,
        "C": 261.63,
        "C#": 277.18
    },
    "G": {
        "G": 196.00,
        "G#": 207.65,
        "A": 220.00,
        "Bb": 233.08,
        "B": 246.94,
        "C": 261.63,
        "C#": 277.18,
        "D": 293.66,
        "D#": 311.13,
        "E": 329.63,
        "F": 349.23,
        "F#": 369.99
    },
    "B": {
        "B": 246.94,
        "C": 261.63,
        "C#": 277.18,
        "D": 293.66,
        "D#": 311.13,
        "E": 329.63,
        "F": 349.23,
        "F#": 369.99,
        "G": 392.00,
        "G#": 415.30,
        "A": 440.00,
        "Bb": 466.16
    },
    "E6": {
        "E": 329.63,
        "F": 349.23,
        "F#": 369.99,
        "G": 392.00,
        "G#": 415.30,
        "A": 440.00,
        "Bb": 466.16,
        "B": 493.88,
        "C": 523.25,
        "C#": 554.37,
        "D": 587.33,
        "D#": 622.25
    }
}


# Return n'th value of the dictionary
def get_nth_key(dictionary, n=0):
    if n < 0:
        n += len(dictionary)
    for i, key in enumerate(dictionary.keys()):
        if i == n:
            return key
    raise IndexError("dictionary index out of range")


# Function to calculate the frequency from the FFT result
def calculate_frequency(data, rate):
    n = len(data)
    k = np.arange(n)
    t = n / rate
    frq = k / t
    frq = frq[range(n // 2)]
    Y = fft(data) / n
    Y = Y[range(n // 2)]

    return frq, abs(Y)


# Function to find the dominant frequency
def find_dominant_frequency(frequencies, magnitudes):
    index = np.argmax(magnitudes)
    return frequencies[index]


# Function to check if the played note matches the target note
def check_note(target_frequency, played_frequency, tolerance=5):
    return abs(target_frequency - played_frequency) < tolerance


# Function to set up the game
def setup():
    string = list(input(
        "Please enter which string you want to practice.\n(Options: E1, A, D, G, B, E6): ").split())
    print(string)
    mult_strings = len(string) >= 2
    print(mult_strings)
    print(random.randint(0, 9))
    return note_freq.get(string[0])


# Main function to listen to the microphone and check the played note
def play_note_game(string):
    # target_note_frequency =
    chunk = 1024  # Number of frames per buffer
    FORMAT = pyaudio.paInt16  # Audio format (16-bit PCM)
    CHANNELS = 1  # Number of audio channels (1 for mono, 2 for stereo)
    RATE = 44100  # Sample rate (samples per second)

    p = pyaudio.PyAudio()
    stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True,
                    frames_per_buffer=chunk)

    try:
        while True:
            data = np.frombuffer(stream.read(chunk), dtype=np.int16)
            frequencies, magnitudes = calculate_frequency(data, RATE)
            dominant_frequency = find_dominant_frequency(
                frequencies, magnitudes)

            if check_note(target_frequency, dominant_frequency):
                print(f"{Fore.GREEN}Correct!{Style.RESET_ALL}")
                break
            else:
                print(f"{Fore.RED}Incorrect. Try again.{Style.RESET_ALL}")

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        stream.stop_stream()
        stream.close()
        p.terminate()
        print("Stream closed.")


if __name__ == "__main__":
    print(get_nth_key(note_freq.get("A"), 7))
    # string = setup()
    # print(note_freq.at(0))
    # play_note_game(string)
