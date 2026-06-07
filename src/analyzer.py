"""
AI Analyzer: score resume sections and generate improvement suggestions.
Uses DeepSeek API (OpenAI-compatible).
"""
from openai import OpenAI
from src.config import DEEPSEEK_API_KEY, DEEPSEEK_BASE_URL, DEEPSEEK_MODEL

client = OpenAI(api_key=DEEPSEEK_API_KEY, base_url=DEEPSEEK_BASE_URL)

SYSTEM_PROMPT = """你是一位资深的HR和简历优化专家，精通中国互联网/AI行业的招聘标准。

你的任务：
1. 分析简历的每个模块（教育背景、项目经历、实习经历、技能栈等）
2. 指出每个模块的具体问题
3. 给出可直接使用的改进版本
4. 以结构化、可操作的方式呈现建议

评分标准（1-10分）：
- 内容完整性：关键信息是否齐全
- 量化成果：是否有具体数据和成果
- 技术关键词：是否包含行业热门技术词汇
- 表达清晰度：语言是否简洁有力
- 排版结构：逻辑是否清晰

请用中文输出，保持专业、直接、有帮助。"""


def analyze_section(section_name: str, section_content: str) -> str:
    """Analyze a specific section of the resume."""
    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""请分析简历中的【{section_name}】部分：

原文内容：
{section_content if section_content else "（此部分为空）"}

请按以下格式输出：
### 当前评分：X/10
### 存在的问题：
1. ...
2. ...
### 改进建议：
1. ...
2. ...
### 优化后的版本：
（直接给出改写后的内容）""",
            },
        ],
        temperature=0.7,
        max_tokens=2000,
    )
    return response.choices[0].message.content


def analyze_overall(resume_text: str) -> str:
    """Generate an overall resume assessment."""
    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""请对以下简历做整体评估：

{resume_text[:4000]}

请按以下格式输出：
## 整体评分：X/10

### 核心优势（2-3点）
### 最大短板（2-3点）
### 优先改进清单（按重要性排序，至少5条）
### 针对「AI/互联网行业」的特别建议""",
            },
        ],
        temperature=0.7,
        max_tokens=2000,
    )
    return response.choices[0].message.content


def chat_about_resume(context: str, user_question: str) -> str:
    """Answer user questions about their resume with RAG context."""
    response = client.chat.completions.create(
        model=DEEPSEEK_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": f"""基于以下简历内容回答用户问题。

简历内容：
{context}

用户问题：{user_question}

请给出具体、可操作的建议。如果是修改建议，直接给出改写后的版本。""",
            },
        ],
        temperature=0.7,
        max_tokens=1500,
    )
    return response.choices[0].message.content
