# src/llm.py

import os
from openai import OpenAI
from logger import LOG

class LLM:
    def __init__(self):
        OpenAI.api_key = os.getenv("OEPNAI_API_KEY")
        self.client = OpenAI()
        LOG.add("daily_progress/llm_logs.log", rotation="1 MB", level="DEBUG")

    def generate_daily_report(self, markdown_content, dry_run=False):
        prompt = f"以下是项目的最新进展，根据功能合并同类项，形成一份简报，至少包含：1）新增功能；2）主要改进；3）修复问题；:\n\n{markdown_content}"
        system_prompt = """
        你接下来收到的都是开源项目的最新进展。

        你根据进展，总结成一个中文的报告，以 项目名称和日期 开头，包含：新增功能、主要改进，修复问题等章节。
        
        参考示例如下:

        # LangChain 项目进展

        ## 时间周期：2024-09-01至2024-09-07

        ## 新增功能
        - langchain-box: 添加langchain box包和DocumentLoader
        - 添加嵌入集成测试

        ## 主要改进
        - 将@root_validator用法升级以与pydantic 2保持一致
        - 将根验证器升级为与pydantic 2兼容

        ## 修复问题
        - 修复Azure的json模式问题
        - 修复Databricks Vector Search演示笔记本问题
        - 修复Microsoft Azure Cosmos集成测试中的连接字符串问题
        """
        if dry_run:
            LOG.info("Dry run mode enabled. Saving prompt to file.")
            with open("daily_progress/prompt.txt", "w+") as f:
                f.write(prompt)
            LOG.debug("Prompt saved to daily_progress/prompt.txt")
            return "DRY RUN"

        LOG.info("Starting report generation using GPT model.")
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]
            )
            LOG.debug("GPT response: {}", response)
            return response.choices[0].message.content
        except Exception as e:
            LOG.error("An error occurred while generating the report: {}", e)
            raise

