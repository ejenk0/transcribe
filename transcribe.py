#! ./venv/bin/python3

from openai import OpenAI, APIConnectionError
import os
import sys
import threading


# Source .env file
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


transcribe_file = client.audio.transcriptions.create
# Dummy function for testing
# def transcribe_file(**kwargs):
#     class TranscriptResponse:
#         def __init__(self, text):
#             self.text = text

#     return TranscriptResponse("This is a test transcription")


output_file = sys.stdout


def transcribe(file_path: str):
    global output_file

    with open(file_path, "rb") as file:
        file_name = file_path.split("/")[-1]

        # Transcribe the audio file
        try:
            transcript = transcribe_file(model="whisper-1", file=file, language="en")
        except APIConnectionError:
            print(
                "Error transcribing "
                + file_name
                + ". Have you set a valid OPENAI_API_KEY in .env?",
                file=sys.stderr,
            )
            return

        # Write the transcript to the output file
        print(
            "\n## " + file_name + "\n\n" + transcript.text,
            file=output_file,
        )

    print("Done transcribing " + file_name, file=sys.stderr)


def convert_to_pdf(path: str):
    import pandoc
    import warnings

    # Suppress the warning about Pandoc version
    warnings.filterwarnings(
        "ignore",
        category=UserWarning,
    )

    print("Converting to PDF...", file=sys.stderr)
    doc = pandoc.read(file=path, format="markdown")
    pandoc.write(
        doc,
        format="pdf",
        file="transcriptions/transcriptions.pdf",
        options=["--pdf-engine=xelatex"],
    )
    print("Done converting to PDF", file=sys.stderr)


def main():
    global output_file
    output_file_path = "transcriptions/transcriptions.md"
    output_file = open(output_file_path, "w")

    if os.name == "nt":
        # Windows
        font = "Microsoft YaHei"
    else:
        # Mac OS / Other hopefully
        font = "PingFang SC"

    # Configure the markdown to be rendered using a font that supports Chinese characters
    print(
        f"""---
mainfont: {font}
---

# Transcriptions""",
        file=output_file,
    )

    # Open every audio file in ./audio and transcribe it in its own thread
    for file in os.listdir("./audio"):
        if file.endswith(".wav") or file.endswith(".mp3"):
            print("Transcribing " + file + "...", file=sys.stderr)
            thread = threading.Thread(target=transcribe, args=("./audio/" + file,))
            thread.start()

    # Wait for all threads to finish
    main_thread = threading.current_thread()
    for thread in threading.enumerate():
        if thread is not main_thread:
            thread.join()

    output_file.close()

    # Convert the markdown file to PDF
    convert_to_pdf(output_file_path)


if __name__ == "__main__":
    main()
