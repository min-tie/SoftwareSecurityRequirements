import py2neo
from py2neo import Node, NodeMatcher, Relationship
from tqdm import tqdm
import csv

# 连接数据库
graph = py2neo.Graph("neo4j://172.28.45.149:7687", auth=("neo4j", "password"))
matcher = NodeMatcher(graph)
cve_file_path = r'.\DATA\CVE.csv'


def CVEImport(cve_file):
    """
    导入CVE节点
    :return:
    """
    with open(cve_file, 'r', encoding='utf-8') as file:
        total_lines = sum(1 for line in file)

    # Reset the file pointer to the beginning
    with open(cve_file, 'r', encoding='utf-8') as file:
        # Create a CSV reader
        csv_reader = csv.reader(file)

        # Use tqdm for a progress bar
        for row in tqdm(csv_reader, total=total_lines, desc="Processing CVE CSV"):
            # Process each row here
            # For example, print the first three columns
            new_node = Node("CVE", name=row[0], status=row[1], description=row[2])
            graph.create(new_node)


def LevelImport():
    """
    :return: 导入四种安全等级及其描述
    """
    describing = [
        "Even if there is a security problem in the system, \
    there will be no serious economic loss, \
    such as personal website and other small systems.",
        "The system is generally a common civil system, \
    security problems will cause certain economic losses and commercial information leakage.",
        "Systems include systems that involve signiﬁcant economic interests or important information, \
    and will suﬀer serious losses if security issues arise. \
    Such as banking system, population information system, etc.",
        "The system is a safety demanding system. \
    If security problems occur, serious economic losses, \
    national security information leakage, or even health and life problems will result. \
    For example, aviation operation control system, nuclear power station remote control system and so on."]
    lev = "level_"
    for i in range(1, 5):
        new_node = Node("LEVEL", name=lev + str(i), description=describing[i - 1])
        graph.create(new_node)


def ThreatClassImport():
    ThreatClass_path = r"./DATA/Threat/ThreatClass.csv"
    with open(ThreatClass_path, 'r', encoding='utf-8') as file:
        total_lines = sum(1 for line in file)

    with open(ThreatClass_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # CSV中包含表头
        for row in tqdm(csv_reader, total=total_lines, desc="Processing ThreateClass CSV"):
            new_node = Node("THREATCLASS", name=row[0], description=row[1])
            graph.create(new_node)


def ThreatImport():
    file_path = r"./DATA/Threat/"
    ThreatClass_path = r"./DATA/Threat/ThreatClass.csv"
    with open(ThreatClass_path, 'r', encoding='utf-8') as file:
        total_lines = sum(1 for line in file)

    with open(ThreatClass_path, 'r', encoding='utf-8') as file:
        class_reader = csv.reader(file)
        next(class_reader)
        for row in tqdm(class_reader, total=total_lines, desc="Processing Threate CSV"):
            class_name = row[0]
            class_node = matcher.match("THREATCLASS", name=class_name).first()
            file_name = file_path + class_name + r".csv"
            with open(file_name, 'r', encoding='utf-8') as f:
                threat_reader = csv.reader(f)
                next(threat_reader)  # csv中包换表头
                for line in threat_reader:
                    new_node = Node("THREAT", name=line[0], description=line[1])
                    graph.create(new_node)
                    rel = Relationship(class_node, "include", new_node)
                    graph.create(rel)


def SFRClassImport():
    SFRClass_path = r"./DATA/SFR/class.csv"
    with open(SFRClass_path, 'r', encoding='utf-8') as file:
        total_lines = sum(1 for line in file)
    with open(SFRClass_path, 'r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in tqdm(csv_reader, total=total_lines, desc="Processing SFRClass CSV"):
            new_node = Node("SFRCLASS", name=row[0], FullName=row[1], description=row[2])
            graph.create(new_node)


def SFRFamilyImport():
    SFRFamily_path = r"./DATA/SFR/family.csv"
    with open(SFRFamily_path, 'r', encoding='utf-8') as file:
        total_lines = sum(1 for line in file)
    with open(SFRFamily_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        class_name = "FAU"
        class_node = matcher.match("SFRCLASS", name=class_name).first()
        if class_node is None:
            print(f"No node found with name '{class_name}' in 'SFRCLASS'.")
            return
        for row in tqdm(reader, total=total_lines, desc="Processing SFR Family CSV"):
            new_node = Node("SFRFAMILY", name=row[1], fullname=row[0], description=row[2])
            graph.create(new_node)
            if class_name != row[1][:3]:
                print(class_name, "->", row[1][:3])
                class_name = row[1][:3]
                class_node = matcher.match("SFRCLASS", name=class_name).first()
                if class_node is None:
                    print(f"No node found with name '{class_name}' in 'SFRCLASS'.")
                    return
            rel = Relationship(class_node, "include", new_node)
            graph.create(rel)


def EalImport():
    Eal_path = r"./DATA/Eal.csv"
    with open(Eal_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            new_node = Node("EAL", name=row[0], function=row[1], Description=row[2])
            graph.create(new_node)


def SARImport():
    sar_path = r'./DATA/SAR/SAR.csv'
    with open(sar_path, "r", encoding="utf-8") as file:
        total_lines = sum(1 for line in file)
    with open(sar_path, "r", encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in tqdm(reader, total=total_lines, desc="Processing SAR csv"):
            if row[0][:5] == "CLASS":
                class_name = row[0][-3:]
                print(f"\nimport Class {class_name}")
                class_node = Node("SARCLASS", name=class_name, fullname=row[1], description=row[2])
                graph.create(class_node)
            else:
                new_node = Node("SARFAMILY", name=row[0], fullname=row[1], descrip=row[2])
                graph.create(new_node)
                rel = Relationship(class_node, "include", new_node)
                graph.create(rel)

