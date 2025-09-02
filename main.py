import os
import sys
from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

# 动态添加当前插件目录到Python路径
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

# 导入组件
from components.config_manager import ConfigManager
from components.api_client import MCCIslandAPIClient
from components.player_service import PlayerService
from components.game_processors import GameStatsProcessor
from components.command_handlers import CommandRouter

@register("mccisland", "YourName", "MCC Island 玩家数据查询插件", "1.0.0")
class MCCIslandPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.config_manager = None
        self.api_client = None
        self.player_service = None
        self.game_processor = None
        self.command_router = None
        self.initialized = False
    
    async def on_startup(self):
        """插件启动时调用"""
        await self.initialize()

    async def initialize(self):
        """初始化插件组件"""
        try:
            # 获取插件目录
            plugin_dir = os.path.dirname(os.path.abspath(__file__))
            config_path = os.path.join(plugin_dir, "config.json")
            template_path = os.path.join(plugin_dir, "config.json.template")
            
            # 初始化配置管理器
            self.config_manager = ConfigManager(config_path)
            
            # 如果配置文件不存在，从模板创建
            if not os.path.exists(config_path):
                logger.info("配置文件不存在，正在创建...")
                if not self.config_manager.create_template_config(template_path):
                    logger.error("创建配置文件失败")
                    return
                logger.warning("请编辑 config.json 文件，设置您的 MCC Island API 密钥")
                return
            
            # 加载配置
            if not self.config_manager.load_config():
                logger.error("加载配置失败，插件无法正常工作")
                return
            
            # 检查API密钥
            api_key = self.config_manager.get_api_key()
            if not api_key or api_key == "YOUR_MCC_ISLAND_API_KEY_HERE":
                logger.error("API密钥未配置，请在 config.json 中设置您的 MCC Island API 密钥")
                return
            
            # 初始化API客户端
            self.api_client = MCCIslandAPIClient(api_key)
            
            # 初始化服务组件
            self.player_service = PlayerService(self.api_client)
            self.game_processor = GameStatsProcessor(self.player_service)
            
            # 初始化命令路由器
            self.command_router = CommandRouter(self.player_service, self.game_processor)
            
            self.initialized = True
            logger.info("MCC Island 插件初始化成功")
            
        except Exception as e:
            logger.error(f"插件初始化失败: {str(e)}")
            self.initialized = False
    
    @filter.command("mcc")
    async def mcc_command(self, event: AstrMessageEvent):
        """MCC Island 玩家查询命令"""
        if not self.initialized:
            yield event.plain_result("❌ 插件未正确初始化，请检查配置文件和API密钥")
            return
        
        try:
            result = await self.command_router.route_command(event, "mcc")
            yield result
        except Exception as e:
            logger.error(f"处理mcc命令时出错: {str(e)}")
            yield event.plain_result(f"❌ 处理命令时出错: {str(e)}")
    
    @filter.command("fishing")
    async def fishing_command(self, event: AstrMessageEvent):
        """MCC Island 钓鱼统计查询命令"""
        if not self.initialized:
            yield event.plain_result("❌ 插件未正确初始化，请检查配置文件和API密钥")
            return
        
        if not self.config_manager.is_feature_enabled("enable_fishing_command"):
            yield event.plain_result("❌ 钓鱼查询功能已禁用")
            return
        
        try:
            result = await self.command_router.route_command(event, "fishing")
            yield result
        except Exception as e:
            logger.error(f"处理fishing命令时出错: {str(e)}")
            yield event.plain_result(f"❌ 处理命令时出错: {str(e)}")
    
    @filter.command("mccgames")
    async def mccgames_command(self, event: AstrMessageEvent):
        """MCC Island 游戏列表查询命令"""
        if not self.initialized:
            yield event.plain_result("❌ 插件未正确初始化，请检查配置文件和API密钥")
            return
        
        if not self.config_manager.is_feature_enabled("enable_games_list_command"):
            yield event.plain_result("❌ 游戏列表查询功能已禁用")
            return
        
        try:
            result = await self.command_router.route_command(event, "mccgames")
            yield result
        except Exception as e:
            logger.error(f"处理mccgames命令时出错: {str(e)}")
            yield event.plain_result(f"❌ 处理命令时出错: {str(e)}")
    
    @filter.command("mcchelp")
    async def mcchelp_command(self, event: AstrMessageEvent):
        """MCC Island 插件帮助命令"""
        help_text = """🎮 **MCC Island 插件帮助**

**可用命令:**
• `/mcc <玩家名>` - 查询玩家完整信息
• `/mcc <玩家名> <游戏>` - 查询特定游戏统计
• `/fishing <玩家名>` - 查询钓鱼统计
• `/mccgames <玩家名>` - 查询玩家有数据的游戏
• `/mcchelp` - 显示此帮助信息

**支持的游戏类型:**
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
• `/mcc Notch` - 查询Notch的完整信息
• `/mcc Notch fishing` - 查询Notch的钓鱼统计
• `/fishing Notch` - 快速查询钓鱼统计
• `/mccgames Notch` - 查询Notch有数据的游戏

**注意:**
• 支持使用玩家名或UUID查询
• 数据来源于 MCC Island 官方API
• 查询结果可能因API限制而延迟"""
        
        yield event.plain_result(help_text)

    async def terminate(self):
        """插件销毁方法"""
        logger.info("MCC Island 插件正在关闭...")
        self.initialized = False
