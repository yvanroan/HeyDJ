from pydub import AudioSegment
import base64
import io
import os


def sound_breathing(file):

    filename = os.path.join('/tmp', file.filename)
    file.save(filename)
    sound = AudioSegment.from_file(filename)
    print('yessa')
    # Convert to the desired format: 44100Hz, Mono, 16-bit PCM
    sound = sound.set_frame_rate(44100).set_channels(1).set_sample_width(2)

    # Export the audio to bytes
    buffer = io.BytesIO()
    sound.export(buffer, format="wav")
    bytes_audio = buffer.getvalue()

    # Encode the audio bytes to base64
    encoded_string = base64.b64encode(bytes_audio)

    # If you need the base64 string in text format
    encoded_text = encoded_string.decode('utf-8')

    return encoded_text