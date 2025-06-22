import os
import json
import random
from datetime import datetime

class PrizeManager:
    def __init__(self, config_path):
        self.config_path = config_path
        self.prizes = []
        self.max_prizes = 100  # 最大奖品数量
        self.load_prizes()
    
    def load_prizes(self):
        """加载奖品配置"""
        try:
            if os.path.exists(self.config_path):
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    if 'prizes' in config:
                        self.prizes = config['prizes']
                        
                # 确保每个奖品都有必要的属性
                for prize in self.prizes:
                    if 'name' not in prize:
                        prize['name'] = "未命名奖品"
                    if 'weight' not in prize:
                        prize['weight'] = 1
                    if 'image' not in prize:
                        prize['image'] = "resources/images/prize1.png"
            
            # 如果没有奖品，添加默认奖品
            if not self.prizes:
                self.add_default_prizes()
                
        except Exception as e:
            print(f"加载奖品配置失败: {e}")
            self.add_default_prizes()
    
    def add_default_prizes(self):
        """添加默认奖品"""
        self.prizes = [
            {
                "name": "一等奖",
                "weight": 10,
                "image": "resources/images/prize1.png"
            },
            {
                "name": "二等奖",
                "weight": 30,
                "image": "resources/images/prize2.png"
            },
            {
                "name": "三等奖",
                "weight": 60,
                "image": "resources/images/prize3.png"
            }
        ]
        self.save_prizes()
    
    def save_prizes(self):
        """保存奖品配置"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            config = {}
            if os.path.exists(self.config_path):
                try:
                    with open(self.config_path, 'r', encoding='utf-8') as f:
                        config = json.load(f)
                except:
                    config = {}
            
            config['prizes'] = self.prizes
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
                
            return True
        except Exception as e:
            print(f"保存奖品配置失败: {e}")
            return False
    
    def get_all_prizes(self):
        """获取所有奖品"""
        return self.prizes
    
    def set_prizes(self, prizes):
        """设置所有奖品"""
        self.prizes = prizes
    
    def get_prize(self, index):
        """获取指定索引的奖品"""
        if 0 <= index < len(self.prizes):
            return self.prizes[index]
        return None
    
    def add_prize(self, name, weight, image):
        """添加奖品"""
        if len(self.prizes) >= self.max_prizes:
            return False
            
        prize = {
            "name": name,
            "weight": weight,
            "image": image
        }
        
        self.prizes.append(prize)
        return True
    
    def update_prize(self, index, name, weight, image):
        """更新奖品"""
        if 0 <= index < len(self.prizes):
            self.prizes[index] = {
                "name": name,
                "weight": weight,
                "image": image
            }
            return True
        return False
    
    def remove_prize(self, index):
        """删除奖品"""
        if 0 <= index < len(self.prizes):
            del self.prizes[index]
            return True
        return False
    
    def draw(self):
        """抽奖"""
        if not self.prizes:
            return None
            
        # 获取所有权重
        weights = self.get_weights()
        
        # 根据权重随机选择
        total_weight = sum(weights)
        if total_weight <= 0:
            # 如果总权重为0，则平均概率
            index = random.randint(0, len(self.prizes) - 1)
        else:
            # 按权重随机
            r = random.randint(1, total_weight)
            cumulative_weight = 0
            index = 0
            for i, weight in enumerate(weights):
                cumulative_weight += weight
                if r <= cumulative_weight:
                    index = i
                    break
        
        # 返回抽中的奖品和索引
        return {
            "prize": self.prizes[index],
            "index": index,
            "timestamp": datetime.now().isoformat()
        }
    
    def get_weights(self):
        """获取所有奖品的权重列表"""
        return [prize.get('weight', 1) for prize in self.prizes] 