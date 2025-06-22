# gacha_app package

import os
import sys
import tkinter as tk

from .src.core.prize_manager import PrizeManager
from .src.core.gacha_engine import GachaEngine
from .src.utils.config import Config
from .src.utils.history import History
from .src.ui.main_window import MainWindow

def main():
    # 设置工作目录
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    # 初始化配置和历史记录
    config = Config('config')
    history = History(os.path.join('config', 'history.json'))
    
    # 初始化奖品管理器和扭蛋机
    prize_manager = PrizeManager()
    prize_manager.prizes = config.load()['prizes']
    gacha_engine = GachaEngine(prize_manager)
    
    # 创建主窗口
    root = tk.Tk()
    app = MainWindow(root, gacha_engine, prize_manager, config, history)
    root.mainloop()
    
if __name__ == '__main__':
    main()