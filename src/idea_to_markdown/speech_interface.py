import openai
import pyaudio
import wave
import time
import os
import tempfile
from pathlib import Path

# Configuration for audio recording
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024


class SpeechInterface:
    """
    Handles real-time voice interaction using OpenAI's services.
    Provides speech-to-text and text-to-speech functionality for the agent.
    """

    def __init__(self, config):
        self.config = config
        if not self.config.openai_api_key:
            print(
                "CRITICAL: OPENAI_API_KEY not found in environment. Voice features will not work.")
            self.client = None
        else:
            try:
                self.client = openai.OpenAI(api_key=self.config.openai_api_key)
                print("OpenAI client initialized successfully.")
            except Exception as e:
                print(f"Error initializing OpenAI client: {e}")
                self.client = None

        self.audio_interface = pyaudio.PyAudio()

        # Create project-specific temp directory instead of global one
        self.temp_dir = Path(tempfile.gettempdir()) / "idea_to_markdown_audio"
        self.temp_dir.mkdir(exist_ok=True)
        print(f"Using temporary audio directory: {self.temp_dir}")

    def _record_audio_chunk(self, stream):
        """Record audio from the user until they stop speaking or timeout occurs."""
        print("🔴 Recording... (Speak now, press Ctrl+C in console to stop)")
        frames = []
        try:
            # Record for a configurable duration
            for _ in range(0, int(RATE / CHUNK * self.config.voice_recording_duration)):
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
                # Future enhancement: Implement VAD here
        except KeyboardInterrupt:
            print("Recording stopped by user.")

        return b''.join(frames)

    def play_audio_stream(self, audio_stream_data):
        """Play audio data using PyAudio."""
        if not audio_stream_data:
            print("No audio data to play.")
            return

        temp_playback_file = self.temp_dir / "temp_agent_response.wav"
        try:
            with wave.open(str(temp_playback_file), 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(self.audio_interface.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(audio_stream_data)

            print("📢 Playing agent response...")
            wf = wave.open(str(temp_playback_file), 'rb')
            stream = self.audio_interface.open(format=self.audio_interface.get_format_from_width(wf.getsampwidth()),
                                               channels=wf.getnchannels(),
                                               rate=wf.getframerate(),
                                               output=True)
            data = wf.readframes(CHUNK)
            while data:
                stream.write(data)
                data = wf.readframes(CHUNK)

            stream.stop_stream()
            stream.close()
            wf.close()
        except Exception as e:
            print(f"Error playing audio: {e}")
        finally:
            # Clean up temp file
            try:
                temp_playback_file.unlink(missing_ok=True)
            except Exception:
                pass

    def conduct_realtime_conversation_turn(self, prompt_message: str = "Listening...") -> str | None:
        """
        Conducts a single turn of voice conversation:
        1. Records user's speech
        2. Transcribes to text using OpenAI
        3. Gets AI response via OpenAI
        4. Converts response to speech and plays it
        5. Returns transcribed user input
        """
        if not self.client:
            print("OpenAI client not available. Cannot conduct voice turn.")
            # Fallback to text input for basic testing
            return input(f"🎤 (Fallback Text Input) {prompt_message}: ")

        print(prompt_message)

        # 1. Record User Audio
        p_stream = self.audio_interface.open(format=FORMAT, channels=CHANNELS,
                                             rate=RATE, input=True,
                                             frames_per_buffer=CHUNK)
        user_audio_data = self._record_audio_chunk(p_stream)
        p_stream.stop_stream()
        p_stream.close()

        if not user_audio_data:
            print("No audio recorded.")
            return None

        try:
            # 2. Transcribe user's audio (STT)
            temp_stt_input_file = self.temp_dir / "temp_stt_input.wav"
            with wave.open(str(temp_stt_input_file), 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(self.audio_interface.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(user_audio_data)

            with open(temp_stt_input_file, "rb") as audio_file_for_stt:
                transcription_response = self.client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file_for_stt
                )
            user_transcribed_text = transcription_response.text
            print(f"👤 You said (transcribed): {user_transcribed_text}")

            if not user_transcribed_text:
                self.play_audio_stream(self._generate_error_speech(
                    "Sorry, I didn't catch that."))
                return None

            # 3. Get LLM response based on transcription
            chat_completion_response = self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system",
                        "content": "You are a helpful voice assistant for capturing ideas."},
                    {"role": "user", "content": user_transcribed_text}
                ]
            )
            agent_text_response = chat_completion_response.choices[0].message.content
            print(f"🧠 Agent thinks: {agent_text_response}")

            # 4. Synthesize agent's text response to speech (TTS)
            tts_response = self.client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=agent_text_response,
                response_format="wav"
            )
            agent_audio_data = tts_response.content

            # 5. Play Agent's Voice Response
            self.play_audio_stream(agent_audio_data)

            # Cleanup
            try:
                temp_stt_input_file.unlink(missing_ok=True)
            except Exception:
                pass

            return user_transcribed_text

        except openai.APIError as e:
            print(f"OpenAI API Error: {e}")
            self.play_audio_stream(self._generate_error_speech(
                "I encountered an API error."))
        except Exception as e:
            print(f"An unexpected error occurred in voice interaction: {e}")
            self.play_audio_stream(self._generate_error_speech(
                "An unexpected error occurred."))

        return None

    def _generate_error_speech(self, error_text: str) -> bytes | None:
        """Generates speech for a given error text if client is available."""
        if not self.client:
            return None
        try:
            response = self.client.audio.speech.create(
                model="tts-1", voice="alloy", input=error_text, response_format="wav"
            )
            return response.content
        except Exception as e:
            print(f"Failed to generate error speech: {e}")
            return None

    def __del__(self):
        # Clean up PyAudio
        if hasattr(self, 'audio_interface') and self.audio_interface:
            self.audio_interface.terminate()
