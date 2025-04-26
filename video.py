import streamlit as st
import yt_dlp
import os

st.set_page_config(page_title="YouTube Video Downloader", page_icon="🎬", layout="centered")
st.title("🎬 YouTube Video Downloader")

url = st.text_input("Enter YouTube video URL:")

def download_video_direct(url):
    ydl_opts = {
        'format': 'best[ext=mp4][vcodec!=none][acodec!=none]',  # Choose a format that is already combined
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # save to downloads folder
        'noplaylist': True,
        'merge_output_format': None,  # Do not merge, just download
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = ydl.prepare_filename(info)
        return filename, info

if st.button("Download"):
    if url:
        try:
            st.info("Fetching video details...")
            filename, info = download_video_direct(url)
            st.success(f"Downloaded: {info.get('title')}")

            # Display thumbnail
            st.image(info.get('thumbnail'), caption=info.get('title'), use_column_width=True)

            # Provide download button
            with open(filename, "rb") as file:
                st.download_button(
                    label="Download Video",
                    data=file,
                    file_name=os.path.basename(filename),
                    mime="video/mp4"
                )
        except Exception as e:
            st.error(f"Error: {e}")
    else:
        st.warning("Please enter a valid YouTube URL.")
