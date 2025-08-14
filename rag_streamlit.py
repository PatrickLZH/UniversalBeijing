import os
from qwen_agent.agents import Assistant
import streamlit as st
from clipboard_component import copy_component
from functools import lru_cache
import uuid  # 导入uuid用于生成唯一键

ES_PASSWORD = '8Hjlfr0sb7RZFW2L*LuA'

# 初始化 session_state 中的按钮状态
if 'like' not in st.session_state:
    st.session_state.like = False
if 'dislike' not in st.session_state:
    st.session_state.dislike = False

def handle_like_click():
    st.session_state.like = not st.session_state.like  # 切换状态
    st.session_state.dislike = False if st.session_state.like else st.session_state.dislike

def handle_dislike_click():
    st.session_state.dislike = not st.session_state.dislike  # 切换状态
    st.session_state.like = False if st.session_state.dislike else st.session_state.like

def get_llm_config():
    return {
        'model': 'qwen3-8b',
        'model_server': 'dashscope',
        'api_key': os.getenv('DASHSCOPE_API_KEY'),
        'generate_cfg': {'top_p': 0.8}
    }

def get_rag_config():
    return {
        "rag_backend": "elasticsearch",  # 关键：指定使用 ES 后端
        "es": {
            "host": "http://localhost",
            "port": 9200,
            "index_name": "universalbeijing_docs_index" # 自定义索引名称
            },
        "parser_page_size": 500 # 文档分块大小
    }

@lru_cache(maxsize=1)
def get_files(type):
    file_dir = os.path.join(os.getcwd(), 'documents', type)
    files = []
    try:
        if os.path.exists(file_dir):
            for file in os.listdir(file_dir):
                file_path = os.path.join(file_dir, file)
                if os.path.isfile(file_path):
                    files.append(file_path)
    except Exception as e:
        print(f"读取文件目录时发生错误: {e}")
    return files
# 封装按钮渲染逻辑
def render_feedback_buttons(response_text):
    col1, col2, col3 = st.columns([12, 1, 1])
    with col1:
        copy_component("复制",content=response_text) 
    with col2:
        # 显示赞按钮（独立状态）
        if st.session_state.like:
            st.markdown('''
                <button style="background-color:red; color:white; 
                             border:none; padding:8px 14px; 
                             border-radius:4px;">
                    赞
                </button>''', unsafe_allow_html=True)
        else:
            # st.button('赞', on_click=handle_like_click)
            # 添加唯一键值
            st.button('赞', on_click=handle_like_click, key=f"like_{uuid.uuid4().hex}")

    with col3:
        # 显示踩按钮（独立状态）
        if st.session_state.dislike:
            st.markdown('''
                <button style="background-color:red; color:white; 
                             border:none; padding:8px 14px; 
                             border-radius:4px;">
                    踩
                </button>''', unsafe_allow_html=True)
        else:
            # st.button('踩', on_click=handle_dislike_click)
            # 添加唯一键值
            st.button('踩', on_click=handle_dislike_click, key=f"dislike_{uuid.uuid4().hex}")

# 初始化会话状态中的消息历史
if 'messages' not in st.session_state:
    st.session_state.messages = []

# 获取 LLM 配置和文件路径
llm_cfg = get_llm_config()
rag_cfg = get_rag_config()
files = get_files('docx')

# 创建 Assistant 实例
system_message = '''你是一个AI助手，请根据提供的文件内容回答问题。
在输出答案的时候，需要在召回的内容后面加上角标，代表引用的文件的来源，
比如来源于文件《XXX》，标记为[1]，并在输出的最后给文件的来源添加序号。
比如：
这是答案1。[1]
这是答案2。[2]
### 参考：
[1]来自文件《XXX》。
[2]来自文件《XXX》。
如果没有召回内容，不需要写参考文献。
比如：
这是答案。
### 参考：
无参考文献。'''



bot = Assistant(
    llm=llm_cfg,
    system_message=system_message,
    files=files,
    rag_cfg=rag_cfg,
)

# 页面标题
st.title("北京环球影城 AI 助手")

# 显示消息历史
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 输入框用于用户提问
query = st.chat_input("请输入您的问题:")

if query:
    if len(st.session_state.messages) > 10:
        st.session_state.messages = st.session_state.messages[-10:]

    # 新增：重置反馈状态
    st.session_state.like = False
    st.session_state.dislike = False

    # 添加用户消息到历史
    st.session_state.messages.append({"role": "user", "content": query})
    
    with st.chat_message("user"):
        st.markdown(query)

    # 调用模型进行回答
    with st.chat_message("assistant"):
        response_placeholder = st.empty()  # 创建空占位符
        full_response = ""  # 存储完整响应
        last_content = ""  # 用于跟踪上次处理的内容

        # 流式处理模型响应
        for chunk in bot.run(messages=st.session_state.messages):
            if chunk and isinstance(chunk, list) and 'content' in chunk[0]:
                current_content  = chunk[0]['content']
                # 只处理新增内容（避免重复）
                if len(current_content) > len(last_content):
                    new_content = current_content[len(last_content):]
                    full_response += new_content
                    response_placeholder.markdown(full_response + "▌")
                    last_content = current_content  # 更新上次处理的内容

        # 流式输出结束后移除光标
        response_placeholder.markdown(full_response)
        # 添加反馈按钮
        render_feedback_buttons(full_response)

    # 添加助手回答到历史
    st.session_state.messages.append({"role": "assistant", "content": full_response})
