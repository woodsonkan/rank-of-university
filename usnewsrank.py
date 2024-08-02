import requests
import openpyxl

# 创建一个新的Excel工作簿和工作表
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "College Rankings"
ws.append(["Rank", "Name", "Location"])

base_url = "https://www.usnews.com/best-colleges/api/search?format=json&schoolType=national-liberal-arts-colleges&_sort=rank&_sortDirection=asc&_page="
headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    "accept-language": "zh-CN,zh;q=0.8",
    "cache-control": "max-age=0",
    "cookie": "usn_visitor_id=0d793517c21c2d00e21b84669400000091591700; akacd_www=2147483647~rv=29~id=0d88a8ea1527d99faa911d2339e4719e; usn_bot=27a1c8f708df9d5d51a5cfc1e90d6963; _abck=02D37E3FFC769D07323FF801656E9848~-1~YAAQyFQhFzDeTOiQAQAARQMhDgwqoyGJQ3vA93Xnb6KN3JS5i/PHma47gBzJ0m27wtpfpTML4sKZzqakbc1sxQJaOeqYnOKKR2UR/hXRtEoEMxjV02dk4HbkoirGm9n8YNhsm7084RQDjH+Je83eoG6cEFwDvZ9OyuAo1vuhyVbALxCuaD80yZnWE8BRYbFU2Bl0bzXpi9J9gHkCREv9CCUYGRY2zbOHXTYDwdP7/VbGTSWnybRB/QkUE+2IwFeVkZAxxoEAl9kBJNQ8WVKFtgMQNnoMjv5cbgMAkpV6zfXR2sMd646B9njMWPD+oPWezT5sZRSRgvrju5nSCe3kI25Ni0JVEnorPyNRjadDs0YW5otG1RHdMY8865zXWLtl9DRboLjnCpn2gA==~-1~-1~-1; gdpr_agreed=4; usn_session_id=2251893010168169; cogv=education; usn_src=web:col_compass:na:ranking_lrail_setting:20171003; edu-page-views=3; modal-page-views=3; bm_so=0948EA97F8B45B3C5255B65FCDF254936C243604A6F3DBF3CE03462D07765BC3~YAAQsMHJF6YtFPqQAQAAinI9DgB94jGLHr933APs993p3be/k2sjx+E2E8mmR9Bp9gkZvc+gepzXTi0mWMpP0QMlawf9mFDVO5hNhskHOp+LlmpjGSMMYT1xhUNKtMquhyFjeu2jsf14SK7RBhrVNHJrw3+Mt8RoJHQW+/31vDa+Egl1b3+EiXfl3AdTbxOKTKlT4jnjuH6PL1hDL/K6+dRNsFyP12+B2Q7PteGMR+4jpIE3RumLwqyOKWaFg+QpDYkMtPWK53StAEkkA4uF1Xrve7VEybrkzFoKIpTCZ15JudRhhskYlDzACN24oSFpcQDdfPuY7yDLvjeK6xlzosVjaB9A47XgWIUMCqPTIwSvOVtsJHco55UIHtW9cYRe0sN4IJDtZvAff4jhNrQqosYVcgKpM7KdAYdBfJ6JBicOp35hMnj1Ptjgbm1zzUXGV7mwzyWWkMfH5qufN7S1wRnM2gIQ+VN0L9TeOfhMUrJe7PYPXrQzkunkJAG0dZW0yvn0TP5zV4WoPWIEBrPkUIo1kwQ4XskOV0Dyd0HRtHHs4JZvHO22emcsBShtFA+hZE/kVYyHXsFbk9rl028=",
    "priority": "u=0, i",
    "sec-ch-ua": "\"Not)A;Brand\";v=\"99\", \"Brave\";v=\"127\", \"Chromium\";v=\"127\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "sec-gpc": "1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
}

for page in range(1, 23):
    response = requests.get(base_url + str(page), headers=headers)
    
    # 检查请求是否成功
    if response.status_code == 200:
        data = response.json()
        items = data.get('data', {}).get('items', [])
        
        # 提取并显示每个institution的数据
        for item in items:
            institution = item.get('institution', {})
            name = institution.get('displayName', '')
            location = institution.get('location', '')
            rank = institution.get('rankingDisplayRank', '')

            # 在终端上显示数据内容
            print(f"Rank: {rank}, Name: {name}, Location: {location}")
            
            # 将数据写入Excel表格
            ws.append([rank, name, location])
    else:
        print(f"无法获取第 {page} 页的数据。状态码: {response.status_code}")

# 保存Excel文件
wb.save("college_rankings.xlsx")
