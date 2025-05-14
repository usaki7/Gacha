import json
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')

def load_config(path=CONFIG_PATH):
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    else:
        default = {
            'prizes': [
                {'name': '一等奖', 'image': 'images/prize1.png', 'weight': 1},
                {'name': '二等奖', 'image': 'images/prize2.png', 'weight': 3},
                {'name': '三等奖', 'image': 'images/prize3.png', 'weight': 6}
            ],
            'animation_duration_ms': 1500,
            'frame_interval_ms': 100
        }
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(default, f, ensure_ascii=False, indent=4)
        return default

def choose_prize_index(weights):
    total = sum(weights)
    r = random.uniform(0, total)
    upto = 0
    for i, w in enumerate(weights):
        if upto + w >= r:
            return i
        upto += w
    return len(weights) - 1

class GachaApp:
    def __init__(self, master):
        self.master = master
        self.master.title('扭蛋机')
        self.config = load_config()
        self.prizes = self.config['prizes']
        self.images = []
        for prize in self.prizes:
            try:
                img = Image.open(os.path.join(os.path.dirname(__file__), prize['image']))
                img = img.resize((150,150), Image.ANTIALIAS)
            except Exception:
                img = Image.new('RGBA', (150,150), (200,200,200))
            self.images.append(ImageTk.PhotoImage(img))

        frame_left = tk.Frame(master)
        frame_left.pack(side=tk.LEFT, padx=20, pady=20)
        frame_right = tk.Frame(master)
        frame_right.pack(side=tk.RIGHT, padx=20, pady=20)

        self.canvas = tk.Canvas(frame_left, width=200, height=200)
        self.canvas.pack()
        self.image_id = self.canvas.create_image(100, 100, image=self.images[0])

        self.draw_btn = tk.Button(frame_right, text='抽 奖', font=('Arial',16), width=10, command=self.start_draw)
        self.draw_btn.pack(pady=5)
        self.settings_btn = tk.Button(frame_right, text='设置权重', font=('Arial',12), command=self.open_settings)
        self.settings_btn.pack(pady=5)

        self.animating = False

    def start_draw(self):
        if self.animating:
            return
        self.animating = True
        self.draw_btn.config(state=tk.DISABLED)
        weights = [p['weight'] for p in self.prizes]
        final_idx = choose_prize_index(weights)
        frames = [random.randrange(len(self.images)) 
                  for _ in range(int(self.config['animation_duration_ms']/self.config['frame_interval_ms']))]
        frames.append(final_idx)
        self.play_frames(frames, 0)

    def play_frames(self, frames, idx):
        if idx < len(frames):
            i = frames[idx]
            self.canvas.itemconfig(self.image_id, image=self.images[i])
            self.master.after(self.config['frame_interval_ms'], lambda: self.play_frames(frames, idx+1))
        else:
            prize = self.prizes[frames[-1]]
            messagebox.showinfo('恭喜', f'您抽中了：{prize["name"]}')
            self.animating = False
            self.draw_btn.config(state=tk.NORMAL)

    def open_settings(self):
        settings_win = tk.Toplevel(self.master)
        settings_win.title('设置权重')
        entries = []
        for i, prize in enumerate(self.prizes):
            tk.Label(settings_win, text=prize['name'], width=10).grid(row=i, column=0)
            var = tk.StringVar(value=str(prize['weight']))
            entry = tk.Entry(settings_win, textvariable=var, width=5)
            entry.grid(row=i, column=1)
            entries.append((i, var))
        def save_weights():
            try:
                for i, var in entries:
                    w = int(var.get())
                    if w < 0: raise ValueError
                    self.config['prizes'][i]['weight'] = w
                with open(CONFIG_PATH, 'w', encoding='utf-8') as f:
                    json.dump(self.config, f, ensure_ascii=False, indent=4)
                messagebox.showinfo('保存', '权重已保存')
                settings_win.destroy()
            except:
                messagebox.showerror('错误', '请输入非负整数')
        tk.Button(settings_win, text='保存', command=save_weights).grid(row=len(entries), column=0, columnspan=2)

def main():
    root = tk.Tk()
    GachaApp(root)
    root.mainloop()

if __name__ == '__main__':
    main()
