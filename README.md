# Gacha Machine (扭蛋机)

一个基于Python和Tkinter的扭蛋机应用程序。

## 功能特点

- 支持自定义奖品（最多30个）
- 每个奖品可设置名称、图片、权重和颜色
- 动画效果展示抽奖过程
- 历史记录和统计信息
- 现代化的用户界面
- 响应式UI设计，支持窗口缩放
- 圆形图片处理和显示
- 表格式奖品管理界面

## 目录结构

```
gacha_app/
├── src/
│   ├── core/           # 核心逻辑
│   │   ├── gacha_engine.py    # 抽奖引擎
│   │   └── prize_manager.py   # 奖品管理
│   ├── ui/            # 用户界面
│   │   ├── main_window.py     # 主窗口
│   │   ├── prize_dialog.py    # 奖品管理对话框
│   │   └── history_dialog.py  # 历史记录对话框
│   └── utils/         # 工具函数
│       ├── config.py          # 配置管理
│       └── history.py         # 历史记录管理
├── resources/         # 资源文件
│   ├── images/        # 图片资源
│   └── app_icon.png   # 应用图标
├── config/           # 配置文件
│   ├── config.json           # 主配置文件
│   ├── example_config.json   # 配置示例
│   └── history.json          # 历史记录
├── run_gacha.py      # 启动脚本
├── setup.py          # 安装脚本
├── requirements.txt  # 依赖列表
└── 启动扭蛋机.bat    # Windows启动脚本
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

2. 首次运行时，点击"🎁 管理奖品"按钮添加奖品：
   - 设置奖品名称
   - 选择奖品图片（支持PNG、JPG等格式）
   - 设置抽中概率（权重）

3. 点击"🎯 开始抽奖"按钮开始抽奖

4. 可以通过"📊 历史"按钮查看历史记录和统计信息

## 配置文件

- `config/config.json`: 存储奖品和程序配置
- `config/history.json`: 存储抽奖历史记录
- `config/example_config.json`: 配置文件示例

## 注意事项

- 奖品图片建议使用正方形图片，程序会自动处理为圆形显示
- 权重值必须为正整数，数值越大概率越高
- 最多支持30个奖品
- 程序支持响应式缩放，可调整窗口大小
- 建议定期备份配置文件

## 版本历史

### v3.0
- 重构项目结构，分离核心逻辑、UI和工具模块
- 实现响应式UI设计，支持窗口缩放
- 添加奖品管理系统，支持自定义奖品和图片上传
- 实现圆形图片处理和显示
- 完善历史记录功能，支持详细统计
- 更新主界面为左右分块布局
- 添加表格式奖品管理界面

## 许可证

MIT License
