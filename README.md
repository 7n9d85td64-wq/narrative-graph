# Narrative Graph — L2 结构化叙事知识图谱

Dify 工作流通过 HTTP 读取本仓库的 JSON 数据，提取约束参数注入 Prompt。

## 目录结构

```
data/
  index.json          # 总索引：列出所有节点
  patterns/           # 情节模式节点
  archetypes/         # 人物原型节点
  rhythms/            # 节奏模板节点
  rules/              # 关联规则节点
schema/
  node.schema.json    # 节点 JSON Schema 定义
```

## 节点格式

每个 JSON 文件包含一个节点，字段：
- `node_id`: 唯一标识符，Dify 代码节点用此 ID 查询
- `type`: 节点类型 (plot_pattern / character_arc / archetype / rhythm / rule)
- `properties`: 该节点特有的约束参数
- `edges`: 关联关系数组，每条包含 `relation` (关系类型) 和 `target` (目标 node_id)

## Dify 调用方式

工作流中「代码节点」通过 raw.githubusercontent.com 或其他 CDN 拉取：

```python
import requests, json

# 1. 读取索引
index = requests.get("https://raw.githubusercontent.com/.../index.json").json()

# 2. 按 node_id 读取具体节点
node = requests.get(f"https://raw.githubusercontent.com/.../{node_type}s/{node_id}.json").json()

# 3. 提取约束参数
constraints = node["properties"]

# 4. 遍历关联节点
for edge in node["edges"]:
    related = load_node(edge["target"])
```

## 与 Obsidian 的同步

Obsidian 笔记中的 `---yaml frontmatter---` 可用于半自动生成 JSON 节点。
未来可通过脚本批量转换。
