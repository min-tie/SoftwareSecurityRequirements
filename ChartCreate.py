import csv
import matplotlib.pyplot as plt
from tqdm import tqdm

cve_file_path = r'.\DATA\CVE.csv'


def CVEChart(cve_path):
    """
    :param cve_path: cve表的路径
    :return: 生成年度变化图
    """
    count = [0] * 26
    with open(cve_path, 'r', encoding='utf-8') as file:
        total_lines = sum(1 for line in file)
    with open(cve_path, 'r', encoding='utf-8') as file:
        # Create a CSV reader
        csv_reader = csv.reader(file)
        for row in tqdm(csv_reader, total=total_lines, desc="Processing CSV"):
            year = row[0][4:8]
            year = int(year) - 1999
            count[year] = count[year] + 1

    # 生成 x 轴坐标，假设 x 轴是 1 到 26
    x = list(range(1999, 2025))

    # 画折线图
    plt.plot(x, count, marker='o', linestyle='-')

    # 设置图表标题和坐标轴标签
    plt.title('chart of quantity changes of CVE')
    plt.xlabel('YEAR')
    plt.ylabel('NUMBER')
    plt.savefig('CVE年度图.png')
    plt.show()