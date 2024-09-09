import os
import requests
from bs4 import BeautifulSoup

from datetime import datetime


class HackerNews:
    def __init__(self) -> None:
        pass

    def fetch_hackernews_top_stories(self):
        url = "https://news.ycombinator.com/"
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功

        soup = BeautifulSoup(response.text, "html.parser")
        # 查找包含新闻的所有 <tr> 标签
        stories = soup.find_all("tr", class_="athing")

        top_stories = []
        for story in stories:
            title_tag = story.find("span", class_="titleline").find("a")
            if title_tag:
                title = title_tag.text
                link = title_tag["href"]
                top_stories.append({"title": title, "link": link})

        if len(top_stories) == 0:
            return None

        date = datetime.now().strftime("%Y-%m-%d")
        hour = datetime.now().strftime("%H")

        save_path = os.path.join("hacker_news", date)
        os.makedirs(save_path, exist_ok=True)

        md_path = os.path.join(save_path, f"{hour}.md")

        with open(md_path, "w") as md:
            md.write(f"# # Hacker News - ({date}-{hour}:00)\n\n")
            for idx, story in enumerate(top_stories, start=1):
                md.write(f"{idx}. [{story['title']}]({story['link']})\n")

        return md_path

if __name__ == "__main__":
    stories = HackerNews().fetch_hackernews_top_stories()
