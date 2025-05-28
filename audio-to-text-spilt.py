import openai
import os
import subprocess
from tkinter import Tk, filedialog
from pydub import AudioSegment
from mutagen.mp3 import MP3
import io
from dotenv import load_dotenv

# Setup ffmpeg for PyDub
os.environ["PATH"] += os.pathsep + r"C:/ffmpeg/bin"
AudioSegment.converter = r"C:/ffmpeg/bin/ffmpeg.exe"
AudioSegment.ffprobe = r"C:/ffmpeg/bin/ffprobe.exe"



# ✅ 載入 .env 中的環境變數
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    openai.api_key = api_key
    print(f"✅ Import successfully, your API key is: {api_key}")
else:
    print("❌ Failed to load OpenAI API key. Please check your .env file.")
    exit()


# Split audio into in-memory chunks (no saving)
def split_audio_to_memory(input_path, chunk_length_ms=5 * 60 * 1000):
    audio = AudioSegment.from_file(input_path)
    total_length = len(audio)
    chunks = []

    for i in range(0, total_length, chunk_length_ms):
        chunk = audio[i:i + chunk_length_ms]
        buffer = io.BytesIO()
        chunk.export(buffer, format="mp3", bitrate="192k")
        buffer.seek(0)
        chunks.append((buffer, len(chunk) / 1000 / 60))  # (BytesIO, minutes)
    
    return chunks

# File selection
Tk().withdraw()
file_path = filedialog.askopenfilename(title="選擇音訊檔案",
                                       filetypes=[("音訊文件", "*.mp3;*.wav;*.flac;*.aac;*.ogg;*.m4a")])
if not file_path:
    print("❌ 未選擇檔案，程式結束。")
    exit()

file_dir, file_name = os.path.split(file_path)
file_base, _ = os.path.splitext(file_name)
converted_output_file = os.path.join(file_dir, file_base + "_converted.mp3")

# Convert to mp3
print("🔁 正在轉換音訊格式為 mp3...")
subprocess.run([
    r"C:/ffmpeg/bin/ffmpeg.exe", "-y", "-i", file_path,
    "-c:a", "libmp3lame", "-b:a", "192k", converted_output_file
], check=True)
print("✅ 音訊轉換完成！")

# In-memory splitting
print("🔪 分割音訊中...")
audio_chunks = split_audio_to_memory(converted_output_file)
print(f"✅ 共分成 {len(audio_chunks)} 段")

# Transcribe each chunk
final_transcript = ""
total_cost = 0

for idx, (buffer, duration_min) in enumerate(audio_chunks, 1):
    print(f"🔊 處理第 {idx} 段（約 {round(duration_min, 2)} 分鐘）")
    response = openai.audio.transcriptions.create(
    model="whisper-1",
    file=("chunk.mp3", buffer, "audio/mpeg"),  # 指定 fake filename + MIME type
    response_format="json"
    )
    final_transcript += f"[段落 {idx} 開始]\n{response.text}\n\n"
    
    cost = round(duration_min * 0.006, 4)
    total_cost += cost
    print(f"💰 段落成本：約 ${cost}")

# Output final transcript
transcript_file = os.path.join(file_dir, file_base + "_transcript.txt")
with open(transcript_file, "w", encoding="utf-8") as f:
    f.write(final_transcript)

print(f"📄 已輸出完整轉錄文字：{transcript_file}")
print(f"💰 預估總成本：約 ${round(total_cost, 4)} 美元")
