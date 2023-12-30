import CreateNode
import ChartCreate
import py2neo
import csv
from tqdm import tqdm
import matplotlib.pyplot as plt

if __name__ == '__main__':
    cve_file_path = r'.\DATA\CVE.csv'  # 'r'表示原始字符，否则/会被翻译为转移符号
    graph = py2neo.Graph("neo4j://172.28.45.149:7687", auth=("neo4j", "password"))
    # CreateNode.CVEImport(cve_file=cve_file_path)  # 导入CVE
    # ChartCreate.CVEChart(cve_path=cve_file_path)
    # CreateNode.LevelImport()  # 导入四个安全等级
    # CreateNode.ThreatClassImport()  # 导入9个威胁大类
    CreateNode.ThreatImport()  # 导入威胁
