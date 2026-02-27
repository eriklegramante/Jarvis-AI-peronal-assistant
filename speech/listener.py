import io
import speech_recognition as sr
from faster_whisper import WhisperModel
import torch

class JarvisListener:
    def __init__(self, model_size="tiny"):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = WhisperModel(model_size, device=device, compute_type="int8")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self):
        """Ouve o áudio do microfone e transcreve para texto."""
        with self.microphone as source:
            print("\n[OUVINDO...] Pode falar, senhor.")
            self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = self.recognizer.listen(source)

        try:
            print("[PROCESSANDO VOZ...]")
            audio_data = io.BytesIO(audio.get_wav_data())
            
            segments, info = self.model.transcribe(audio_data, beam_size=5, language="pt")
            
            text = "".join([segment.text for segment in segments]).strip()
            return text
        
        except Exception as e:
            return f"Erro na transcrição: {e}"