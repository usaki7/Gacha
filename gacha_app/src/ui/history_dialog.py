import tkinter as tk
from tkinter import ttk, messagebox
from ..utils.config import COLOR_PALETTE
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

class HistoryDialog(tk.Toplevel):
    def __init__(self, parent, history):
        super().__init__(parent)
        self.history = history
        
        self.title("历史记录")
        self.geometry("800x600")
        self.resizable(True, True)
        
        # 设置窗口图标
        try:
            self.iconbitmap(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'resources', 'app_icon.ico'))
        except:
            pass
        
        # 使对话框模态
        self.transient(parent)
        self.grab_set()
        
        # 配置样式
        self.style = ttk.Style()
        self.style.configure("TButton", font=("Arial", 10))
        self.style.configure("TLabel", font=("Arial", 10))
        self.style.configure("Heading.TLabel", font=("Arial", 12, "bold"))
        
        self.setup_ui()
        
    def setup_ui(self):
        """设置UI界面"""
        # 主框架
        main_frame = ttk.Frame(self, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(title_frame, text="抽奖历史记录", style="Heading.TLabel").pack(side=tk.LEFT)
        ttk.Label(title_frame, text="查看您的抽奖历史和统计数据", foreground="#666666").pack(side=tk.LEFT, padx=(10, 0))
        
        # 创建分页界面
        notebook = ttk.Notebook(main_frame)
        notebook.pack(fill=tk.BOTH, expand=True)
        
        # 抽奖记录页面
        records_frame = ttk.Frame(notebook, padding="10")
        notebook.add(records_frame, text="抽奖记录")
        
        # 统计信息页面
        stats_frame = ttk.Frame(notebook, padding="10")
        notebook.add(stats_frame, text="统计信息")
        
        # 图表页面
        chart_frame = ttk.Frame(notebook, padding="10")
        notebook.add(chart_frame, text="图表分析")
        
        # 设置抽奖记录表格
        self.setup_records_table(records_frame)
        
        # 设置统计信息表格
        self.setup_stats_table(stats_frame)
        
        # 设置图表
        self.setup_charts(chart_frame)
        
        # 底部按钮
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(button_frame, text="导出数据", 
                  command=self.export_data).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="清空记录",
                  command=self.clear_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="关闭",
                  command=self.destroy).pack(side=tk.RIGHT)
        
        # 状态栏
        status_frame = ttk.Frame(self)
        status_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_label = ttk.Label(status_frame, text="就绪", anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        # 加载数据
        self.load_data()
        
    def setup_records_table(self, parent):
        """设置抽奖记录表格"""
        # 创建表格
        columns = ('时间', '奖品', '权重')
        self.records_tree = ttk.Treeview(parent, columns=columns, show='headings', selectmode='browse')
        
        # 设置列标题
        for col in columns:
            self.records_tree.heading(col, text=col)
        
        self.records_tree.column('时间', width=200)
        self.records_tree.column('奖品', width=150)
        self.records_tree.column('权重', width=100)
        
        # 添加滚动条
        scrollbar_y = ttk.Scrollbar(parent, orient=tk.VERTICAL,
                                command=self.records_tree.yview)
        scrollbar_x = ttk.Scrollbar(parent, orient=tk.HORIZONTAL,
                                command=self.records_tree.xview)
        self.records_tree.configure(yscrollcommand=scrollbar_y.set,
                                  xscrollcommand=scrollbar_x.set)
        
        # 布局
        self.records_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        # 配置网格
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
        # 添加右键菜单
        self.record_menu = tk.Menu(self, tearoff=0)
        self.record_menu.add_command(label="查看详情", command=self.show_record_details)
        self.record_menu.add_separator()
        self.record_menu.add_command(label="删除记录", command=self.delete_record)
        
        self.records_tree.bind("<Button-3>", self.show_record_menu)
        self.records_tree.bind("<Double-1>", lambda e: self.show_record_details())
        
    def setup_stats_table(self, parent):
        """设置统计信息表格"""
        # 创建表格
        columns = ('奖品', '次数', '概率', '颜色')
        self.stats_tree = ttk.Treeview(parent, columns=columns, show='headings', selectmode='browse')
        
        # 设置列标题
        for col in columns:
            self.stats_tree.heading(col, text=col)
            
        self.stats_tree.column('奖品', width=150)
        self.stats_tree.column('次数', width=80)
        self.stats_tree.column('概率', width=80)
        self.stats_tree.column('颜色', width=80)
        
        # 添加滚动条
        scrollbar_y = ttk.Scrollbar(parent, orient=tk.VERTICAL,
                                command=self.stats_tree.yview)
        scrollbar_x = ttk.Scrollbar(parent, orient=tk.HORIZONTAL,
                                command=self.stats_tree.xview)
        self.stats_tree.configure(yscrollcommand=scrollbar_y.set,
                               xscrollcommand=scrollbar_x.set)
        
        # 布局
        self.stats_tree.grid(row=0, column=0, sticky='nsew')
        scrollbar_y.grid(row=0, column=1, sticky='ns')
        scrollbar_x.grid(row=1, column=0, sticky='ew')
        
        # 配置网格
        parent.grid_columnconfigure(0, weight=1)
        parent.grid_rowconfigure(0, weight=1)
        
    def setup_charts(self, parent):
        """设置图表"""
        # 创建标签页
        chart_notebook = ttk.Notebook(parent)
        chart_notebook.pack(fill=tk.BOTH, expand=True)
        
        # 饼图页面
        pie_frame = ttk.Frame(chart_notebook)
        chart_notebook.add(pie_frame, text="饼图")
        
        # 柱状图页面
        bar_frame = ttk.Frame(chart_notebook)
        chart_notebook.add(bar_frame, text="柱状图")
        
        # 时间趋势页面
        trend_frame = ttk.Frame(chart_notebook)
        chart_notebook.add(trend_frame, text="时间趋势")
        
        # 创建图表
        self.pie_canvas_widget = None
        self.bar_canvas_widget = None
        self.trend_canvas_widget = None
        
        # 将创建图表的逻辑放在load_data中，以便在数据加载后创建
        
    def load_data(self):
        """加载数据"""
        self.status_label.config(text="正在加载数据...")
        
        # 加载历史记录
        self.load_records()
        
        # 加载统计信息
        self.load_statistics()
        
        # 加载图表
        try:
            self.load_charts()
        except Exception as e:
            print(f"加载图表失败: {e}")
        
        # 更新状态栏
        history_data = self.history.load()
        total_draws = len(history_data.get('draws', []))
        self.status_label.config(text=f"共 {total_draws} 次抽奖记录")
        
    def load_records(self):
        """加载抽奖记录"""
        # 清空表格
        for item in self.records_tree.get_children():
            self.records_tree.delete(item)
            
        # 加载数据
        history_data = self.history.load()
        for i, draw in enumerate(reversed(history_data.get('draws', []))):
            try:
                # 转换时间格式
                timestamp = datetime.fromisoformat(draw['timestamp'])
                time_str = timestamp.strftime("%Y-%m-%d %H:%M:%S")
                
                prize_name = draw['prize']['name']
                prize_weight = draw['prize']['weight']
                
                values = (
                    time_str,
                    prize_name,
                    prize_weight
                )
                
                # 交替行颜色
                tags = ('even',) if i % 2 == 0 else ('odd',)
                
                self.records_tree.insert('', tk.END, values=values, tags=tags)
            except Exception as e:
                print(f"加载记录失败: {e}")
                
        # 设置交替行颜色
        self.records_tree.tag_configure('odd', background='#f0f0f0')
        self.records_tree.tag_configure('even', background='#ffffff')
                
    def load_statistics(self):
        """加载统计信息"""
        # 清空表格
        for item in self.stats_tree.get_children():
            self.stats_tree.delete(item)
            
        # 加载数据
        history_data = self.history.load()
        stats = history_data.get('statistics', {})
        total_draws = len(history_data.get('draws', []))
        
        if total_draws > 0:
            for i, (prize_name, data) in enumerate(sorted(stats.items(), 
                                                        key=lambda x: x[1]['count'], 
                                                        reverse=True)):
                count = data['count']
                color = data['color']
                
                probability = f"{(count / total_draws * 100):.2f}%"
                
                values = (prize_name, count, probability, color)
                
                # 交替行颜色
                tags = ('even',) if i % 2 == 0 else ('odd',)
                
                item_id = self.stats_tree.insert('', tk.END, values=values, tags=tags)
                
                # 设置颜色指示器
                self.stats_tree.tag_configure(f'color_{item_id}', background=color)
                
            # 设置交替行颜色
            self.stats_tree.tag_configure('odd', background='#f0f0f0')
            self.stats_tree.tag_configure('even', background='#ffffff')
                
    def load_charts(self):
        """加载图表"""
        history_data = self.history.load()
        stats = history_data.get('statistics', {})
        total_draws = len(history_data.get('draws', []))
        
        if total_draws > 0:
            # 饼图
            self.create_pie_chart(stats, total_draws)
            
            # 柱状图
            self.create_bar_chart(stats, total_draws)
            
            # 时间趋势图
            self.create_trend_chart(history_data.get('draws', []))
            
    def create_pie_chart(self, stats, total_draws):
        """创建饼图"""
        try:
            # 获取饼图页面
            notebook = self.winfo_children()[0].winfo_children()[3]
            if not notebook.winfo_children():
                print("图表标签页未创建")
                return
                
            pie_frame = notebook.winfo_children()[0]
            
            # 清空现有内容
            for widget in pie_frame.winfo_children():
                widget.destroy()
                
            # 准备数据
            labels = []
            sizes = []
            colors = []
            
            for prize_name, data in sorted(stats.items(), 
                                          key=lambda x: x[1]['count'], 
                                          reverse=True):
                labels.append(prize_name)
                sizes.append(data['count'])
                colors.append(data['color'])
                
            # 创建图表
            fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
            ax.axis('equal')  # 确保饼图是圆的
            ax.set_title('奖品分布')
            
            # 添加到界面
            canvas = FigureCanvasTkAgg(fig, master=pie_frame)
            self.pie_canvas_widget = canvas.get_tk_widget()
            self.pie_canvas_widget.pack(fill=tk.BOTH, expand=True)
            canvas.draw()
        except Exception as e:
            print(f"创建饼图失败: {e}")
        
    def create_bar_chart(self, stats, total_draws):
        """创建柱状图"""
        try:
            # 获取柱状图页面
            notebook = self.winfo_children()[0].winfo_children()[3]
            if len(notebook.winfo_children()) < 2:
                print("柱状图标签页未创建")
                return
                
            bar_frame = notebook.winfo_children()[1]
            
            # 清空现有内容
            for widget in bar_frame.winfo_children():
                widget.destroy()
                
            # 准备数据
            names = []
            counts = []
            colors = []
            
            for prize_name, data in sorted(stats.items(), 
                                          key=lambda x: x[1]['count'], 
                                          reverse=True):
                names.append(prize_name)
                counts.append(data['count'])
                colors.append(data['color'])
                
            # 创建图表
            fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
            bars = ax.bar(names, counts, color=colors)
            
            # 添加数值标签
            for bar in bars:
                height = bar.get_height()
                ax.annotate(f'{height}',
                          xy=(bar.get_x() + bar.get_width() / 2, height),
                          xytext=(0, 3),  # 3点垂直偏移
                          textcoords="offset points",
                          ha='center', va='bottom')
                          
            ax.set_title('奖品获取次数')
            ax.set_ylabel('次数')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # 添加到界面
            canvas = FigureCanvasTkAgg(fig, master=bar_frame)
            self.bar_canvas_widget = canvas.get_tk_widget()
            self.bar_canvas_widget.pack(fill=tk.BOTH, expand=True)
            canvas.draw()
        except Exception as e:
            print(f"创建柱状图失败: {e}")
        
    def create_trend_chart(self, draws):
        """创建时间趋势图"""
        if not draws:
            return
            
        try:
            # 获取趋势图页面
            notebook = self.winfo_children()[0].winfo_children()[3]
            if len(notebook.winfo_children()) < 3:
                print("趋势图标签页未创建")
                return
                
            trend_frame = notebook.winfo_children()[2]
            
            # 清空现有内容
            for widget in trend_frame.winfo_children():
                widget.destroy()
                
            # 准备数据
            dates = []
            prizes = {}
            
            for draw in draws:
                try:
                    timestamp = datetime.fromisoformat(draw['timestamp'])
                    date_str = timestamp.strftime("%Y-%m-%d")
                    
                    prize_name = draw['prize']['name']
                    prize_color = draw['prize']['color']
                    
                    dates.append(date_str)
                    
                    if prize_name not in prizes:
                        prizes[prize_name] = {
                            'dates': [],
                            'counts': [],
                            'color': prize_color
                        }
                        
                    prizes[prize_name]['dates'].append(date_str)
                    
                except Exception as e:
                    print(f"处理抽奖记录失败: {e}")
                    
            # 计算每个日期的累计次数
            for prize_name, data in prizes.items():
                date_counts = {}
                for date in data['dates']:
                    if date not in date_counts:
                        date_counts[date] = 0
                    date_counts[date] += 1
                    
                # 排序并转换为列表
                sorted_dates = sorted(date_counts.keys())
                data['sorted_dates'] = sorted_dates
                data['counts'] = [date_counts[date] for date in sorted_dates]
                
            # 创建图表
            fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
            
            for prize_name, data in prizes.items():
                if data['sorted_dates'] and data['counts']:
                    ax.plot(data['sorted_dates'], data['counts'], marker='o', 
                          label=prize_name, color=data['color'])
                    
            ax.set_title('抽奖时间趋势')
            ax.set_ylabel('次数')
            ax.set_xlabel('日期')
            plt.xticks(rotation=45, ha='right')
            plt.legend()
            plt.tight_layout()
            
            # 添加到界面
            canvas = FigureCanvasTkAgg(fig, master=trend_frame)
            self.trend_canvas_widget = canvas.get_tk_widget()
            self.trend_canvas_widget.pack(fill=tk.BOTH, expand=True)
            canvas.draw()
        except Exception as e:
            print(f"创建趋势图失败: {e}")
        
    def show_record_menu(self, event):
        """显示记录右键菜单"""
        item = self.records_tree.identify_row(event.y)
        if item:
            self.records_tree.selection_set(item)
            self.record_menu.post(event.x_root, event.y_root)
            
    def show_record_details(self):
        """显示记录详情"""
        selection = self.records_tree.selection()
        if not selection:
            return
            
        # 获取选中的记录
        values = self.records_tree.item(selection[0], 'values')
        if values:
            # 创建详情对话框
            details = tk.Toplevel(self)
            details.title("记录详情")
            details.geometry("300x200")
            details.resizable(False, False)
            details.transient(self)
            details.grab_set()
            
            # 设置内容
            frame = ttk.Frame(details, padding=20)
            frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(frame, text="抽奖时间:", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky=tk.W, pady=5)
            ttk.Label(frame, text=values[0]).grid(row=0, column=1, sticky=tk.W, pady=5)
            
            ttk.Label(frame, text="奖品名称:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky=tk.W, pady=5)
            ttk.Label(frame, text=values[1]).grid(row=1, column=1, sticky=tk.W, pady=5)
            
            ttk.Label(frame, text="奖品权重:", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky=tk.W, pady=5)
            ttk.Label(frame, text=values[2]).grid(row=2, column=1, sticky=tk.W, pady=5)
            
            ttk.Button(frame, text="关闭", command=details.destroy).grid(row=3, column=0, columnspan=2, pady=20)
            
    def delete_record(self):
        """删除记录"""
        selection = self.records_tree.selection()
        if not selection:
            return
            
        if messagebox.askyesno("确认", "确定要删除此记录吗？"):
            # 获取选中的记录
            values = self.records_tree.item(selection[0], 'values')
            if values:
                # 在这里实现删除记录的逻辑
                # 注意：当前的History类没有提供删除单条记录的方法，需要扩展
                messagebox.showinfo("提示", "此功能尚未实现")
                
    def export_data(self):
        """导出数据"""
        # 在这里实现导出数据的逻辑
        messagebox.showinfo("提示", "此功能尚未实现")
        
    def clear_history(self):
        """清空历史记录"""
        if messagebox.askyesno("确认", "确定要清空所有历史记录吗？这个操作无法撤销！"):
            if self.history.clear():
                self.load_data()
                messagebox.showinfo("成功", "历史记录已清空！") 