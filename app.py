"""
AI Resume Optimizer — Streamlit App
Upload your resume, get AI-powered analysis and improvement suggestions.
"""
import streamlit as st
from src.parser import parse_resume
from src.rag_engine import build_vectorstore, retrieve_context
from src.analyzer import analyze_section, analyze_overall, chat_about_resume
from src.config import DEEPSEEK_API_KEY

# ─── Page config ───
st.set_page_config(
    page_title="AI简历优化器",
    page_icon="📄",
    layout="wide",
)

# ─── Sidebar ───
with st.sidebar:
    st.title("📄 AI简历优化器")
    st.markdown("---")
    st.markdown("### 使用说明")
    st.markdown("""
    1. 上传你的简历（PDF/DOCX）
    2. 等待AI分析完成
    3. 点击左侧模块查看建议
    4. 在聊天框中追问细节
    """)
    st.markdown("---")
    st.markdown("### 分析模块")
    analysis_mode = st.radio(
        "选择分析模式",
        ["整体评估", "教育背景", "项目经历", "实习/工作经历", "技能栈", "自由提问"],
    )
    st.markdown("---")
    st.caption("Powered by DeepSeek + RAG")

# ─── Main area ───
st.title("📄 AI 简历优化器")
st.caption("上传简历，获取AI驱动的专业分析和改进建议")

# ─── Check API key ───
if not DEEPSEEK_API_KEY or DEEPSEEK_API_KEY == "sk-your-deepseek-key":
    st.warning("⚠️ 请先在 `.env` 文件中配置你的 DeepSeek API Key")
    with st.expander("如何获取API Key？"):
        st.markdown("""
        1. 访问 [platform.deepseek.com](https://platform.deepseek.com)
        2. 注册/登录账号
        3. 在 API Keys 页面创建新的 Key
        4. 将 Key 复制到项目根目录的 `.env` 文件中：
        ```
        DEEPSEEK_API_KEY=sk-your-actual-key
        ```
        """)
    st.stop()

# ─── File upload ───
uploaded_file = st.file_uploader(
    "上传简历文件",
    type=["pdf", "docx"],
    help="支持 PDF 和 Word 文档",
)

if uploaded_file is None:
    st.info("👆 请上传你的简历文件开始分析")
    # Show example
    with st.expander("没有简历？点这里看演示效果"):
        st.markdown("""
        ### 演示功能展示

        上传简历后，AI 将自动：
        - 📊 **整体评估**：从5个维度打分，指出核心优势和短板
        - 🎓 **教育背景分析**：检查学历、课程、GPA等呈现方式
        - 💼 **项目经历优化**：改写为STAR法则，补充量化数据
        - 🛠 **技能栈检查**：确保关键词覆盖目标岗位
        - 💬 **自由提问**：基于简历内容，随时追问优化建议
        """)
    st.stop()

# ─── Parse resume ───
file_bytes = uploaded_file.read()
try:
    resume_text, file_type = parse_resume(file_bytes, uploaded_file.name)
except ValueError as e:
    st.error(str(e))
    st.stop()

if not resume_text.strip():
    st.error("未能从文件中提取到文字内容，请确认文件不是扫描图片。")
    st.stop()

# ─── Build vector store (cached) ───
@st.cache_resource(show_spinner=False)
def get_vectorstore(resume_text: str):
    return build_vectorstore(resume_text)

with st.spinner("🔍 正在分析简历..."):
    vectorstore = get_vectorstore(resume_text)

# ─── Two-column layout ───
col_left, col_right = st.columns([1, 2])

with col_left:
    st.subheader("📋 简历原文")
    with st.container(height=500):
        st.text_area("", resume_text, height=480, label_visibility="collapsed")

    # Stats
    word_count = len(resume_text)
    st.metric("字数统计", word_count)
    st.metric("文件类型", file_type.upper())

with col_right:
    st.subheader(f"🤖 {analysis_mode}")

    with st.spinner("AI 分析中..."):
        if analysis_mode == "整体评估":
            result = analyze_overall(resume_text)
            st.markdown(result)

        elif analysis_mode == "自由提问":
            # Initialize chat history
            if "messages" not in st.session_state:
                st.session_state.messages = []

            # Display chat history
            for msg in st.session_state.messages:
                with st.chat_message(msg["role"]):
                    st.markdown(msg["content"])

            # Chat input
            if question := st.chat_input("基于你的简历，想问什么？"):
                st.session_state.messages.append({"role": "user", "content": question})
                with st.chat_message("user"):
                    st.markdown(question)

                context = retrieve_context(vectorstore, question)
                with st.chat_message("assistant"):
                    with st.spinner("思考中..."):
                        answer = chat_about_resume(context, question)
                        st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})

        else:
            # Extract relevant section
            section_map = {
                "教育背景": ["教育", "学校", "大学", "学历", "专业", "GPA", "成绩"],
                "项目经历": ["项目", "经历", "开发", "负责", "使用", "实现"],
                "实习/工作经历": ["实习", "工作", "公司", "任职", "担任"],
                "技能栈": ["技能", "掌握", "熟悉", "了解", "语言", "框架", "工具"],
            }

            keywords = section_map.get(analysis_mode, [analysis_mode])
            # Combine keyword search
            context_parts = []
            for kw in keywords:
                context_parts.append(retrieve_context(vectorstore, kw, k=3))
            context = "\n\n".join(context_parts)

            result = analyze_section(analysis_mode, context[:3000] if context else "未找到相关内容")
            st.markdown(result)

# ─── Footer ───
st.markdown("---")
st.caption("⚠️ AI分析仅供参考，建议结合人工判断使用。简历数据仅用于本次分析，不会存储。")
