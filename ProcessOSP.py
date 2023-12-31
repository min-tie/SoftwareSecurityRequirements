from lxml import html
import json


def trimSpace(s: str):
    result = s.split(" ", 1)
    if len(result) > 1:
        st = result[1]
        return st
    else:
        print(f"Not found space in {s}")
        return None


def Html2Json():
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
        print(li[k][0])
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
    #
    # print(f"提取的数据已写入到 {json_file_path}")


if __name__ == "__main__":
    Html2Json()
