# Gacha Machine (扭蛋机)

一个基于Python和Tkinter的扭蛋机应用程序。

## 功能特点

- 支持自定义奖品（最多30个）
- 每个奖品可设置名称、图片、权重和颜色
- 动画效果展示抽奖过程
- 历史记录和统计信息
- 现代化的用户界面

## 目录结构

```
gacha_app/
├── src/
│   ├── core/           # 核心逻辑
│   ├── ui/            # 用户界面
│   └── utils/         # 工具函数
├── resources/         # 资源文件
│   ├── images/        # 图片资源
└── config/           # 配置文件
```

## 安装要求

- Python 3.6+
- Pillow >= 9.0.0
- tkinter (通常随Python一起安装)

## 安装步骤

1. 克隆或下载本仓库
2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

1. 运行程序：
   ```bash
   python run_gacha.py
   ```
   或双击 `启动扭蛋机.bat`（Windows）

2. 首次运行时，点击"PRIZES"按钮添加奖品：
   - 设置奖品名称
   - 选择奖品图片
   - 设置抽中概率（权重）
   - 选择显示颜色

3. 点击中央星形按钮或底部"DRAW"按钮开始抽奖

4. 可以通过"HISTORY"按钮查看历史记录和统计信息

## 配置文件

- `config/config.json`: 存储奖品和程序配置
- `config/history.json`: 存储抽奖历史记录

## 注意事项

- 奖品图片建议使用正方形图片，程序会自动缩放至100x100像素
- 权重值必须为正整数，数值越大概率越高
- 最多支持30个奖品
- 建议定期备份配置文件

## 许可证

MIT License
