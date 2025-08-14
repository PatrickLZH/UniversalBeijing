import os
from qwen_agent.agents import Assistant

llm_config = {
        'model': 'qwen3-8b',
        'model_server': 'dashscope',
        'api_key': os.getenv('DASHSCOPE_API_KEY'),
        'generate_cfg': {'top_p': 0.8},
        }

system_message = "对问答对做摘要总结，小标题格式，不超过20个字。"

query = "请总结下这个问答对，小标题格式，不超过20个字。"

# history = [{'role': 'user', 'content': '你好！'}, 
#            {'role': 'assistant', 
#             'content': '你好！欢迎来到北京环球\n\n度假区！有什么问题或需要帮助的吗？[1]\n\n'}]

def get_summary(history):
    bot = Assistant(
        llm=llm_config,
        system_message=system_message,
    )
    history.append({'role': 'user', 'content': query})
    for response in bot.run(messages=history):
        current_response = response[0]['content']
    return current_response

# print(get_summary(history))