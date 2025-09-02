import re
from typing import Optional, List
from astrbot.api.event import AstrMessageEvent, MessageEventResult
from astrbot.api import logger
from .player_service import PlayerService
from .game_processors import GameStatsProcessor
from .data_models import Player

class CommandHandler:
    """命令处理器基类"""
    
    def __init__(self, player_service: PlayerService, game_processor: GameStatsProcessor):
        self.player_service = player_service
        self.game_processor = game_processor
    
    def parse_arguments(self, message: str, command: str) -> List[str]:
        """解析命令参数"""
        # 移除命令前缀（支持有斜杠和无斜杠的情况）
        args_str = message.replace(f"/{command}", "").strip()
        
        # 如果没有找到斜杠前缀，尝试移除无斜杠的命令
        if args_str == message.strip():
            # 检查消息是否以命令开头（无斜杠）
            if message.strip().startswith(command + " "):
                args_str = message.replace(command, "", 1).strip()
            elif message.strip() == command:
                args_str = ""
        
        if not args_str:
            return []
        
        # 简单的参数分割
        return [arg.strip() for arg in args_str.split() if arg.strip()]
    
    async def handle_error(self, event: AstrMessageEvent, error_msg: str) -> MessageEventResult:
        """处理错误消息"""
        logger.error(error_msg)
        return event.plain_result(f"❌ {error_msg}")
    
    async def handle_success(self, event: AstrMessageEvent, success_msg: str) -> MessageEventResult:
        """处理成功消息"""
        return event.plain_result(success_msg)

class PlayerQueryHandler(CommandHandler):
    """玩家查询命令处理器"""
    
    async def handle_player_query(self, event: AstrMessageEvent) -> MessageEventResult:
        """处理玩家查询命令"""
        args = self.parse_arguments(event.message_str, "mcc")
        
        if not args:
            help_text = """🎮 **MCC Island 玩家查询帮助**

**基本用法:**
`/mcc <玩家名或UUID>` - 查询玩家完整信息
`/mcc <玩家名或UUID> <游戏>` - 查询特定游戏统计

**支持的游戏:**
• `global` - 全局统计
• `parkour` - 跑酷勇士
• `skybattle` - 天空大战
• `tgttos` - TGTTOS
• `hitw` - HITW
• `battlebox` - 战斗盒子
• `dynaball` - 炸弹球
• `rocketspleef` - 火箭铲雪
• `fishing` - 钓鱼

**示例:**
`/mcc Notch` - 查询Notch的完整信息
`/mcc Notch fishing` - 查询Notch的钓鱼统计
`/mcc 6a085b2c-19fb-4986-b453-231aa942bbec` - 通过UUID查询"""
            return await self.handle_success(event, help_text)
        
        player_identifier = args[0]
        game_filter = args[1].lower() if len(args) > 1 else None
        
        try:
            # 获取玩家信息
            player = await self.player_service.get_player(player_identifier)
            
            if not player:
                error_msg = f"未找到玩家: {player_identifier}\n\n💡 **可能的原因:**\n• API密钥未配置或无效\n• 玩家名称拼写错误\n• 玩家在MCC Island中不存在\n\n📖 请查看 API_SETUP.md 获取配置帮助"
                return await self.handle_error(event, error_msg)
            
            # 根据参数返回不同的信息
            if game_filter:
                return await self._handle_game_specific_query(event, player, game_filter)
            else:
                return await self._handle_full_player_query(event, player)
                
        except Exception as e:
            return await self.handle_error(event, f"查询玩家信息时出错: {str(e)}")
    
    async def _handle_game_specific_query(self, event: AstrMessageEvent, player: Player, game: str) -> MessageEventResult:
        """处理特定游戏查询"""
        game_mapping = self.game_processor.get_game_name_mapping()
        
        if game not in game_mapping:
            available_games = ", ".join(game_mapping.keys())
            return await self.handle_error(event, f"不支持的游戏类型: {game}\n支持的游戏: {available_games}")
        
        # 获取玩家概览
        overview = self.game_processor.format_player_overview(player)
        
        # 获取特定游戏统计
        game_stats = self.game_processor.format_game_stats(player, game)
        
        if not game_stats:
            return await self.handle_error(event, f"玩家 {player.username} 没有 {game_mapping[game]} 的游戏数据")
        
        result = f"{overview}\n\n{game_stats}"
        return await self.handle_success(event, result)
    
    async def _handle_full_player_query(self, event: AstrMessageEvent, player: Player) -> MessageEventResult:
        """处理完整玩家查询"""
        # 检查消息长度，如果太长则分段发送
        full_stats = self.game_processor.format_all_stats(player)
        
        # 如果消息太长，只返回概览和可用游戏列表
        if len(full_stats) > 2000:
            overview = self.game_processor.format_player_overview(player)
            available_games = self.game_processor.get_available_games(player)
            
            if available_games:
                game_mapping = self.game_processor.get_game_name_mapping()
                game_list = "\n".join([f"• `/mcc {player.username} {game}` - {game_mapping.get(game, game)}" for game in available_games])
                
                result = f"{overview}\n\n🎮 **可查询的游戏统计:**\n{game_list}\n\n💡 使用 `/mcc {player.username} <游戏>` 查询特定游戏统计"
            else:
                result = f"{overview}\n\n❌ 该玩家暂无游戏统计数据"
            
            return await self.handle_success(event, result)
        
        return await self.handle_success(event, full_stats)

class FishingQueryHandler(CommandHandler):
    """钓鱼专用查询处理器"""
    
    async def handle_fishing_query(self, event: AstrMessageEvent) -> MessageEventResult:
        """处理钓鱼查询命令"""
        args = self.parse_arguments(event.message_str, "fishing")
        
        if not args:
            help_text = """🎣 **MCC Island 钓鱼统计查询**

**用法:**
`/fishing <玩家名或UUID>` - 查询玩家钓鱼统计

**示例:**
`/fishing Notch` - 查询Notch的钓鱼统计
`/fishing 6a085b2c-19fb-4986-b453-231aa942bbec` - 通过UUID查询"""
            return await self.handle_success(event, help_text)
        
        player_identifier = args[0]
        
        try:
            # 获取玩家信息
            player = await self.player_service.get_player(player_identifier)
            
            if not player:
                error_msg = f"未找到玩家: {player_identifier}\n\n💡 **可能的原因:**\n• API密钥未配置或无效\n• 玩家名称拼写错误\n• 玩家在MCC Island中不存在\n\n📖 请查看 API_SETUP.md 获取配置帮助"
                return await self.handle_error(event, error_msg)
            
            # 获取玩家概览
            overview = self.game_processor.format_player_overview(player)
            
            # 获取钓鱼统计
            fishing_stats = self.game_processor.format_game_stats(player, "fishing")
            
            if not fishing_stats:
                return await self.handle_error(event, f"玩家 {player.username} 没有钓鱼数据")
            
            result = f"{overview}\n\n{fishing_stats}"
            return await self.handle_success(event, result)
            
        except Exception as e:
            return await self.handle_error(event, f"查询钓鱼统计时出错: {str(e)}")

class GameListHandler(CommandHandler):
    """游戏列表查询处理器"""
    
    async def handle_games_list(self, event: AstrMessageEvent) -> MessageEventResult:
        """处理游戏列表查询"""
        args = self.parse_arguments(event.message_str, "mccgames")
        
        if not args:
            # 显示支持的游戏类型列表
            game_mapping = self.game_processor.get_game_name_mapping()
            game_list = "\n".join([f"• `{key}` - {value}" for key, value in game_mapping.items()])
            
            help_text = f"""🎮 **MCC Island 支持的游戏类型**

{game_list}

**用法:**
`/mcc <玩家名> <游戏类型>` - 查询特定游戏统计
`/mccgames <玩家名>` - 查询玩家有数据的游戏

**示例:**
`/mcc Notch fishing` - 查询Notch的钓鱼统计
`/mccgames Notch` - 查询Notch有数据的游戏"""
            return await self.handle_success(event, help_text)
        
        player_identifier = args[0]
        
        try:
            # 获取玩家信息
            player = await self.player_service.get_player(player_identifier)
            
            if not player:
                return await self.handle_error(event, f"未找到玩家: {player_identifier}")
            
            # 获取可用游戏
            available_games = self.game_processor.get_available_games(player)
            
            if not available_games:
                return await self.handle_error(event, f"玩家 {player.username} 暂无游戏统计数据")
            
            game_mapping = self.game_processor.get_game_name_mapping()
            game_list = "\n".join([f"• `/mcc {player.username} {game}` - {game_mapping.get(game, game)}" for game in available_games])
            
            result = f"""👤 **玩家 {player.username} 的可用游戏统计:**

{game_list}

💡 点击上方命令快速查询对应游戏统计"""
            
            return await self.handle_success(event, result)
            
        except Exception as e:
            return await self.handle_error(event, f"查询玩家游戏列表时出错: {str(e)}")

class CommandRouter:
    """命令路由器"""
    
    def __init__(self, player_service: PlayerService, game_processor: GameStatsProcessor):
        self.player_query_handler = PlayerQueryHandler(player_service, game_processor)
        self.fishing_query_handler = FishingQueryHandler(player_service, game_processor)
        self.games_list_handler = GameListHandler(player_service, game_processor)
    
    async def route_command(self, event: AstrMessageEvent, command: str) -> MessageEventResult:
        """路由命令到对应的处理器"""
        try:
            if command == "mcc":
                return await self.player_query_handler.handle_player_query(event)
            elif command == "fishing":
                return await self.fishing_query_handler.handle_fishing_query(event)
            elif command == "mccgames":
                return await self.games_list_handler.handle_games_list(event)
            else:
                return event.plain_result(f"❌ 未知命令: {command}")
        except Exception as e:
            logger.error(f"Command routing error: {str(e)}")
            return event.plain_result(f"❌ 处理命令时出错: {str(e)}")