import streamlit as st
from pydub import AudioSegment
import os
import io
import matplotlib.pyplot as plt
import numpy as np
import librosa
import librosa.display

# Page config
st.set_page_config(page_title="Audio Trimmer", page_icon="✂️", layout="wide")

# Custom CSS for a more premium look
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: #ffffff;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #ff4b4b;
        color: white;
    }
    .stDownloadButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #28a745;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("✂️ MP3/Audio Trimmer")
st.write("Dễ dàng cắt nhỏ file âm thanh của bạn!")

# Sidebar for controls
st.sidebar.header("Tùy chọn")
uploaded_file = st.sidebar.file_uploader("Tải lên file âm thanh", type=["mp3", "wav", "ogg", "flac"])

if uploaded_file is not None:
    # Load audio
    with st.spinner("Đang tải file âm thanh..."):
        audio_bytes = uploaded_file.read()
        audio = AudioSegment.from_file(io.BytesIO(audio_bytes))
        
        # Duration in seconds
        duration_sec = len(audio) / 1000.0
        
        st.info(f"Đã tải: {uploaded_file.name} | Độ dài: {duration_sec:.2f} giây")
        
        # Visualizing waveform
        st.subheader("Waveform Visualization")
        
        # We use librosa for better visualization
        y, sr = librosa.load(io.BytesIO(audio_bytes), sr=None)
        
        fig, ax = plt.subplots(figsize=(12, 4))
        librosa.display.waveshow(y, sr=sr, ax=ax, color='cyan')
        ax.set_title("Biểu đồ sóng âm")
        ax.set_ylabel("Biên độ")
        ax.set_xlabel("Thời gian (giây)")
        # Customize plot for dark mode
        fig.patch.set_facecolor('#0e1117')
        ax.set_facecolor('#0e1117')
        ax.xaxis.label.set_color('white')
        ax.yaxis.label.set_color('white')
        ax.title.set_color('white')
        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')
        for spine in ax.spines.values():
            spine.set_color('white')
            
        st.pyplot(fig)

        # Trimming controls
        st.subheader("Cắt âm thanh")
        start_time, end_time = st.slider(
            "Chọn khoảng thời gian cần giữ lại (giây)",
            0.0, float(duration_sec), (0.0, float(duration_sec)),
            step=0.1
        )
        
        st.write(f"Khoảng đã chọn: {start_time:.1f}s - {end_time:.1f}s (Độ dài: {end_time - start_time:.1f}s)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("Nghe thử đoạn đã chọn"):
                # Preview selection
                trimmed_audio = audio[int(start_time * 1000):int(end_time * 1000)]
                preview_io = io.BytesIO()
                trimmed_audio.export(preview_io, format="mp3")
                st.audio(preview_io.getvalue(), format="audio/mp3")
        
        with col2:
            # Process and Download
            trimmed_audio = audio[int(start_time * 1000):int(end_time * 1000)]
            output_io = io.BytesIO()
            trimmed_audio.export(output_io, format="mp3")
            
            st.download_button(
                label="Tải về file đã cắt (.mp3)",
                data=output_io.getvalue(),
                file_name=f"trimmed_{uploaded_file.name}.mp3",
                mime="audio/mp3"
            )

else:
    st.info("Vui lòng tải lên một file âm thanh ở thanh bên để bắt đầu.")
    # Show case image or placeholder
    st.image("https://images.unsplash.com/photo-1470225620780-dba8ba36b745?ixlib=rb-1.2.1&auto=format&fit=crop&w=1350&q=80", caption="Bắt đầu tạo ra những đoạn nhạc tuyệt vời")

st.markdown("---")
st.markdown("Author: Nguyễn Hoàng Tùng")
