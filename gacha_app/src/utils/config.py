import os
import json

# 颜色配置
COLOR_PALETTE = {
    'background': '#F5F5F5',      # 背景色
    'title_bar': '#EEEEEE',       # 标题栏背景
    'light_bg': '#FFFFFF',        # 亮色背景
    'dark_text': '#333333',       # 深色文本
    'light_text': '#FFFFFF',      # 亮色文本
    'yellow_btn': '#FFC107',      # 黄色按钮
    'blue_btn': '#2196F3',        # 蓝色按钮
    'green_btn': '#4CAF50',       # 绿色按钮
    'red_btn': '#F44336',         # 红色按钮
}

class Config:
    def __init__(self, config_path):
        self.config_path = config_path
        
    def load(self):
        """加载配置"""
        # 默认配置
        default_config = {
            'prizes': [
                {
                    'name': '一等奖',
                    'weight': 10,
                    'image': 'resources/images/prize1.png'
                },
                {
                    'name': '二等奖',
                    'weight': 30,
                    'image': 'resources/images/prize2.png'
                },
                {
                    'name': '三等奖',
                    'weight': 60,
                    'image': 'resources/images/prize3.png'
                }
            ],
            'settings': {
                'animation_speed': 10,
                'sound_enabled': True,
                'language': 'zh_CN'
            }
        }
        
        # 如果配置文件存在，加载它
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    
                # 确保所有必要的配置项都存在
                if 'prizes' not in config:
                    config['prizes'] = default_config['prizes']
                    
                if 'settings' not in config:
                    config['settings'] = default_config['settings']
                else:
                    # 确保设置中的所有项都存在
                    for key, value in default_config['settings'].items():
                        if key not in config['settings']:
                            config['settings'][key] = value
                
                return config
            except Exception as e:
                print(f"加载配置失败: {e}")
                return default_config
        else:
            # 如果配置文件不存在，创建一个默认配置
            self.save(default_config)
            return default_config
    
    def save(self, config):
        """保存配置"""
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(self.config_path), exist_ok=True)
            
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"保存配置失败: {e}")
            return False
            
    def get_example_config_path(self):
        """获取示例配置文件路径"""
        return os.path.join(os.path.dirname(self.config_path), 'example_config.json')
    
    def create_example_config(self):
        """创建示例配置文件"""
        example_config = {
            'prizes': [
                {
                    'name': '示例一等奖',
                    'weight': 10,
                    'image': 'resources/images/prize1.png'
                },
                {
                    'name': '示例二等奖',
                    'weight': 30,
                    'image': 'resources/images/prize2.png'
                },
                {
                    'name': '示例三等奖',
                    'weight': 60,
                    'image': 'resources/images/prize3.png'
                }
            ],
            'settings': {
                'animation_speed': 10,
                'sound_enabled': True,
                'language': 'zh_CN'
            }
        }
        
        example_path = self.get_example_config_path()
        
        try:
            # 确保目录存在
            os.makedirs(os.path.dirname(example_path), exist_ok=True)
            
            with open(example_path, 'w', encoding='utf-8') as f:
                json.dump(example_config, f, ensure_ascii=False, indent=4)
            return True
        except Exception as e:
            print(f"创建示例配置失败: {e}")
            return False 