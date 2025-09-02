import re
from typing import Optional, Union
from .api_client import MCCIslandAPIClient
from .data_models import Player, DataParser
from astrbot.api import logger

class PlayerService:
    """玩家查询服务"""
    
    def __init__(self, api_client: MCCIslandAPIClient):
        self.api_client = api_client
    
    def is_valid_uuid(self, uuid_string: str) -> bool:
        """验证UUID格式"""
        uuid_pattern = re.compile(
            r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
            re.IGNORECASE
        )
        return bool(uuid_pattern.match(uuid_string))
    
    def is_valid_username(self, username: str) -> bool:
        """验证用户名格式"""
        # Minecraft用户名规则：3-16个字符，只能包含字母、数字和下划线
        if not username or len(username) < 3 or len(username) > 16:
            return False
        return re.match(r'^[a-zA-Z0-9_]+$', username) is not None
    
    async def get_player(self, identifier: str) -> Optional[Player]:
        """获取玩家信息（自动识别UUID或用户名）"""
        try:
            # 清理输入
            identifier = identifier.strip()
            
            if self.is_valid_uuid(identifier):
                # 使用UUID查询（暂时使用基本信息）
                logger.info(f"Querying player by UUID: {identifier}")
                response = await self.api_client.get_player_by_uuid(identifier)
            elif self.is_valid_username(identifier):
                # 使用用户名查询（使用简化版本避免字段错误）
                logger.info(f"Querying player by username: {identifier}")
                response = await self.api_client.get_player_basic_info(identifier)
            else:
                logger.warning(f"Invalid identifier format: {identifier}")
                return None
            
            # 检查响应是否有错误
            if "error" in response:
                error_msg = response['error']
                logger.error(f"API error: {error_msg}")
                # 如果是401错误，提供更详细的错误信息
                if "状态码: 401" in error_msg:
                    logger.error("API密钥无效或未配置，请检查config.json文件")
                return None
            
            # 检查是否找到玩家数据
            if "data" not in response:
                logger.warning("No data in API response")
                return None
            
            player_data = None
            if "player" in response["data"] and response["data"]["player"]:
                player_data = response["data"]["player"]
            elif "playerByUsername" in response["data"] and response["data"]["playerByUsername"]:
                player_data = response["data"]["playerByUsername"]
            
            if not player_data:
                logger.info(f"Player not found: {identifier}")
                return None
            
            # 解析玩家数据
            player = DataParser.parse_player(player_data)
            if player:
                logger.info(f"Successfully retrieved player: {player.username} ({player.uuid})")
            
            return player
            
        except Exception as e:
            logger.error(f"Error getting player {identifier}: {str(e)}")
            return None
    
    async def get_player_by_uuid(self, uuid: str) -> Optional[Player]:
        """通过UUID获取玩家信息"""
        if not self.is_valid_uuid(uuid):
            logger.warning(f"Invalid UUID format: {uuid}")
            return None
        
        try:
            response = await self.api_client.get_player_by_uuid(uuid)
            
            if "error" in response:
                logger.error(f"API error: {response['error']}")
                return None
            
            if "data" not in response or not response["data"].get("player"):
                logger.info(f"Player not found with UUID: {uuid}")
                return None
            
            return DataParser.parse_player(response["data"]["player"])
            
        except Exception as e:
            logger.error(f"Error getting player by UUID {uuid}: {str(e)}")
            return None
    
    async def get_player_by_username(self, username: str) -> Optional[Player]:
        """通过用户名获取玩家信息"""
        if not self.is_valid_username(username):
            logger.warning(f"Invalid username format: {username}")
            return None
        
        try:
            response = await self.api_client.get_player_basic_info(username)
            
            if "error" in response:
                logger.error(f"API error: {response['error']}")
                return None
            
            if "data" not in response or not response["data"].get("playerByUsername"):
                logger.info(f"Player not found with username: {username}")
                return None
            
            return DataParser.parse_player(response["data"]["playerByUsername"])
            
        except Exception as e:
            logger.error(f"Error getting player by username {username}: {str(e)}")
            return None
    
    def format_playtime(self, seconds: int) -> str:
        """格式化游戏时间"""
        if seconds < 60:
            return f"{seconds}秒"
        elif seconds < 3600:
            minutes = seconds // 60
            return f"{minutes}分钟"
        elif seconds < 86400:
            hours = seconds // 3600
            minutes = (seconds % 3600) // 60
            return f"{hours}小时{minutes}分钟"
        else:
            days = seconds // 86400
            hours = (seconds % 86400) // 3600
            return f"{days}天{hours}小时"
    
    def calculate_win_rate(self, wins: int, played: int) -> float:
        """计算胜率"""
        if played == 0:
            return 0.0
        return (wins / played) * 100
    
    def calculate_kd_ratio(self, kills: int, deaths: int) -> float:
        """计算K/D比率"""
        if deaths == 0:
            return float(kills) if kills > 0 else 0.0
        return kills / deaths
    
    def get_rank_display_name(self, ranks: list[str]) -> str:
        """获取等级显示名称"""
        if not ranks:
            return "无等级"
        
        rank_names = {
            "CHAMP": "冠军",
            "GRAND_CHAMP": "大冠军",
            "CREATOR": "创作者",
            "NOXCREW": "Noxcrew团队",
            "MODERATOR": "管理员",
            "SUPPORT": "支持团队"
        }
        
        display_ranks = []
        for rank in ranks:
            display_ranks.append(rank_names.get(rank, rank))
        
        return ", ".join(display_ranks)