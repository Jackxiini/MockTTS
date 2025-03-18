## MockTTS: Build your custom mock assistant

This project is built on [ChatTTSPlus](https://github.com/warmshao/ChatTTSPlus/tree/master).

The current version is working on finetuning the model based on your own dataset.

### 1. Prepare your own audio file
Make sure your file is wav file, if it is not, then you need to convert it to wav. You can use **ffmpeg**. For example, convert m4a to wav:
```
ffmpeg -i input.m4a output.wav
```

### 2. Generate transcripts and timestamps
You may need to use **Whisper**
```
pip install git+https://github.com/openai/whisper.git
```
```
whisper your_audio.wav --model small --output_format json
```

### 3. Run prepare_dataset.py
It will generate multiple wav files, each of which basically contains one or two sentences. And it will generate the corresponding list file.
Note: Sometimes the end of the audio will contain a very short beginning of the next sentence. If this happens, you can modify the code to use ```"-t", str(duration - 0.5)``` For example, here we set 0.5s to avoid extra audio at the end.
```
python prepare_dataset.py your.json your.wav
```
#### Done!

### 4. Finetune the model on your voice
Check [this](https://github.com/Jackxiini/MockTTS/blob/main/assets/docs/voice_clone.md)
