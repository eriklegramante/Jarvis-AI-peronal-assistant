import io
import speech_recognition as sr
from faster_whisper import WhisperModel
import torch

class JarvisListener:
    def __init__(self, model_size="tiny"):
        device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = WhisperModel(model_size, device=device, compute_type="int8")
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone(sample_rate=16000)

        self.model = WhisperModel("base", device=device, compute_type="int8")

    def listen(self):
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1.5) 
                self.recognizer.energy_threshold = 400
                self.recognizer.pause_threshold = 0.8
                
                print("\n[ESCUTANDO...]")
                try:
                    audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=8)
                except sr.WaitTimeoutError:
                    return ""

            try:
                print("[TRANSCREVENDO...]")
                audio_data = io.BytesIO(audio.get_wav_data())
                
                segments, info = self.model.transcribe(
                    audio_data, 
                    beam_size=5, 
                    language="pt",
                    initial_prompt="Jarvis, sistema, rede, comandos, computador, tecnologia.",
                    condition_on_previous_text=False, 
                    repetition_penalty=1.2,           
                    no_speech_threshold=0.6          
                )
                
                full_text = ""
                for segment in segments:
                    full_text += segment.text
                
                return full_text.strip()
        
            except Exception as e:
                return f"Erro na transcrição: {e}"