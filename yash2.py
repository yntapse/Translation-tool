import nltk
import os
import numpy as np
import speech_recognition as sr
from gtts import gTTS
import torch
from nltk.tokenize import word_tokenize

# Load data from file
marathi_sentences = []
english_sentences = []

# with open('marathi.txt', 'r', encoding='utf-8') as file:
#     for line in file:
#         line = line.strip().split('\t')
#         marathi_sentences.append(line[1])  # Extract only the first item (marathi)
#         english_sentences.append(line[0])  # Extract only the second item (English)

with open('marathi.txt', 'r', encoding='utf-8') as file:
    for line in file:
        line = line.strip().split(',')  # Split the line by comma
        marathi_sentences.append(line[1])  # Extract the second item (marathi)
        english_sentences.append(line[0]) 


# Tokenize the text data using nltk
nltk.download('punkt')  # Download the necessary nltk data
marathi_sequences = [word_tokenize(sentence) for sentence in marathi_sentences]
english_sequences = [word_tokenize(sentence) for sentence in english_sentences]

print("Kindly please wait for a moment till data load....")


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
marathi_sequences_padded = pad_sequences(marathi_sequences, maxlen=max_length, padding='post')
english_sequences_padded = pad_sequences(english_sequences, maxlen=max_length, padding='post')

# Define functions for speech recognition and text-to-speech synthesis
def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Speak in marathi:")
        audio = recognizer.listen(source)
    try:
        text = recognizer.recognize_google(audio, language='mr-IN')
        return text
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return None

# Inside synthesize_speech function
def synthesize_speech(text, output_file):
    tts = gTTS(text=text, lang='en')
    tts.save(output_file)
    os.system("mpg321 " + output_file)  



# Create translation dictionary
translation_dict = dict(zip(marathi_sentences, english_sentences))
# print("Translation dictionary:", translation_dict)

def translate_marathi_to_english(input_text):
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
        print("Input (marathi):", input_text)

        # Translation
        translated_text = translate_marathi_to_english(input_text)
        print("Translated (English):", translated_text)

        # Text-to-speech synthesis
        output_file = "translated_output.mp3"
        synthesize_speech(translated_text, output_file)
        print("Speech output saved to:", output_file)

if __name__ == "__main__":
    main()
