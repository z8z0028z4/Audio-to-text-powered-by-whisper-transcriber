<p align="center">
  <img src="assets/whisp-cover.png" width="600"/>
</p>

# 🎙 Whisp — Audio-to-Text Tool Using OpenAI Whisper

Whisper-powered transcriber with in-memory chunking, auto conversion, and OpenAI API cost estimation. 中文 & English supported!

## 🚀 Features

- 🎧 Supports multiple formats: mp3, wav, m4a, etc.
- 🔁 Auto convert to `.mp3`
- ✂️ Automatically splits large files into 5-minute chunks
- 🧠 Transcribes via OpenAI Whisper API (`whisper-1`)
- 💰 Shows per-chunk and total cost
- 🗂 Outputs transcript as `.txt` in same folder

## 📦 Installation

```bash
pip install -r requirements.txt
```

## ⚙️ Setup

1. Download and install ffmpeg from https://www.gyan.dev/ffmpeg/builds/
2. Place it under `C:/ffmpeg` so that:
   - `C:/ffmpeg/bin/ffmpeg.exe`
   - `C:/ffmpeg/bin/ffprobe.exe`

3. Create a `.env` file based on `.env.example`:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

## ▶️ Usage

```bash
python audio-to-text-split.py
```

- Select a local audio file
- Wait for processing and transcription
- Output will be in the same folder as `yourfile_transcript.txt`

## 🛡 .env security

`.env` is excluded via `.gitignore`, do **NOT** upload your API key to GitHub.

## 🏷 Topics

`whisper`, `openai`, `speech-to-text`, `audio`, `pydub`, `dotenv`, `transcription`
