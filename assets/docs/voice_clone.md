### Model Training
#### Lora Training (Recommended)
* Modify `DATA/meta_infos` in `configs/train/train_voice_clone_lora.yaml` to the `.list` file processed in previous step
* Modify `exp_name` in `configs/train/train_voice_clone_lora.yaml` to the experiment name, preferably using speaker_name for identification.
* Then run `accelerate launch train_lora.py --config configs/train/train_voice_clone_lora.yaml` to start training.
* Trained models will be saved in the `outputs` folder, like `outputs/xionger_lora-1732809910.2932503/checkpoints/step-900`
* You can visualize training logs using tensorboard, e.g., `tensorboad --logdir=outputs/xionger_lora-1732809910.2932503/tf_logs`

#### Speaker Embedding Training (Not Recommended, Hard to Converge)
* Modify `DATA/meta_infos` in `configs/train/train_speaker_embedding.yaml` to the `.list` file processed in previous step
* Modify `exp_name` in `configs/train/train_speaker_embedding.yaml` to the experiment name, preferably using speaker_name for identification.
* Then run `accelerate launch train_lora.py --config configs/train/train_speaker_embedding.yaml` to start training.
* Trained speaker embeddings will be saved in the `outputs` folder, like `outputs/xionger_speaker_emb-1732931630.7137222/checkpoints/step-1/xionger.pt`
* You can visualize training logs using tensorboard, e.g., `tensorboad --logdir=outputs/xionger_speaker_emb-1732931630.7137222/tf_logs`

#### Some Tips
* For better results, it's best to prepare more than 1 hour of audio. I tried training lora with 1 minute of audio, but it was prone to overfitting and the results were mediocre.
* Don't train for too long, otherwise it can easily overfit. When I trained with 1 hour of Lei Jun's audio, it converged between 2000 to 3000 steps.
* If you understand lora training, you can try adjusting the parameters in the config file.

### Model Inference
* Launch webui: `python webui.py --cfg configs/infer/chattts_plus.yaml`
* Refer to the following video tutorial for usage:

<video src="https://github.com/user-attachments/assets/b1590f92-e86b-4dc7-b304-9546a9d8a30e" controls="controls" width="500" height="300">Your browser doesn't support playing this video!</video>
