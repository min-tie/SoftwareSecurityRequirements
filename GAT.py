import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

from neo4j import GraphDatabase


class Neo4jConnection:
    def __init__(self, uri, user, pwd):
        self._uri = uri
        self._user = user
        self._password = pwd
        self._driver = None

    def close(self):
        if self._driver is not None:
            self._driver.close()

    def connect(self):
        self._driver = GraphDatabase.driver(self._uri, auth=(self._user, self._password))
        return self._driver


class GAT(nn.Module):
    def __init__(self, n_features, n_classes, n_heads, dropout, alpha):
        super(GAT, self).__init__()
        self.n_features = n_features
        self.n_classes = n_classes
        self.n_heads = n_heads
        self.dropout = dropout

        self.attention_heads = nn.ModuleList([GraphAttentionLayer(n_features, n_features // n_heads, dropout=dropout, alpha=alpha, concat=True) for _ in range(n_heads)])

        self.out_att = GraphAttentionLayer(n_features, n_classes, dropout=dropout, alpha=alpha, concat=False)

    def forward(self, x, adj):
        x = F.dropout(x, self.dropout, training=self.training)
        x = torch.cat([att(x, adj) for att in self.attention_heads], dim=1)
        x = F.dropout(x, self.dropout, training=self.training)
        x = F.elu(self.out_att(x, adj))
        return F.log_softmax(x, dim=1)



neo4j_uri = "neo4j://172.28.45.149:7687"
neo4j_user = "neo4j"
neo4j_password = "password"

neo4j_conn = Neo4jConnection(uri=neo4j_uri, user=neo4j_user, pwd=neo4j_password)
driver = neo4j_conn.connect()
query = "MATCH (n)-[r]->(m) RETURN n, r, m LIMIT 100"
with driver.session() as session:
    result = session.run(query)
    # 处理查询结果，将节点和边的信息转换为PyTorch张量
# 定义数据集和数据加载器
dataset = YourDataset(...)  # 使用你的数据集类
dataloader = DataLoader(dataset, batch_size=10, shuffle=True)