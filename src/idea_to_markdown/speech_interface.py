import openai
import pyaudio
import wave
import time  # For simulating delays or simple timing

# Configuration for audio recording
FORMAT = pyaudio.paInt16  # Audio format
CHANNELS = 1              # Mono audio
RATE = 16000              # Sample rate (Hz), common for voice
CHUNK = 1024              # Buffer size (frames per buffer)
# TEMP_WAVE_FILENAME = "temp_user_audio.wav" # If saving audio to file before sending


class SpeechInterface:
    """
    Handles real-time voice interaction using OpenAI's services.
    NOTE: The current implementation simulates a turn-by-turn conversational flow
    by recording a full utterance, then processing STT, LLM, and TTS sequentially.
    True real-time streaming (like OpenAI's "Advanced Voice Mode") would require
    more complex asynchronous handling of audio chunks for lower latency.
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

    def _record_audio_chunk(self, stream):
        """
        Helper to record a chunk of audio for a single utterance.
        Future Enhancement: Implement Voice Activity Detection (VAD) for smarter recording.
        """
        # This is a simplified recording for one utterance.
        # Real-time streaming would involve continuously capturing and sending chunks.
        print(
            "🔴 Recording... (Speak now, press Ctrl+C in console to stop - basic simulation)")
        frames = []
        try:
            # Record for a configurable duration or implement VAD
            # TODO: Implement VAD for smarter recording
            for _ in range(0, int(RATE / CHUNK * self.config.voice_recording_duration)):
                data = stream.read(CHUNK, exception_on_overflow=False)
                frames.append(data)
                # Basic VAD could be implemented here to stop on silence
        except KeyboardInterrupt:
            print("Recording stopped by user.")

        return b''.join(frames)

    def play_audio_stream(self, audio_stream_data):
        """
        Plays audio data received from an audio stream (e.g., OpenAI TTS).
        This is a simplified playback using a temporary file.
        Future Enhancement: Stream audio bytes directly to PyAudio for lower latency.
        """
        if not audio_stream_data:
            print("No audio data to play.")
            return

        # For simplicity, save to a temporary file and play.
        temp_playback_file = "temp_agent_response.wav"
        try:
            with wave.open(temp_playback_file, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(self.audio_interface.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(audio_stream_data)

            print(f"📢 Playing agent response...")
            wf = wave.open(temp_playback_file, 'rb')
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
            # Consider removing the temp file:
            # import os
            # if os.path.exists(temp_playback_file):
            #     os.remove(temp_playback_file)
            pass

    def conduct_realtime_conversation_turn(self, prompt_message: str = "Listening...") -> str | None:
        """
        Conducts a single turn of real-time voice conversation.
        1. Listens to user's voice.
        2. Sends to OpenAI (simulating Realtime API for speech-to-speech).
        3. Receives OpenAI's voice response.
        4. Plays OpenAI's voice response.
        5. Returns the transcribed text of the user's input for the agent logic.

        NOTE: This is a conceptual outline. True Realtime API integration
        would involve more complex streaming logic for both input and output audio.
        OpenAI's specific Realtime API for speech-to-speech might have different SDK usage.
        Refer to the latest OpenAI documentation for their "Realtime Conversations" API.
        """
        if not self.client:
            print("OpenAI client not available. Cannot conduct voice turn.")
            # Fallback to text input for basic testing if desired
            return input(f"🎤 (Fallback Text Input) {prompt_message}: ")

        print(prompt_message)

        # 1. Record User Audio (Simplified)
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
            # 2. Send to OpenAI & Get Response (Conceptual - API details may vary)
            # This part heavily depends on the specifics of OpenAI's Realtime API for speech-to-speech.
            # The following is a *conceptual representation* of what might happen.
            # You'd typically use a streaming STT, then send text to LLM, then use streaming TTS.
            # Or, a unified Realtime API might handle this more directly.

            # Step A: Transcribe user's audio (STT)
            # For this example, we'll save to a temporary file to use with `audio.transcriptions.create`
            # A true realtime API would stream this.
            # Future Enhancement: Use OpenAI's streaming STT if available via SDK, or another streaming STT service.
            temp_stt_input_file = "temp_stt_input.wav"
            with wave.open(temp_stt_input_file, 'wb') as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(self.audio_interface.get_sample_size(FORMAT))
                wf.setframerate(RATE)
                wf.writeframes(user_audio_data)

            with open(temp_stt_input_file, "rb") as audio_file_for_stt:
                transcription_response = self.client.audio.transcriptions.create(
                    model="whisper-1",  # Or other suitable model
                    file=audio_file_for_stt
                )
            user_transcribed_text = transcription_response.text
            print(f"👤 You said (transcribed): {user_transcribed_text}")

            if not user_transcribed_text:
                self.play_audio_stream(self._generate_error_speech(
                    "Sorry, I didn't catch that."))
                return None

            # Step B: Get LLM response based on transcription
            # This is where your agent's context/logic would feed into the LLM prompt
            # For now, using a simplified chat completion
            chat_completion_response = self.client.chat.completions.create(
                model="gpt-4o",  # Or your preferred model
                messages=[
                    {"role": "system",
                        "content": "You are a helpful voice assistant for capturing ideas."},
                    {"role": "user", "content": user_transcribed_text}
                ]
            )
            agent_text_response = chat_completion_response.choices[0].message.content
            print(f"🧠 Agent thinks: {agent_text_response}")

            # Step C: Synthesize agent's text response to speech (TTS)
            # Future Enhancement: Use OpenAI's streaming TTS if available via SDK for faster response.
            tts_response = self.client.audio.speech.create(
                model="tts-1",  # Or other suitable model
                voice="alloy",  # Or your preferred voice
                input=agent_text_response,
                response_format="wav"  # Or other format like mp3, opus
            )
            # tts_response.content contains the audio data bytes
            # For streaming: tts_response.stream_to_file("output.wav") or iterate chunks
            agent_audio_data = tts_response.content

            # 3. Play Agent's Voice Response
            self.play_audio_stream(agent_audio_data)

            # 4. Return user's transcribed text for agent logic
            return user_transcribed_text

        except openai.APIError as e:
            print(f"OpenAI API Error: {e}")
            # Potentially play a generic error message if TTS is available
            # self.play_audio_stream(self._generate_error_speech("I encountered an API error."))
        except Exception as e:
            print(f"An unexpected error occurred in voice interaction: {e}")
            # self.play_audio_stream(self._generate_error_speech("An unexpected error occurred."))

        return None  # In case of errors

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
