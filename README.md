# AI 简历优化器 (AI Resume Optimizer)

基于 RAG + DeepSeek 的智能简历分析与优化工具。上传简历 PDF/DOCX，获得分模块的AI分析、评分和改进建议。

## 功能

- **整体评估** — 5维度评分，核心优势与短板分析
- **分模块优化** — 教育背景、项目经历、实习经历、技能栈逐个优化
- **AI对话** — 基于简历内容的自由问答，追问具体修改建议
- **量化评分** — 每项给出 1-10 分评分，直观了解简历质量

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Streamlit |
| LLM | DeepSeek (deepseek-chat) |
| 向量存储 | ChromaDB |
| 嵌入模型 | text2vec-base-chinese（本地运行，免费） |
| RAG框架 | LangChain |
| 文档解析 | PyPDF + python-docx |

## 为什么选择 DeepSeek？

- 国产大模型，中文理解能力强
- API 价格极低（约 OpenAI 的 1/10）
- API 完全兼容 OpenAI 格式，代码改动最小
- 嵌入模型本地运行，零成本

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置 API Key

```bash
cp .env.example .env
# 编辑 .env 文件，填入你的 DeepSeek API Key
```

去 [platform.deepseek.com](https://platform.deepseek.com) 注册获取 Key，新用户有免费额度。

### 3. 运行

```bash
streamlit run app.py
```

浏览器打开 http://localhost:8501

## 项目结构

```
ai-resume-optimizer/
├── app.py              # Streamlit 主界面
├── src/
│   ├── config.py       # 配置管理
│   ├── parser.py       # PDF/DOCX 解析
│   ├── rag_engine.py   # 向量存储与检索（本地嵌入模型）
│   └── analyzer.py     # AI 分析逻辑
├── data/               # 示例简历
├── requirements.txt
└── .env.example
```

## 简历亮点（写在简历里）

> **AI简历优化器** — 基于RAG技术的智能简历分析工具
> - 使用 LangChain + ChromaDB 构建RAG pipeline，实现简历文档的语义检索
> - 集成 DeepSeek 大模型，分5个维度对简历进行评分和生成优化建议
> - 采用本地嵌入模型（text2vec-base-chinese），零成本向量化方案
> - 技术栈：Python / Streamlit / LangChain / ChromaDB / DeepSeek API
> - 已部署在线Demo：[你的HuggingFace链接]
