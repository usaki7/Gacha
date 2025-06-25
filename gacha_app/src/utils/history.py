import json
import os
from datetime import datetime

class History:
    def __init__(self, history_path):
        self.history_path = history_path
        self.default_history = {
            'draws': [],
            'statistics': {}
        }
        
    def load(self):
        """加载历史记录"""
        try:
            if os.path.exists(self.history_path):
                with open(self.history_path, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self._create_default_history()
        except Exception as e:
            print(f"加载历史记录失败: {e}")
            return self._create_default_history()
    
    def get_all_records(self):
        """获取所有抽奖记录"""
        history_data = self.load()
        return history_data.get('draws', [])
            
    def save(self, history_data):
        """保存历史记录"""
        try:
            os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
            with open(self.history_path, 'w', encoding='utf-8') as f:
                json.dump(history_data, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"保存历史记录失败: {e}")
            return False
            
    def add_record(self, prize_data):
        """添加抽奖记录"""
        history_data = self.load()
        
        # 创建新的记录
        record = {
            'prize': {
                'name': prize_data['prize']['name'],
                'weight': prize_data['prize']['weight'],
                'image': prize_data['prize'].get('image', '')
            },
            'timestamp': prize_data['timestamp'],
            'index': prize_data['index']
        }
        
        history_data['draws'].append(record)
        self._update_statistics(history_data)
        return self.save(history_data)
        
    def clear(self):
        """清空历史记录"""
        return self.save(self.default_history.copy())
        
    def _create_default_history(self):
        """创建默认历史记录文件"""
        try:
            os.makedirs(os.path.dirname(self.history_path), exist_ok=True)
            with open(self.history_path, 'w', encoding='utf-8') as f:
                json.dump(self.default_history, f, ensure_ascii=False, indent=4)
            return self.default_history.copy()
        except Exception as e:
            print(f"创建默认历史记录文件失败: {e}")
            return self.default_history.copy()
            
    def _update_statistics(self, history_data):
        """更新统计信息"""
        stats = {}
        
        for draw in history_data.get('draws', []):
            prize_name = draw['prize']['name']
            
            if prize_name not in stats:
                stats[prize_name] = {
                    'count': 0
                }
            stats[prize_name]['count'] += 1
        
        history_data['statistics'] = stats 