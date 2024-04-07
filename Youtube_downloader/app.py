from flask import Flask, render_template, request
import pytube

app = Flask(__name__)

# Function to download a YouTube video with error handling
def download_video(url, output_path=".", quality=None):
    """Downloads a YouTube video to the specified output path.

    Args:
        url (str): The URL of the YouTube video to download.
        output_path (str, optional): The path where the downloaded video
            will be saved. Defaults to the current working directory.
        quality (str, optional): The desired quality or resolution of the video.
            If not specified, the highest available quality will be chosen.

    Returns:
        None
    """

    try:
        # Create a YouTube object
        youtube = pytube.YouTube(url)

        # Get available video streams (filters for MP4 by default)
        video_streams = youtube.streams.filter(progressive=True)

        # Allow user to choose video resolution (optional)
        if quality:
            selected_stream = video_streams.filter(resolution=quality).first()
            if not selected_stream:
                print("Requested quality not available. Downloading highest resolution...")
                selected_stream = video_streams.order_by('resolution').desc().first()
        else:
            selected_stream = video_streams.order_by('resolution').desc().first()

        # Download the video
        print(f"Downloading '{selected_stream.title}'...")
        selected_stream.download(output_path=output_path)

        return True, f"Download of '{selected_stream.title}' complete!"

    except pytube.exceptions.PytubeError as e:
        return False, f"Error downloading video: {e}"

# Home page
@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        video_url = request.form["video_url"]
        quality = request.form["quality"]
        success, message = download_video(video_url, quality=quality)
        return render_template("result.html", success=success, message=message)
    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0')
