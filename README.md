speech-to-text
===
This repo uses some of the examples provided by Google to use their Speech to
Text API.

There is also a short reminder on how to get prepared to use it.

---
1. Ensure you have `gcloud` set up and that you have created and activated a service account. Follow the [Quickstart](https://cloud.google.com/speech-to-text/docs/quickstart-client-libraries) guide to set it up and get your credential key. You will need a credit card. The first hour is free, then it's around 1.44$ per hour. Keep
in mind that the first time you use Google API, you get 300$ of free credits and
one year to spend it.  
Once you have downloaded your credential key (a .json file), you will need to set
the `GOOGLE_APPLICATION_CREDENTIALS` variable to the path to the file. You could
set it in your .bashrc file, but then if you were to use multiple Google API paid service, it could conflict. A simple solution could be to set it in your python
script directly, and this is what we are going to do.  
At the beginning of each script, replace the following line
```
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'REPLACE_WITH_PATH_TO_CREDENTIALS'
```
with the right value. For instance, in my case it would be
```
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Users/me/Developer/nlp/STT/CCC-media-transcription.json'
```
2. Now that everything is prepared, we can use the example code provided by Google
to transcript a speech.
There are three kinds of scripts used in this example. One for audio files up to
one minute long, one for audio files up to 180 minutes long and one for streaming
input, when the source is a microphone. You can get all the details and differences
looking at the Google [documentation](https://cloud.google.com/speech-to-text/docs/how-to).  
We will just cover the case where audio file are shorter than one minute. To do
this, you must first transcode your audio file to a `FLAC` format with only one channel (mono). You can do this with `ffmpeg` very easily with the following command:
```
ffmpeg -i your_audio_file.wav -ac 1 output_file.flac
```
Then, you can use the transcribe.py script to get a transcript of your audio file.
It will print the result in the console as well as in a `result.txt` file.  
Finally, run
```
python3 transcribe.py output_file.flac
```
and enjoy
