# Translation-tool
The Translation Tool is Convert The voice To text and save audio and txt file of output its used to translate Marathi to English

Data Processing:  Loading Marathi and English sentences from a file.
Tokenizing the sentences using NLTK's word_tokenize function.
Padding the tokenized sequences to a maximum length.


Speech Recognition:  Utilizing the SpeechRecognition library to recognize speech input in Marathi.

Translation: Creating a translation dictionary to map Marathi sentences to their English translations.
Implementing a function to translate Marathi input text to English using the dictionary.

Text-to-Speech Synthesis:  Using the gTTS library to synthesize the translated English text into speech and save it as an MP3 file.
Playing the synthesized speech using the 'mpg321' command.


to run these project 
install libraries
NLTK
NUMPY
speech_recognition
pytorch


## to run this we use 
python yash2.py
