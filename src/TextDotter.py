import re
import os

def convert_text(input_text):
    pattern = r'(\S+)［＃「(.+?)」に傍点］'
    match = re.search(pattern, input_text)
    if match:
        word_before_marker = match.group(1)
        highlighted_text = match.group(2)
        new_text = ''.join([f'｜{char}《﹅》' for char in highlighted_text])
        output_text = input_text.replace(f'{word_before_marker}［＃「{highlighted_text}」に傍点］', f'{word_before_marker}{new_text}')
        return output_text.strip()
    else:
        return input_text

def process_file(file_path, output_folder):
    with open(file_path, 'r', encoding='utf-8') as file:
        input_text = file.read()
    output_text = convert_text(input_text)
    output_file = os.path.join(output_folder, f"{os.path.basename(file_path).rsplit('.', 1)[0]}_投稿用.txt")
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(output_text)
    print(f"変換が完了しました。出力ファイル: {output_file}")

def process_folder(input_folder, output_folder):
    for root, _, files in os.walk(input_folder):
        for file_name in files:
            if file_name.endswith('.txt'):
                file_path = os.path.join(root, file_name)
                process_file(file_path, output_folder)

# 現在のディレクトリを取得
current_dir = os.path.dirname(os.path.abspath(__file__))

# 入力フォルダと出力フォルダのパスを指定
input_folder = os.path.join(current_dir, '../Draft')
output_folder = os.path.join(current_dir, '../Post')

# 出力フォルダが存在しない場合は作成
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# フォルダ内のテキストファイルを再帰的に処理
process_folder(input_folder, output_folder)
