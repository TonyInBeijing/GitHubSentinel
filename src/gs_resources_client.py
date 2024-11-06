from datetime import datetime
import os
from logger import LOG # 导入日志模块
import requests # 导入requests库用于HTTP请求
from bs4 import BeautifulSoup # 导入BeautifulSoup库用于解析HTML内容

class GSResourcesClient:
    def __init__(self):
        self.url = 'https://www.thegsresources.com/_forum/forum/technical-forums/general-maintenance'

    def fetch_top_stories(self):
        LOG.debug("准备获取GS Resources论坛的热门帖子。")
        try:
            response = requests.get(self.url, timeout=10)
            response.raise_for_status()  # 检查请求是否成功
            top_stories = self.parse_stories(response.text)  # 解析新闻数据
            return top_stories
        except Exception as e:
            LOG.error(f"获取GS Resources论坛的热门帖子失败：{str(e)}")
            return []
        
    def parse_stories(self, html_content):
        LOG.debug("解析GS Resources论坛的HTML内容。")
        soup = BeautifulSoup(html_content, 'html.parser')
        stories = soup.find_all('tr', class_='topic-item')  # 查找所有包含新闻的<tr>标签
        top_stories = []
        
        for story in stories:
            title_tag = story.find('div', class_='topic-wrapper').find('a',class_='topic-title')
            if title_tag:
                title = title_tag.text
                link = title_tag['href']
                top_stories.append({'title': title, 'link': link})
        return top_stories
    
    def export_top_stories(self, date=None, hour=None):
        LOG.debug("准备导出GS Resources论坛的热门帖子。")
        top_stories = self.fetch_top_stories()
        
        if not top_stories:
            LOG.warning("未找到任何GS Resources论坛的热门帖子。")
            return None
        
        # 如果未提供 date 和 hour 参数，使用当前日期和时间
        if date is None:
            date = datetime.now().strftime('%Y-%m-%d')
        if hour is None:
            hour = datetime.now().strftime('%H')
            
        # 构建存储路径
        dir_path = os.path.join('gs_resources', date)
        os.makedirs(dir_path, exist_ok=True)  # 确保目录存在
        
        file_path = os.path.join(dir_path, f'{hour}.md')  # 定义文件路径
        with open(file_path, 'w') as file:
            file.write(f"# GS Resources论坛热门帖子 ({date} {hour}:00)\n\n")
            for idx, story in enumerate(top_stories, start=1):
                file.write(f"{idx}. [{story['title']}]({story['link']})\n")
        LOG.info(f"GS Resources论坛热门帖子文件生成：{file_path}")
        return file_path
    
    
if __name__ == "__main__":
    client = GSResourcesClient()
    client.export_top_stories()
