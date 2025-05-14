# Gacha App

本地可视化扭蛋机应用，使用 Python + Tkinter。

## 结构

```
gacha_app_skeleton/
├── gacha_app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.json
│   └── images/
│       ├── prize1.png
│       ├── prize2.png
│       └── prize3.png
├── setup.py
├── requirements.txt
├── .gitignore
└── README.md
```

## 快速开始

1. 安装依赖：
   ```
   pip install -r requirements.txt
   ```
2. 本地开发：
   ```
   python -m gacha_app.main
   ```
3. 或安装为包并使用命令行启动：
   ```
   pip install -e .
   gacha
   ```
