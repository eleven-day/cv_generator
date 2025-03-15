from typing import Dict, Any, Optional
import os
from google import genai
from google.genai import types
from app.utils.markdown_helpers import extract_html_from_markdown, extract_image_placeholders
from app.utils.templates import DEFAULT_RESUME_HTML, GENERATE_PROMPT_TEMPLATE
from app.utils.logger import app_logger

# 初始化 Google Gemini API 客户端
API_KEY = os.getenv("GEMINI_API_KEY", "AIzaSyD65DzyhRLN4YmGS6PRbJrx10j_PC8nBb0")  # 在生产环境中替换为您的 API 密钥

def generate_resume_content(
    name: str,
    position: str,
    additional_info: Dict[str, Any] = None,
    existing_content: Optional[str] = None,
    update_instructions: Optional[str] = None
) -> Dict[str, Any]:
    """
    使用Google Gemini API生成简历内容
    
    Args:
        name: 用户姓名
        position: 职位
        additional_info: 额外的简历信息
        existing_content: 要更新的现有HTML内容
        update_instructions: 更新现有内容的具体指示
        
    Returns:
        包含HTML内容和图片占位符的字典
    """
    app_logger.info(f"为 {name} 生成简历，职位: {position}")
    
    additional_info_str = ""
    if additional_info:
        for key, value in additional_info.items():
            additional_info_str += f"{key}: {value}\n"
    
    # 创建提示
    if existing_content:
        # 如果更新现有内容，使用不同的提示
        app_logger.info("更新现有简历内容")
        prompt = f"""
        <背景>
        您是一位专业简历撰写AI助手，精通更新专业简历。您专门为中国求职市场服务，了解中国雇主的喜好和期望。
        在中国求职市场，简历中应避免出现工作或学习的空窗期（gap year），如有空窗期应适当填充或合理解释。
        </背景>

        <角色>
        简历撰写专家
        </角色>

        <任务>
        更新现有HTML格式的简历，加入新信息同时保持格式一致。
        </任务>

        <用户输入>
        姓名: {name}
        职位: {position}
        {additional_info_str}
        </用户输入>

        <现有简历>
        {existing_content}
        </现有简历>

        <更新要求>
        {update_instructions if update_instructions else "保持现有排版和设计，更新内容。"}
        </更新要求>

        <输出格式>
        提供更新后的完整HTML格式简历。保留现有图片占位符。
        </输出格式>
        """
    else:
        # 创建新简历
        app_logger.info("创建新简历内容")
        prompt = GENERATE_PROMPT_TEMPLATE.format(
            name=name,
            position=position,
            additional_info=additional_info_str,
            default_html_template=DEFAULT_RESUME_HTML
        )
    
    try:
        # 使用Gemini生成内容
        client = genai.Client(api_key=API_KEY)
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt,
            config=types.GenerateContentConfig(
                max_output_tokens=4000,
                temperature=0.2
            )
        )
        
        # 处理响应文本，以防它包含markdown格式
        raw_text = response.text
        html_content = extract_html_from_markdown(raw_text)
        
        # 提取图片占位符
        image_placeholders = extract_image_placeholders(html_content)
        
        app_logger.info(f"简历生成成功，包含 {len(image_placeholders)} 个图片占位符")
        
        return {
            "html_content": html_content,
            "image_placeholders": image_placeholders
        }
    except Exception as e:
        app_logger.error(f"生成简历内容时出错: {str(e)}")
        raise

if __name__ == "__main__":
    # 测试简历生成功能
    print("测试生成新简历")
    resume_content = generate_resume_content(
        name="张三",
        position="数据分析师",
        additional_info={
            "邮箱": "609887398@qq.com",
            "手机": "18812345678",
            "所在地": "北京",
            "求职意向": "数据分析"
        }
    )
    print(resume_content["html_content"])
    print("图片占位符:", resume_content["image_placeholders"])
    
    # 测试更新功能
    print("\n测试更新现有简历")
    updated_resume = generate_resume_content(
        name="张三",
        position="高级数据分析师",
        additional_info={
            "邮箱": "609887398@qq.com",
            "手机": "18812345678",
            "所在地": "北京",
            "求职意向": "数据分析与挖掘",
            "教育经历": "北京大学，计算机科学与技术，硕士",
            "专业技能": "Python, SQL, 数据可视化",
            "项目经历": "数据分析项目1，数据分析项目2",
            "工作经历": "数据分析师，高级数据分析师",
            "语言能力": "英语CET-6",
            "证书与资质": "数据分析证书",
            "兴趣爱好": "阅读，篮球"
        },
        existing_content=resume_content["html_content"],
        update_instructions="请将简历排版顺序调整为：教育经历、专业技能、项目经历、工作经历、语言能力、证书与资质、兴趣爱好"
    )
    print(updated_resume["html_content"])
    print("图片占位符:", updated_resume["image_placeholders"])