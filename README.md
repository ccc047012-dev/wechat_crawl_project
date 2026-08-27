# 数据爬取与下载准备项目

## 目录结构
```
wechat_crawl_project/
├── raw_data/     # 存放爬取的【原始数据】（不做处理，原样保存）
├── output/       # 存放【结果数据】（整理、清洗后的成果）
├── scripts/      # 爬虫 & 数据处理脚本
├── logs/         # 运行日志
├── requirements.txt
└── README.md
```

## 用途
- 按照你指定的【变量】从网上抓取数据
- 原始数据 → raw_data/
- 处理后的结果（CSV / Excel / JSON / 文本）→ output/
- 所有文件都会保存在你的本机，方便你直接取用

## 如何从 Continue 打开本项目
在 Continue / VS Code 中：文件 → 打开文件夹，选择：
C:\Users\26936\wechat_crawl_project

## 如何安装依赖
powershell
pip install -r requirements.txt
