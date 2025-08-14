import os
from flask import request
from openai import OpenAI

def get_files(type):
    documents_path = os.path.abspath('documents').replace('\\', '/')
    file_dir = os.path.join('documents', type)
    files = []
    for file in os.listdir(file_dir):
        file_path = f"file://{documents_path}/{type}/{file}"
        files.append(file_path)
    return files

file_urls = get_files('docx') + get_files('csv')
print(file_urls)

csv_file_path = os.path.join('documents', 'csv','UniverseBeijingTest.csv')
with open(csv_file_path, 'r', encoding='utf-8') as f:
    csv_content = f.read()
# print(csv_content)

client = OpenAI(
    # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
    api_key=os.getenv("DASHSCOPE_API_KEY"),  # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
)

query = f'''
《[clean] 6.13-6.29 年卡专属：酷爽夏日主题实体徽章兑换券（变形金刚主题角色款）.docx》
《[clean] 环球影城大酒店环球影城莲花园自助晚餐券.docx》
《[clean] 熙悦餐厅自助晚餐券.docx》
《产品Terms and Conditions.docx》
《入园须知.docx》
《探索护照介绍.docx》
是一些知识库文件，根据这些文件内容回答问题。
《UniverseBeijingTest.csv》是以'|'为分隔符的CSV文件，
其中的字段notebooklm_query是问题，一共有24个，
notebooklm_answer和qwen3-8b_answer分别是notebooklm和qwen3-8b给出的答案，
first_token_use_time是首个token的耗时。
以下是《UniverseBeijingTest.csv》的所有内容：
################################################################################
{csv_content}
################################################################################
请给二者的回答分别打分，写入到字段notebooklm_score和qwen3-8b_score中，并给出理由，以markdown格式用表格输出。
比如：
问题,notebooklm_score,qwen3-8b_score,理由
'''

completion = client.chat.completions.create(
    model="Moonshot-Kimi-K2-Instruct",
    messages=[{'role': 'user', 'content': query}],
    extra_body={
        "file_url": file_urls
    }
)
answer = completion.choices[0].message.content

with open('kimi_evaluate.md','w', encoding='utf-8') as f:
    f.write(answer)
print(answer)