import json
import os
import subprocess
import sys
import glob

def process_file(json_file, wav_file, output_dir, list_lines, seg_counter, min_length=20):
    print(f"\n处理文件：\n  JSON: {json_file}\n  WAV:  {wav_file}")
    # 读取 JSON 文件
    try:
        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"读取 {json_file} 失败：{e}")
        return seg_counter

    segments = data.get("segments", [])
    print("  总共找到分段数量：", len(segments))
    
    # 筛选出文本长度超过阈值的分段
    valid_segments = [seg for seg in segments if len(seg.get("text", "").strip()) > min_length]
    print("  符合条件的分段数量（过短过滤后）：", len(valid_segments))
    
    # 对连续重复的文本进行过滤：
    # 如果连续出现两个或更多完全相同的文本，则将这些分段全部删除
    filtered_segments = []
    i = 0
    while i < len(valid_segments):
        current_text = valid_segments[i].get("text", "").strip()
        group = [valid_segments[i]]
        j = i + 1
        while j < len(valid_segments) and valid_segments[j].get("text", "").strip() == current_text:
            group.append(valid_segments[j])
            j += 1
        if len(group) >= 2:
            print(f"  删除重复文本的分段：'{current_text}'（共 {len(group)} 个连续重复）")
        else:
            filtered_segments.extend(group)
        i = j

    print("  经过重复过滤后的分段数量：", len(filtered_segments))
    
    # 遍历过滤后的分段，调用 ffmpeg 提取音频
    for i, segment in enumerate(filtered_segments):
        start_time = segment.get("start", 0)
        end_time = segment.get("end", 0)
        duration = end_time - start_time
        text = segment.get("text", "").strip()
        # 输出文件命名为 lxx_数字.wav，数字为全局连续计数
        wav_filename = f"lxx_{seg_counter}.wav"
        output_file = os.path.join(output_dir, wav_filename)
        
        # 构造 ffmpeg 命令：-ss 指定开始时间，-t 指定持续时长
        command = [
            "ffmpeg",
            "-i", wav_file,
            "-ss", str(start_time),
            "-t", str(duration),
            "-c", "copy",
            output_file,
            "-y"
        ]
        
        print(f"  提取分段 {i+1}：起始 {start_time}s，时长 {duration}s，文本：{text}")
        try:
            subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        except subprocess.CalledProcessError as e:
            print(f"  分段 {i+1} 提取失败：{e.stderr.decode()}")
            continue
        
        # 构造 list 文件行，格式： lxx/lxx_数字.wav|lxx|en|文本内容
        line = f"{output_dir}/{wav_filename}|lxx|en|{text}"
        list_lines.append(line)
        seg_counter += 1

    return seg_counter

def main():
    if len(sys.argv) < 2:
        print("Usage: python split_audio_with_list_batch.py <input_directory>")
        sys.exit(1)
    
    input_dir = sys.argv[1]
    if not os.path.isdir(input_dir):
        print("输入路径不是一个有效的目录！")
        sys.exit(1)
    
    # 输出目录，所有切分的音频都存放在此目录下
    output_dir = "lxx"
    os.makedirs(output_dir, exist_ok=True)
    
    list_lines = []  # 用于存储 list 文件的每一行
    seg_counter = 1  # 全局分段计数
    
    # 搜索目录下所有的 JSON 文件
    json_files = glob.glob(os.path.join(input_dir, "*.json"))
    if not json_files:
        print("在指定目录中未找到 JSON 文件！")
        sys.exit(1)
    
    # 按文件名排序，便于有序处理
    json_files = sorted(json_files)
    
    for json_file in json_files:
        base_name = os.path.splitext(os.path.basename(json_file))[0]
        wav_file = os.path.join(input_dir, base_name + ".wav")
        if not os.path.exists(wav_file):
            print(f"警告：对应的 WAV 文件不存在，跳过 {json_file}")
            continue
        
        seg_counter = process_file(json_file, wav_file, output_dir, list_lines, seg_counter)
    
    # 将所有 list 行写入 list.txt 文件
    list_file = "list.txt"
    try:
        with open(list_file, "w", encoding="utf-8") as f:
            for line in list_lines:
                f.write(line + "\n")
    except Exception as e:
        print("写入 list.txt 文件失败：", e)
        sys.exit(1)
    
    print("\n音频分割完成！")
    print("所有切分的音频保存在目录：", output_dir)
    print("生成的 list 文件为：", list_file)

if __name__ == "__main__":
    main()
