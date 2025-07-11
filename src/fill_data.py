from openai import OpenAI
import json
from jinja2 import Template
import random  # 添加random模块

client = OpenAI(api_key="<DeepSeek API Key>", base_url="https://api.deepseek.com")


prompt_template = Template("""
你是一个专业的数据标注员，请参考示例，输出十条意图为{{intent}}的文本，示例：

{{texts_list}}

请以列表格式输出十条意图为{{intent}}的文本，不要有其他内容。
""")

datas = json.load(open('data/intent.json', 'r', encoding='utf-8'))

for intent, texts in datas.items():
    if len(texts) >= 100:
        continue
    
    # 如果文本数量大于10，随机选择10条；否则使用所有文本
    sample_texts = random.sample(texts, min(10, len(texts)))
    texts_list = '\n'.join([f'- {text}' for text in sample_texts])
    prompt = prompt_template.render(intent=intent, texts_list=texts_list)
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt},  # 使用prompt而不是未定义的text
        ],
        stream=False
    )
    content = response.choices[0].message.content
