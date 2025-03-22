## MockTTS: Build your custom mock assistant

This project is built on [ChatTTSPlus](https://github.com/warmshao/ChatTTSPlus/tree/master).

The current version is working on finetuning the model based on your own dataset.

### 1. Prepare your own audio file
Make sure your files are wav files, if it is not, then you need to convert it to wav. You can use **ffmpeg**. For example, convert m4a to wav:
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
It will generate multiple wav files, each of which basically contains one or two sentences. And it will generate the corresponding list file. (You could have multiple wav file and corresponding json in the folder, it will generate all in one folder)
Note: Sometimes the end of the audio will contain a very short beginning of the next sentence. If this happens, you can modify the code to use ```"-t", str(duration - 0.5)``` For example, here we set 0.5s to avoid extra audio at the end.
```
python prepare_dataset.py PATH_TO_WAV_AND_JSONS
```
In the list file, it should be like:
```
lxx/lxx_1.wav|lxx|en|You don't live here, said the fox.
lxx/lxx_2.wav|lxx|en|What is that you are looking for?
```
The first part is the location of each file, the second part is the speaker name, the third part *en* represents English, *zh* represents Chinese, and the last part is the text in the corresponding wav file.
#### Done!

### 4. Finetune the model on your voice
Check [this](https://github.com/Jackxiini/MockTTS/blob/main/assets/docs/voice_clone.md)
