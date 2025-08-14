import os
import time
import pandas as pd
from rag_main_test import get_answer
def extract_qa_from_txt(file_path):
    queries = []
    answers = []
    elapseds = []
    full_responses = []
    current_query = None
    
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            stripped = line.strip()
            if not stripped:
                continue
                
            if stripped[0].isdigit() and '.' in stripped.split()[0]:
                # 新问题开始
                if current_query:
                    current_query = current_query[4:]
                    print(current_query)
                    queries.append(current_query)
                    answers.append(current_answer.strip())

                    start_time = time.time()
                    elapsed, full_response = get_answer(current_query, start_time)
                    elapseds.append(elapsed)
                    full_responses.append(full_response)
                current_query = stripped
                current_answer = ""
            elif current_query:
                current_answer += stripped + " "
    
    # 处理最后一个问答对
    if current_query and current_answer:
        current_query = current_query[4:]
        print(current_query)
        queries.append(current_query)
        answers.append(current_answer.strip())

        start_time = time.time()
        elapsed, full_response = get_answer(current_query, start_time)
        elapseds.append(elapsed)
        full_responses.append(full_response)
        
    return queries, answers, elapseds, full_responses

# def write_to_csv(queries, answers, output_path):
def write_to_csv(queries, answers, elapseds, full_responses, output_path):
    """将问答对写入csv文件"""
    # 创建DataFrame
    df = pd.DataFrame({
        'notebooklm_query': queries,
        'notebooklm_answer': answers,
        'qwen3-8b_answer': full_responses,
        'first_token_use_time': elapseds
    })
    
    # 写入csv文件
    df.to_csv(output_path, sep='|', index=False)
    print(f"成功生成csv文件: {output_path}")

# 主程序
if __name__ == "__main__":
    # 文件路径配置
    txt_file = os.path.join(os.getcwd(),'documents','txt','NotebookLM_常见问题解答.txt')
    print(txt_file)
    output_file = os.path.join(os.getcwd(),'documents','csv','UniverseBeijingTest.csv')
    print(output_file)
    
    # 处理文件
    if os.path.exists(txt_file):
        queries, answers, elapseds, full_responses = extract_qa_from_txt(txt_file)
        # queries, answers = extract_qa_from_txt(txt_file)
        write_to_csv(queries, answers, elapseds, full_responses, output_file)
        # write_to_csv(queries, answers, output_file)
    else:
        print(f"错误: 文件不存在 - {txt_file}")


# import os
# import time
# import pandas as pd
# from rag_main_test import get_answer

# def process_questions_from_excel(file_path):
#     # 读取Excel文件
#     df = pd.read_excel(file_path)

#     # 遍历每一行，调用 get_answer 并写入答案
#     for index, row in df.iterrows():
#         question = row['问题（必填）']
#         if pd.isna(question) or question.strip() == '':
#             continue

#         print(f"处理问题：{question}")
#         start_time = time.time()
#         elapsed, full_response = get_answer(question, start_time)
#         df.at[index, '答案（必填）'] = full_response.strip()
#         print(f"生成答案：{full_response[:50]}...")

#     return df

# # 主程序
# if __name__ == "__main__":
#     # 文件路径配置
#     excel_dir = os.path.join(os.getcwd(), 'documents', 'excel')
#     excel_file = os.path.join(excel_dir, 'QwenAgent-qwen3-8b.xlsx')

#     # 处理文件
#     if os.path.exists(excel_file):
#         updated_df = process_questions_from_excel(excel_file)
#         # 保存回原文件或新文件
#         updated_df.to_excel(excel_file, index=False)
#         print(f"处理完成，已更新文件：{excel_file}")
#     else:
#         print(f"错误: 文件不存在 - {excel_file}")
