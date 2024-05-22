import json
import re

# 输入和输出文件路径
input_file = 'FormatDPO.json'
output_file = 'converted_chats_oasst.json'

# 加载原始数据
with open(input_file, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 函数：清理并创建有效的内容
def sanitize_content(content):
    return re.sub(r'[^\w\s-]', '', content).strip()

# 创建并写入 JSONL 文件
with open(output_file, 'w', encoding='utf-8') as f_out:
    lst = []
    for dialog in data:
        new_dialog = {
            "instruction": dialog["prompt"],
            "input": "",
            "output": dialog["chosen"],
            "history": []
        }
        
        lst.append(new_dialog)
        
    # 写入每个对话组为一行 JSON
    f_out.write(json.dumps(lst, ensure_ascii=False) + '\n')

print("转换完成。")