import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import json
import shutil
from PIL import Image, ImageTk

from ..utils.config import COLOR_PALETTE
from ..core.prize_manager import PrizeManager

class PrizeDialog:
    def __init__(self, parent, prize_manager):
        self.parent = parent
        self.prize_manager = prize_manager
        self.dialog = None
        self.prizes = prize_manager.get_all_prizes()
        self.current_index = 0
        self.original_prizes = None  # 用于存储原始奖品列表
        
        # 创建对话框
        self.create_dialog()
        
    def create_dialog(self):
        """创建奖品管理对话框"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("奖品管理")
        self.dialog.geometry("700x500")
        self.dialog.resizable(True, True)
        self.dialog.configure(bg=COLOR_PALETTE['background'])
        
        # 使对话框模态
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.parent.winfo_width() // 2) - (width // 2) + self.parent.winfo_x()
        y = (self.parent.winfo_height() // 2) - (height // 2) + self.parent.winfo_y()
        self.dialog.geometry(f"+{x}+{y}")
        
        # 保存原始奖品列表，以便在取消时恢复
        self.original_prizes = [prize.copy() for prize in self.prizes]
        
        # 创建UI
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI界面"""
        # 主框架
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(title_frame, text="奖品管理", font=("Arial", 12, "bold")).pack(side=tk.LEFT)
        ttk.Label(title_frame, text="管理您的扭蛋机奖品库", foreground="#666666").pack(side=tk.LEFT, padx=(10, 0))
        
        # 奖品列表
        list_frame = ttk.LabelFrame(main_frame, text="奖品列表", padding="10")
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 创建表格
        columns = ('序号', '奖品名称', '图片路径', '权重')
        self.tree = ttk.Treeview(list_frame, columns=columns, show='headings', selectmode='browse')
        
        # 设置列标题
        for col in columns:
            self.tree.heading(col, text=col)
            
        self.tree.column('序号', width=50)
        self.tree.column('奖品名称', width=150)
        self.tree.column('图片路径', width=200)
        self.tree.column('权重', width=80)
        
        # 添加滚动条
        scrollbar_y = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(list_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        
        # 布局
        self.tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        # 配置网格
        list_frame.grid_columnconfigure(0, weight=1)
        list_frame.grid_rowconfigure(0, weight=1)
        
        # 双击编辑
        self.tree.bind("<Double-1>", lambda e: self.edit_prize())
        
        # 按钮框架
        button_frame = ttk.Frame(main_frame, padding="10")
        button_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 添加按钮
        ttk.Button(button_frame, text="添加奖品", command=self.add_prize, 
                  style="Accent.TButton").pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="编辑奖品", command=self.edit_prize).pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="删除奖品", command=self.delete_prize).pack(fill=tk.X, pady=2)
        ttk.Separator(button_frame, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=10)
        ttk.Button(button_frame, text="保存更改", command=self.save_changes, 
                  style="Accent.TButton").pack(fill=tk.X, pady=2)
        ttk.Button(button_frame, text="取消", command=self.cancel).pack(fill=tk.X, pady=(20, 2))
        
        # 状态栏
        status_frame = ttk.Frame(self.dialog)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(status_frame, text="就绪", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # 刷新表格
        self.refresh_table()
        
    def refresh_table(self):
        """刷新奖品列表"""
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        for i, prize in enumerate(self.prizes):
            values = (
                i + 1,
                prize['name'],
                os.path.basename(prize['image']),
                prize['weight']
            )
            self.tree.insert('', tk.END, values=values)
            
        # 更新状态栏
        total = len(self.prizes)
        self.status_label.config(text=f"共 {total} 个奖品")
            
    def add_prize(self):
        """添加奖品"""
        self.status_label.config(text="添加新奖品...")
        dialog = PrizeEditDialog(self.dialog, "添加奖品")
        if dialog.result:
            new_prize = {
                'name': dialog.result['name'],
                'weight': dialog.result['weight'],
                'image': dialog.result['image']
            }
            self.prizes.append(new_prize)
            self.refresh_table()
            self.status_label.config(text=f"已添加奖品: {dialog.result['name']}")
                
    def edit_prize(self):
        """编辑奖品"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个奖品")
            return
            
        self.status_label.config(text="编辑奖品...")
        index = self.tree.index(selection[0])
        prize = self.prizes[index]
        if prize:
            dialog = PrizeEditDialog(self.dialog, "编辑奖品", prize)
            if dialog.result:
                self.prizes[index] = {
                    'name': dialog.result['name'],
                    'weight': dialog.result['weight'],
                    'image': dialog.result['image']
                }
                self.refresh_table()
                self.status_label.config(text=f"已更新奖品: {dialog.result['name']}")
                
    def delete_prize(self):
        """删除奖品"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("警告", "请先选择一个奖品")
            return
            
        index = self.tree.index(selection[0])
        prize = self.prizes[index]
        if prize and messagebox.askyesno("确认", f"确定要删除奖品 '{prize['name']}' 吗？"):
            del self.prizes[index]
            self.refresh_table()
            self.status_label.config(text=f"已删除奖品: {prize['name']}")
            
    def save_changes(self):
        """保存更改"""
        self.status_label.config(text="正在保存...")
        # 更新奖品管理器
        self.prize_manager.set_prizes(self.prizes)
        # 保存到配置
        self.prize_manager.save_prizes()
        messagebox.showinfo("成功", "奖品配置已保存！")
        self.dialog.destroy()
        
    def cancel(self):
        """取消所有更改"""
        # 恢复原始奖品列表
        self.prizes = self.original_prizes
        # 关闭对话框
        self.dialog.destroy()

class PrizeEditDialog:
    def __init__(self, parent, title, prize=None):
        self.parent = parent
        self.title = title
        self.prize = prize
        self.result = None
        self.image_path = prize['image'] if prize else None
        self.preview_image = None
        
        # 创建对话框
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(title)
        self.dialog.geometry("500x400")
        self.dialog.resizable(False, False)
        self.dialog.configure(bg=COLOR_PALETTE['background'])
        
        # 使对话框模态
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # 居中显示
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (parent.winfo_width() // 2) - (width // 2) + parent.winfo_x()
        y = (parent.winfo_height() // 2) - (height // 2) + parent.winfo_y()
        self.dialog.geometry(f"+{x}+{y}")
        
        self.setup_ui()
        
        # 等待对话框关闭
        self.dialog.wait_window()
        
    def setup_ui(self):
        """设置UI界面"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_text = "编辑奖品" if self.prize else "添加新奖品"
        ttk.Label(main_frame, text=title_text, font=("Arial", 12, "bold")).grid(row=0, column=0, columnspan=3, sticky=tk.W, pady=(0, 15))
        
        # 左侧表单
        form_frame = ttk.Frame(main_frame)
        form_frame.grid(row=1, column=0, sticky='nw', padx=(0, 20))
        
        # 名称
        ttk.Label(form_frame, text="奖品名称:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar(value=self.prize['name'] if self.prize else "")
        name_entry = ttk.Entry(form_frame, textvariable=self.name_var, width=30)
        name_entry.grid(row=0, column=1, sticky=tk.EW, pady=5)
        name_entry.focus_set()  # 设置焦点
        
        # 权重
        ttk.Label(form_frame, text="抽取权重:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.weight_var = tk.StringVar(value=str(self.prize['weight']) if self.prize else "10")
        ttk.Entry(form_frame, textvariable=self.weight_var, width=10).grid(row=1, column=1, sticky=tk.W, pady=5)
        ttk.Label(form_frame, text="(数值越大概率越高)").grid(row=1, column=2, sticky=tk.W, padx=5, pady=5)
        
        # 图片
        ttk.Label(form_frame, text="奖品图片:").grid(row=2, column=0, sticky=tk.W, pady=5)
        img_frame = ttk.Frame(form_frame)
        img_frame.grid(row=2, column=1, columnspan=2, sticky=tk.EW, pady=5)
        
        # 使用网格布局来确保按钮始终可见
        img_frame.columnconfigure(0, weight=1)  # 让标签列可以扩展
        img_frame.columnconfigure(1, weight=0)  # 让按钮列保持固定
        
        # 图片路径标签，设置最大宽度并截断长文件名
        filename = os.path.basename(self.image_path) if self.image_path else "未选择"
        if len(filename) > 25:  # 如果文件名太长，截断并添加省略号
            filename = filename[:22] + "..."
        self.image_label = ttk.Label(img_frame, text=filename, width=25)
        self.image_label.grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        
        # 浏览按钮，固定宽度
        ttk.Button(img_frame, text="浏览...", command=self.browse_image, width=8).grid(row=0, column=1, sticky=tk.E)
        
        # 右侧预览
        preview_frame = ttk.LabelFrame(main_frame, text="预览", padding=10)
        preview_frame.grid(row=1, column=1, sticky='n', padx=(0, 10))
        
        self.preview_canvas = tk.Canvas(preview_frame, width=150, height=150, bg="#f0f0f0", highlightthickness=1, highlightbackground="#cccccc")
        self.preview_canvas.pack()
        
        self.update_preview()
        
        # 底部按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=(20, 0))
        
        ttk.Button(button_frame, text="保存", command=self.save, width=10).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="取消", command=self.cancel, width=10).pack(side=tk.LEFT)
        
        # 绑定事件
        self.name_var.trace_add("write", lambda *args: self.update_preview())
        self.weight_var.trace_add("write", lambda *args: self.update_preview())
        
        # 配置网格
        main_frame.columnconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=0)
        form_frame.columnconfigure(1, weight=1)  # 让表单的第二列可以扩展
    
    def browse_image(self):
        """浏览图片"""
        path = filedialog.askopenfilename(
            title="选择奖品图片",
            filetypes=[("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp")]
        )
        if path:
            # 获取资源目录
            resources_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'resources', 'images')
            os.makedirs(resources_dir, exist_ok=True)
            
            # 生成目标文件名
            base_name = os.path.basename(path)
            target_path = os.path.join(resources_dir, base_name)
            
            # 如果不是在资源目录中，复制文件
            if os.path.abspath(path) != os.path.abspath(target_path):
                try:
                    shutil.copy2(path, target_path)
                except Exception as e:
                    messagebox.showerror("错误", f"复制图片失败: {e}")
                    return
            
            # 更新路径为相对路径
            rel_path = os.path.join('resources', 'images', base_name)
            self.image_path = rel_path
            
            # 截断长文件名
            display_name = base_name
            if len(display_name) > 25:
                display_name = display_name[:22] + "..."
            self.image_label.config(text=display_name)
            self.update_preview()
            
    def update_preview(self):
        """更新预览"""
        # 清除画布
        self.preview_canvas.delete("all")
        
        # 绘制背景
        self.preview_canvas.create_rectangle(0, 0, 150, 150, fill="#f0f0f0", outline="")
        
        # 获取名称
        name = self.name_var.get().strip() or "未命名奖品"
        
        try:
            # 尝试加载图片
            if self.image_path:
                img_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), self.image_path)
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    img = img.resize((100, 100), Image.LANCZOS)
                    self.preview_image = ImageTk.PhotoImage(img)
                    self.preview_canvas.create_image(75, 50, image=self.preview_image)
                else:
                    # 绘制占位图像
                    self.preview_canvas.create_rectangle(25, 10, 125, 90, fill="#FDD835", outline="#333333")
                    self.preview_canvas.create_text(75, 50, text=name[0], fill="#333333", font=("Arial", 24, "bold"))
            else:
                # 绘制占位图像
                self.preview_canvas.create_rectangle(25, 10, 125, 90, fill="#FDD835", outline="#333333")
                self.preview_canvas.create_text(75, 50, text=name[0], fill="#333333", font=("Arial", 24, "bold"))
                
            # 绘制名称
            self.preview_canvas.create_text(75, 110, text=name, fill="#333333", font=("Arial", 10, "bold"))
            
            # 绘制权重
            try:
                weight = int(self.weight_var.get())
                weight_text = f"权重: {weight}"
            except:
                weight_text = "权重: 无效"
                
            self.preview_canvas.create_text(75, 130, text=weight_text, fill="#666666", font=("Arial", 9))
            
        except Exception as e:
            print(f"预览更新失败: {e}")
            self.preview_canvas.create_text(75, 75, text="预览失败", fill="#FF0000")
            
    def save(self):
        """保存"""
        try:
            weight = int(self.weight_var.get())
            if weight <= 0:
                raise ValueError("权重必须大于0")
        except ValueError as e:
            messagebox.showerror("错误", "权重必须是正整数")
            return
            
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("错误", "名称不能为空")
            return
            
        if not self.image_path:
            messagebox.showerror("错误", "请选择图片")
            return
            
        self.result = {
            'name': name,
            'image': self.image_path,
            'weight': weight
        }
        self.dialog.destroy()
    
    def cancel(self):
        """取消"""
        self.dialog.destroy() 