#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
扭蛋机应用启动脚本
直接运行此文件即可启动扭蛋机应用
"""

import tkinter as tk
import os
import sys
from pathlib import Path
import traceback

# 添加项目根目录到 Python 路径
sys.path.insert(0, str(Path(__file__).parent))

from gacha_app.src.ui.main_window import MainWindow
from gacha_app.src.core.gacha_engine import GachaEngine
from gacha_app.src.core.prize_manager import PrizeManager
from gacha_app.src.utils.config import Config
from gacha_app.src.utils.history import History

def main():
    # 设置配置文件路径
    config_dir = os.path.join(os.path.dirname(__file__), 'gacha_app', 'config')
    os.makedirs(config_dir, exist_ok=True)
    
    config_path = os.path.join(config_dir, 'config.json')
    history_path = os.path.join(config_dir, 'history.json')
    
    # 初始化配置和历史记录
    config = Config(config_path)
    history = History(history_path)
    
    # 初始化奖品管理器
    prize_manager = PrizeManager(config_path)
    
    # 初始化抽奖引擎
    gacha_engine = GachaEngine(prize_manager)
    
    # 创建主窗口
    root = tk.Tk()
    app = MainWindow(root, gacha_engine, prize_manager, config, history)
    
    # 启动应用
    root.mainloop()

def run_app():
    """启动扭蛋机应用"""
    try:
        main()
    except ImportError as e:
        print(f"❌ 导入错误: {e}")
        print("请确保已安装所需依赖: pip install -r requirements.txt")
        return 1
    except Exception as e:
        print(f"❌ 启动失败: {e}")
        print("错误详情:")
        traceback.print_exc()
        print("\n请检查Python环境和依赖包是否正确安装")
        return 2
    return 0

if __name__ == '__main__':
    sys.exit(run_app()) 