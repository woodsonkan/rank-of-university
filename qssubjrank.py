import pandas as pd
import requests
from bs4 import BeautifulSoup
import json

# 读取 Excel 文件中的数据
data = pd.read_excel('test.xlsx')

# 合并 site 字段和 url 字段成完整的 URL
data['full_url'] = data['site'] + data['url']

# 遍历每个 URL，发送 HTTP 请求并解析 HTML
for index, row in data.iterrows():
    # 创建一个空的 list 用于存储每个 name 的数据
    name_data = []
    response = requests.get(row['full_url'])
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article = soup.find('article')
        if article:
            data_history_node_id = article.get('data-history-node-id')
            # 构造新的 URL 并发送 HTTP 请求
            new_url = f"https://www.topuniversities.com/rankings/endpoint?nid={data_history_node_id}&page=0&items_per_page=9999&tab="
            print(f"Generated new URL: {new_url}")  # 打印生成的新URL
            new_response = requests.get(new_url)
            if new_response.status_code == 200:
                json_data = json.loads(new_response.text)
                score_nodes = json_data.get('score_nodes', [])
                for score_node in score_nodes:
                    title = score_node.get('title')
                    region = score_node.get('region')
                    rank_display = score_node.get('rank_display')
                    rank = score_node.get('rank')
                    city = score_node.get('city')
                    country = score_node.get('country')
                    print(f"{title}，{country}")  # 打印符合要求的数据
                    # 将数据添加到 name_data list 中
                    name_data.append({
                        'title': title,
                        'region': region,
                        'rank_display': rank_display,
                        'rank': rank,
                        'city': city,
                        'country': country
                    })
    # 将 list 转换为 DataFrame 并保存到 Excel 文件
    name_data_df = pd.DataFrame(name_data)
    name_data_df.to_excel(f"{row['name']}_data.xlsx", index=False, columns=['rank', 'rank_display', 'title', 'city', 'country', 'region'])

