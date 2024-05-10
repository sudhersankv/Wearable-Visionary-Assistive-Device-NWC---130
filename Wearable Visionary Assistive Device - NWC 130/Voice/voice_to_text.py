import whisper

def voice_to_text():

    model = whisper.load_model('small')

    result = model.transcribe(r"recorded.wav",fp16=False)

    final_result = result["text"]
    return final_result
