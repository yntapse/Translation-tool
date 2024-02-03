import nltk
import os
import numpy as np
import speech_recognition as sr
from gtts import gTTS
import torch
from nltk.tokenize import word_tokenize

# Load data from file
hindi_sentences = []
english_sentences = []

with open('hindi.txt', 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip().split('\t')
        hindi_sentences.append(line[1])  # Extract only the first item (Hindi)
        english_sentences.append(line[0])  # Extract only the second item (English)


# Tokenize the text data using nltk
nltk.download('punkt')  # Download the necessary nltk data
hindi_sequences = [word_tokenize(sentence) for sentence in hindi_sentences]
english_sequences = [word_tokenize(sentence) for sentence in english_sentences]

# Define padding function
def pad_sequences(sequences, maxlen, padding='post'):
    padded_sequences = []
    for sequence in sequences:
        if len(sequence) >= maxlen:
            padded_sequence = sequence[:maxlen]
        else:
            if padding == 'post':
                padded_sequence = sequence + [0] * (maxlen - len(sequence))
            else:
                padded_sequence = [0] * (maxlen - len(sequence)) + sequence
        padded_sequences.append(padded_sequence)
    return np.array(padded_sequences)

# Convert tokens to sequences
max_length = 100
hindi_sequences_padded = pad_sequences(hindi_sequences, maxlen=max_length, padding='post')
english_sequences_padded = pad_sequences(english_sequences, maxlen=max_length, padding='post')

print("Kindly please wait for a moment till data load....")

# Define functions for speech recognition and text-to-speech synthesis
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak in Hindi:")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='hi-IN')
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return None

# Inside synthesize_speech function
def synthesize_speech(text, output_file):
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)
    os.system("mpg321 " + output_file)  # Assuming mpg321 is installed for playing mp3 files

# Print out the loaded data
# print("Loaded Hindi sentences:", hindi_sentences)
# print("Loaded English sentences:", english_sentences)

# Create translation dictionary
translation_dict = dict(zip(hindi_sentences, english_sentences))
# print("Translation dictionary:", translation_dict)

def translate_hindi_to_english(input_text):
    translations = [value for key, value in translation_dict.items() if key == input_text]
    if translations:
        # return "{} -> {}".format(input_text, ", ".join(translations))
        return translations[0]
    else:
        return "Translation not found for '{}'.".format(input_text)
# Main function
def main():
    # Speech recognition
    input_text = recognize_speech()
    if input_text:
        print("Input (Hindi):", input_text)

        # Translation
        translated_text = translate_hindi_to_english(input_text)
        print("Translated (English):", translated_text)

        # Text-to-speech synthesis
        output_file = "translated_output.mp3"
        synthesize_speech(translated_text, output_file)
        print("Speech output saved to:", output_file)

if __name__ == "__main__":
    main()
