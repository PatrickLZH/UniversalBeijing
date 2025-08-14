import os
import time
from qwen_agent.agents import Assistant

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

system_message = '''你是一个AI助手，请根据提供的文件内容回答问题。
在输出答案的时候，需要在召回的内容后面加上角标，代表引用的文件的来源，
比如来源于文件《XXX》，标记为[1]，并在输出的最后给文件的来源添加序号。
比如：
这是答案1。[1]
这是答案2。[2]
#### 参考：
[1]来自文件《XXX》。
[2]来自文件《XXX》。
如果没有召回内容，不需要写参考文献。
比如：
这是答案。
#### 参考：
无参考文献。'''
bot = Assistant(
    llm=get_llm_config(),
    system_message=system_message,
    files=get_files('docx'),
    rag_cfg=get_rag_config(),
)

def get_answer(query, start_time):
    messages = [{'role': 'user', 'content': query}]
    current_index = 0
    first_word_shown = False
    full_response = ""
    for response in bot.run(messages=messages):
        current_response = response[0]['content'][current_index:]
        current_index = len(response[0]['content'])
        
        if not first_word_shown and len(current_response) > 0:
            elapsed = int((time.time() - start_time)*1000)
            print(f"\n[第一个词耗时: {elapsed}ms]")  # 输出耗时标签
            first_word_shown = True
            
        if current_response:  # 仅当有内容时输出
            full_response += current_response
    print()  # 最终换行
    return elapsed,full_response

if __name__ == "__main__":
    while True:
        query = input("请输入您的问题:")
        start_time = time.time()
        elapsed,full_response = get_answer(query, start_time)
        print(f"查询耗时: {elapsed} 毫秒")
        print("答案:", full_response)
