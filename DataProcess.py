from lxml import html
import json
import csv
from itertools import islice
from tqdm import tqdm


def trimSpace(s: str):
    result = s.split(" ", 1)
    if len(result) > 1:
        st = result[1]
        return st
    else:
        print(f"Not found space in {s}")
        return None


def OSP2Json():
    # 本地HTML文件路径
    file_path = (r"./DATA/OSP/Minimum Security Standards for Electronic Information (MSSEI) _ Information Security "
                 r"Office.html")

    # 读取本地HTML文件内容
    with open(file_path, "r", encoding="utf-8") as file:
        html_content = file.read()

    # 将文件内容转换为HTML文档
    html_tree = html.fromstring(html_content)
    # 无论是大标题、小标题，还是描述内容，它们的父节点都相同。
    parent_node = r'//*[@id="page-page"]/div/div/div[1]/div/div/div/article/div/div/div/div/'
    p1 = []
    p2 = []
    # 提取大标题
    for i in range(5, 20, 1):
        xpath_expression = parent_node + f'h2[{str(i)}]'
        li = html_tree.xpath(xpath_expression)
        if len(li) > 0:
            result = li[0]
            # 提取标题在父节点中的相对位置，方便之后进行p1和p2的合并
            pos = result.xpath('count(preceding-sibling::*) + 1')
            desc_xpath = f'{xpath_expression}/following-sibling::*[3]'
            desc = html_tree.xpath(desc_xpath)[0].text_content().strip()
            tu = [result.text_content().strip(), pos, desc]
            p1.append(tu)
    # 提取小标题
    for j in range(7, 36, 1):
        xpath_expression = parent_node + f'h4[{str(j)}]'
        li = html_tree.xpath(xpath_expression)
        if len(li) > 0:
            result = li[0]
            pos = result.xpath('count(preceding-sibling::*) + 1')
            desc_xpath = f'{xpath_expression}/following-sibling::*[1]'
            desc = html_tree.xpath(desc_xpath)[0].text_content().strip()
            text = result.text_content().strip()
            if text[0].isdigit():
                tu = [text, pos, desc]
                p2.append(tu)

    merged_list = p1 + p2
    sorted_list = sorted(merged_list, key=lambda x: x[1])
    li = [[x[0], x[2]] for x in sorted_list]
    h1 = [x[0] for x in p1]
    pos_h1 = []  # h1在sorted_list中的位置
    for i in range(0, len(li)):
        if li[i][0] in h1:
            pos_h1.append(i)
        else:
            pass
    pos_h1.append(len(li))

    data = []
    for i in range(0, len(pos_h1) - 2):
        k = pos_h1[i]
        dic = {"class": trimSpace(li[k][0]), "description": li[i][1]}
        j = pos_h1[i + 1]
        family_ = li[k + 1:j]
        family = [[trimSpace(X[0]), X[1]] for X in family_]
        dic.update({"family": family})
        data.append(dic)

    # 将提取的数据写入JSON文件
    json_file_path = r"./DATA/OSP/MSSEI.json"
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


def CWE2Json() -> None:
    """
    将CWE官网上的内容转换成json型，获得CLASS和Family之间的所属关系
    :return:
    """
    CWE_file_path = r"./DATA/CWE/CWE.html"
    with open(CWE_file_path, "r", encoding="utf-8") as file:
        html_content = file.read()
    html_tree = html.fromstring(html_content)
    # Assuming html_tree is already defined
    parent_xpath = '//*[@id="oc_699_Relationships"]/div/div/div/div[2]'

    # Extract all child nodes under the parent node
    # child_nodes = html_tree.xpath(f'{parent_xpath}//div[contains(@id, "6991228")]')
    child_nodes = html_tree.xpath(f'{parent_xpath}//div')

    # Iterate over the child nodes
    all_line = []
    for child_node in child_nodes:
        # Access the id attribute of each child node
        lines = child_node.text_content().splitlines()
        for line in lines:
            if line[:3] == "699":
                parts = [part.strip() for part in line.split(">")]
                all_line.append(parts)

    pos = []  # 记录类在all_lines的位置
    for i, line in enumerate(all_line):
        if len(line) == 2:
            pos.append(i)
        elif len(line) == 3:
            pass
        else:
            print("wrong")
    pos.append(len(all_line))

    data = []
    for i in range(len(pos) - 1):
        class_index = pos[i]
        next_class_index = pos[i + 1]
        line = all_line[class_index][1].strip().split(" ", 1)
        num = line[0]
        name = line[1].strip("()")
        fam_li = []
        for j in range(class_index + 1, next_class_index):
            if len(all_line[j]) <= 2:
                print("wrong")
            line = all_line[j][2].strip().split(" ", 1)
            num_ = line[0]
            name_ = line[1].strip("()")
            fam_li.append([num_, name_])
        dic = {"No.": num,
               "name": name,
               "include": fam_li}
        data.append(dic)

    json_file_path = r"./DATA/CWE/CWE.json"
    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, ensure_ascii=False, indent=2)


def CVEGetLastest():
    """
    从CVE中截取最近的100000条中，没有被标记“rejected”、“disputed”等的表象
    :return:
    """
    input_csv_file = r"./DATA/CVE.csv"
    output_csv_file = "./DATA/CVE/CVE.csv"
    rows_to_save = 100000

    # 逐行读取CSV文件的最后2000行并写入新文件
    with open(input_csv_file, 'r', encoding='utf-8') as input_file, \
            open(output_csv_file, 'w', encoding='utf-8', newline='') as output_file:
        csv_reader = csv.reader(input_file)
        csv_writer = csv.writer(output_file)

        total_lines = sum(1 for _ in csv_reader)
        # 跳过前面的行，保留最后2000行
        past = total_lines - rows_to_save
        input_file.seek(0)  # 将指针移动至文件首
        # 使用 islice 跳过前面的行
        csv_reader = islice(csv_reader, past, None)
        for row in tqdm(csv_reader, total=rows_to_save, desc="generating latest CVE csv"):
            if row[2][:2] == "**":
                pass
            else:
                csv_writer.writerow(row)
