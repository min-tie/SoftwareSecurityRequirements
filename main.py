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
    # # ChartCreate.CVEChart(cve_path=cve_file_path)
    # CreateNode.LevelImport()  # 导入四个安全等级
    # CreateNode.ThreatClassImport()  # 导入9个威胁大类
    # CreateNode.ThreatImport()  # 导入68种威胁
    # CreateNode.SFRClassImport()  # 导入11种安全功能需求类
    # CreateNode.SFRFamilyImport()  # 导入74个安全功能需求族
    # CreateNode.EalImport()  # 导入7个评估等级
    # CreateNode.SARImport()  # 导入9个安全保障需求类和47个族
    CreateNode.AssetClassImport()
    CreateNode.AssetFamilyImprot()
