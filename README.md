# MCC Island Plugin for AstrBot

一个用于查询 MCC Island 玩家数据的 AstrBot 插件，支持查询所有游戏的统计数据，包括钓鱼等特殊游戏模式。

## 功能特性

- 🎮 **全面的游戏支持**: 支持所有 MCC Island 游戏模式
- 🎣 **钓鱼专项查询**: 独立的钓鱼统计查询功能
- 👤 **灵活的玩家查询**: 支持使用玩家名或 UUID 查询
- ⚙️ **可配置功能**: 通过配置文件控制各项功能开关
- 🏗️ **组件化架构**: 模块化设计，易于维护和扩展
- 📊 **详细统计**: 提供胜率、K/D比、游戏时长等详细数据

## 支持的游戏

- **Global** - 全局统计
- **Parkour Warrior** - 跑酷勇士
- **Sky Battle** - 天空大战
- **TGTTOS** - To Get To The Other Side
- **Hole in the Wall** - 穿墙而过
- **Battle Box** - 战斗盒子
- **Dynaball** - 炸弹球
- **Rocket Spleef** - 火箭铲雪
- **Fishing** - 钓鱼

## 安装步骤

### 1. 前置要求

- AstrBot 框架
- Python 3.7+
- MCC Island API 密钥

### 2. 获取 API 密钥

1. 访问 [MCC Island API 文档](https://api.mccisland.net/docs)
2. 按照官方指引获取 API 密钥
3. 保存好您的 API 密钥，稍后配置时需要使用

### 3. 安装插件

1. 将插件文件夹放置到 AstrBot 的插件目录
2. 安装依赖包：
   ```bash
   pip install -r requirements.txt
   ```

### 4. 配置插件

1. 首次启动插件时，会自动创建 `config.json` 配置文件
2. 编辑 `config.json` 文件，将 `YOUR_MCC_ISLAND_API_KEY_HERE` 替换为您的实际 API 密钥
3. 重启 AstrBot

**重要提示**: 如果您看到 "❌ 未找到玩家" 错误，通常是因为 API 密钥未正确配置。请参考 `API_SETUP.md` 获取详细配置指南。

### 5. 配置文件说明

`config.json` 文件包含以下配置选项：
- `api_key`: 您的 MCC Island API 密钥
- `rate_limit`: API 请求频率限制
- `cache`: 缓存设置
- `features`: 功能开关
- `display`: 显示选项

## 使用方法

### 基本命令

#### `/mcc <玩家名>` - 查询玩家完整信息
查询指定玩家的基本信息和全局统计数据。

**示例:**
```
/mcc Notch
/mcc 069a79f4-44e9-4726-a5be-fca90e38aaf5
```

#### `/mcc <玩家名> <游戏>` - 查询特定游戏统计
查询指定玩家在特定游戏中的详细统计数据。

**示例:**
```
/mcc Notch fishing
/mcc Notch parkour
/mcc Notch skybattle
```

#### `/fishing <玩家名>` - 快速查询钓鱼统计
专门用于查询钓鱼统计的快捷命令。

**示例:**
```
/fishing Notch
```

#### `/mccgames <玩家名>` - 查询可用游戏列表
显示指定玩家有统计数据的所有游戏。

**示例:**
```
/mccgames Notch
```

#### `/mcchelp` - 显示帮助信息
显示插件的详细使用说明。

### 支持的游戏类型参数

- `global` - 全局统计
- `parkour` - 跑酷勇士
- `skybattle` - 天空大战
- `tgttos` - TGTTOS
- `hitw` - 穿墙而过
- `battlebox` - 战斗盒子
- `dynaball` - 炸弹球
- `rocketspleef` - 火箭铲雪
- `fishing` - 钓鱼

## 配置选项

### API 配置
- `api_key`: MCC Island API 密钥（必需）

### 速率限制
- `requests_per_minute`: 每分钟最大请求数
- `burst_limit`: 突发请求限制

### 缓存设置
- `enable_cache`: 是否启用缓存
- `cache_duration_minutes`: 缓存持续时间（分钟）

### 功能开关
- `enable_fishing_command`: 启用钓鱼查询命令
- `enable_games_list_command`: 启用游戏列表命令
- `enable_detailed_stats`: 启用详细统计显示

### 显示设置
- `max_games_per_message`: 每条消息最大显示游戏数
- `show_rank_colors`: 显示等级颜色
- `compact_mode`: 紧凑显示模式

## 项目结构

```
bot-MCCisland/
├── main.py                    # 主插件文件
├── metadata.yaml              # 插件元数据
├── requirements.txt           # 依赖包列表
├── config.json.template       # 配置文件模板
├── config.json               # 实际配置文件（自动生成）
├── README.md                 # 说明文档
└── components/               # 组件目录
    ├── __init__.py          # 组件包初始化
    ├── api_client.py        # API 客户端
    ├── data_models.py       # 数据模型
    ├── player_service.py    # 玩家服务
    ├── game_processors.py   # 游戏数据处理器
    ├── command_handlers.py  # 命令处理器
    └── config_manager.py    # 配置管理器
```

## 故障排除

### 常见问题

1. **插件无法初始化**
   - 检查 `config.json` 文件是否存在且格式正确
   - 确认 API 密钥已正确设置
   - 查看 AstrBot 日志获取详细错误信息

2. **API 请求失败**
   - 验证 API 密钥是否有效
   - 检查网络连接
   - 确认是否超出 API 速率限制

3. **玩家查询无结果**
   - 确认玩家名拼写正确
   - 尝试使用 UUID 查询
   - 检查玩家是否在 MCC Island 有游戏记录

### 日志信息

插件会在 AstrBot 日志中记录以下信息：
- 初始化状态
- API 请求结果
- 错误和异常信息
- 配置加载状态

## 开发信息

### 技术栈
- **框架**: AstrBot Plugin API
- **HTTP 客户端**: aiohttp
- **数据处理**: Python dataclasses
- **异步支持**: asyncio

### 架构设计
- **组件化**: 每个功能模块独立设计
- **异步处理**: 全异步 API 调用
- **错误处理**: 完善的异常捕获和用户友好的错误提示
- **配置驱动**: 灵活的配置选项

## 故障排除

### ❌ 未找到玩家: xxx

**可能原因:**
- API 密钥未配置或无效
- 玩家名称拼写错误
- 玩家在 MCC Island 中不存在

**解决方法:**
1. 检查 `config.json` 中的 API 密钥是否正确
2. 确认玩家名称拼写无误
3. 参考 `API_SETUP.md` 重新配置 API 密钥

### ❌ 插件未正确初始化

**可能原因:**
- 配置文件格式错误
- API 密钥未设置
- 依赖包未安装

**解决方法:**
1. 检查 `config.json` 文件格式是否正确
2. 确认 API 密钥已正确设置
3. 运行 `pip install -r requirements.txt` 安装依赖
4. 查看 AstrBot 日志获取详细错误信息

### ❌ API请求失败，状态码: 401

**原因:** API 密钥无效或已过期

**解决方法:**
1. 重新生成 API 密钥
2. 更新 `config.json` 中的 API 密钥
3. 重启 AstrBot

## 贡献

欢迎提交 Issue 和 Pull Request 来改进这个插件！

## 许可证

本项目采用 MIT 许可证。

## 相关链接

- [MCC Island 官网](https://mccisland.net/)
- [MCC Island API 文档](https://api.mccisland.net/docs)
- [AstrBot 框架](https://github.com/Soulter/AstrBot)

---

**注意**: 本插件非官方插件，与 MCC Island 官方无关。使用时请遵守 MCC Island API 的使用条款。
