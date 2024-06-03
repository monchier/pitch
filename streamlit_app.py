import streamlit as st
import pandas as pd
from io import BytesIO
from omnizart.music import app as music_app

# Initialize omnizart
omnizart.initialize()

def extract_notes(audio_bytes):
    # Save audio_bytes to a temporary file
    with open("temp_audio.wav", "wb") as f:
        f.write(audio_bytes.getbuffer())

    # Transcribe the audio file to MIDI
    transcribed_midi = music_app.transcribe("temp_audio.wav")
    
    # Convert MIDI to dataframe
    notes = []
    for instrument in transcribed_midi.instruments:
        for note in instrument.notes:
            notes.append({
                "start": note.start,
                "end": note.end,
                "pitch": note.pitch,
                "duration": note.end - note.start
            })
    df = pd.DataFrame(notes)
    return df

st.title("Music Transcription using Omnizart")
st.write("Upload an audio WAV file to transcribe the musical notes.")

audio_file = st.file_uploader("Upload Audio File", type=["wav"])

if audio_file is not None:
    audio_bytes = BytesIO(audio_file.read())
    st.audio(audio_bytes, format='audio/wav')
    
    # Extract notes using Omnizart
    notes_df = extract_notes(audio_bytes)
    
    st.write("Transcribed Musical Notes:")
    st.dataframe(notes_df)
    
    csv = notes_df.to_csv(index=False)
    st.download_button(
        label="Download data as CSV",
        data=csv,
        file_name='transcribed_notes.csv',
        mime='text/csv',
    )

    st.write("Musical Notes Textual Representation:")
    notes_text = notes_df.to_string(index=False)
    st.text(notes_text)

