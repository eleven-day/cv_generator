# 更新后的单列式 HTML+CSS 简历模板
DEFAULT_RESUME_HTML = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>个人简历</title>
    <style>
        /* A4 页面设置 */
        body {
            width: 210mm;
            height: 297mm;
            margin: 0 auto;
            padding: 20mm;
            font-family: "SimSun", "Microsoft YaHei", sans-serif;
            box-sizing: border-box;
            color: #333;
        }
        
        /* 简历标题 */
        .resume-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
            border-bottom: 2px solid #1e88e5;
            padding-bottom: 10px;
        }
        
        /* 头像区域 */
        .profile-photo {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            border: 2px solid #1e88e5;
            overflow: hidden;
            background-color: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        /* 个人信息区域 */
        .personal-info {
            flex-grow: 1;
            margin-left: 20px;
        }
        
        .name {
            font-size: 26px;
            font-weight: bold;
            margin-bottom: 5px;
        }
        
        .contact-info {
            display: flex;
            flex-wrap: wrap;
            font-size: 14px;
        }
        
        .contact-item {
            margin-right: 15px;
            margin-bottom: 5px;
        }
        
        /* 简历主体部分 - 单列布局 */
        .resume-body {
            width: 100%;
        }
        
        /* 部分标题 */
        .section-title {
            font-size: 18px;
            font-weight: bold;
            margin-top: 15px;
            margin-bottom: 10px;
            border-bottom: 1px solid #ddd;
            padding-bottom: 5px;
            color: #1e88e5;
        }
        
        /* 教育经历 */
        .education-item {
            margin-bottom: 12px;
        }
        
        .school-logo {
            width: 50px;
            height: 50px;
            background-color: #f0f0f0;
            float: right;
            margin-left: 10px;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        
        .school-name {
            font-weight: bold;
        }
        
        .education-date {
            color: #666;
            font-size: 14px;
        }
        
        /* 工作经历 */
        .experience-item {
            margin-bottom: 15px;
        }
        
        .company-name {
            font-weight: bold;
        }
        
        .job-title {
            font-style: italic;
        }
        
        .experience-date {
            color: #666;
            font-size: 14px;
        }
        
        /* 技能部分 */
        .skills-list {
            display: flex;
            flex-wrap: wrap;
        }
        
        .skill-item {
            background-color: #f0f0f0;
            padding: 5px 10px;
            margin: 0 5px 5px 0;
            border-radius: 3px;
            font-size: 14px;
        }
        
        /* 项目经历 */
        .project-item {
            margin-bottom: 15px;
        }
        
        .project-title {
            font-weight: bold;
        }
        
        .project-date {
            color: #666;
            font-size: 14px;
        }
        
        /* 列表样式 */
        ul {
            margin: 5px 0;
            padding-left: 20px;
        }
        
        li {
            margin-bottom: 5px;
        }
    </style>
</head>
<body>
    <div class="resume-header">
        <div class="profile-photo">
            <!-- 头像占位符 -->
            <img src="image:profile_photo" alt="个人照片">
        </div>
        <div class="personal-info">
            <div class="name">{姓名}</div>
            <div class="contact-info">
                <div class="contact-item">📧 {邮箱}</div>
                <div class="contact-item">📱 {手机}</div>
                <div class="contact-item">🏠 {所在地}</div>
                <div class="contact-item">💼 {求职意向}</div>
            </div>
        </div>
    </div>
    
    <div class="resume-body">
        <!-- 教育经历 -->
        <div class="section-title">教育经历</div>
        <div class="education-item">
            <div class="school-logo">
                <!-- 学校logo占位符 -->
                <img src="image:school_logo" alt="学校logo">
            </div>
            <div class="school-name">{学校名称}</div>
            <div class="education-date">{入学年份} - {毕业年份}</div>
            <div>{专业} · {学历}</div>
            <ul>
                <li>{教育经历描述1}</li>
                <li>{教育经历描述2}</li>
            </ul>
        </div>
        
        <!-- 工作经历 -->
        <div class="section-title">工作经历</div>
        <div class="experience-item">
            <div class="company-name">{公司名称}</div>
            <div class="job-title">{职位名称}</div>
            <div class="experience-date">{开始日期} - {结束日期}</div>
            <ul>
                <li>{工作职责描述1}</li>
                <li>{工作职责描述2}</li>
                <li>{工作职责描述3}</li>
            </ul>
        </div>
        
        <!-- 项目经历 -->
        <div class="section-title">项目经历</div>
        <div class="project-item">
            <div class="project-title">{项目名称}</div>
            <div class="project-date">{项目时间段}</div>
            <ul>
                <li>{项目描述1}</li>
                <li>{项目描述2}</li>
            </ul>
        </div>
        
        <!-- 技能 -->
        <div class="section-title">专业技能</div>
        <div class="skills-list">
            <div class="skill-item">{技能1}</div>
            <div class="skill-item">{技能2}</div>
            <div class="skill-item">{技能3}</div>
            <div class="skill-item">{技能4}</div>
            <div class="skill-item">{技能5}</div>
        </div>
        
        <!-- 语言能力 -->
        <div class="section-title">语言能力</div>
        <ul>
            <li>{语言1} - {熟练程度}</li>
            <li>{语言2} - {熟练程度}</li>
        </ul>
        
        <!-- 证书 -->
        <div class="section-title">证书与资质</div>
        <ul>
            <li>{证书1} ({获得年份})</li>
            <li>{证书2} ({获得年份})</li>
        </ul>
        
        <!-- 兴趣爱好 -->
        <div class="section-title">兴趣爱好</div>
        <ul>
            <li>{兴趣1}</li>
            <li>{兴趣2}</li>
            <li>{兴趣3}</li>
        </ul>
    </div>
</body>
</html>
"""


GENERATE_PROMPT_TEMPLATE = """
<背景>
您是一位专业简历撰写AI助手，精通创建专业、简洁且格式规范的简历。您专门为中国求职市场服务，了解中国雇主的喜好和期望。
在中国求职市场，简历中应避免出现工作或学习的空窗期（gap year），如有空窗期应适当填充或合理解释。
</背景>

<角色>
简历撰写专家
</角色>

<任务>
根据用户提供的信息，使用HTML和CSS创建一份专业简历，适合在A4纸上打印。
</任务>

<风格>
- 专业简洁
- 结构清晰（个人信息、概述、工作经验、教育背景、技能等）
- 整洁的排版，适当使用标题、项目符号和间距
- 图片占位符使用特殊语法标记：<img src="image:placeholder_id" alt="描述">
</风格>

<指标>
- 长度：内容应适合单页A4纸张
- 只关注相关信息
- 使用专业语言和行业适用的术语
- 避免出现空窗期，确保时间线连贯
</指标>

<用户输入>
姓名: {name}
职位: {position}
{additional_info}
</用户输入>

<输出格式>
提供完整的HTML和CSS格式的简历。使用单列布局，按照以下顺序排列主要部分：
1. 个人信息（顶部）
2. 教育经历
3. 工作经历
4. 项目经历
5. 专业技能

可选部分(用户未提供时可忽略)：
6. 语言能力
7. 证书与资质
8. 兴趣爱好

对于任何图片（个人照片、图标等），请使用占位符语法：<img src="image:placeholder_id" alt="描述">，
其中placeholder_id是唯一标识符。

请基于以下模板创建或调整简历：

{default_html_template}
</输出格式>
"""