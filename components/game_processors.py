from typing import Optional, List
from .data_models import (
    Player, PlayerStatistics, GlobalStats, ParkourWarriorStats, SkyBattleStats,
    TGTTOSStats, HITWStats, BattleBoxStats, DynaballStats, RocketSpleefStats, FishingStats
)
from .player_service import PlayerService

class GameStatsFormatter:
    """游戏统计数据格式化器"""
    
    def __init__(self, player_service: PlayerService):
        self.player_service = player_service
    
    def format_global_stats(self, stats: GlobalStats) -> str:
        """格式化全局统计"""
        win_rate = self.player_service.calculate_win_rate(stats.wins, stats.played)
        playtime = self.player_service.format_playtime(stats.playtime)
        
        return f"""📊 **全局统计**
🏆 胜利次数: {stats.wins}
🎮 游戏次数: {stats.played}
📈 胜率: {win_rate:.1f}%
⏱️ 游戏时长: {playtime}"""
    
    def format_parkour_warrior_stats(self, stats: ParkourWarriorStats) -> str:
        """格式化跑酷勇士统计"""
        win_rate = self.player_service.calculate_win_rate(stats.wins, stats.played)
        playtime = self.player_service.format_playtime(stats.playtime)
        completion_rate = (stats.completions / stats.played * 100) if stats.played > 0 else 0
        
        fastest_text = "无记录"
        if stats.fastest_completion:
            fastest_text = f"{stats.fastest_completion / 1000:.2f}秒"
        
        return f"""🏃 **跑酷勇士 (Parkour Warrior)**
🏆 胜利次数: {stats.wins}
🎮 游戏次数: {stats.played}
📈 胜率: {win_rate:.1f}%
✅ 完成次数: {stats.completions}
📊 完成率: {completion_rate:.1f}%
⚡ 最快完成: {fastest_text}
⏱️ 游戏时长: {playtime}"""
    
    def format_sky_battle_stats(self, stats: SkyBattleStats) -> str:
        """格式化天空大战统计"""
        win_rate = self.player_service.calculate_win_rate(stats.wins, stats.played)
        kd_ratio = self.player_service.calculate_kd_ratio(stats.kills, stats.deaths)
        playtime = self.player_service.format_playtime(stats.playtime)
        
        return f"""⚔️ **天空大战 (Sky Battle)**
🏆 胜利次数: {stats.wins}
🎮 游戏次数: {stats.played}
📈 胜率: {win_rate:.1f}%
💀 击杀数: {stats.kills}
☠️ 死亡数: {stats.deaths}
📊 K/D比率: {kd_ratio:.2f}
⏱️ 游戏时长: {playtime}"""
    
    def format_tgttos_stats(self, stats: TGTTOSStats) -> str:
        """格式化TGTTOS统计"""
        win_rate = self.player_service.calculate_win_rate(stats.wins, stats.played)
        finish_rate = (stats.finishes / stats.played * 100) if stats.played > 0 else 0
        playtime = self.player_service.format_playtime(stats.playtime)
        
        fastest_text = "无记录"
        if stats.fastest_completion:
            fastest_text = f"{stats.fastest_completion / 1000:.2f}秒"
        
        return f"""🏁 **TGTTOS (To Get To The Other Side)**
🏆 胜利次数: {stats.wins}
🎮 游戏次数: {stats.played}
📈 胜率: {win_rate:.1f}%
🎯 完成次数: {stats.finishes}
📊 完成率: {finish_rate:.1f}%
⚡ 最快完成: {fastest_text}
⏱️ 游戏时长: {playtime}"""
    
    def format_hitw_stats(self, stats: HITWStats) -> str:
        """格式化HITW统计"""
        win_rate = self.player_service.calculate_win_rate(stats.wins, stats.played)
        qualification_rate = (stats.qualifications / stats.played * 100) if stats.played > 0 else 0
        playtime = self.player_service.format_playtime(stats.playtime)
        
        fastest_text = "无记录"
        if stats.fastest_completion:
            fastest_text = f"{stats.fastest_completion / 1000:.2f}秒"
        
        return f"""🕳️ **HITW (Hole in the Wall)**
🏆 胜利次数: {stats.wins}
🎮 游戏次数: {stats.played}
📈 胜率: {win_rate:.1f}%
✅ 晋级次数: {stats.qualifications}
📊 晋级率: {qualification_rate:.1f}%
⚡ 最快完成: {fastest_text}
⏱️ 游戏时长: {playtime}"""
    
    def format_battle_box_stats(self, stats: BattleBoxStats) -> str:
        """格式化战斗盒子统计"""
        win_rate = self.player_service.calculate_win_rate(stats.wins, stats.played)
        kd_ratio = self.player_service.calculate_kd_ratio(stats.kills, stats.deaths)
        playtime = self.player_service.format_playtime(stats.playtime)
        
        return f"""📦 **战斗盒子 (Battle Box)**
🏆 胜利次数: {stats.wins}
🎮 游戏次数: {stats.played}
📈 胜率: {win_rate:.1f}%
💀 击杀数: {stats.kills}
☠️ 死亡数: {stats.deaths}
📊 K/D比率: {kd_ratio:.2f}
⏱️ 游戏时长: {playtime}"""
    
    def format_dynaball_stats(self, stats: DynaballStats) -> str:
        """格式化炸弹球统计"""
        win_rate = self.player_service.calculate_win_rate(stats.wins, stats.played)
        kd_ratio = self.player_service.calculate_kd_ratio(stats.kills, stats.deaths)
        playtime = self.player_service.format_playtime(stats.playtime)
        
        return f"""💣 **炸弹球 (Dynaball)**
🏆 胜利次数: {stats.wins}
🎮 游戏次数: {stats.played}
📈 胜率: {win_rate:.1f}%
💀 击杀数: {stats.kills}
☠️ 死亡数: {stats.deaths}
📊 K/D比率: {kd_ratio:.2f}
⏱️ 游戏时长: {playtime}"""
    
    def format_rocket_spleef_stats(self, stats: RocketSpleefStats) -> str:
        """格式化火箭铲雪统计"""
        win_rate = self.player_service.calculate_win_rate(stats.wins, stats.played)
        kd_ratio = self.player_service.calculate_kd_ratio(stats.kills, stats.deaths)
        playtime = self.player_service.format_playtime(stats.playtime)
        
        return f"""🚀 **火箭铲雪 (Rocket Spleef)**
🏆 胜利次数: {stats.wins}
🎮 游戏次数: {stats.played}
📈 胜率: {win_rate:.1f}%
💀 击杀数: {stats.kills}
☠️ 死亡数: {stats.deaths}
📊 K/D比率: {kd_ratio:.2f}
⏱️ 游戏时长: {playtime}"""
    
    def format_fishing_stats(self, stats: FishingStats) -> str:
        """格式化钓鱼统计"""
        if stats.total == 0:
            return "🎣 **钓鱼统计**\n暂无钓鱼记录"
        
        treasure_rate = (stats.treasure / stats.total * 100) if stats.total > 0 else 0
        fish_rate = (stats.fish / stats.total * 100) if stats.total > 0 else 0
        junk_rate = (stats.junk / stats.total * 100) if stats.total > 0 else 0
        
        return f"""🎣 **钓鱼统计**
🎯 总钓鱼次数: {stats.total}
💎 宝藏: {stats.treasure} ({treasure_rate:.1f}%)
🐟 鱼类: {stats.fish} ({fish_rate:.1f}%)
🗑️ 垃圾: {stats.junk} ({junk_rate:.1f}%)"""

class GameStatsProcessor:
    """游戏统计处理器"""
    
    def __init__(self, player_service: PlayerService):
        self.player_service = player_service
        self.formatter = GameStatsFormatter(player_service)
    
    def get_available_games(self, player: Player) -> List[str]:
        """获取玩家有数据的游戏列表"""
        if not player.statistics:
            return []
        
        games = []
        stats = player.statistics
        
        if stats.parkour_warrior and stats.parkour_warrior.played > 0:
            games.append("parkour")
        if stats.sky_battle and stats.sky_battle.played > 0:
            games.append("skybattle")
        if stats.tgttos and stats.tgttos.played > 0:
            games.append("tgttos")
        if stats.hitw and stats.hitw.played > 0:
            games.append("hitw")
        if stats.battle_box and stats.battle_box.played > 0:
            games.append("battlebox")
        if stats.dynaball and stats.dynaball.played > 0:
            games.append("dynaball")
        if stats.rocket_spleef and stats.rocket_spleef.played > 0:
            games.append("rocketspleef")
        if stats.fishing and stats.fishing.total > 0:
            games.append("fishing")
        
        return games
    
    def format_player_overview(self, player: Player) -> str:
        """格式化玩家概览"""
        rank_display = self.player_service.get_rank_display_name(player.ranks)
        
        overview = f"""👤 **玩家信息: {player.username}**
🆔 UUID: `{player.uuid}`
🏅 等级: {rank_display}"""
        
        if player.crown_level:
            overview += f"\n👑 皇冠等级: {player.crown_level.level} ({player.crown_level.progress:.1f}%)"
        
        if player.mcc_plus_status:
            plus_status = "激活" if player.mcc_plus_status.active else "未激活"
            overview += f"\n⭐ MCC+: {plus_status}"
            if player.mcc_plus_status.tier:
                overview += f" ({player.mcc_plus_status.tier})"
        
        if player.status:
            online_status = "在线" if player.status.online else "离线"
            overview += f"\n🟢 状态: {online_status}"
            if player.status.last_login:
                overview += f"\n🕐 最后登录: {player.status.last_login}"
        
        if player.collections:
            if player.collections.currency is not None:
                overview += f"\n💰 货币: {player.collections.currency}"
            if player.collections.trophies is not None:
                overview += f"\n🏆 奖杯: {player.collections.trophies}"
        
        return overview
    
    def format_game_stats(self, player: Player, game: str) -> Optional[str]:
        """格式化指定游戏的统计数据"""
        if not player.statistics:
            return None
        
        stats = player.statistics
        
        if game == "global":
            return self.formatter.format_global_stats(stats.global_stats)
        elif game == "parkour" and stats.parkour_warrior:
            return self.formatter.format_parkour_warrior_stats(stats.parkour_warrior)
        elif game == "skybattle" and stats.sky_battle:
            return self.formatter.format_sky_battle_stats(stats.sky_battle)
        elif game == "tgttos" and stats.tgttos:
            return self.formatter.format_tgttos_stats(stats.tgttos)
        elif game == "hitw" and stats.hitw:
            return self.formatter.format_hitw_stats(stats.hitw)
        elif game == "battlebox" and stats.battle_box:
            return self.formatter.format_battle_box_stats(stats.battle_box)
        elif game == "dynaball" and stats.dynaball:
            return self.formatter.format_dynaball_stats(stats.dynaball)
        elif game == "rocketspleef" and stats.rocket_spleef:
            return self.formatter.format_rocket_spleef_stats(stats.rocket_spleef)
        elif game == "fishing" and stats.fishing:
            return self.formatter.format_fishing_stats(stats.fishing)
        
        return None
    
    def format_all_stats(self, player: Player) -> str:
        """格式化所有统计数据"""
        result = [self.format_player_overview(player)]
        
        if player.statistics:
            # 添加全局统计
            global_stats = self.formatter.format_global_stats(player.statistics.global_stats)
            result.append(global_stats)
            
            # 添加各游戏统计
            games = self.get_available_games(player)
            for game in games:
                game_stats = self.format_game_stats(player, game)
                if game_stats:
                    result.append(game_stats)
        
        return "\n\n".join(result)
    
    def get_game_name_mapping(self) -> dict:
        """获取游戏名称映射"""
        return {
            "global": "全局统计",
            "parkour": "跑酷勇士",
            "skybattle": "天空大战",
            "tgttos": "TGTTOS",
            "hitw": "HITW",
            "battlebox": "战斗盒子",
            "dynaball": "炸弹球",
            "rocketspleef": "火箭铲雪",
            "fishing": "钓鱼"
        }