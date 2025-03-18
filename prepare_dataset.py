import json
import os
import subprocess
import sys

def main():
    if len(sys.argv) < 3:
        print("Usage: python split_audio_with_list.py <transcript.json> <input_audio_file>")
        sys.exit(1)
    
    json_file = sys.argv[1]
    audio_file = sys.argv[2]
    
    # 读取 JSON 文件
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    segments = data.get("segments", [])
    print("总共找到分段数量：", len(segments))
    
    # 创建输出目录（命名为 "lxx" 以符合 list 文件要求）
    output_dir = "lxx"
    os.makedirs(output_dir, exist_ok=True)
    
    # 设置文本最小字符长度阈值
    min_length = 20
    
    # 筛选出文本长度超过阈值的分段
    valid_segments = [seg for seg in segments if len(seg.get("text", "").strip()) > min_length]
    print("符合条件的分段数量：", len(valid_segments))
    
    list_lines = []  # 用于存储 list 文件的每一行
    
    for i, segment in enumerate(valid_segments):
        start_time = segment.get("start", 0)
        end_time = segment.get("end", 0)
        duration = end_time - start_time
        text = segment.get("text", "").strip()
        # 输出文件命名为 lxx_1.wav, lxx_2.wav, ...
        wav_filename = f"lxx_{i+1}.wav"
        output_file = os.path.join(output_dir, wav_filename)
        
        # 构造 ffmpeg 命令：-ss 指定开始时间，-t 指定持续时长
        # 这里 duration-0.5 用于避免末尾多余的音频（可根据需要调整）
        command = [
            "ffmpeg",
            "-i", audio_file,
            "-ss", str(start_time),
            "-t", str(duration - 0.5),
            "-c", "copy",
            output_file,
            "-y"
        ]
        
        print(f"提取分段 {i+1}：起始 {start_time}s，时长 {duration}s，文本：{text}")
        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"分段 {i+1} 提取失败：{e.stderr.decode()}")
            continue
        
        # 构造 list 文件行，格式： lxx/lxx_1.wav|lxx|en|文本内容
        line = f"{output_dir}/{wav_filename}|lxx|en|{text}"
        list_lines.append(line)
    
    # 将所有 list 行写入 list.txt 文件
    list_file = "list.txt"
    with open(list_file, "w", encoding="utf-8") as f:
        for line in list_lines:
            f.write(line + "\n")
    
    print("音频分割完成，结果保存在目录：", output_dir)
    print("生成的 list 文件为：", list_file)

if __name__ == "__main__":
    main()

