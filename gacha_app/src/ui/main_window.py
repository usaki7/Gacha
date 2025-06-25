import tkinter as tk
from tkinter import font, messagebox, filedialog
from PIL import Image, ImageTk, ImageDraw
import os
import random
from datetime import datetime

from ..utils.config import COLOR_PALETTE
from .prize_dialog import PrizeDialog
from .history_dialog import HistoryDialog

class MainWindow:
    def __init__(self, master, gacha_engine, prize_manager, config, history):
        self.master = master
        self.gacha_engine = gacha_engine
        self.prize_manager = prize_manager
        self.config = config
        self.history = history
        
        # 基础设置
        self.master.title('扭蛋机 v3.0 - 自定义奖品版')
        self.master.geometry('800x600')
        self.master.configure(bg=COLOR_PALETTE['background'])
        self.master.resizable(True, True)
        
        # 设置最小窗口大小
        self.master.minsize(600, 450)
        
        # 基准尺寸 - 用于缩放计算
        self.base_width = 800
        self.base_height = 600
        self.scale_factor = 1.0
        
        # 设置应用图标
        try:
            icon_path = self.create_app_icon()
            self.app_icon = ImageTk.PhotoImage(file=icon_path)
            self.master.iconphoto(True, self.app_icon)
        except Exception as e:
            print(f"无法设置应用图标: {e}")

        # 字体定义 - 会在缩放时动态调整
        self.update_fonts()

        self.images = []
        self.scaled_images = []  # 存储缩放后的图像
        self.original_images = []  # 存储原始图像对象
        self.animating = False
        self.current_result = None
        
        self.load_images()
        self.setup_ui()
        self.update_statistics()
        
        # 绑定窗口大小变化事件
        self.master.bind("<Configure>", self.on_window_resize)
        
    def update_fonts(self):
        """根据缩放因子更新字体大小"""
        base_title_size = 18
        base_button_size = 14
        base_stats_size = 10
        base_result_size = 16
        base_small_button_size = 10
        
        title_size = max(int(base_title_size * self.scale_factor), 10)
        button_size = max(int(base_button_size * self.scale_factor), 8)
        stats_size = max(int(base_stats_size * self.scale_factor), 8)
        result_size = max(int(base_result_size * self.scale_factor), 10)
        small_button_size = max(int(base_small_button_size * self.scale_factor), 8)
        
        self.title_font = font.Font(family="Arial", size=title_size, weight="bold")
        self.button_font = font.Font(family="Arial", size=button_size, weight="bold")
        self.stats_font = font.Font(family="Courier New", size=stats_size)
        self.result_font = font.Font(family="Arial", size=result_size, weight="bold")
        self.small_button_font = font.Font(family="Arial", size=small_button_size)
        
    def on_window_resize(self, event):
        """处理窗口大小变化，实现整体缩放"""
        # 只处理主窗口的大小变化
        if event.widget == self.master:
            # 计算新的缩放因子
            width_scale = event.width / self.base_width
            height_scale = event.height / self.base_height
            
            # 使用较小的缩放因子以确保内容完全可见
            self.scale_factor = min(width_scale, height_scale)
            
            # 更新字体
            self.update_fonts()
            
            # 更新UI元素
            self.update_ui_scale()
            
            # 更新图像（但不在动画播放期间）
            if (hasattr(self, 'image_label') and hasattr(self, 'original_images') and self.original_images and 
                not (hasattr(self, 'animating') and self.animating)):
                # 如果有当前结果，更新图像
                if hasattr(self, 'current_result') and self.current_result:
                    img_idx = self.current_result.get('index', 0)
                else:
                    img_idx = 0
                self.update_displayed_image(img_idx)
        
    def update_ui_scale(self):
        """更新UI元素的缩放"""
        # 更新标题字体
        if hasattr(self, 'title_label'):
            self.title_label.configure(font=self.title_font)
            
        # 更新结果标签字体
        if hasattr(self, 'result_label'):
            self.result_label.configure(font=self.result_font)
            
        # 更新按钮字体和大小
        if hasattr(self, 'draw_btn'):
            self.draw_btn.configure(font=self.button_font)
            button_width = max(int(15 * self.scale_factor), 8)
            button_height = max(int(2 * self.scale_factor), 1)
            self.draw_btn.configure(width=button_width, height=button_height)
            
        # 更新小按钮字体和大小
        if hasattr(self, 'history_btn'):
            self.history_btn.configure(font=self.small_button_font)
            
        if hasattr(self, 'prizes_btn'):
            self.prizes_btn.configure(font=self.small_button_font)
            
        if hasattr(self, 'settings_btn'):
            self.settings_btn.configure(font=self.small_button_font)
            
        # 更新状态栏字体
        if hasattr(self, 'stats_label'):
            self.stats_label.configure(font=self.stats_font)
            
    def update_displayed_image(self, index=0):
        """更新显示的图像大小"""
        if 0 <= index < len(self.images):
            try:
                # 获取Label的当前尺寸
                label_width = self.image_label.winfo_width()
                label_height = self.image_label.winfo_height()
                
                # 计算合适的图像尺寸 - 使用Label尺寸的较小值的80%
                display_size = min(label_width, label_height) * 0.8
                scaled_size = int(max(display_size, 50))  # 确保最小尺寸
                
                # 使用PIL缩放图像
                img = self.original_images[index].resize((scaled_size, scaled_size), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                # 确保scaled_images列表足够长
                while len(self.scaled_images) <= index:
                    self.scaled_images.append(None)
                    
                # 更新缓存的缩放图像
                self.scaled_images[index] = photo
                
                # 更新Label中的图像
                self.image_label.configure(image=photo)
            except Exception as e:
                print(f"更新图像失败: {e}")
    
    def prepare_animation_images(self):
        """预先准备动画所需的所有图像"""
        try:
            # 获取Label的当前尺寸
            label_width = self.image_label.winfo_width()
            label_height = self.image_label.winfo_height()
            
            # 计算合适的图像尺寸
            display_size = min(label_width, label_height) * 0.8
            scaled_size = int(max(display_size, 50))
            
            # 为所有奖品图像创建统一尺寸的缩放版本
            self.scaled_images = []
            for i, original_img in enumerate(self.original_images):
                try:
                    img = original_img.resize((scaled_size, scaled_size), Image.LANCZOS)
                    photo = ImageTk.PhotoImage(img)
                    self.scaled_images.append(photo)
                except Exception as e:
                    print(f"预处理图像 {i} 失败: {e}")
                    # 使用默认图像
                    if i < len(self.images):
                        self.scaled_images.append(self.images[i])
                    else:
                        self.scaled_images.append(None)
        except Exception as e:
            print(f"预处理动画图像失败: {e}")
        
    def create_app_icon(self):
        """创建应用图标"""
        icon_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'resources')
        icon_path = os.path.join(icon_dir, 'app_icon.png')
        
        if not os.path.exists(icon_path):
            # 如果图标不存在，创建一个
            os.makedirs(os.path.dirname(icon_path), exist_ok=True)
            img = Image.new('RGBA', (64, 64), (255, 0, 0, 0))
            draw = ImageDraw.Draw(img)
            
            # 绘制一个简单的扭蛋机图标
            draw.ellipse((5, 5, 59, 59), fill="#FDD835", outline="#333333", width=2)
            draw.ellipse((20, 20, 44, 44), fill="#FFFFFF", outline="#333333", width=1)
            draw.text((25, 25), "G", fill="#333333")
            
            img.save(icon_path)
        
        return icon_path
        
    def create_default_image(self, prize, size=(100, 100)):
        """为奖品创建默认图像 - 圆形"""
        img_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'resources', 'images')
        os.makedirs(img_dir, exist_ok=True)
        
        # 从奖品名称中提取首字母
        first_char = prize['name'][0] if prize['name'] else "?"
        
        # 创建透明背景
        img = Image.new('RGBA', size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # 绘制圆形
        circle_color = "#FDD835"  # 黄色扭蛋
        draw.ellipse((0, 0, size[0]-1, size[1]-1), fill=circle_color, outline="#333333", width=2)
        
        # 添加文字
        font_size = int(size[0] / 3)
        draw.text((size[0]//2-font_size//2, size[1]//2-font_size//2), first_char, 
                 fill="#333333", stroke_width=1, stroke_fill="#FFFFFF")
        
        # 提取文件名
        filename = os.path.basename(prize['image'])
        img_path = os.path.join(img_dir, filename)
        
        # 保存图像
        img.save(img_path)
        
        return img
    
    def load_images(self):
        """加载奖品图片 - 处理为圆形"""
        self.images = []
        self.scaled_images = []
        self.original_images = []  # 存储原始图像对象
        
        for prize in self.prize_manager.get_all_prizes():
            try:
                img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), prize['image'])
                
                # 如果图片不存在，创建一个默认的
                if not os.path.exists(img_path):
                    img = self.create_default_image(prize)
                else:
                    # 加载图片并转换为圆形
                    original = Image.open(img_path).convert("RGBA")
                    
                    # 创建圆形蒙版
                    mask = Image.new('L', original.size, 0)
                    draw = ImageDraw.Draw(mask)
                    draw.ellipse((0, 0, original.size[0], original.size[1]), fill=255)
                    
                    # 应用蒙版创建圆形图像
                    img = Image.new('RGBA', original.size, (0, 0, 0, 0))
                    img.paste(original, (0, 0), mask)
                    
                    # 添加边框
                    draw = ImageDraw.Draw(img)
                    draw.ellipse((0, 0, original.size[0]-1, original.size[1]-1), 
                               outline="#333333", width=2)
                    
                # 保存原始图像
                self.original_images.append(img.copy())
                
                # 创建初始显示图像
                img = img.resize((100, 100), Image.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                self.images.append(photo)
                self.scaled_images.append(photo)  # 初始时缩放图像与原始图像相同
            except Exception as e:
                print(f"加载图片失败: {e}")
                img = self.create_default_image(prize)
                self.original_images.append(img.copy())
                photo = ImageTk.PhotoImage(img)
                self.images.append(photo)
                self.scaled_images.append(photo)
    
    def setup_ui(self):
        """设置UI界面"""
        # 顶部标题栏
        top_bar = tk.Frame(self.master, bg=COLOR_PALETTE['title_bar'])
        top_bar.pack(fill=tk.X)
        
        # 标题
        self.title_label = tk.Label(top_bar, text="🎰 自定义扭蛋机 🎰", font=self.title_font,
                                  bg=COLOR_PALETTE['title_bar'], fg=COLOR_PALETTE['dark_text'])
        self.title_label.pack(pady=10)
        
        # 创建主内容区域 - 左右分块
        content_frame = tk.Frame(self.master, bg=COLOR_PALETTE['background'])
        content_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 左侧 - 扭蛋图像显示区域
        left_frame = tk.Frame(content_frame, bg=COLOR_PALETTE['background'])
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # 奖品图像显示
        self.image_label = tk.Label(left_frame, bg=COLOR_PALETTE['background'],
                                  image=self.images[0] if self.images else None)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # 绑定Label大小变化事件
        self.image_label.bind("<Configure>", self.on_label_resize)
        
        # 抽奖结果显示
        self.result_label = tk.Label(left_frame, text="准备抽奖", 
                                   font=self.result_font,
                                   bg=COLOR_PALETTE['background'], 
                                   fg=COLOR_PALETTE['dark_text'])
        self.result_label.pack(pady=10)
        
        # 右侧 - 统计信息区域
        right_frame = tk.LabelFrame(content_frame, text="🎲 抽奖统计", 
                                  bg=COLOR_PALETTE['background'], 
                                  fg=COLOR_PALETTE['dark_text'],
                                  font=self.stats_font)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        
        # 统计信息文本区域
        self.stats_text = tk.Text(right_frame, width=30, height=20, 
                                bg=COLOR_PALETTE['light_bg'], 
                                fg=COLOR_PALETTE['dark_text'],
                                font=self.stats_font,
                                state=tk.DISABLED, wrap=tk.WORD)
        self.stats_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 底部按钮区域
        button_frame = tk.Frame(self.master, bg=COLOR_PALETTE['background'])
        button_frame.pack(fill=tk.X, pady=10)
        
        # 主抽奖按钮
        self.draw_btn = tk.Button(button_frame, text='🎯 开始抽奖',
                                font=self.button_font,
                                bg=COLOR_PALETTE['yellow_btn'],
                                fg=COLOR_PALETTE['dark_text'],
                                command=self.start_draw,
                                relief=tk.RAISED, bd=4,
                                width=15, height=2,
                                activebackground="#FFB300",
                                cursor="hand2")
        self.draw_btn.pack(side=tk.LEFT, padx=20)
        
        # 功能按钮组
        func_frame = tk.Frame(button_frame, bg=COLOR_PALETTE['background'])
        func_frame.pack(side=tk.RIGHT, padx=20)
        
        # 管理奖品按钮
        self.prizes_btn = tk.Button(func_frame, text='🎁 管理奖品',
                                  font=self.small_button_font,
                                  bg=COLOR_PALETTE['blue_btn'],
                                  fg=COLOR_PALETTE['light_text'],
                                  command=self.open_prize_manager,
                                  width=12, height=1)
        self.prizes_btn.pack(side=tk.LEFT, padx=5)
        
        # 设置按钮
        self.settings_btn = tk.Button(func_frame, text='⚙️ 设置',
                                    font=self.small_button_font,
                                    bg=COLOR_PALETTE['blue_btn'],
                                    fg=COLOR_PALETTE['light_text'],
                                    command=self.open_settings,
                                    width=8, height=1)
        self.settings_btn.pack(side=tk.LEFT, padx=5)
        
        # 历史记录按钮
        self.history_btn = tk.Button(func_frame, text='📊 历史',
                                   font=self.small_button_font,
                                   bg=COLOR_PALETTE['blue_btn'],
                                   fg=COLOR_PALETTE['light_text'],
                                   command=self.open_history,
                                   width=8, height=1)
        self.history_btn.pack(side=tk.LEFT, padx=5)
        
        # 状态栏
        status_frame = tk.Frame(self.master, bg="#F5F5F5", bd=1, relief=tk.SUNKEN)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.stats_label = tk.Label(status_frame, text="Welcome!",
                                  bd=0, anchor=tk.W, padx=10, pady=3,
                                  bg="#F5F5F5", fg="#333333",
                                  font=self.stats_font)
        self.stats_label.pack(side=tk.LEFT, fill=tk.X)
        
        # 添加版本信息
        self.version_label = tk.Label(status_frame, text="v3.0",
                                    bd=0, padx=10, pady=3,
                                    bg="#F5F5F5", fg="#999999",
                                    font=self.stats_font)
        self.version_label.pack(side=tk.RIGHT)
        
        # 初始调整一次UI
        self.master.update_idletasks()  # 确保所有组件已经绘制
        self.update_ui_scale()
    
    def on_label_resize(self, event):
        """当图像标签大小变化时调整图像"""
        # 如果正在播放动画，不要调整图像大小
        if hasattr(self, 'animating') and self.animating:
            return
            
        if hasattr(self, 'current_result') and self.current_result:
            img_idx = self.current_result.get('index', 0)
        else:
            img_idx = 0
        self.update_displayed_image(img_idx)
    
    def play_frames(self, frames, idx, result=None):
        """播放动画帧"""
        if idx < len(frames) and self.animating:
            # 显示当前帧
            frame_idx = frames[idx]
            if 0 <= frame_idx < len(self.scaled_images):
                self.image_label.configure(image=self.scaled_images[frame_idx])
            
            # 继续下一帧
            self.master.after(50, lambda: self.play_frames(frames, idx + 1, result))
        else:
            # 动画结束，显示最终结果
            if result:
                self.show_result(result)
            else:
                self.animating = False
                self.draw_btn.config(state=tk.NORMAL, relief=tk.RAISED)
                # 动画结束后，确保图像尺寸正确
                if hasattr(self, 'current_result') and self.current_result:
                    img_idx = self.current_result.get('index', 0)
                    self.update_displayed_image(img_idx)
    
    def show_result(self, result):
        """显示抽奖结果"""
        if result:
            try:
                # 添加时间戳
                result["timestamp"] = datetime.now().isoformat()
                self.history.add_record(result)
                self.update_statistics()
                
                # 保存当前结果
                self.current_result = result
                
                # 更新结果标签
                prize_name = result["prize"]["name"]
                prize_weight = result["prize"]["weight"]
                timestamp = datetime.fromisoformat(result["timestamp"])
                time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                
                # 计算概率
                total_weight = sum(self.prize_manager.get_weights())
                probability = f"{(prize_weight / total_weight * 100):.2f}%" if total_weight > 0 else "0%"
                
                # 设置结果标签
                self.result_label.config(
                    text=f"🎉 恭喜中奖: {prize_name} 🎉",
                    fg=COLOR_PALETTE['dark_text'],
                    font=self.result_font
                )
                
                # 添加闪烁效果
                self.flash_result_label(5)
                
                # 更新显示的图像
                self.update_displayed_image(result["index"])
                
            except Exception as e:
                print(f"显示抽奖结果失败: {e}")
                self.result_label.config(text="抽奖出错，请重试")
        
        self.animating = False
        self.draw_btn.config(state=tk.NORMAL, relief=tk.RAISED)
        
    def flash_result_label(self, count):
        """闪烁结果标签"""
        if count > 0 and self.current_result:
            # 交替颜色
            if count % 2 == 0:
                self.result_label.config(fg=COLOR_PALETTE['dark_text'])
            else:
                self.result_label.config(fg=COLOR_PALETTE['blue_btn'])
                
            # 继续闪烁
            self.master.after(300, lambda: self.flash_result_label(count - 1))
        elif self.current_result:
            # 恢复正常颜色
            self.result_label.config(fg=COLOR_PALETTE['dark_text'])
              
    def open_prize_manager(self):
        """打开奖品管理对话框"""
        dialog = PrizeDialog(self.master, self.prize_manager)
        self.master.wait_window(dialog.dialog)
        # 重新加载图片以反映可能的变化
        self.load_images()
        # 更新统计信息
        self.update_statistics()
        
    def open_history(self):
        """打开历史记录对话框"""
        dialog = HistoryDialog(self.master, self.history)
        
    def open_settings(self):
        """打开设置对话框"""
        messagebox.showinfo("设置", "设置功能开发中...")
        
    def update_statistics(self):
        """更新统计信息"""
        try:
            records = self.history.get_all_records()
            total_draws = len(records)
            
            # 清空文本区域
            self.stats_text.config(state=tk.NORMAL)
            self.stats_text.delete(1.0, tk.END)
            
            # 基本统计
            self.stats_text.insert(tk.END, f"总抽奖次数: {total_draws}\n")
            self.stats_text.insert(tk.END, f"当前奖品数量: {len(self.prize_manager.get_all_prizes())}\n")
            self.stats_text.insert(tk.END, f"最大奖品数量: {self.prize_manager.max_prizes}\n\n")
            
            # 各奖品统计
            self.stats_text.insert(tk.END, "各奖品统计:\n")
            self.stats_text.insert(tk.END, "-" * 30 + "\n")
            
            if total_draws > 0:
                prize_counts = {}
                for record in records:
                    prize_name = record["prize"]["name"]
                    prize_counts[prize_name] = prize_counts.get(prize_name, 0) + 1
                
                # 显示每个奖品的统计
                for prize in self.prize_manager.get_all_prizes():
                    name = prize["name"]
                    count = prize_counts.get(name, 0)
                    percentage = (count / total_draws * 100) if total_draws > 0 else 0
                    weight = prize["weight"]
                    total_weight = sum(self.prize_manager.get_weights())
                    expected_percentage = (weight / total_weight * 100) if total_weight > 0 else 0
                    
                    self.stats_text.insert(tk.END, f"{name}:\n")
                    self.stats_text.insert(tk.END, f"  抽取: {count}次 ({percentage:.1f}%)\n")
                    self.stats_text.insert(tk.END, f"  权重: {weight} ({expected_percentage:.1f}%)\n\n")
            else:
                for prize in self.prize_manager.get_all_prizes():
                    name = prize["name"]
                    weight = prize["weight"]
                    total_weight = sum(self.prize_manager.get_weights())
                    expected_percentage = (weight / total_weight * 100) if total_weight > 0 else 0
                    
                    self.stats_text.insert(tk.END, f"{name}:\n")
                    self.stats_text.insert(tk.END, f"  抽取: 0次 (0.0%)\n")
                    self.stats_text.insert(tk.END, f"  权重: {weight} ({expected_percentage:.1f}%)\n\n")
            
            self.stats_text.config(state=tk.DISABLED)
            
            # 更新状态栏
            if total_draws > 0:
                last_record = records[-1]
                last_prize = last_record["prize"]["name"]
                self.stats_label.config(text=f"上次抽中: {last_prize}")
            else:
                self.stats_label.config(text="还没有抽奖记录")
                
        except Exception as e:
            print(f"更新统计信息失败: {e}")
    
    def start_draw(self):
        """开始抽奖"""
        if self.animating:
            return
            
        if not self.prize_manager.get_all_prizes():
            messagebox.showwarning("警告", "请先添加奖品！")
            return
            
        self.animating = True
        self.draw_btn.config(state=tk.DISABLED, relief=tk.SUNKEN)
        self.result_label.config(text="抽奖中...")
        
        # 生成动画帧
        result = self.gacha_engine.draw()
        if result:
            # 预先确保所有动画帧的图像都已正确缩放
            self.prepare_animation_images()
            frames = self.gacha_engine.generate_animation_frames(result["index"])
            self.play_frames(frames, 0, result)
        else:
            self.animating = False
            self.draw_btn.config(state=tk.NORMAL, relief=tk.RAISED)
            messagebox.showerror("错误", "抽奖失败，请检查奖品配置！") 