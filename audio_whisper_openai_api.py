from the_notebook_tools import save_transcript
import os
import openai
import json

CHATGPT_API_KEY = "sk-..."

# OpenAI said "We do not train on your business data (data from ChatGPT Team, ChatGPT Enterprise, or our API Platform)" at https://openai.com/enterprise-privacy/
# Use it at your own risk.


# Set your OpenAI API key and base URL
CHATGPT_BASE_URL = "https://api.openai.com/v1"
client = openai.OpenAI(api_key=CHATGPT_API_KEY, base_url=CHATGPT_BASE_URL, timeout=600)


def transcribe_audio_whisper_api(file_path, language="zh", temperature=0.4):
    """
    Transcribe an audio file using OpenAI API and save the result as .json, .srt, and .txt files.

    Args:
        file_path (str): Path to the audio file.
        language (str, optional): Language of the audio. Default is "zh" (Chinese).
    """
    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: 文件 {file_path} 不存在。")
        return

    # Open the audio file
    with open(file_path, "rb") as audio_file:
        try:
            transcript = client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-1",
                response_format="verbose_json",
                timestamp_granularities=["segment"],
                language=language,
                temperature=temperature,
            )
            # print(transcript)
        except Exception as e:
            print(f"Error: 转录音频文件时出错：{e}")
            return

    # Convert the transcript to a dictionary
    transcript_dict = transcript.to_dict()
    # print(transcript_dict["text"])

    # Save the raw JSON response
    json_file_path = file_path + "api_whisper.json"
    if temperature != 0.4:
        json_file_path = file_path + str(temperature) + "api_whisper.json"
    try:
        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(transcript_dict, json_file, indent=4)
    except Exception as e:
        print(f"Error: 无法保存 .json 文件：{e}")

    txt_file_path = save_transcript(
        file_path, json_file_path, "api_openai_whisper", "tg"
    )

    # 输出信息
    return txt_file_path


# Test different temperatures
def test_temperatures():
    file = "2021-06-13T23_11_47.m4a"
    while True:
        temperature = input("Enter temperature: ")
        transcribe_audio_whisper_api(file, temperature=float(temperature))


# test_temperatures()
