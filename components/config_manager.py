import json
import os
from typing import Dict, Any, Optional

# 尝试导入astrbot logger，如果失败则使用标准logging
try:
    from astrbot.api import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

class ConfigManager:
    """配置管理器"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = {}
        self.default_config = {
            "api_key": "",
            "rate_limit": {
                "requests_per_minute": 60,
                "burst_limit": 10
            },
            "cache": {
                "enabled": True,
                "ttl_seconds": 300,
                "max_entries": 1000
            },
            "features": {
                "enable_fishing_command": True,
                "enable_games_list_command": True,
                "enable_detailed_stats": True
            },
            "display": {
                "max_message_length": 2000,
                "use_emojis": True,
                "show_uuid": True
            }
        }
    
    def load_config(self) -> bool:
        """加载配置文件"""
        try:
            if not os.path.exists(self.config_path):
                logger.warning(f"配置文件不存在: {self.config_path}，使用默认配置")
                self.config = self.default_config.copy()
                return False
            
            with open(self.config_path, 'r', encoding='utf-8') as f:
                loaded_config = json.load(f)
            
            # 合并配置，确保所有必需的键都存在
            self.config = self._merge_config(self.default_config, loaded_config)
            
            # 验证配置
            if not self._validate_config():
                logger.error("配置验证失败，使用默认配置")
                self.config = self.default_config.copy()
                return False
            
            logger.info("配置文件加载成功")
            return True
            
        except json.JSONDecodeError as e:
            logger.error(f"配置文件JSON格式错误: {e}")
            self.config = self.default_config.copy()
            return False
        except Exception as e:
            logger.error(f"加载配置文件时出错: {e}")
            self.config = self.default_config.copy()
            return False
    
    def _merge_config(self, default: Dict[str, Any], loaded: Dict[str, Any]) -> Dict[str, Any]:
        """合并配置，确保所有默认键都存在"""
        result = default.copy()
        
        for key, value in loaded.items():
            if key in result:
                if isinstance(value, dict) and isinstance(result[key], dict):
                    result[key] = self._merge_config(result[key], value)
                else:
                    result[key] = value
            else:
                result[key] = value
        
        return result
    
    def _validate_config(self) -> bool:
        """验证配置"""
        try:
            # 检查API密钥
            if not self.config.get("api_key") or self.config["api_key"] == "YOUR_MCC_ISLAND_API_KEY_HERE":
                logger.error("API密钥未配置或使用默认值")
                return False
            
            # 检查必需的配置结构
            required_sections = ["rate_limit", "cache", "features", "display"]
            for section in required_sections:
                if section not in self.config:
                    logger.error(f"缺少配置节: {section}")
                    return False
            
            # 验证数值范围
            if self.config["rate_limit"]["requests_per_minute"] <= 0:
                logger.error("requests_per_minute必须大于0")
                return False
            
            if self.config["cache"]["ttl_seconds"] <= 0:
                logger.error("ttl_seconds必须大于0")
                return False
            
            if self.config["display"]["max_message_length"] <= 0:
                logger.error("max_message_length必须大于0")
                return False
            
            return True
            
        except Exception as e:
            logger.error(f"配置验证时出错: {e}")
            return False
    
    def save_config(self) -> bool:
        """保存配置文件"""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
            
            logger.info("配置文件保存成功")
            return True
            
        except Exception as e:
            logger.error(f"保存配置文件时出错: {e}")
            return False
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值（支持点号分隔的嵌套键）"""
        keys = key.split('.')
        value = self.config
        
        try:
            for k in keys:
                value = value[k]
            return value
        except (KeyError, TypeError):
            return default
    
    def set(self, key: str, value: Any) -> None:
        """设置配置值（支持点号分隔的嵌套键）"""
        keys = key.split('.')
        config = self.config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def get_api_key(self) -> str:
        """获取API密钥"""
        return self.get("api_key", "")
    
    def is_feature_enabled(self, feature: str) -> bool:
        """检查功能是否启用"""
        return self.get(f"features.{feature}", False)
    
    def get_rate_limit(self) -> Dict[str, int]:
        """获取速率限制配置"""
        return self.get("rate_limit", self.default_config["rate_limit"])
    
    def get_cache_config(self) -> Dict[str, Any]:
        """获取缓存配置"""
        return self.get("cache", self.default_config["cache"])
    
    def get_display_config(self) -> Dict[str, Any]:
        """获取显示配置"""
        return self.get("display", self.default_config["display"])
    
    def create_template_config(self, template_path: str = "config.json.template") -> bool:
        """创建配置模板文件"""
        try:
            if os.path.exists(template_path):
                # 如果模板存在，复制到配置文件
                with open(template_path, 'r', encoding='utf-8') as f:
                    template_content = f.read()
                
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    f.write(template_content)
                
                logger.info(f"已从模板创建配置文件: {self.config_path}")
                return True
            else:
                # 创建默认配置文件
                with open(self.config_path, 'w', encoding='utf-8') as f:
                    json.dump(self.default_config, f, indent=2, ensure_ascii=False)
                
                logger.info(f"已创建默认配置文件: {self.config_path}")
                return True
                
        except Exception as e:
            logger.error(f"创建配置文件时出错: {e}")
            return False