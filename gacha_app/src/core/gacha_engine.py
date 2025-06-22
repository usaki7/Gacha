import random
import time
from datetime import datetime

class GachaEngine:
    def __init__(self, prize_manager):
        self.prize_manager = prize_manager
        
    def draw(self):
        """抽奖"""
        return self.prize_manager.draw()
        
    def simulate_draws(self, num_draws):
        """模拟多次抽奖，用于统计概率"""
        results = []
        for _ in range(num_draws):
            results.append(self.draw())
        return results
        
    def get_statistics(self, results):
        """获取抽奖统计信息"""
        stats = {}
        total = len(results)
        
        for result in results:
            prize_name = result['prize']['name']
            if prize_name in stats:
                stats[prize_name] += 1
            else:
                stats[prize_name] = 1
                
        # 计算百分比
        for prize_name, count in stats.items():
            stats[prize_name] = {
                'count': count,
                'percentage': round(count / total * 100, 2) if total > 0 else 0
            }
            
        return stats
    
    def generate_animation_frames(self, final_index, duration_ms=1500, interval_ms=50):
        """生成动画帧序列"""
        total_prizes = len(self.prize_manager.get_all_prizes())
        if total_prizes == 0:
            return []
            
        frame_count = int(duration_ms / interval_ms)
        # 生成随机帧
        frames = [random.randrange(total_prizes) for _ in range(frame_count)]
        # 添加最终结果帧
        frames.append(final_index)
        return frames 