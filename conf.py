# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'P5 CPU MOCKUP UP board'
copyright = '2025, Jeremy_Chen'
author = 'Jeremy_Chen'
release = '0.0.1'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
	"sphinx_rtd_theme",
    'sphinx_copybutton',
    'sphinxcontrib.video'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# conf.py

numfig = True  # 启用自动编号
numfig_format = {
    'figure': 'Figure %s',  # 定义图片编号格式（英文可改为 'Figure %s'）
    'table': 'Table %s',
    'code-block': 'Code %s',
    "section": 'Section %s'    # 章节编号（需 Sphinx >= 3.5）
}

numfig_secnum_depth = 3  # 控制章节编号层级

html_theme_options = {
    "navigation_depth": 4,  # 控制侧边栏展开层级
    "collapse_navigation": False,  # 禁止折叠导航（可选）
    "sticky_navigation": True
}

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
html_theme_options = {"navigation_depth": 3}  # 确保侧边栏展开层级足够

# 可选：扩展路径到系统路径（避免路径错误）
import os
import sys
sys.path.append(os.path.abspath('_static'))


# PDF 文档元数据
pdf_documents = [
    ('index', 'output_filename', '文档标题', '作者'),
]

# 中文字体配置（需提前安装系统字体）
pdf_font_path = ['/usr/share/fonts/truetype/simsun']  # 示例路径（Windows为 C:\Windows\Fonts）
pdf_style_path = ['.']
pdf_stylesheets = ['zh_CN']  # 自定义样式表

# 中文换行与断词
pdf_language = "zh_CN"
pdf_fit_mode = "shrink"  # 自动调整内容宽度