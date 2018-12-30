#!/usr/bin/env python

# Copyright 2017 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Google Cloud Speech API sample application using the REST API for async
batch processing.

Example usage:
    python transcribe_async.py resources/audio.raw
    python transcribe_async.py gs://cloud-samples-tests/speech/vr.flac
"""

import argparse
import io
import os


os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'REPLACE_WITH_PATH_TO_CREDENTIALS'


def transcribe_file(speech_file):
    """Transcribe the given audio file asynchronously."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    config = types.RecognitionConfig(
        # encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        model='video',
        language_code='en-US',
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    with io.open('result.txt', 'w') as result_file:
        for result in response.results:
            # The first alternative is the most likely one for this portion.
            txt = result.alternatives[0].transcript
            confidence = result.alternatives[0].confidence
            print(u'Transcript with confidence {}:\n{}'.format(confidence, txt))
            result_file.write('Result confidence: {}\n'.format(confidence))
            result_file.write(txt)
            # alternative = result.alternatives[0]
            # for word_info in alternative.words:
            #     word = word_info.word
            #     start_time = word_info.start_time
            #     end_time = word_info.end_time
            #     print('Word: {}, start_time: {}, end_time: {}'.format(
            #         word,
            #         start_time.seconds + start_time.nanos * 1e-9,
            #         end_time.seconds + end_time.nanos * 1e-9))
            #     result_file.write('Word: {}, start_time: {}, end_time: {}'.format(
            #         word,
            #         start_time.seconds + start_time.nanos * 1e-9,
            #         end_time.seconds + end_time.nanos * 1e-9))


def transcribe_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""
    from google.cloud import speech
    from google.cloud.speech import enums
    from google.cloud.speech import types
    client = speech.SpeechClient()

    audio = types.RecognitionAudio(uri=gcs_uri)
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        model='video',
        language_code='en-US',
        enable_automatic_punctuation=True,
        enable_word_time_offsets=True)

    operation = client.long_running_recognize(config, audio)

    print('Waiting for operation to complete...')
    response = operation.result(timeout=90)

    # Each result is for a consecutive portion of the audio. Iterate through
    # them to get the transcripts for the entire audio file.
    with io.open('result.txt', 'w') as result_file:
        for result in response.results:
            # The first alternative is the most likely one for this portion.
            txt = result.alternatives[0].transcript
            confidence = result.alternatives[0].confidence
            print(u'Transcript with confidence {}:\n{}'.format(confidence, txt))
            result_file.write('Result confidence: {}\n'.format(confidence))
            result_file.write(txt)
            # alternative = result.alternatives[0]
            # for word_info in alternative.words:
            #     word = word_info.word
            #     start_time = word_info.start_time
            #     end_time = word_info.end_time
            #     print('Word: {}, start_time: {}, end_time: {}'.format(
            #         word,
            #         start_time.seconds + start_time.nanos * 1e-9,
            #         end_time.seconds + end_time.nanos * 1e-9))
            #     result_file.write('Word: {}, start_time: {}, end_time: {}'.format(
            #         word,
            #         start_time.seconds + start_time.nanos * 1e-9,
            #         end_time.seconds + end_time.nanos * 1e-9))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'path', help='File or GCS path for audio file to be recognized')
    args = parser.parse_args()
    if args.path.startswith('gs://'):
        transcribe_gcs(args.path)
    else:
        transcribe_file(args.path)
