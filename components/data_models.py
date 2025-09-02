from dataclasses import dataclass
from typing import Optional, Dict, Any
from datetime import datetime

@dataclass
class MCCPlusStatus:
    """MCC Plus状态"""
    active: bool
    tier: Optional[str] = None

@dataclass
class CrownLevel:
    """皇冠等级"""
    level: int
    progress: float

@dataclass
class PlayerStatus:
    """玩家状态"""
    first_login: Optional[str]
    last_login: Optional[str]
    online: bool

@dataclass
class Collections:
    """收藏品"""
    currency: Optional[int]
    cosmetics: Optional[int]
    trophies: Optional[int]

@dataclass
class Social:
    """社交信息"""
    friends: Optional[int]
    party: Optional[Dict[str, Any]]

@dataclass
class GlobalStats:
    """全局统计"""
    wins: int
    played: int
    playtime: int

@dataclass
class ParkourWarriorStats:
    """跑酷勇士统计"""
    wins: int
    played: int
    playtime: int
    completions: int
    fastest_completion: Optional[int]

@dataclass
class SkyBattleStats:
    """天空大战统计"""
    wins: int
    played: int
    playtime: int
    kills: int
    deaths: int

@dataclass
class TGTTOSStats:
    """TGTTOS统计"""
    wins: int
    played: int
    playtime: int
    finishes: int
    fastest_completion: Optional[int]

@dataclass
class HITWStats:
    """HITW统计"""
    wins: int
    played: int
    playtime: int
    qualifications: int
    fastest_completion: Optional[int]

@dataclass
class BattleBoxStats:
    """战斗盒子统计"""
    wins: int
    played: int
    playtime: int
    kills: int
    deaths: int

@dataclass
class DynaballStats:
    """炸弹球统计"""
    wins: int
    played: int
    playtime: int
    kills: int
    deaths: int

@dataclass
class RocketSpleefStats:
    """火箭铲雪统计"""
    wins: int
    played: int
    playtime: int
    kills: int
    deaths: int

@dataclass
class FishingStats:
    """钓鱼统计"""
    total: int
    treasure: int
    fish: int
    junk: int

@dataclass
class PlayerStatistics:
    """玩家统计数据"""
    global_stats: GlobalStats
    parkour_warrior: Optional[ParkourWarriorStats] = None
    sky_battle: Optional[SkyBattleStats] = None
    tgttos: Optional[TGTTOSStats] = None
    hitw: Optional[HITWStats] = None
    battle_box: Optional[BattleBoxStats] = None
    dynaball: Optional[DynaballStats] = None
    rocket_spleef: Optional[RocketSpleefStats] = None
    fishing: Optional[FishingStats] = None

@dataclass
class Player:
    """玩家信息"""
    uuid: str
    username: str
    ranks: list[str]
    mcc_plus_status: Optional[MCCPlusStatus] = None
    crown_level: Optional[CrownLevel] = None
    status: Optional[PlayerStatus] = None
    collections: Optional[Collections] = None
    social: Optional[Social] = None
    statistics: Optional[PlayerStatistics] = None

class DataParser:
    """数据解析器"""
    
    @staticmethod
    def parse_mcc_plus_status(data: Optional[Dict[str, Any]]) -> Optional[MCCPlusStatus]:
        if not data:
            return None
        return MCCPlusStatus(
            active=data.get('active', False),
            tier=data.get('tier')
        )
    
    @staticmethod
    def parse_crown_level(data: Optional[Dict[str, Any]]) -> Optional[CrownLevel]:
        if not data:
            return None
        return CrownLevel(
            level=data.get('level', 0),
            progress=data.get('progress', 0.0)
        )
    
    @staticmethod
    def parse_status(data: Optional[Dict[str, Any]]) -> Optional[PlayerStatus]:
        if not data:
            return None
        return PlayerStatus(
            first_login=data.get('firstLogin'),
            last_login=data.get('lastLogin'),
            online=data.get('online', False)
        )
    
    @staticmethod
    def parse_collections(data: Optional[Dict[str, Any]]) -> Optional[Collections]:
        if not data:
            return None
        return Collections(
            currency=data.get('currency'),
            cosmetics=data.get('cosmetics'),
            trophies=data.get('trophies')
        )
    
    @staticmethod
    def parse_social(data: Optional[Dict[str, Any]]) -> Optional[Social]:
        if not data:
            return None
        return Social(
            friends=data.get('friends'),
            party=data.get('party')
        )
    
    @staticmethod
    def parse_global_stats(data: Optional[Dict[str, Any]]) -> Optional[GlobalStats]:
        if not data:
            return None
        return GlobalStats(
            wins=data.get('wins', 0),
            played=data.get('played', 0),
            playtime=data.get('playtime', 0)
        )
    
    @staticmethod
    def parse_parkour_warrior_stats(data: Optional[Dict[str, Any]]) -> Optional[ParkourWarriorStats]:
        if not data:
            return None
        return ParkourWarriorStats(
            wins=data.get('wins', 0),
            played=data.get('played', 0),
            playtime=data.get('playtime', 0),
            completions=data.get('completions', 0),
            fastest_completion=data.get('fastestCompletion')
        )
    
    @staticmethod
    def parse_sky_battle_stats(data: Optional[Dict[str, Any]]) -> Optional[SkyBattleStats]:
        if not data:
            return None
        return SkyBattleStats(
            wins=data.get('wins', 0),
            played=data.get('played', 0),
            playtime=data.get('playtime', 0),
            kills=data.get('kills', 0),
            deaths=data.get('deaths', 0)
        )
    
    @staticmethod
    def parse_tgttos_stats(data: Optional[Dict[str, Any]]) -> Optional[TGTTOSStats]:
        if not data:
            return None
        return TGTTOSStats(
            wins=data.get('wins', 0),
            played=data.get('played', 0),
            playtime=data.get('playtime', 0),
            finishes=data.get('finishes', 0),
            fastest_completion=data.get('fastestCompletion')
        )
    
    @staticmethod
    def parse_hitw_stats(data: Optional[Dict[str, Any]]) -> Optional[HITWStats]:
        if not data:
            return None
        return HITWStats(
            wins=data.get('wins', 0),
            played=data.get('played', 0),
            playtime=data.get('playtime', 0),
            qualifications=data.get('qualifications', 0),
            fastest_completion=data.get('fastestCompletion')
        )
    
    @staticmethod
    def parse_battle_box_stats(data: Optional[Dict[str, Any]]) -> Optional[BattleBoxStats]:
        if not data:
            return None
        return BattleBoxStats(
            wins=data.get('wins', 0),
            played=data.get('played', 0),
            playtime=data.get('playtime', 0),
            kills=data.get('kills', 0),
            deaths=data.get('deaths', 0)
        )
    
    @staticmethod
    def parse_dynaball_stats(data: Optional[Dict[str, Any]]) -> Optional[DynaballStats]:
        if not data:
            return None
        return DynaballStats(
            wins=data.get('wins', 0),
            played=data.get('played', 0),
            playtime=data.get('playtime', 0),
            kills=data.get('kills', 0),
            deaths=data.get('deaths', 0)
        )
    
    @staticmethod
    def parse_rocket_spleef_stats(data: Optional[Dict[str, Any]]) -> Optional[RocketSpleefStats]:
        if not data:
            return None
        return RocketSpleefStats(
            wins=data.get('wins', 0),
            played=data.get('played', 0),
            playtime=data.get('playtime', 0),
            kills=data.get('kills', 0),
            deaths=data.get('deaths', 0)
        )
    
    @staticmethod
    def parse_fishing_stats(data: Optional[Dict[str, Any]]) -> Optional[FishingStats]:
        if not data:
            return None
        return FishingStats(
            total=data.get('total', 0),
            treasure=data.get('treasure', 0),
            fish=data.get('fish', 0),
            junk=data.get('junk', 0)
        )
    
    @staticmethod
    def parse_statistics(data: Optional[Dict[str, Any]]) -> Optional[PlayerStatistics]:
        if not data:
            return None
        
        global_stats = DataParser.parse_global_stats(data.get('global'))
        if not global_stats:
            return None
            
        return PlayerStatistics(
            global_stats=global_stats,
            parkour_warrior=DataParser.parse_parkour_warrior_stats(data.get('parkourWarrior')),
            sky_battle=DataParser.parse_sky_battle_stats(data.get('skyBattle')),
            tgttos=DataParser.parse_tgttos_stats(data.get('tgttos')),
            hitw=DataParser.parse_hitw_stats(data.get('hitw')),
            battle_box=DataParser.parse_battle_box_stats(data.get('battleBox')),
            dynaball=DataParser.parse_dynaball_stats(data.get('dynaball')),
            rocket_spleef=DataParser.parse_rocket_spleef_stats(data.get('rocketSpleef')),
            fishing=DataParser.parse_fishing_stats(data.get('fishing'))
        )
    
    @staticmethod
    def parse_player(data: Dict[str, Any]) -> Optional[Player]:
        """解析玩家数据"""
        if not data or 'uuid' not in data:
            return None
        
        # 对于简化的查询，只解析基本字段
        return Player(
            uuid=data['uuid'],
            username=data.get('username', ''),
            ranks=data.get('ranks', []),
            mcc_plus_status=DataParser.parse_mcc_plus_status(data.get('mccPlusStatus')) if 'mccPlusStatus' in data else None,
            crown_level=DataParser.parse_crown_level(data.get('crownLevel')) if 'crownLevel' in data else None,
            status=DataParser.parse_status(data.get('status')) if 'status' in data else None,
            collections=DataParser.parse_collections(data.get('collections')) if 'collections' in data else None,
            social=DataParser.parse_social(data.get('social')) if 'social' in data else None,
            statistics=DataParser.parse_statistics(data.get('statistics')) if 'statistics' in data else None
        )