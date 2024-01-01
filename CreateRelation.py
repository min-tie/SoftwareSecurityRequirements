from lxml import html
import json
import csv
from itertools import islice
from tqdm import tqdm
import py2neo
from py2neo import Node, NodeMatcher, Relationship

graph = py2neo.Graph("neo4j://172.28.45.149:7687", auth=("neo4j", "password"))
matcher = NodeMatcher(graph)


def CWE2CVE():
    """
    查询CWE节点的Observed Examples中的CVE漏洞，建立CVE漏洞节点，并为CWE和CVE建立关系
    """
    label = "CWEFAMILY"
    query = (f'match(n:{label}) '
             f'return n.name as name, '
             f'n.ObservedExamples as examples ')
    result = graph.run(query)  # run返回的不是一个列表，而是可迭代的对象

    # 导入CVE节点
    for cwe in tqdm(result, desc="Processing linked CVE"):
        cwe_node = matcher.match(label, name=cwe["name"]).first()
        if cwe_node is None:
            print("wrong")
            return
        examples = cwe["examples"]
        if examples is None or examples == "":
            continue
        parts = examples.split("::REFERENCE:")
        for i, part in enumerate(parts):
            if i == 0:
                continue
            a = part.split(":LINK:http")[0]  # 分离每个CVE样例最后的链接
            b = a.split(":", 2)
            cve_name = b[0]
            cve_desc = b[2]
            cve_node = Node("CVE", name=cve_name, description=cve_desc)
            graph.create(cve_node)
            rel = Relationship(cwe_node, "exemplify", cve_node)
            graph.create(rel)
