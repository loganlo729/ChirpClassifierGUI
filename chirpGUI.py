# VERY BASIC GUI for Chirp Classifier.

import streamlit as st
import numpy as np
import tempfile
import os

# Transition setup
st.markdown(
    """
    <style>

        /* -------------------- ANIMATION -------------------- */
        @keyframes slideIn {
            0% {
                opacity: 0;
                transform: translateX(-40px);
            }
            100% {
                opacity: 1;
                transform: translateX(0px);
            }
        }

        .slide-in {
            opacity: 0;
            animation: slideIn 0.8s ease-out forwards;
        }

        .delay-1 { animation-delay: 0.2s; }


        /* -------------------- CENTERING -------------------- */
        .centered-img-container {
            display: flex;
            justify-content: center;
            align-items: center;
            flex-direction: column;
            text-align: center;
        }


        /* -------------------- IMAGE CARD STYLE -------------------- */
        .image-card {
            background-color: #1e1e1e;
            padding: 18px;
            border-radius: 14px;
            box-shadow: 0 0 12px rgba(255, 255, 255, 0.05);
            margin-top: 10px;
            margin-bottom: 10px;
        }

        .image-caption {
            color: #cccccc;
            font-size: 0.9rem;
            margin-top: 8px;
            text-align: center;
        }

    </style>
    """,
    unsafe_allow_html=True
)

# Run model based on audio (PLACEHOLDER)
def run_model(audio_path):
    """
        [
            ("Species A", 0.82),
            ("Species B", 0.10),
            ("Species C", 0.04),
            ("Species D", 0.02),
            ("Species E", 0.02)
        ]
    """
    mock_species = ["American Robin", "Northern Cardinal", "Blue Jay", "House Finch", "Crow"]
    probs = np.random.dirichlet(np.ones(5), size=1)[0]
    return list(zip(mock_species, probs))

# Header section
st.markdown(
    """
    <div class="slide-in delay-1" style="text-align:center;">
        <h1>Chirp Classifier</h1>
        <h3>Identify bird species from short audio recordings</h3>
    </div>
    """,
    unsafe_allow_html=True,
)

# Image + description
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown('<div class="image-card slide-in delay-1 centered-img-container">', unsafe_allow_html=True)

    st.image(
        "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR7wRB27czFMbCL-3lwgoVrbSkHBPEQ0YOVf-Bok-47ZdKAuoWeW66751tM7CpusEV7SgqXIshnSA8gcbGQNThIl0P2GCGzuigWe3Bo7w&s=10",
        use_container_width=True
    )

    st.markdown(
        '<div class="image-caption">Piping plover – a bird often seen at Presque Isle State Park</div>',
        unsafe_allow_html=True
    )

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="slide-in delay-1">', unsafe_allow_html=True)
    st.markdown(
        """
        ### About This Project
        Our system analyzes bird chirps using machine learning to determine  
        **which species found in Erie is most likely making the sound**.

        *Upload an audio file (WAV, MP3, OGG, FLAC)*  
        The model will extract spectrogram features from the file, and
        then predict the top 5 matching bird species. The results are 
        listed with probability scores.
        """
    )

st.write("---")

# File upload
st.markdown('<div class="slide-in delay-1">', unsafe_allow_html=True)
uploaded_file = st.file_uploader("Upload a bird chirp audio file", type=["wav", "mp3", "ogg", "flac"])
st.markdown('</div>', unsafe_allow_html=True)

# Run prediction after upload
if uploaded_file is not None:

    with tempfile.NamedTemporaryFile(delete=False, suffix=uploaded_file.name) as tmp:
        tmp.write(uploaded_file.read())
        temp_audio_path = tmp.name

    st.audio(uploaded_file, format="audio/wav")
    st.write("---")

    if st.button("Run Prediction"):
        with st.spinner("Analyzing bird chirp... please wait..."):
            results = run_model(temp_audio_path)

        st.success("Prediction complete!")

        # Results section
        st.subheader("Top 5 Predictions")
        for species, prob in results:
            st.write(f"**{species}** — {prob*100:.2f}%")

        # Bar chart display
        st.bar_chart({species: prob for species, prob in results})

        # Cleanup
        os.remove(temp_audio_path)
