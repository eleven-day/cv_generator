import re
from typing import Dict

# app/utils/markdown_helpers.py的新函数实现
def extract_html_from_markdown(text):
    """
    从markdown文本中提取HTML内容。
    如果没有检测到markdown格式，则返回原始文本。
    
    Args:
        text: 可能包含markdown格式的文本
        
    Returns:
        提取的HTML或原始文本
    """
    # 检查文本是否包含带有HTML的markdown代码块
    html_pattern = r"```html\s+(.*?)\s+```"
    matches = re.findall(html_pattern, text, re.DOTALL)
    
    if matches:
        # 返回找到的第一个HTML块
        return matches[0]
    else:
        # 未找到markdown HTML块，返回原始文本
        return text

def extract_image_placeholders(html_content):
    """
    从HTML内容中提取图片占位符。
    图片占位符格式为: src="image:placeholder_id"
    
    Args:
        html_content: 包含图片占位符的HTML内容
        
    Returns:
        占位符ID和其alt文本的字典
    """
    # 提取具有正确占位符格式的图像标签
    pattern = r'<img\s+src="image:([^"]+)"\s+alt="([^"]*)"'
    matches = re.findall(pattern, html_content)
    
    # 创建占位符ID和alt文本的字典
    placeholders = {}
    for placeholder_id, alt_text in matches:
        placeholders[placeholder_id] = alt_text
    
    return placeholders


def replace_placeholders_with_images(
    html_content: str, image_data: Dict[str, str]
) -> str:
    """
    用实际图像URL替换HTML内容中的图片占位符。
    
    Args:
        html_content: 包含图片占位符的HTML内容
        image_data: 图片占位符ID和URL的字典
        
    Returns:
        替换占位符后的HTML内容
    """
    # 提取占位符ID和alt文本
    placeholders = extract_image_placeholders(html_content)
    
    # 替换占位符
    for placeholder_id, alt_text in placeholders.items():
        if placeholder_id in image_data:
            # 使用实际图像URL替换占位符
            image_url = image_data[placeholder_id]
            img_tag = f'<img src="{image_url}" alt="{alt_text}">'
            html_content = html_content.replace(
                f'<img src="image:{placeholder_id}" alt="{alt_text}">', img_tag
            )
    
    return html_content

if __name__ == "__main__":
    # 测试新函数实现
    markdown_text = """
    ```html
    <img src="image:123" alt="A placeholder image">
    ```
    """
    html_content = extract_html_from_markdown(markdown_text)
    image_data = {"123": "https://example.com/image.jpg"}
    replaced_html = replace_placeholders_with_images(html_content, image_data)
    print(replaced_html)    