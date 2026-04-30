import streamlit as st
import os

st.set_page_config(
    page_title="多功能AI助手",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

from openai import OpenAI

client = OpenAI(
    api_key=st.secrets["DEEPSEEK_API_KEY"],
    base_url="https://api.deepseek.com"
)

with st.sidebar:
    st.title("🧠 多功能AI助手")
    st.markdown("---")
    menu = st.selectbox(
        "选择功能",
        [
            "💬 AI智能对话",
            "📝 文案生成",
            "💻 代码助手",
            "🌐 多语言翻译",
            "📄 文本总结",
            "📂 文件内容问答"
        ]
    )
    st.markdown("---")
    st.info("基于 DeepSeek 大模型")

# 对话
if menu == "💬 AI智能对话":
    st.header("💬 AI智能对话")
    st.caption("支持上下文记忆")

    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    prompt = st.chat_input("输入你想询问的内容...")

    if prompt:
        st.chat_message("user").markdown(prompt)
        st.session_state.chat_messages.append({"role": "user", "content": prompt})

        with st.chat_message("assistant"):
            with st.spinner("思考中..."):
                response = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=st.session_state.chat_messages
                )
                ans = response.choices[0].message.content
                st.markdown(ans)
                st.session_state.chat_messages.append({"role": "assistant", "content": ans})

    if st.button("清空对话记录"):
        st.session_state.chat_messages = []
        st.rerun()

# 文案生成
elif menu == "📝 文案生成":
    st.header("📝 AI文案生成")
    kind = st.selectbox("文案类型", ["工作邮件", "工作总结", "朋友圈文案", "短视频脚本", "广告语"])
    prompt = st.text_area("输入需求", height=120)
    if st.button("生成文案") and prompt:
        with st.spinner("生成中..."):
            rsp = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role":"user","content":f"请生成{kind}，内容：{prompt}"}]
            )
            st.markdown("### 生成结果")
            st.success(rsp.choices[0].message.content)

# 代码助手
elif menu == "💻 代码助手":
    st.header("💻 AI代码助手")
    task = st.radio("选择功能", ["写代码", "解释代码"], horizontal=True)
    lang = st.selectbox("编程语言", ["Python", "Java", "JavaScript", "C++", "SQL", "HTML"])
    code_input = st.text_area("输入内容", height=150)
    if st.button("执行") and code_input:
        with st.spinner("处理中..."):
            rsp = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role":"user","content":f"{task}，语言：{lang}，内容：{code_input}"}]
            )
            st.code(rsp.choices[0].message.content)

# 翻译
elif menu == "🌐 多语言翻译":
    st.header("🌐 AI智能翻译")
    col1, col2 = st.columns(2)
    with col1:
        from_lang = st.selectbox("源语言", ["自动检测", "中文", "英文", "日文", "韩文"])
        text = st.text_area("输入文本", height=200)
    with col2:
        to_lang = st.selectbox("目标语言", ["中文", "英文", "日文", "韩文"])
        if st.button("立即翻译") and text:
            with st.spinner("翻译中..."):
                rsp = client.chat.completions.create(
                    model="deepseek-chat",
                    messages=[{"role":"user","content":f"把{from_lang}翻译成{to_lang}：{text}"}]
            )
            st.markdown("### 翻译结果")
            st.success(rsp.choices[0].message.content)

# 总结
elif menu == "📄 文本总结":
    st.header("📄 长文本总结")
    text = st.text_area("粘贴需要总结的文本", height=220)
    level = st.radio("总结风格", ["简洁", "详细"], horizontal=True)
    if st.button("一键总结") and text:
        with st.spinner("总结中..."):
            rsp = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role":"user","content":f"{level}总结以下内容，保留核心信息：{text}"}]
            )
            st.info(rsp.choices[0].message.content)

# 文件问答
elif menu == "📂 文件内容问答":
    st.header("📂 上传文件并提问")
    uploaded_file = st.file_uploader("上传 TXT / MD 文件", type=["txt", "md"])
    question = st.text_input("针对文件内容提问")
    if uploaded_file and question and st.button("分析文件"):
        content = uploaded_file.read().decode("utf-8")
        with st.spinner("分析中..."):
            rsp = client.chat.completions.create(
                model="deepseek-chat",
                messages=[{"role":"user","content":f"文件内容：{content}\n问题：{question}"}]
            )
            st.success(rsp.choices[0].message.content)