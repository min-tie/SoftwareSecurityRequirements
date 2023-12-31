import CreateNode
import ChartCreate
import py2neo
import csv
from tqdm import tqdm
import matplotlib.pyplot as plt

lebels = ["CVE", "LEVEL", "THREATCLASS", "THREAT", "SFRCLASS",
          "SFRFAMILY", "EAL", "SARCLASS", "SARFAMILY",
          "ASSETCLASS", "ASSETFAMILY", "OSPCLASS", "OSPFAMILY"]
if __name__ == '__main__':
    graph = py2neo.Graph("neo4j://172.28.45.149:7687", auth=("neo4j", "password"))
    # CreateNode.CVEImport()  # 导入CVE
    # # ChartCreate.CVEChart(cve_path=cve_file_path)
    # CreateNode.LevelImport()  # 导入四个安全等级
    # CreateNode.ThreatClassImport()  # 导入9个威胁大类
    # CreateNode.ThreatImport()  # 导入68种威胁
    # CreateNode.SFRClassImport()  # 导入11种安全功能需求类
    # CreateNode.SFRFamilyImport()  # 导入74个安全功能需求族
    # CreateNode.EalImport()  # 导入7个评估等级
    # CreateNode.SARImport()  # 导入9个安全保障需求类和47个族
    # CreateNode.AssetClassImport()  # 导入5个资产实体类
    # CreateNode.AssetFamilyImprot()  # 导入24个资产实体族
    # CreateNode.OSPImport()  # 导入组织安全策略
    CreateNode.OSPImport()  # 导入安全目的
