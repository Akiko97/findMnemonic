import json


class Data:
    def __init__(self):
        self.instruction = []
        self.opcodeinstruction = []


def process_json_file(file_path):
    data = Data()
    try:
        with open(file_path, 'r') as file:
            content = json.load(file)
            for item in content:
                if 'table' in item:
                    for table_item in item['table']:
                        if table_item.get('type') == 'table':
                            for i in table_item['value'].get('items'):
                                if 'instruction' in i:
                                    data.instruction.append(i['instruction'])
                                if 'opcodeinstruction' in i:
                                    data.opcodeinstruction.append(i['opcodeinstruction'])
    except FileNotFoundError:
        print(f"文件 {file_path} 未找到。")
    except json.JSONDecodeError:
        print(f"文件 {file_path} 不是有效的 JSON 格式。")
    return data


def process_data(data):
    mnemonics = set()

    for instr in data.instruction:
        word = instr.split(" ")[0].lower()
        mnemonics.add(word)

    for opcode in data.opcodeinstruction:
        parts = opcode.split("/r")
        if len(parts) > 1:
            word = parts[1].strip().split(" ")[0].lower()
            mnemonics.add(word)

    mnemonics.remove("")

    return list(mnemonics)


def save_to_json(data, output_file):
    with open(output_file, 'w') as file:
        json.dump(data.__dict__, file, indent=4)


def save_list_to_json(lst, output_file):
    with open(output_file, 'w') as file:
        json.dump(lst, file, indent=4)


# 主程序
if __name__ == "__main__":
    input_file = './instructions.json'
    data_output_file = './data_output.json'
    mnemonics_output_file = './mnemonics_output.json'

    data = process_json_file(input_file)
    save_to_json(data, data_output_file)
    print("data 处理完成，数据已保存至", data_output_file)

    mnemonics = process_data(data)
    save_list_to_json(mnemonics, mnemonics_output_file)
    print("mnemonics 处理完成，数据已保存至", mnemonics_output_file)
