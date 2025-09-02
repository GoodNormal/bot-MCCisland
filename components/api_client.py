import aiohttp
import json
from typing import Dict, Any, Optional

# 尝试导入astrbot logger，如果失败则使用标准logging
try:
    from astrbot.api import logger
except ImportError:
    import logging
    logger = logging.getLogger(__name__)

class MCCIslandAPIClient:
    """MCC Island GraphQL API客户端 - 修复版本"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.mccisland.net/graphql"
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json",
            "User-Agent": "MCCIsland-AstrBot-Plugin/1.0.0"
        }
    
    async def execute_query(self, query: str, variables: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """执行GraphQL查询"""
        payload = {
            "query": query,
            "variables": variables or {}
        }
        
        try:
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=self.headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        data = await response.json()
                        if "errors" in data:
                            logger.error(f"GraphQL errors: {data['errors']}")
                            return {"error": "GraphQL查询出错", "details": data["errors"]}
                        return data
                    else:
                        logger.error(f"API request failed with status {response.status}")
                        return {"error": f"API请求失败，状态码: {response.status}"}
        except Exception as e:
            logger.error(f"API request exception: {str(e)}")
            return {"error": f"请求异常: {str(e)}"}
    
    async def get_player_by_uuid(self, uuid: str) -> Dict[str, Any]:
        """通过UUID获取玩家信息 - 仅基本字段"""
        query = """
        query player($uuid: UUID!) {
            player(uuid: $uuid) {
                uuid
                username
                ranks
                status {
                    online
                }
            }
        }
        """
        variables = {"uuid": uuid}
        return await self.execute_query(query, variables)
    
    async def get_player_by_username(self, username: str) -> Dict[str, Any]:
        """通过用户名获取玩家信息 - 仅基本字段"""
        query = """
        query playerByUsername($username: String!) {
            playerByUsername(username: $username) {
                uuid
                username
                ranks
                status {
                    online
                }
            }
        }
        """
        variables = {"username": username}
        return await self.execute_query(query, variables)
    
    async def get_player_basic_info(self, username: str) -> Dict[str, Any]:
        """获取玩家基本信息 - 最简化版本"""
        query = """
        query playerByUsername($username: String!) {
            playerByUsername(username: $username) {
                uuid
                username
                ranks
            }
        }
        """
        variables = {"username": username}
        return await self.execute_query(query, variables)
    
    async def get_next_rotation(self, rotation: str = "DAILY") -> Dict[str, Any]:
        """获取下次轮换时间"""
        query = """
        query nextRotation($rotation: Rotation!) {
            nextRotation(rotation: $rotation)
        }
        """
        variables = {"rotation": rotation}
        return await self.execute_query(query, variables)