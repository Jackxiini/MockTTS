## ChatTTSPlus 声音克隆
目前支持两种声音克隆的方式:
* 训练lora
* 训练speaker embedding

### 模型训练:
#### lora训练(推荐):
* 修改`configs/train/train_voice_clone_lora.yaml`里 `DATA/meta_infos`为上一个处理到的`.list`文件
* 修改`configs/train/train_voice_clone_lora.yaml`里 `exp_name`为实验的名称，最好用speaker_name做区分识别。
* 然后运行`accelerate launch train_lora.py --config configs/train/train_voice_clone_lora.yaml`开始训练。
* 训练的模型会保存在: `outputs` 文件夹下，比如`outputs/xionger_lora-1732809910.2932503/checkpoints/step-900`
* 你可以使用tensorboard可视化训练的log, 比如`tensorboad --logdir=outputs/xionger_lora-1732809910.2932503/tf_logs`

#### speaker embedding训练(不推荐，很难收敛):
* 修改`configs/train/train_speaker_embedding.yaml`里 `DATA/meta_infos`为上一个处理到的`.list`文件
* 修改`configs/train/train_speaker_embedding.yaml`里 `exp_name`为实验的名称，最好用speaker_name做区分识别。
* 然后运行`accelerate launch train_lora.py --config configs/train/train_speaker_embedding.yaml`开始训练。
* 训练的speaker embedding 会保存在: `outputs` 文件夹下，比如`outputs/xionger_speaker_emb-1732931630.7137222/checkpoints/step-1/xionger.pt`
* 你可以使用tensorboard可视化训练的log, 比如`tensorboad --logdir=outputs/xionger_speaker_emb-1732931630.7137222/tf_logs`

#### 一些Tips
* 如果要效果好的话，最好准备1小时以上的音频。我试过1分钟训练lora，但是比较容易过拟合，效果一般。
* 不要训练太久，不然容易过拟合，我用1小时的雷军音频训练，2000到3000 step就收敛了。
* 如果你懂lora训练的话，你可以尝试调整config里面的参数。

### 模型推理
* 启动webui: ` python webui.py --cfg configs/infer/chattts_plus.yaml`
* 参考以下视频教程使用:

<video src="https://github.com/user-attachments/assets/b1590f92-e86b-4dc7-b304-9546a9d8a30e" controls="controls" width="500" height="300">您的浏览器不支持播放该视频！</video>
