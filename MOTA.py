import pygame
import random
import sys
import math
from collections import deque

# -------- 常量设置 --------
COLOR_BUTTON = (90, 90, 90)  # 开场按钮
COLOR_BUTTON_HOVER = (120, 120, 120)
COLOR_UI_TEXT = (200, 160, 60)
COLOR_DEATH_RED = (139, 0, 0)

SIDEBAR_WIDTH = 300  # 右侧属性栏宽度

TILE_SIZE = 35
MAP_WIDTH = 37  # 必须为奇数，方便生成迷宫
MAP_HEIGHT = 37

# 屏幕尺寸
CONFIG = {
    "SCREEN_WIDTH": MAP_WIDTH * TILE_SIZE + 2 * SIDEBAR_WIDTH,
    "SCREEN_HEIGHT": MAP_HEIGHT * TILE_SIZE,
    "TILE_SIZE": TILE_SIZE,
    "MAP_WIDTH": MAP_WIDTH,
    "MAP_HEIGHT": MAP_HEIGHT
}

# 在常量设置中增加消息日志区域的高度
SCREEN_WIDTH = MAP_WIDTH * TILE_SIZE + 2 * SIDEBAR_WIDTH
SCREEN_HEIGHT = MAP_HEIGHT * TILE_SIZE  # 增加窗口高度

# 颜色定义
# 墙壁相关颜色
COLOR_STONE = (40, 40, 40)  # 基础石墙颜色
COLOR_MOSS = (34, 139, 34)  # 青苔颜色
COLOR_CRACK = (80, 80, 80)  # 裂缝颜色
COLOR_HIGHLIGHT = (90, 90, 90)  # 石墙高光
COLOR_SHADOW = (20, 20, 20)  # 石墙阴影

COLOR_FLOOR_CRACK = (180, 180, 180, 60)  # 半透明裂缝颜色
COLOR_FLOOR_STONE = (200, 200, 200, 40)  # 石块边缘颜色

COLOR_ICE = (175, 238, 238)  # 冰颜色
COLOR_POISON = (50, 205, 50)  # 毒液颜色

COLOR_WALL = (0, 0, 0)
COLOR_FLOOR = (150, 150, 150)
COLOR_PLAYER = (0, 255, 0)
COLOR_MONSTER = (255, 0, 0)
COLOR_CHEST = (255, 215, 0)
COLOR_EXIT = (0, 0, 255)
COLOR_TEXT = (255, 255, 255)
COLOR_HP = (255, 0, 0)
COLOR_ATK = (255, 165, 0)
COLOR_DEF = (0, 255, 255)

# -------- 怪物追踪系统设置 --------
MONSTER_DISTANCE = 6                  # 怪物追踪距离
MONSTER_TRACKING_DURATION = 10.0       # 追踪持续时间(秒)
MONSTER_PATH_UPDATE_RATE = 1.0        # 路径更新频率(秒)
MONSTER_TRACKING_INDICATORS = True    # 是否显示追踪指示器
MONSTER_PATH_VISUALIZATION = True     # 是否显示路径可视化
MONSTER_DEBUG_INFO = False            # 是否显示调试信息

MAX_ROOM = 6
MAX_ROOM_SIZE = 19

# 路径效果

PATHTIME = 0.35 # 路径显示时长 秒
ORDINARYEFFECT = True
LIGHTNINGEFFECT_RED = False
LIGHTNINGEFFECT_YELLOW = False
LIGHTNINGEFFECT_BLUE = False

# 怪物强度参数
S_MONSTER = 2

N = 5
# 普通怪物数目范围
MONSTER_MIN = math.ceil(N)
MONSTER_MAX = math.ceil(N * 8)

# 喷泉相关参数
FOUNTAIN_ROOM_PROB = 0.2  # 20%概率生成喷泉房间
FOUNTAIN_SPAWN_INTERVAL = 2000  # 2秒生成一次史莱姆（毫秒

# 岩浆房
LAVA_ROOM_PROB = 0.2  # 岩浆房间生成概率
LAVA_SPAWN_INTERVAL = 2500  # 2.5秒生成一次怪物
LAVA_DAMAGE = 80      # 岩浆每秒伤害

M = 4
# 道具数目范围
ITEM_MIN = math.ceil(8)
ITEM_MAX = math.ceil(M * 8)

# 普通怪物权重
MONSTER_WEIGHT = [10, 10, 5, 5, 5, 12, 16, 12, 8, 6, 5, 5, 8, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1]

# 怪物列表，每个怪物的属性
monsters_data = [
    # 基础怪物
    {"name": "蝙蝠", "HP": 50, "ATK": 20, "DEF": 5, "size": (1, 1),
     "attack_range": 1, "attack_speed": 1.0, "coin": 20, "speed": 5, "level": 1},
    {"name": "白色蝙蝠", "HP": 55, "ATK": 22, "DEF": 6, "size": (1, 1),
     "attack_range": 1, "attack_speed": 1.2, "coin": 22, "speed": 4, "level": 1},
    {"name": "腐蚀怪", "HP": 200, "ATK": 40, "DEF": 15, "size": (1, 1),
     "attack_range": 1, "attack_speed": 0.8, "coin": 50, "speed": 15, "level": 2},
    {"name": "火焰骑士", "HP": 250, "ATK": 35, "DEF": 30, "size": (1, 1),
     "attack_range": 1, "attack_speed": 1.0, "coin": 50, "speed": 18, "level": 3},
    {"name": "纯火焰骑士", "HP": 300, "ATK": 40, "DEF": 35, "size": (1, 1),
     "attack_range": 1, "attack_speed": 1.2, "coin": 55, "speed": 15, "level": 4},
    {"name": "骷髅", "HP": 100, "ATK": 30, "DEF": 10, "size": (1, 2),
     "attack_range": 1, "attack_speed": 0.8, "coin": 35, "speed": 25, "level": 1},
    {"name": "史莱姆", "HP": 80, "ATK": 25, "DEF": 8, "size": (1, 1),
     "attack_range": 1, "attack_speed": 1.0, "coin": 25, "speed": 20, "level": 1},
    {"name": "红史莱姆", "HP": 160, "ATK": 35, "DEF": 12, "size": (1, 1),
     "attack_range": 1, "attack_speed": 1.2, "coin": 45, "speed": 25, "level": 2},
    {"name": "黑史莱姆", "HP": 240, "ATK": 45, "DEF": 16, "size": (1, 1),
     "attack_range": 1, "attack_speed": 1.5, "coin": 60, "speed": 30, "level": 3},
    {"name": "闪光史莱姆", "HP": 280, "ATK": 55, "DEF": 30, "size": (1, 1),
     "attack_range": 1, "attack_speed": 1.8, "coin": 90, "speed": 20, "level": 4},
    {"name": "电击球", "HP": 200, "ATK": 40, "DEF": 15, "size": (1, 1),
     "attack_range": 2, "attack_speed": 0.8, "coin": 50, "speed": 4, "level": 2},
    {"name": "异色电击球", "HP": 220, "ATK": 44, "DEF": 18, "size": (1, 1),
     "attack_range": 2, "attack_speed": 1.0, "coin": 55, "speed": 4, "level": 2},
    {"name": "魔法师", "HP": 120, "ATK": 35, "DEF": 12, "size": (1, 2),
     "attack_range": 3, "attack_speed": 0.6, "coin": 60, "speed": 35, "level": 3},
    {"name": "魔王", "HP": 1000, "ATK": 50, "DEF": 20, "size": (2, 2),
     "attack_range": 2, "attack_speed": 0.5, "coin": 300, "speed": 50, "level": 5},
    {"name": "圣洁魔王", "HP": 1100, "ATK": 55, "DEF": 22, "size": (2, 2),
     "attack_range": 2, "attack_speed": 0.6, "coin": 330, "speed": 45, "level": 6},
    {"name": "普通巨龙", "HP": 5000, "ATK": 110, "DEF": 50, "size": (3, 3),
     "attack_range": 2, "attack_speed": 0.4, "coin": 1200, "speed": 60, "level": 6},
    {"name": "冰霜巨龙", "HP": 5500, "ATK": 130, "DEF": 55, "size": (3, 3),
     "attack_range": 3, "attack_speed": 0.5, "coin": 1300, "speed": 60, "level": 7},
    {"name": "血腥闪电", "HP": 6000, "ATK": 200, "DEF": 110, "size": (3, 3),
     "attack_range": 4, "attack_speed": 0.3, "coin": 1500, "speed": 30, "level": 7},
    {"name": "纯青闪电", "HP": 7000, "ATK": 300, "DEF": 130, "size": (3, 3),
     "attack_range": 4, "attack_speed": 0.4, "coin": 2000, "speed": 30, "level": 8},
    {"name": "金色闪电", "HP": 8000, "ATK": 400, "DEF": 150, "size": (3, 3),
     "attack_range": 4, "attack_speed": 0.5, "coin": 2500, "speed": 30, "level": 9},
    {"name": "火焰领主", "HP": 6500, "ATK": 130, "DEF": 60, "size": (3, 3),
     "attack_range": 3, "attack_speed": 0.6, "coin": 1500, "speed": 60, "level": 8},
    {"name": "纯火焰领主", "HP": 7500, "ATK": 180, "DEF": 80, "size": (3, 3),
     "attack_range": 3, "attack_speed": 0.7, "coin": 1900, "speed": 50, "level": 9},
    {"name": "神圣灾祸骑士", "HP": 10000, "ATK": 250, "DEF": 180, "size": (3, 3),
     "attack_range": 7, "attack_speed": 0.7, "coin": 3000, "speed": 40, "level": 9, "num_balls": 6}
]

# 道具类型
ITEM_TYPES = ["CHEST", "HP_SMALL", "HP_LARGE", "MP_SMALL", "MP_LARGE", "ATK_GEM", "DEF_GEM", "ATK_GEM_LARGE", "DEF_GEM_LARGE"]


EQUIPMENT_TYPES = {
    # 武器列表
    "WOOD_SWORD": {
        "tag": "WOOD_SWORD",
        "name": "木剑",
        "type": "weapon",
        "atk": 5,
        "multiple": 1,
        "attack_speed": 1.2,  # 攻击速度（次/秒）
        "attack_range": 1,     # 攻击范围（格）
        "durability": 20       # 耐久度
    },
    "BRONZE_DAGGER": {
        "tag": "BRONZE_DAGGER",
        "name": "青铜匕首",
        "type": "weapon",
        "atk": 8,
        "multiple": 1.1,
        "attack_speed": 1.5,  # 快速攻击
        "attack_range": 1,    # 近战
        "durability": 30
    },
    "STEEL_DAGGER": {
        "tag": "STEEL_DAGGER",
        "name": "钢匕首",
        "type": "weapon",
        "atk": 12,
        "multiple": 1.2,
        "attack_speed": 1.8,  # 更快攻击
        "attack_range": 1,    # 近战
        "durability": 40
    },
    "COPPER_SWORD": {
        "tag": "COPPER_SWORD",
        "name": "铜剑",
        "type": "weapon",
        "atk": 15,
        "multiple": 1.1,
        "attack_speed": 1.0,  # 标准攻击速度
        "attack_range": 1,    # 近战
        "durability": 50
    },
    "IRON_SWORD": {
        "tag": "IRON_SWORD",
        "name": "铁剑",
        "type": "weapon",
        "atk": 20,
        "multiple": 1.2,
        "attack_speed": 1.0,  # 标准攻击速度
        "attack_range": 1,    # 近战
        "durability": 60
    },
    "FINE_STEEL_DAGGER": {
        "tag": "FINE_STEEL_DAGGER",
        "name": "精钢匕首",
        "type": "weapon",
        "atk": 25,
        "multiple": 1.3,
        "attack_speed": 2.0,  # 极快攻击
        "attack_range": 1,    # 近战
        "durability": 70
    },
    "FINE_IRON_SWORD": {
        "tag": "FINE_IRON_SWORD",
        "name": "精铁长剑",
        "type": "weapon",
        "atk": 30,
        "multiple": 1.3,
        "attack_speed": 0.9,  # 稍慢但威力大
        "attack_range": 1,    # 近战
        "durability": 80
    },
    "GUTS_GREATSWORD": {
        "tag": "GUTS_GREATSWORD",
        "name": "格斯大剑",
        "type": "weapon",
        "atk": 50,
        "multiple": 1.5,
        "attack_speed": 0.6,  # 慢速重击
        "attack_range": 1,    # 近战
        "durability": 100
    },
    "LONG_SPEAR": {
        "tag": "LONG_SPEAR",
        "name": "长矛",
        "type": "weapon",
        "atk": 18,
        "multiple": 1.2,
        "attack_speed": 0.8,  # 较慢
        "attack_range": 2,    # 远程攻击
        "durability": 50
    },
    "CROSSBOW": {
        "tag": "CROSSBOW",
        "name": "弩",
        "type": "weapon",
        "atk": 22,
        "multiple": 1.3,
        "attack_speed": 0.5,  # 慢速
        "attack_range": 3,    # 远程攻击
        "durability": 40
    },

    # 护甲列表（保持不变）
    "WOOD_ARMOR": {
        "tag": "WOOD_ARMOR",
        "name": "木甲",
        "type": "armor",
        "def": 5,
        "multiple": 1,
        "durability": 30
    },
    "COPPER_ARMOR": {
        "tag": "COPPER_ARMOR",
        "name": "铜甲",
        "type": "armor",
        "def": 10,
        "multiple": 1.1,
        "durability": 50
    },
    "IRON_ARMOR": {
        "tag": "IRON_ARMOR",
        "name": "铁甲",
        "type": "armor",
        "def": 15,
        "multiple": 1.2,
        "durability": 70
    },
    "STEEL_ARMOR": {
        "tag": "STEEL_ARMOR",
        "name": "钢甲",
        "type": "armor",
        "def": 20,
        "multiple": 1.3,
        "durability": 90
    },
    "LIGHTNING_ARMOR_RED": {
        "tag": "LIGHTNING_ARMOR_RED",
        "name": "红闪电甲",
        "type": "armor",
        "def": 30,
        "multiple": 1.4,
        "durability": 110
    },
    "LIGHTNING_ARMOR_BLUE": {
        "tag": "LIGHTNING_ARMOR_BLUE",
        "name": "蓝闪电甲",
        "type": "armor",
        "def": 30,
        "multiple": 1.4,
        "durability": 110
    },
    "LIGHTNING_ARMOR_YELLOW": {
        "tag": "LIGHTNING_ARMOR_YELLOW",
        "name": "黄闪电甲",
        "type": "armor",
        "def": 30,
        "multiple": 1.4,
        "durability": 110
    }
}


# -------- UI类 --------


class Encyclopedia:
    def __init__(self, screen, game):
        self.screen = screen
        self.game = game
        self.screen_width, self.screen_height = screen.get_size()

        # 获取全局常量
        global TILE_SIZE, MAP_WIDTH, MAP_HEIGHT
        self.TILE_SIZE = TILE_SIZE  # 直接存储为类属性
        self.EQUIPMENT_TYPES = EQUIPMENT_TYPES  # 存储装备类型数据

        # 图鉴页面设置 - 移除怪物页面
        self.page = 0  # 0 = 物品页, 1 = 武器页, 2 = 防具页
        self.max_pages = 3  # 减少为3页

        # 加载字体
        try:
            self.title_font = pygame.font.SysFont("SimHei", 36, bold=True)
            self.item_font = pygame.font.SysFont("SimHei", 20)
            self.desc_font = pygame.font.SysFont("SimSun", 18)
        except:
            # 回退到默认字体
            self.title_font = pygame.font.Font(None, 36)
            self.item_font = pygame.font.Font(None, 20)
            self.desc_font = pygame.font.Font(None, 18)

        # 颜色设置
        self.colors = {
            'bg': (20, 20, 30, 230),  # 背景色带透明度
            'border': (80, 80, 120),  # 边框色
            'title': (255, 215, 0),  # 标题金色
            'text': (220, 220, 220),  # 普通文本
            'highlight': (100, 150, 255),  # 高亮文本
            'button': (60, 60, 80),  # 按钮颜色
            'button_hover': (80, 80, 120),  # 按钮悬停颜色
            'item_bg': (40, 40, 60)  # 物品背景
        }

        # 网格设置
        self.grid_size = 70  # 每个格子大小
        self.grid_padding = 10  # 格子间隔
        self.grid_cols = 8  # 每行显示数量
        self.grid_rows = 4  # 每页行数

        # 详细信息框
        self.info_panel = {
            'visible': False,
            'item': None,
            'type': None  # 'item', 'weapon', 'armor'
        }

        # 模拟一个物品实例用于展示
        self.dummy_item = type('DummyItem', (), {'x': 0, 'y': 0, 'item_type': None, 'equipment_data': None})

        # 页面按钮
        self.buttons = self.create_buttons()

        # 鼠标状态
        self.hover_button = None
        self.hover_item = None

    def get_page_title(self):
        """获取当前页面的标题"""
        titles = ["消耗品图鉴", "武器图鉴", "防具图鉴"]
        return titles[self.page]

    def get_page_items(self):
        """获取当前页面应该显示的物品列表"""
        if self.page == 0:
            # 消耗品页面: HP药水, 宝石等
            return ["CHEST", "HP_SMALL", "HP_LARGE", "MP_SMALL", "MP_LARGE", "ATK_GEM", "DEF_GEM", "ATK_GEM_LARGE", "DEF_GEM_LARGE"]
        elif self.page == 1:
            # 武器页面
            return [key for key, data in self.EQUIPMENT_TYPES.items()
                    if data["type"] == "weapon"]
        elif self.page == 2:
            # 防具页面
            return [key for key, data in self.EQUIPMENT_TYPES.items()
                    if data["type"] == "armor"]

    def draw_item_in_cell(self, item_id, x, y, rect):
        # 设置物品坐标以便绘制
        center_x = rect.centerx
        center_y = rect.centery

        # 将 dummy_item 放置在适当位置
        self.dummy_item.x = center_x // self.TILE_SIZE
        self.dummy_item.y = center_y // self.TILE_SIZE

        if self.page == 0:  # 消耗品
            self.dummy_item.item_type = item_id
            self.dummy_item.equipment_data = None

            # 计算绘制偏移，使物品居中显示
            old_x, old_y = self.dummy_item.x, self.dummy_item.y
            self.dummy_item.x = center_x // self.TILE_SIZE
            self.dummy_item.y = center_y // self.TILE_SIZE

            # 使用game的绘制函数
            if item_id == "CHEST":
                # 调用游戏的宝箱绘制函数
                self.game.draw_chest(self.dummy_item)
            elif "HP_" in item_id or "MP_" in item_id:
                # 调用游戏的药水绘制函数
                self.game.draw_potion(self.dummy_item)
            elif "GEM" in item_id:
                # 调用游戏的宝石绘制函数
                self.game.draw_gem(self.dummy_item)

            # 恢复原始坐标
            self.dummy_item.x, self.dummy_item.y = old_x, old_y

        else:  # 武器或防具
            self.dummy_item.item_type = item_id
            self.dummy_item.equipment_data = self.EQUIPMENT_TYPES[item_id].copy()

            # 计算绘制偏移，使物品居中显示
            old_x, old_y = self.dummy_item.x, self.dummy_item.y
            self.dummy_item.x = center_x // self.TILE_SIZE
            self.dummy_item.y = center_y // self.TILE_SIZE

            # 使用game的绘制函数绘制装备
            self.game.draw_equipment(self.dummy_item)

            # 恢复原始坐标
            self.dummy_item.x, self.dummy_item.y = old_x, old_y

        # 在格子底部添加物品名称
        if self.page == 0:
            if item_id == "CHEST":
                name = "宝箱"
            elif item_id == "HP_SMALL":
                name = "小红药水"
            elif item_id == "HP_LARGE":
                name = "大红药水"
            elif item_id == "MP_SMALL":
                name = "小蓝药水"
            elif item_id == "MP_LARGE":
                name = "大蓝药水"
            elif item_id == "ATK_GEM":
                name = "攻击宝石"
            elif item_id == "DEF_GEM":
                name = "防御宝石"
            elif item_id == "ATK_GEM_LARGE":
                name = "大攻击宝石"
            elif item_id == "DEF_GEM_LARGE":
                name = "大防御宝石"
            else:
                name = item_id
        else:
            name = self.dummy_item.equipment_data['name']

        name_text = self.desc_font.render(name[:6] + ".." if len(name) > 6 else name,
                                          True, self.colors['text'])
        name_rect = name_text.get_rect(centerx=rect.centerx, bottom=rect.bottom - 2)
        self.screen.blit(name_text, name_rect)

    def draw_info_panel(self):
        """绘制详细信息面板"""
        if not self.info_panel['visible'] or not self.hover_item:
            return

        item_id = self.hover_item['id']

        # 设置面板尺寸和位置
        panel_width, panel_height = 300, 250
        panel_x = max(50, min(self.screen_width - panel_width - 50,
                              self.hover_item['rect'].right + 10))
        panel_y = max(100, min(self.screen_height - panel_height - 50,
                               self.hover_item['rect'].top))

        # 绘制面板背景
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, self.colors['bg'], panel_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.colors['border'], panel_rect, 2, border_radius=8)

        # 绘制物品信息
        self.draw_item_info(panel_rect, item_id)

    def draw_item_info(self, rect, item_id):
        """绘制物品详细信息"""
        if self.page == 0:  # 消耗品
            # 标题
            if item_id == "CHEST":
                title = "宝箱"
                desc = ["打开后获得随机金币"]
            elif item_id == "HP_SMALL":
                title = "小生命药水"
                desc = ["恢复少量生命值", "与楼层数相关"]
            elif item_id == "HP_LARGE":
                title = "大生命药水"
                desc = ["恢复大量生命值", "与楼层数相关"]
            elif item_id == "MP_SMALL":
                title = "小魔法药水"
                desc = ["恢复少量魔法值", "与楼层数相关"]
            elif item_id == "MP_LARGE":
                title = "大魔法药水"
                desc = ["恢复大量魔法值", "与楼层数相关"]
            elif item_id == "ATK_GEM":
                title = "攻击宝石"
                desc = ["提升攻击力", "与楼层数相关"]
            elif item_id == "DEF_GEM":
                title = "防御宝石"
                desc = ["提升防御力", "与楼层数相关"]
            elif item_id == "ATK_GEM_LARGE":
                title = "大攻击宝石"
                desc = ["大幅提升攻击力", "与楼层数相关"]
            elif item_id == "DEF_GEM_LARGE":
                title = "大防御宝石"
                desc = ["大幅提升防御力", "与楼层数相关"]
            else:
                title = item_id
                desc = ["未知物品"]
        else:  # 武器或防具
            equipment_data = self.EQUIPMENT_TYPES[item_id]
            title = equipment_data['name']

            if equipment_data['type'] == 'weapon':
                desc = [
                    f"类型: 武器",
                    f"攻击力: +{equipment_data['atk']}",
                    f"攻击倍率: x{equipment_data['multiple']}",
                    f"攻击速度: {equipment_data['attack_speed']} 次/秒",
                    f"攻击范围: {equipment_data['attack_range']} 格",
                    f"耐久度: {equipment_data['durability']}"
                ]
            else:  # armor
                desc = [
                    f"类型: 防具",
                    f"防御力: +{equipment_data['def']}",
                    f"防御倍率: x{equipment_data['multiple']}",
                    f"耐久度: {equipment_data['durability']}"
                ]

        # 绘制标题
        title_text = self.item_font.render(title, True, self.colors['title'])
        title_rect = title_text.get_rect(centerx=rect.centerx, top=rect.top + 10)
        self.screen.blit(title_text, title_rect)

        # 分隔线
        pygame.draw.line(self.screen, self.colors['border'],
                         (rect.left + 20, title_rect.bottom + 5),
                         (rect.right - 20, title_rect.bottom + 5), 2)

        # 绘制描述
        y = title_rect.bottom + 20
        for line in desc:
            text = self.desc_font.render(line, True, self.colors['text'])
            self.screen.blit(text, (rect.left + 30, y))
            y += 25

    def create_buttons(self):
        """创建导航按钮"""
        buttons = []

        # 左右翻页按钮
        btn_width, btn_height = 100, 40

        # 上一页按钮
        prev_btn = {
            'rect': pygame.Rect(50, self.screen_height - 70, btn_width, btn_height),
            'text': "上一页",
            'action': self.prev_page,
            'hover': False
        }
        buttons.append(prev_btn)

        # 下一页按钮
        next_btn = {
            'rect': pygame.Rect(self.screen_width - 150, self.screen_height - 70, btn_width, btn_height),
            'text': "下一页",
            'action': self.next_page,
            'hover': False
        }
        buttons.append(next_btn)

        # 返回按钮
        exit_btn = {
            'rect': pygame.Rect(self.screen_width // 2 - 50, self.screen_height - 70, btn_width, btn_height),
            'text': "关闭",
            'action': self.close,
            'hover': False
        }
        buttons.append(exit_btn)

        return buttons

    def prev_page(self):
        """切换到上一页"""
        self.page = (self.page - 1) % self.max_pages
        self.info_panel['visible'] = False
        return True

    def next_page(self):
        """切换到下一页"""
        self.page = (self.page + 1) % self.max_pages
        self.info_panel['visible'] = False
        return True

    def close(self):
        """关闭图鉴"""
        return False

    def draw_buttons(self):
        """绘制界面按钮"""
        self.hover_button = None
        mouse_pos = pygame.mouse.get_pos()

        for btn in self.buttons:
            # 检查悬停状态
            btn['hover'] = btn['rect'].collidepoint(mouse_pos)
            if btn['hover']:
                self.hover_button = btn

            # 绘制按钮
            btn_color = self.colors['button_hover'] if btn['hover'] else self.colors['button']
            pygame.draw.rect(self.screen, btn_color, btn['rect'], border_radius=5)
            pygame.draw.rect(self.screen, self.colors['border'], btn['rect'], 2, border_radius=5)

            # 文本
            text = self.item_font.render(btn['text'], True, self.colors['text'])
            text_rect = text.get_rect(center=btn['rect'].center)
            self.screen.blit(text, text_rect)

    def draw_item_grid(self, items):
        """绘制物品网格"""
        start_x = (self.screen_width - (self.grid_size + self.grid_padding) * self.grid_cols) // 2
        start_y = 100  # 从顶部留出空间给标题

        for i, item_id in enumerate(items):
            row = i // self.grid_cols
            col = i % self.grid_cols

            if row >= self.grid_rows:
                continue  # 超过当前页显示数量

            # 计算格子位置
            x = start_x + col * (self.grid_size + self.grid_padding)
            y = start_y + row * (self.grid_size + self.grid_padding)

            # 绘制格子背景
            cell_rect = pygame.Rect(x, y, self.grid_size, self.grid_size)
            hover = cell_rect.collidepoint(pygame.mouse.get_pos())

            # 背景颜色根据悬停状态变化
            bg_color = self.colors['button_hover'] if hover else self.colors['item_bg']
            pygame.draw.rect(self.screen, bg_color, cell_rect, border_radius=5)
            pygame.draw.rect(self.screen, self.colors['border'], cell_rect, 2, border_radius=5)

            # 绘制物品
            self.draw_item_in_cell(item_id, x, y, cell_rect)

            # 存储悬停物品
            if hover:
                self.hover_item = {
                    'id': item_id,
                    'rect': cell_rect,
                    'type': 'item'
                }

    def draw(self):
        """绘制整个图鉴界面"""
        # 半透明遮罩层
        overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        # 主面板背景
        panel_width, panel_height = self.screen_width - 100, self.screen_height - 100
        panel_rect = pygame.Rect(50, 50, panel_width, panel_height)
        pygame.draw.rect(self.screen, self.colors['bg'], panel_rect, border_radius=10)
        pygame.draw.rect(self.screen, self.colors['border'], panel_rect, 3, border_radius=10)

        # 标题
        title_text = self.title_font.render(self.get_page_title(), True, self.colors['title'])
        title_rect = title_text.get_rect(centerx=self.screen_width // 2, top=60)
        self.screen.blit(title_text, title_rect)

        # 绘制物品网格
        self.hover_item = None
        self.draw_item_grid(self.get_page_items())

        # 绘制按钮
        self.draw_buttons()

        # 如果鼠标悬停在物品上，显示详细信息
        if self.hover_item:
            self.info_panel['visible'] = True
            self.draw_info_panel()
        else:
            self.info_panel['visible'] = False

        # 页码指示器
        page_text = self.desc_font.render(f"{self.page + 1}/{self.max_pages}", True, self.colors['text'])
        page_rect = page_text.get_rect(centerx=self.screen_width // 2, bottom=self.screen_height - 30)
        self.screen.blit(page_text, page_rect)

        pygame.display.flip()

    def handle_event(self, event):
        """处理事件"""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # 点击按钮
            if self.hover_button:
                return self.hover_button['action']()

        return True  # 继续运行图鉴界面

    def run(self):
        """运行图鉴界面"""
        running = True
        clock = pygame.time.Clock()

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_n:
                        return  # 关闭图鉴
                else:
                    # 其他事件处理
                    result = self.handle_event(event)
                    if result is False:
                        return

            # 绘制界面
            self.draw()

            # 控制帧率
            clock.tick(60)


class SettingsMenu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        # 颜色方案
        self.colors = {
            'background': (25, 25, 35),  # 深色背景
            'panel': (35, 35, 45),  # 面板背景
            'panel_border': (60, 60, 80),  # 面板边框
            'text': (220, 220, 220),  # 文字颜色
            'title': (255, 215, 0),  # 标题颜色
            'slider_bg': (50, 50, 70),  # 滑动条背景
            'slider_handle': (100, 150, 255),  # 滑动条把手
            'slider_active': (120, 170, 255),  # 滑动条激活颜色
            'button': (60, 60, 80),  # 按钮背景
            'button_hover': (80, 80, 100),  # 按钮悬停
            'button_border': (100, 100, 120),  # 按钮边框
            'button_text': (220, 220, 220),  # 按钮文字
            'accent': (100, 150, 255),  # 强调色
            'section': (210, 180, 140)  # 分区标题颜色
        }

        # 字体设置 - 使用系统中文字体
        try:
            self.title_font = pygame.font.SysFont("SimHei", 42, bold=True)
            self.section_font = pygame.font.SysFont("SimHei", 32, bold=True)
            self.label_font = pygame.font.SysFont("SimHei", 28)
            self.button_font = pygame.font.SysFont("SimHei", 32)
        except:
            # 尝试其他中文字体
            try:
                self.title_font = pygame.font.SysFont("Microsoft YaHei", 42, bold=True)
                self.section_font = pygame.font.SysFont("Microsoft YaHei", 32, bold=True)
                self.label_font = pygame.font.SysFont("Microsoft YaHei", 28)
                self.button_font = pygame.font.SysFont("Microsoft YaHei", 32)
            except:
                # 最后尝试系统默认字体
                self.title_font = pygame.font.Font(None, 42)
                self.section_font = pygame.font.Font(None, 32)
                self.label_font = pygame.font.Font(None, 28)
                self.button_font = pygame.font.Font(None, 32)
                print("警告: 未能加载中文字体，将使用默认字体")

        # 布局参数
        panel_width = 700  # 增加宽度以容纳更多滑动条
        panel_height = 1000  # 进一步增加高度以避免按钮与滑动条重合
        self.panel_rect = pygame.Rect(
            (self.screen_width - panel_width) // 2,
            (self.screen_height - panel_height) // 2,
            panel_width, panel_height
        )

        # 滑动条设置
        slider_width = 400
        slider_height = 8
        slider_y_start = self.panel_rect.top + 120
        slider_spacing = 90  # 进一步增加滑动条之间的垂直间距

        # 第一个分区 - 地图设置
        map_section_y = slider_y_start

        self.sliders = [
            {
                "label": "地图宽度",
                "value": CONFIG["MAP_WIDTH"],
                "min": 21, "max": 51,
                "step": 2,  # 确保总是奇数
                "rect": pygame.Rect(
                    self.panel_rect.centerx - slider_width // 2,
                    map_section_y,
                    slider_width, slider_height
                ),
                "hover": False,
                "tooltip": "设置地图的宽度 (格子数)",
                "section": "地图设置"
            },
            {
                "label": "地图高度",
                "value": CONFIG["MAP_HEIGHT"],
                "min": 21, "max": 51,
                "step": 2,  # 确保总是奇数
                "rect": pygame.Rect(
                    self.panel_rect.centerx - slider_width // 2,
                    map_section_y + slider_spacing,
                    slider_width, slider_height
                ),
                "hover": False,
                "tooltip": "设置地图的高度 (格子数)",
                "section": "地图设置"
            },
            {
                "label": "方块大小",
                "value": CONFIG["TILE_SIZE"],
                "min": 20, "max": 80,
                "step": 1,
                "rect": pygame.Rect(
                    self.panel_rect.centerx - slider_width // 2,
                    map_section_y + slider_spacing * 2,
                    slider_width, slider_height
                ),
                "hover": False,
                "tooltip": "设置每个方块的像素大小",
                "section": "地图设置"
            },

        # 第二个分区 - 游戏难度设置
            {
                "label": "怪物追踪距离",
                "value": MONSTER_DISTANCE,
                "min": 3, "max": 10,
                "step": 1,
                "rect": pygame.Rect(
                    self.panel_rect.centerx - slider_width // 2,
                    map_section_y + slider_spacing * 3 + 60,  # 额外间距用于分区标题
                    slider_width, slider_height
                ),
                "hover": False,
                "tooltip": "设置怪物开始追踪玩家的距离",
                "section": "游戏难度设置"
            },
            {
                "label": "怪物追踪持续时间",
                "value": MONSTER_TRACKING_DURATION,
                "min": 2.0, "max": 10.0,
                "step": 0.5,
                "rect": pygame.Rect(
                    self.panel_rect.centerx - slider_width // 2,
                    map_section_y + slider_spacing * 4 + 60,
                    slider_width, slider_height
                ),
                "hover": False,
                "tooltip": "设置怪物丢失目标后继续追踪的时间(秒)",
                "section": "游戏难度设置"
            },
            {
                "label": "怪物生成数目",
                "value": N,
                "min": 1, "max": 10,
                "step": 1,
                "rect": pygame.Rect(
                    self.panel_rect.centerx - slider_width // 2,
                    map_section_y + slider_spacing * 5 + 60,
                    slider_width, slider_height
                ),
                "hover": False,
                "tooltip": "设置每层生成的怪物数量基数 (影响最小/最大值)",
                "section": "游戏难度设置"
            },
            {
                "label": "道具生成数目",
                "value": M,
                "min": 2, "max": 8,
                "step": 1,
                "rect": pygame.Rect(
                    self.panel_rect.centerx - slider_width // 2,
                    map_section_y + slider_spacing * 6 + 60,
                    slider_width, slider_height
                ),
                "hover": False,
                "tooltip": "设置每层生成的道具数量基数 (影响最小/最大值)",
                "section": "游戏难度设置"
            }
        ]

        # 找出所有不同的分区
        self.sections = []
        for slider in self.sliders:
            if slider["section"] not in self.sections:
                self.sections.append(slider["section"])

        # 按钮设置
        button_width = 180
        button_height = 60
        button_y = self.panel_rect.bottom - 120  # 进一步下移按钮位置，远离最后一个滑动条

        self.back_button = {
            'rect': pygame.Rect(
                self.panel_rect.centerx - button_width - 20,
                button_y,
                button_width, button_height
            ),
            'text': "返回",
            'hover': False,
            'active': False
        }

        self.apply_button = {
            'rect': pygame.Rect(
                self.panel_rect.centerx + 20,
                button_y,
                button_width, button_height
            ),
            'text': "应用",
            'hover': False,
            'active': False
        }

        # 拖动状态
        self.dragging = None

        # 动画效果
        self.animation_time = 0
        self.show_tooltip = False
        self.tooltip_text = ""
        self.tooltip_pos = (0, 0)

        # 创建背景图案
        self.background_pattern = self.create_background_pattern()

    def create_background_pattern(self):
        """创建美观的背景图案"""
        pattern_size = 100
        pattern = pygame.Surface((pattern_size, pattern_size), pygame.SRCALPHA)

        # 背景底色
        pattern.fill(self.colors['background'])

        # 添加微妙的格子线条
        for i in range(0, pattern_size, 20):
            pygame.draw.line(pattern, (40, 40, 50, 30), (0, i), (pattern_size, i), 1)
            pygame.draw.line(pattern, (40, 40, 50, 30), (i, 0), (i, pattern_size), 1)

        # 添加点缀
        for _ in range(3):
            x = random.randint(0, pattern_size)
            y = random.randint(0, pattern_size)
            pygame.draw.circle(pattern, (60, 60, 80, 20), (x, y), random.randint(2, 5))

        return pattern

    def draw_slider(self, slider):
        """绘制精美的滑动条"""
        # 滑动条背景
        pygame.draw.rect(self.screen, self.colors['slider_bg'], slider["rect"], border_radius=4)

        # 滑动条激活部分
        ratio = (slider["value"] - slider["min"]) / (slider["max"] - slider["min"])
        active_width = int(slider["rect"].width * ratio)
        active_rect = pygame.Rect(
            slider["rect"].x, slider["rect"].y,
            active_width, slider["rect"].height
        )
        pygame.draw.rect(self.screen, self.colors['accent'], active_rect, border_radius=4)

        # 滑动条把手
        handle_x = slider["rect"].x + active_width - 8
        handle_y = slider["rect"].y - 12
        handle_rect = pygame.Rect(handle_x, handle_y, 16, 32)

        # 把手发光效果
        if slider["hover"] or self.dragging == self.sliders.index(slider):
            glow = pygame.Surface((40, 40), pygame.SRCALPHA)
            pygame.draw.circle(glow, (*self.colors['slider_active'], 50), (20, 20), 15)
            self.screen.blit(glow, (handle_rect.centerx - 20, handle_rect.centery - 20))

        # 绘制把手
        handle_color = self.colors['slider_active'] if slider["hover"] or self.dragging == self.sliders.index(
            slider) else self.colors['slider_handle']
        pygame.draw.rect(self.screen, handle_color, handle_rect, border_radius=8)

        # 高光效果
        if slider["hover"] or self.dragging == self.sliders.index(slider):
            highlight = pygame.Surface((12, 28), pygame.SRCALPHA)
            highlight_rect = pygame.Rect(0, 0, 12, 28)
            pygame.draw.rect(highlight, (255, 255, 255, 50), highlight_rect, border_radius=6)
            self.screen.blit(highlight, (handle_x + 2, handle_y + 2))

        # 绘制标签
        label = self.label_font.render(f"{slider['label']}", True, self.colors['text'])
        self.screen.blit(label, (slider["rect"].x, slider["rect"].y - 40))

        # 绘制数值
        value_text = self.label_font.render(f"{slider['value']}", True, self.colors['accent'])
        self.screen.blit(value_text, (slider["rect"].right - value_text.get_width(), slider["rect"].y - 40))

    def draw_button(self, button):
        """绘制精美的按钮"""
        # 按钮背景
        button_color = self.colors['button_hover'] if button['hover'] else self.colors['button']
        if button['active']:
            # 按下效果
            button_rect = pygame.Rect(button['rect'].x, button['rect'].y + 2, button['rect'].width,
                                      button['rect'].height)
        else:
            button_rect = button['rect']

        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=10)

        # 按钮边框
        pygame.draw.rect(self.screen, self.colors['button_border'], button_rect, 2, border_radius=10)

        # 按钮文字
        text = self.button_font.render(button['text'], True, self.colors['button_text'])
        text_rect = text.get_rect(center=button_rect.center)
        self.screen.blit(text, text_rect)

        # 按钮悬停效果
        if button['hover'] and not button['active']:
            # 微妙的光晕
            glow = pygame.Surface((button_rect.width + 20, button_rect.height + 20), pygame.SRCALPHA)
            pygame.draw.rect(glow, (*self.colors['accent'], 30),
                             (10, 10, button_rect.width, button_rect.height),
                             border_radius=10)
            self.screen.blit(glow,
                             (button_rect.x - 10, button_rect.y - 10))

    def draw_tooltip(self):
        """绘制工具提示"""
        if not self.show_tooltip:
            return

        # 工具提示背景
        text = self.label_font.render(self.tooltip_text, True, self.colors['text'])
        padding = 10
        tooltip_rect = pygame.Rect(
            self.tooltip_pos[0], self.tooltip_pos[1],
            text.get_width() + padding * 2, text.get_height() + padding * 2
        )

        # 确保工具提示在屏幕内
        if tooltip_rect.right > self.screen_width:
            tooltip_rect.right = self.screen_width - 5
        if tooltip_rect.bottom > self.screen_height:
            tooltip_rect.bottom = self.screen_height - 5

        # 绘制背景
        pygame.draw.rect(self.screen, (40, 40, 50, 230), tooltip_rect, border_radius=5)
        pygame.draw.rect(self.screen, self.colors['panel_border'], tooltip_rect, 1, border_radius=5)

        # 绘制文字
        self.screen.blit(text, (tooltip_rect.x + padding, tooltip_rect.y + padding))

    def draw(self):
        """绘制整个设置界面"""
        # 填充背景
        for y in range(0, self.screen_height, 100):
            for x in range(0, self.screen_width, 100):
                self.screen.blit(self.background_pattern, (x, y))

        # 半透明中央面板
        panel_surface = pygame.Surface((self.panel_rect.width, self.panel_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (*self.colors['panel'], 250),
                         (0, 0, self.panel_rect.width, self.panel_rect.height),
                         border_radius=15)

        # 面板边框
        pygame.draw.rect(panel_surface, self.colors['panel_border'],
                         (0, 0, self.panel_rect.width, self.panel_rect.height),
                         2, border_radius=15)

        # 面板顶部装饰
        pygame.draw.rect(panel_surface, self.colors['accent'],
                         (20, 0, self.panel_rect.width - 40, 5),
                         border_radius=2)

        self.screen.blit(panel_surface, self.panel_rect.topleft)

        # 标题
        title = self.title_font.render("游戏设置", True, self.colors['title'])
        title_rect = title.get_rect(centerx=self.panel_rect.centerx, top=self.panel_rect.top + 30)
        self.screen.blit(title, title_rect)

        # 分隔线
        pygame.draw.line(self.screen, self.colors['panel_border'],
                         (self.panel_rect.left + 40, title_rect.bottom + 20),
                         (self.panel_rect.right - 40, title_rect.bottom + 20),
                         2)

        # 绘制分区标题和滑动条
        current_section = ""
        for slider in self.sliders:
            # 如果到了新的分区，绘制分区标题
            if slider["section"] != current_section:
                current_section = slider["section"]

                # 计算分区标题位置（放在第一个该分区滑动条的上方）
                section_y = slider["rect"].y - 80

                # 绘制分区标题
                section_text = self.section_font.render(current_section, True, self.colors['section'])
                self.screen.blit(section_text, (self.panel_rect.left + 40, section_y))

                # 分区下方的短分隔线
                pygame.draw.line(self.screen, self.colors['section'],
                                 (self.panel_rect.left + 40, section_y + 35),
                                 (self.panel_rect.left + 40 + section_text.get_width(), section_y + 35),
                                 1)

            # 绘制滑动条
            self.draw_slider(slider)

        # 绘制按钮
        self.draw_button(self.back_button)
        self.draw_button(self.apply_button)

        # 绘制工具提示
        self.draw_tooltip()

        # 更新显示
        pygame.display.flip()

    def update(self, dt):
        self.animation_time += dt

        # 更新按钮悬停状态
        mouse_pos = pygame.mouse.get_pos()
        self.back_button['hover'] = self.back_button['rect'].collidepoint(mouse_pos)
        self.apply_button['hover'] = self.apply_button['rect'].collidepoint(mouse_pos)

        # 更新滑动条悬停状态
        self.show_tooltip = False
        for slider in self.sliders:
            # 检查把手区域
            handle_x = slider["rect"].x + int(slider["rect"].width *
                                              ((slider["value"] - slider["min"]) /
                                               (slider["max"] - slider["min"]))) - 8
            handle_y = slider["rect"].y - 12
            handle_rect = pygame.Rect(handle_x, handle_y, 16, 32)

            slider['hover'] = handle_rect.collidepoint(mouse_pos)

            # 检查是否显示工具提示
            label_rect = pygame.Rect(
                slider["rect"].x, slider["rect"].y - 40,
                slider["rect"].width, 40
            )
            if label_rect.collidepoint(mouse_pos) and 'tooltip' in slider:
                self.show_tooltip = True
                self.tooltip_text = slider['tooltip']
                self.tooltip_pos = (mouse_pos[0], mouse_pos[1] - 40)

    def handle_event(self, event):
        """处理用户输入事件"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # 左键点击
                # 检查滑动条
                for i, slider in enumerate(self.sliders):
                    # 检查把手区域
                    handle_x = slider["rect"].x + int(slider["rect"].width *
                                                      ((slider["value"] - slider["min"]) /
                                                       (slider["max"] - slider["min"]))) - 8
                    handle_y = slider["rect"].y - 12
                    handle_rect = pygame.Rect(handle_x, handle_y, 16, 32)

                    if handle_rect.collidepoint(event.pos):
                        self.dragging = i
                        break

                    # 如果点击了滑动条而不是把手，直接移动把手到点击位置
                    if slider["rect"].collidepoint(event.pos):
                        ratio = (event.pos[0] - slider["rect"].x) / slider["rect"].width
                        value = slider["min"] + ratio * (slider["max"] - slider["min"])
                        # 按步长取整
                        step = slider.get("step", 1)
                        slider["value"] = int(round(value / step) * step)
                        # 确保值在范围内
                        slider["value"] = max(slider["min"], min(slider["max"], slider["value"]))
                        self.dragging = i
                        break

                # 检查按钮
                if self.back_button['rect'].collidepoint(event.pos):
                    self.back_button['active'] = True
                    return "menu"

                if self.apply_button['rect'].collidepoint(event.pos):
                    self.apply_button['active'] = True

                    # 更新配置
                    global CONFIG, MONSTER_DISTANCE, N, M

                    # 地图设置
                    CONFIG["MAP_WIDTH"] = self.sliders[0]["value"]
                    CONFIG["MAP_HEIGHT"] = self.sliders[1]["value"]
                    CONFIG["TILE_SIZE"] = self.sliders[2]["value"]
                    CONFIG["SCREEN_WIDTH"] = CONFIG["MAP_WIDTH"] * CONFIG["TILE_SIZE"] + 2 * SIDEBAR_WIDTH
                    CONFIG["SCREEN_HEIGHT"] = CONFIG["MAP_HEIGHT"] * CONFIG["TILE_SIZE"]

                    # 游戏难度设置
                    MONSTER_DISTANCE = self.sliders[3]["value"]
                    N = self.sliders[4]["value"]
                    M = self.sliders[5]["value"]

                    return "apply"

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = None
            self.back_button['active'] = False
            self.apply_button['active'] = False

        elif event.type == pygame.MOUSEMOTION and self.dragging is not None:
            slider = self.sliders[self.dragging]
            # 计算新值
            ratio = (event.pos[0] - slider["rect"].x) / slider["rect"].width
            value = slider["min"] + ratio * (slider["max"] - slider["min"])
            # 按步长取整
            step = slider.get("step", 1)
            slider["value"] = int(round(value / step) * step)
            # 确保值在范围内
            slider["value"] = max(slider["min"], min(slider["max"], slider["value"]))

        return "settings"

    def run(self):
        """运行设置菜单循环"""
        clock = pygame.time.Clock()
        running = True

        while running:
            dt = clock.tick(60) / 1000  # 帧时间（秒）

            # 更新状态
            self.update(dt)

            # 处理事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                result = self.handle_event(event)
                if result != "settings":
                    return result

            # 绘制界面
            self.draw()

class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.screen_width, self.screen_height = screen.get_size()

        # 字体设置 - 使用系统字体以支持中文
        try:
            # 尝试使用系统中文字体
            self.font_title = pygame.font.SysFont("SimHei", 80, bold=True)  # 使用黑体
            self.font_button = pygame.font.SysFont("SimHei", 36)            # 同样使用黑体
        except:
            # 如果找不到中文字体，回退到默认字体
            self.font_title = pygame.font.Font(None, 80)
            self.font_button = pygame.font.Font(None, 36)
            print("警告: 未能加载中文字体，将使用默认字体")

        # 加载/创建资源
        self.background = self.create_stone_background()
        self.torch_animation = self.create_torch_animation()
        self.torch_frame_index = 0
        self.torch_timer = 0

        # 标题位置和效果
        self.title_pos = (self.screen_width // 2, self.screen_height // 4)
        self.title_glow = 0
        self.title_glow_dir = 1

        # 按钮设置
        button_width, button_height = 300, 80

        # 开始游戏按钮
        self.start_button = {
            'rect': pygame.Rect(0, 0, button_width, button_height),
            'text': "进入地牢",
            'hover': False,
            'active': False,
            'particles': []
        }
        self.start_button['rect'].center = (self.screen_width // 2, self.screen_height * 3 // 5)

        # 设置按钮
        self.settings_button = {
            'rect': pygame.Rect(0, 0, button_width - 40, button_height - 10),
            'text': "设置",
            'hover': False,
            'active': False,
            'particles': []
        }
        self.settings_button['rect'].center = (self.screen_width // 2, self.screen_height * 3 // 5 + button_height + 20)

        # 装饰元素
        self.decorations = self.generate_decorations()

        # 动画计时器
        self.animation_time = 0

    def create_stone_background(self):
        texture = pygame.Surface((self.screen_width, self.screen_height))

        # 渐变背景 - 从深色到稍微亮一点
        for y in range(self.screen_height):
            # 计算渐变颜色
            gradient_val = 25 + int(20 * (y / self.screen_height))
            color = (gradient_val, gradient_val, gradient_val + 10)
            pygame.draw.line(texture, color, (0, y), (self.screen_width, y))

        # 添加噪点纹理
        for _ in range(8000):
            x = random.randint(0, self.screen_width - 1)
            y = random.randint(0, self.screen_height - 1)
            brightness = random.randint(-15, 15)
            size = random.randint(1, 3)

            # 获取当前像素颜色并调整
            pixel_color = texture.get_at((x, y))
            adjusted_color = (
                max(0, min(255, pixel_color[0] + brightness)),
                max(0, min(255, pixel_color[1] + brightness)),
                max(0, min(255, pixel_color[2] + brightness))
            )

            pygame.draw.circle(texture, adjusted_color, (x, y), size)

        # 添加石块纹理
        for _ in range(100):
            x = random.randint(0, self.screen_width - 20)
            y = random.randint(0, self.screen_height - 20)
            width = random.randint(50, 150)
            height = random.randint(50, 150)
            brightness = random.randint(-10, 10)

            stone_rect = pygame.Rect(x, y, width, height)
            # 使用带SRCALPHA标志的Surface创建透明度
            overlay = pygame.Surface((width, height), pygame.SRCALPHA)
            overlay_color = (brightness + 128, brightness + 128, brightness + 128, 30)
            overlay.fill(overlay_color)
            texture.blit(overlay, (x, y))

            # 石块边缘
            pygame.draw.rect(texture, (40, 40, 50), stone_rect, 2)

        # 添加苔藓斑点
        for _ in range(50):
            x = random.randint(0, self.screen_width - 20)
            y = random.randint(0, self.screen_height - 20)
            size = random.randint(5, 15)
            alpha = random.randint(30, 100)

            # 创建带透明度的苔藓
            moss_surf = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            moss_color = (34, 139, 34, alpha)  # RGBA格式
            pygame.draw.circle(moss_surf, moss_color, (size, size), size)
            texture.blit(moss_surf, (x, y))

        return texture

    def create_torch_animation(self):
        frames = []
        frame_count = 8
        torch_width, torch_height = 120, 180  # 增加尺寸以获得更好的细节

        for i in range(frame_count):
            frame = pygame.Surface((torch_width, torch_height), pygame.SRCALPHA)

            # 火把支架 - 金属杆
            pygame.draw.rect(frame, (80, 80, 80),
                             (torch_width // 2 - 5, torch_height - 60, 10, 50))

            # 支架底座
            pygame.draw.rect(frame, (100, 100, 100),
                             (torch_width // 2 - 15, torch_height - 25, 30, 15),
                             border_radius=5)

            # 装饰环
            pygame.draw.circle(frame, (120, 120, 120),
                               (torch_width // 2, torch_height - 60), 7)
            pygame.draw.circle(frame, (0, 0, 0),
                               (torch_width // 2, torch_height - 60), 7, 1)

            # 火把头 - 缠绕的布
            pygame.draw.ellipse(frame, (139, 69, 19),
                                (torch_width // 2 - 12, torch_height - 90, 24, 30))

            # 随机布纹理
            for _ in range(5):
                x = torch_width // 2 - 10 + random.randint(0, 20)
                y = torch_height - 90 + random.randint(0, 30)
                pygame.draw.line(frame, (101, 67, 33),
                                 (x, y), (x + random.randint(-5, 5), y + random.randint(-5, 5)),
                                 random.randint(1, 2))

            # 动态火焰 - 核心
            flame_x = torch_width // 2
            flame_y = torch_height - 95

            # 基础火焰形状 - 由多个叠加的椭圆组成
            # 火焰高度根据帧数变化
            flame_height_mod = math.sin(i * math.pi / 4) * 10

            # 外层火焰（红色）
            pygame.draw.ellipse(frame, (255, 69, 0, 200),
                                (flame_x - 20, flame_y - 60 - flame_height_mod,
                                 40, 60 + flame_height_mod))

            # 中层火焰（橙色）
            pygame.draw.ellipse(frame, (255, 140, 0, 220),
                                (flame_x - 15, flame_y - 50 - flame_height_mod,
                                 30, 50 + flame_height_mod))

            # 内层火焰（黄色）
            pygame.draw.ellipse(frame, (255, 215, 0, 240),
                                (flame_x - 10, flame_y - 40 - flame_height_mod,
                                 20, 40 + flame_height_mod))

            # 最内层火焰（白色）
            pygame.draw.ellipse(frame, (255, 255, 200, 250),
                                (flame_x - 5, flame_y - 25 - flame_height_mod,
                                 10, 25 + flame_height_mod))

            # 添加动态火花
            for _ in range(8):
                spark_x = flame_x + random.randint(-15, 15)
                spark_y = flame_y - random.randint(20, 60)
                spark_size = random.randint(1, 3)

                # 随机火花颜色
                spark_color = random.choice([
                    (255, 255, 200, 200),  # 白色
                    (255, 215, 0, 200),  # 黄色
                    (255, 140, 0, 200)  # 橙色
                ])

                pygame.draw.circle(frame, spark_color, (spark_x, spark_y), spark_size)

            # 添加火焰光晕效果
            glow_surf = pygame.Surface((torch_width, torch_height), pygame.SRCALPHA)
            glow_radius = 60 + int(flame_height_mod)
            for r in range(glow_radius, 0, -10):
                alpha = max(0, 50 - r // 2)
                glow_color = (255, 140, 0, alpha)
                pygame.draw.circle(glow_surf, glow_color,
                                   (flame_x, flame_y - 30), r)

            frame.blit(glow_surf, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

            frames.append(frame)

        return frames

    def generate_decorations(self):
        """生成各种装饰元素"""
        decorations = []

        # 随机添加一些环境装饰
        for _ in range(12):
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)
            size = random.randint(3, 8)
            speed = random.uniform(0.2, 1.0)

            decorations.append({
                'type': 'dust',
                'pos': [x, y],
                'size': size,
                'speed': speed,
                'alpha': random.randint(20, 100)
            })

        # 添加装饰性的石墙挂饰
        for i in range(3):
            x = random.randint(100, self.screen_width - 100)
            y = random.randint(50, self.screen_height // 3)

            decorations.append({
                'type': 'wall_ornament',
                'pos': [x, y],
                'size': random.randint(30, 60),
                'style': random.choice(['shield', 'sword', 'banner'])
            })

        # 挂在墙上的锁链
        for i in range(4):
            x = random.randint(50, self.screen_width - 50)
            y = random.randint(20, 80)
            length = random.randint(100, 200)

            decorations.append({
                'type': 'chain',
                'pos': [x, y],
                'length': length,
                'segments': random.randint(5, 10)
            })

        return decorations

    def update_decorations(self, dt):
        """更新装饰元素的状态"""
        # 更新灰尘粒子
        for dec in self.decorations:
            if dec['type'] == 'dust':
                # 移动灰尘
                dec['pos'][1] += dec['speed'] * dt * 60

                # 如果灰尘离开屏幕，重置到顶部
                if dec['pos'][1] > self.screen_height:
                    dec['pos'][1] = 0
                    dec['pos'][0] = random.randint(0, self.screen_width)
                    dec['alpha'] = random.randint(20, 100)

    def update_button_particles(self, dt):
        """更新按钮粒子效果"""

        def update_button_particles_for_button(button):
            # 如果按钮被悬停，添加新粒子
            if button['hover']:
                if random.random() < 0.7:
                    # 从按钮边缘随机位置生成粒子
                    side = random.randint(0, 3)  # 0=top, 1=right, 2=bottom, 3=left
                    if side == 0:
                        pos = [button['rect'].left + random.random() * button['rect'].width,
                               button['rect'].top]
                    elif side == 1:
                        pos = [button['rect'].right,
                               button['rect'].top + random.random() * button['rect'].height]
                    elif side == 2:
                        pos = [button['rect'].left + random.random() * button['rect'].width,
                               button['rect'].bottom]
                    else:
                        pos = [button['rect'].left,
                               button['rect'].top + random.random() * button['rect'].height]

                    # 粒子基础属性
                    particle = {
                        'pos': pos,
                        'vel': [random.uniform(-1, 1), random.uniform(-1, 1)],
                        'size': random.uniform(1, 3),
                        'life': random.uniform(0.5, 2),
                        'max_life': 2,
                        'color': random.choice([(255, 215, 0), (255, 165, 0), (255, 140, 0)])
                    }
                    button['particles'].append(particle)

            # 更新现有粒子
            for p in button['particles'][:]:
                p['pos'][0] += p['vel'][0] * dt * 60
                p['pos'][1] += p['vel'][1] * dt * 60
                p['life'] -= dt

                # 移除死亡粒子
                if p['life'] <= 0:
                    button['particles'].remove(p)

        # 更新每个按钮的粒子
        update_button_particles_for_button(self.start_button)
        update_button_particles_for_button(self.settings_button)

    def draw_decorations(self):
        """绘制装饰元素"""
        for dec in self.decorations:
            if dec['type'] == 'dust':
                # 绘制灰尘粒子 - 使用Surface而非直接绘制带Alpha的颜色
                dust_surf = pygame.Surface((dec['size'] * 2, dec['size'] * 2), pygame.SRCALPHA)
                dust_color = (200, 200, 200, dec['alpha'])
                pygame.draw.circle(dust_surf, dust_color,
                                   (dec['size'], dec['size']),
                                   dec['size'])
                self.screen.blit(dust_surf,
                                 (int(dec['pos'][0] - dec['size']),
                                  int(dec['pos'][1] - dec['size'])))

            elif dec['type'] == 'wall_ornament':
                # 绘制墙上装饰
                if dec['style'] == 'shield':
                    # 盾牌
                    pygame.draw.ellipse(self.screen, (100, 100, 120),
                                        (dec['pos'][0] - dec['size'] // 2,
                                         dec['pos'][1] - dec['size'] // 2,
                                         dec['size'], dec['size'] * 1.2))
                    pygame.draw.ellipse(self.screen, (60, 60, 80),
                                        (dec['pos'][0] - dec['size'] // 2,
                                         dec['pos'][1] - dec['size'] // 2,
                                         dec['size'], dec['size'] * 1.2), 2)

                    # 盾牌中央图案
                    pygame.draw.rect(self.screen, (150, 120, 50),
                                     (dec['pos'][0] - dec['size'] // 4,
                                      dec['pos'][1] - dec['size'] // 4,
                                      dec['size'] // 2, dec['size'] // 2))

                elif dec['style'] == 'sword':
                    # 剑 - 简化版本
                    # 剑身
                    pygame.draw.rect(self.screen, (200, 200, 200),
                                     (dec['pos'][0] - 2,
                                      dec['pos'][1] - dec['size'] // 2,
                                      4, dec['size']))
                    # 剑柄
                    pygame.draw.rect(self.screen, (139, 69, 19),
                                     (dec['pos'][0] - 6,
                                      dec['pos'][1] + dec['size'] // 2 - 10,
                                      12, 15))
                    # 剑格
                    pygame.draw.rect(self.screen, (180, 150, 50),
                                     (dec['pos'][0] - 10,
                                      dec['pos'][1] + dec['size'] // 2 - 12,
                                      20, 5))

                elif dec['style'] == 'banner':
                    # 旗帜
                    banner_color = random.choice([(180, 0, 0), (0, 80, 180), (80, 120, 0)])
                    pygame.draw.rect(self.screen, banner_color,
                                     (dec['pos'][0] - dec['size'] // 2,
                                      dec['pos'][1],
                                      dec['size'], dec['size'] * 1.5))
                    # 旗杆
                    pygame.draw.rect(self.screen, (100, 80, 60),
                                     (dec['pos'][0] - dec['size'] // 2 - 4,
                                      dec['pos'][1] - 20,
                                      4, dec['size'] * 1.5 + 30))
                    # 装饰纹章
                    pygame.draw.circle(self.screen, (220, 220, 220),
                                       (dec['pos'][0], dec['pos'][1] + dec['size'] // 2),
                                       dec['size'] // 5)

            elif dec['type'] == 'chain':
                # 绘制锁链
                for i in range(dec['segments']):
                    segment_length = dec['length'] / dec['segments']
                    chain_x = dec['pos'][0]
                    chain_y = dec['pos'][1] + i * segment_length

                    # 左右偏移，创造自然晃动效果
                    offset_x = math.sin(self.animation_time / 500 + i * 0.5) * 5

                    # 锁链环
                    pygame.draw.ellipse(self.screen, (100, 100, 100),
                                        (chain_x - 7 + offset_x, chain_y, 14, segment_length * 0.9))
                    pygame.draw.ellipse(self.screen, (50, 50, 50),
                                        (chain_x - 7 + offset_x, chain_y, 14, segment_length * 0.9), 2)

    def draw_button(self, button):
        """绘制精美的按钮"""
        rect = button['rect']
        hover = button['hover']

        # 绘制基本按钮
        base_color = (80, 80, 100) if hover else (60, 60, 80)
        pygame.draw.rect(self.screen, base_color, rect, border_radius=12)

        # 3D效果阴影
        highlight_rect = rect.inflate(-6, -6)
        pygame.draw.rect(self.screen, (100, 100, 120) if hover else (80, 80, 100),
                         highlight_rect, border_radius=10)

        # 金色边框
        border_color = (200, 170, 60) if hover else (150, 120, 40)
        pygame.draw.rect(self.screen, border_color, rect, 2, border_radius=12)

        # 内部装饰图案 - 角落装饰
        corner_size = 8
        corner_color = (200, 170, 60) if hover else (150, 120, 40)

        # 左上角
        pygame.draw.line(self.screen, corner_color,
                         (rect.left + 5, rect.top + 5),
                         (rect.left + 5 + corner_size, rect.top + 5), 2)
        pygame.draw.line(self.screen, corner_color,
                         (rect.left + 5, rect.top + 5),
                         (rect.left + 5, rect.top + 5 + corner_size), 2)

        # 右上角
        pygame.draw.line(self.screen, corner_color,
                         (rect.right - 5, rect.top + 5),
                         (rect.right - 5 - corner_size, rect.top + 5), 2)
        pygame.draw.line(self.screen, corner_color,
                         (rect.right - 5, rect.top + 5),
                         (rect.right - 5, rect.top + 5 + corner_size), 2)

        # 左下角
        pygame.draw.line(self.screen, corner_color,
                         (rect.left + 5, rect.bottom - 5),
                         (rect.left + 5 + corner_size, rect.bottom - 5), 2)
        pygame.draw.line(self.screen, corner_color,
                         (rect.left + 5, rect.bottom - 5),
                         (rect.left + 5, rect.bottom - 5 - corner_size), 2)

        # 右下角
        pygame.draw.line(self.screen, corner_color,
                         (rect.right - 5, rect.bottom - 5),
                         (rect.right - 5 - corner_size, rect.bottom - 5), 2)
        pygame.draw.line(self.screen, corner_color,
                         (rect.right - 5, rect.bottom - 5),
                         (rect.right - 5, rect.bottom - 5 - corner_size), 2)

        # 绘制文字
        text_color = (255, 220, 100) if hover else (220, 180, 60)
        text_surf = self.font_button.render(button['text'], True, text_color)
        text_rect = text_surf.get_rect(center=rect.center)

        # 如果按钮被激活，文字略微下移以增加按压感
        if button['active']:
            text_rect.y += 2

        self.screen.blit(text_surf, text_rect)

        # 绘制粒子效果
        for p in button['particles']:
            alpha = int(255 * (p['life'] / p['max_life']))
            size = p['size'] * (p['life'] / p['max_life'])

            # 绘制粒子
            particle_surf = pygame.Surface((int(size * 2), int(size * 2)), pygame.SRCALPHA)
            particle_color = (*p['color'], alpha)
            pygame.draw.circle(particle_surf, particle_color,
                               (int(size), int(size)), int(size))

            self.screen.blit(particle_surf,
                             (int(p['pos'][0] - size), int(p['pos'][1] - size)))

    def draw_title(self):
        # 动态更新标题光晕
        self.title_glow += 0.02 * self.title_glow_dir
        if self.title_glow >= 1.0:
            self.title_glow = 1.0
            self.title_glow_dir = -1
        elif self.title_glow <= 0.0:
            self.title_glow = 0.0
            self.title_glow_dir = 1

        # 计算光晕颜色
        glow_alpha = int(50 + 100 * self.title_glow)
        glow_size = int(10 + 20 * self.title_glow)

        # 渲染主标题文本
        title_text = "魔塔地牢"

        # 标题阴影
        shadow_surf = self.font_title.render(title_text, True, (0, 0, 0))
        shadow_rect = shadow_surf.get_rect(center=(self.title_pos[0] + 3, self.title_pos[1] + 3))
        self.screen.blit(shadow_surf, shadow_rect)

        # 主标题
        title_surf = self.font_title.render(title_text, True, (220, 180, 60))
        title_rect = title_surf.get_rect(center=self.title_pos)

        # 底层光晕效果
        if glow_alpha > 30:
            glow_surf = pygame.Surface((title_rect.width + glow_size * 2,
                                        title_rect.height + glow_size * 2), pygame.SRCALPHA)
            for i in range(3):
                # 确保glow_color是有效的RGBA值
                glow_alpha_i = glow_alpha // (i + 1)
                glow_color = (255, 200, 100, glow_alpha_i)
                pygame.draw.rect(glow_surf, glow_color,
                                 (glow_size - i * 3, glow_size - i * 3,
                                  title_rect.width + i * 6, title_rect.height + i * 6),
                                 border_radius=10)

            self.screen.blit(glow_surf,
                             (title_rect.left - glow_size, title_rect.top - glow_size))

        # 绘制标题
        self.screen.blit(title_surf, title_rect)

        # 装饰线条
        line_color = (220, 180, 60)
        line_length = 200
        pygame.draw.line(self.screen, line_color,
                         (self.title_pos[0] - line_length, self.title_pos[1] + title_rect.height // 2),
                         (self.title_pos[0] - 20, self.title_pos[1] + title_rect.height // 2), 2)
        pygame.draw.line(self.screen, line_color,
                         (self.title_pos[0] + 20, self.title_pos[1] + title_rect.height // 2),
                         (self.title_pos[0] + line_length, self.title_pos[1] + title_rect.height // 2), 2)

        # 装饰图案
        ornament_radius = 10
        pygame.draw.circle(self.screen, line_color,
                           (self.title_pos[0] - line_length - ornament_radius,
                            self.title_pos[1] + title_rect.height // 2),
                           ornament_radius)
        pygame.draw.circle(self.screen, line_color,
                           (self.title_pos[0] + line_length + ornament_radius,
                            self.title_pos[1] + title_rect.height // 2),
                           ornament_radius)

    def update(self, dt):
        """更新菜单的各种动画和状态"""
        # 更新动画计时
        self.animation_time += dt * 1000  # 毫秒

        # 更新火把动画
        self.torch_timer += dt
        if self.torch_timer >= 0.1:  # 每0.1秒更新一帧
            self.torch_timer = 0
            self.torch_frame_index = (self.torch_frame_index + 1) % len(self.torch_animation)

        # 更新按钮效果
        mouse_pos = pygame.mouse.get_pos()

        # 更新开始按钮状态
        self.start_button['hover'] = self.start_button['rect'].collidepoint(mouse_pos)

        # 更新设置按钮状态
        self.settings_button['hover'] = self.settings_button['rect'].collidepoint(mouse_pos)

        # 更新按钮粒子
        self.update_button_particles(dt)

        # 更新装饰元素
        self.update_decorations(dt)

    def draw(self):
        """绘制整个菜单界面"""
        # 绘制背景
        self.screen.blit(self.background, (0, 0))

        # 绘制装饰
        self.draw_decorations()

        # 绘制火把
        torch_frame = self.torch_animation[self.torch_frame_index]

        # 左侧火把
        left_torch_x = self.title_pos[0] - 250
        left_torch_y = self.title_pos[1] - torch_frame.get_height() // 2
        self.screen.blit(torch_frame, (left_torch_x, left_torch_y))

        # 右侧火把（水平翻转）
        right_torch_x = self.title_pos[0] + 250 - torch_frame.get_width()
        right_torch_y = self.title_pos[1] - torch_frame.get_height() // 2
        flipped_torch = pygame.transform.flip(torch_frame, True, False)
        self.screen.blit(flipped_torch, (right_torch_x, right_torch_y))

        # 绘制标题
        self.draw_title()

        # 绘制按钮
        self.draw_button(self.start_button)
        self.draw_button(self.settings_button)

        # 返回按钮区域用于点击检测
        return [self.start_button['rect'], self.settings_button['rect']]


class DeathScreen:
    def __init__(self, screen, player, floor):
        self.screen = screen
        self.player = player
        self.floor = floor
        self.font_title = pygame.font.Font(None, 64)
        self.font_stats = pygame.font.Font(None, 32)
        self.blood_texture = self.create_blood_texture()

    def create_blood_texture(self):
        texture = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        # 血渍效果
        for _ in range(50):
            x = random.randint(0, SCREEN_WIDTH)
            y = random.randint(0, SCREEN_HEIGHT)
            radius = random.randint(10, 30)
            alpha = random.randint(100, 150)
            pygame.draw.circle(texture, (139, 0, 0, alpha), (x, y), radius)
            # 血滴飞溅
            for _ in range(5):
                dx = random.randint(-20, 20)
                dy = random.randint(-20, 20)
                pygame.draw.line(texture, (139, 0, 0, alpha),
                                 (x, y), (x + dx, y + dy), 3)
        return texture

    def draw(self):
        # 暗红色覆盖层
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((50, 0, 0, 200))
        self.screen.blit(overlay, (0, 0))
        self.screen.blit(self.blood_texture, (0, 0))

        # 破碎盾牌装饰
        shield = pygame.Surface((256, 256), pygame.SRCALPHA)
        # 绘制盾牌基底
        pygame.draw.polygon(shield, (150, 150, 150), [
            (128, 20), (220, 80), (220, 176), (128, 236), (36, 176), (36, 80)
        ])
        # 添加裂痕效果
        pygame.draw.line(shield, (80, 80, 80), (100, 100), (156, 156), 5)
        pygame.draw.line(shield, (80, 80, 80), (156, 100), (100, 156), 5)
        self.screen.blit(shield, (SCREEN_WIDTH // 2 - 128, SCREEN_HEIGHT // 2 - 100))

        # 标题
        title_surf = self.font_title.render("YOU DIED", True, COLOR_DEATH_RED)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, 150))
        self.screen.blit(title_surf, title_rect)

        # 统计信息
        stats = [
            f"Reached Floor: {self.floor}",
            f"ATK: {self.player.atk}",
            f"DEF: {self.player.defense}"
        ]
        y_start = 300
        for text in stats:
            text_surf = self.font_stats.render(text, True, (200, 200, 200))
            text_rect = text_surf.get_rect(center=(SCREEN_WIDTH // 2, y_start))
            self.screen.blit(text_surf, text_rect)
            y_start += 50

        # 重新开始按钮
        button_rect = pygame.Rect(0, 0, 280, 70)
        button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
        mouse_pos = pygame.mouse.get_pos()
        is_hover = button_rect.collidepoint(mouse_pos)

        # 按钮样式
        button_color = COLOR_BUTTON_HOVER if is_hover else COLOR_BUTTON
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=8)
        pygame.draw.rect(self.screen, COLOR_DEATH_RED, button_rect.inflate(-10, -10), border_radius=5)

        # 按钮文字
        text_surf = self.font_stats.render("Retry Journey", True, COLOR_TEXT)
        text_rect = text_surf.get_rect(center=button_rect.center)
        self.screen.blit(text_surf, text_rect)

        return button_rect

# ---------------- 物品生成系统 ---------------


class ItemProbabilitySystem:
    def __init__(self, game):
        self.game = game

        # 基础物品权重 - 将作为基准值
        self.base_weights = {
            "CHEST": 10,  # 宝箱
            "HP_SMALL": 15,  # 小红药
            "HP_LARGE": 5,  # 大红药
            "MP_SMALL": 15,  # 小蓝药
            "MP_LARGE": 5,  # 大蓝药
            "ATK_GEM": 10,  # 攻击宝石
            "DEF_GEM": 10,  # 防御宝石
            "ATK_GEM_LARGE": 3,  # 大攻击宝石
            "DEF_GEM_LARGE": 3  # 大防御宝石
        }

        # 物品稀有度分类
        self.rarity_tiers = {
            "普通": ["CHEST", "HP_SMALL", "MP_SMALL"],
            "稀有": ["ATK_GEM", "DEF_GEM"],
            "罕见": ["HP_LARGE", "MP_LARGE"],
            "珍贵": ["ATK_GEM_LARGE", "DEF_GEM_LARGE"]
        }

        # 稀有度显示颜色
        self.rarity_colors = {
            "普通": (200, 200, 200),  # 白色
            "稀有": (30, 144, 255),  # 蓝色
            "罕见": (148, 0, 211),  # 紫色
            "珍贵": (255, 165, 0)  # 橙色
        }

        # 初始化玩家的幸运值
        self.player_luck = 0

        # 上次稀有物品掉落记录（防止连续掉落太多低级物品）
        self.pity_counter = 0
        self.pity_threshold = 15  # 连续15次没有稀有物品后，提高稀有物品概率

        # 当前楼层特殊加成
        self.floor_bonus = {}

    def get_item_rarity(self, item_type):
        """根据物品类型获取其稀有度"""
        for rarity, items in self.rarity_tiers.items():
            if item_type in items:
                return rarity
        return "普通"  # 默认为普通

    def get_rarity_color(self, rarity):
        return self.rarity_colors.get(rarity, (255, 255, 255))

    def update_floor_bonus(self, floor):
        # 基础修正
        self.floor_bonus = {
            "CHEST": 1.0 + floor * 0.05,  # 金币随楼层略微增加
            "HP_SMALL": 1.0,  # 保持不变
            "HP_LARGE": 0.5 + floor * 0.1,  # 大红药随楼层明显增加
            "MP_SMALL": 1.0,  # 保持不变
            "MP_LARGE": 0.5 + floor * 0.1,  # 大蓝药随楼层明显增加
            "ATK_GEM": 0.8 + floor * 0.07,  # 攻击宝石随楼层增加
            "DEF_GEM": 0.8 + floor * 0.07,  # 防御宝石随楼层增加
            "ATK_GEM_LARGE": 0.1 + floor * 0.15,  # 大攻击宝石随楼层大幅增加
            "DEF_GEM_LARGE": 0.1 + floor * 0.15  # 大防御宝石随楼层大幅增加
        }

        # 特殊楼层修正
        if floor % 10 == 0:  # 每10层为BOSS层，提高稀有物品概率
            for item in self.rarity_tiers["珍贵"]:
                self.floor_bonus[item] *= 2.0

        # 为确保不同楼层有不同的偏好
        if floor % 3 == 0:  # 每3层偏好攻击类物品
            self.floor_bonus["ATK_GEM"] *= 1.5
            self.floor_bonus["ATK_GEM_LARGE"] *= 1.3
        elif floor % 3 == 1:  # 每3层偏好防御类物品
            self.floor_bonus["DEF_GEM"] *= 1.5
            self.floor_bonus["DEF_GEM_LARGE"] *= 1.3
        else:  # 偏好恢复类物品
            self.floor_bonus["HP_LARGE"] *= 1.5
            self.floor_bonus["MP_LARGE"] *= 1.5

    def update_player_needs(self, player):
        """根据玩家当前状态更新物品需求值"""
        player_needs = {}

        # 根据生命值状态调整药水权重
        hp_ratio = player.hp / player.max_hp
        if hp_ratio < 0.3:  # 生命值危急
            player_needs["HP_SMALL"] = 2.0
            player_needs["HP_LARGE"] = 2.5
        elif hp_ratio < 0.6:  # 生命值较低
            player_needs["HP_SMALL"] = 1.5
            player_needs["HP_LARGE"] = 1.8
        else:  # 生命值充足
            player_needs["HP_SMALL"] = 1.0
            player_needs["HP_LARGE"] = 1.0

        # 根据魔法值状态调整药水权重
        mp_ratio = player.mp / player.max_mp
        if mp_ratio < 0.3:  # 魔法值危急
            player_needs["MP_SMALL"] = 2.0
            player_needs["MP_LARGE"] = 2.5
        elif mp_ratio < 0.6:  # 魔法值较低
            player_needs["MP_SMALL"] = 1.5
            player_needs["MP_LARGE"] = 1.8
        else:  # 魔法值充足
            player_needs["MP_SMALL"] = 1.0
            player_needs["MP_LARGE"] = 1.0

        # 根据战斗能力调整属性宝石权重
        effective_atk = player.atk / (self.game.floor * 50)  # 根据当前楼层估算合理攻击力
        effective_def = player.defense / (self.game.floor * 50)  # 根据当前楼层估算合理防御力

        if effective_atk < 0.8:  # 攻击力不足
            player_needs["ATK_GEM"] = 1.8
            player_needs["ATK_GEM_LARGE"] = 2.0
        else:
            player_needs["ATK_GEM"] = 1.0
            player_needs["ATK_GEM_LARGE"] = 1.0

        if effective_def < 0.8:  # 防御力不足
            player_needs["DEF_GEM"] = 1.8
            player_needs["DEF_GEM_LARGE"] = 2.0
        else:
            player_needs["DEF_GEM"] = 1.0
            player_needs["DEF_GEM_LARGE"] = 1.0

        return player_needs

    def calculate_drop_weights(self):
        player_needs = self.update_player_needs(self.game.player)

        final_weights = {}
        for item_type, base_weight in self.base_weights.items():
            # 组合各种修正因子
            weight = base_weight

            # 楼层修正
            if item_type in self.floor_bonus:
                weight *= self.floor_bonus[item_type]

            # 玩家需求修正
            if item_type in player_needs:
                weight *= player_needs[item_type]

            # 幸运值修正
            if self.get_item_rarity(item_type) in ["罕见", "珍贵"]:
                weight *= (1.0 + self.player_luck * 0.1)

            # 保底机制修正
            if self.get_item_rarity(item_type) in ["罕见", "珍贵"] and self.pity_counter > self.pity_threshold:
                pity_bonus = (self.pity_counter - self.pity_threshold) * 0.15
                weight *= (1.0 + pity_bonus)

            final_weights[item_type] = max(0.1, weight)  # 确保权重最小为0.1

        return final_weights

    def generate_random_item(self, x, y):
        """生成一个随机物品"""
        weights = self.calculate_drop_weights()

        # 将权重转换为可用于random.choices的格式
        items = list(weights.keys())
        weight_values = list(weights.values())

        # 选择一个物品类型
        item_type = random.choices(items, weights=weight_values, k=1)[0]

        # 获取物品稀有度
        rarity = self.get_item_rarity(item_type)

        # 更新保底计数器
        if rarity in ["罕见", "珍贵"]:
            self.pity_counter = 0  # 重置保底计数器
            # 在游戏消息中显示稀有物品生成
            rarity_color_name = self._get_color_name(self.get_rarity_color(rarity))
            self.game.add_message(f"{rarity_color_name}{rarity}物品：{self._get_item_name(item_type)}！")
        else:
            self.pity_counter += 1  # 增加保底计数器

        return Item(x, y, item_type)

    def _get_color_name(self, color_tuple):
        """将颜色元组转换为可读的颜色名称（用于文本消息）"""
        colors = {
            (200, 200, 200): "白色",
            (30, 144, 255): "蓝色",
            (148, 0, 211): "紫色",
            (255, 165, 0): "橙色"
        }
        return colors.get(color_tuple, "")

    def _get_item_name(self, item_type):
        """根据物品类型获取可读的物品名称"""
        item_names = {
            "CHEST": "宝箱",
            "HP_SMALL": "小型生命药水",
            "HP_LARGE": "大型生命药水",
            "MP_SMALL": "小型魔法药水",
            "MP_LARGE": "大型魔法药水",
            "ATK_GEM": "攻击宝石",
            "DEF_GEM": "防御宝石",
            "ATK_GEM_LARGE": "高级攻击宝石",
            "DEF_GEM_LARGE": "高级防御宝石"
        }
        return item_names.get(item_type, item_type)

# ----------------- 玩家类 -------------------

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 1000
        self.max_hp = 1000000
        self.mp = 50  # Initial magic points
        self.max_mp = 500000  # Maximum magic points
        self.base_atk = 25  # 基础攻击力
        self.base_defense = 25  # 基础防御力
        self.base_attack_speed = 1.0  # 基础攻击速度
        self.base_attack_range = 1   # 基础攻击范围
        self.attack_cooldown = 0
        self.coins = 0
        self.equipped_weapon = None  # 当前装备的武器
        self.equipped_armor = None  # 当前装备的护甲
        self.skills = {
            'FireStrikeEffect': {
                'name': "火焰重击",
                'cooldown': 5,
                'current_cd': 0,
                'range': 6,
                'radius': 2,
                'damage_multiple': 2.2,
                'effect': FireStrikeEffect,
                'key': pygame.K_f,
                'mp_cost': 60  # Added MP cost
            },
            'LightningEffect': {
                'name': "闪电链",
                'cooldown': 3,
                'current_cd': 0,
                'range': 8,
                'max_targets': 3,
                'damage_multiple': 1.8,
                'effect': LightningEffect,
                'key': pygame.K_e,
                'mp_cost': 40  # Added MP cost
            },
            'HolyBallEffect': {
                'name': "神圣球",
                'cooldown': 8,
                'current_cd': 0,
                'seek_range': 10,
                'ball_count': 6,
                'damage_multiple': 2.5,
                'effect': HolyBallEffect,
                'key': pygame.K_c,
                'mp_cost': 100  # Added MP cost
            },
            'TripleAttack': {
                'name': "三连斩",
                'cooldown': 6,
                'current_cd': 0,
                'range': 2,
                'damage_multipliers': [0.8, 1.0, 1.5],  # 三连斩伤害系数
                'effect': TripleAttack,
                'key': pygame.K_q,
                'mp_cost': 60  # Added MP cost
            },
            'SummonLightningBall': {
                'name': "守护闪电球阵",
                'cooldown': 30,  # 30秒冷却时间
                'current_cd': 0,
                'duration': 20,  # 闪电球存在15秒
                'ball_count': 6,  # 召唤6个闪电球
                'attack_range': 6,  # 攻击范围6格
                'attack_speed': 1.0,  # 每秒攻击1次
                'damage_multiple': 1.0,  # 伤害为玩家攻击力的1倍
                'effect': SummonLightningBall,
                'key': pygame.K_z,
                'mp_cost': 150  # Added MP cost
            },
            'SummonHolyBall': {
                'name': "神圣光环",
                'cooldown': 45,
                'current_cd': 0,
                'duration': 20,  # 20 seconds duration
                'ball_count': 6,  # 6 holy balls
                'attack_range': 6,  # 6 tiles attack range
                'attack_speed': 0.8,  # 0.8 attacks per second
                'damage_multiple': 1.2,  # 1.2x player's attack damage
                'heal_percent': 0.05,  # Heal 5% of max HP per second
                'effect': SummonHolyBall,
                'key': pygame.K_x,
                'mp_cost': 200  # Added MP cost
            }
        }

    @property
    def attack_speed(self):
        if self.equipped_weapon:
            return self.base_attack_speed * self.equipped_weapon.get("attack_speed", 1.0)
        return self.base_attack_speed

    @property
    def attack_range(self):
        if self.equipped_weapon:
            return self.equipped_weapon.get("attack_range", 1)
        return self.base_attack_range

    @property
    def atk(self):
        bonus = self.equipped_weapon["atk"] if self.equipped_weapon else 0
        multiple = self.equipped_weapon["multiple"] if self.equipped_weapon else 1
        return self.base_atk * multiple + bonus

    @property
    def defense(self):
        bonus = self.equipped_armor["def"] if self.equipped_armor else 0
        multiple = self.equipped_armor["multiple"] if self.equipped_armor else 1
        return self.base_defense * multiple + bonus

    def move(self, dx, dy, game):
        new_x = self.x + dx
        new_y = self.y + dy
        if game.is_walkable(new_x, new_y):
            self.x = new_x
            self.y = new_y



class Monster:
    def __init__(self, x, y, mdata, floor):
        self.x = x
        self.y = y
        self.name = mdata["name"]
        self.hp = self.Num_Random_Control(floor, mdata["HP"])  # 根据楼层增强怪物
        self.atk = self.Num_Random_Control(floor, mdata["ATK"])
        self.defense = self.Num_Random_Control(floor, mdata["DEF"])
        self.attack_range = mdata["attack_range"]  # 攻击范围
        self.attack_speed = mdata["attack_speed"]  # 攻击速度
        self.attack_cooldown = 0
        self.size = mdata["size"]  # 怪物尺寸
        self.coin = self.Num_Random_Control(floor, mdata["coin"])
        self.speed = mdata["speed"]  # 初始化移动速度
        self.move_counter = 0  # 用于控制移动频率的计数器

        # 追踪系统新增属性
        self.is_tracking = False  # 是否正在追踪玩家
        self.tracking_timeout = 0  # 追踪超时计时器
        self.tracking_duration = MONSTER_TRACKING_DURATION  # 追踪持续时间(秒)
        self.path_to_player = []  # 存储到玩家的路径
        self.path_update_cooldown = 0  # 路径更新冷却
        self.path_update_rate = MONSTER_PATH_UPDATE_RATE  # 路径更新频率(秒)
        self.wander_direction = None  # 非追踪状态下的随机移动方向
        self.wander_steps = 0  # 随机移动剩余步数
        self.last_pos = (x, y)  # 上一个位置，用于检测卡住
        self.stuck_counter = 0  # 卡住计数器

        if "魔王" in self.name:
            self.skill_cd = 0  # 技能冷却计时器
            self.crack_cd = 10  # 地裂冷却
            self.crack_range = 4
            self.crack_damage = self.Num_Random_Control(floor, mdata["ATK"])
            self.stun_duration = 3
        elif "冰霜巨龙" in self.name:
            self.skill_cd = 0  # 技能冷却计时器
            self.breath_cd = 8
            self.breath_range = 6
            self.ice_damage = 1.5 * self.Num_Random_Control(floor, mdata["ATK"])
        elif "魔法师" in self.name:
            self.skill_cd = 0  # 技能冷却计时器
            self.magic_cd = 5
            self.magic_range = 4
        elif "电击球" in self.name:
            self.skill_cd = 0
            self.electric_cd = 1  # 冷却1秒
            self.electric_range = 4  # 四格范围
        elif "火焰领主" in self.name:
            self.skill_cd = 0
            self.strike_cd = 1.7  # 技能冷却
            self.strike_range = 9  # 影响范围
            self.strike_damage = self.Num_Random_Control(floor, mdata["ATK"]) * 2
        elif "神圣灾祸骑士" in self.name:
            self.num_balls= mdata["num_balls"]

    def Num_Random_Control(self, floor, x):
        return math.ceil(
            x * (1 + 0.2 * random.randint(0, floor)) * (0.6 + 0.4 * floor) * (1 + S_MONSTER * random.random()))

# ---------------- 游戏商店 ----------------------

class DungeonShop:
    def __init__(self, screen, player, floor):
        """
        初始化商店界面
        :param screen: 游戏屏幕
        :param player: 玩家对象
        :param floor: 当前楼层
        """
        self.screen = screen
        self.player = player
        self.floor = floor

        # 获取屏幕尺寸
        self.screen_width, self.screen_height = screen.get_size()

        # 商店窗口参数 - 调整窗口大小，为文字提供更多空间
        self.window_width = 700
        self.window_height = 570  # 增加高度，为更多物品提供空间
        self.window_x = (self.screen_width - self.window_width) // 2
        self.window_y = (self.screen_height - self.window_height) // 2

        # 字体和颜色 - 使用支持中文的字体
        try:
            # 尝试使用系统中文字体，调整字体大小
            self.title_font = pygame.font.SysFont("SimHei", 38, bold=True)  # 黑体标题
            self.item_font = pygame.font.SysFont("SimSun", 22)  # 宋体项目
            self.info_font = pygame.font.SysFont("SimSun", 18)  # 宋体描述，减小字体
            self.price_font = pygame.font.SysFont("SimSun", 20, bold=True)  # 价格专用字体，减小字体
        except:
            # 回退到默认字体
            self.title_font = pygame.font.Font(None, 46)
            self.item_font = pygame.font.Font(None, 30)
            self.info_font = pygame.font.Font(None, 26)
            self.price_font = pygame.font.Font(None, 28)

            # 颜色定义
        self.COLOR_BG = (30, 30, 40, 220)  # 增加不透明度
        self.COLOR_BORDER = (70, 70, 100)
        self.COLOR_TITLE = (255, 215, 0)  # 金色
        self.COLOR_TEXT = (220, 220, 220)
        self.COLOR_DESC = (180, 180, 200)  # 描述文字颜色
        self.COLOR_HIGHLIGHT = (80, 80, 130)
        self.COLOR_PRICE = (255, 165, 0)  # 橙色
        self.COLOR_AFFORDABLE = (80, 220, 80)  # 绿色
        self.COLOR_UNAFFORDABLE = (220, 80, 80)  # 红色
        self.COLOR_SHINE = (255, 255, 200)
        self.COLOR_BUTTON = (60, 60, 80)
        self.COLOR_BUTTON_HOVER = (80, 80, 120)

        # 商品项目列表 - Add new magic potions (最多8个物品，分2排显示)
        self.items = [
            {
                "name": f"生命",
                "description": f"恢复 {1000 * floor} 点生命值",
                "price": 100 * floor,
                "key": pygame.K_1,
                "label": "1",
                "icon": self._create_potion_icon((255, 0, 0)),  # 红色药水
                "action": self._buy_small_hp
            },
            {
                "name": f"魔法",
                "description": f"恢复 {50 * floor} 点魔法值",
                "price": 200 * floor,
                "key": pygame.K_2,
                "label": "2",
                "icon": self._create_potion_icon((0, 0, 255)),  # 蓝色药水
                "action": self._buy_small_mp
            },
            {
                "name": f"力量",
                "description": f"提升 {5 * floor} 点攻击力",
                "price": 100 * floor,
                "key": pygame.K_3,
                "label": "3",
                "icon": self._create_gem_icon((255, 100, 100)),  # 红色宝石
                "action": self._buy_small_atk
            },
            {
                "name": f"护盾",
                "description": f"提升 {5 * floor} 点防御力",
                "price": 100 * floor,
                "key": pygame.K_4,
                "label": "4",
                "icon": self._create_gem_icon((100, 100, 255)),  # 蓝色宝石
                "action": self._buy_small_def
            },
            {
                "name": f"大红药",
                "description": f"恢复 {10000 * floor} 点生命值",
                "price": 1000 * floor,
                "key": pygame.K_5,
                "label": "5",
                "icon": self._create_potion_icon((200, 0, 0), large=True),  # 深红色大药水
                "action": self._buy_large_hp
            },
            {
                "name": f"大蓝药",
                "description": f"恢复 {500 * floor} 点魔法值",
                "price": 2000 * floor,
                "key": pygame.K_6,
                "label": "6",
                "icon": self._create_potion_icon((0, 0, 200), large=True),  # 深蓝色大药水
                "action": self._buy_large_mp
            },
            {
                "name": f"大力量",
                "description": f"提升 {50 * floor} 点攻击力",
                "price": 1000 * floor,
                "key": pygame.K_7,
                "label": "7",
                "icon": self._create_gem_icon((255, 50, 50), large=True),  # 深红色大宝石
                "action": self._buy_large_atk
            },
            {
                "name": f"大防御",
                "description": f"提升 {50 * floor} 点防御力",
                "price": 1000 * floor,
                "key": pygame.K_8,
                "label": "8",
                "icon": self._create_gem_icon((50, 50, 255), large=True),  # 深蓝色大宝石
                "action": self._buy_large_def
            }
        ]

        # 商店按钮
        self.exit_button = pygame.Rect(
            self.window_x + self.window_width - 160,
            self.window_y + self.window_height - 60,
            140, 40
        )

        # 购买结果消息
        self.message = None
        self.message_time = 0
        self.message_duration = 2000  # 消息显示时长（毫秒）

        # 移除粒子效果
        self.particles = []

        # 商品悬停状态
        self.hovered_item = None
        self.hovered_button = False

        # 创建商店表面（用于绘制基础界面）
        self.shop_surface = pygame.Surface((self.window_width, self.window_height), pygame.SRCALPHA)
        self._create_shop_background()

    def _create_potion_icon(self, color, large=False):
        """创建药水图标"""
        size = 32 if large else 24
        icon = pygame.Surface((size, size), pygame.SRCALPHA)

        # 瓶身
        bottle_width = size - 8
        bottle_height = size * 0.8

        # 瓶身（玻璃半透明效果）
        bottle_rect = pygame.Rect(
            (size - bottle_width) // 2,
            size - bottle_height,
            bottle_width, bottle_height
        )
        pygame.draw.rect(icon, (150, 150, 200, 180), bottle_rect, border_radius=int(bottle_width * 0.3))

        # 液体
        liquid_height = bottle_height * 0.7
        liquid_rect = pygame.Rect(
            bottle_rect.x + 2,
            bottle_rect.y + bottle_height - liquid_height,
            bottle_width - 4, liquid_height - 2
        )
        pygame.draw.rect(icon, color, liquid_rect, border_radius=int(bottle_width * 0.2))

        # 瓶口和瓶塞
        neck_width = bottle_width * 0.4
        neck_height = size * 0.15
        pygame.draw.rect(icon, (180, 180, 220),
                         ((size - neck_width) // 2, size - bottle_height - neck_height,
                          neck_width, neck_height),
                         border_radius=2)

        # 瓶塞
        cork_rect = pygame.Rect(
            (size - neck_width + 2) // 2,
            size - bottle_height - neck_height - 4,
            neck_width - 2, 6
        )
        pygame.draw.rect(icon, (150, 100, 50), cork_rect, border_radius=2)

        # 高光效果
        pygame.draw.line(icon, (255, 255, 255, 150),
                         (bottle_rect.x + 2, bottle_rect.y + 5),
                         (bottle_rect.x + 5, bottle_rect.y + 8), 2)

        return icon

    def _create_gem_icon(self, color, large=False):
        """创建宝石图标"""
        size = 32 if large else 24
        icon = pygame.Surface((size, size), pygame.SRCALPHA)

        # 宝石中心点
        center = (size // 2, size // 2)

        # 宝石切面（八边形）
        gem_size = size * 0.7
        points = []
        for i in range(8):
            angle = math.pi * i / 4
            x = center[0] + math.cos(angle) * gem_size / 2
            y = center[1] + math.sin(angle) * gem_size / 2
            points.append((x, y))

        # 绘制宝石主体
        pygame.draw.polygon(icon, color, points)

        # 绘制高光
        highlight_points = [
            (center[0], center[1] - gem_size / 3),
            (center[0] + gem_size / 4, center[1]),
            (center[0], center[1] + gem_size / 3)
        ]
        pygame.draw.polygon(icon, (255, 255, 255, 100), highlight_points)

        # 添加闪光点
        pygame.draw.circle(icon, (255, 255, 255, 200),
                           (center[0] - gem_size / 4, center[1] - gem_size / 4), 2)

        return icon

    def _create_shop_background(self):
        """创建商店背景"""
        # 绘制主窗口背景（使用半透明背景）
        self.shop_surface.fill(self.COLOR_BG)

        # 窗口边框
        border_size = 4
        pygame.draw.rect(self.shop_surface, self.COLOR_BORDER,
                         (0, 0, self.window_width, self.window_height),
                         border_size, border_radius=10)

        # 绘制装饰性的角落纹饰
        corner_size = 20
        # 左上角
        pygame.draw.line(self.shop_surface, self.COLOR_TITLE,
                         (border_size, border_size),
                         (corner_size, border_size), 3)
        pygame.draw.line(self.shop_surface, self.COLOR_TITLE,
                         (border_size, border_size),
                         (border_size, corner_size), 3)

        # 右上角
        pygame.draw.line(self.shop_surface, self.COLOR_TITLE,
                         (self.window_width - border_size, border_size),
                         (self.window_width - corner_size, border_size), 3)
        pygame.draw.line(self.shop_surface, self.COLOR_TITLE,
                         (self.window_width - border_size, border_size),
                         (self.window_width - border_size, corner_size), 3)

        # 左下角
        pygame.draw.line(self.shop_surface, self.COLOR_TITLE,
                         (border_size, self.window_height - border_size),
                         (corner_size, self.window_height - border_size), 3)
        pygame.draw.line(self.shop_surface, self.COLOR_TITLE,
                         (border_size, self.window_height - border_size),
                         (border_size, self.window_height - corner_size), 3)

        # 右下角
        pygame.draw.line(self.shop_surface, self.COLOR_TITLE,
                         (self.window_width - border_size, self.window_height - border_size),
                         (self.window_width - corner_size, self.window_height - border_size), 3)
        pygame.draw.line(self.shop_surface, self.COLOR_TITLE,
                         (self.window_width - border_size, self.window_height - border_size),
                         (self.window_width - border_size, self.window_height - corner_size), 3)

        # 绘制标题
        title_text = self.title_font.render("神秘商店", True, self.COLOR_TITLE)
        title_rect = title_text.get_rect(centerx=self.window_width // 2, top=20)
        self.shop_surface.blit(title_text, title_rect)

        # 绘制分隔线
        pygame.draw.line(self.shop_surface, self.COLOR_BORDER,
                         (50, title_rect.bottom + 15),
                         (self.window_width - 50, title_rect.bottom + 15), 2)

        # 绘制底部信息
        info_text = self.info_font.render("按下对应数字键购买物品，按ESC退出", True, self.COLOR_TEXT)
        info_rect = info_text.get_rect(centerx=self.window_width // 2, bottom=self.window_height - 20)
        self.shop_surface.blit(info_text, info_rect)

    def _draw_item_card(self, item, x, y, width, height, hovered=False):
        # 基础卡片背景
        card_color = self.COLOR_HIGHLIGHT if hovered else (50, 50, 70)
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, card_color, card_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.COLOR_BORDER, card_rect, 2, border_radius=8)

        # 物品图标 - 位置调整
        icon_rect = item['icon'].get_rect(topleft=(x + 10, y + (height - item['icon'].get_height()) // 2))
        self.screen.blit(item['icon'], icon_rect)

        # 键位示意
        key_size = 24 # 减小按键尺寸
        key_rect = pygame.Rect(x + width - key_size - 10, y + 8, key_size, key_size)
        pygame.draw.rect(self.screen, (70, 70, 90), key_rect, border_radius=5)
        pygame.draw.rect(self.screen, self.COLOR_BORDER, key_rect, 1, border_radius=5)

        key_text = self.item_font.render(item['label'], True, self.COLOR_TEXT)
        key_text_rect = key_text.get_rect(center=key_rect.center)
        self.screen.blit(key_text, key_text_rect)

        # 物品名称 - 位置调整
        name_text = self.item_font.render(item['name'], True, self.COLOR_TEXT)
        name_rect = name_text.get_rect(topleft=(x + 45, y + 10))
        self.screen.blit(name_text, name_rect)

        # 物品描述 - 位置调整，颜色变淡
        desc_lines = []
        desc_words = item['description'].split()
        line = ""
        for word in desc_words:
            test_line = line + word + " "
            # 检查行宽度，如果太宽则换行
            if self.info_font.size(test_line)[0] > width - 50:
                desc_lines.append(line)
                line = word + " "
            else:
                line = test_line
        if line:
            desc_lines.append(line)

        # 绘制描述（可能有多行）
        for i, line in enumerate(desc_lines):
            desc_text = self.info_font.render(line, True, self.COLOR_DESC)
            desc_rect = desc_text.get_rect(topleft=(x + 45, y + 35 + i * 18))
            self.screen.blit(desc_text, desc_rect)

        # 价格（根据玩家能否负担变色）- 移至底部
        affordable = self.player.coins >= item['price']
        price_color = self.COLOR_AFFORDABLE if affordable else self.COLOR_UNAFFORDABLE

        price_text = self.price_font.render(f"{item['price']} 金币", True, price_color)
        price_rect = price_text.get_rect(bottomright=(x + width - 10, y + height - 10))
        self.screen.blit(price_text, price_rect)

        # 金币图标
        coin_radius = 6 # 减小金币尺寸
        coin_center = (price_rect.left - coin_radius - 5, price_rect.centery)
        pygame.draw.circle(self.screen, self.COLOR_PRICE, coin_center, coin_radius)
        pygame.draw.circle(self.screen, self.COLOR_SHINE,
                        (coin_center[0] - 2, coin_center[1] - 2), 2)

        return card_rect

    def _buy_small_hp(self):
        """购买小HP药水"""
        price = 100 * self.floor
        if self.player.coins >= price:
            self.player.hp = min(self.player.hp + 1000 * self.floor, self.player.max_hp)
            self.player.coins -= price
            self.message = f"购买成功！恢复 {1000 * self.floor} 点生命值"
            self._create_purchase_effect((255, 0, 0))
            return True
        else:
            self.message = "金币不足！"
            return False

    def _buy_small_atk(self):
        """购买小攻击宝石"""
        price = 100 * self.floor
        if self.player.coins >= price:
            self.player.base_atk += 5 * self.floor
            self.player.coins -= price
            self.message = f"购买成功！攻击力 +{5 * self.floor}"
            self._create_purchase_effect((255, 100, 100))
            return True
        else:
            self.message = "金币不足！"
            return False

    def _buy_small_def(self):
        """购买小防御宝石"""
        price = 100 * self.floor
        if self.player.coins >= price:
            self.player.base_defense += 5 * self.floor
            self.player.coins -= price
            self.message = f"购买成功！防御力 +{5 * self.floor}"
            self._create_purchase_effect((100, 100, 255))
            return True
        else:
            self.message = "金币不足！"
            return False

    def _buy_large_hp(self):
        """购买大HP药水"""
        price = 1000 * self.floor
        if self.player.coins >= price:
            self.player.hp = min(self.player.hp + 10000 * self.floor, self.player.max_hp)
            self.player.coins -= price
            self.message = f"购买成功！恢复 {10000 * self.floor} 点生命值"
            self._create_purchase_effect((200, 0, 0), large=True)
            return True
        else:
            self.message = "金币不足！"
            return False

    def _buy_large_atk(self):
        """购买大攻击宝石"""
        price = 1000 * self.floor
        if self.player.coins >= price:
            self.player.base_atk += 50 * self.floor
            self.player.coins -= price
            self.message = f"购买成功！攻击力 +{50 * self.floor}"
            self._create_purchase_effect((255, 50, 50), large=True)
            return True
        else:
            self.message = "金币不足！"
            return False

    def _buy_large_def(self):
        """购买大防御宝石"""
        price = 1000 * self.floor
        if self.player.coins >= price:
            self.player.base_defense += 50 * self.floor
            self.player.coins -= price
            self.message = f"购买成功！防御力 +{50 * self.floor}"
            self._create_purchase_effect((50, 50, 255), large=True)
            return True
        else:
            self.message = "金币不足！"
            return False

    def _buy_small_mp(self):
        """购买小MP药水"""
        price = 100 * self.floor
        if self.player.coins >= price:
            self.player.mp = min(self.player.mp + 500 * self.floor, self.player.max_mp)
            self.player.coins -= price
            self.message = f"购买成功！恢复 {500 * self.floor} 点魔法值"
            self._create_purchase_effect((0, 0, 255))
            return True
        else:
            self.message = "金币不足！"
            return False

    def _buy_large_mp(self):
        """购买大MP药水"""
        price = 1000 * self.floor
        if self.player.coins >= price:
            self.player.mp = min(self.player.mp + 5000 * self.floor, self.player.max_mp)
            self.player.coins -= price
            self.message = f"购买成功！恢复 {5000 * self.floor} 点魔法值"
            self._create_purchase_effect((0, 0, 200), large=True)
            return True
        else:
            self.message = "金币不足！"
            return False

    def _create_purchase_effect(self, color, large=False):
        """创建购买特效 - 已禁用粒子效果和音效"""
        # 所有效果已移除，保留函数以维持接口一致性
        pass

    def run(self):
        """运行商店界面"""
        clock = pygame.time.Clock()
        running = True

        # 创建半透明遮罩
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))  # 半透明黑色背景

        while running:
            dt = clock.tick(60) / 1000  # 转换为秒
            current_time = pygame.time.get_ticks()

            # 处理输入
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    else:
                        # 检查是否按下了商品对应的键
                        for item in self.items:
                            if event.key == item['key']:
                                success = item['action']()
                                if success:
                                    self.message_time = current_time

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # 左键点击
                        # 检查是否点击了退出按钮
                        if self.exit_button.collidepoint(event.pos):
                            running = False

                        # 检查是否点击了商品
                        for i, item in enumerate(self.items):
                            item_rect = self._get_item_rect(i)
                            if item_rect.collidepoint(event.pos):
                                success = item['action']()
                                if success:
                                    self.message_time = current_time

            # 更新鼠标悬停状态
            mouse_pos = pygame.mouse.get_pos()
            self.hovered_item = None
            for i, item in enumerate(self.items):
                item_rect = self._get_item_rect(i)
                if item_rect.collidepoint(mouse_pos):
                    self.hovered_item = i
                    break

            self.hovered_button = self.exit_button.collidepoint(mouse_pos)

            # 绘制界面
            self._draw_shop(current_time)

            pygame.display.flip()

    def _get_item_rect(self, index):
        # 计算行和列 - 改为4列2行布局
        row = index // 4
        col = index % 4

        # 计算卡片尺寸和位置 - 调整为更适合的尺寸
        card_width = (self.window_width - 100) // 4  # 增加间距，4列布局
        card_height = 110  # 增加卡片高度，避免文字重叠
        card_x = self.window_x + 30 + col * (card_width + 10) # 减小间距
        card_y = self.window_y + 100 + row * (card_height + 20)

        return pygame.Rect(card_x, card_y, card_width, card_height)

    def _draw_shop(self, current_time):
        # 绘制商店窗口
        self.screen.blit(self.shop_surface, (self.window_x, self.window_y))

        # 绘制当前金币（左上角）
        coin_text = self.price_font.render(f"金币: {self.player.coins}", True, self.COLOR_PRICE)
        coin_rect = coin_text.get_rect(topleft=(self.window_x + 30, self.window_y + 70))
        self.screen.blit(coin_text, coin_rect)

        # 绘制金币图标
        coin_radius = 10
        coin_center = (coin_rect.right + coin_radius + 5, coin_rect.centery)
        pygame.draw.circle(self.screen, self.COLOR_PRICE, coin_center, coin_radius)
        # 添加金币图标高光效果
        pygame.draw.circle(self.screen, self.COLOR_SHINE,
                           (coin_center[0] - 3, coin_center[1] - 3), 3)

        # 绘制楼层信息（右上角）
        floor_text = self.price_font.render(f"当前楼层: {self.floor}", True, self.COLOR_TEXT)
        floor_rect = floor_text.get_rect(topright=(self.window_x + self.window_width - 30, self.window_y + 70))
        self.screen.blit(floor_text, floor_rect)

        # 绘制商品项目
        for i, item in enumerate(self.items):
            rect = self._get_item_rect(i)
            self._draw_item_card(
                item, rect.x, rect.y, rect.width, rect.height,
                hovered=(i == self.hovered_item)
            )

        # 绘制退出按钮
        button_color = self.COLOR_BUTTON_HOVER if self.hovered_button else self.COLOR_BUTTON
        pygame.draw.rect(self.screen, button_color, self.exit_button, border_radius=5)
        pygame.draw.rect(self.screen, self.COLOR_BORDER, self.exit_button, 2, border_radius=5)

        exit_text = self.item_font.render("退出", True, self.COLOR_TEXT)
        exit_rect = exit_text.get_rect(center=self.exit_button.center)
        self.screen.blit(exit_text, exit_rect)

        # 绘制消息
        if self.message and current_time - self.message_time < self.message_duration:
            # 消息框背景
            msg_width = 450
            msg_height = 60
            msg_x = self.window_x + (self.window_width - msg_width) // 2
            msg_y = self.window_y + 20

            msg_rect = pygame.Rect(msg_x, msg_y, msg_width, msg_height)
            pygame.draw.rect(self.screen, (50, 50, 70, 200), msg_rect, border_radius=10)
            pygame.draw.rect(self.screen, self.COLOR_PRICE, msg_rect, 2, border_radius=10)

            # 消息文本
            msg_text = self.item_font.render(self.message, True, self.COLOR_TEXT)
            msg_text_rect = msg_text.get_rect(center=msg_rect.center)
            self.screen.blit(msg_text, msg_text_rect)


def shop_screen(screen, player, floor):
    shop = DungeonShop(screen, player, floor)
    shop.run()

# -------------- 攻击类特效 -------------------


# 新增攻击特效类
class WeaponSwingEffect:
    def __init__(self, x, y, duration=0.2):
        self.x = x
        self.y = y
        self.progress = 0
        self.duration = duration

    def update(self, dt):
        self.progress += dt / self.duration
        return self.progress < 1.0

    def draw(self, screen):
        alpha = int(255 * (1 - self.progress))
        angle = 30 + 120 * self.progress
        center = (self.x * TILE_SIZE + TILE_SIZE // 2,
                  self.y * TILE_SIZE + TILE_SIZE // 2)
        length = TILE_SIZE * 1.2

        # 绘制弧线
        start_angle = math.radians(angle)
        end_angle = start_angle + math.radians(90)
        pygame.draw.arc(screen, (255, 255, 0, alpha),
                        (center[0] - length // 2, center[1] - length // 2, length, length),
                        start_angle, end_angle, 3)


class ProjectileEffect:
    def __init__(self, start, end, speed, damage):
        self.start = (start[0] * TILE_SIZE + TILE_SIZE // 2,
                      start[1] * TILE_SIZE + TILE_SIZE // 2)
        self.end = (end[0] * TILE_SIZE + TILE_SIZE // 2,
                    end[1] * TILE_SIZE + TILE_SIZE // 2)
        self.speed = speed
        self.damage = damage
        self.direction = (self.end[0] - self.start[0],
                          self.end[1] - self.start[1])
        distance = math.hypot(*self.direction)
        if distance == 0:
            self.direction = (0, 0)
        else:
            self.direction = (self.direction[0] / distance,
                              self.direction[1] / distance)
        self.pos = list(self.start)

    def update(self, dt):
        self.pos[0] += self.direction[0] * self.speed * dt
        self.pos[1] += self.direction[1] * self.speed * dt
        # 碰撞检测
        if math.hypot(self.pos[0] - self.end[0], self.pos[1] - self.end[1]) < 5:
            return False
        return True

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 0, 0),
                           (int(self.pos[0]), int(self.pos[1])), 3)


class ClawEffect:
    def __init__(self, x, y, direction, duration=0.3):
        """
        爪击特效
        :param x: 怪物X坐标
        :param y: 怪物Y坐标
        :param direction: 攻击方向元组 (dx, dy)
        :param duration: 动画持续时间（秒）
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.duration = duration
        self.progress = 0  # 动画进度 0~1
        self.claw_colors = [
            (255, 0, 0, 200),  # 红色爪痕
            (200, 100, 0, 150),  # 橙色拖影
            (150, 50, 0, 100)  # 深红残影
        ]

    def update(self, dt):
        """更新动画进度"""
        self.progress += dt / self.duration
        return self.progress < 1.0  # 返回是否还需更新

    def draw(self, screen):
        """绘制爪击特效"""
        center_x = self.x * TILE_SIZE + TILE_SIZE // 2
        center_y = self.y * TILE_SIZE + TILE_SIZE // 2

        # 根据方向计算偏移
        dx, dy = self.direction
        angle = math.atan2(dy, dx)  # 攻击方向的角度

        # 动态参数
        max_length = TILE_SIZE * 1.5 * self.progress
        alpha = int(255 * (1 - self.progress))
        spread = math.sin(self.progress * math.pi) * 30  # 爪痕展开角度

        # 绘制三层爪痕（从内到外）
        for i, color in enumerate(self.claw_colors):
            # 计算当前层的参数
            length = max_length - i * 10
            current_alpha = max(0, color[3] - i * 50)

            # 计算三个爪尖的位置
            points = []
            for j in range(3):
                angle_offset = math.radians(-spread + j * spread)
                claw_angle = angle + angle_offset
                x = center_x + math.cos(claw_angle) * length
                y = center_y + math.sin(claw_angle) * length
                points.append((x, y))

            # 绘制渐变爪痕
            for j in range(len(points) - 1):
                start = points[j]
                end = points[j + 1]
                pygame.draw.line(screen, (*color[:3], current_alpha),
                                 start, end, 3 - i)

            # 添加随机血滴
            if random.random() < 0.3:
                blood_pos = random.choice(points)
                pygame.draw.circle(screen, (139, 0, 0, alpha),
                                   (int(blood_pos[0]), int(blood_pos[1])),
                                   random.randint(2, 3))


# --------------- 技能类 ----------------

# --------------- 三连斩 ----------------

class TripleAttack:
    def __init__(self, player_pos, attack_range=2, damage_multiplier=(0.8, 1.0, 1.5)):
        self.player_pos = player_pos
        self.range = attack_range
        self.damage_multipliers = damage_multiplier
        self.duration = 0.75  # Total duration of triple attack
        self.progress = 0.0
        self.slash_delay = 0.2  # Delay between slashes
        self.slashes = [
            {'start_time': 0.0, 'angle': 45, 'color': (220, 180, 20), 'hit': False, 'target': None},  # Gold
            {'start_time': self.slash_delay, 'angle': 135, 'color': (200, 70, 20), 'hit': False, 'target': None},
            # Orange-red
            {'start_time': self.slash_delay * 2, 'angle': 90, 'color': (220, 20, 60), 'hit': False, 'target': None}
            # Crimson
        ]
        self.hit_effects = []

    def update(self, dt, monsters):
        self.progress += dt / self.duration
        damage_results = []

        # Check for new hits
        for i, slash in enumerate(self.slashes):
            slash_time = slash['start_time'] / self.duration
            if self.progress >= slash_time and not slash['hit']:
                eligible_targets = [m for m in monsters if self._calculate_distance(
                    self.player_pos, (m.x, m.y)) <= self.range and m.hp > 0]

                if eligible_targets:
                    # Select a random target for this slash
                    target = random.choice(eligible_targets)
                    slash['target'] = target

                    # Add visual effect
                    self.hit_effects.append({
                        'pos': (target.x * TILE_SIZE + TILE_SIZE // 2,
                                target.y * TILE_SIZE + TILE_SIZE // 2),
                        'time': 0.3,
                        'angle': slash['angle'],
                        'color': slash['color'],
                        'slash_index': i  # 添加斩击索引，表示第几击
                    })

                    # Record damage
                    damage_results.append((target, self.damage_multipliers[i]))

                slash['hit'] = True

        # Update hit effects
        for effect in self.hit_effects[:]:
            effect['time'] -= dt
            if effect['time'] <= 0:
                self.hit_effects.remove(effect)

        # Check if effect is still active
        return self.progress < 1.0 or self.hit_effects, damage_results

    def _calculate_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def draw(self, screen):
        for effect in self.hit_effects:
            self._draw_slash(screen, effect)

    def _draw_slash(self, screen, effect):
        pos = effect['pos']
        angle = math.radians(effect['angle'])
        color = effect['color']
        slash_index = effect.get('slash_index', 0)  # 获取斩击索引
        time_ratio = effect['time'] / 0.3  # 时间比例，用于淡出效果
        alpha = int(255 * time_ratio)

        # 根据斩击索引决定不同的斩击风格
        if slash_index == 0:  # 第一斩：金色，直线型
            self._draw_straight_slash(screen, pos, angle, color, alpha)
            self._draw_impact_marks(screen, pos, color, alpha, "small")
        elif slash_index == 1:  # 第二斩：橙红色，十字型
            self._draw_cross_slash(screen, pos, angle, color, alpha)
            self._draw_impact_marks(screen, pos, color, alpha, "medium")
        else:  # 第三斩：深红色，爆裂型
            self._draw_burst_slash(screen, pos, angle, color, alpha)
            self._draw_impact_marks(screen, pos, color, alpha, "large")

    def _draw_straight_slash(self, screen, pos, angle, color, alpha):
        """绘制直线型斩击"""
        # 主要斩击线
        length = TILE_SIZE * 1.7
        width = 5

        start_x = pos[0] - math.cos(angle) * length / 2
        start_y = pos[1] - math.sin(angle) * length / 2
        end_x = pos[0] + math.cos(angle) * length / 2
        end_y = pos[1] + math.sin(angle) * length / 2

        # 绘制主线
        pygame.draw.line(
            screen,
            (*color, alpha),
            (int(start_x), int(start_y)),
            (int(end_x), int(end_y)),
            width
        )

        # 绘制外光晕
        glow_color = (min(255, color[0] + 50), min(255, color[1] + 50), min(255, color[2] + 50), alpha // 2)
        pygame.draw.line(
            screen,
            glow_color,
            (int(start_x), int(start_y)),
            (int(end_x), int(end_y)),
            width + 3
        )

    def _draw_cross_slash(self, screen, pos, angle, color, alpha):
        """绘制十字型斩击"""
        length = TILE_SIZE * 1.5
        width = 4

        # 第一条线（主角度）
        start_x1 = pos[0] - math.cos(angle) * length / 2
        start_y1 = pos[1] - math.sin(angle) * length / 2
        end_x1 = pos[0] + math.cos(angle) * length / 2
        end_y1 = pos[1] + math.sin(angle) * length / 2

        # 第二条线（垂直于主角度）
        perpendicular = angle + math.pi / 2
        start_x2 = pos[0] - math.cos(perpendicular) * length / 3
        start_y2 = pos[1] - math.sin(perpendicular) * length / 3
        end_x2 = pos[0] + math.cos(perpendicular) * length / 3
        end_y2 = pos[1] + math.sin(perpendicular) * length / 3

        # 绘制十字交叉线
        pygame.draw.line(
            screen,
            (*color, alpha),
            (int(start_x1), int(start_y1)),
            (int(end_x1), int(end_y1)),
            width
        )
        pygame.draw.line(
            screen,
            (*color, alpha),
            (int(start_x2), int(start_y2)),
            (int(end_x2), int(end_y2)),
            width - 1
        )

        # 交点处添加亮点
        highlight_color = (min(255, color[0] + 70), min(255, color[1] + 70), min(255, color[2] + 70), alpha)
        pygame.draw.circle(screen, highlight_color, (int(pos[0]), int(pos[1])), width)

    def _draw_burst_slash(self, screen, pos, angle, color, alpha):
        """绘制爆裂型斩击（最终一击）"""
        center_x, center_y = int(pos[0]), int(pos[1])
        radius = TILE_SIZE * 0.8

        # 中心爆发光晕
        glow_surface = pygame.Surface((int(radius * 2), int(radius * 2)), pygame.SRCALPHA)
        for r in range(int(radius), 0, -4):
            # 渐变透明度
            circle_alpha = min(alpha, int(alpha * (r / radius)))
            glow_color = (*color, circle_alpha)
            pygame.draw.circle(glow_surface, glow_color, (int(radius), int(radius)), r, 2)

        # 添加放射状线条
        line_count = 12
        line_length = radius * 1.3
        for i in range(line_count):
            line_angle = 2 * math.pi * i / line_count
            start_x = radius + radius * 0.5 * math.cos(line_angle)
            start_y = radius + radius * 0.5 * math.sin(line_angle)
            end_x = radius + line_length * math.cos(line_angle)
            end_y = radius + line_length * math.sin(line_angle)

            # 线宽度随时间变化
            line_width = max(1, int(3 * alpha / 255))
            pygame.draw.line(
                glow_surface,
                (*color, alpha),
                (int(start_x), int(start_y)),
                (int(end_x), int(end_y)),
                line_width
            )

        # 绘制到屏幕
        screen.blit(glow_surface, (center_x - int(radius), center_y - int(radius)))

    def _draw_impact_marks(self, screen, pos, color, alpha, size):
        """绘制斩击痕迹"""
        center_x, center_y = int(pos[0]), int(pos[1])

        if size == "small":
            # 小型痕迹：简单的交叉
            pygame.draw.line(
                screen,
                (*color, alpha),
                (center_x - 6, center_y - 6),
                (center_x + 6, center_y + 6),
                2
            )
            pygame.draw.line(
                screen,
                (*color, alpha),
                (center_x - 6, center_y + 6),
                (center_x + 6, center_y - 6),
                2
            )

        elif size == "medium":
            # 中型痕迹：带有些许不规则的星形痕迹
            points = []
            point_count = 5
            for i in range(point_count):
                angle = 2 * math.pi * i / point_count
                # 内外半径交替，形成星形
                radius = 7 if i % 2 == 0 else 4
                x = center_x + radius * math.cos(angle)
                y = center_y + radius * math.sin(angle)
                points.append((x, y))

            # 绘制连接的线段
            for i in range(point_count):
                start = points[i]
                end = points[(i + 1) % point_count]
                pygame.draw.line(
                    screen,
                    (*color, alpha),
                    start, end,
                    2
                )

        else:  # large
            # 大型痕迹：不规则的破碎痕迹
            # 中心破碎区
            pygame.draw.circle(screen, (*color, alpha), (center_x, center_y), 8)

            # 放射状破碎线
            for i in range(8):
                angle = 2 * math.pi * i / 8 + random.uniform(-0.2, 0.2)
                length = random.uniform(8, 14)
                end_x = center_x + length * math.cos(angle)
                end_y = center_y + length * math.sin(angle)

                # 有些线断开一点，增加破碎感
                if random.random() < 0.5:
                    mid_x = center_x + length * 0.6 * math.cos(angle)
                    mid_y = center_y + length * 0.6 * math.sin(angle)
                    pygame.draw.line(
                        screen,
                        (*color, alpha),
                        (center_x, center_y),
                        (mid_x, mid_y),
                        2
                    )
                    pygame.draw.line(
                        screen,
                        (*color, alpha),
                        (mid_x + 2 * math.cos(angle), mid_y + 2 * math.sin(angle)),
                        (end_x, end_y),
                        2
                    )
                else:
                    pygame.draw.line(
                        screen,
                        (*color, alpha),
                        (center_x, center_y),
                        (end_x, end_y),
                        2
                    )

            # 添加一些小碎片
            for _ in range(5):
                dist = random.uniform(6, 12)
                angle = random.uniform(0, 2 * math.pi)
                fragment_x = center_x + dist * math.cos(angle)
                fragment_y = center_y + dist * math.sin(angle)
                pygame.draw.circle(
                    screen,
                    (*color, alpha),
                    (int(fragment_x), int(fragment_y)),
                    random.randint(1, 2)
                )

# -------------------- 纯青烈焰重击 --------------


class BlueFireStrikeEffect:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.lifetime = 2.0
        self.flames = []
        # 生成火焰区域
        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                if abs(dx) + abs(dy) <= radius:
                    self.flames.append({
                        'pos': (x+dx, y+dy),
                        'particles': [self.create_particle(x+dx, y+dy) for _ in range(5)]
                    })

    def create_particle(self, x, y):
        return {
            'px': x * TILE_SIZE + random.randint(5, 25),
            'py': y * TILE_SIZE + random.randint(5, 25),
            'vx': random.uniform(-2, 2),
            'vy': random.uniform(-5, -2),
            'life': 1.0
        }

    def update(self, dt):
        self.lifetime -= dt
        for flame in self.flames:
            # 更新现有粒子
            for p in flame['particles']:
                p['px'] += p['vx']
                p['py'] += p['vy']
                p['vy'] += 0.3  # 重力
                p['life'] -= dt * 0.5
            # 生成新粒子
            if random.random() < 0.6:
                flame['particles'].append(self.create_particle(*flame['pos']))
            # 移除过期粒子
            flame['particles'] = [p for p in flame['particles'] if p['life'] > 0]
        return self.lifetime > 0

    def draw(self, screen):
        for flame in self.flames:
            # 绘制基底火焰
            rect = pygame.Rect(flame['pos'][0]*TILE_SIZE, flame['pos'][1]*TILE_SIZE,
                             TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (55, 175, 255), rect)
            # 绘制动态粒子
            for p in flame['particles']:
                alpha = int(255 * p['life'])
                color = (0, 105 - int(105*p['life']), 255, alpha)
                pygame.draw.circle(screen, color, (int(p['px']), int(p['py'])),
                                 int(3*p['life']))

# -------------- 烈焰重击 -----------------


class FireStrikeEffect:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.lifetime = 1.5
        self.flames = []
        # 生成火焰区域
        for dx in range(-radius, radius+1):
            for dy in range(-radius, radius+1):
                if abs(dx) + abs(dy) <= radius:
                    self.flames.append({
                        'pos': (x+dx, y+dy),
                        'particles': [self.create_particle(x+dx, y+dy) for _ in range(5)]
                    })

    def create_particle(self, x, y):
        return {
            'px': x * TILE_SIZE + random.randint(5, 25),
            'py': y * TILE_SIZE + random.randint(5, 25),
            'vx': random.uniform(-2, 2),
            'vy': random.uniform(-5, -2),
            'life': random.uniform(0.2, 0.6)
        }

    def update(self, dt):
        self.lifetime -= dt
        for flame in self.flames:
            # 更新现有粒子
            for p in flame['particles']:
                p['px'] += p['vx']
                p['py'] += p['vy']
                p['vy'] += 0.3  # 重力
                p['life'] -= dt * 0.5
            # 生成新粒子
            if random.random() < 0.6:
                flame['particles'].append(self.create_particle(*flame['pos']))
            # 移除过期粒子
            flame['particles'] = [p for p in flame['particles'] if p['life'] > 0]
        return self.lifetime > 0

    def draw(self, screen):
        for flame in self.flames:
            # 绘制基底火焰
            rect = pygame.Rect(flame['pos'][0]*TILE_SIZE, flame['pos'][1]*TILE_SIZE,
                             TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (200, 80, 0), rect)
            # 绘制动态粒子
            for p in flame['particles']:
                alpha = int(255 * p['life'])
                color = (255, 150 + int(105*p['life']), 0, alpha)
                pygame.draw.circle(screen, color, (int(p['px']), int(p['py'])),
                                 int(5*p['life']))

# 电击球闪电击


class ElectricEffect:
    def __init__(self, px, py):
        self.center_x = px * TILE_SIZE + TILE_SIZE // 2
        self.center_y = py * TILE_SIZE + TILE_SIZE // 2
        self.duration = 0.4  # 稍微延长持续时间
        self.time_passed = 0

        # 主电击效果
        self.sparks = []
        self.branches = []
        self.glow_radius = TILE_SIZE // 2

        # 生成多层次的电击效果
        self._generate_sparks()

    def _generate_sparks(self):
        # 主电击射线 - 从中心向外发散
        for _ in range(6):
            angle = random.uniform(0, 2 * math.pi)
            length = random.uniform(TILE_SIZE * 0.5, TILE_SIZE * 0.8)
            self.sparks.append({
                'angle': angle,
                'length': length,
                'width': random.uniform(1.5, 3),
                'segments': random.randint(3, 5),  # 闪电段数
                'lifetime': self.duration * random.uniform(0.7, 1.0),
                'color': (255, 255, 0) if random.random() > 0.4 else (200, 230, 255),
                'branches': []
            })

            # 每条主射线添加分支
            if random.random() > 0.3:
                for _ in range(random.randint(1, 2)):
                    fork_distance = random.uniform(0.3, 0.7)  # 从主射线的位置开始分叉
                    fork_angle = angle + random.uniform(-1, 1)  # 分叉角度
                    fork_length = length * random.uniform(0.4, 0.6)  # 分叉长度

                    self.sparks[-1]['branches'].append({
                        'distance': fork_distance,
                        'angle': fork_angle,
                        'length': fork_length,
                        'width': random.uniform(1, 2),
                        'lifetime': self.duration * random.uniform(0.5, 0.8)
                    })

    def update(self, dt):
        self.time_passed += dt

        # 周期性闪烁效果
        if self.time_passed > self.duration * 0.7 and random.random() > 0.7:
            self._generate_sparks()  # 随机再生成一些电火花

        return self.time_passed < self.duration

    def draw(self, screen):
        progress = self.time_passed / self.duration
        fade_factor = 1.0 - progress  # 随时间淡出

        # 绘制中心光晕
        glow_alpha = int(180 * fade_factor * (0.7 + 0.3 * math.sin(self.time_passed * 15)))
        glow_radius = self.glow_radius * (0.8 + 0.2 * math.sin(self.time_passed * 10))

        glow_surface = pygame.Surface((int(glow_radius * 2), int(glow_radius * 2)), pygame.SRCALPHA)
        pygame.draw.circle(glow_surface, (255, 255, 100, glow_alpha),
                           (int(glow_radius), int(glow_radius)), int(glow_radius))
        screen.blit(glow_surface,
                    (int(self.center_x - glow_radius), int(self.center_y - glow_radius)))

        # 绘制电击射线
        for spark in self.sparks:
            if self.time_passed > spark['lifetime']:
                continue

            spark_progress = self.time_passed / spark['lifetime']
            alpha = int(255 * (1.0 - spark_progress))

            # 生成闪电路径点
            points = self._generate_lightning_path(
                self.center_x, self.center_y,
                spark['angle'], spark['length'],
                spark['segments']
            )

            # 绘制主射线
            for i in range(len(points) - 1):
                # 随机闪烁效果
                if random.random() > 0.1 * spark_progress:  # 随时间增加闪烁概率
                    color = (*spark['color'], alpha)
                    width = max(1, spark['width'] * (1.0 - spark_progress))
                    pygame.draw.line(screen, color, points[i], points[i + 1], int(width))

            # 绘制分支
            for branch in spark['branches']:
                if self.time_passed > branch['lifetime']:
                    continue

                branch_progress = self.time_passed / branch['lifetime']
                branch_alpha = int(200 * (1.0 - branch_progress))

                # 计算分支起点
                branch_index = min(int(branch['distance'] * len(points)), len(points) - 1)
                if branch_index < 1:
                    continue

                branch_start = points[branch_index]

                # 生成分支路径
                branch_points = self._generate_lightning_path(
                    branch_start[0], branch_start[1],
                    branch['angle'], branch['length'],
                    max(2, spark['segments'] - 1)
                )

                # 绘制分支
                for i in range(len(branch_points) - 1):
                    if random.random() > 0.2 * branch_progress:
                        color = (*spark['color'], branch_alpha)
                        width = max(1, branch['width'] * (1.0 - branch_progress))
                        pygame.draw.line(screen, color, branch_points[i], branch_points[i + 1], int(width))

        # 随机添加电火花粒子
        if random.random() > 0.7:
            spark_pos = (
                self.center_x + random.uniform(-glow_radius, glow_radius) * 0.8,
                self.center_y + random.uniform(-glow_radius, glow_radius) * 0.8
            )
            spark_size = random.uniform(1, 3) * fade_factor
            spark_color = (255, 255, 100, int(200 * fade_factor))

            pygame.draw.circle(screen, spark_color,
                               (int(spark_pos[0]), int(spark_pos[1])), int(spark_size))

    def _generate_lightning_path(self, x, y, angle, length, segments):
        points = [(x, y)]

        current_x, current_y = x, y
        segment_length = length / segments

        for i in range(segments):
            # 增加随机偏移，但保持大致方向
            jitter_angle = angle + random.uniform(-0.5, 0.5)

            # 对于最后一段，减少偏移以保持目标方向
            if i == segments - 1:
                jitter_angle = angle + random.uniform(-0.2, 0.2)

            next_x = current_x + math.cos(jitter_angle) * segment_length
            next_y = current_y + math.sin(jitter_angle) * segment_length

            points.append((next_x, next_y))

            current_x, current_y = next_x, next_y

        return points


# --------------- 闪电链技能特效 ---------------
class LightningEffect:
    def __init__(self, start, end, duration=0.5, damage=0):
        self.start = start  # 起点屏幕坐标
        self.end = end  # 终点屏幕坐标
        self.damage = damage
        self.duration = duration
        self.progress = 0  # 动画进度 0~1
        self.particles = []  # 闪电粒子
        self.main_points = self._generate_lightning_points(start, end, branch_prob=0.3)

    def _generate_lightning_points(self, start, end, branch_prob=0.3):
        """生成带随机分叉的闪电路径"""
        points = [start]
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.hypot(dx, dy)
        segments = max(6, int(length / 10))

        for i in range(1, segments):
            t = i / segments
            base_x = start[0] + dx * t
            base_y = start[1] + dy * t
            offset_range = 25 * (1 - t ** 2)
            offset_x = random.uniform(-offset_range, offset_range)
            offset_y = random.uniform(-offset_range, offset_range)

            # 添加分叉点
            if random.random() < branch_prob:
                points.append((int(base_x + offset_x * 0.5), int(base_y + offset_y * 0.5)))

            points.append((int(base_x + offset_x), int(base_y + offset_y)))

        points.append(end)
        return points

    def _add_ion_sparks(self, pos, intensity=2.0):
        """生成炫酷的离子火花"""
        for _ in range(int(15 * intensity)):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 9) * intensity
            lifespan = random.uniform(0.1, 0.8)

            spark_color = random.choice([
                (255, 255, 200),  # 炽白色
                (255, 150, 255),  # 粉紫色
                (255, 100, 200),  # 霓虹粉
                (255, 51, 51)  # 猩红色
            ])

            self.particles.append({
                'pos': list(pos),
                'vel': [math.cos(angle) * speed, math.sin(angle) * speed],
                'life': lifespan,
                'max_life': lifespan,
                'size': random.uniform(0.2, 4),
                'color': spark_color
            })

    def update(self, dt):
        """更新闪电状态"""
        self.progress += dt / self.duration

        # 更新粒子系统
        for p in self.particles:
            p['pos'][0] += p['vel'][0] * dt * 60  # 调整速度系数
            p['pos'][1] += p['vel'][1] * dt * 60
            p['life'] -= dt
        self.particles = [p for p in self.particles if p['life'] > 0]

        return self.progress < 1.0

    def draw(self, screen):
        """绘制动态闪电效果"""
        alpha = int(255 * (1 - self.progress))

        # 绘制主闪电路径
        for i in range(len(self.main_points) - 1):
            start_pos = self.main_points[i]
            end_pos = self.main_points[i + 1]

            # 动态颜色系统
            base_color = random.choice([(255, 255, 0), (255, 165, 0)])
            color_variation = random.choice([
                base_color,
                (min(base_color[0] + 50, 255), min(base_color[1] + 50, 255), min(base_color[2] + 50, 255)),
                (max(base_color[0] - 50, 0), max(base_color[1] - 50, 0), max(base_color[2] - 50, 0))
            ])
            line_color = color_variation + (alpha,)

            # 动态线宽系统
            thickness = max(1, int(5 * (1 - self.progress)))
            pygame.draw.line(screen, line_color, start_pos, end_pos,
                             random.randint(1, thickness))  # 随机线宽增强质感

            # 生成随机分叉
            if random.random() < 0.3 and i < len(self.main_points) - 2:
                mid_point = (
                    (start_pos[0] + end_pos[0]) // 2 + random.randint(-5, 5),
                    (start_pos[1] + end_pos[1]) // 2 + random.randint(-5, 5)
                )
                branch_end = (
                    mid_point[0] + random.randint(-10, 10),
                    mid_point[1] + random.randint(-10, 10)
                )
                branch_points = self._generate_lightning_points(mid_point, branch_end, 0.5)

                # 绘制分支闪电
                for j in range(len(branch_points) - 1):
                    branch_color = (
                        min(color_variation[0] + 100, 255),
                        min(color_variation[1] + 100, 255),
                        min(color_variation[2] + 100, 255),
                        alpha // 2
                    )
                    pygame.draw.line(screen, branch_color,
                                     branch_points[j], branch_points[j + 1],
                                     max(1, thickness - 1))

                # 添加火花效果
                if random.random() < 0.1:
                    self._add_ion_sparks(mid_point, intensity=0.8)

        # 绘制动态粒子
        for p in self.particles:
            if p['life'] > 0:
                life_ratio = p['life'] / p['max_life']
                particle_alpha = int(255 * life_ratio * (1 - self.progress))

                # 核心亮光
                pygame.draw.circle(screen, p['color'] + (particle_alpha,),
                                   (int(p['pos'][0]), int(p['pos'][1])),
                                   p['size'] * life_ratio)

# -------------- 守护闪电 ----------------


class SummonLightningBall:
    def __init__(self, player, ball_count=6, duration=10.0, attack_range=6, attack_speed=1.0, damage_multiple=1.5):
        self.player = player
        self.duration = duration  # 球体存在时间（秒）
        self.lifetime = duration  # 剩余生命周期
        self.attack_range = attack_range  # 攻击范围（格）
        self.ball_count = ball_count  # 闪电球数量

        # 创建多个闪电球
        self.lightning_balls = []
        for i in range(ball_count):
            self.lightning_balls.append(self.LightningBall(
                player,
                orbit_angle=int(2 * math.pi * i / ball_count),  # 均匀分布在圆周上
                orbit_speed=1.0 + random.uniform(-0.3, 0.3),  # 略微不同的轨道速度
                attack_speed=attack_speed,
                damage_multiple=damage_multiple
            ))

    def update(self, dt, game):
        # 更新生命周期
        self.lifetime -= dt
        if self.lifetime <= 0:
            # 生成消散特效
            for ball in self.lightning_balls:
                for _ in range(10):  # 每个球生成10个粒子
                    game.fear_particles.append({
                        'pos': list(ball.position),
                        'vel': [random.uniform(-8, 8), random.uniform(-8, 8)],
                        'life': random.uniform(0.5, 1.2),
                        'max_life': 1.2,
                        'size': random.uniform(2, 5),
                        'color': (0, 191, 255)
                    })
            return False  # 生命周期结束，移除所有球体

        # 更新所有球体
        for ball in self.lightning_balls:
            ball.update(dt, game)

        # 寻找范围内的目标
        targets = []
        for monster in game.monsters:
            distance = game.calculate_distance(
                (game.player.x, game.player.y),
                (monster.x, monster.y)
            )
            if distance <= self.attack_range:
                targets.append(monster)

        # 每个球体尝试攻击目标
        if targets:
            for ball in self.lightning_balls:
                ball.try_attack(targets, game)

        return True  # 继续存在

    def draw(self, screen):
        for ball in self.lightning_balls:
            ball.draw(screen)

    # 内部类: 单个闪电球
    class LightningBall:
        def __init__(self, player, orbit_angle=0, orbit_speed=2.0, attack_speed=1.0, damage_multiple=1.5):
            self.player = player

            # 轨道参数
            self.orbit_radius = TILE_SIZE * 2.0  # 环绕玩家的距离
            self.orbit_angle = orbit_angle  # 初始角度
            self.orbit_speed = orbit_speed  # 轨道速度（弧度/秒）

            # 攻击参数
            self.attack_speed = attack_speed  # 每秒攻击次数
            self.attack_cooldown = random.uniform(0, 1.0 / attack_speed)  # 随机初始冷却
            self.damage_multiple = damage_multiple  # 伤害倍率

            # 位置为玩家位置的偏移
            player_pos = (player.x * TILE_SIZE + TILE_SIZE // 2,
                          player.y * TILE_SIZE + TILE_SIZE // 2)
            self.position = [
                player_pos[0] + math.cos(orbit_angle) * self.orbit_radius,
                player_pos[1] + math.sin(orbit_angle) * self.orbit_radius
            ]

            # 视觉参数
            self.size = 11  # 球体基础尺寸
            self.particles = []  # 粒子效果列表
            self.lightning_connections = []  # 闪电连接点

            # 添加初始粒子效果
            for _ in range(10):
                self.add_particle()

        def update(self, dt, game):
            # 更新轨道位置
            self.orbit_angle += self.orbit_speed * dt
            player_center = (game.player.x * TILE_SIZE + TILE_SIZE // 2,
                             game.player.y * TILE_SIZE + TILE_SIZE // 2)
            self.position = [
                player_center[0] + math.cos(self.orbit_angle) * self.orbit_radius,
                player_center[1] + math.sin(self.orbit_angle) * self.orbit_radius
            ]

            # 更新攻击冷却
            if self.attack_cooldown > 0:
                self.attack_cooldown -= dt

            # 更新粒子效果
            for p in self.particles[:]:
                p['pos'][0] += p['vel'][0] * dt * 60
                p['pos'][1] += p['vel'][1] * dt * 60
                p['life'] -= dt
                if p['life'] <= 0:
                    self.particles.remove(p)

            # 定期添加新粒子
            if random.random() < 0.2:
                self.add_particle()

            # 动态更新闪电连接点
            if random.random() < 0.15 or not self.lightning_connections:
                self.lightning_connections = []
                connection_count = random.randint(2, 3)
                for _ in range(connection_count):
                    angle = random.uniform(0, 2 * math.pi)
                    distance = random.uniform(self.size * 1.2, self.size * 2)
                    self.lightning_connections.append({
                        'pos': [
                            self.position[0] + math.cos(angle) * distance,
                            self.position[1] + math.sin(angle) * distance
                        ],
                        'life': random.uniform(0.2, 0.4)
                    })

            # 更新连接点生命周期
            for conn in self.lightning_connections[:]:
                conn['life'] -= dt
                if conn['life'] <= 0:
                    self.lightning_connections.remove(conn)

        def try_attack(self, targets, game):
            # 如果有攻击冷却，不攻击
            if self.attack_cooldown > 0 or not targets:
                return

            # 选择一个随机目标攻击
            target = random.choice(targets)

            # 计算伤害（带随机波动）
            base_damage = game.player.atk * self.damage_multiple
            damage_variation = random.uniform(0.8, 1.2)
            damage = base_damage * damage_variation
            actual_damage = max(damage - target.defense, 0)

            # 应用伤害
            target.hp -= actual_damage

            # 添加闪电效果
            start_pos = list(self.position)
            # 闪电起点小幅度随机偏移，增加视觉多样性
            start_jitter = [random.uniform(-5, 5), random.uniform(-5, 5)]
            start_pos[0] += start_jitter[0]
            start_pos[1] += start_jitter[1]

            # 闪电终点为怪物位置（也带随机偏移）
            end_pos = [target.x * TILE_SIZE + TILE_SIZE // 2,
                       target.y * TILE_SIZE + TILE_SIZE // 2]
            end_jitter = [random.uniform(-5, 5), random.uniform(-5, 5)]
            end_pos[0] += end_jitter[0]
            end_pos[1] += end_jitter[1]

            # 创建闪电效果
            effect = LightningEffect(
                start=tuple(start_pos),
                end=tuple(end_pos),
                duration=0.4,
                damage=actual_damage
            )
            game.skill_effects.append(effect)
            game.add_message(f"守护闪电球对{target.name}造成{int(actual_damage)}点伤害!") # 添加攻击信息
            self.attack_cooldown = 1.0 / self.attack_speed # 设置攻击冷却

        def add_particle(self):
            """添加能量粒子效果"""
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 5)
            lifespan = random.uniform(0.2, 0.8)

            # 随机选择粒子颜色
            spark_color = random.choice([
                (255, 255, 200),  # 明亮白色
                (150, 150, 255),  # 淡蓝色
                (0, 191, 255),  # 深蓝色
                (100, 220, 255)  # 天蓝色
            ])

            self.particles.append({
                'pos': list(self.position),
                'vel': [math.cos(angle) * speed, math.sin(angle) * speed],
                'life': lifespan,
                'max_life': lifespan,
                'size': random.uniform(1, 2.5),
                'color': spark_color
            })

        def draw(self, screen):
            anim_time = pygame.time.get_ticks()

            # 球体核心脉动效果
            pulse = 0.5 + 0.5 * math.sin(anim_time / 200 + self.orbit_angle)
            core_radius = int(self.size * (1 + 0.2 * pulse))

            # 绘制多层递减透明度的核心
            for i in range(3):
                alpha = 200 - i * 50
                radius = core_radius - i * 2

                if radius <= 0:
                    continue

                temp_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                color = (0, 191, 255, alpha) if i % 2 == 0 else (100, 180, 255, alpha)
                pygame.draw.circle(temp_surf, color, (radius, radius), radius)
                screen.blit(temp_surf, (int(self.position[0] - radius), int(self.position[1] - radius)))

            # 绘制能量粒子
            for p in self.particles:
                life_ratio = p['life'] / p['max_life']
                particle_alpha = int(255 * life_ratio)

                temp_surf = pygame.Surface((int(p['size'] * 2), int(p['size'] * 2)), pygame.SRCALPHA)
                pygame.draw.circle(temp_surf, (*p['color'], particle_alpha),
                                   (int(p['size']), int(p['size'])),
                                   int(p['size'] * life_ratio))
                screen.blit(temp_surf, (int(p['pos'][0] - p['size']), int(p['pos'][1] - p['size'])))

            # 绘制闪电连接
            for conn in self.lightning_connections:
                # 绘制从球心到连接点的闪电
                life_ratio = conn['life'] / 0.4  # 假设最大生命周期为0.4

                # 生成闪电路径点
                points = []
                # 起点为球心
                points.append(tuple(self.position))

                # 生成中间随机点
                segments = random.randint(1, 3)
                for i in range(segments):
                    t = (i + 1) / (segments + 1)
                    mid_x = self.position[0] + (conn['pos'][0] - self.position[0]) * t
                    mid_y = self.position[1] + (conn['pos'][1] - self.position[1]) * t

                    # 添加随机偏移
                    jitter_range = 8 * (1 - t) * life_ratio
                    jitter_x = random.uniform(-jitter_range, jitter_range)
                    jitter_y = random.uniform(-jitter_range, jitter_range)

                    points.append((mid_x + jitter_x, mid_y + jitter_y))

                # 终点为连接点
                points.append(tuple(conn['pos']))

                # 绘制闪电线段
                for i in range(len(points) - 1):
                    # 随机选择颜色
                    color = random.choice([
                        (150, 220, 255, int(255 * life_ratio)),
                        (200, 230, 255, int(255 * life_ratio)),
                        (100, 180, 255, int(255 * life_ratio))
                    ])

                    pygame.draw.line(screen, color, points[i], points[i + 1],
                                     max(1, int(3 * life_ratio)))

# ---------------- 圣光球 -------------------------


class HolyBallEffect:
    def __init__(self, player_pos, ball_count=6, seek_range=10, damage_multiplier=2.5,
                 is_monster_skill=False, target=None, monster=None):
        self.player_pos = player_pos
        self.ball_count = ball_count
        self.seek_range = seek_range
        self.damage_multiplier = damage_multiplier
        self.duration = 5.0
        self.progress = 0.0

        # 新增参数用于区分怪物/玩家技能
        self.is_monster_skill = is_monster_skill
        self.target = target  # 怪物技能时为玩家对象，玩家技能时为None
        self.monster = monster  # 怪物技能时为怪物对象，玩家技能时为None

        # Lightning balls data
        self.balls = []
        self.targets = []
        self.explosions = []

        # Initialize the balls with random positions around the origin position
        for i in range(ball_count):
            angle = math.pi * 2 * i / ball_count
            offset_x = math.cos(angle) * 3
            offset_y = math.sin(angle) * 3
            self.balls.append({
                'pos': [
                    player_pos[0] + offset_x,
                    player_pos[1] + offset_y
                ],
                'screen_pos': [
                    (player_pos[0] + offset_x) * TILE_SIZE + TILE_SIZE // 2,
                    (player_pos[1] + offset_y) * TILE_SIZE + TILE_SIZE // 2
                ],
                'size': random.uniform(0.4, 0.6) * TILE_SIZE,
                'phase': random.uniform(0, math.pi * 2),
                'speed': random.uniform(3.0, 6.0),
                'state': 'seeking',  # States: seeking, attacking, exploded
                'target': None,
                'color': self._generate_random_holy_color(),
            })

    def _generate_random_holy_color(self):
        colors = [
            (255, 215, 0),  # Gold
            (240, 240, 200),  # Soft white
            (135, 206, 250),  # Light sky blue
            (255, 255, 240),  # Ivory
            (218, 165, 32)  # Golden rod
        ]
        return random.choice(colors)

    def update(self, dt, monsters_or_player):
        self.progress += dt / self.duration
        damage_results = []

        # 根据释放者类型确定目标列表
        if self.is_monster_skill:
            # 怪物技能 - 目标是玩家
            player = self.target
        else:
            # 玩家技能 - 目标是怪物列表
            monsters = monsters_or_player

        # Process each ball
        for ball in self.balls:
            if ball['state'] == 'exploded':
                continue

            # Seeking logic - find a target if needed
            if ball['state'] == 'seeking':
                if not ball['target']:
                    if self.is_monster_skill:
                        # 怪物技能直接瞄准玩家
                        distance = self._calculate_distance(
                            (ball['pos'][0], ball['pos'][1]),
                            (player.x, player.y)
                        )
                        if distance <= self.seek_range:
                            ball['target'] = player
                            ball['state'] = 'attacking'
                        else:
                            # 没有目标时围绕原点移动
                            self._update_seeking_movement(ball, dt)
                    else:
                        # 玩家技能寻找怪物目标
                        potential_targets = []
                        for monster in monsters:
                            distance = self._calculate_distance(
                                (ball['pos'][0], ball['pos'][1]),
                                (monster.x, monster.y)
                            )
                            if distance <= self.seek_range:
                                potential_targets.append((distance, monster))

                        # Select closest target
                        if potential_targets:
                            potential_targets.sort(key=lambda x: x[0])
                            ball['target'] = potential_targets[0][1]
                            ball['state'] = 'attacking'
                        else:
                            # 没有目标时围绕原点移动
                            self._update_seeking_movement(ball, dt)
                else:
                    ball['state'] = 'attacking'

            # Attacking logic - move toward target
            if ball['state'] == 'attacking' and ball['target']:
                if self.is_monster_skill:
                    # 攻击玩家
                    target = ball['target']
                    target_pos = [
                        target.x * TILE_SIZE + TILE_SIZE // 2,
                        target.y * TILE_SIZE + TILE_SIZE // 2
                    ]
                else:
                    # 攻击怪物
                    monster = ball['target']

                    # 检查怪物是否还存在
                    if monster not in monsters or monster.hp <= 0:
                        ball['target'] = None
                        ball['state'] = 'seeking'
                        continue

                    target_pos = [
                        monster.x * TILE_SIZE + TILE_SIZE // 2,
                        monster.y * TILE_SIZE + TILE_SIZE // 2
                    ]

                # 通用逻辑：向目标移动
                current_pos = ball['screen_pos']
                dx = target_pos[0] - current_pos[0]
                dy = target_pos[1] - current_pos[1]
                distance = math.hypot(dx, dy)

                # If reached the target, explode and damage
                if distance < TILE_SIZE:
                    self.explosions.append({
                        'pos': ball['target'].x if hasattr(ball['target'], 'x') else 0,
                        'screen_pos': target_pos,
                        'time': 0.5,  # Explosion duration
                        'size': TILE_SIZE * 2,
                        'color': ball['color']
                    })

                    # 基于释放者类型计算伤害
                    if self.is_monster_skill:
                        # 怪物对玩家造成伤害（直接在这里执行）
                        dmg = self.monster.atk * self.damage_multiplier * random.uniform(0.8, 1.2)
                        actual_damage = max(dmg - self.target.defense, 0)
                        self.target.hp -= actual_damage

                        # 不需要保存到damage_results，直接添加消息
                        if hasattr(self, 'add_message'):
                            self.add_message(f"神圣球对你造成{int(actual_damage)}点伤害！")
                    else:
                        # 玩家对怪物造成伤害（通过damage_results返回）
                        damage_results.append((ball['target'], self.damage_multiplier))

                    # Mark as exploded
                    ball['state'] = 'exploded'
                else:
                    # Move toward target
                    if distance > 0:
                        move_step = ball['speed'] * dt * 60  # Speed in pixels per second
                        ball['screen_pos'][0] += (dx / distance) * move_step
                        ball['screen_pos'][1] += (dy / distance) * move_step

                        # Update grid position
                        ball['pos'][0] = ball['screen_pos'][0] // TILE_SIZE
                        ball['pos'][1] = ball['screen_pos'][1] // TILE_SIZE

        # Update explosions
        for explosion in self.explosions[:]:
            explosion['time'] -= dt
            if explosion['time'] <= 0:
                self.explosions.remove(explosion)

        # Return True if the effect is still active
        return self.progress < 1.0 or self.explosions, damage_results

    def _update_seeking_movement(self, ball, dt):
        # Orbit around the origin position with some randomness
        time = pygame.time.get_ticks() / 1000
        radius = 3 * TILE_SIZE

        # Calculate new position in a circular path
        origin_pos = [self.player_pos[0] * TILE_SIZE + TILE_SIZE // 2,
                      self.player_pos[1] * TILE_SIZE + TILE_SIZE // 2]

        ball['screen_pos'][0] = origin_pos[0] + math.cos(
            time + ball['phase']) * radius
        ball['screen_pos'][1] = origin_pos[1] + math.sin(
            time + ball['phase']) * radius

        # Add some randomness to make it look more dynamic
        ball['screen_pos'][0] += random.uniform(-5, 5)
        ball['screen_pos'][1] += random.uniform(-5, 5)

        # Update grid position
        ball['pos'][0] = ball['screen_pos'][0] // TILE_SIZE
        ball['pos'][1] = ball['screen_pos'][1] // TILE_SIZE

    def _calculate_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def draw(self, screen):
        # Draw explosions (behind balls)
        for explosion in self.explosions:
            self._draw_explosion(screen, explosion)

        # Draw each holy ball
        for ball in self.balls:
            if ball['state'] == 'exploded':
                continue

            # Draw particles first (behind the ball)
            ball_x, ball_y = ball['screen_pos'][0], ball['screen_pos'][1]

            # Draw the holy ball with pulsating effect
            pulse = 0.8 + 0.2 * math.sin(pygame.time.get_ticks() / 100)
            size = ball['size'] * pulse

            # Draw outer glow
            glow_surface = pygame.Surface(
                (int(size * 2.5), int(size * 2.5)),
                pygame.SRCALPHA
            )
            glow_color = (*ball['color'], 100)
            pygame.draw.circle(
                glow_surface,
                glow_color,
                (int(size * 1.25), int(size * 1.25)),
                int(size * 1.2)
            )
            screen.blit(
                glow_surface,
                (int(ball_x - size * 1.25),
                 int(ball_y - size * 1.25))
            )

            # Draw core of the ball
            pygame.draw.circle(
                screen,
                ball['color'],
                (int(ball_x), int(ball_y)),
                int(size)
            )

            # Draw inner light
            inner_color = (255, 255, 255)  # White center
            pygame.draw.circle(
                screen,
                inner_color,
                (int(ball_x - size * 0.3), int(ball_y - size * 0.3)),
                int(size * 0.5)
            )

            # Draw electric arcs if in attacking mode
            if ball['state'] == 'attacking' and ball['target']:
                self._draw_electric_arc(screen, ball)

    def _draw_explosion(self, screen, explosion):
        """Draw an explosion effect"""
        # Calculate explosion progress (1.0 to 0.0)
        progress = explosion['time'] / 0.5

        # Draw expanding rings
        for i in range(3):
            ring_progress = progress - (i * 0.2)
            if ring_progress <= 0:
                continue

            ring_size = explosion['size'] * (1 - ring_progress) * (i + 1) * 0.5
            ring_alpha = int(200 * ring_progress)
            ring_color = (*explosion['color'], ring_alpha)

            # Draw ring
            ring_surface = pygame.Surface(
                (int(ring_size * 2), int(ring_size * 2)),
                pygame.SRCALPHA
            )
            pygame.draw.circle(
                ring_surface,
                ring_color,
                (int(ring_size), int(ring_size)),
                int(ring_size),
                max(1, int(ring_size * 0.1))  # Ring thickness
            )
            screen.blit(
                ring_surface,
                (int(explosion['screen_pos'][0] - ring_size),
                 int(explosion['screen_pos'][1] - ring_size))
            )

    def _draw_electric_arc(self, screen, ball):
        if not ball['target']:
            return

        # 获取目标位置
        if self.is_monster_skill:
            # 目标是玩家
            target_pos = [
                ball['target'].x * TILE_SIZE + TILE_SIZE // 2,
                ball['target'].y * TILE_SIZE + TILE_SIZE // 2
            ]
        else:
            # 目标是怪物
            target_pos = [
                ball['target'].x * TILE_SIZE + TILE_SIZE // 2,
                ball['target'].y * TILE_SIZE + TILE_SIZE // 2
            ]

        # 生成光线路径
        points = []
        segments = 5

        for i in range(segments + 1):
            t = i / segments
            # 线性插值
            x = ball['screen_pos'][0] * (1 - t) + target_pos[0] * t
            y = ball['screen_pos'][1] * (1 - t) + target_pos[1] * t

            # 添加微小抖动
            if 0 < i < segments:
                x += random.uniform(-3, 3)
                y += random.uniform(-3, 3)

            points.append((x, y))

        # 绘制光线
        if len(points) > 1:
            for i in range(len(points) - 1):
                # 从明亮到暗淡
                alpha = int(200 * (1 - i / segments))
                width = max(1, 3 - i)

                pygame.draw.line(
                    screen,
                    (*ball['color'], alpha),
                    points[i],
                    points[i + 1],
                    width
                )

# ----------------- 神圣光束 -------------


class HolyBeamEffect:
    def __init__(self, start, end, duration=0.5, color_scheme="holy", damage=0):
        self.start = start
        self.end = end
        self.duration = duration
        self.progress = 0
        self.color_scheme = color_scheme
        self.damage = damage

        # Simplified direct beam path with minimal points
        self.beam_points = self._generate_straight_beam(start, end)
        self.particles = []

        # Streamlined color palettes
        if color_scheme == "holy":
            self.primary_colors = [
                (255, 215, 0),  # Gold
                (255, 223, 0)  # Golden yellow
            ]
            self.secondary_colors = [
                (255, 255, 200),  # Pale gold
                (255, 250, 205)  # Lemon chiffon
            ]
        else:  # lightning
            self.primary_colors = [
                (30, 144, 255),  # Dodger blue
                (0, 191, 255)  # Deep sky blue
            ]
            self.secondary_colors = [
                (200, 200, 255),  # Light blue
                (240, 248, 255)  # Alice blue
            ]

        # Beam properties
        self.beam_width = random.randint(3, 4)  # Reduced width
        self.beam_phase = random.uniform(0, math.pi * 2)
        self.beam_frequency = random.uniform(10, 12)

        # Animation timing
        self.time_elapsed = 0
        self.pulse_frequency = random.uniform(9, 12)

        # Initialize particles (fewer)
        self._initialize_particles()

        # Just a few energy nodes along the straight beam
        self.energy_nodes = []
        # Only add 1-2 nodes
        for _ in range(random.randint(1, 2)):
            t = random.uniform(0.3, 0.7)  # Position somewhere in the middle
            node_pos = (
                self.start[0] + (self.end[0] - self.start[0]) * t,
                self.start[1] + (self.end[1] - self.start[1]) * t
            )
            self.energy_nodes.append({
                'pos': node_pos,
                'size': random.uniform(0.8, 1.5),  # Smaller
                'phase': random.uniform(0, math.pi * 2)
            })

    def _generate_straight_beam(self, start, end):
        """Generate a straight beam path with minimal points"""
        points = [start]

        # Add just one or two midpoints with very slight variation
        distance = math.hypot(end[0] - start[0], end[1] - start[1])
        if distance > 100:  # Only add midpoints for longer beams
            # Create perpendicular vector for minimal deviation
            dx = end[0] - start[0]
            dy = end[1] - start[1]
            length = max(0.001, math.sqrt(dx * dx + dy * dy))
            perp_x, perp_y = -dy / length, dx / length

            # Add 1-2 midpoints with very minimal offset
            num_midpoints = 1 if distance < 200 else 2

            for i in range(1, num_midpoints + 1):
                t = i / (num_midpoints + 1)

                # Base point along straight line
                x = start[0] + dx * t
                y = start[1] + dy * t

                # Very slight offset (max 3 pixels)
                offset = random.uniform(-3, 3)
                x += perp_x * offset
                y += perp_y * offset

                points.append((x, y))

        points.append(end)
        return points

    def _initialize_particles(self):
        """Initialize minimal particles along the beam path"""
        # Main particles (very few)
        num_particles = max(3, int(math.hypot(self.end[0] - self.start[0], self.end[1] - self.start[1]) / 50))

        for i in range(num_particles):
            t = i / num_particles
            x = self.start[0] + (self.end[0] - self.start[0]) * t
            y = self.start[1] + (self.end[1] - self.start[1]) * t

            # Add minimal randomness
            x += random.uniform(-4, 4)
            y += random.uniform(-4, 4)

            self._add_beam_particles(x, y)

        # Small particles at endpoints
        for _ in range(2):
            self._add_beam_particles(
                self.start[0] + random.uniform(-3, 3),
                self.start[1] + random.uniform(-3, 3),
                size_mult=1.2
            )
            self._add_beam_particles(
                self.end[0] + random.uniform(-3, 3),
                self.end[1] + random.uniform(-3, 3),
                size_mult=1.2
            )

    def _add_beam_particles(self, x, y, size_mult=1.0):
        """Add minimal particles at beam location"""
        colors = self.primary_colors if random.random() < 0.7 else self.secondary_colors

        # Just 1 particle per location
        velocity = random.uniform(0.6, 2.0)

        self.particles.append({
            'pos': [x + random.uniform(-3, 3), y + random.uniform(-3, 3)],
            'vel': [random.uniform(-0.8, 0.8) * velocity, random.uniform(-0.8, 0.8) * velocity],
            'size': random.uniform(1.0, 2.5) * size_mult,
            'life': random.uniform(0.15, 0.3),
            'max_life': 0.3,
            'color': random.choice(colors),
            'pulse': random.random() < 0.3,
            'alpha_mult': random.uniform(0.8, 1.0)
        })

    def update(self, dt):
        """Update beam animation with streamlined dynamics"""
        self.progress += dt / self.duration
        self.time_elapsed += dt

        # Update particles
        for p in self.particles[:]:
            # Apply velocity damping
            p['vel'][0] *= 0.92
            p['vel'][1] *= 0.92

            # Update position
            p['pos'][0] += p['vel'][0] * dt * 60
            p['pos'][1] += p['vel'][1] * dt * 60

            # Life decay
            p['life'] -= dt
            if p['life'] <= 0:
                self.particles.remove(p)

        # Generate new particles - minimal rate
        if self.progress < 0.5:  # Shorter period
            spawn_chance = 0.3 - self.progress * 0.5  # Reduced chance
            if random.random() < spawn_chance:
                # Place along straight line
                t = random.random()
                x = self.start[0] + (self.end[0] - self.start[0]) * t
                y = self.start[1] + (self.end[1] - self.start[1]) * t

                # Add particle
                self._add_beam_particles(x, y)

        # Check if complete
        return self.progress < 1.0

    def draw(self, screen):
        """Draw the streamlined, straight beam effect"""
        # Improved fade curve
        fade_curve = 1.0 - max(0, (self.progress - 0.7) / 0.3) ** 2 if self.progress > 0.7 else 1.0
        base_alpha = int(255 * fade_curve)

        # Skip when nearly invisible
        if base_alpha <= 5:
            return

        # Current time for animations
        t = self.time_elapsed

        # More subtle beam width pulsation
        width_scale = 1.0 + 0.12 * math.sin(t * self.pulse_frequency)

        # Draw the beam segments (now straight or nearly straight)
        for i in range(len(self.beam_points) - 1):
            start_pos = self.beam_points[i]
            end_pos = self.beam_points[i + 1]

            # Calculate segment properties
            segment_t = i / max(1, len(self.beam_points) - 1)

            # Minimal wave amplitude
            wave_amplitude = math.sin(segment_t * math.pi) * 0.4 + 0.3

            # Width modulation
            segment_width = self.beam_width * width_scale
            segment_width *= 1.0 + 0.1 * math.sin(
                self.beam_frequency * segment_t + t * 8 + self.beam_phase
            ) * wave_amplitude

            # Alpha modulation
            segment_alpha = base_alpha * (0.9 + 0.1 * math.sin(
                self.beam_frequency * segment_t * 2 + t * 10
            ))

            # Determine colors
            if self.color_scheme == "holy":
                outer_glow = (255, 215, 0, int(segment_alpha * 0.2))
                mid_glow = (255, 230, 100, int(segment_alpha * 0.4))
                inner_core = (255, 255, 240, segment_alpha)
            else:  # lightning
                outer_glow = (30, 144, 255, int(segment_alpha * 0.2))
                mid_glow = (100, 180, 255, int(segment_alpha * 0.4))
                inner_core = (240, 248, 255, segment_alpha)

            # Simplified color shifting
            primary_idx = int(((math.sin(t * 5) + 1) / 2) * (len(self.primary_colors) - 0.01))
            core_color = list(self.primary_colors[primary_idx]) + [int(segment_alpha)]

            # Layer 1: Outer glow - reduced scale
            pygame.draw.line(
                screen,
                outer_glow,
                start_pos,
                end_pos,
                int(segment_width * 2.0)
            )

            # Layer 2: Mid glow
            pygame.draw.line(
                screen,
                mid_glow,
                start_pos,
                end_pos,
                int(segment_width * 1.3)
            )

            # Layer 3: Core beam
            pygame.draw.line(
                screen,
                core_color,
                start_pos,
                end_pos,
                int(segment_width)
            )

            # Layer 4: Inner core
            pygame.draw.line(
                screen,
                inner_core,
                start_pos,
                end_pos,
                max(1, int(segment_width * 0.4))
            )

        # Draw energy nodes - minimal
        for node in self.energy_nodes:
            # Subtle pulsating
            node_pulse = 0.85 + 0.15 * math.sin(t * 10 + node['phase'])
            node_size = node['size'] * segment_width * node_pulse

            # Node color
            if self.color_scheme == "holy":
                node_color = (255, 255, 200, int(base_alpha * 0.8))
            else:  # lightning
                node_color = (200, 230, 255, int(base_alpha * 0.8))

            # Draw node
            pygame.draw.circle(
                screen,
                node_color,
                (int(node['pos'][0]), int(node['pos'][1])),
                int(node_size)
            )

            # Inner core
            if self.color_scheme == "holy":
                inner_node_color = (255, 255, 255, base_alpha)
            else:
                inner_node_color = (230, 240, 255, base_alpha)

            pygame.draw.circle(
                screen,
                inner_node_color,
                (int(node['pos'][0]), int(node['pos'][1])),
                int(node_size * 0.4)
            )

        # Draw particles - minimal effects
        for p in self.particles:
            life_ratio = p['life'] / p['max_life']

            # Subtle pulse effect
            size_mod = 1.0
            if p['pulse']:
                size_mod = 0.85 + 0.25 * math.sin(t * 12 + hash(str(p['pos'])) % 10)

            # Alpha calculation
            p_alpha = int(255 * life_ratio * p['alpha_mult'])
            p_color = (*p['color'], p_alpha)

            # Minimal glow
            if p_alpha > 150:  # Higher threshold
                glow_size = p['size'] * 1.8 * size_mod
                glow_surf = pygame.Surface((int(glow_size * 2), int(glow_size * 2)), pygame.SRCALPHA)
                glow_color = (*p['color'], int(p_alpha * 0.2))
                pygame.draw.circle(
                    glow_surf,
                    glow_color,
                    (int(glow_size), int(glow_size)),
                    int(glow_size)
                )
                screen.blit(
                    glow_surf,
                    (int(p['pos'][0] - glow_size), int(p['pos'][1] - glow_size))
                )

            # Main particle
            pygame.draw.circle(
                screen,
                p_color,
                (int(p['pos'][0]), int(p['pos'][1])),
                int(p['size'] * life_ratio * size_mod)
            )

    def create_impact_particles(self, game, target, count=20):  # Increased from 10 to 20
        # Determine impact center
        if hasattr(target, 'x') and hasattr(target, 'y'):
            impact_center = (target.x * TILE_SIZE + TILE_SIZE // 2,
                             target.y * TILE_SIZE + TILE_SIZE // 2)
        else:
            impact_center = target

        # Colors based on beam type
        if self.color_scheme == "holy":
            colors = [(255, 215, 0), (255, 255, 200), (255, 230, 150)]
            explosion_color = (255, 215, 0)
            core_color = (255, 255, 220)
        else:  # lightning
            colors = [(30, 144, 255), (100, 200, 255), (200, 240, 255)]
            explosion_color = (30, 144, 255)
            core_color = (200, 240, 255)

        # Create expanding rings with better transparency
        for i in range(3):
            delay = i * 0.1  # Staggered ring expansion
            size_mult = 1.0 + i * 0.4  # Each ring is larger

            game.fear_particles.append({
                'pos': list(impact_center),
                'vel': [0, 0],  # Must include velocity for all particles
                'life': 0.5 - i * 0.1,  # Longer-lived initial rings
                'max_life': 0.5 - i * 0.1,
                'size': 10 * size_mult,
                'color': explosion_color,
                'is_ring': True,
                'ring_width': 2,
                'delay': delay,
                'alpha_start': 180 - i * 30  # Higher initial opacity that fades out
            })

        # Create central flash with improved transparency
        game.fear_particles.append({
            'pos': list(impact_center),
            'vel': [0, 0],  # Static particle
            'life': 0.3,
            'max_life': 0.3,
            'size': 12,  # Larger flash
            'color': core_color,
            'is_flash': True,
            'alpha_mult': 0.9  # Control max opacity
        })

        # Add primary particles - more of them with better variety
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3.0, 12.0)  # Wider speed range
            size = random.uniform(1.5, 4.0)  # Larger size range
            life = random.uniform(0.3, 1.0)  # Longer life for some particles

            # Random transparency multiplier
            alpha_mult = random.uniform(0.7, 1.0)

            particle = {
                'pos': [impact_center[0], impact_center[1]],
                'vel': [math.cos(angle) * speed, math.sin(angle) * speed],
                'life': life,
                'max_life': life,
                'size': size,
                'color': random.choice(colors),
                'alpha_mult': alpha_mult,  # Control max opacity
            }

            game.fear_particles.append(particle)

        # Add secondary glow particles (smaller, more numerous)
        for _ in range(count // 2):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1.0, 6.0)  # Slower speed for lingering effect
            size = random.uniform(0.8, 2.5)  # Smaller particles
            life = random.uniform(0.6, 1.2)  # Longer-lived

            # More transparent
            alpha_mult = random.uniform(0.4, 0.7)

            particle = {
                'pos': [impact_center[0] + random.uniform(-10, 10),
                        impact_center[1] + random.uniform(-10, 10)],  # Slight position variance
                'vel': [math.cos(angle) * speed, math.sin(angle) * speed],
                'life': life,
                'max_life': life,
                'size': size,
                'color': random.choice(colors),
                'alpha_mult': alpha_mult,
                'is_glow': True  # Flag for special rendering
            }

            game.fear_particles.append(particle)

# --------------- 神圣守护 -----------------


class SummonHolyBall:
    def __init__(self, owner, ball_count=6, duration=20.0, attack_range=6, attack_speed=0.8,
                 damage_multiple=1.2, heal_percent=0.05, is_monster_skill=False, target=None):
        self.owner = owner  # 玩家或怪物
        self.duration = duration  # 球体存在时间（秒）
        self.lifetime = duration  # 剩余生命周期
        self.attack_range = attack_range  # 攻击范围（格）
        self.ball_count = ball_count  # 闪电球数量
        self.heal_percent = heal_percent  # 治疗百分比
        self.heal_timer = 0  # 治疗计时器

        # 新增参数
        self.is_monster_skill = is_monster_skill
        self.target = target  # 怪物技能时为玩家

        # 创建多个神圣球
        self.holy_balls = []
        for i in range(ball_count):
            self.holy_balls.append(self.HolyBall(
                owner,
                orbit_angle=2 * math.pi * i / ball_count,  # 均匀分布在圆周上
                orbit_speed=0.8 + random.uniform(-0.2, 0.2),  # 略微不同的轨道速度
                attack_speed=attack_speed,
                damage_multiple=damage_multiple,
                is_monster_skill=is_monster_skill
            ))

    def update(self, dt, game):
        # 更新生命周期
        self.lifetime -= dt
        if self.lifetime <= 0:
            # 生成消散特效
            for ball in self.holy_balls:
                for _ in range(10):  # 每个球生成10个粒子
                    game.fear_particles.append({
                        'pos': list(ball.position),
                        'vel': [random.uniform(-8, 8), random.uniform(-8, 8)],
                        'life': random.uniform(0.5, 1.2),
                        'max_life': 1.2,
                        'size': random.uniform(2, 5),
                        'color': (255, 215, 0)
                    })
            return False  # 生命周期结束，移除所有球体

        # 根据释放者类型决定行为
        if self.is_monster_skill:
            # 怪物技能：攻击玩家，不治疗怪物
            self.update_monster_skill(dt, game)
        else:
            # 玩家技能：攻击怪物，治疗玩家
            self.update_player_skill(dt, game)

        return True  # 继续存在

    def update_monster_skill(self, dt, game):
        # 检查玩家是否在攻击范围内
        player = self.target
        distance = game.calculate_distance(
            (player.x, player.y),
            (self.owner.x + 1, self.owner.y + 1)  # 怪物中心位置
        )

        # 如果玩家在范围内，造成伤害
        if distance <= self.attack_range:
            # 每秒造成一次伤害
            self.heal_timer += dt
            if self.heal_timer >= 1.0:
                # 计算伤害
                damage = self.owner.atk * 0.8
                actual_damage = max(damage - player.defense, 0)
                player.hp -= actual_damage
                game.add_message(f"神圣光环造成 {actual_damage} 点伤害！")

                # 重置计时器
                self.heal_timer = 0

                # 添加受击特效
                game.fear_particles.append({
                    'pos': [player.x * TILE_SIZE + TILE_SIZE // 2,
                            player.y * TILE_SIZE + TILE_SIZE // 2],
                    'vel': [random.uniform(-3, 3), random.uniform(-5, -2)],
                    'life': 0.8,
                    'max_life': 0.8,
                    'size': 3,
                    'color': (255, 255, 200)
                })

        # 更新所有球体
        for ball in self.holy_balls:
            ball.update(dt, game)

        # 让神圣球也攻击玩家 - 关键修复
        if player:
            for ball in self.holy_balls:
                if ball.attack_cooldown <= 0:
                    distance = game.calculate_distance(
                        (player.x, player.y),
                        (int(ball.position[0] / TILE_SIZE), int(ball.position[1] / TILE_SIZE))
                    )
                    if distance <= self.attack_range:
                        ball.try_attack_player(player, game)

    def update_player_skill(self, dt, game):
        # 治疗玩家
        self.heal_timer += dt
        if self.heal_timer >= 1.0:  # 每秒治疗一次
            heal_amount = min(200, int(game.player.hp * self.heal_percent))
            game.player.hp = min(game.player.hp + heal_amount, game.player.max_hp)
            game.add_message(f"神圣光球恢复 {heal_amount} 点生命值!")
            self.heal_timer = 0

        # 更新所有球体
        for ball in self.holy_balls:
            ball.update(dt, game)

        # 寻找范围内的目标
        targets = []
        for monster in game.monsters:
            distance = game.calculate_distance(
                (game.player.x, game.player.y),
                (monster.x, monster.y)
            )
            if distance <= self.attack_range:
                targets.append(monster)

        # 每个球体尝试攻击目标
        if targets:
            for ball in self.holy_balls:
                ball.try_attack(targets, game)

    def draw(self, screen):
        # 如果是怪物技能，绘制攻击范围指示
        if self.is_monster_skill:
            # 获取怪物中心位置
            center_x = self.owner.x * TILE_SIZE + TILE_SIZE * 1.5  # 假设3x3怪物
            center_y = self.owner.y * TILE_SIZE + TILE_SIZE * 1.5

            # 绘制攻击范围指示
            range_radius = self.attack_range * TILE_SIZE
            range_surf = pygame.Surface((int(range_radius * 2), int(range_radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(range_surf, (255, 255, 200, 15),
                               (int(range_radius), int(range_radius)),
                               int(range_radius))
            screen.blit(range_surf,
                        (center_x - range_radius, center_y - range_radius))

        # 绘制所有球体
        for ball in self.holy_balls:
            ball.draw(screen)

    # 内部类: 单个神圣球
    class HolyBall:
        def __init__(self, owner, orbit_angle=0, orbit_speed=1.0, attack_speed=0.8,
                     damage_multiple=1.5, is_monster_skill=False):
            self.owner = owner
            self.is_monster_skill = is_monster_skill

            # 轨道参数
            self.orbit_radius = TILE_SIZE * 2.0  # 环绕距离
            self.orbit_angle = orbit_angle  # 初始角度
            self.orbit_speed = orbit_speed  # 轨道速度（弧度/秒）

            # 攻击参数
            self.attack_speed = attack_speed  # 每秒攻击次数
            self.attack_cooldown = random.uniform(0, 1.0 / attack_speed)  # 随机初始冷却
            self.damage_multiple = damage_multiple  # 伤害倍率

            # 位置为拥有者位置的偏移
            if is_monster_skill:
                # 怪物是3x3的，中心位置不同
                owner_pos = (owner.x * TILE_SIZE + TILE_SIZE * 1.5,
                             owner.y * TILE_SIZE + TILE_SIZE * 1.5)
            else:
                # 玩家是1x1的
                owner_pos = (owner.x * TILE_SIZE + TILE_SIZE // 2,
                             owner.y * TILE_SIZE + TILE_SIZE // 2)

            self.position = [
                owner_pos[0] + math.cos(orbit_angle) * self.orbit_radius,
                owner_pos[1] + math.sin(orbit_angle) * self.orbit_radius
            ]

            # 视觉参数
            self.size = 11  # 球体基础尺寸
            self.light_rays = []  # 光线连接点

        def update(self, dt, game):
            # 更新轨道位置
            self.orbit_angle += self.orbit_speed * dt

            if self.is_monster_skill:
                # 怪物中心位置
                owner_center = (self.owner.x * TILE_SIZE + TILE_SIZE * 1.5,
                                self.owner.y * TILE_SIZE + TILE_SIZE * 1.5)
            else:
                # 玩家中心位置
                owner_center = (game.player.x * TILE_SIZE + TILE_SIZE // 2,
                                game.player.y * TILE_SIZE + TILE_SIZE // 2)

            self.position = [
                owner_center[0] + math.cos(self.orbit_angle) * self.orbit_radius,
                owner_center[1] + math.sin(self.orbit_angle) * self.orbit_radius
            ]

            # 更新攻击冷却
            if self.attack_cooldown > 0:
                self.attack_cooldown -= dt

            # 动态更新光线连接点
            if random.random() < 0.15 or not self.light_rays:
                self.light_rays = []
                connection_count = random.randint(2, 3)
                for _ in range(connection_count):
                    angle = random.uniform(0, 2 * math.pi)
                    distance = random.uniform(self.size * 1.2, self.size * 2)
                    self.light_rays.append({
                        'pos': [
                            self.position[0] + math.cos(angle) * distance,
                            self.position[1] + math.sin(angle) * distance
                        ],
                        'life': random.uniform(0.2, 0.4)
                    })

            # 更新连接点生命周期
            for conn in self.light_rays[:]:
                conn['life'] -= dt
                if conn['life'] <= 0:
                    self.light_rays.remove(conn)

        def try_attack_player(self, player, game):
            """针对怪物控制的神圣球攻击玩家的方法"""
            if self.attack_cooldown > 0:
                return

            # 计算伤害（带随机波动）
            base_damage = self.owner.atk * self.damage_multiple
            damage_variation = random.uniform(0.8, 1.2)
            damage = base_damage * damage_variation
            actual_damage = max(damage - player.defense, 0)

            # 应用伤害
            player.hp -= actual_damage

            # 添加神圣光束效果
            start_pos = list(self.position)
            # 光束起点小幅度随机偏移
            start_jitter = [random.uniform(-5, 5), random.uniform(-5, 5)]
            start_pos[0] += start_jitter[0]
            start_pos[1] += start_jitter[1]

            # 光束终点为玩家位置（也带随机偏移）
            end_pos = [player.x * TILE_SIZE + TILE_SIZE // 2,
                       player.y * TILE_SIZE + TILE_SIZE // 2]
            end_jitter = [random.uniform(-5, 5), random.uniform(-5, 5)]
            end_pos[0] += end_jitter[0]
            end_pos[1] += end_jitter[1]

            # 创建神圣光束效果
            holy_beam = HolyBeamEffect(
                start=tuple(start_pos),
                end=tuple(end_pos),
                duration=0.4,
                color_scheme="holy",
                damage=actual_damage
            )
            game.skill_effects.append(holy_beam)

            # 创建冲击效果
            holy_beam.create_impact_particles(game, player)

            game.add_message(f"敌方神圣光球对你造成{int(actual_damage)}点伤害!")
            self.attack_cooldown = 1.0 / self.attack_speed  # 设置冷却时间

        def try_attack(self, targets, game):
            """玩家控制的神圣球攻击怪物的方法"""
            # 如果是怪物技能，不应该在这里调用
            if self.is_monster_skill:
                return

            # 如果有攻击冷却，不攻击
            if self.attack_cooldown > 0 or not targets:
                return

            # 选择一个随机目标攻击
            target = random.choice(targets)

            # 计算伤害（带随机波动）
            base_damage = game.player.atk * self.damage_multiple
            damage_variation = random.uniform(0.8, 1.2)
            damage = base_damage * damage_variation
            actual_damage = max(damage - target.defense, 0)

            # 应用伤害
            target.hp -= actual_damage

            # 添加神圣光束效果
            start_pos = list(self.position)
            # 光束起点小幅度随机偏移
            start_jitter = [random.uniform(-5, 5), random.uniform(-5, 5)]
            start_pos[0] += start_jitter[0]
            start_pos[1] += start_jitter[1]

            # 光束终点为怪物位置（也带随机偏移）
            end_pos = [target.x * TILE_SIZE + TILE_SIZE // 2,
                       target.y * TILE_SIZE + TILE_SIZE // 2]
            end_jitter = [random.uniform(-5, 5), random.uniform(-5, 5)]
            end_pos[0] += end_jitter[0]
            end_pos[1] += end_jitter[1]

            # 创建神圣光束效果 - 确保使用"holy"颜色方案
            holy_beam = HolyBeamEffect(
                start=tuple(start_pos),
                end=tuple(end_pos),
                duration=0.4,
                color_scheme="holy",  # 使用金色系的圣光效果
                damage=actual_damage
            )
            game.skill_effects.append(holy_beam)

            # 创建冲击效果
            holy_beam.create_impact_particles(game, target)

            game.add_message(f"神圣光球对{target.name}造成{int(actual_damage)}点伤害!")
            self.attack_cooldown = 1.0 / self.attack_speed  # 设置冷却时间

        def draw(self, screen):
            anim_time = pygame.time.get_ticks()

            # 球体核心脉动效果
            pulse = 0.5 + 0.5 * math.sin(anim_time / 200 + self.orbit_angle)
            core_radius = int(self.size * (1 + 0.2 * pulse))

            # 添加外部光晕渐变效果 - 新增
            for i in range(4):
                outer_radius = core_radius * (1.8 - i * 0.2)
                alpha = int(70 - i * 15)  # 从外到内逐渐降低透明度

                if outer_radius <= 0:
                    continue

                outer_surf = pygame.Surface((outer_radius * 2, outer_radius * 2), pygame.SRCALPHA)

                # 根据技能类型选择颜色
                if self.is_monster_skill:
                    outer_color = (255, 215, 0, alpha)  # 怪物技能偏金色
                else:
                    outer_color = (255, 230, 150, alpha)  # 玩家技能圣光色

                pygame.draw.circle(outer_surf, outer_color, (outer_radius, outer_radius), outer_radius)
                screen.blit(outer_surf,
                            (int(self.position[0] - outer_radius),
                             int(self.position[1] - outer_radius)))

            # 绘制多层递减透明度的核心
            for i in range(3):
                alpha = 200 - i * 50
                radius = core_radius - i * 2

                if radius <= 0:
                    continue

                temp_surf = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)

                # 根据技能类型选择颜色 - 修正为都使用圣光金色系
                if self.is_monster_skill:
                    color = (255, 215, 0, alpha)  # 怪物技能偏金色
                else:
                    color = (255, 230, 150, alpha) if i % 2 == 0 else (255, 255, 220, alpha)  # 玩家技能也使用圣光色

                pygame.draw.circle(temp_surf, color, (radius, radius), radius)
                screen.blit(temp_surf, (int(self.position[0] - radius), int(self.position[1] - radius)))

            # 绘制内部发光核心 - 新增
            inner_glow_radius = core_radius * 0.6
            inner_glow = pygame.Surface((inner_glow_radius * 2, inner_glow_radius * 2), pygame.SRCALPHA)

            # 创建径向渐变效果
            for r in range(int(inner_glow_radius), 0, -1):
                intensity = r / inner_glow_radius
                alpha = int(255 * intensity)
                if self.is_monster_skill:
                    glow_color = (255, 255, 220, alpha)  # 怪物技能内核偏白
                else:
                    glow_color = (255, 255, 255, alpha)  # 玩家技能内核纯白

                pygame.draw.circle(inner_glow, glow_color,
                                   (int(inner_glow_radius), int(inner_glow_radius)),
                                   r)

            screen.blit(inner_glow,
                        (int(self.position[0] - inner_glow_radius),
                         int(self.position[1] - inner_glow_radius)))

            # 绘制光线连接
            for conn in self.light_rays:
                # 绘制从球心到连接点的光线
                life_ratio = conn['life'] / 0.4  # 假设最大生命周期为0.4

                # 生成光线路径点
                points = []
                # 起点为球心
                points.append(tuple(self.position))

                # 生成中间随机点
                segments = random.randint(1, 3)
                for i in range(segments):
                    t = (i + 1) / (segments + 1)
                    mid_x = self.position[0] + (conn['pos'][0] - self.position[0]) * t
                    mid_y = self.position[1] + (conn['pos'][1] - self.position[1]) * t

                    # 添加随机偏移
                    jitter_range = 8 * (1 - t) * life_ratio
                    jitter_x = random.uniform(-jitter_range, jitter_range)
                    jitter_y = random.uniform(-jitter_range, jitter_range)

                    points.append((mid_x + jitter_x, mid_y + jitter_y))

                # 终点为连接点
                points.append(tuple(conn['pos']))

                # 绘制光线段
                for i in range(len(points) - 1):
                    # 根据释放者选择不同颜色 - 修正为都使用圣光系颜色
                    if self.is_monster_skill:
                        line_color = (255, 215, 0, int(255 * life_ratio))  # 金色
                    else:
                        line_color = (255, 240, 180, int(255 * life_ratio))  # 淡金色

                    pygame.draw.line(screen, line_color, points[i], points[i + 1],
                                     max(1, int(3 * life_ratio)))

            # 随机添加粒子效果 - 新增
            if random.random() < 0.3:
                angle = random.uniform(0, math.pi * 2)
                distance = random.uniform(core_radius * 0.7, core_radius * 1.5)
                particle_pos = [
                    self.position[0] + math.cos(angle) * distance,
                    self.position[1] + math.sin(angle) * distance
                ]

                # 判断粒子颜色
                if self.is_monster_skill:
                    particle_color = (255, 255, 150)  # 怪物技能粒子
                else:
                    particle_color = (255, 250, 200)  # 玩家技能粒子

                # 添加到游戏的粒子系统
                game_particle = {
                    'pos': particle_pos,
                    'vel': [random.uniform(-1, 1), random.uniform(-1, 1)],
                    'life': random.uniform(0.3, 0.7),
                    'max_life': 0.7,
                    'size': random.uniform(1, 2.5),
                    'color': particle_color
                }

                # 如果游戏对象可访问，添加粒子
                try:
                    if hasattr(self.owner, 'fear_particles'):
                        self.owner.fear_particles.append(game_particle)
                except:
                    pass  # 忽略如果添加失败


# ---------------- 魔王重锤眩晕 --------------------
class CrackEffect:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.lifetime = 2.0  # 效果持续时间(秒)
        self.cracks = []  # 裂缝列表
        # 生成裂缝
        for dx in range(-radius, radius + 1):
            for dy in range(-radius, radius + 1):
                if abs(dx) + abs(dy) <= radius:
                    self.cracks.append((x + dx, y + dy))

    def update(self, dt):
        self.lifetime -= dt
        return self.lifetime > 0

    def draw(self, screen):
        for (cx, cy) in self.cracks:
            rect = pygame.Rect(cx * TILE_SIZE, cy * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (80, 80, 80), rect)  # 裂缝颜色
            # 绘制裂缝细节
            for _ in range(3):
                start_x = cx * TILE_SIZE + random.randint(2, TILE_SIZE - 2)
                start_y = cy * TILE_SIZE + random.randint(2, TILE_SIZE - 2)
                end_x = start_x + random.randint(-4, 4)
                end_y = start_y + random.randint(-4, 4)
                pygame.draw.line(screen, (50, 50, 50), (start_x, start_y), (end_x, end_y), 2)


# 冰霜龙吐息：
class IceBreathEffect:
    def __init__(self, start_pos, direction):
        self.start_pos = start_pos  # 吐息起点(巨龙嘴部位置)
        self.direction = direction  # 吐息方向向量
        self.lifetime = 2.0  # 效果持续时间(秒)
        self.ice_particles = []  # 冰晶粒子
        self.area = set()  # 影响区域坐标
        # 生成扇形区域
        length = 7  # 最大长度
        angle = math.radians(45)  # 扇形角度
        base_dir = math.atan2(direction[1], direction[0])
        for r in range(1, length + 1):
            for theta in [base_dir - angle / 2 + i * angle / 8 for i in range(9)]:
                x = int(start_pos[0] / TILE_SIZE + r * math.cos(theta))
                y = int(start_pos[1] / TILE_SIZE + r * math.sin(theta))
                if 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT:
                    self.area.add((x, y))
                    # 添加冰雾粒子
                    self.ice_particles.append({
                        'pos': (x * TILE_SIZE + random.randint(2, 22), y * TILE_SIZE + random.randint(2, 22)),
                        'size': random.randint(2, 4),
                        'alpha': random.randint(100, 200)
                    })

    def update(self, dt):
        self.lifetime -= dt
        # 粒子飘散效果
        for p in self.ice_particles:
            p['pos'] = (p['pos'][0] + random.randint(-1, 1), p['pos'][1] + random.randint(-1, 1))
            p['alpha'] = max(0, p['alpha'] - 5)
        return self.lifetime > 0

    def draw(self, screen):
        # 绘制寒冰区域
        for (x, y) in self.area:
            rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, (135, 206, 235, 50), rect)  # 半透明冰雾
        # 绘制动态冰晶
        for p in self.ice_particles:
            alpha_surface = pygame.Surface((p['size'] * 2, p['size'] * 2), pygame.SRCALPHA)
            pygame.draw.circle(alpha_surface, (240, 255, 255, p['alpha']),
                               (p['size'], p['size']), p['size'])
            screen.blit(alpha_surface, p['pos'])


class PoisonBall:  # 法师毒液球
    def __init__(self, start, target):
        self.pos = list(start)
        self.target = target
        self.speed = 8  # 像素/帧
        self.trail = []  # 拖尾轨迹
        self.exploded = False

        # 计算移动方向
        dx = target[0] - start[0]
        dy = target[1] - start[1]
        dist = math.hypot(dx, dy)
        if dist == 0:
            self.dir = (1, 0)
        else:
            self.dir = (dx / dist * self.speed, dy / dist * self.speed)

    def update(self, dt):
        if not self.exploded:
            # 更新位置
            self.pos[0] += self.dir[0]
            self.pos[1] += self.dir[1]
            self.trail.append(tuple(self.pos))
            if len(self.trail) > 10:
                self.trail.pop(0)

            # 命中检测
            if math.hypot(self.pos[0] - self.target[0], self.pos[1] - self.target[1]) < self.speed:
                self.exploded = True
                return True  # 需要触发中毒效果
        return False

    def draw(self, screen):
        # 绘制拖尾
        for i, pos in enumerate(self.trail):
            alpha = 255 * (i + 1) / len(self.trail)
            radius = int(3 * (i + 1) / len(self.trail))
            pygame.draw.circle(screen, (50, 205, 50, alpha),
                               (int(pos[0]), int(pos[1])), radius)

        # 绘制毒球主体
        if not self.exploded:
            pygame.draw.circle(screen, COLOR_POISON,
                               (int(self.pos[0]), int(self.pos[1])), 6)
            # 毒球光晕
            glow = pygame.Surface((20, 20), pygame.SRCALPHA)
            pygame.draw.circle(glow, (50, 205, 50, 80), (10, 10), 8)
            screen.blit(glow, (int(self.pos[0] - 10), int(self.pos[1] - 10)))


class CorrosionEffect:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.create_time = pygame.time.get_ticks()
        self.particles = []  # Particle effects for corrosion

        # Create more particles for richer effect
        for _ in range(20):
            self.particles.append({
                'pos': (x * TILE_SIZE + random.randint(2, TILE_SIZE - 2),
                        y * TILE_SIZE + random.randint(2, TILE_SIZE - 2)),
                'size': random.randint(2, 6),
                'alpha': 255,
                'speed': (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
            })

        # Generate irregular corrosion blobs
        self.corrosion_points = []
        for _ in range(8):
            self.corrosion_points.append({
                'pos': (x * TILE_SIZE + random.randint(5, TILE_SIZE - 5),
                        y * TILE_SIZE + random.randint(5, TILE_SIZE - 5)),
                'radius': random.randint(4, 12),
                'alpha': random.randint(150, 200)
            })

    def update(self, current_time):
        # Calculate elapsed time
        elapsed = current_time - self.create_time

        # Update particle positions and alpha
        for p in self.particles:
            p['pos'] = (p['pos'][0] + p['speed'][0], p['pos'][1] + p['speed'][1])
            p['alpha'] = max(0, 255 - (elapsed * 85 // 1000))  # Fade over 3 seconds

            # Slow down particle movement over time
            p['speed'] = (p['speed'][0] * 0.98, p['speed'][1] * 0.98)

        # Update corrosion points alpha
        for point in self.corrosion_points:
            point['alpha'] = max(0, point['alpha'] - (elapsed // 20))

        return elapsed < 3000  # Effect lasts 3 seconds

    def draw(self, screen):
        # Draw corrosion base - irregular splotches
        for point in self.corrosion_points:
            if point['alpha'] > 0:
                # Create a surface for the blob with alpha
                blob_surf = pygame.Surface((point['radius'] * 2, point['radius'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(blob_surf, (91, 13, 133, point['alpha']),
                                   (point['radius'], point['radius']), point['radius'])

                # Add some irregularity to the blob
                for _ in range(3):
                    offset_x = random.randint(-4, 4)
                    offset_y = random.randint(-4, 4)
                    pygame.draw.circle(blob_surf, (91, 13, 133, point['alpha'] // 2),
                                       (point['radius'] + offset_x, point['radius'] + offset_y),
                                       point['radius'] // 2)

                screen.blit(blob_surf, (int(point['pos'][0] - point['radius']),
                                        int(point['pos'][1] - point['radius'])))

        # Draw particles
        for p in self.particles:
            if p['alpha'] > 0:
                # Alternate between dark red and purple for variety
                color = (139, 0, 0, p['alpha']) if random.random() < 0.5 else (120, 20, 130, p['alpha'])

                # Create surface with alpha
                part_surf = pygame.Surface((p['size'] * 2, p['size'] * 2), pygame.SRCALPHA)
                pygame.draw.circle(part_surf, color, (p['size'], p['size']), p['size'])

                screen.blit(part_surf, (int(p['pos'][0] - p['size']), int(p['pos'][1] - p['size'])))

        # Draw random corrosion streaks/cracks
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.create_time
        fade_factor = max(0, 1 - (elapsed / 3000))

        if random.random() < 0.3 * fade_factor:  # Less frequent streaks as effect fades
            for _ in range(2):
                # Random streak position and direction
                start_x = self.x * TILE_SIZE + random.randint(5, TILE_SIZE - 5)
                start_y = self.y * TILE_SIZE + random.randint(5, TILE_SIZE - 5)

                # Create irregular path for the streak
                points = [(start_x, start_y)]
                for i in range(3):
                    next_x = points[-1][0] + random.randint(-8, 8)
                    next_y = points[-1][1] + random.randint(-8, 8)
                    points.append((next_x, next_y))

                # Draw the corrosion streak
                streak_alpha = int(180 * fade_factor)
                if streak_alpha > 0:
                    for i in range(len(points) - 1):
                        pygame.draw.line(screen, (139, 0, 0, streak_alpha),
                                         points[i], points[i + 1],
                                         max(1, int(2 * fade_factor)))

 # ----------------------- 物品装备实体 --------------------------


class Item:
    def __init__(self, x, y, item_type, equipment_data=None):
        self.x = x
        self.y = y
        self.item_type = item_type # 物品类前缀名，如 “GEM”， “WOOD_SWORD”
        self.equipment_data = equipment_data  # 存储装备数据

# -------- 迷宫生成函数 --------


def generate_maze(width=CONFIG["MAP_WIDTH"], height=CONFIG["MAP_HEIGHT"]):
    maze = [[1 for _ in range(width)] for _ in range(height)]
    start_x = random.randrange(1, width, 2)
    start_y = random.randrange(1, height, 2)
    maze[start_y][start_x] = 0
    stack = [(start_x, start_y)]
    while stack:
        x, y = stack[-1]
        neighbors = []
        for dx, dy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
            nx, ny = x + dx, y + dy
            if 0 < nx < width and 0 < ny < height and maze[ny][nx] == 1:
                neighbors.append((nx, ny, dx, dy))
        if neighbors:
            nx, ny, dx, dy = random.choice(neighbors)
            maze[y + dy // 2][x + dx // 2] = 0
            maze[ny][nx] = 0
            stack.append((nx, ny))
        else:
            stack.pop()
    return maze


# 修改房间生成函数
def add_rooms(maze, max_rooms=MAX_ROOM, room_max_size=MAX_ROOM_SIZE):
    height = len(maze)
    width = len(maze[0])
    num_rooms = random.randint(0, max_rooms)
    rooms = []
    for _ in range(num_rooms):
        w = random.randint(5, room_max_size)  # 最小房间尺寸改为5
        h = random.randint(5, room_max_size)
        x = random.randint(1, width - w - 1)
        y = random.randint(1, height - h - 1)
        # 检查是否与其他房间重叠
        overlap = False
        for other in rooms:
            if (x < other[0] + other[2] and x + w > other[0] and
                    y < other[1] + other[3] and y + h > other[1]):
                overlap = True
                break
        if not overlap:
            for i in range(y, y + h):
                for j in range(x, x + w):
                    maze[i][j] = 0
            rooms.append((x, y, w, h))
    return rooms


# -------- 游戏主类 --------


class Game:
    # 在Game类的__init__方法中调整窗口大小
    def __init__(self):
        pygame.init()
        self.apply_config()  # 应用配置
        self.screen = pygame.display.set_mode((CONFIG["SCREEN_WIDTH"], CONFIG["SCREEN_HEIGHT"]),
                                            pygame.HWSURFACE | pygame.DOUBLEBUF)
        # pygame.display.set_caption("魔塔游戏")
        self.clock = pygame.time.Clock()
        self.game_state = "menu"
        self.main_menu = MainMenu(self.screen)  # 确保 MainMenu 被正确初始化
        self.floor = 1
        self.tile_styles = []  # 用于存储地砖样式数据
        self.maze = []
        self.rooms = []

        # 初始化物品概率系统
        self.item_system = ItemProbabilitySystem(self)

        self.is_animating = False  # 动画播放状态
        self.animation_radius = 0  # 当前动画半径
        self.animation_max_radius = 0  # 最大动画半径
        self.animation_speed = 400  # 动画扩展速度（像素/秒）
        self.animation_center = (0, 0)  # 动画圆心坐标

        self.fountain_room = None  # 存储喷泉房间坐标和范围
        self.last_spawn_time = 0  # 上次生成史莱姆的时间

        self.lava_room = None  # 存储喷泉房间坐标和范围
        self.last_lava_spawn = 0  # 上次生成史莱姆的时间

        self.message_log = []  # 消息日志
        self.max_log_lines = 39  # 最大显示消息行数

        self.path = []  # 用于存储当前路径
        self.path_timer = 0  # 路径显示计时器

        self.skill_effects = []  # 存储所有技能特效
        self.player_debuff = {
            'frozen_area': None,  # (start_time, area)
            'poison_end': 0,  # 中毒结束时间
            'stun_end': 0,  # 眩晕
            'paralyze_end': 0,  # 麻痹时间
            'in_corrosion': None,  # 腐蚀
            'red_fear': False,  # 血腥闪电状态存储块
            'blue_fear': None,
            'gold_fear': None
        }

        self.corrosion_effects = []  # 存储腐蚀痕迹数据
        self.player_debuff['in_corrosion'] = False  # 玩家是否在腐蚀区域
        # 闪电boss球体参数
        self.s = 1  # 角速度
        self.radius_large = 1.2
        self.radius_small = TILE_SIZE // 2.5
        self.red_fear = False  # 血腥闪电状态存储块
        self.blue_fear = False  # 纯青闪电状态存储块
        self.gold_fear = False  # 金色闪电状态存储块

        self.fear_particles = []
        self.lightning_balls = []  # 存储闪电位置

        self.side_panel = pygame.Surface((SIDEBAR_WIDTH, SCREEN_HEIGHT))

        self.nearby_monsters = []  # 存储附近怪物的列表
        self.guardian_lightning_balls = []  # 存储守护闪电球

        # 游戏状态管理
        self.game_state = "menu"  # menu/playing/dead
        self.main_menu = MainMenu(self.screen)
        self.death_screen = None

        # ------------------- 静态背景渲染 -----------------------
        self.background_surface = None  # 新增背景Surface
        self.player = Player(0,0)
        self.generate_floor()

        self.player = Player(self.start_pos[0], self.start_pos[1])  # 游戏生成后玩家位置

        # ---------------- 游戏内玩家移动轨迹效果 ----------------

        self.lightning_path_red = LIGHTNINGEFFECT_RED
        self.lightning_path_yellow = LIGHTNINGEFFECT_YELLOW
        self.lightning_path_blue = LIGHTNINGEFFECT_BLUE

        # ------------------- 设置初始化函数 --------------------

    def apply_config(self):
        global MAP_WIDTH, MAP_HEIGHT, TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT
        MAP_WIDTH = CONFIG["MAP_WIDTH"]
        MAP_HEIGHT = CONFIG["MAP_HEIGHT"]
        TILE_SIZE = CONFIG["TILE_SIZE"]
        SCREEN_WIDTH = CONFIG["SCREEN_WIDTH"]
        SCREEN_HEIGHT = CONFIG["SCREEN_HEIGHT"]


    def show_encyclopedia(self):  # 百科全书函数
        encyclopedia = Encyclopedia(self.screen, self)
        encyclopedia.run()

        # ------------------- 更新移动动画效果 ---------------------
    def set_path_effect(self):
        if self.player.equipped_armor:
            if self.player.equipped_armor['name'] == "红闪电甲":
                self.lightning_path_red = True
            else:
                self.lightning_path_red = False
            if self.player.equipped_armor['name'] == "黄闪电甲":
                self.lightning_path_yellow = True
            else:
                self.lightning_path_yellow = False
            if self.player.equipped_armor['name'] == "蓝闪电甲":
                self.lightning_path_blue = True
            else:
                self.lightning_path_blue = False

    def clear_dynamic(self):
        self.fear_particles = []
        self.lightning_balls = []  # 存储闪电位置
        self.corrosion_effects = []  # 存储腐蚀痕迹数据
        self.player_debuff['in_corrosion'] = False  # 玩家是否在腐蚀区域
        self.skill_effects = []  # 存储所有技能特效
        self.guardian_lightning_balls = []  # 守护闪电球列表
        self.fountain_room = None
        self.lava_room = None

    # ----------- 耐久度 ---------
    def reduce_equipment_durability(self):
        # 在每次战斗后调用
        if self.player.equipped_weapon:
            self.player.equipped_weapon["durability"] -= 1
            if self.player.equipped_weapon["durability"] <= 0:
                self.add_message(f"{self.player.equipped_weapon['name']} 已损坏！")
                self.player.equipped_weapon = None

        if self.player.equipped_armor:
            self.player.equipped_armor["durability"] -= 1
            if self.player.equipped_armor["durability"] <= 0:
                self.add_message(f"{self.player.equipped_armor['name']} 已损坏！")
                self.player.equipped_armor = None

    # ------------ 绘制玩家 ----------------
    def draw_player(self):
        px = self.player.x * TILE_SIZE
        py = self.player.y * TILE_SIZE

        # ------ 配色方案：庄重、威武 ------
        armor_color = (50, 70, 150)  # 深蓝色盔甲
        armor_highlight = (100, 120, 220)  # 盔甲高光
        skin_color = (220, 170, 150)  # 自然肤色
        cape_color = (140, 20, 20)  # 深红色披风
        gold_trim = (230, 190, 50)  # 金色装饰

        # ------ 披风 ------
        cape_points = [
            (px + TILE_SIZE * 0.25, py + TILE_SIZE * 0.35),  # 左肩
            (px + TILE_SIZE * 0.75, py + TILE_SIZE * 0.35),  # 右肩
            (px + TILE_SIZE * 0.85, py + TILE_SIZE * 0.85),  # 右下角
            (px + TILE_SIZE * 0.15, py + TILE_SIZE * 0.85),  # 左下角
        ]
        pygame.draw.polygon(self.screen, cape_color, cape_points)

        # ------ 躯干（盔甲） ------
        torso_rect = pygame.Rect(
            px + TILE_SIZE * 0.3, py + TILE_SIZE * 0.35,
            TILE_SIZE * 0.4, TILE_SIZE * 0.3
        )
        pygame.draw.rect(self.screen, armor_color, torso_rect)

        # 胸甲装饰线
        pygame.draw.line(
            self.screen, gold_trim,
            (px + TILE_SIZE * 0.3, py + TILE_SIZE * 0.45),
            (px + TILE_SIZE * 0.7, py + TILE_SIZE * 0.45),
            2
        )

        # 肩甲
        pygame.draw.rect(
            self.screen, armor_highlight,
            (px + TILE_SIZE * 0.25, py + TILE_SIZE * 0.35, TILE_SIZE * 0.2, TILE_SIZE * 0.1)
        )
        pygame.draw.rect(
            self.screen, armor_highlight,
            (px + TILE_SIZE * 0.55, py + TILE_SIZE * 0.35, TILE_SIZE * 0.2, TILE_SIZE * 0.1)
        )

        # ------ 头部与头盔 ------
        # 头盔
        helmet_points = [
            (px + TILE_SIZE * 0.35, py + TILE_SIZE * 0.25),  # 左侧
            (px + TILE_SIZE * 0.5, py + TILE_SIZE * 0.15),  # 顶部
            (px + TILE_SIZE * 0.65, py + TILE_SIZE * 0.25),  # 右侧
            (px + TILE_SIZE * 0.65, py + TILE_SIZE * 0.35),  # 右下
            (px + TILE_SIZE * 0.35, py + TILE_SIZE * 0.35),  # 左下
        ]
        pygame.draw.polygon(self.screen, armor_color, helmet_points)

        # 头盔装饰
        pygame.draw.line(
            self.screen, gold_trim,
            (px + TILE_SIZE * 0.5, py + TILE_SIZE * 0.15),
            (px + TILE_SIZE * 0.5, py + TILE_SIZE * 0.25),
            2
        )

        # 面罩开口处露出的脸部
        face_rect = pygame.Rect(
            px + TILE_SIZE * 0.4, py + TILE_SIZE * 0.25,
            TILE_SIZE * 0.2, TILE_SIZE * 0.1
        )
        pygame.draw.rect(self.screen, skin_color, face_rect)

        # 眼睛（简单威严表情）
        pygame.draw.line(
            self.screen, (0, 0, 0),
            (px + TILE_SIZE * 0.43, py + TILE_SIZE * 0.28),
            (px + TILE_SIZE * 0.46, py + TILE_SIZE * 0.28),
            1
        )
        pygame.draw.line(
            self.screen, (0, 0, 0),
            (px + TILE_SIZE * 0.54, py + TILE_SIZE * 0.28),
            (px + TILE_SIZE * 0.57, py + TILE_SIZE * 0.28),
            1
        )

        # ------ 腿部装甲 ------
        left_leg = pygame.Rect(
            px + TILE_SIZE * 0.35, py + TILE_SIZE * 0.65,
            TILE_SIZE * 0.1, TILE_SIZE * 0.25
        )
        right_leg = pygame.Rect(
            px + TILE_SIZE * 0.55, py + TILE_SIZE * 0.65,
            TILE_SIZE * 0.1, TILE_SIZE * 0.25
        )
        pygame.draw.rect(self.screen, armor_color, left_leg)
        pygame.draw.rect(self.screen, armor_color, right_leg)

        # 靴子
        pygame.draw.rect(
            self.screen, (40, 40, 40),
            (px + TILE_SIZE * 0.35, py + TILE_SIZE * 0.9, TILE_SIZE * 0.1, TILE_SIZE * 0.1)
        )
        pygame.draw.rect(
            self.screen, (40, 40, 40),
            (px + TILE_SIZE * 0.55, py + TILE_SIZE * 0.9, TILE_SIZE * 0.1, TILE_SIZE * 0.1)
        )

        # ------ 武器：大剑 ------
        # 剑位置（固定在右侧，威武姿态）
        sword_x = px + TILE_SIZE * 0.75
        sword_y = py + TILE_SIZE * 0.5

        # 剑柄
        pygame.draw.rect(
            self.screen, (80, 60, 40),
            (sword_x, sword_y, TILE_SIZE * 0.1, TILE_SIZE * 0.15)
        )

        # 护手
        pygame.draw.rect(
            self.screen, gold_trim,
            (sword_x - TILE_SIZE * 0.05, sword_y, TILE_SIZE * 0.2, TILE_SIZE * 0.05)
        )

        # 剑身：上长、锋利、威武
        blade_points = [
            (sword_x + TILE_SIZE * 0.05, sword_y),  # 连接护手
            (sword_x + TILE_SIZE * 0.05, py + TILE_SIZE * 0.2),  # 剑尖
            (sword_x + TILE_SIZE * 0.07, py + TILE_SIZE * 0.2),  # 剑尖右侧
            (sword_x + TILE_SIZE * 0.07, sword_y),  # 连回护手
        ]
        pygame.draw.polygon(self.screen, (180, 180, 200), blade_points)

        # 剑身中线（增加立体感）
        pygame.draw.line(
            self.screen, (220, 220, 230),
            (sword_x + TILE_SIZE * 0.06, sword_y),
            (sword_x + TILE_SIZE * 0.06, py + TILE_SIZE * 0.2),
            1
        )

        # ------ 左手盾牌 ------
        shield_x = px + TILE_SIZE * 0.15
        shield_y = py + TILE_SIZE * 0.5

        # 盾牌主体
        shield_points = [
            (shield_x, shield_y),  # 顶点
            (shield_x - TILE_SIZE * 0.15, shield_y + TILE_SIZE * 0.15),  # 左侧
            (shield_x, shield_y + TILE_SIZE * 0.3),  # 底部
            (shield_x + TILE_SIZE * 0.15, shield_y + TILE_SIZE * 0.15),  # 右侧
        ]
        pygame.draw.polygon(self.screen, armor_color, shield_points)

        # 盾牌边缘
        pygame.draw.lines(
            self.screen, gold_trim, True, shield_points, 2
        )

        # 盾牌花纹
        pygame.draw.circle(
            self.screen, gold_trim,
            (shield_x, shield_y + TILE_SIZE * 0.15), TILE_SIZE * 0.05
        )

    # --------------- 玩家技能释放 -----------------

    def cast_skill(self, skill_key):
        skill = self.player.skills[skill_key]
        if skill['current_cd'] > 0:
            self.add_message(f"{skill['name']}冷却中!")
            return

        if self.player.mp < skill.get('mp_cost', 0):
            self.add_message(f"魔法不足，无法释放{skill['name']}!")
            return

        self.player.mp -= skill.get('mp_cost', 0)

        # 火焰重击
        if skill_key == 'FireStrikeEffect':
            # 寻找有效目标
            targets = [
                m for m in self.monsters
                if abs(m.x - self.player.x) + abs(m.y - self.player.y) <= skill['range']
            ]

            if not targets:
                self.add_message("没有可攻击目标!")
                return

            target = random.choice(targets)
            # 创建技能效果
            effect = FireStrikeEffect(target.x, target.y, skill['radius'])
            self.add_message(f"释放{skill['name']}!")

            # 范围伤害
            for dx in range(-skill['radius'], skill['radius'] + 1):
                for dy in range(-skill['radius'], skill['radius'] + 1):
                    if abs(dx) + abs(dy) <= skill['radius']:
                        for m in self.monsters[:]:
                            if m.x == target.x + dx and m.y == target.y + dy:
                                dmg = self.player.atk * skill['damage_multiple']
                                m.hp -= max(dmg - m.defense, 0)
                                self.add_message(f"你对{m.name}造成{max(dmg - m.defense, 0)}点伤害！")
                                if m.hp <= 0:
                                    self.add_message(f"击败{m.name}，获得{m.coin}金币")
                                    self.player.coins += m.coin

            self.skill_effects.append(effect)

        # 闪电链
        elif skill_key == 'LightningEffect':
            # 获取范围内最近的3个目标
            targets = []
            for m in self.monsters:
                distance = self.calculate_distance(
                    (self.player.x, self.player.y),
                    (m.x, m.y)
                )
                if distance <= skill['range']:
                    targets.append((distance, m))

            if len(targets) < 1:
                self.add_message("没有可攻击目标!")
                return

            # 按距离排序并选择前N个
            targets.sort(key=lambda x: x[0])
            selected = [m for _, m in targets[:skill['max_targets']]]

            # 生成闪电链效果
            last_pos = (self.player.x * TILE_SIZE + TILE_SIZE // 2,
                        self.player.y * TILE_SIZE + TILE_SIZE // 2)
            total_damage = 0

            for i, monster in enumerate(selected):
                # 计算伤害
                dmg = self.player.atk * skill['damage_multiple']
                dmg = max(dmg - monster.defense, 0)
                monster.hp -= dmg
                total_damage += dmg

                # 闪电终点坐标
                end_pos = (monster.x * TILE_SIZE + TILE_SIZE // 2,
                           monster.y * TILE_SIZE + TILE_SIZE // 2)

                # 创建闪电效果
                effect = LightningEffect(
                    start=last_pos,
                    end=end_pos,
                    duration=0.5,
                    damage=dmg
                )
                self.skill_effects.append(effect)
                self.add_message(f"释放{skill['name']}!")

                # 更新上一个位置
                last_pos = end_pos

                # 处理怪物死亡
                if monster.hp <= 0:
                    self.add_message(f"击败{monster.name}，获得{monster.coin}金币")
                    self.player.coins += monster.coin
                    self.monsters.remove(monster)

            self.add_message(f"闪电链造成总计{total_damage}点伤害！")

        elif skill_key == 'HolyBallEffect':
            effect = HolyBallEffect(
                player_pos=(self.player.x, self.player.y),
                ball_count=skill['ball_count'],
                seek_range=skill['seek_range'],
                damage_multiplier=skill['damage_multiple']
            )
            self.skill_effects.append(effect)
            self.add_message(f"释放{skill['name']}!")

        elif skill_key == 'TripleAttack':
            effect = TripleAttack(
                player_pos=(self.player.x, self.player.y),
                attack_range=skill['range'],
                damage_multiplier=skill['damage_multipliers']
            )
            self.skill_effects.append(effect)
            self.add_message(f"释放{skill['name']}!")

        elif skill_key == 'SummonLightningBall':
            # 创建守护闪电球
            lightning_ball = SummonLightningBall(
                self.player,
                ball_count=skill['ball_count'],
                duration=skill['duration'],
                attack_range=skill['attack_range'],
                attack_speed=skill['attack_speed'],
                damage_multiple=skill['damage_multiple']
            )
            self.guardian_lightning_balls.append(lightning_ball)

            self.add_message(f"释放{skill['name']}!")

        elif skill_key == 'SummonHolyBall':
            # Create holy balls effect
            holy_ball = SummonHolyBall(
                self.player,
                ball_count=skill['ball_count'],
                duration=skill['duration'],
                attack_range=skill['attack_range'],
                attack_speed=skill['attack_speed'],
                damage_multiple=skill['damage_multiple'],
                heal_percent=skill['heal_percent']
            )
            self.guardian_lightning_balls.append(holy_ball)
            self.add_message(f"释放{skill['name']}!")

        skill['current_cd'] = skill['cooldown']

    # --------------- 游戏怪物绘制 -----------------

    # 怪物追踪状态指示
    def draw_monster_tracking_indicators(self):
        """绘制怪物的追踪状态指示器"""
        if not MONSTER_TRACKING_INDICATORS:
            return

        for monster in self.monsters:
            if monster.is_tracking:
                # 绘制追踪指示器
                x = monster.x * TILE_SIZE + TILE_SIZE // 2
                y = monster.y * TILE_SIZE - 10
                radius = 4

                # 绘制感叹号
                pygame.draw.circle(self.screen, (255, 0, 0), (x, y), radius + 2)
                pygame.draw.circle(self.screen, (255, 255, 255), (x, y), radius)

                # 感叹号竖线
                pygame.draw.line(self.screen, (255, 0, 0), (x, y - 3), (x, y + 1), 2)
                # 感叹号点
                pygame.draw.circle(self.screen, (255, 0, 0), (x, y + 3), 1)

                # 如果有路径且允许路径可视化，绘制路径点
                if MONSTER_PATH_VISUALIZATION and monster.path_to_player and len(monster.path_to_player) > 1:
                    # 只绘制部分路径点，避免过度绘制
                    path_points = monster.path_to_player[1:min(len(monster.path_to_player), 6)]

                    # 绘制怪物到第一个路径点的线
                    pygame.draw.line(self.screen, (255, 0, 0, 80),
                                     (monster.x * TILE_SIZE + TILE_SIZE // 2, monster.y * TILE_SIZE + TILE_SIZE // 2),
                                     (path_points[0][0] * TILE_SIZE + TILE_SIZE // 2,
                                      path_points[0][1] * TILE_SIZE + TILE_SIZE // 2),
                                     1)

                    # 绘制路径点之间的线
                    for i in range(len(path_points) - 1):
                        start = (path_points[i][0] * TILE_SIZE + TILE_SIZE // 2,
                                 path_points[i][1] * TILE_SIZE + TILE_SIZE // 2)
                        end = (path_points[i + 1][0] * TILE_SIZE + TILE_SIZE // 2,
                               path_points[i + 1][1] * TILE_SIZE + TILE_SIZE // 2)

                        # 使用半透明红色
                        pygame.draw.line(self.screen, (255, 0, 0, 50), start, end, 1)

                    # 绘制路径点
                    for point in path_points:
                        pygame.draw.circle(self.screen, (255, 150, 150, 120),
                                           (point[0] * TILE_SIZE + TILE_SIZE // 2,
                                            point[1] * TILE_SIZE + TILE_SIZE // 2),
                                           2)

            # 调试信息
            if MONSTER_DEBUG_INFO:
                # 显示怪物状态信息
                debug_y = monster.y * TILE_SIZE - 25
                debug_x = monster.x * TILE_SIZE

                # 状态文本
                status = "追踪中" if monster.is_tracking else "游荡中"
                status_surf = pygame.font.SysFont("SimHei", 12).render(status, True, (255, 255, 255))
                status_rect = status_surf.get_rect(center=(debug_x + TILE_SIZE // 2, debug_y))

                # 背景矩形
                bg_rect = status_rect.inflate(10, 5)
                pygame.draw.rect(self.screen, (0, 0, 0, 150), bg_rect)
                self.screen.blit(status_surf, status_rect)

                # 额外显示超时计时
                if monster.is_tracking:
                    timeout_text = f"{monster.tracking_timeout:.1f}/{monster.tracking_duration:.1f}"
                    timeout_surf = pygame.font.SysFont("Arial", 10).render(timeout_text, True, (255, 200, 200))
                    self.screen.blit(timeout_surf, (debug_x, debug_y - 15))

    def update_monsters(self, dt):
        for monster in self.monsters[:]:
            # 为怪物添加必要的属性，如果没有
            if not hasattr(monster, 'message_cooldown'):
                monster.message_cooldown = 0  # 消息冷却时间
                monster.detection_cooldown = 0  # 检测冷却时间
                monster.detection_interval = 1.0  # 每1秒检测一次玩家位置

            # 更新消息和检测冷却
            monster.message_cooldown = max(0, monster.message_cooldown - dt)
            monster.detection_cooldown = max(0, monster.detection_cooldown - dt)

            # 更新移动计数器
            monster.move_counter += dt * 60  # 累积时间，保持原单位

            # 更新追踪超时
            if monster.is_tracking:
                # 检查玩家是否仍在追踪范围内
                distance = self.calculate_distance((monster.x, monster.y), (self.player.x, self.player.y))

                if distance <= MONSTER_DISTANCE:
                    # 重置追踪超时
                    monster.tracking_timeout = 0
                else:
                    # 增加超时时间
                    monster.tracking_timeout += dt * 60

                    # 超过持续时间，停止追踪
                    if monster.tracking_timeout >= monster.tracking_duration:
                        monster.is_tracking = False
                        monster.path_to_player = []
                        monster.wander_direction = None
                        monster.wander_steps = 0
                        # 只有当消息冷却结束时才发送追踪丢失消息
                        if monster.message_cooldown <= 0:
                            self.add_message(f"{monster.name}失去了你的踪迹！")
                            monster.message_cooldown = 10.0  # 10秒内不再发送此类消息

            # 更新路径 - 使用秒为单位
            if monster.is_tracking:
                monster.path_update_cooldown -= dt * 60
                if monster.path_update_cooldown <= 0:
                    # 更新到玩家的路径
                    monster.path_to_player = self.find_path_for_monster(monster, (self.player.x, self.player.y))
                    monster.path_update_cooldown = monster.path_update_rate

                    # 如果找不到路径，停止追踪
                    if not monster.path_to_player:
                        monster.is_tracking = False
                        monster.wander_direction = None
                        monster.wander_steps = 0

            # 定期检查玩家位置，而不是每帧都检查
            if monster.detection_cooldown <= 0:
                # 重置检测冷却
                monster.detection_cooldown = monster.detection_interval

                # 检查是否应该开始追踪
                if not monster.is_tracking:
                    distance = self.calculate_distance((monster.x, monster.y), (self.player.x, self.player.y))
                    if distance <= MONSTER_DISTANCE:
                        # 开始追踪
                        monster.is_tracking = True
                        monster.tracking_timeout = 0
                        monster.path_update_cooldown = 0  # 立即更新路径
                        monster.wander_direction = None

                        # 添加消息（只有当消息冷却结束时）
                        if monster.message_cooldown <= 0:
                            self.add_message(f"{monster.name}发现了你！")
                            monster.message_cooldown = 8.0  # 8秒内不再发送发现消息

            # 移动逻辑 - 当移动计数器达到怪物速度参数时移动
            if monster.move_counter >= monster.speed:
                # 重置移动计数器
                monster.move_counter = 0

                # 保存当前位置以检测卡住
                current_pos = (monster.x, monster.y)

                # 根据追踪状态决定移动逻辑
                if monster.is_tracking and monster.path_to_player:
                    # 追踪模式：按路径移动
                    self.move_monster_along_path(monster)
                else:
                    # 游荡模式：随机移动
                    self.move_monster_randomly(monster)

                # 检测怪物是否卡住
                if current_pos == (monster.x, monster.y):
                    monster.stuck_counter += 1

                    # 如果连续卡住多次，重置移动状态
                    if monster.stuck_counter >= 3:
                        monster.stuck_counter = 0
                        monster.is_tracking = False
                        monster.path_to_player = []
                        monster.wander_direction = None
                        monster.wander_steps = 0
                else:
                    monster.stuck_counter = 0
                    monster.last_pos = current_pos

    def find_path_for_monster(self, monster, target):
        """为怪物寻找到目标的路径，考虑怪物尺寸"""
        # 获取怪物尺寸
        size_x, size_y = monster.size

        # 怪物的起始位置
        start = (monster.x, monster.y)

        # 不直接寻路到玩家位置，而是找到玩家附近的可到达点
        # 这样怪物不会尝试与玩家重叠
        nearby_tiles = []

        # 检查玩家周围的格子
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                # 跳过玩家自己的位置
                if dx == 0 and dy == 0:
                    continue

                # 计算相邻格子
                nearby_x = target[0] + dx
                nearby_y = target[1] + dy

                # 检查是否可通行
                if self.can_monster_move_to(monster, nearby_x, nearby_y):
                    # 计算到玩家的曼哈顿距离
                    distance = abs(nearby_x - target[0]) + abs(nearby_y - target[1])
                    nearby_tiles.append((distance, (nearby_x, nearby_y)))

        # 如果没有找到可到达的相邻格子，直接返回空路径
        if not nearby_tiles:
            return []

        # 按距离排序，优先选择离玩家最近的格子
        nearby_tiles.sort()
        target_pos = nearby_tiles[0][1]

        # 使用 BFS 寻找路径
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上下左右
        queue = deque([start])
        visited = {start: None}  # 记录访问过的节点及其父节点

        # 获取所有怪物位置（排除自己）
        monster_positions = set()
        for m in self.monsters:
            if m is not monster:  # 排除自己
                for dx in range(m.size[0]):
                    for dy in range(m.size[1]):
                        monster_positions.add((m.x + dx, m.y + dy))

        while queue:
            current = queue.popleft()
            if current == target_pos:
                # 重建路径
                path = []
                while current is not None:
                    path.append(current)
                    current = visited[current]
                return path[::-1]  # 反转路径

            for dx, dy in directions:
                next_pos = (current[0] + dx, current[1] + dy)

                # 检查该位置是否适合怪物移动
                if self.can_monster_move_to(monster, next_pos[0], next_pos[1]) and next_pos not in visited:
                    queue.append(next_pos)
                    visited[next_pos] = current

        # 没有找到路径
        return []

    def move_monster_along_path(self, monster):
        """沿路径移动怪物"""
        if not monster.path_to_player or len(monster.path_to_player) < 2:
            # 路径为空或只有起点，无法移动
            return

        # 获取下一个位置（路径中的第二个点，因为第一个是当前位置）
        next_pos = monster.path_to_player[1]

        # 检查下一位置是否仍然可通行
        if self.can_monster_move_to(monster, next_pos[0], next_pos[1]):
            # 移动到下一个位置 - 不需要考虑速度，因为这个函数只在计数器达到阈值时调用
            monster.x = next_pos[0]
            monster.y = next_pos[1]

            # 更新路径（移除已经到达的点）
            monster.path_to_player.pop(0)
        else:
            # 如果下一个位置不可通行，重新计算路径
            monster.path_update_cooldown = 0  # 触发路径重新计算
            monster.path_to_player = []  # 清空当前路径

    def move_monster_randomly(self, monster):
        """随机移动怪物"""
        # 如果没有当前方向或者已经走完步数，选择新方向
        if monster.wander_direction is None or monster.wander_steps <= 0:
            # 随机选择方向
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上下左右
            random.shuffle(directions)

            # 尝试每个方向
            for dx, dy in directions:
                new_x = monster.x + dx
                new_y = monster.y + dy

                if self.can_monster_move_to(monster, new_x, new_y):
                    monster.wander_direction = (dx, dy)
                    monster.wander_steps = random.randint(1, 3)  # 随机步数
                    break

            # 如果所有方向都不可行，保持原地
            if monster.wander_direction is None:
                return

        # 按当前方向移动
        dx, dy = monster.wander_direction
        new_x = monster.x + dx
        new_y = monster.y + dy

        if self.can_monster_move_to(monster, new_x, new_y):
            monster.x = new_x
            monster.y = new_y
            monster.wander_steps -= 1
        else:
            # 如果当前方向不可行，重置方向
            monster.wander_direction = None
            monster.wander_steps = 0

    def color_reverse(self, color):
        return (255 - color[0], 255 - color[0], 255 - color[0])

    # -------------- 血腥闪电绘制函数 -------------------------------
    def draw_lightning_boss(self, monster):
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE

        # 动态参数
        anim_time = pygame.time.get_ticks()

        # 根据BOSS名称选择配色
        if "纯青" in monster.name:
            ball_colors = [(0, 191, 255), (0, 255, 255), (0, 150, 255), (0, 200, 255), (0, 100, 255), (0, 255, 200)]
        elif "金色" in monster.name:
            ball_colors = [(255, 215, 0), (255, 165, 0), (255, 140, 0), (255, 200, 0), (255, 180, 0), (255, 220, 0)]
        else:  # 默认血腥闪电配色
            ball_colors = [(178, 34, 34), (139, 0, 0), (220, 20, 60), (255, 36, 0), (200, 36, 80), (150, 30, 30)]

        # 更新闪电球位置（混沌运动）
        if not self.lightning_balls:
            # 初始化六个球体的位置
            self.lightning_balls = [
                {'pos': (x + TILE_SIZE, y + TILE_SIZE),
                 'dir': random.uniform(0, self.s * math.pi),
                 'size': self.radius_small},
                {'pos': (x + TILE_SIZE, y + TILE_SIZE),
                 'dir': random.uniform(0, self.s * math.pi),
                 'size': self.radius_small},
                {'pos': (x + TILE_SIZE, y + TILE_SIZE),
                 'dir': random.uniform(0, self.s * math.pi),
                 'size': self.radius_small},
                {'pos': (x + TILE_SIZE, y + TILE_SIZE),
                 'dir': random.uniform(0, self.s * math.pi),
                 'size': self.radius_small},
                {'pos': (x + TILE_SIZE, y + TILE_SIZE),
                 'dir': random.uniform(0, self.s * math.pi),
                 'size': self.radius_small},
                {'pos': (x + TILE_SIZE, y + TILE_SIZE),
                 'dir': random.uniform(0, self.s * math.pi),
                 'size': self.radius_small}
            ]

        # 绘制六个闪电球体
        for i, ball in enumerate(self.lightning_balls):
            # 更新位置（混沌运动）
            ball['dir'] += random.uniform(-0.3, 0.3)
            ball['pos'] = (
                x + TILE_SIZE * 1.5 + math.sin(anim_time / 200 + i) * TILE_SIZE * self.radius_large,
                y + TILE_SIZE * 1.5 + math.cos(anim_time / 300 + i) * TILE_SIZE * self.radius_large
            )

            # 绘制球体核心
            pygame.draw.circle(self.screen, ball_colors[i],
                               (int(ball['pos'][0]), int(ball['pos'][1])),
                               int(ball['size'] * abs(math.sin(anim_time / 100))))

            # 绘制闪电连接
            self.draw_lightning((x + TILE_SIZE * 1.5 + math.sin(anim_time / 200 + i) * TILE_SIZE * self.radius_large,
                y + TILE_SIZE * 1.5 + math.cos(anim_time / 300 + i) * TILE_SIZE * self.radius_large), (x + TILE_SIZE * 1.5 + math.sin(anim_time / 200 + (i+1)%6) * TILE_SIZE * self.radius_large,
                y + TILE_SIZE * 1.5 + math.cos(anim_time / 300 + (i+1)%6) * TILE_SIZE * self.radius_large), 4, ball_colors[i])
            self.draw_lightning((x + TILE_SIZE * 1.5 + math.sin(anim_time / 200 + i) * TILE_SIZE * self.radius_large,
                y + TILE_SIZE * 1.5 + math.cos(anim_time / 300 + i) * TILE_SIZE * self.radius_large), (x + TILE_SIZE * 1.5 + math.sin(anim_time / 200 + (i+1)%6) * TILE_SIZE * self.radius_large,
                y + TILE_SIZE * 1.5 + math.cos(anim_time / 300 + (i+1)%6) * TILE_SIZE * self.radius_large), 9, ball_colors[i])

    def draw_lightning(self, start, end, thickness, color):
        """绘制闪电效果，增加分叉和火花效果"""
        # 生成主路径
        main_points = self.generate_lightning_points(start, end, branch_prob=0.3)
        lthickness = random.randint(1, thickness)

        # 绘制主闪电
        for i in range(len(main_points) - 1):
            start_pos = main_points[i]
            end_pos = main_points[i + 1]
            # 主闪电颜色随机变化
            main_color = random.choice(
                [color, (min(color[0] + 50, 255), min(color[1] + 50, 255), min(color[2] + 50, 255)), ( max(color[0] - 50, 0), max(color[1] - 50, 0), max(color[2] - 50, 0))])
            pygame.draw.line(self.screen, main_color, start_pos, end_pos, lthickness)

            # 50%概率生成分叉闪电
            if random.random() < 0.5 and i < len(main_points) - 2:
                mid_point = ((start_pos[0] + end_pos[0]) // 2, (start_pos[1] + end_pos[1]) // 2)
                branch_end = (
                    mid_point[0] + random.randint(-30, 30),
                    mid_point[1] + random.randint(-30, 30)
                )
                branch_points = self.generate_lightning_points(mid_point, branch_end, branch_prob=0.5)

                # 绘制分叉闪电
                for j in range(len(branch_points) - 1):
                    pygame.draw.line(self.screen,
                                     (min(color[0] + 100, 255), min(color[1] + 100, 255), min(color[2] + 100, 255)),
                                     branch_points[j], branch_points[j + 1], max(1, lthickness - 1))

                # 在分叉点添加离子火花
                if random.random() < 0.02:
                    self.add_ion_sparks(mid_point, intensity=0.5)


        # 添加主路径火花
        if random.random() < 0.04:
            self.add_ion_sparks(end)

    # 生成闪电路径点，增加随机分叉
    def generate_lightning_points(self, start, end, branch_prob=0.2):
        points = [start]
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        length = math.hypot(dx, dy)
        segments = max(5, int(length / 10))  # 动态分段

        for i in range(1, segments):
            t = i / segments
            # 基础插值
            base_x = start[0] + dx * t
            base_y = start[1] + dy * t

            # 随机偏移（越接近末端偏移越小）
            offset_range = 20 * (1 - t ** 2)
            offset_x = random.uniform(-offset_range, offset_range)
            offset_y = random.uniform(-offset_range, offset_range)

            # 加入分叉点
            if random.random() < branch_prob:
                points.append((int(base_x + offset_x * 0.5), int(base_y + offset_y * 0.5)))

            points.append((int(base_x + offset_x), int(base_y + offset_y)))

        points.append(end)
        return points

    # 添加离子火花效果
    def add_ion_sparks(self, pos, intensity=1.5):
        """添加离子火花效果"""
        for _ in range(int(15 * intensity)):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 6) * intensity
            lifespan = random.uniform(0.3, 1.5)

            # 随机颜色（黄白色系）
            spark_color = random.choice([
                (255, 150, 255),
                (255, 100, 200),
                (255, 255, 200),
                (255, 51, 51)
            ])

            self.fear_particles.append({
                'pos': list(pos),  # 火花初始位置
                'vel': [math.cos(angle) * speed, math.sin(angle) * speed],  # 速度向量
                'life': lifespan,  # 当前生命周期
                'max_life': lifespan,  # 最大生命周期
                'size': random.uniform(1, 3),  # 火花大小
                'color': spark_color  # 火花颜色
            })

    # -------------------- 蝙蝠绘制 ---------------------

    def draw_bat(self, monster):
        # Base position
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE

        # Animation parameters
        anim_time = pygame.time.get_ticks()
        flap_speed = anim_time / 150  # Wing flapping speed
        flap_position = math.sin(flap_speed)  # -1 to 1 value for wing position
        hover_offset = int(math.sin(anim_time / 400) * 2)  # Vertical hovering motion

        # Colors based on bat type
        if "白色" in monster.name:
            body_color = (200, 200, 210)  # Light gray for white bat
            wing_color = (170, 170, 180)  # Slightly darker for wings
            eye_color = (255, 0, 0)  # Red eyes
        else:
            body_color = (54, 54, 54)  # Dark gray for regular bat
            wing_color = (30, 30, 30)  # Black wings
            eye_color = (255, 0, 0)  # Red eyes

        # Center point of the bat
        center_x = x + TILE_SIZE // 2
        center_y = y + TILE_SIZE // 2 + hover_offset

        # Body size parameters - reduced overall size
        body_width = TILE_SIZE // 4  # Reduced from TILE_SIZE // 3
        body_height = TILE_SIZE // 3  # Reduced from TILE_SIZE // 2
        head_radius = TILE_SIZE // 8  # Reduced from TILE_SIZE // 6

        # Draw the bat body (oval shape)
        body_rect = pygame.Rect(
            center_x - body_width // 2,
            center_y - body_height // 2,
            body_width,
            body_height
        )
        pygame.draw.ellipse(self.screen, body_color, body_rect)

        # Draw the head
        head_y = center_y - body_height // 3  # Position head at upper part of body
        pygame.draw.circle(self.screen, body_color, (center_x, head_y), head_radius)

        # Draw the ears (triangular)
        ear_height = head_radius
        ear_width = head_radius // 2

        # Left ear
        left_ear_points = [
            (center_x - ear_width, head_y - head_radius // 2),
            (center_x - ear_width // 2, head_y - head_radius - ear_height),
            (center_x, head_y - head_radius // 2)
        ]
        pygame.draw.polygon(self.screen, body_color, left_ear_points)

        # Right ear
        right_ear_points = [
            (center_x, head_y - head_radius // 2),
            (center_x + ear_width // 2, head_y - head_radius - ear_height),
            (center_x + ear_width, head_y - head_radius // 2)
        ]
        pygame.draw.polygon(self.screen, body_color, right_ear_points)

        # Draw the eyes (red and glowing)
        eye_radius = max(2, head_radius // 3)
        eye_spacing = head_radius

        # Left eye
        pygame.draw.circle(self.screen, eye_color,
                           (center_x - eye_spacing // 2, head_y),
                           eye_radius)

        # Right eye
        pygame.draw.circle(self.screen, eye_color,
                           (center_x + eye_spacing // 2, head_y),
                           eye_radius)

        # Draw the wings with animation - reduced wing span
        wing_span = TILE_SIZE * (0.4 + 0.2 * abs(flap_position))  # Reduced from 0.5 + 0.3
        wing_droop = 0.2 - 0.2 * flap_position  # Wing droop varies with flap

        # Left wing
        left_wing_tip_x = center_x - wing_span
        left_wing_tip_y = center_y - wing_span * wing_droop

        left_wing_points = [
            (center_x - body_width // 3, center_y - body_height // 4),  # Wing base
            (center_x - wing_span // 2, center_y - wing_span * 0.3),  # Wing middle
            (left_wing_tip_x, left_wing_tip_y),  # Wing tip
            (center_x - wing_span // 2, center_y + body_height // 4)  # Wing bottom
        ]
        pygame.draw.polygon(self.screen, wing_color, left_wing_points)

        # Right wing
        right_wing_tip_x = center_x + wing_span
        right_wing_tip_y = center_y - wing_span * wing_droop

        right_wing_points = [
            (center_x + body_width // 3, center_y - body_height // 4),  # Wing base
            (center_x + wing_span // 2, center_y - wing_span * 0.3),  # Wing middle
            (right_wing_tip_x, right_wing_tip_y),  # Wing tip
            (center_x + wing_span // 2, center_y + body_height // 4)  # Wing bottom
        ]
        pygame.draw.polygon(self.screen, wing_color, right_wing_points)

        # Wing bone structure (simple lines)
        # Left wing bones
        pygame.draw.line(self.screen, body_color,
                         left_wing_points[0], left_wing_points[2], 1)
        pygame.draw.line(self.screen, body_color,
                         left_wing_points[0], left_wing_points[3], 1)

        # Right wing bones
        pygame.draw.line(self.screen, body_color,
                         right_wing_points[0], right_wing_points[2], 1)
        pygame.draw.line(self.screen, body_color,
                         right_wing_points[0], right_wing_points[3], 1)

        # Legs/claws (small details)
        claw_length = body_height // 3
        pygame.draw.line(self.screen, body_color,
                         (center_x - body_width // 4, center_y + body_height // 2),
                         (center_x - body_width // 4, center_y + body_height // 2 + claw_length), 1)
        pygame.draw.line(self.screen, body_color,
                         (center_x + body_width // 4, center_y + body_height // 2),
                         (center_x + body_width // 4, center_y + body_height // 2 + claw_length), 1)

    # -------------------- 腐蚀怪绘制 ---------------------
    def draw_corrosion_monster(self, monster):
        # Base position
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE

        # Animation parameters
        anim_time = pygame.time.get_ticks()
        pulse_factor = 0.15 * math.sin(anim_time / 300)  # Pulsing effect

        # Color definitions
        base_color = (91, 13, 133)  # Dark purple base
        spot_color = (139, 0, 0)  # Blood red spots
        drip_color = (120, 10, 120)  # Drip color
        bubble_color = (160, 32, 240)  # Bubble highlights

        # Center coordinates
        center_x = x + TILE_SIZE // 2
        center_y = y + TILE_SIZE // 2

        # Calculate wobble radius with pulsing
        radius_x = int(TILE_SIZE // 2 * (1 + pulse_factor))
        radius_y = int(TILE_SIZE // 2 * (1 - pulse_factor * 0.5))

        # Draw wobbling main body (elliptical shape)
        body_rect = pygame.Rect(
            center_x - radius_x,
            center_y - radius_y,
            radius_x * 2,
            radius_y * 2
        )
        pygame.draw.ellipse(self.screen, base_color, body_rect)

        # Draw a darker bottom area for depth
        bottom_rect = pygame.Rect(
            center_x - radius_x * 0.8,
            center_y + radius_y * 0.2,
            radius_x * 1.6,
            radius_y * 0.8
        )
        darker_color = (70, 5, 100)  # Darker version of base color
        pygame.draw.ellipse(self.screen, darker_color, bottom_rect)

        # Draw blood-like spots in pseudo-random positions based on animation time
        num_spots = 6
        for i in range(num_spots):
            # Use animation time to create semi-random but stable spot positions
            angle = math.radians((i * 60 + anim_time // 30) % 360)
            distance = TILE_SIZE // 3 * (0.5 + 0.3 * math.sin(anim_time / 400 + i))

            spot_x = center_x + math.cos(angle) * distance
            spot_y = center_y + math.sin(angle) * distance
            spot_size = 2 + i % 3  # Vary spot sizes

            pygame.draw.circle(self.screen, spot_color, (int(spot_x), int(spot_y)), spot_size)

        # Draw surface wave/bulge effects to show movement
        for i in range(3):
            wave_y = y + TILE_SIZE // 2 + i * 8
            wave_width = TILE_SIZE // 2 - i * 3
            wave_height = 6
            wave_x = x + TILE_SIZE // 2 - wave_width // 2

            # Make waves move
            wave_x += int(math.sin(anim_time / 200 + i * 1.5) * 4)

            wave_rect = pygame.Rect(wave_x, wave_y, wave_width, wave_height)
            pygame.draw.ellipse(self.screen, bubble_color, wave_rect)

        # Occasionally create dripping effect
        if anim_time % 500 < 200:  # Drip visible 40% of the time
            drip_x = center_x + int(math.sin(anim_time / 1000) * (TILE_SIZE // 3))
            drip_length = 5 + int(3 * math.sin(anim_time / 250))

            pygame.draw.line(self.screen, drip_color,
                             (drip_x, y + TILE_SIZE - 2),
                             (drip_x, y + TILE_SIZE + drip_length), 3)

            # Drip droplet at the end
            pygame.draw.circle(self.screen, drip_color,
                               (drip_x, y + TILE_SIZE + drip_length), 2)

        # Add bubbling effect (small bubbles occasionally rising)
        if random.random() < 0.3:  # 30% chance each frame
            bubble_x = center_x + random.randint(-radius_x // 2, radius_x // 2)
            bubble_y = center_y + random.randint(-radius_y // 2, radius_y // 2)
            bubble_radius = random.randint(1, 3)

            # Draw bubble with highlight
            pygame.draw.circle(self.screen, bubble_color,
                               (bubble_x, bubble_y), bubble_radius)
            pygame.draw.circle(self.screen, (200, 100, 220),
                               (bubble_x - 1, bubble_y - 1), bubble_radius // 2)

        # Draw eyes (more menacing)
        eye_spacing = TILE_SIZE // 3
        eye_y = center_y - radius_y // 2
        eye_size = 3

        # Left eye
        pygame.draw.circle(self.screen, (255, 20, 20),
                           (center_x - eye_spacing // 2, eye_y), eye_size)

        # Right eye
        pygame.draw.circle(self.screen, (255, 20, 20),
                           (center_x + eye_spacing // 2, eye_y), eye_size)

        # Add small pupil to each eye for more detail
        pygame.draw.circle(self.screen, (0, 0, 0),
                           (center_x - eye_spacing // 2, eye_y), 1)
        pygame.draw.circle(self.screen, (0, 0, 0),
                           (center_x + eye_spacing // 2, eye_y), 1)

    # -------------------- 火焰骑士绘制 ---------------------
    def draw_fire_knight(self, monster):
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE
        # 动画参数
        anim_time = pygame.time.get_ticks()
        hammer_swing = math.sin(anim_time / 300) * 0.5  # 锤子摆动弧度
        shield_glow = abs(math.sin(anim_time / 500))  # 盾牌发光强度
        armor_pulse = 0.1 * math.sin(anim_time / 400)  # 盔甲呼吸效果

        # 颜色定义
        if "纯" in monster.name:
            body_color = (50, 140, 220)  # 纯火焰骑士为冰蓝色
            flame_color = (30, 150, 255)  # 冰焰颜色
            highlight_color = (150, 200, 255)  # 高光色
            ember_colors = [(100, 200, 255), (150, 220, 255), (200, 240, 255)]  # 冰焰微粒
        else:
            body_color = (80, 40, 30)  # 暗红褐色基底
            flame_color = (220, 100, 50)  # 火焰颜色
            highlight_color = (255, 200, 100)  # 高光色
            ember_colors = [(255, 180, 0), (255, 120, 0), (255, 60, 0)]  # 火焰微粒

        # ---- 躯干 ----
        # 基础体型（1x1格子）调整为略微更大
        torso_width = int(TILE_SIZE * (0.6 + armor_pulse))
        torso_height = int(TILE_SIZE * (0.7 + armor_pulse))
        torso_x = x + (TILE_SIZE - torso_width) // 2
        torso_y = y + (TILE_SIZE - torso_height) // 2 + 5  # 下移调整位置

        # 绘制躯干主体
        pygame.draw.rect(self.screen, body_color,
                         (torso_x, torso_y, torso_width, torso_height),
                         border_radius=3)

        # ---- 头部 ----
        # 方形头盔（略大一点）
        head_size = TILE_SIZE // 3
        head_x = x + (TILE_SIZE - head_size) // 2
        head_y = torso_y - head_size + 5  # 让头部略微嵌入躯干

        # 头盔主体 - 更精细的渐变
        pygame.draw.rect(self.screen, body_color,
                         (head_x, head_y, head_size, head_size),
                         border_radius=2)

        # 头盔装饰纹路 - 增加质感
        pygame.draw.line(self.screen, highlight_color,
                         (head_x, head_y + head_size // 3),
                         (head_x + head_size, head_y + head_size // 3), 1)

        # 眼部发光 - 强化动态效果
        eye_size = head_size // 4
        eye_y = head_y + head_size // 3
        eye_spacing = head_size // 2
        eye_glow = 150 + int(100 * math.sin(anim_time / 250))  # 动态发光

        # 左眼
        if "纯" in monster.name:
            eye_color = (0, eye_glow, 255)  # 冰蓝眼睛
        else:
            eye_color = (255, eye_glow, 0)  # 火红眼睛

        pygame.draw.rect(self.screen, eye_color,
                         (head_x + (head_size - eye_spacing) // 2 - eye_size // 2,
                          eye_y, eye_size, eye_size // 2))

        # 右眼
        pygame.draw.rect(self.screen, eye_color,
                         (head_x + (head_size + eye_spacing) // 2 - eye_size // 2,
                          eye_y, eye_size, eye_size // 2))

        # 恶魔之角 - 更尖锐立体
        horn_height = head_size // 2
        # 左角
        pygame.draw.polygon(self.screen, body_color, [
            (head_x, head_y),
            (head_x - head_size // 4, head_y - horn_height),
            (head_x + head_size // 4, head_y)
        ])
        # 右角
        pygame.draw.polygon(self.screen, body_color, [
            (head_x + head_size, head_y),
            (head_x + head_size + head_size // 4, head_y - horn_height),
            (head_x + head_size - head_size // 4, head_y)
        ])

        # ---- 深渊铠甲 ----
        # 肩甲
        shoulder_height = torso_height // 4
        pygame.draw.rect(self.screen, highlight_color,
                         (torso_x - 2, torso_y, torso_width + 4, shoulder_height),
                         border_radius=2)

        # 胸甲（带精细恶魔浮雕）
        chest_x = torso_x + torso_width // 4
        chest_y = torso_y + shoulder_height + 2
        chest_width = torso_width // 2
        chest_height = torso_height // 2

        # 绘制胸甲基底
        pygame.draw.rect(self.screen, body_color,
                         (chest_x, chest_y, chest_width, chest_height),
                         border_radius=1)

        # 浮雕细节 - 增加神秘恶魔符文
        symbol_size = min(chest_width, chest_height) // 2
        symbol_x = chest_x + (chest_width - symbol_size) // 2
        symbol_y = chest_y + (chest_height - symbol_size) // 2

        # 动态发光符文
        if anim_time % 1000 < 500:  # 间歇性发光
            rune_intensity = 100 + int(155 * shield_glow)
            if "纯" in monster.name:
                rune_color = (0, rune_intensity, 255)
            else:
                rune_color = (255, rune_intensity, 0)

            # 五角星符文
            pygame.draw.polygon(self.screen, rune_color, [
                (symbol_x + symbol_size // 2, symbol_y),
                (symbol_x + symbol_size, symbol_y + symbol_size * 3 // 4),
                (symbol_x, symbol_y + symbol_size * 3 // 4),
                (symbol_x + symbol_size, symbol_y + symbol_size // 4),
                (symbol_x, symbol_y + symbol_size // 4)
            ], 1)

        # ---- 地狱重锤 ----
        hammer_length = TILE_SIZE * 0.7
        hammer_angle = math.radians(30 + hammer_swing * 30)  # 更大摆动范围
        hammer_base_x = torso_x + torso_width
        hammer_base_y = torso_y + torso_height // 2

        hammer_head_x = hammer_base_x + math.cos(hammer_angle) * hammer_length
        hammer_head_y = hammer_base_y + math.sin(hammer_angle) * hammer_length

        # 锤柄（带纹理）
        pygame.draw.line(self.screen, (60, 40, 20),
                         (hammer_base_x, hammer_base_y),
                         (hammer_head_x, hammer_head_y), 3)

        # 锤头（更精细的设计）
        hammer_head_size = TILE_SIZE // 5  # 锤头尺寸

        # 绘制锤头主体
        if "纯" in monster.name:
            pygame.draw.circle(self.screen, (30, 120, 200),
                               (int(hammer_head_x), int(hammer_head_y)), hammer_head_size)
        else:
            pygame.draw.circle(self.screen, (160, 40, 40),
                               (int(hammer_head_x), int(hammer_head_y)), hammer_head_size)

        # 锤头装饰 - 尖刺效果
        spikes = 5
        for i in range(spikes):
            spike_angle = i * (2 * math.pi / spikes) + anim_time / 500  # 缓慢旋转
            spike_length = hammer_head_size * 0.7
            spike_end_x = hammer_head_x + math.cos(spike_angle) * spike_length
            spike_end_y = hammer_head_y + math.sin(spike_angle) * spike_length

            pygame.draw.line(self.screen, highlight_color,
                             (hammer_head_x, hammer_head_y),
                             (spike_end_x, spike_end_y), 2)

        # ---- 邪能盾牌 ----
        shield_center = (torso_x - torso_width // 4, torso_y + torso_height // 2)
        shield_size = torso_width // 2

        # 盾牌基底 - 六边形更适合骑士
        if "纯" in monster.name:
            shield_color = (30, 100, 200)  # 冰蓝盾牌
        else:
            shield_color = (120, 40, 40)  # 暗红盾牌

        shield_points = []
        for i in range(6):
            angle = i * (2 * math.pi / 6) + math.pi / 6  # 旋转使六边形直立
            px = shield_center[0] + math.cos(angle) * shield_size
            py = shield_center[1] + math.sin(angle) * shield_size
            shield_points.append((px, py))

        pygame.draw.polygon(self.screen, shield_color, shield_points)

        # 盾牌发光符文 - 更精细的符文
        rune_color = flame_color
        rune_size = shield_size * 0.5 * (0.8 + 0.2 * shield_glow)  # 动态大小

        # 中心十字符文
        pygame.draw.line(self.screen, rune_color,
                         (shield_center[0] - rune_size, shield_center[1]),
                         (shield_center[0] + rune_size, shield_center[1]), 2)
        pygame.draw.line(self.screen, rune_color,
                         (shield_center[0], shield_center[1] - rune_size),
                         (shield_center[0], shield_center[1] + rune_size), 2)

        # 周围小圆
        small_circles = 3
        for i in range(small_circles):
            circle_angle = i * (2 * math.pi / small_circles) + anim_time / 800  # 缓慢旋转
            circle_distance = rune_size * 0.7
            circle_x = shield_center[0] + math.cos(circle_angle) * circle_distance
            circle_y = shield_center[1] + math.sin(circle_angle) * circle_distance
            circle_size = rune_size * 0.15 * (0.8 + 0.2 * math.sin(anim_time / 300 + i))

            pygame.draw.circle(self.screen, highlight_color,
                               (int(circle_x), int(circle_y)), int(circle_size))

        # ---- 火焰/冰焰特效 ----
        ember_count = 5 + int(3 * math.sin(anim_time / 400))  # 动态数量

        # 从锤头和角生成火焰/冰焰微粒
        emission_points = [
            (hammer_head_x, hammer_head_y),  # 锤头
            (head_x - head_size // 4, head_y - horn_height),  # 左角
            (head_x + head_size + head_size // 4, head_y - horn_height)  # 右角
        ]

        for point in emission_points:
            for _ in range(ember_count // 2):
                # 随机方向、大小和透明度
                ember_angle = random.uniform(0, math.pi * 2)
                ember_distance = random.uniform(2, 8)
                ember_size = random.uniform(1, 3)
                ember_alpha = random.randint(100, 200)

                # 计算位置
                ember_x = point[0] + math.cos(ember_angle) * ember_distance
                ember_y = point[1] + math.sin(ember_angle) * ember_distance

                # 绘制微粒
                ember_color = random.choice(ember_colors)
                pygame.draw.circle(self.screen, (*ember_color, ember_alpha),
                                   (int(ember_x), int(ember_y)), int(ember_size))

        # ---- 地面阴影 ----
        shadow_surface = pygame.Surface((TILE_SIZE, TILE_SIZE // 4), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 60),
                            (0, 0, TILE_SIZE, TILE_SIZE // 4))
        self.screen.blit(shadow_surface, (x, y + TILE_SIZE - TILE_SIZE // 6))

    # -------------------- 骷髅绘制 ---------------------
    def draw_skeleton(self, monster):
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE

        # Animation parameters - subtle for small space
        anim_time = pygame.time.get_ticks()
        jaw_motion = math.sin(anim_time / 300) * 1.5  # Subtle jaw movement

        # Bone colors
        bone_color = (240, 240, 220)  # Bone white
        shadow_color = (210, 210, 190)  # Subtle shadow for bones

        # Create a central alignment point
        center_x = x + TILE_SIZE // 2
        center_y = y + TILE_SIZE // 2

        # Draw skull (smaller and centered in the tile)
        skull_radius = TILE_SIZE // 5
        skull_y = center_y - TILE_SIZE // 3
        pygame.draw.circle(self.screen, bone_color, (center_x, skull_y), skull_radius)

        # Eye sockets (small but visible)
        eye_size = max(2, TILE_SIZE // 12)
        pygame.draw.circle(self.screen, (30, 30, 30),
                           (center_x - skull_radius // 2, skull_y - 1), eye_size)
        pygame.draw.circle(self.screen, (30, 30, 30),
                           (center_x + skull_radius // 2, skull_y - 1), eye_size)

        # Jaw (simple but animated)
        jaw_width = skull_radius * 1.5
        jaw_y_offset = int(jaw_motion)
        pygame.draw.polygon(self.screen, bone_color, [
            (center_x - jaw_width // 2, skull_y + skull_radius // 2),
            (center_x + jaw_width // 2, skull_y + skull_radius // 2),
            (center_x + jaw_width // 2 - 2, skull_y + skull_radius + jaw_y_offset),
            (center_x - jaw_width // 2 + 2, skull_y + skull_radius + jaw_y_offset)
        ])

        # Spine and ribs (simplified for small tiles)
        spine_top = skull_y + skull_radius + jaw_y_offset + 2
        spine_bottom = center_y + TILE_SIZE // 4

        # Spine (central line with segments)
        spine_segments = 3  # Fewer segments for small space
        for i in range(spine_segments):
            segment_y = spine_top + (spine_bottom - spine_top) * i // spine_segments
            segment_height = (spine_bottom - spine_top) // spine_segments - 1
            pygame.draw.rect(self.screen, bone_color,
                             (center_x - 1, segment_y, 2, segment_height))

        # Ribcage (simplified, just two pairs)
        rib_y1 = spine_top + (spine_bottom - spine_top) // 3
        rib_y2 = spine_top + (spine_bottom - spine_top) * 2 // 3
        rib_width = TILE_SIZE // 3

        # Upper ribs
        pygame.draw.arc(self.screen, bone_color,
                        (center_x - rib_width // 2, rib_y1, rib_width, 5),
                        math.radians(180), math.radians(360), 1)

        # Lower ribs
        pygame.draw.arc(self.screen, bone_color,
                        (center_x - rib_width // 2, rib_y2, rib_width, 5),
                        math.radians(180), math.radians(360), 1)

        # Pelvis (simple curved line)
        pelvis_y = spine_bottom + 4
        pygame.draw.arc(self.screen, bone_color,
                        (center_x - TILE_SIZE // 4, pelvis_y, TILE_SIZE // 2, 5),
                        math.radians(0), math.radians(180), 2)

        # Arms (simplified for small space)
        # Left arm
        arm_angle = math.sin(anim_time / 600) * 0.2
        shoulder_y = rib_y1

        # Calculate arm joint positions with subtle animation
        left_shoulder_x = center_x - TILE_SIZE // 6
        left_elbow_x = left_shoulder_x - TILE_SIZE // 8
        left_elbow_y = shoulder_y + TILE_SIZE // 6

        # Draw upper and lower arm
        pygame.draw.line(self.screen, bone_color,
                         (left_shoulder_x, shoulder_y),
                         (left_elbow_x, left_elbow_y), 2)
        pygame.draw.line(self.screen, bone_color,
                         (left_elbow_x, left_elbow_y),
                         (left_elbow_x - TILE_SIZE // 10, left_elbow_y + TILE_SIZE // 7), 1)

        # Right arm
        right_shoulder_x = center_x + TILE_SIZE // 6
        right_elbow_x = right_shoulder_x + TILE_SIZE // 8
        right_elbow_y = shoulder_y + TILE_SIZE // 6

        pygame.draw.line(self.screen, bone_color,
                         (right_shoulder_x, shoulder_y),
                         (right_elbow_x, right_elbow_y), 2)
        pygame.draw.line(self.screen, bone_color,
                         (right_elbow_x, right_elbow_y),
                         (right_elbow_x + TILE_SIZE // 10, right_elbow_y + TILE_SIZE // 7), 1)

        # Legs (simplified for small space)
        hip_y = pelvis_y
        left_hip_x = center_x - TILE_SIZE // 8
        right_hip_x = center_x + TILE_SIZE // 8

        # Left leg
        left_knee_y = hip_y + TILE_SIZE // 6
        left_foot_y = hip_y + TILE_SIZE // 3
        pygame.draw.line(self.screen, bone_color,
                         (left_hip_x, hip_y),
                         (left_hip_x - 2, left_knee_y), 2)
        pygame.draw.line(self.screen, bone_color,
                         (left_hip_x - 2, left_knee_y),
                         (left_hip_x - 4, left_foot_y), 1)

        # Right leg
        right_knee_y = hip_y + TILE_SIZE // 6
        right_foot_y = hip_y + TILE_SIZE // 3
        pygame.draw.line(self.screen, bone_color,
                         (right_hip_x, hip_y),
                         (right_hip_x + 2, right_knee_y), 2)
        pygame.draw.line(self.screen, bone_color,
                         (right_hip_x + 2, right_knee_y),
                         (right_hip_x + 4, right_foot_y), 1)

        # Add subtle ethereal effect (one small particle)
        if random.random() < 0.3:
            glow_x = center_x + random.randint(-TILE_SIZE // 4, TILE_SIZE // 4)
            glow_y = center_y + random.randint(-TILE_SIZE // 4, TILE_SIZE // 4)
            glow_size = random.randint(1, 2)
            glow_color = (150, 150, 255, 100)

            # Only draw if pygame supports per-pixel alpha
            try:
                glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surf, glow_color, (glow_size, glow_size), glow_size)
                self.screen.blit(glow_surf, (glow_x - glow_size, glow_y - glow_size))
            except:
                # Fallback if SRCALPHA not supported
                pygame.draw.circle(self.screen, glow_color[:3], (glow_x, glow_y), glow_size)

    # -------------------- 史莱姆绘制 ---------------------
    def draw_slim(self, monster):
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE
        w = monster.size[0] * TILE_SIZE
        h = monster.size[1] * TILE_SIZE

        # Animation parameters
        anim_time = pygame.time.get_ticks()
        bounce_offset = int(2 * math.sin(anim_time / 300))  # Bouncing motion
        squish_factor = 0.15 * math.sin(anim_time / 200)  # Body squishing effect

        # Center of the slime for rounded shape
        center_x = x + w // 2
        center_y = y + h // 2 + bounce_offset

        # Calculate radius with squish effect (taller/shorter)
        radius_x = int(w * 0.45 * (1.0 + squish_factor))
        radius_y = int(h * 0.45 * (1.0 - squish_factor * 0.8))

        # Get base color based on slime type
        if "红" in monster.name:
            base_color = (220, 20, 60)  # 红色史莱姆
            highlight_color = (255, 99, 71)
            bubble_color = (255, 150, 150)
        elif "黑" in monster.name:
            base_color = (35, 35, 35)  # 黑色史莱姆
            highlight_color = (105, 105, 105)
            bubble_color = (80, 80, 80)
        elif "闪光" in monster.name:
            # Flashy slime has faster color-shifting effect
            color_phase = (anim_time % 800) / 800  # Increased frequency (1500 → 800ms)
            if color_phase < 0.33:
                base_color = (50, 205, 50)  # Green
                highlight_color = (144, 238, 144)
                bubble_color = (200, 255, 200)
            elif color_phase < 0.66:
                base_color = (220, 20, 60)  # Red
                highlight_color = (255, 99, 71)
                bubble_color = (255, 200, 200)
            else:
                base_color = (35, 35, 35)  # Black
                highlight_color = (105, 105, 105)
                bubble_color = (150, 150, 150)
        else:  # 普通史莱姆
            base_color = (50, 205, 50)
            highlight_color = (144, 238, 144)
            bubble_color = (200, 255, 200)

        # Draw slime body - perfectly round with squish
        slime_rect = pygame.Rect(
            center_x - radius_x,
            center_y - radius_y,
            radius_x * 2,
            radius_y * 2
        )

        # Shadow beneath (slightly offset and darker)
        shadow_rect = pygame.Rect(
            center_x - radius_x + 2,
            center_y - radius_y + radius_y * 1.5,
            radius_x * 2,
            radius_y * 0.5
        )
        shadow_color = (max(0, base_color[0] - 40), max(0, base_color[1] - 40), max(0, base_color[2] - 40))
        pygame.draw.ellipse(self.screen, shadow_color, shadow_rect)

        # Main slime body - perfect ellipse
        pygame.draw.ellipse(self.screen, base_color, slime_rect)

        # Bottom edge for depth (darker area at bottom of slime)
        bottom_height = radius_y * 0.3
        bottom_rect = pygame.Rect(
            center_x - radius_x * 0.85,
            center_y + radius_y - bottom_height,
            radius_x * 1.7,
            bottom_height
        )

        # Calculate darker bottom color
        darker_color = (max(0, base_color[0] - 30), max(0, base_color[1] - 30), max(0, base_color[2] - 30))
        pygame.draw.ellipse(self.screen, darker_color, bottom_rect)

        # Top highlight (shiny spot) - smaller ellipse near top
        highlight_width = radius_x * 1.3
        highlight_height = radius_y * 0.6
        highlight_rect = pygame.Rect(
            center_x - highlight_width // 2,
            center_y - radius_y + radius_y * 0.25,
            highlight_width,
            highlight_height
        )
        pygame.draw.ellipse(self.screen, highlight_color, highlight_rect)

        # Secondary smaller highlight (extra shine)
        small_highlight = pygame.Rect(
            center_x - radius_x * 0.2,
            center_y - radius_y * 0.6,
            radius_x * 0.4,
            radius_y * 0.3
        )
        pygame.draw.ellipse(self.screen, (255, 255, 255, 180), small_highlight)

        # Draw internal features based on slime type
        if "黑" in monster.name:
            # Metallic sheen for black slime - curved reflections
            pygame.draw.arc(self.screen, (100, 100, 100),
                            (center_x - radius_x * 0.6, center_y - radius_y * 0.5,
                             radius_x * 1.2, radius_y * 1.0),
                            math.radians(220), math.radians(320), 2)
        elif "红" in monster.name:
            # Fire-like core for red slime
            core_width = radius_x
            core_height = radius_y * 1.2
            pygame.draw.ellipse(self.screen, (255, 165, 0, 180),
                                (center_x - core_width // 2, center_y - core_height // 2,
                                 core_width, core_height))

        # Add bubbles and inner details (except for black slime)
        if "黑" not in monster.name:
            # Dynamic bubble positions inside the rounded shape
            for i in range(3):
                # Calculate position with angle to keep bubbles inside ellipse
                angle = math.radians(i * 120 + anim_time / 10)
                distance = radius_x * 0.5 * random.uniform(0.5, 0.8)
                bx = center_x + math.cos(angle) * distance
                by = center_y + math.sin(angle) * distance * (radius_y / radius_x)  # Adjust for ellipse

                # Bubble size varies
                bubble_size = 1 + i % 3

                # Draw bubble
                pygame.draw.circle(self.screen, bubble_color, (int(bx), int(by)), bubble_size)
                # Small highlight in bubble
                pygame.draw.circle(self.screen, (255, 255, 255),
                                   (int(bx - bubble_size * 0.3), int(by - bubble_size * 0.3)),
                                   max(1, bubble_size // 2))

        # Special effects for Flash Slime
        if "闪光" in monster.name:
            # Enhanced glow effect around the slime
            glow_radius_x = radius_x * 1.3
            glow_radius_y = radius_y * 1.3

            try:
                # Create a soft glow using a semi-transparent surface
                glow_surf = pygame.Surface((glow_radius_x * 2, glow_radius_y * 2), pygame.SRCALPHA)

                # Pulsating glow intensity based on time
                glow_intensity = 40 + int(20 * math.sin(anim_time / 100))  # Faster pulsing

                # Draw multiple layers of glow with different opacity
                for i in range(3):
                    scale = 1.0 - i * 0.2
                    alpha = glow_intensity - i * 10
                    # Use the current slime color for the glow
                    glow_color = (base_color[0], base_color[1], base_color[2], alpha)

                    pygame.draw.ellipse(glow_surf, glow_color,
                                        (glow_radius_x * (1 - scale),
                                         glow_radius_y * (1 - scale),
                                         glow_radius_x * 2 * scale,
                                         glow_radius_y * 2 * scale))

                # Draw the glow behind the slime
                self.screen.blit(glow_surf,
                                 (center_x - glow_radius_x,
                                  center_y - glow_radius_y))
            except:
                # Fallback if SRCALPHA not supported
                pass

            # Add more sparkle effects (increased from 3 to 5)
            for _ in range(5):
                # Random angle and distance within slime
                angle = random.uniform(0, math.pi * 2)
                distance = random.uniform(0, radius_x * 0.8)
                spark_x = center_x + math.cos(angle) * distance
                spark_y = center_y + math.sin(angle) * distance * (radius_y / radius_x)

                # Draw sparkle (tiny star-like shape)
                pygame.draw.circle(self.screen, (255, 255, 200), (int(spark_x), int(spark_y)), 1)

                # Add more frequent larger flashes (increased probability from 0.2 to 0.4)
                if random.random() < 0.4:
                    pygame.draw.circle(self.screen, (255, 255, 200), (int(spark_x), int(spark_y)), 2)

            # Add occasional bright flashing star (new feature)
            if random.random() < 0.15:  # 15% chance per frame
                flash_x = center_x + random.uniform(-radius_x * 0.7, radius_x * 0.7)
                flash_y = center_y + random.uniform(-radius_y * 0.7, radius_y * 0.7)

                # Draw a 4-point star
                star_size = random.randint(3, 5)
                pygame.draw.line(self.screen, (255, 255, 255),
                                 (flash_x - star_size, flash_y),
                                 (flash_x + star_size, flash_y), 1)
                pygame.draw.line(self.screen, (255, 255, 255),
                                 (flash_x, flash_y - star_size),
                                 (flash_x, flash_y + star_size), 1)

        # Draw face (all slimes have faces)
        # Eyes position - in upper part of slime
        eye_y_pos = center_y - radius_y * 0.2
        eye_x_spacing = radius_x * 0.4
        eye_size = max(2, radius_x // 10)

        # Draw eyes
        left_eye_x = center_x - eye_x_spacing
        right_eye_x = center_x + eye_x_spacing

        # Left eye
        pygame.draw.circle(self.screen, (0, 0, 0), (int(left_eye_x), int(eye_y_pos)), eye_size)
        # Right eye
        pygame.draw.circle(self.screen, (0, 0, 0), (int(right_eye_x), int(eye_y_pos)), eye_size)

        # Eye highlights (small white dots)
        pygame.draw.circle(self.screen, (255, 255, 255),
                           (int(left_eye_x - eye_size * 0.3), int(eye_y_pos - eye_size * 0.3)),
                           max(1, eye_size // 2))
        pygame.draw.circle(self.screen, (255, 255, 255),
                           (int(right_eye_x - eye_size * 0.3), int(eye_y_pos - eye_size * 0.3)),
                           max(1, eye_size // 2))

        # Mouth - simple curve below eyes
        mouth_y = eye_y_pos + radius_y * 0.25
        mouth_width = radius_x * 0.8
        mouth_height = radius_y * 0.3

        # Happy curved mouth
        pygame.draw.arc(self.screen, (0, 0, 0),
                        (center_x - mouth_width // 2, mouth_y,
                         mouth_width, mouth_height),
                        math.pi * 0.2, math.pi * 0.8, 2)

        # Add occasional drip effect (10% chance per frame)
        if random.random() < 0.03:
            drip_x = center_x + random.uniform(-radius_x * 0.6, radius_x * 0.6)
            drip_top = center_y + radius_y * 0.8
            drip_length = random.randint(3, 6)

            # Draw drip
            pygame.draw.line(self.screen, base_color,
                             (drip_x, drip_top),
                             (drip_x, drip_top + drip_length), 2)

            # Drip droplet at end
            pygame.draw.circle(self.screen, base_color,
                               (int(drip_x), int(drip_top + drip_length)), 2)

    # -------------------- 电击球绘制 ---------------------

    def draw_lightning_ball(self, monster):
        # Base position and animation time
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE
        anim_time = pygame.time.get_ticks()
        center_x = x + TILE_SIZE // 2
        center_y = y + TILE_SIZE // 2

        # Colors based on monster type
        if "异色" in monster.name:
            core_color = (0, 210, 255)  # Cyan-blue core
            outer_color = (0, 150, 200)  # Darker cyan-blue outer
            arc_color = (120, 230, 255)  # Bright cyan electric arcs
        else:
            core_color = (255, 255, 0)  # Yellow core
            outer_color = (240, 180, 0)  # Darker yellow outer
            arc_color = (255, 255, 200)  # Electric arcs

        # Pulsing radius
        base_radius = TILE_SIZE // 3
        pulse = 0.15 * math.sin(anim_time / 150)
        radius = base_radius * (1 + pulse)

        # Draw outer glow
        glow_radius = int(radius * 1.5)
        pygame.draw.circle(self.screen, outer_color, (center_x, center_y), glow_radius, 1)

        # Draw core layers
        pygame.draw.circle(self.screen, outer_color, (center_x, center_y), int(radius * 1.2))
        pygame.draw.circle(self.screen, core_color, (center_x, center_y), int(radius * 0.8))

        # Highlight effect
        highlight_radius = int(radius * 0.4)
        pygame.draw.circle(self.screen, arc_color,
                           (center_x - highlight_radius // 2, center_y - highlight_radius // 2),
                           highlight_radius)

        # Electric arcs
        num_arcs = 5 + int(2 * math.sin(anim_time / 400))
        for i in range(num_arcs):
            # Calculate starting point on ball surface
            angle = math.radians(i * (360 / num_arcs) + anim_time / 20)
            start_x = center_x + math.cos(angle) * radius
            start_y = center_y + math.sin(angle) * radius

            # Calculate end point with some randomness
            length = radius * (1.0 + 0.3 * math.sin(anim_time / 250))
            end_angle = angle + math.radians(random.uniform(-20, 20))
            end_x = start_x + math.cos(end_angle) * length
            end_y = start_y + math.sin(end_angle) * length

            # Draw the main arc
            pygame.draw.line(self.screen, arc_color, (start_x, start_y), (end_x, end_y), 2)

            # Add a simple branch (50% chance)
            if random.random() < 0.5:
                branch_angle = end_angle + math.radians(random.uniform(-90, 90))
                branch_length = length * 0.6
                branch_x = end_x + math.cos(branch_angle) * branch_length * 0.5
                branch_y = end_y + math.sin(branch_angle) * branch_length * 0.5

                pygame.draw.line(self.screen, arc_color, (end_x, end_y), (branch_x, branch_y), 1)

        # Add a few random electric particles
        for _ in range(5):
            particle_angle = random.uniform(0, math.pi * 2)
            particle_dist = random.uniform(radius * 0.9, radius * 1.7)
            particle_x = center_x + math.cos(particle_angle) * particle_dist
            particle_y = center_y + math.sin(particle_angle) * particle_dist

            pygame.draw.circle(self.screen, arc_color,
                               (int(particle_x), int(particle_y)),
                               random.randint(1, 2))

        # Special circular field effect for "异色" variant (occasional)
        if "异色" in monster.name and random.random() < 0.4:
            field_radius = radius * 2.0
            # Draw a simple circular arc
            start_angle = math.radians((anim_time // 50) % 360)
            end_angle = start_angle + math.radians(random.randint(30, 180))
            pygame.draw.arc(self.screen, arc_color,
                            (center_x - field_radius, center_y - field_radius,
                             field_radius * 2, field_radius * 2),
                            start_angle, end_angle, 1)

    # -------------------- 魔法师绘制 ---------------------
    def draw_magician_evil(self, monster):
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE
        anim_time = pygame.time.get_ticks()
        center_x = x + TILE_SIZE // 2
        center_y = y + TILE_SIZE // 2

        # 动态波动效果参数
        pulse = 0.1 * math.sin(anim_time / 200)
        eye_glow = abs(math.sin(anim_time / 300))

        # 绘制优雅长袍底部 (更流线型设计)
        robe_color = (80, 0, 80)  # 深紫色主色
        robe_highlight = (120, 0, 120)  # 高光色
        pygame.draw.ellipse(self.screen, robe_color,
                            (x + 5, y + TILE_SIZE // 2, TILE_SIZE - 10, TILE_SIZE * (1 + pulse)))

        # 神秘魔法纹饰 (更立体的弧线)
        for i in range(3):
            arc_rect = (x + i * 5, y + TILE_SIZE // 2 + i * 3, TILE_SIZE - 10, TILE_SIZE - 10)
            pygame.draw.arc(self.screen, robe_highlight, arc_rect,
                            math.radians(0), math.radians(180), 2)

        # 神秘兜帽 (更深邃的阴影)
        hood_rect = (x + TILE_SIZE // 4, y, TILE_SIZE // 2, TILE_SIZE // 2)
        pygame.draw.arc(self.screen, (30, 30, 30), hood_rect,
                        math.radians(180), math.radians(360), 10)

        # 发光双眼 (带动态闪烁效果)
        eye_color = (0, int(200 * eye_glow), int(200 * eye_glow))
        eye_size = 4 + int(pulse * 10)
        left_eye_pos = (center_x - 8, y + TILE_SIZE // 3)
        right_eye_pos = (center_x + 8, y + TILE_SIZE // 3)
        pygame.draw.circle(self.screen, eye_color, left_eye_pos, eye_size)
        pygame.draw.circle(self.screen, eye_color, right_eye_pos, eye_size)

        # 魔法水晶法杖 (更精致的设计)
        staff_x = center_x + int(3 * math.sin(anim_time / 400))  # 微微摇晃的法杖
        staff_y = y + TILE_SIZE // 4
        # 法杖主体
        pygame.draw.line(self.screen, (150, 150, 150),
                         (staff_x - 15, staff_y - 5), (staff_x + 15, staff_y + 5), 5)
        # 法杖装饰纹路
        pygame.draw.line(self.screen, (180, 180, 180),
                         (staff_x - 10, staff_y - 3), (staff_x + 10, staff_y + 3), 2)

        # 闪耀水晶 (更动态的形状)
        crystal_color = (0, 200, 200)
        crystal_points = [
            (staff_x + 15, staff_y + 5),
            (staff_x + 25 + int(2 * math.sin(anim_time / 200)), staff_y),
            (staff_x + 15, staff_y - 5)
        ]
        pygame.draw.polygon(self.screen, crystal_color, crystal_points)

        # 水晶辉光 (更自然的光晕)
        crystal_center = (staff_x + 20, staff_y)
        for _ in range(3):
            glow_radius = 4 + random.randint(0, 2)
            offset_x = random.randint(-3, 3)
            offset_y = random.randint(-3, 3)
            pygame.draw.circle(self.screen, (0, 220, 220, 150),
                               (crystal_center[0] + offset_x, crystal_center[1] + offset_y), glow_radius)

        # 毒雾环绕 (更流畅的粒子效果)
        for i in range(6):  # 减少粒子数量但增加质量
            angle = math.radians(anim_time / 10 + i * 60)
            radius = 20 + 5 * math.sin(anim_time / 200 + i)
            px = center_x + radius * math.cos(angle)
            py = center_y + radius * math.sin(angle)
            # 绘制渐变毒雾粒子
            size = 3 + int(math.sin(anim_time / 300 + i) * 2)
            pygame.draw.circle(self.screen, (50, 200, 50, 100), (int(px), int(py)), size)
            # 添加内部高光
            pygame.draw.circle(self.screen, (150, 255, 150, 80),
                               (int(px - 1), int(py - 1)), size // 2)

    # -------------------- 魔王绘制 ---------------------

    def draw_monster_knight_boss(self, monster):
        # 基本颜色设置与类型判断
        body_color = (30, 30, 30)  # 黑铁色基底
        trim_color = (80, 80, 80)  # 盔甲镶边
        is_holy = "圣洁" in monster.name
        if is_holy:
            body_color = self.color_reverse(body_color)  # 圣洁版本用反色
            trim_color = self.color_reverse(trim_color)

        # 动画与位置参数
        anim_time = pygame.time.get_ticks()
        x, y = monster.x * TILE_SIZE, monster.y * TILE_SIZE
        center_x, center_y = x + TILE_SIZE // 2, y + TILE_SIZE // 2  # 中心点，根据TILE_SIZE=35调整

        # 动态特效参数（更增强的动态效果）
        hammer_swing = math.sin(anim_time / 300) * 0.5  # 锤子摆动弧度
        shield_glow = 0.5 + 0.5 * abs(math.sin(anim_time / 500))  # 盾牌发光强度
        eye_glow = 100 + int(155 * abs(math.sin(anim_time / 200)))  # 眼部红光波动
        armor_pulse = 1 + 0.08 * math.sin(anim_time / 400)  # 装甲脉动效果增强

        # ==== 躯干与基础护甲 ====
        # 更加雄壮的躯干（更具威严和霸气）
        torso_width = int(TILE_SIZE * 0.55)  # ~19像素宽度，进一步增宽
        torso_height = int(TILE_SIZE * 0.73)  # ~26像素高度，显著增加高度
        torso_tilt = int(2 * math.sin(anim_time / 800))  # 轻微倾斜效果

        # 绘制躯干（带动态呼吸效果）- 位置上移以适应增加的高度
        torso_rect = pygame.Rect(
            center_x - torso_width // 2 + torso_tilt,
            center_y - torso_height // 2 - 2,  # 上移2像素让整体更高
            torso_width,
            int(torso_height * armor_pulse)  # 高度随呼吸变化
        )
        pygame.draw.rect(self.screen, body_color, torso_rect)

        # 装甲接缝与纹路（更加精细的细节）
        for i in range(3):
            y_pos = torso_rect.top + 5 + i * (torso_rect.height // 3)
            pygame.draw.line(self.screen, trim_color,
                             (torso_rect.left - 1, y_pos),
                             (torso_rect.right + 1, y_pos), 1)

        # ==== 头部系统 ====
        # 更为宏伟的头盔尺寸
        helmet_width = int(TILE_SIZE * 0.5)  # ~18像素宽度，接近躯干宽度
        helmet_height = int(TILE_SIZE * 0.32)  # ~11像素高度，明显增高

        # 头盔位置（微微晃动增加生命感）- 进一步上移，增加整体高度
        helmet_x = center_x - helmet_width // 2 + int(math.sin(anim_time / 600) * 2)
        helmet_y = torso_rect.top - helmet_height - 3  # 上移1像素，增加身高

        # 带角巨盔（更长、更锋利的角设计，增强威慑力）
        horn_length = int(TILE_SIZE * 0.38)  # ~13像素角长度，更长的角
        horn_angle_left = math.radians(130 + math.sin(anim_time / 700) * 5)  # 左角动态角度（更水平）
        horn_angle_right = math.radians(50 - math.sin(anim_time / 700) * 5)  # 右角动态角度（更水平）

        helmet_points = [
            (helmet_x, helmet_y + helmet_height),  # 左下
            (helmet_x, helmet_y),  # 左上
            (helmet_x + horn_length * math.cos(horn_angle_left), helmet_y + horn_length * math.sin(horn_angle_left)),
            # 左角尖
            (helmet_x + helmet_width + horn_length * math.cos(horn_angle_right),
             helmet_y + horn_length * math.sin(horn_angle_right)),  # 右角尖
            (helmet_x + helmet_width, helmet_y),  # 右上
            (helmet_x + helmet_width, helmet_y + helmet_height)  # 右下
        ]
        pygame.draw.polygon(self.screen, (50, 50, 50), helmet_points)  # 绘制头盔主体

        # 面甲与发光双眼（邪恶的注视）
        visor_width = int(helmet_width * 0.8)
        visor_height = int(helmet_height * 0.7)
        visor_x = helmet_x + (helmet_width - visor_width) // 2
        visor_y = helmet_y + helmet_height - 1

        # 面甲开口
        pygame.draw.arc(self.screen, (100, 100, 100),
                        (visor_x, visor_y, visor_width, visor_height),
                        math.radians(220), math.radians(320), 2)

        # 发光红眼（更加明亮，带脉动效果）
        eye_size = 2 + int(math.sin(anim_time / 200) * 1.5)  # 动态眼睛大小
        eye_color = (eye_glow, 0, 0) if not is_holy else (0, 0, eye_glow)  # 根据类型变化眼色
        pygame.draw.circle(self.screen, eye_color,
                           (center_x - 5, visor_y + visor_height // 2), eye_size)
        pygame.draw.circle(self.screen, eye_color,
                           (center_x + 5, visor_y + visor_height // 2), eye_size)

        # ==== 肩甲系统 ====
        pauldron_size = int(TILE_SIZE * 0.45)  # ~16像素，极为宽大的肩甲
        left_pauldron_x = torso_rect.left - pauldron_size // 2 - 2  # 左移2像素，扩展整体宽度
        left_pauldron_y = torso_rect.top - 1  # 上移1像素，扩展肩甲高度

        # 左肩甲形状改为更宽大的六边形，增强视觉体积感
        left_pauldron_points = [
            (left_pauldron_x + pauldron_size // 3, left_pauldron_y - 3),  # 上点上移
            (left_pauldron_x - 2, left_pauldron_y + pauldron_size // 3),  # 左点左移
            (left_pauldron_x, left_pauldron_y + pauldron_size),  # 左下
            (left_pauldron_x + pauldron_size // 2, left_pauldron_y + pauldron_size + 3),  # 下点下移
            (left_pauldron_x + pauldron_size, left_pauldron_y + pauldron_size),  # 右下
            (left_pauldron_x + pauldron_size + 2, left_pauldron_y + pauldron_size // 3),  # 右点右移
        ]
        pygame.draw.polygon(self.screen, body_color, left_pauldron_points)

        # 肩甲装饰尖刺
        spike_length = int(TILE_SIZE * 0.2)  # ~7像素
        spike_angle = math.radians(225 + math.sin(anim_time / 500) * 10)
        spike_end = (
            left_pauldron_x + spike_length * math.cos(spike_angle),
            left_pauldron_y + pauldron_size // 2 + spike_length * math.sin(spike_angle)
        )
        pygame.draw.line(self.screen, trim_color,
                         (left_pauldron_x, left_pauldron_y + pauldron_size // 2),
                         spike_end, 2)

        # 右肩甲（魔纹浮雕）- 超大化处理
        right_pauldron_x = torso_rect.right - pauldron_size // 2 + 2  # 右移2像素，进一步扩展宽度
        right_pauldron_y = torso_rect.top - 1  # 上移1像素，与左肩同高
        # 使用梯形而非矩形，增加立体感和威严
        right_pauldron_points = [
            (right_pauldron_x, right_pauldron_y - 3),  # 左上角上移
            (right_pauldron_x + pauldron_size + 2, right_pauldron_y),  # 右上角右移
            (right_pauldron_x + pauldron_size, right_pauldron_y + pauldron_size + 3),  # 右下角下移
            (right_pauldron_x - 2, right_pauldron_y + pauldron_size),  # 左下角左移
        ]
        pygame.draw.polygon(self.screen, body_color, right_pauldron_points)

        # 魔纹浮雕（闪烁的符文）
        if anim_time % 1000 < 800:  # 间歇性闪烁
            rune_color = (200, 0, 0) if not is_holy else (0, 150, 255)
            rune_size = int(TILE_SIZE * 0.1)  # ~3-4像素

            # V字形符文
            pygame.draw.line(self.screen, rune_color,
                             (right_pauldron_x + pauldron_size // 2 - rune_size, right_pauldron_y + rune_size),
                             (right_pauldron_x + pauldron_size // 2, right_pauldron_y + pauldron_size - rune_size), 2)
            pygame.draw.line(self.screen, rune_color,
                             (right_pauldron_x + pauldron_size // 2 + rune_size, right_pauldron_y + rune_size),
                             (right_pauldron_x + pauldron_size // 2, right_pauldron_y + pauldron_size - rune_size), 2)

        # ==== 中央符文 ====
        # 更大更明显的脉动符文
        rune_scale = 1 + 0.3 * math.sin(anim_time / 250)  # 符文脉动效果
        rune_size = int(TILE_SIZE * 0.13 * rune_scale)  # ~5-6像素，更大的符文核心
        rune_color = (200, 0, 0) if not is_holy else (0, 150, 255)

        # 菱形符文
        rune_points = [
            (center_x, center_y - rune_size),  # 上
            (center_x + rune_size, center_y),  # 右
            (center_x, center_y + rune_size),  # 下
            (center_x - rune_size, center_y)  # 左
        ]
        pygame.draw.polygon(self.screen, rune_color, rune_points)

        # 符文光晕效果
        if anim_time % 800 < 400:  # 间歇性光晕
            glow_size = rune_size + 2
            glow_alpha = int(100 * math.sin(anim_time / 200))
            glow_color = (*rune_color[:2], 0, glow_alpha)  # 提取RGB，添加Alpha

            try:  # 尝试绘制带透明度的光晕
                glow_surf = pygame.Surface((glow_size * 2, glow_size * 2), pygame.SRCALPHA)
                pygame.draw.polygon(glow_surf, glow_color, [
                    (glow_size, 0),
                    (glow_size * 2, glow_size),
                    (glow_size, glow_size * 2),
                    (0, glow_size)
                ])
                self.screen.blit(glow_surf, (center_x - glow_size, center_y - glow_size))
            except:
                pass  # 如果不支持透明度，则跳过光晕效果

        # ==== 下半身烟雾系统（虚化灵魂效果）====
        mist_height = int(TILE_SIZE * 0.7)  # 烟雾高度
        mist_base_y = torso_rect.bottom - 3  # 烟雾起始位置（略微与躯干重叠）
        mist_max_width = torso_width * 1.4  # 烟雾最大宽度（略大于躯干）

        # 绘制多层烟雾，从密到稀
        for i in range(5):
            # 烟雾渐变尺寸和透明度 - 降低透明度使烟雾更明显
            layer_ratio = (5 - i) / 5  # 从底部向上渐变（1.0到0.2）
            mist_width = int(mist_max_width * (0.5 + layer_ratio * 0.5))  # 下宽上窄
            mist_alpha = int(170 * layer_ratio)  # 透明度提高到170，更清晰可见

            # 烟雾漂浮动态效果 - 减缓移动速度
            drift_x = int(math.sin(anim_time / 800 + i) * 2)  # 横向漂移减慢(500->800)，幅度减小(3->2)
            layer_y = mist_base_y + int(mist_height * i / 5)  # 每层位置
            wave_effect = int(math.sin(anim_time / 500 + i * 0.7) * 2)  # 波动效果减缓(300->500)，幅度减小(3->2)

            # 烟雾颜色 - 根据类型使用不同颜色，增强颜色饱和度
            if is_holy:
                mist_color = (170, 170, 240, mist_alpha)  # 更亮的蓝紫色烟雾（圣洁版）
            else:
                mist_color = (70, 70, 70, mist_alpha)  # 更亮的暗黑烟雾（普通版）

            try:
                # 创建烟雾层
                mist_surf = pygame.Surface((mist_width, int(mist_height / 5)), pygame.SRCALPHA)
                pygame.draw.ellipse(mist_surf, mist_color, (0, 0, mist_width, int(mist_height / 5)))

                # 绘制带有波动效果的烟雾层
                self.screen.blit(mist_surf, (
                    center_x - mist_width // 2 + drift_x + wave_effect,
                    layer_y
                ))

                # 随机添加小烟雾粒子（增加动态感）
                if random.random() < 0.4:
                    particle_size = random.randint(3, 5)  # 增大粒子(2-4->3-5)使其更明显
                    particle_x = center_x + random.randint(-mist_width // 2, mist_width // 2)
                    particle_y = layer_y + random.randint(-3, 3)
                    particle_alpha = random.randint(150, 200)  # 提高透明度(30-100->150-200)更清晰

                    particle_surf = pygame.Surface((particle_size * 2, particle_size * 2), pygame.SRCALPHA)
                    if is_holy:
                        particle_color = (220, 220, 255, particle_alpha)  # 更亮的粒子颜色
                    else:
                        particle_color = (100, 100, 100, particle_alpha)  # 更亮的粒子颜色

                    pygame.draw.circle(particle_surf, particle_color,
                                       (particle_size, particle_size), particle_size)
                    self.screen.blit(particle_surf, (particle_x - particle_size, particle_y - particle_size))
            except:
                # 备用简单烟雾（不支持透明度时）
                simple_width = mist_width // 2
                simple_color = (150, 150, 220) if is_holy else (70, 70, 70)
                pygame.draw.ellipse(self.screen, simple_color,
                                    (center_x - simple_width // 2 + drift_x, layer_y,
                                     simple_width, mist_height // 10))

        # ==== 毁灭重锤 ====
        # 更巨大的毁灭重锤（体现力量与压迫感）
        hammer_length = int(TILE_SIZE * 0.85)  # ~30像素，更长的锤柄
        hammer_angle = math.radians(30 + hammer_swing * 15)
        hammer_base_x = torso_rect.right + 4
        hammer_base_y = torso_rect.bottom - 5

        hammer_head_x = hammer_base_x + math.cos(hammer_angle) * hammer_length
        hammer_head_y = hammer_base_y + math.sin(hammer_angle) * hammer_length

        # 锤柄（带纹理）- 更粗壮
        pygame.draw.line(self.screen, (50, 50, 50),
                         (hammer_base_x, hammer_base_y),
                         (hammer_head_x, hammer_head_y), 5)  # 增加线宽

        # 锤头（更具威慑力）- 更大
        hammer_head_size = int(TILE_SIZE * 0.33)  # ~12像素，更大的锤头
        pygame.draw.circle(self.screen, (60, 60, 60),
                           (int(hammer_head_x), int(hammer_head_y)), hammer_head_size)

        # 锤头尖刺（动态伸缩）
        for i, angle in enumerate([0, 90, 180, 270]):
            spike_phase = anim_time / 400 + i * math.pi / 2
            spike_length = int(TILE_SIZE * 0.3 * (0.8 + 0.2 * math.sin(spike_phase)))  # ~10像素，动态变化

            rad_angle = math.radians(angle)
            spike_end_x = hammer_head_x + math.cos(rad_angle) * spike_length
            spike_end_y = hammer_head_y + math.sin(rad_angle) * spike_length

            spike_color = (100, 100, 100) if not is_holy else (200, 200, 200)
            pygame.draw.line(self.screen, spike_color,
                             (int(hammer_head_x), int(hammer_head_y)),
                             (int(spike_end_x), int(spike_end_y)), 3)

        # 锤头裂纹与魔纹（更具魔性）
        if not is_holy:  # 只有普通魔王有裂纹
            crack_offset = int(math.sin(anim_time / 300) * 2)  # 裂纹抖动
            pygame.draw.line(self.screen, (30, 30, 30),
                             (hammer_head_x - hammer_head_size // 2 + crack_offset,
                              hammer_head_y - hammer_head_size // 2),
                             (hammer_head_x + hammer_head_size // 2,
                              hammer_head_y + hammer_head_size // 2 - crack_offset), 2)
        else:  # 圣洁魔王有魔法纹路
            glow_intensity = int(150 + 100 * abs(math.sin(anim_time / 300)))  # 保证值在150-250范围内
            pygame.draw.circle(self.screen, (200, 200, 255),
                               (int(hammer_head_x), int(hammer_head_y)), hammer_head_size // 2, 1)

        # ==== 魔能护盾 ====
        # 动态脉动的能量场 - 更大范围的能量场
        shield_radius = int(TILE_SIZE * 0.75 * shield_glow)  # ~26像素，随时间变化，更大范围
        try:
            shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
            shield_color = (0, 100, 200, 70) if is_holy else (200, 0, 0, 70)  # 根据类型改变颜色

            # 多层护盾效果
            for i in range(3):
                layer_alpha = 70 - i * 20
                layer_radius = shield_radius - i * 3
                pygame.draw.circle(shield_surface, (*shield_color[:3], layer_alpha),
                                   (shield_radius, shield_radius), layer_radius)

            self.screen.blit(shield_surface, (center_x - shield_radius, center_y - shield_radius))
        except:
            # 备用简单护盾（无透明度）
            shield_color_simple = (0, 100, 200) if is_holy else (200, 0, 0)
            pygame.draw.circle(self.screen, shield_color_simple,
                               (center_x, center_y), int(shield_radius * 0.7), 1)

        # ==== 环境影响效果 ====
        # 地面裂纹（显示力量压迫）- 调整到烟雾下方
        mist_bottom = mist_base_y + mist_height  # 获取烟雾底部位置
        crack_width = int(TILE_SIZE * 0.6 + TILE_SIZE * 0.1 * math.sin(anim_time / 600))  # 动态裂纹宽度
        pygame.draw.arc(self.screen, (60, 60, 60),
                        (center_x - crack_width // 2, mist_bottom - 5,
                         crack_width, TILE_SIZE * 0.25),
                        math.radians(180), math.radians(360), 3)

        # 环绕气息效果（邪能/圣光）
        if anim_time % 400 < 200:  # 间歇性气息释放
            fog_color = (30, 30, 30, 80) if not is_holy else (255, 255, 200, 50)
            for _ in range(2):  # 少量但高质量的粒子
                fog_distance = TILE_SIZE * (0.3 + 0.5 * random.random()) * shield_glow
                fog_angle = random.uniform(0, math.pi * 2)
                fog_x = center_x + math.cos(fog_angle) * fog_distance
                fog_y = center_y + math.sin(fog_angle) * fog_distance
                fog_size = int(TILE_SIZE * 0.1 * (0.8 + 0.4 * shield_glow))  # ~4-5像素

                try:
                    fog_surf = pygame.Surface((fog_size * 2, fog_size * 2), pygame.SRCALPHA)
                    pygame.draw.circle(fog_surf, fog_color, (fog_size, fog_size), fog_size)
                    self.screen.blit(fog_surf, (fog_x - fog_size, fog_y - fog_size))
                except:
                    # 备用实心粒子
                    simple_color = (30, 30, 30) if not is_holy else (200, 200, 150)
                    pygame.draw.circle(self.screen, simple_color, (int(fog_x), int(fog_y)), fog_size // 2)

    # -------------------- 普通巨龙绘制 ---------------------

    def draw_dragon_boss(self, monster):
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE
        # 动画和基础参数
        anim_time = pygame.time.get_ticks()
        wing_flap = math.sin(anim_time / 300) * 0.3  # 翅膀摆动弧度
        breath_phase = int((anim_time % 600) / 120)  # 五阶段火焰循环
        eye_glow = abs(math.sin(anim_time / 400))  # 眼睛发光强度
        body_pulse = 0.03 * math.sin(anim_time / 500)  # 身体微弱起伏效果
        neck_sway = math.sin(anim_time / 850) * 0.1  # 脖子摆动效果

        # 根据TILE_SIZE调整比例
        scale_factor = TILE_SIZE / 35  # 基于原始TILE_SIZE=35的比例调整

        # ---- 阴影效果 ----
        shadow_surf = pygame.Surface((TILE_SIZE * 3, TILE_SIZE * 0.8), pygame.SRCALPHA)
        shadow_ellipse = (TILE_SIZE * 0.5, 0, TILE_SIZE * 2, TILE_SIZE * 0.4)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 70), shadow_ellipse)  # 半透明阴影
        self.screen.blit(shadow_surf, (x, y + TILE_SIZE * 2.5))

        # ---- 身体主体 ----
        body_width = int(TILE_SIZE * 1.2 * (1 + body_pulse))
        body_height = int(TILE_SIZE * 0.8 * (1 + body_pulse))
        body_x = x + TILE_SIZE - body_width * 0.3
        body_y = y + TILE_SIZE * 1.5

        # ---- 尾部 ----
        tail_width = int(TILE_SIZE * 0.3)
        tail_base_x = body_x + body_width * 0.1
        tail_base_y = body_y + body_height * 0.5

        tail_points = [
            (tail_base_x, tail_base_y),  # 尾部根部连接到身体
            (tail_base_x - TILE_SIZE * 0.6, body_y + body_height + TILE_SIZE * 0.2),  # 尾部中段
            (tail_base_x - TILE_SIZE * 1.0, body_y + body_height + TILE_SIZE * 0.4),  # 尾部末端
            (tail_base_x - TILE_SIZE * 1.2, body_y + body_height + TILE_SIZE * 0.2)  # 尾部尖端
        ]

        # 尾部摆动效果
        tail_swing = math.sin(anim_time / 450) * (TILE_SIZE * 0.2)  # 摆动幅度
        for i in range(1, len(tail_points)):
            # 越往后的部分摆动幅度越大
            swing_amount = tail_swing * (i / len(tail_points))
            tail_points[i] = (tail_points[i][0] + swing_amount, tail_points[i][1])

        # 绘制尾部
        pygame.draw.polygon(self.screen, (110, 30, 30), tail_points)

        # 尾部棘刺 - 更多更明显的棘刺
        for i in range(3):
            # 计算棘刺位置 - 沿着尾部曲线分布
            if i < len(tail_points) - 1:
                spike_base_x = (tail_points[i][0] + tail_points[i + 1][0]) / 2
                spike_base_y = (tail_points[i][1] + tail_points[i + 1][1]) / 2

                # 棘刺指向 - 垂直于尾部方向
                dx = tail_points[i + 1][0] - tail_points[i][0]
                dy = tail_points[i + 1][1] - tail_points[i][1]
                length = max(1, math.sqrt(dx * dx + dy * dy))

                # 归一化并旋转90度
                nx, ny = -dy / length, dx / length

                # 棘刺尺寸随着尾部位置变化
                spike_length = TILE_SIZE * 0.2 * (1 - i / len(tail_points))

                spike_tip_x = spike_base_x + nx * spike_length
                spike_tip_y = spike_base_y + ny * spike_length

                pygame.draw.line(self.screen, (140, 50, 40),
                                 (spike_base_x, spike_base_y),
                                 (spike_tip_x, spike_tip_y),
                                 max(1, int(3 * scale_factor)))

        # ---- 绘制身体 ----
        # 身体主体
        pygame.draw.ellipse(self.screen, (130, 50, 50), (body_x, body_y, body_width, body_height))

        # 身体鳞片纹理 - 更明显的龙鳞
        for i in range(3):
            for j in range(4):
                scale_x = int(body_x + j * body_width * 0.25 + (i % 2) * (body_width * 0.125))
                scale_y = int(body_y + i * body_height * 0.33)

                # 鳞片形状 - 菱形或半圆
                if random.random() > 0.5:
                    # 菱形鳞片
                    scale_size = int(TILE_SIZE * 0.08)
                    scale_points = [
                        (scale_x, scale_y - scale_size),
                        (scale_x + scale_size, scale_y),
                        (scale_x, scale_y + scale_size),
                        (scale_x - scale_size, scale_y)
                    ]
                    scale_color = (
                        110 + random.randint(-15, 15),
                        40 + random.randint(-10, 10),
                        40 + random.randint(-10, 10)
                    )
                    pygame.draw.polygon(self.screen, scale_color, scale_points)
                    # 鳞片高光
                    pygame.draw.line(self.screen, (scale_color[0] + 30, scale_color[1] + 20, scale_color[2] + 20),
                                     scale_points[0], scale_points[1], 1)
                else:
                    # 半圆鳞片
                    scale_size = int(TILE_SIZE * 0.07)
                    scale_color = (
                        100 + random.randint(-10, 10),
                        35 + random.randint(-5, 5),
                        35 + random.randint(-5, 5)
                    )
                    pygame.draw.circle(self.screen, scale_color, (scale_x, scale_y), scale_size)
                    pygame.draw.line(self.screen, (scale_color[0] + 25, scale_color[1] + 15, scale_color[2] + 15),
                                     (scale_x - scale_size / 2, scale_y - scale_size / 2),
                                     (scale_x + scale_size / 2, scale_y - scale_size / 2), 1)

        # 背部脊刺 - 龙的典型特征
        spine_count = 4
        for i in range(spine_count):
            spine_base_x = body_x + body_width * (0.3 + 0.5 * i / spine_count)
            spine_base_y = body_y - body_height * 0.1

            # 脊刺高度随位置变化
            spine_height = TILE_SIZE * 0.3 * (1 - abs(i - spine_count / 2) / (spine_count / 2))

            spine_tip_x = spine_base_x
            spine_tip_y = spine_base_y - spine_height

            pygame.draw.line(self.screen, (140, 55, 45),
                             (spine_base_x, spine_base_y),
                             (spine_tip_x, spine_tip_y),
                             max(1, int(3 * scale_factor)))

        # ---- 翅膀系统 ----
        # 翅膀基点连接到身体
        wing_base_left = (body_x + body_width * 0.3, body_y + body_height * 0.2)
        wing_base_right = (body_x + body_width * 0.7, body_y + body_height * 0.2)

        # 翅膀形态参数 - 更大更有力的翅膀
        wing_length = TILE_SIZE * 1.2
        wing_width = TILE_SIZE * 0.7

        # 左翼 - 带动态翅膀弯曲
        left_wing_tip_x = wing_base_left[0] - wing_length * math.cos(wing_flap)
        left_wing_tip_y = wing_base_left[1] - wing_length * math.sin(wing_flap * 0.8)
        left_wing_mid_x = wing_base_left[0] - wing_length * 0.6 * math.cos(wing_flap + 0.2)
        left_wing_mid_y = wing_base_left[1] - wing_length * 0.4 * math.sin(wing_flap * 0.8 + 0.2)

        left_wing = [
            wing_base_left,
            (left_wing_mid_x, left_wing_mid_y),
            (left_wing_tip_x, left_wing_tip_y),
            (left_wing_mid_x - wing_width * 0.3, left_wing_mid_y + wing_width * 0.5),
            (wing_base_left[0] - wing_width * 0.2, wing_base_left[1] + wing_width * 0.3)
        ]

        # 右翼 - 带动态翅膀弯曲
        right_wing_tip_x = wing_base_right[0] + wing_length * math.cos(wing_flap)
        right_wing_tip_y = wing_base_right[1] - wing_length * math.sin(wing_flap * 0.8)
        right_wing_mid_x = wing_base_right[0] + wing_length * 0.6 * math.cos(wing_flap + 0.2)
        right_wing_mid_y = wing_base_right[1] - wing_length * 0.4 * math.sin(wing_flap * 0.8 + 0.2)

        right_wing = [
            wing_base_right,
            (right_wing_mid_x, right_wing_mid_y),
            (right_wing_tip_x, right_wing_tip_y),
            (right_wing_mid_x + wing_width * 0.3, right_wing_mid_y + wing_width * 0.5),
            (wing_base_right[0] + wing_width * 0.2, wing_base_right[1] + wing_width * 0.3)
        ]

        # 绘制翅膀
        for wing in [left_wing, right_wing]:
            # 翅膀与身体的连接部分
            connect_x = wing[0][0]
            connect_y = wing[0][1]
            connect_radius = TILE_SIZE * 0.12
            pygame.draw.circle(self.screen, (140, 50, 50), (int(connect_x), int(connect_y)), int(connect_radius))

            # 翅膀膜 - 半透明效果
            wing_color = (160, 60, 60)
            # 绘制主膜
            pygame.draw.polygon(self.screen, wing_color, wing)

            # 翅膀骨架 - 更多的翅骨
            for i in range(min(4, len(wing) - 1)):
                pygame.draw.line(self.screen, (100, 40, 40),
                                 wing[0], wing[i + 1],
                                 max(1, int(2 * scale_factor)))

            # 翅膀纹理 - 类似蝙蝠翅膀的膜纹理
            for i in range(3):
                fold_start_idx = random.randint(0, len(wing) - 2)
                fold_end_idx = random.randint(fold_start_idx + 1, len(wing) - 1)

                # 确保不是重复的线
                if fold_start_idx != fold_end_idx:
                    fold_color = (120, 40, 40, 180)
                    pygame.draw.line(self.screen, fold_color,
                                     wing[fold_start_idx], wing[fold_end_idx], 1)

        # ---- 脖子系统 - 突出显示长脖子，这是龙的典型特征 ----
        # 脖子基点连接到身体
        neck_base_x = body_x + body_width * 0.7
        neck_base_y = body_y + body_height * 0.3

        # 脖子终点（头部连接处）
        neck_end_x = body_x + body_width + TILE_SIZE * 0.5 + neck_sway * TILE_SIZE
        neck_end_y = body_y - TILE_SIZE * 0.2

        # 脖子弯曲控制点
        neck_ctrl1_x = neck_base_x + (neck_end_x - neck_base_x) * 0.3
        neck_ctrl1_y = neck_base_y - TILE_SIZE * 0.3

        neck_ctrl2_x = neck_base_x + (neck_end_x - neck_base_x) * 0.7
        neck_ctrl2_y = neck_end_y + TILE_SIZE * 0.2

        # 生成脖子曲线点
        neck_points = []
        neck_width = TILE_SIZE * 0.25  # 脖子宽度

        # 生成贝塞尔曲线描述脖子
        segments = 8
        for i in range(segments + 1):
            t = i / segments
            # 三次贝塞尔曲线公式
            px = (1 - t) ** 3 * neck_base_x + 3 * (1 - t) ** 2 * t * neck_ctrl1_x + 3 * (
                        1 - t) * t ** 2 * neck_ctrl2_x + t ** 3 * neck_end_x
            py = (1 - t) ** 3 * neck_base_y + 3 * (1 - t) ** 2 * t * neck_ctrl1_y + 3 * (
                        1 - t) * t ** 2 * neck_ctrl2_y + t ** 3 * neck_end_y
            neck_points.append((px, py))

        # 绘制脖子主体
        if len(neck_points) > 1:
            for i in range(len(neck_points) - 1):
                # 脖子宽度沿长度逐渐变窄
                segment_width = neck_width * (1 - 0.4 * i / segments)

                # 获取当前线段的方向
                dx = neck_points[i + 1][0] - neck_points[i][0]
                dy = neck_points[i + 1][1] - neck_points[i][1]
                # 线段长度
                segment_len = max(0.001, math.sqrt(dx * dx + dy * dy))
                # 单位方向向量
                dx, dy = dx / segment_len, dy / segment_len
                # 垂直方向向量
                nx, ny = -dy, dx

                # 计算脖子线段的四个角点
                neck_segment = [
                    (neck_points[i][0] + nx * segment_width / 2, neck_points[i][1] + ny * segment_width / 2),
                    (neck_points[i + 1][0] + nx * segment_width / 2, neck_points[i + 1][1] + ny * segment_width / 2),
                    (neck_points[i + 1][0] - nx * segment_width / 2, neck_points[i + 1][1] - ny * segment_width / 2),
                    (neck_points[i][0] - nx * segment_width / 2, neck_points[i][1] - ny * segment_width / 2)
                ]

                # 绘制脖子段
                pygame.draw.polygon(self.screen, (125, 45, 45), neck_segment)

                # 脖子关节鳞片 - 每隔一段绘制
                if i % 2 == 0:
                    mid_x = (neck_segment[0][0] + neck_segment[3][0]) / 2
                    mid_y = (neck_segment[0][1] + neck_segment[3][1]) / 2

                    scale_size = segment_width * 0.7
                    scale_color = (140, 55, 45)

                    pygame.draw.ellipse(self.screen, scale_color,
                                        (mid_x - scale_size / 2, mid_y - scale_size / 2, scale_size, scale_size))

        # ---- 头部系统 ----
        head_radius = int(TILE_SIZE * 0.32)
        # 头部位置：脖子末端
        head_center = (neck_end_x, neck_end_y)

        # 绘制头部 - 更加细长的龙头
        head_length = head_radius * 2.8
        head_height = head_radius * 1.6

        head_rect = (
            head_center[0] - head_radius * 0.5,  # 向后偏移
            head_center[1] - head_height / 2,
            head_length,
            head_height
        )
        pygame.draw.ellipse(self.screen, (135, 52, 52), head_rect)

        # 加强头部与脖子的连接
        neck_join_radius = head_radius * 0.8
        pygame.draw.circle(self.screen, (130, 50, 50),
                           (int(head_center[0]), int(head_center[1])),
                           int(neck_join_radius))

        # 眼睛 - 更有神的龙眼
        eye_radius = max(2, int(head_radius * 0.4))
        eye_center = (head_center[0] + head_radius * 0.4, head_center[1] - head_radius * 0.2)

        # 眼眶
        pygame.draw.circle(self.screen, (90, 30, 30), eye_center, eye_radius * 1.2)

        # 眼白
        pygame.draw.circle(self.screen, (240, 240, 220), eye_center, eye_radius)

        # 动态瞳孔 - 竖直的龙瞳
        pupil_offset_x = math.sin(anim_time / 1700) * (eye_radius * 0.3)
        pupil_offset_y = math.cos(anim_time / 1500) * (eye_radius * 0.2)
        pupil_center = (
            int(eye_center[0] + pupil_offset_x),
            int(eye_center[1] + pupil_offset_y)
        )

        # 龙眼瞳孔 - 细长的竖瞳
        pupil_color = (
            min(255, int(200 + 55 * eye_glow)),
            min(100, int(20 + 80 * eye_glow)),
            0
        )
        # 竖瞳
        pupil_height = eye_radius * 1.2
        pupil_width = eye_radius * 0.4

        # 旋转角度 - 随机晃动
        pupil_angle = math.sin(anim_time / 1000) * 15

        # 创建竖瞳椭圆
        pupil_surf = pygame.Surface((int(pupil_width), int(pupil_height)), pygame.SRCALPHA)
        pygame.draw.ellipse(pupil_surf, pupil_color, (0, 0, int(pupil_width), int(pupil_height)))

        # 旋转瞳孔
        rotated_pupil = pygame.transform.rotate(pupil_surf, pupil_angle)
        # 获取旋转后的矩形并居中
        pupil_rect = rotated_pupil.get_rect(center=pupil_center)
        # 绘制瞳孔
        self.screen.blit(rotated_pupil, pupil_rect)

        # 瞳孔高光
        highlight_pos = (pupil_center[0] - 1, pupil_center[1] - pupil_height / 4)
        highlight_size = max(1, eye_radius // 4)
        pygame.draw.circle(self.screen, (255, 255, 255, 200),
                           highlight_pos, highlight_size)

        # ---- 龙角和头部装饰 ----
        # 更突出的龙角 - 弯曲的角
        horn_base_left = (head_center[0] + head_radius * 0.7, head_center[1] - head_radius * 0.6)
        # 弯曲角 - 多段线
        horn_mid_left = (horn_base_left[0] + head_radius * 0.4, horn_base_left[1] - head_radius * 0.5)
        horn_tip_left = (horn_mid_left[0] + head_radius * 0.2, horn_mid_left[1] - head_radius * 0.7)

        # 左角
        horn_points_left = [horn_base_left, horn_mid_left, horn_tip_left]
        for i in range(len(horn_points_left) - 1):
            pygame.draw.line(self.screen, (90, 30, 30),
                             horn_points_left[i], horn_points_left[i + 1],
                             max(1, int(3 * scale_factor)))

        # 右角 - 对称
        horn_base_right = (head_center[0] + head_radius * 1.4, head_center[1] - head_radius * 0.5)
        horn_mid_right = (horn_base_right[0] + head_radius * 0.4, horn_base_right[1] - head_radius * 0.5)
        horn_tip_right = (horn_mid_right[0] + head_radius * 0.2, horn_mid_right[1] - head_radius * 0.7)

        # 右角
        horn_points_right = [horn_base_right, horn_mid_right, horn_tip_right]
        for i in range(len(horn_points_right) - 1):
            pygame.draw.line(self.screen, (90, 30, 30),
                             horn_points_right[i], horn_points_right[i + 1],
                             max(1, int(3 * scale_factor)))

        # ---- 口鼻部分 ----
        # 吻部 - 突出的龙吻
        snout_length = head_radius * 1.5
        snout_height = head_radius * 0.7
        snout_x = head_center[0] + head_radius * 0.8
        snout_y = head_center[1] - snout_height * 0.2

        # 绘制龙吻 - 狭长的吻部
        pygame.draw.ellipse(self.screen, (125, 45, 45),
                            (snout_x, snout_y, snout_length, snout_height))

        # 龙嘴线条 - 微张的嘴
        jaw_start_x = snout_x + snout_length * 0.2
        jaw_start_y = snout_y + snout_height * 0.7
        jaw_end_x = snout_x + snout_length * 0.8
        jaw_end_y = snout_y + snout_height * 0.8

        pygame.draw.line(self.screen, (90, 30, 30),
                         (jaw_start_x, jaw_start_y),
                         (jaw_end_x, jaw_end_y),
                         max(1, int(2 * scale_factor)))

        # 添加牙齿 - 龙的标志性特征
        teeth_count = 3
        teeth_height = snout_height * 0.15

        for i in range(teeth_count):
            tooth_x = jaw_start_x + i * (jaw_end_x - jaw_start_x) / (teeth_count - 1)
            # 上牙
            pygame.draw.polygon(self.screen, (240, 240, 240), [
                (tooth_x, jaw_start_y),
                (tooth_x - teeth_height / 2, jaw_start_y - teeth_height),
                (tooth_x + teeth_height / 2, jaw_start_y - teeth_height)
            ])

            # 下牙 - 错开放置
            lower_tooth_x = tooth_x + (jaw_end_x - jaw_start_x) / (teeth_count * 2)
            if lower_tooth_x < jaw_end_x:
                pygame.draw.polygon(self.screen, (240, 240, 240), [
                    (lower_tooth_x, jaw_start_y),
                    (lower_tooth_x - teeth_height / 2, jaw_start_y + teeth_height),
                    (lower_tooth_x + teeth_height / 2, jaw_start_y + teeth_height)
                ])

        # 鼻孔 - 椭圆形双鼻孔
        nostril_w = max(1, head_radius // 6)
        nostril_h = max(1, head_radius // 10)
        nostril_y = snout_y + snout_height * 0.3

        # 左鼻孔
        left_nostril_x = snout_x + snout_length * 0.7
        pygame.draw.ellipse(self.screen, (60, 20, 20),
                            (left_nostril_x, nostril_y, nostril_w, nostril_h))

        # 右鼻孔
        right_nostril_x = left_nostril_x + nostril_w * 1.5
        pygame.draw.ellipse(self.screen, (60, 20, 20),
                            (right_nostril_x, nostril_y, nostril_w, nostril_h))

        # ---- 火焰吐息特效 ----
        if breath_phase > 0:  # 有火焰吐息时
            mouth_pos = (jaw_end_x, jaw_end_y)

            # 火焰特效参数 - 更长更猛烈的火焰
            flame_length = TILE_SIZE * (0.6 + 0.3 * breath_phase)  # 随阶段增长
            flame_width = TILE_SIZE * (0.3 + 0.15 * breath_phase)

            # 创建主火焰多边形 - 更多角的不规则形状
            flame_points = [
                mouth_pos,
                (mouth_pos[0] + flame_length * 0.5, mouth_pos[1] - flame_width * 0.4),
                (mouth_pos[0] + flame_length * 0.7, mouth_pos[1] - flame_width * 0.2),
                (mouth_pos[0] + flame_length * 0.9, mouth_pos[1] - flame_width * 0.5),
                (mouth_pos[0] + flame_length * 1.2, mouth_pos[1]),  # 尖端
                (mouth_pos[0] + flame_length * 0.9, mouth_pos[1] + flame_width * 0.5),
                (mouth_pos[0] + flame_length * 0.7, mouth_pos[1] + flame_width * 0.2),
                (mouth_pos[0] + flame_length * 0.5, mouth_pos[1] + flame_width * 0.4)
            ]

            # 火焰颜色 - 多层渐变
            flame_outer = (255, 100 + breath_phase * 30, 0)  # 外焰黄红色
            flame_mid = (255, 150 + breath_phase * 20, 50)  # 中焰橙色
            flame_inner = (255, 200 + breath_phase * 10, 100)  # 内焰亮黄色

            # 绘制外层火焰
            pygame.draw.polygon(self.screen, flame_outer, flame_points)

            # 绘制中层火焰
            mid_points = []
            for point in flame_points:
                # 收缩20%
                dx = point[0] - mouth_pos[0]
                dy = point[1] - mouth_pos[1]
                mid_points.append((mouth_pos[0] + dx * 0.8, mouth_pos[1] + dy * 0.8))

            pygame.draw.polygon(self.screen, flame_mid, mid_points)

            # 绘制内层火焰
            inner_points = []
            for point in flame_points:
                # 收缩50%
                dx = point[0] - mouth_pos[0]
                dy = point[1] - mouth_pos[1]
                inner_points.append((mouth_pos[0] + dx * 0.5, mouth_pos[1] + dy * 0.5))

            pygame.draw.polygon(self.screen, flame_inner, inner_points)

            # 火焰粒子效果 - 更丰富的火星
            for _ in range(min(12, breath_phase * 4)):
                # 在火焰范围内随机位置
                t = random.random()  # 位置参数 0-1
                angle = random.uniform(-0.5, 0.5)  # 角度偏移

                # 火星距离随机化
                dist = random.uniform(0.3, 1.0) * flame_length

                # 使用极坐标计算火星位置
                spark_radius = flame_width * 0.4 * (1 - t)  # 火焰宽度随长度减小
                px = mouth_pos[0] + dist * math.cos(angle)
                py = mouth_pos[1] + dist * math.sin(angle)

                # 火星尺寸
                particle_size = max(1, int(random.randint(1, 3) * scale_factor * (1 - 0.7 * t)))

                # 火星颜色 - 更多样化
                color_type = random.random()
                if color_type < 0.6:  # 60% 几率亮黄色
                    particle_color = (255, 220 + random.randint(0, 35), 100 + random.randint(0, 50))
                elif color_type < 0.9:  # 30% 几率橙色
                    particle_color = (255, 180 + random.randint(0, 40), 0 + random.randint(0, 30))
                else:  # 10% 几率红色
                    particle_color = (255, 100 + random.randint(0, 50), 0 + random.randint(0, 20))

                pygame.draw.circle(self.screen, particle_color, (int(px), int(py)), particle_size)

                # 火星轨迹 - 拖尾效果
                if random.random() < 0.3 and particle_size > 1:  # 30% 几率有拖尾
                    trail_length = random.randint(3, 8)
                    trail_x = px - trail_length * math.cos(angle)
                    trail_y = py - trail_length * math.sin(angle)

                    # 半透明拖尾
                    pygame.draw.line(self.screen,
                                     (particle_color[0], particle_color[1], particle_color[2], 100),
                                     (px, py), (trail_x, trail_y), 1)



    # -------------------- 冰霜巨龙绘制 ---------------------
    def draw_dragon_ice(self, monster):
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE

        # 动画参数
        anim_time = pygame.time.get_ticks()
        wing_flap = math.sin(anim_time / 300) * 0.3  # 翅膀摆动弧度
        breath_phase = int((anim_time % 600) / 150)  # 四阶段呼吸循环
        eye_glow = abs(math.sin(anim_time / 400))  # 眼睛发光强度
        body_pulse = 0.03 * math.sin(anim_time / 500)  # 身体微弱起伏效果

        # ---- 阴影效果 ----
        shadow_surf = pygame.Surface((TILE_SIZE * 3, TILE_SIZE * 0.8), pygame.SRCALPHA)
        shadow_ellipse = (TILE_SIZE * 0.5, 0, TILE_SIZE * 2, TILE_SIZE * 0.4)
        pygame.draw.ellipse(shadow_surf, (0, 0, 0, 60), shadow_ellipse)  # 半透明阴影
        self.screen.blit(shadow_surf, (x, y + TILE_SIZE * 2.5))

        # ---- 龙身主体 ----
        # 身体尺寸随呼吸轻微变化
        body_width = int(TILE_SIZE * 1.2 * (1 + body_pulse))
        body_height = int(TILE_SIZE * 0.8 * (1 + body_pulse))
        body_x = x + TILE_SIZE - body_width * 0.3
        body_y = y + TILE_SIZE * 1.5

        # 龙身主体 - 冰霜蓝色
        body_color = (70, 130, 180)  # 冰蓝底色
        pygame.draw.ellipse(self.screen, body_color, (body_x, body_y, body_width, body_height))

        # 冰霜纹理 - 在身体表面添加结晶纹路
        crystal_points = []
        for i in range(4):
            angle = math.pi * 2 * i / 4 + anim_time / 2000
            crystal_points.append((
                body_x + body_width / 2 + math.cos(angle) * body_width / 3,
                body_y + body_height / 2 + math.sin(angle) * body_height / 3
            ))

        # 绘制身体结晶
        for point in crystal_points:
            pygame.draw.circle(self.screen, (200, 240, 255), point, 4)
            # 添加辐射线条
            for j in range(3):
                angle = random.uniform(0, math.pi * 2)
                end_x = point[0] + math.cos(angle) * 6
                end_y = point[1] + math.sin(angle) * 6
                pygame.draw.line(self.screen, (220, 240, 255), point, (end_x, end_y), 1)

        # ---- 尾部 ----
        tail_width = int(TILE_SIZE * 0.3)
        tail_base_x = body_x + body_width * 0.1
        tail_base_y = body_y + body_height * 0.5

        # 尾巴摆动效果
        tail_swing = math.sin(anim_time / 450) * (TILE_SIZE * 0.2)

        tail_points = [
            (tail_base_x, tail_base_y),  # 尾部根部连接到身体
            (tail_base_x - TILE_SIZE * 0.6 + tail_swing * 0.3, body_y + body_height + TILE_SIZE * 0.2),
            (tail_base_x - TILE_SIZE * 1.0 + tail_swing * 0.6, body_y + body_height + TILE_SIZE * 0.4),
            (tail_base_x - TILE_SIZE * 1.2 + tail_swing, body_y + body_height + TILE_SIZE * 0.2)  # 尾部尖端
        ]

        # 绘制尾部
        pygame.draw.polygon(self.screen, (100, 160, 200), tail_points)

        # 尾部冰刺
        for i in range(len(tail_points) - 1):
            mid_x = (tail_points[i][0] + tail_points[i + 1][0]) / 2
            mid_y = (tail_points[i][1] + tail_points[i + 1][1]) / 2

            # 计算垂直于尾部方向的向量
            dx = tail_points[i + 1][0] - tail_points[i][0]
            dy = tail_points[i + 1][1] - tail_points[i][1]
            length = max(0.1, math.sqrt(dx * dx + dy * dy))
            nx, ny = -dy / length, dx / length

            # 绘制冰刺
            spike_length = 8 - i * 2  # 尾尖刺更短
            spike_tip_x = mid_x + nx * spike_length
            spike_tip_y = mid_y + ny * spike_length

            pygame.draw.polygon(self.screen, (200, 240, 255), [
                (mid_x - nx * 2, mid_y - ny * 2),
                (spike_tip_x, spike_tip_y),
                (mid_x + nx * 2, mid_y + ny * 2)
            ])

        # ---- 翅膀系统 ----
        # 翅膀基点连接到身体
        wing_base_left = (body_x + body_width * 0.3, body_y + body_height * 0.2)
        wing_base_right = (body_x + body_width * 0.7, body_y + body_height * 0.2)

        # 翅膀尺寸
        wing_length = TILE_SIZE * 1.2
        wing_width = TILE_SIZE * 0.7

        # 左翼 - 带动态弯曲
        left_wing_tip_x = wing_base_left[0] - wing_length * math.cos(wing_flap)
        left_wing_tip_y = wing_base_left[1] - wing_length * math.sin(wing_flap * 0.8)
        left_wing_mid_x = wing_base_left[0] - wing_length * 0.6 * math.cos(wing_flap + 0.2)
        left_wing_mid_y = wing_base_left[1] - wing_length * 0.4 * math.sin(wing_flap * 0.8 + 0.2)

        left_wing = [
            wing_base_left,
            (left_wing_mid_x, left_wing_mid_y),
            (left_wing_tip_x, left_wing_tip_y),
            (left_wing_mid_x - wing_width * 0.3, left_wing_mid_y + wing_width * 0.5),
            (wing_base_left[0] - wing_width * 0.2, wing_base_left[1] + wing_width * 0.3)
        ]

        # 右翼 - 带动态弯曲
        right_wing_tip_x = wing_base_right[0] + wing_length * math.cos(wing_flap)
        right_wing_tip_y = wing_base_right[1] - wing_length * math.sin(wing_flap * 0.8)
        right_wing_mid_x = wing_base_right[0] + wing_length * 0.6 * math.cos(wing_flap + 0.2)
        right_wing_mid_y = wing_base_right[1] - wing_length * 0.4 * math.sin(wing_flap * 0.8 + 0.2)

        right_wing = [
            wing_base_right,
            (right_wing_mid_x, right_wing_mid_y),
            (right_wing_tip_x, right_wing_tip_y),
            (right_wing_mid_x + wing_width * 0.3, right_wing_mid_y + wing_width * 0.5),
            (wing_base_right[0] + wing_width * 0.2, wing_base_right[1] + wing_width * 0.3)
        ]

        # 绘制翅膀
        for wing_points in [left_wing, right_wing]:
            # 翅膀主体
            pygame.draw.polygon(self.screen, (135, 206, 235), wing_points)  # 淡蓝色翼膜

            # 翅膀骨架
            for i in range(min(3, len(wing_points) - 1)):
                pygame.draw.line(self.screen, (190, 230, 255),
                                 wing_points[0], wing_points[i + 1], 2)

            # 翅膀冰晶
            for i in range(1, len(wing_points)):
                # 随机位置添加冰晶
                crystal_x = (wing_points[i][0] + wing_points[0][0]) / 2 + random.randint(-3, 3)
                crystal_y = (wing_points[i][1] + wing_points[0][1]) / 2 + random.randint(-3, 3)

                # 绘制冰晶
                crystal_size = random.randint(2, 4)
                pygame.draw.polygon(self.screen, (240, 255, 255), [
                    (crystal_x, crystal_y - crystal_size),
                    (crystal_x + crystal_size, crystal_y),
                    (crystal_x, crystal_y + crystal_size),
                    (crystal_x - crystal_size, crystal_y)
                ])

        # ---- 头部系统 ----
        # 脖子
        neck_start = (body_x + body_width * 0.7, body_y + body_height * 0.3)
        neck_end = (body_x + body_width + TILE_SIZE * 0.5, body_y - TILE_SIZE * 0.2)

        # 控制点创建弯曲的脖子
        neck_ctrl1 = (neck_start[0] + (neck_end[0] - neck_start[0]) * 0.3,
                      neck_start[1] - TILE_SIZE * 0.3)
        neck_ctrl2 = (neck_start[0] + (neck_end[0] - neck_start[0]) * 0.7,
                      neck_end[1] + TILE_SIZE * 0.2)

        # 生成脖子曲线点
        neck_points = []
        segments = 8
        for i in range(segments + 1):
            t = i / segments
            # 三次贝塞尔曲线
            px = (1 - t) ** 3 * neck_start[0] + 3 * (1 - t) ** 2 * t * neck_ctrl1[0] + 3 * (1 - t) * t ** 2 * \
                 neck_ctrl2[0] + t ** 3 * neck_end[0]
            py = (1 - t) ** 3 * neck_start[1] + 3 * (1 - t) ** 2 * t * neck_ctrl1[1] + 3 * (1 - t) * t ** 2 * \
                 neck_ctrl2[1] + t ** 3 * neck_end[1]
            neck_points.append((px, py))

        # 绘制脖子
        for i in range(len(neck_points) - 1):
            # 脖子逐渐变窄
            neck_width = 10 - i * 0.8
            pygame.draw.line(self.screen, (100, 160, 200),
                             neck_points[i], neck_points[i + 1], int(neck_width))

            # 添加脖子冰刺
            if i % 2 == 0:
                spine_x = neck_points[i][0]
                spine_y = neck_points[i][1] - neck_width / 2
                spine_height = 6 - i * 0.5

                pygame.draw.polygon(self.screen, (190, 230, 255), [
                    (spine_x - 2, spine_y),
                    (spine_x, spine_y - spine_height),
                    (spine_x + 2, spine_y)
                ])

        # 头部
        head_radius = TILE_SIZE // 3
        head_center = neck_end
        head_rect = (head_center[0] - head_radius * 0.5,
                     head_center[1] - head_radius,
                     head_radius * 2.5,
                     head_radius * 2)

        # 绘制头部
        pygame.draw.ellipse(self.screen, (100, 160, 200), head_rect)

        # 下颚
        jaw_points = [
            (head_center[0], head_center[1] + head_radius * 0.5),
            (head_center[0] + head_radius * 1.2, head_center[1] + head_radius * 0.8),
            (head_center[0] + head_radius * 2, head_center[1] + head_radius * 0.5)
        ]
        pygame.draw.polygon(self.screen, (70, 130, 180), jaw_points)

        # 眼睛 - 发光蓝眼
        eye_radius = head_radius // 3
        eye_center = (head_center[0] + head_radius * 0.5, head_center[1] - head_radius * 0.3)

        # 眼眶
        eye_socket = pygame.Surface((eye_radius * 2.5, eye_radius * 2.5), pygame.SRCALPHA)
        pygame.draw.ellipse(eye_socket, (50, 90, 140, 200), (0, 0, eye_radius * 2.5, eye_radius * 2.5))
        self.screen.blit(eye_socket, (eye_center[0] - eye_radius * 1.25, eye_center[1] - eye_radius * 1.25))

        # 眼白
        pygame.draw.circle(self.screen, (200, 240, 255), eye_center, eye_radius)

        # 动态瞳孔 - 随着动画时间变化
        pupil_offset_x = math.sin(anim_time / 1500) * (eye_radius * 0.3)
        pupil_offset_y = math.cos(anim_time / 1300) * (eye_radius * 0.2)
        pupil_center = (int(eye_center[0] + pupil_offset_x), int(eye_center[1] + pupil_offset_y))

        # 动态发光强度
        glow_intensity = 150 + int(105 * eye_glow)

        # 冰蓝色瞳孔
        pupil_color = (0, glow_intensity, 255)

        # 椭圆形竖瞳 - 冰霜龙的特征
        pupil_height = eye_radius * 1.4
        pupil_width = eye_radius * 0.4
        pupil_rect = (pupil_center[0] - pupil_width / 2, pupil_center[1] - pupil_height / 2,
                      pupil_width, pupil_height)
        pygame.draw.ellipse(self.screen, pupil_color, pupil_rect)

        # 眼睛高光
        highlight_pos = (eye_center[0] - eye_radius * 0.3, eye_center[1] - eye_radius * 0.3)
        highlight_size = max(1, eye_radius // 3)
        pygame.draw.circle(self.screen, (255, 255, 255), highlight_pos, highlight_size)

        # 冰晶角
        horn_base = (head_center[0] + head_radius * 0.3, head_center[1] - head_radius * 0.8)
        horn_mid = (horn_base[0] + head_radius * 0.2, horn_base[1] - head_radius * 0.8)
        horn_tip = (horn_mid[0] + head_radius * 0.1, horn_mid[1] - head_radius * 0.6)

        # 绘制角 - 透明效果
        horn_points = [horn_base, horn_mid, horn_tip]
        for i in range(len(horn_points) - 1):
            # 渐变的蓝色到透明
            alpha = 255 - i * 80
            horn_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.line(horn_surf, (150, 220, 255, alpha),
                             (horn_points[i][0] - x, horn_points[i][1] - y),
                             (horn_points[i + 1][0] - x, horn_points[i + 1][1] - y), 4 - i)
            self.screen.blit(horn_surf, (x, y))

        # 添加角的结晶分支
        branch_count = 3
        for i in range(branch_count):
            t = (i + 1) / (branch_count + 1)
            branch_start_x = horn_base[0] * (1 - t) + horn_tip[0] * t
            branch_start_y = horn_base[1] * (1 - t) + horn_tip[1] * t

            branch_length = (branch_count - i) * 5
            branch_angle = math.pi / 4 + (i * math.pi / 6)

            branch_end_x = branch_start_x + math.cos(branch_angle) * branch_length
            branch_end_y = branch_start_y + math.sin(branch_angle) * branch_length

            pygame.draw.line(self.screen, (200, 240, 255, 150),
                             (branch_start_x, branch_start_y),
                             (branch_end_x, branch_end_y), 2)

        # ---- 冰霜吐息特效 ----
        if breath_phase > 0:
            breath_length = TILE_SIZE * (0.5 + 0.3 * breath_phase)
            mouth_pos = (head_center[0] + head_radius * 2, head_center[1] + head_radius * 0.3)

            # 冰雾主体 - 半透明锥形
            breath_points = [
                mouth_pos,
                (mouth_pos[0] + breath_length, mouth_pos[1] - breath_length / 3),
                (mouth_pos[0] + breath_length * 1.2, mouth_pos[1]),
                (mouth_pos[0] + breath_length, mouth_pos[1] + breath_length / 3)
            ]

            # 绘制冰雾
            breath_surf = pygame.Surface((TILE_SIZE * 4, TILE_SIZE * 2), pygame.SRCALPHA)
            pygame.draw.polygon(breath_surf, (200, 240, 255, 150 - breath_phase * 20),
                                [(p[0] - mouth_pos[0] + TILE_SIZE * 1.5, p[1] - mouth_pos[1] + TILE_SIZE) for p in
                                 breath_points])
            self.screen.blit(breath_surf, (mouth_pos[0] - TILE_SIZE * 1.5, mouth_pos[1] - TILE_SIZE))

            # 添加冰晶粒子
            for _ in range(4 + breath_phase * 2):
                # 随机位置
                t = random.random()
                angle = random.uniform(-0.3, 0.3)
                dist = breath_length * t * 0.8
                px = mouth_pos[0] + dist * math.cos(angle)
                py = mouth_pos[1] + dist * math.sin(angle)

                # 冰晶大小随距离变化
                crystal_size = 3 - t * 2

                # 随机冰晶形态
                if random.random() < 0.5:
                    # 菱形冰晶
                    pygame.draw.polygon(self.screen, (220, 240, 255), [
                        (px, py - crystal_size),
                        (px + crystal_size, py),
                        (px, py + crystal_size),
                        (px - crystal_size, py)
                    ])
                else:
                    # 圆形冰晶
                    pygame.draw.circle(self.screen, (220, 240, 255), (int(px), int(py)), int(crystal_size))
                    # 添加高光
                    pygame.draw.circle(self.screen, (255, 255, 255),
                                       (int(px - crystal_size * 0.3), int(py - crystal_size * 0.3)),
                                       max(1, int(crystal_size * 0.5)))

        # ---- 环境冰霜效果 ----
        # 地面冰霜
        frost_effect = pygame.Surface((TILE_SIZE * 3, TILE_SIZE), pygame.SRCALPHA)
        for _ in range(15):
            fx = random.randint(0, TILE_SIZE * 3 - 1)
            fy = random.randint(TILE_SIZE // 2, TILE_SIZE - 1)
            size = random.randint(2, 5)
            alpha = random.randint(40, 80)
            pygame.draw.circle(frost_effect, (200, 240, 255, alpha), (fx, fy), size)
        self.screen.blit(frost_effect, (x, y + TILE_SIZE * 2))

    # ----------------- 神圣骑士绘制 -------------------

    def draw_holy_knight(self, monster, holy_ball_count=5):
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE
        w = monster.size[0] * TILE_SIZE
        h = monster.size[1] * TILE_SIZE

        # 动画参数和时间
        anim_time = pygame.time.get_ticks()

        # 整体缩放因子 (调整这个值来控制整体大小)
        scale_factor = 0.7

        # ----- 背景光晕效果 (按比例缩小) -----

        # 更紧凑的光晕区域
        glow_radius = int((w * 0.8 + 20 + int(15 * math.sin(anim_time / 400))) * scale_factor * 0.45)
        glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)

        # 多层渐变光晕
        for i in range(5):
            alpha = 110 - i * 18  # 略微降低透明度
            s_scale = 1 - (i * 0.15)
            color = (255, 255, 200, alpha)
            pygame.draw.circle(glow_surface, color,
                               (glow_radius, glow_radius),
                               int(glow_radius * s_scale))

        # 绘制脉动的光晕波纹
        pulse_scale = 0.6 + 0.4 * math.sin(anim_time / 300)
        outer_glow = pygame.Surface((int(glow_radius * 2.2), int(glow_radius * 2.2)), pygame.SRCALPHA)
        pygame.draw.circle(outer_glow, (255, 255, 200, 40),
                           (int(glow_radius * 1.1), int(glow_radius * 1.1)),
                           int(glow_radius * pulse_scale * 1.2))

        # 绘制光晕到屏幕
        glow_center = (x + w // 2, y + h // 2)
        self.screen.blit(outer_glow,
                         (glow_center[0] - int(glow_radius * 1.1),
                          glow_center[1] - int(glow_radius * 1.1)))
        self.screen.blit(glow_surface,
                         (glow_center[0] - glow_radius,
                          glow_center[1] - glow_radius))

        # ----- 核心菱形特效 (按比例缩小) -----

        # 菱形核心尺寸
        core_size = int((w // 4) * scale_factor)  # 按比例缩小核心
        core_center = (x + w // 2, y + h // 2)

        # 强烈脉冲光效果
        pulse_intensity = 0.6 + 0.4 * abs(math.sin(anim_time / 150))
        for i in range(4):
            pulse_radius = (core_size // 2) * (1 + i * 0.9) * pulse_intensity
            pulse_alpha = int(180 * pulse_intensity) - i * 35  # 略微降低亮度
            pulse_surf = pygame.Surface((int(pulse_radius * 2), int(pulse_radius * 2)), pygame.SRCALPHA)
            pygame.draw.circle(pulse_surf, (255, 255, 220, pulse_alpha),
                               (int(pulse_radius), int(pulse_radius)),
                               int(pulse_radius))
            self.screen.blit(pulse_surf,
                             (core_center[0] - int(pulse_radius),
                              core_center[1] - int(pulse_radius)))

        # 菱形点坐标 (按比例缩小)
        diamond_points = [
            (core_center[0], core_center[1] - core_size // 2),  # 上
            (core_center[0] + core_size // 2, core_center[1]),  # 右
            (core_center[0], core_center[1] + core_size // 2),  # 下
            (core_center[0] - core_size // 2, core_center[1])  # 左
        ]

        # 绘制主菱形
        pygame.draw.polygon(self.screen, (255, 230, 150), diamond_points)

        # 内部装饰 (按比例缩小)
        inner_diamond_points = []
        for point in diamond_points:
            # 缩小到70%大小
            dx = point[0] - core_center[0]
            dy = point[1] - core_center[1]
            inner_point = (core_center[0] + dx * 0.7, core_center[1] + dy * 0.7)
            inner_diamond_points.append(inner_point)

        # 绘制内部菱形
        pygame.draw.polygon(self.screen, (255, 250, 220), inner_diamond_points)

        # 核心十字线 (按比例缩小)
        cross_color = (255, 255, 255, int(200 * pulse_intensity))
        cross_length = core_size * pulse_intensity
        pygame.draw.line(self.screen, cross_color,
                         (core_center[0], core_center[1] - cross_length // 2),
                         (core_center[0], core_center[1] + cross_length // 2), 2)  # 线宽减小
        pygame.draw.line(self.screen, cross_color,
                         (core_center[0] - cross_length // 2, core_center[1]),
                         (core_center[0] + cross_length // 2, core_center[1]), 2)  # 线宽减小

        # 脉冲光线 (按比例缩小)
        for i in range(8):
            angle = anim_time / 500 + i * math.pi / 4
            line_length = core_size * (0.8 + 0.4 * math.sin(anim_time / 200 + i))
            end_x = core_center[0] + math.cos(angle) * line_length
            end_y = core_center[1] + math.sin(angle) * line_length

            # 变化的线宽和透明度
            line_width = max(1, int(2 * pulse_intensity))  # 线宽减小但至少为1
            line_alpha = int(150 * pulse_intensity)

            # 创建线性渐变效果
            for j in range(3):
                t = j / 2
                mid_x = core_center[0] + math.cos(angle) * line_length * t
                mid_y = core_center[1] + math.sin(angle) * line_length * t

                # 计算线段的透明度和宽度
                segment_alpha = line_alpha * (1 - t)
                segment_width = max(1, line_width * (1 - t))

                pygame.draw.line(self.screen, (255, 255, 200, int(segment_alpha)),
                                 (mid_x, mid_y),
                                 (end_x, end_y), int(segment_width))

        # ----- 周围圣光球 (按比例缩小) -----

        # 创建5个围绕的圣光球 (适当缩小)
        holy_balls = []
        for i in range(holy_ball_count):
            # 计算基础轨道位置 (轨道半径按比例缩小)
            angle = anim_time / 800 + i * math.pi * 2 / holy_ball_count
            radius = (core_size * 3.5 + 15 * math.sin(anim_time / 600 + i * 0.7)) * scale_factor * 1.1  # 适当放大一点轨道以保持平衡

            # 添加不规则运动 (抖动幅度减小)
            jitter_x = 6 * math.sin(anim_time / 250 + i * 0.9)
            jitter_y = 6 * math.cos(anim_time / 220 + i * 1.1)

            ball_x = core_center[0] + radius * math.cos(angle) + jitter_x
            ball_y = core_center[1] + radius * math.sin(angle) + jitter_y
            ball_size = (13 + 4 * math.sin(anim_time / 200 + i)) * scale_factor  # 球体大小按比例缩小

            holy_balls.append((ball_x, ball_y, ball_size, i))

        # 绘制神圣球连接光线 (按比例缩小)
        if anim_time % 800 < 400:  # 交替显示连接光线
            for i in range(len(holy_balls)):
                start_ball = holy_balls[i]
                end_ball = holy_balls[(i + 1) % len(holy_balls)]

                # 创建弧形光线路径
                points = []
                segments = 8
                for j in range(segments + 1):
                    t = j / segments
                    # 线性插值球体位置
                    x = start_ball[0] * (1 - t) + end_ball[0] * t
                    y = start_ball[1] * (1 - t) + end_ball[1] * t

                    # 添加向核心的弯曲 (弯曲程度按比例缩小)
                    curve_factor = math.sin(t * math.pi) * 15 * scale_factor
                    dx = core_center[0] - x
                    dy = core_center[1] - y
                    dist = math.hypot(dx, dy)
                    if dist > 0:
                        x += dx / dist * curve_factor
                        y += dy / dist * curve_factor

                    points.append((x, y))

                # 绘制连接线 (线宽减小)
                if len(points) > 1:
                    for j in range(len(points) - 1):
                        alpha = int(100 * (1 - abs(j / segments - 0.5) * 2))  # 降低亮度
                        pygame.draw.line(self.screen, (255, 255, 180, alpha),
                                         points[j], points[j + 1], 1)  # 线宽减为1

        # 绘制神圣球 (按比例缩小)
        for ball_x, ball_y, ball_size, idx in holy_balls:
            # 多层光晕效果 (缩小版)
            max_glow = 2.2  # 略微减小光晕系数

            # 外层柔和光晕
            for j in range(3):
                glow_size = ball_size * (max_glow - j * 0.4)
                alpha = 90 - j * 25  # 降低透明度
                ball_glow = pygame.Surface((int(glow_size * 2), int(glow_size * 2)), pygame.SRCALPHA)

                # 根据索引变化颜色
                hue_shift = idx * 30  # 0-120 度色相变化
                glow_color = self._hue_shift((255, 255, 200), hue_shift, alpha)

                pygame.draw.circle(ball_glow, glow_color,
                                   (int(glow_size), int(glow_size)),
                                   int(glow_size))
                self.screen.blit(ball_glow,
                                 (ball_x - int(glow_size),
                                  ball_y - int(glow_size)))

            # 球体主体
            main_color = self._hue_shift((255, 255, 220), idx * 30, 255)
            pygame.draw.circle(self.screen, main_color,
                               (int(ball_x), int(ball_y)),
                               int(ball_size))

            # 内部高光 (按比例缩小)
            highlight_size = ball_size * 0.4
            pygame.draw.circle(self.screen, (255, 255, 255),
                               (int(ball_x - ball_size * 0.2), int(ball_y - ball_size * 0.2)),
                               int(highlight_size))

            # 球体内部能量螺旋 (螺旋段数减少)
            spiral_points = []
            spiral_segments = 8  # 减少螺旋段数
            for s in range(spiral_segments):
                spiral_t = s / spiral_segments
                spiral_radius = ball_size * spiral_t * 0.85
                spiral_angle = spiral_t * 4 * math.pi + anim_time / 200

                sx = ball_x + math.cos(spiral_angle) * spiral_radius
                sy = ball_y + math.sin(spiral_angle) * spiral_radius
                spiral_points.append((sx, sy))

            # 绘制螺旋 (线宽减小)
            if len(spiral_points) > 1:
                for s in range(len(spiral_points) - 1):
                    alpha = int(170 * (1 - s / spiral_segments))
                    pygame.draw.line(self.screen, (255, 255, 255, alpha),
                                     spiral_points[s], spiral_points[s + 1], 1)  # 线宽减为1

        # ----- 环绕粒子特效 (减少生成概率和数量) -----

        # 随机添加环绕粒子 (降低生成概率)
        if random.random() < 0.25:  # 降低生成概率
            particle_angle = random.uniform(0, math.pi * 2)
            particle_dist = random.uniform(core_size, glow_radius * 0.8)
            particle_x = core_center[0] + math.cos(particle_angle) * particle_dist
            particle_y = core_center[1] + math.sin(particle_angle) * particle_dist

            # 向核心的速度矢量
            dx = core_center[0] - particle_x
            dy = core_center[1] - particle_y
            dist = math.hypot(dx, dy)
            vx = dx / dist * random.uniform(1, 4)  # 略微降低速度
            vy = dy / dist * random.uniform(1, 4)

            # 添加粒子到游戏粒子系统 (尺寸按比例缩小)
            self.fear_particles.append({
                'pos': [particle_x, particle_y],
                'vel': [vx, vy],
                'life': random.uniform(0.4, 1.0),  # 略微缩短寿命
                'max_life': 1.0,
                'size': random.uniform(1.5, 3.5) * scale_factor,  # 粒子尺寸按比例缩小
                'color': (255, 255, 200)  # 圣光金色
            })

    # 辅助函数：调整颜色色相
    def _hue_shift(self, color, shift, alpha=255):
        r, g, b = color
        # 转换为HSV并偏移色相 (简化版本)
        max_val = max(r, g, b)
        min_val = min(r, g, b)
        delta = max_val - min_val

        if delta == 0:
            return (r, g, b, alpha)  # 灰色无色相

        # 非精确的色相偏移，但足够用于视觉效果
        shifted_r = int(r * (1 + math.sin(math.radians(shift)) * 0.2))
        shifted_g = int(g * (1 + math.sin(math.radians(shift + 120)) * 0.2))
        shifted_b = int(b * (1 + math.sin(math.radians(shift + 240)) * 0.2))

        # 限制在0-255范围内
        shifted_r = max(0, min(255, shifted_r))
        shifted_g = max(0, min(255, shifted_g))
        shifted_b = max(0, min(255, shifted_b))

        return (shifted_r, shifted_g, shifted_b, alpha)

    # ------------------- 火焰领主的绘制 -------------------

    def draw_fire_lord(self, monster):
        anim_time = pygame.time.get_ticks()
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE

        # 主体火焰
        if "纯" in monster.name:
            core_color = (0, 155 - int(100 * math.sin(anim_time / 300)), 205 - int(50 * (-math.sin(anim_time / 300))))
        else:
            core_color = (255, 100 + int(100 * math.sin(anim_time / 300)), 50 + int(50 * (-math.sin(anim_time / 300))))

        core_pos = (x + TILE_SIZE * 1.85, y + TILE_SIZE * 1.5)
        pygame.draw.circle(self.screen, core_color,
                           core_pos, 20)
        period = 5
        for i in range(period):
            if "纯" in monster.name:
                pygame.draw.circle(self.screen, (5, 155 - int(100 * math.sin(anim_time / 300 + 2 * i * math.pi / period)),
                205 - int(50 * (-math.cos(anim_time / 400 + 2 * i * math.pi / period)))),
                                   (x + TILE_SIZE * 1.85 + int(
                                       TILE_SIZE * 0.9 * math.sin(anim_time / 300 + 2 * i * math.pi / period)),
                                    y + TILE_SIZE * 1.5 + int(
                                        TILE_SIZE * 0.9 * math.cos(anim_time / 200 + 2 * i * math.pi / period))), 5)
            else:
                pygame.draw.circle(self.screen, (250, 100 + int(100 * math.sin(anim_time / 300 + 2 * i * math.pi / period)),
                50 + int(50 * (-math.cos(anim_time / 400 + 2 * i * math.pi / period)))),
                                   (x + TILE_SIZE * 1.85 + int(
                                       TILE_SIZE * 0.9 * math.sin(anim_time / 300 + 2 * i * math.pi / period)),
                                    y + TILE_SIZE * 1.5 + int(
                                        TILE_SIZE * 0.9 * math.cos(anim_time / 200 + 2 * i * math.pi / period))), 5)

        length_vertical = 0.45 * TILE_SIZE
        length_horizontal = 0.12 * TILE_SIZE

        # 头部火焰
        flame_points = [
            (x + TILE_SIZE * 1.85 - length_horizontal, y + TILE_SIZE * 1.5),
            (x + TILE_SIZE * 1.85, y + TILE_SIZE * 1.5 + length_vertical),
            (x + TILE_SIZE * 1.85 + length_horizontal, y + TILE_SIZE * 1.5),
            (x + TILE_SIZE * 1.85, y + TILE_SIZE * 1.5 - length_vertical)
        ]
        if "纯" in monster.name:
            pygame.draw.polygon(self.screen, (0, 100 - int(100 * math.sin(anim_time / 300)), 100), flame_points)
        else:
            pygame.draw.polygon(self.screen, (255, 155 + int(100 * math.sin(anim_time / 300)), 155), flame_points)

        # 双手火焰
        for i in range(2):
            hand_x = x + (100 if i else 20)
            for j in range(3):
                angle = anim_time / 200 + i * 180 + j * 30
                px = hand_x + math.cos(math.radians(angle)) * 30
                py = y + 80 + math.sin(math.radians(angle * 2)) * 30
                size = 15 - j * 4
                if "纯" in monster.name:
                    pygame.draw.circle(self.screen, (0, 155 - j * 50, 255),
                                       (int(px), int(py)), size)
                    self.draw_lightning((int(px), int(py)), (int(px), int(py)), 9 - j,
                                        (0, 155 - j * 50, 255))
                else:
                    pygame.draw.circle(self.screen, (255, 100 + j * 50, 0),
                                       (int(px), int(py)), size)
                    self.draw_lightning((int(px), int(py)), (int(px), int(py)), 9 - j,
                                        (255, 100 + j * 50, 0))

        # 动态粒子
        if random.random() < 0.3:
            self.fear_particles.append({
                'pos': [x + 50 + random.randint(-20, 20), y + 50],
                'vel': [random.uniform(-2, 2), random.uniform(-5, -2)],
                'life': 1.0,
                'max_life': 1.0,
                'size': random.randint(3, 6),
                'color': (0, 255- random.randint(100, 200), 255) if "纯" in monster.name else (255, random.randint(100, 200), 0)
            })

    # ------------- 游戏物品绘制 ------------------

    # ------------- 宝箱 ----------------

    def draw_chest(self, item):
        x = item.x * TILE_SIZE
        y = item.y * TILE_SIZE
        anim_time = pygame.time.get_ticks()

        # 调整尺寸比例，适合单格
        width = TILE_SIZE * 0.8
        height = TILE_SIZE * 0.65
        x_offset = (TILE_SIZE - width) / 2
        y_offset = (TILE_SIZE - height) / 2

        # 箱体底色(红褐色)
        pygame.draw.rect(self.screen, (140, 60, 60),
                         (x + x_offset, y + y_offset, width, height),
                         border_radius=int(height / 3))

        # 金色边框
        pygame.draw.rect(self.screen, (220, 180, 50),
                         (x + x_offset, y + y_offset, width, height),
                         2, border_radius=int(height / 3))

        # 水平金属条(上)
        pygame.draw.rect(self.screen, (220, 180, 50),
                         (x + x_offset, y + y_offset + height * 0.3, width, height * 0.1))

        # 水平金属条(下)
        pygame.draw.rect(self.screen, (220, 180, 50),
                         (x + x_offset, y + y_offset + height * 0.6, width, height * 0.1))

        # 垂直金属条
        pygame.draw.rect(self.screen, (220, 180, 50),
                         (x + x_offset + width / 2 - 2, y + y_offset, 4, height))

        # 锁具
        lock_size = width * 0.2
        pygame.draw.rect(self.screen, (180, 150, 40),
                         (x + x_offset + width / 2 - lock_size / 2,
                          y + y_offset + height * 0.4,
                          lock_size, lock_size))

        # 骷髅图案(简化)
        skull_x = x + x_offset + width / 2
        skull_y = y + y_offset + height * 0.45
        skull_size = width * 0.14

        # 头骨
        pygame.draw.circle(self.screen, (240, 240, 240),
                           (skull_x, skull_y), int(skull_size))

        # 红宝石(闪烁效果替代眼睛)
        ruby_size = skull_size * 0.35
        ruby_glow = abs(math.sin(anim_time / 300))
        ruby_color = (200 + int(55 * ruby_glow), 20, 20)  # 红宝石颜色随时间变化

        # 中央红宝石
        pygame.draw.circle(self.screen, ruby_color,
                           (skull_x, skull_y), int(ruby_size))

        # 宝石高光
        if ruby_glow > 0.7:
            pygame.draw.circle(self.screen, (255, 180, 180),
                               (skull_x - ruby_size / 3, skull_y - ruby_size / 3), 2)

        # 箱体闪光效果
        if anim_time % 2000 < 300:
            shine_pos = x + x_offset + width * 0.25
            pygame.draw.circle(self.screen, (255, 255, 200),
                               (shine_pos, y + y_offset + height * 0.25), 2)

    # ------------- 红药水 ----------------

    def draw_potion(self, item):
        x = item.x * TILE_SIZE
        y = item.y * TILE_SIZE

        # 确定药水尺寸和位置 - 适合单格
        width = TILE_SIZE * 0.6
        height = TILE_SIZE * 0.7
        bottle_x = x + (TILE_SIZE - width) / 2
        bottle_y = y + (TILE_SIZE - height) / 2

        # 药水颜色
        if "HP" in item.item_type:
            if "SMALL" in item.item_type:
                liquid_color = (220, 40, 40)  # 鲜红色 (小红药)
                glow_color = (255, 120, 120)  # 高光色
            else:
                liquid_color = (180, 0, 0)  # 深红色 (大红药)
                glow_color = (220, 60, 60)  # 高光色
        elif "MP" in item.item_type:
            if "SMALL" in item.item_type:
                liquid_color = (40, 40, 220)  # 鲜蓝色 (小蓝药)
                glow_color = (120, 120, 255)  # 高光色
            else:
                liquid_color = (0, 0, 180)  # 深蓝色 (大蓝药)
                glow_color = (60, 60, 220)  # 高光色

        # 瓶颈
        neck_width = width * 0.4
        neck_height = height * 0.2
        neck_x = bottle_x + (width - neck_width) / 2
        neck_y = bottle_y
        pygame.draw.rect(self.screen, (170, 170, 210),
                         (neck_x, neck_y, neck_width, neck_height),
                         border_radius=int(neck_width * 0.2))

        # 瓶塞
        cork_width = neck_width * 0.8
        cork_height = neck_height * 0.5
        cork_x = neck_x + (neck_width - cork_width) / 2
        cork_y = neck_y - cork_height * 0.8
        pygame.draw.rect(self.screen, (140, 90, 40),
                         (cork_x, cork_y, cork_width, cork_height),
                         border_radius=int(cork_width * 0.2))

        # 瓶身
        body_width = width
        body_height = height * 0.8
        body_x = bottle_x
        body_y = bottle_y + neck_height * 0.8
        pygame.draw.rect(self.screen, (180, 180, 220, 200),
                         (body_x, body_y, body_width, body_height),
                         border_radius=int(body_width * 0.3))

        # 药水液体
        liquid_height = body_height * 0.85
        liquid_y = body_y + body_height - liquid_height
        pygame.draw.rect(self.screen, liquid_color,
                         (body_x + 2, liquid_y, body_width - 4, liquid_height),
                         border_radius=int(body_width * 0.25))

        # 液体波纹
        wave_y = liquid_y + liquid_height * 0.15
        pygame.draw.line(self.screen, glow_color,
                         (body_x + 3, wave_y),
                         (body_x + body_width - 3, wave_y), 2)

        # 瓶身反光/高光
        pygame.draw.line(self.screen, (255, 255, 255, 150),
                         (body_x + body_width * 0.2, body_y + body_height * 0.2),
                         (body_x + body_width * 0.1, body_y + body_height * 0.5), 2)

    # ------------- 宝石 ----------------

    def draw_gem(self, item):
        x = item.x * TILE_SIZE
        y = item.y * TILE_SIZE
        anim_time = pygame.time.get_ticks()

        # 确定宝石中心位置和尺寸
        size = TILE_SIZE * 0.6
        center_x = x + TILE_SIZE // 2
        center_y = y + TILE_SIZE // 2

        # 根据类型设置颜色
        if item.item_type == "ATK_GEM":
            main_color = (180, 30, 30)  # 深红色
            mid_color = (220, 50, 50)  # 中红色
            light_color = (255, 100, 100)  # 浅红色
        elif item.item_type == "DEF_GEM":
            main_color = (20, 50, 150)  # 深蓝色
            mid_color = (40, 80, 200)  # 中蓝色
            light_color = (80, 120, 240)  # 浅蓝色
        elif item.item_type == "ATK_GEM_LARGE":
            main_color = (180, 20, 20)  # 深红色
            mid_color = (220, 40, 40)  # 中红色
            light_color = (255, 80, 80)  # 浅红色
            # 大宝石尺寸略大
            size = TILE_SIZE * 0.75
        elif item.item_type == "DEF_GEM_LARGE":
            main_color = (10, 40, 140)  # 深蓝色
            mid_color = (30, 70, 190)  # 中蓝色
            light_color = (70, 110, 230)  # 浅蓝色
            # 大宝石尺寸略大
            size = TILE_SIZE * 0.75

        # 椭圆形宝石基本形状
        pygame.draw.ellipse(self.screen, main_color,
                            (center_x - size / 2, center_y - size / 2 + size * 0.05, size, size * 0.9))

        # 主要切面
        facet_points = [
            (center_x, center_y - size * 0.35),  # 顶部
            (center_x + size * 0.35, center_y),  # 右侧
            (center_x, center_y + size * 0.35),  # 底部
            (center_x - size * 0.35, center_y),  # 左侧
        ]
        pygame.draw.polygon(self.screen, mid_color, facet_points)

        # 中央切面
        inner_scale = 0.2
        inner_facet = [
            (center_x, center_y - size * inner_scale),
            (center_x + size * inner_scale, center_y),
            (center_x, center_y + size * inner_scale),
            (center_x - size * inner_scale, center_y)
        ]
        pygame.draw.polygon(self.screen, light_color, inner_facet)

        # 高光切面 (顶部和右侧)
        highlight_points = [
            (center_x, center_y - size * 0.35),  # 顶点
            (center_x + size * 0.2, center_y - size * 0.2),  # 右上
            (center_x, center_y)  # 中心
        ]
        pygame.draw.polygon(self.screen, light_color, highlight_points)

        # 随机闪烁高光点
        if anim_time % 3000 < 200:
            # 右上高光点
            pygame.draw.circle(self.screen, (255, 255, 255), (int(center_x + size * 0.15), int(center_y - size * 0.15)),
                               2)

        # 为大宝石添加额外的闪烁效果
        if "LARGE" in item.item_type and anim_time % 1500 < 150:
            # 中心高光
            pygame.draw.circle(self.screen, (255, 255, 255), (int(center_x), int(center_y)), 3)

    # ------------------- 玩家传送路径绘制 -------------------

    def draw_path(self):
        """绘制路径"""
        if self.path_timer > 0:
            for i, (x, y) in enumerate(self.path):
                # 使用黄色透明荧光虚线
                if i < len(self.path) - 1:
                    next_x, next_y = self.path[i + 1]
                    # 计算起点和终点的屏幕坐标
                    start_pos = (x * TILE_SIZE + TILE_SIZE // 2, y * TILE_SIZE + TILE_SIZE // 2)
                    end_pos = (next_x * TILE_SIZE + TILE_SIZE // 2, next_y * TILE_SIZE + TILE_SIZE // 2)
                    # 绘制路径效果
                    if ORDINARYEFFECT:
                        pygame.draw.line(self.screen, (255, 255, 0, int(255 * (self.path_timer / (PATHTIME * 30)))),
                                         start_pos, end_pos, 3)
                    if self.lightning_path_yellow:
                        self.draw_lightning(start_pos, end_pos, 4, (255, 255, 0))
                    if self.lightning_path_blue:
                        self.draw_lightning(start_pos, end_pos, 4, (51, 51, 255))
                    if self.lightning_path_red:
                        self.draw_lightning(start_pos, end_pos, 4, (255, 51, 51))
            # 减少计时器
            self.path_timer -= 1

    # ----------------------- 楼层生成 ------------------------

    def generate_items(self, count):
        items = []

        # 更新当前楼层的物品掉落修正
        self.item_system.update_floor_bonus(self.floor)

        # 生成指定数量的物品
        for _ in range(count):
            while True:
                x = random.randint(1, MAP_WIDTH - 2)
                y = random.randint(1, MAP_HEIGHT - 2)
                if self.is_position_empty(x, y):
                    break

            # 使用物品概率系统生成物品
            item = self.item_system.generate_random_item(x, y)
            items.append(item)

        return items

    def draw_item_with_rarity(self, item):
        # 先绘制基本物品
        if "CHEST" in item.item_type:
            self.draw_chest(item)
        elif "HP_" in item.item_type or "MP_" in item.item_type:
            self.draw_potion(item)
        elif "GEM" in item.item_type:
            self.draw_gem(item)

        # 获取物品稀有度和颜色
        rarity = self.item_system.get_item_rarity(item.item_type)
        rarity_color = self.item_system.get_rarity_color(rarity)

        # 对"珍贵"物品添加额外粒子效果
        if rarity == "珍贵" and random.random() < 0.2:  # 10%概率生成粒子
            x = item.x * TILE_SIZE
            y = item.y * TILE_SIZE
            angle = random.uniform(0, math.pi * 2)
            distance = random.uniform(5, 15)
            particle_x = x + TILE_SIZE // 2 + math.cos(angle) * distance
            particle_y = y + TILE_SIZE // 2 + math.sin(angle) * distance

            pygame.draw.circle(self.screen, rarity_color,
                               (int(particle_x), int(particle_y)),
                               random.randint(1, 3))

    def generate_floor(self):
        # 生成迷宫
        self.maze = generate_maze(MAP_WIDTH, MAP_HEIGHT)

        # 生成房间
        self.rooms = add_rooms(self.maze)

        # 在生成完迷宫后创建背景Surface 静态渲染
        self.background_surface = pygame.Surface((MAP_WIDTH * TILE_SIZE, MAP_HEIGHT * TILE_SIZE))

        #---------------------------- 动态部分 -----------------------------

        # 在生成普通房间时替换为喷泉房间
        for i in range(len(self.rooms)):
            room = self.rooms[i]
            if (room[2] >= 7 and room[3] >= 7 and
                    random.random() < FOUNTAIN_ROOM_PROB+LAVA_ROOM_PROB):
                if random.random() < 0.5:
                    # 替换为喷泉房间
                    self.create_fountain_room(room)
                else:
                    # 替换为喷泉房间
                    self.create_lava_room(room)
                # 从房间列表中移除原房间
                self.rooms.pop(i)
                break

        floor_tiles = [(x, y) for y in range(MAP_HEIGHT) for x in range(MAP_WIDTH) if self.maze[y][x] == 0]
        self.start_pos = random.choice(floor_tiles) if floor_tiles else (1, 1)
        far_tiles = [pos for pos in floor_tiles if
                     abs(pos[0] - self.start_pos[0]) + abs(pos[1] - self.start_pos[1]) > 10]
        self.exit_pos = random.choice(far_tiles) if far_tiles else self.start_pos

        # 生成怪物和道具
        self.monsters = []
        self.items = []

        # 记录实体占位
        occupied = {self.start_pos, self.exit_pos}

        # 首先生成boss
        boss_monsters = [
            monster for monster in monsters_data
            if monster["name"] in ["普通巨龙", "魔王", "圣洁魔王", "冰霜巨龙", "血腥闪电", "纯青闪电", "金色闪电", "火焰领主", "纯火焰领主"]
               and monster.get("level", 1) <= self.floor
        ]
        for alpha in boss_monsters:
            boss = random.choice(boss_monsters)
            # 只在房间中央生成
            room_centers = [(room[0] + room[2] // 2, room[1] + room[3] // 2) for room in self.rooms]
            for center in room_centers:
                if self.is_position_empty_for_monster(center[0], center[1], boss["size"], occupied):
                    if random.random() < 0.5:
                        self.monsters.append(Monster(center[0], center[1], boss, self.floor))
                        # 标记占用区域
                        for dx in range(boss["size"][0]):
                            for dy in range(boss["size"][1]):
                                occupied.add((center[0] + dx, center[1] + dy))  # 记录boss占位
                        break

        # 生成其他怪物
        eligible_monsters = []
        eligible_weights = []
        for i, m in enumerate(monsters_data):
            if (m.get("level", 1) <= self.floor and
                    m["name"] not in ["普通巨龙", "魔王", "圣洁魔王", "冰霜巨龙", "血腥闪电", "纯青闪电", "金色闪电", "火焰领主", "纯火焰领主"]):
                eligible_monsters.append(m)
                eligible_weights.append(MONSTER_WEIGHT[i])

        # 生成普通怪物
        for _ in range(random.randint(MONSTER_MIN, MONSTER_MAX)):
            if not eligible_monsters:
                break
            mdata = random.choices(eligible_monsters, weights=eligible_weights, k=1)[0]

            if mdata["name"] in ["普通巨龙", "魔王", "圣洁魔王", "冰霜巨龙", "血腥闪电", "纯青闪电", "金色闪电", "火焰领主", "纯火焰领主"]:
                continue  # 已经生成过boss
            pos = self.get_random_tile_for_monster(floor_tiles, occupied, mdata["size"])
            if pos:
                self.monsters.append(Monster(pos[0], pos[1], mdata, self.floor))
                # 标记占用区域
                for dx in range(mdata["size"][0]):
                    for dy in range(mdata["size"][1]):
                        occupied.add((pos[0] + dx, pos[1] + dy))  # 记录普通怪占位

        # 生成道具
        item_count = random.randint(ITEM_MIN, ITEM_MAX)
        self.items = self.generate_items(item_count)

        for room in self.rooms:
            room_center = (room[0] + room[2] // 3, room[1] + room[3] // 3)
            if random.random() < 0.3:  # 30%概率生成装备
                equip_type = random.choice(list(EQUIPMENT_TYPES.keys()))
                self.items.append(Item(room_center[0], room_center[1], equip_type, EQUIPMENT_TYPES[equip_type]))

        # 预生成墙壁和地板的样式数据
        self.tile_styles = [[None for _ in range(MAP_WIDTH)] for _ in range(MAP_HEIGHT)]
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if self.maze[y][x] == 1:  # 墙壁
                    # 随机选择样式类型并生成参数
                    style_data = self.generate_wall_style(x, y)
                else:  # 地板
                    style_data = self.generate_floor_style(x, y)
                self.tile_styles[y][x] = style_data

        # 动画参数设置
        center_x = self.start_pos[0] * TILE_SIZE + TILE_SIZE // 2
        center_y = self.start_pos[1] * TILE_SIZE + TILE_SIZE // 2
        self.animation_center = (center_x, center_y)

        # 计算最大半径（屏幕对角线）
        dx = max(center_x, SCREEN_WIDTH - center_x)
        dy = max(center_y, SCREEN_HEIGHT - center_y)
        self.animation_max_radius = math.hypot(dx, dy)

        self.animation_radius = 0
        self.is_animating = True  # 触发动画

        # 预绘制静态背景
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if self.maze[y][x] == 1:
                    self.draw_wall(x, y, self.background_surface)
                else:
                    self.draw_floor(x, y, self.background_surface)

    # ---------------------- 喷泉房 ----------------------

    def draw_fountain_room(self):
        for y in range(MAP_HEIGHT):
            for x in range(MAP_WIDTH):
                if self.maze[y][x] == 2:  # 喷泉区域
                    self.draw_fountain_tile(x, y)
                elif self.maze[y][x] == 3:  # 岩浆
                    self.draw_lava_tile(x, y)
                elif self.maze[y][x] == 4:  # 黑曜石雕像
                    self.draw_obsidian_statue(x, y)

    def create_fountain_room(self, room):
        x, y, w, h = room
        # 确保房间足够大
        w = min(w, 7)
        h = min(h, 7)
        # 计算喷泉位置（居中3x3）
        fx = x + (w - 3) // 2
        fy = y + (h - 3) // 2
        # 记录喷泉房间信息
        self.fountain_room = {
            'x1': x, 'y1': y,
            'x2': x + w, 'y2': y + h,
            'center': (fx + 1, fy + 1)
        }
        # 创建喷泉区域
        for i in range(fx, fx + 3):
            for j in range(fy, fy + 3):
                self.maze[j][i] = 2  # 用2表示喷泉区域

    # 新增喷泉瓷砖绘制方法
    def draw_fountain_tile(self, x, y):
        anim_time = pygame.time.get_ticks()
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        # 水池基底
        pygame.draw.rect(self.screen, (30, 144, 255), rect)  # 水池蓝色

        # 动态水波纹效果
        for i in range(3):
            wave_radius = (anim_time % 1000) / 1000 * TILE_SIZE
            alpha = 100 - i * 30
            wave_rect = rect.inflate(-wave_radius + i * 5, -wave_radius + i * 5)
            pygame.draw.ellipse(self.screen, (255, 255, 255, alpha), wave_rect, 2)

        # 中心喷泉特效（仅中心格）
        if (x, y) == self.fountain_room['center']:
            # 水柱粒子
            for _ in range(8):
                px = rect.centerx + random.randint(-8, 8)
                py = rect.centery - random.randint(0, 20)
                pygame.draw.line(self.screen, (255, 255, 255),
                                 (px, py), (px, py - 8), 2)

            # 彩虹光晕
            for i in range(3):
                radius = 15 + i * 5
                color = (255, 165, 0) if i == 0 else (0, 255, 0) if i == 1 else (0, 0, 255)
                alpha_surface = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(alpha_surface, (*color, 50), (radius, radius), radius)
                self.screen.blit(alpha_surface, (rect.centerx - radius, rect.centery - radius))

        # 边缘装饰（仅外围喷泉格）
        elif abs(x - self.fountain_room['center'][0]) == 1 or \
                abs(y - self.fountain_room['center'][1]) == 1:
            # 大理石边缘
            pygame.draw.rect(self.screen, (200, 200, 200), rect, 3)
            # 青铜雕像
            if (x + y) % 2 == 0:
                statue_color = (198, 155, 93)
                # 人鱼雕像
                pygame.draw.ellipse(self.screen, statue_color,
                                    (rect.left + 5, rect.top + 5, 10, 20))  # 身体
                pygame.draw.circle(self.screen, statue_color,
                                   (rect.centerx, rect.top + 15), 4)  # 头部
                # 鱼尾
                pygame.draw.polygon(self.screen, statue_color, [
                    (rect.left + 5, rect.bottom - 5),
                    (rect.centerx, rect.bottom - 10),
                    (rect.right - 5, rect.bottom - 5)
                ])

        # ---------------------- 岩浆房 ----------------------

    def create_lava_room(self, room):
        x, y, w, h = room
        # 确保房间至少7x7
        w = min(w, 7)
        h = min(h, 7)
        # 计算中心位置
        center_x = x + w // 2
        center_y = y + h // 2

        self.lava_room = {
            'x1': x, 'y1': y,
            'x2': x + w, 'y2': y + h,
            'center': (center_x, center_y)
        }

        # 设置区域类型
        for i in range(x, x + w):
            for j in range(y, y + h):
                # 中心1x1为雕像
                if i == center_x and j == center_y:
                    self.maze[j][i] = 4
                # 周围1格为岩浆
                elif abs(i - center_x) <= 1 and abs(j - center_y) <= 1:
                    self.maze[j][i] = 3
                    # 其他区域为地狱地板
                else:
                    self.maze[j][i] = 5

    def draw_lava_tile(self, x, y):
        """绘制岩浆地板 - 简化版本：气泡从内部生成，无竖纹和颜色变化"""
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        anim_time = pygame.time.get_ticks()

        # 为每个特定位置生成固定的随机种子
        position_seed = hash((x, y, self.floor))
        random.seed(position_seed)

        # 确定此位置的气泡特性
        bubble_count = random.randint(3, 5)  # 每个瓦片3-5个气泡
        bubbles = []

        for i in range(bubble_count):
            # 气泡位置 - 现在在岩浆块内部
            bubble_x = random.randint(TILE_SIZE // 4, 3 * TILE_SIZE // 4)
            bubble_y = random.randint(TILE_SIZE // 4, 3 * TILE_SIZE // 4)
            base_size = random.randint(3, 6)  # 基础大小

            # 每个气泡的生命周期随机，确保不同时出现和消失
            cycle_offset = random.randint(0, 2000)
            cycle_duration = random.randint(1500, 2500)  # 气泡周期1.5-2.5秒

            bubbles.append({
                'x': bubble_x,
                'y': bubble_y,
                'base_size': base_size,
                'cycle_offset': cycle_offset,
                'cycle_duration': cycle_duration,
            })

        # 重置随机种子
        random.seed()

        # 岩浆固定颜色 - 无动态变化
        lava_color = (220, 80, 0)  # 统一亮度的岩浆颜色
        pygame.draw.rect(self.screen, lava_color, rect)

        # 绘制底层岩浆纹理 - 静态纹理
        for i in range(4):
            texture_start_x = rect.left + random.randint(5, TILE_SIZE - 10)
            texture_start_y = rect.top + random.randint(5, TILE_SIZE - 10)
            texture_width = random.randint(5, 15)
            texture_height = random.randint(3, 8)

            # 较暗的纹理色
            texture_color = (180, 60, 0)  # 统一的较暗纹理色

            # 绘制不规则纹理块
            pygame.draw.ellipse(self.screen, texture_color,
                                (texture_start_x, texture_start_y, texture_width, texture_height))

        # 绘制岩浆气泡
        for bubble in bubbles:
            # 计算当前气泡周期状态 (0.0 - 1.0)
            bubble_time = (anim_time + bubble['cycle_offset']) % bubble['cycle_duration']
            cycle_position = bubble_time / bubble['cycle_duration']

            # 气泡位置 - 固定在岩浆内部
            current_x = rect.left + bubble['x']
            current_y = rect.top + bubble['y']

            # 气泡生命周期：形成 -> 膨胀 -> 破裂
            if cycle_position < 0.7:  # 形成和膨胀阶段
                # 气泡从小变大
                size_factor = min(1.0, cycle_position / 0.3)  # 前30%时间逐渐形成
                if cycle_position > 0.3:
                    size_factor = 1.0 + (cycle_position - 0.3) * 0.5 / 0.4  # 中间40%时间膨胀

                current_size = bubble['base_size'] * size_factor

                # 气泡颜色 - 较亮
                bubble_color = (255, 150, 50)  # 统一的气泡颜色

                # 绘制气泡主体
                pygame.draw.circle(self.screen, bubble_color,
                                   (int(current_x), int(current_y)),
                                   int(current_size))

                # 气泡高光
                highlight_size = max(1, int(current_size * 0.4))
                highlight_x = current_x - current_size * 0.3
                highlight_y = current_y - current_size * 0.3
                pygame.draw.circle(self.screen, (255, 220, 150),
                                   (int(highlight_x), int(highlight_y)),
                                   highlight_size)

            elif cycle_position < 0.85:  # 破裂阶段 (15%的时间)
                # 破裂进度 (0.0 - 1.0)
                burst_progress = (cycle_position - 0.7) / 0.15

                # 绘制破裂效果 - 渐渐分散的多个小圆
                fragments = 5
                max_spread = bubble['base_size'] * 1.5  # 最大扩散距离

                for i in range(fragments):
                    angle = math.pi * 2 * i / fragments + burst_progress * 0.5  # 随时间略微旋转
                    spread_factor = burst_progress * max_spread

                    # 片段位置
                    frag_x = current_x + math.cos(angle) * spread_factor
                    frag_y = current_y + math.sin(angle) * spread_factor

                    # 片段大小随破裂进度减小
                    frag_size = bubble['base_size'] * (1.0 - burst_progress) * 0.5

                    # 片段颜色
                    frag_color = (255, 150, 50)  # 统一的片段颜色

                    # 绘制破裂片段
                    if frag_size > 0.5:  # 只绘制足够大的片段
                        pygame.draw.circle(self.screen, frag_color,
                                           (int(frag_x), int(frag_y)),
                                           int(frag_size))

                # 气泡破裂时的中心涟漪
                ripple_size = bubble['base_size'] * (0.5 + burst_progress)
                ripple_width = max(1, int(2 * (1.0 - burst_progress)))
                pygame.draw.circle(self.screen, (255, 160, 60),
                                   (int(current_x), int(current_y)),
                                   int(ripple_size),
                                   ripple_width)

    def draw_obsidian_statue(self, x, y):
        """绘制更加生动形象的黑曜石雕像"""
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        current_time = pygame.time.get_ticks()

        # 基础参数
        base_color = (15, 15, 15)  # 深黑色
        lava_color = (255, 80, 0, 180)  # 岩浆颜色
        pulse_factor = 0.5 + 0.5 * math.sin(current_time / 300)  # 脉动系数

        # 雕像主体 - 简化的多边形
        statue_points = [
            (rect.centerx, rect.top + 5),  # 顶部
            (rect.left + 8, rect.centery),  # 左侧
            (rect.left + 10, rect.bottom - 5),  # 左下
            (rect.centerx, rect.bottom - 3),  # 底部
            (rect.right - 10, rect.bottom - 5),  # 右下
            (rect.right - 8, rect.centery)  # 右侧
        ]
        pygame.draw.polygon(self.screen, base_color, statue_points)

        # 岩浆纹路 - 简化的路径
        lava_path = [
            (rect.centerx, rect.top + 15),
            (rect.centerx - 5, rect.centery),
            (rect.centerx, rect.bottom - 8)
        ]

        # 绘制岩浆纹路
        lava_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.lines(lava_surf, lava_color, False, lava_path,
                          max(2, int(3 * pulse_factor)))  # 动态宽度
        self.screen.blit(lava_surf, rect.topleft)

        # 恶魔之眼
        eye_center = (rect.centerx, rect.centery - 5)
        eye_radius = 6

        # 眼睛底色 - 血红色
        pygame.draw.circle(self.screen, (180, 0, 0), eye_center, eye_radius)

        # 眼球 - 随时间小幅移动
        pupil_offset = int(math.sin(current_time / 800) * 2)
        pupil_center = (eye_center[0] + pupil_offset, eye_center[1])
        pygame.draw.circle(self.screen, (0, 0, 0), pupil_center, eye_radius // 2)

        # 眼球高光
        pygame.draw.circle(self.screen, (255, 255, 255),
                           (pupil_center[0] - 1, pupil_center[1] - 1), 1)

        # 顶部恶魔角 - 简化版
        pygame.draw.line(self.screen, base_color,
                         (rect.centerx - 5, rect.top + 8),
                         (rect.centerx - 9, rect.top + 3), 2)
        pygame.draw.line(self.screen, base_color,
                         (rect.centerx + 5, rect.top + 8),
                         (rect.centerx + 9, rect.top + 3), 2)

        # 随机岩浆滴落 - 偶尔出现
        if random.random() < 0.08:
            drop_start = (rect.centerx, rect.bottom - 6)
            drop_end = (rect.centerx, rect.bottom - 1)
            drop_surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            pygame.draw.line(drop_surf, (255, 100, 0, 200), drop_start, drop_end, 2)
            self.screen.blit(drop_surf, rect.topleft)

    def draw_hell_floor(self, x, y):
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        # 为每个地板格子提供唯一且固定的随机种子
        position_seed = hash((x, y, self.floor))
        random.seed(position_seed)

        # 决定此地砖的主要类型
        tile_type = random.choices(['magma_dominant', 'obsidian_dominant', 'mixed'], weights=[0.4, 0.4, 0.2], k=1)[0]

        # 黑曜石结晶参数
        has_obsidian = True if tile_type in ['obsidian_dominant', 'mixed'] else random.random() < 0.3
        num_obsidian = random.randint(2, 4) if tile_type == 'obsidian_dominant' else random.randint(1, 2)

        # 裂纹参数
        num_cracks = random.randint(2, 5)
        crack_features = []
        for _ in range(num_cracks):
            start_x = rect.left + random.randint(2, TILE_SIZE - 2)
            start_y = rect.top + random.randint(2, TILE_SIZE - 2)
            crack_features.append({
                'start': (start_x, start_y),
                'dx': random.randint(-8, 8),
                'dy': random.randint(-8, 8),
                'width': random.randint(1, 2)
            })

        # 黑曜石结晶点
        obsidian_crystals = []
        if has_obsidian:
            for _ in range(num_obsidian):
                crystal_x = rect.left + random.randint(5, TILE_SIZE - 5)
                crystal_y = rect.top + random.randint(5, TILE_SIZE - 5)

                shape_type = random.choice(['polygon', 'shard'])  # 形状类型

                if shape_type == 'polygon':
                    # 多边形黑曜石
                    num_sides = random.randint(4, 7)
                    radius = random.randint(4, 8)
                    angle_offset = random.uniform(0, math.pi * 2)

                    points = []
                    for i in range(num_sides):
                        angle = angle_offset + i * (2 * math.pi / num_sides)
                        r = radius * random.uniform(0.8, 1.2)  # 不规则边缘
                        px = crystal_x + int(math.cos(angle) * r)
                        py = crystal_y + int(math.sin(angle) * r)
                        points.append((px, py))

                    obsidian_crystals.append({
                        'type': 'polygon',
                        'points': points,
                        'color': (20, 20, 25),
                        'highlight': random.random() < 0.7  # 70%几率有高光
                    })
                else:
                    # 锐利碎片形状
                    length = random.randint(5, 10)
                    angle = random.uniform(0, math.pi * 2)

                    # 主轴
                    main_dx = int(math.cos(angle) * length)
                    main_dy = int(math.sin(angle) * length)

                    # 副轴（垂直于主轴）
                    perp_angle = angle + math.pi / 2
                    perp_length = length * random.uniform(0.4, 0.8)
                    perp_dx = int(math.cos(perp_angle) * perp_length)
                    perp_dy = int(math.sin(perp_angle) * perp_length)

                    # 碎片顶点
                    points = [
                        (crystal_x, crystal_y),
                        (crystal_x + main_dx, crystal_y + main_dy),
                        (crystal_x + main_dx + perp_dx, crystal_y + main_dy + perp_dy),
                        (crystal_x + perp_dx, crystal_y + perp_dy)
                    ]

                    obsidian_crystals.append({
                        'type': 'shard',
                        'points': points,
                        'color': (15, 15, 20),
                        'highlight': random.random() < 0.5  # 50%几率有高光
                    })

        # 重置随机种子
        random.seed()

        # 绘制基础地面
        if tile_type == 'magma_dominant':
            base_color = (70, 35, 30)  # 略带红色
        elif tile_type == 'obsidian_dominant':
            base_color = (40, 40, 45)  # 更深灰色带蓝
        else:
            base_color = (60, 35, 35)  # 中性色
        pygame.draw.rect(self.screen, base_color, rect)

        # 绘制裂纹
        for crack in crack_features:
            # 根据地板类型调整裂纹颜色
            if tile_type == 'magma_dominant':
                crack_color = (100, 50, 40)  # 红棕色
            elif tile_type == 'obsidian_dominant':
                crack_color = (40, 40, 50)  # 深蓝灰
            else:
                crack_color = (80, 45, 45)  # 中间色
            pygame.draw.line(self.screen, crack_color,
                             crack['start'],
                             (crack['start'][0] + crack['dx'], crack['start'][1] + crack['dy']),
                             crack['width'])

        # 绘制黑曜石结晶
        for crystal in obsidian_crystals:
            # 绘制主体
            pygame.draw.polygon(self.screen, crystal['color'], crystal['points'])

            # 添加简化的反光/高光效果
            if crystal['highlight']:
                # 找到多边形的质心
                cx = sum(p[0] for p in crystal['points']) / len(crystal['points'])
                cy = sum(p[1] for p in crystal['points']) / len(crystal['points'])

                # 从质心到随机顶点作为高光
                highlight_idx = random.randint(0, len(crystal['points']) - 1)
                highlight_point = crystal['points'][highlight_idx]

                # 绘制高光线
                highlight_color = (60, 60, 70)  # 浅灰色高光
                pygame.draw.line(self.screen, highlight_color,
                                 (cx, cy),
                                 (0.7 * cx + 0.3 * highlight_point[0],
                                  0.7 * cy + 0.3 * highlight_point[1]),
                                 1)

                # 额外的尖锐反光点
                if random.random() < 0.5:
                    random_point = random.choice(crystal['points'])
                    pygame.draw.circle(self.screen, (100, 100, 120),
                                       (int(random_point[0]), int(random_point[1])),
                                       1)

        # ----------------------迷宫墙壁绘画 ----------------------

    def generate_wall_style(self, x, y):
        """生成墙壁的固定样式参数"""
        style_types = ['moss', 'cracked', 'basic', 'basic', 'basic']  # 调整概率分布
        style_type = random.choice(style_types)

        # 固定随机种子以确保可重复性
        seed = hash((x, y, self.floor))
        random.seed(seed)

        if style_type == 'moss':
            return {
                'type': 'moss',
                'moss_pos': [(random.randint(2, TILE_SIZE - 2), random.randint(2, TILE_SIZE - 2))
                             for _ in range(8)]
            }
        elif style_type == 'cracked':
            start = (random.randint(2, TILE_SIZE - 2), random.randint(2, TILE_SIZE - 2))
            end = (start[0] + random.randint(-8, 8), start[1] + random.randint(8, 12))
            return {
                'type': 'cracked',
                'crack_start': start,
                'crack_end': end,
                'small_cracks': [
                    (random.randint(2, TILE_SIZE - 2), random.randint(2, TILE_SIZE - 2))
                    for _ in range(3)
                ]
            }
        else:  # basic
            return {
                'type': 'basic',
                'highlights': [
                    (random.randint(2, TILE_SIZE - 2), random.randint(2, TILE_SIZE - 2))
                    for _ in range(3)
                ]
            }

    def generate_floor_style(self, x, y):
        """生成地板的固定样式参数，与周围墙壁风格相协调"""
        seed = hash((x, y, self.floor))
        random.seed(seed)

        # 检查相邻的墙壁类型，使地板风格与之协调
        wall_count = 0
        wall_types = []

        # 检查周围8个方向的墙壁
        for dx, dy in [(-1, -1), (0, -1), (1, -1), (-1, 0), (1, 0), (-1, 1), (0, 1), (1, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < MAP_WIDTH and 0 <= ny < MAP_HEIGHT and self.maze[ny][nx] == 1:
                wall_count += 1
                if hasattr(self, 'tile_styles') and self.tile_styles[ny][nx]:
                    wall_types.append(self.tile_styles[ny][nx]['type'])

        # 生成基于周围环境的地板样式
        style = {
            'crack_h': random.random() < 0.45,  # 40%概率有水平裂缝
            'crack_v': random.random() < 0.45,  # 40%概率有垂直裂缝
            'stain_pos': (
                random.randint(2, TILE_SIZE - 6),
                random.randint(2, TILE_SIZE - 6)
            ) if random.random() < 0.1 else None,  # 10%概率有污渍
            'wear_pattern': random.choice(['none', 'corner', 'center', 'edge']),  # 磨损模式
            'dust_level': random.random() * 0.5,  # 灰尘等级 (0-0.5)
            'moisture': random.random() < 0.15  # 15%概率显示潮湿
        }

        # 根据周围墙壁类型调整地板外观
        if 'moss' in wall_types:
            style['moss_patches'] = True if random.random() < 0.6 else False  # 60%概率有青苔小块
            style['moss_color'] = (34, 139, 34)  # 青苔颜色

        if 'cracked' in wall_types:
            style['crack_h'] = True if random.random() < 0.7 else style['crack_h']  # 增加裂缝概率
            style['crack_v'] = True if random.random() < 0.7 else style['crack_v']
            style['extra_cracks'] = random.randint(0, 3)  # 额外的小裂缝数量

        # 根据墙壁密度调整地板风格
        if wall_count >= 5:  # 周围墙壁较多，意味着这是一个狭窄区域
            style['dust_level'] += 0.3  # 灰尘更多
            style['wear_pattern'] = 'center'  # 中央磨损（因为中央走的人多）

        # 重置随机种子
        random.seed()
        return style

    def is_position_empty_for_monster(self, x, y, size, occupied):
        """检查目标位置是否为空（没有怪物、道具、墙壁），并且可以容纳怪物的大小"""
        for dx in range(size[0]):
            for dy in range(size[1]):
                if (x + dx, y + dy) in occupied:
                    return False
                if not self.is_walkable(x + dx, y + dy):
                    return False
        return True

    def get_random_tile(self, tiles, occupied):
        available = [pos for pos in tiles if pos not in occupied]
        return random.choice(available) if available else None

    def get_random_tile_for_monster(self, tiles, occupied, size):
        available = []
        for pos in tiles:
            if self.is_position_empty_for_monster(pos[0], pos[1], size, occupied):
                available.append(pos)
        return random.choice(available) if available else None

    def is_walkable(self, x, y):
        return 0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT and self.maze[y][x] in [0, 5]

    def handle_item_pickup(self, item):
        if item.item_type in EQUIPMENT_TYPES:
            equipped_data = EQUIPMENT_TYPES[item.item_type].copy()
            eq_type = EQUIPMENT_TYPES[item.item_type]["type"]
            old_equip = None

            if eq_type == "weapon":
                old_equip = self.player.equipped_weapon
                self.player.equipped_weapon = equipped_data
            elif eq_type == "armor":
                old_equip = self.player.equipped_armor
                self.player.equipped_armor = equipped_data

            if old_equip:
                self.add_message(f"装备了 {item.equipment_data['name']} 替换了 {old_equip['name']}")
            else:
                self.add_message(f"装备了 {item.equipment_data['name']}")
        else:
            # 获取物品稀有度
            rarity = self.item_system.get_item_rarity(item.item_type)
            if item.item_type == "CHEST":
                # 随机金币量基于稀有度和楼层
                gold_multiplier = 1.0
                if rarity == "稀有":
                    gold_multiplier = 1.5
                elif rarity == "罕见":
                    gold_multiplier = 4.0
                elif rarity == "珍贵":
                    gold_multiplier = 6.0

                gold = int(random.randint(5, 150) * self.floor * gold_multiplier)
                self.player.coins += gold
                self.add_message(f"获得 {gold} 金币!")
                return True
            elif item.item_type == "HP_SMALL":
                self.player.hp = min(self.player.hp + 100 * self.floor, self.player.max_hp)
                self.add_message(f"生命药水, HP +{100 * self.floor}")
                return True
            elif item.item_type == "HP_LARGE":
                self.player.hp = min(self.player.hp + 500 * self.floor, self.player.max_hp)
                self.add_message(f"大生命药水, HP +{500 * self.floor}")
                return True
            elif item.item_type == "MP_SMALL":
                self.player.mp = min(self.player.mp + 10 * self.floor, self.player.max_mp)
                self.add_message(f"魔法药水, MP +{10 * self.floor}")
                return True
            elif item.item_type == "MP_LARGE":
                self.player.mp = min(self.player.mp + 50 * self.floor, self.player.max_mp)
                self.add_message(f"大魔法药水, MP +{50 * self.floor}")
                return True
            elif item.item_type == "ATK_GEM":
                atk = random.randint(1, 4) * self.floor
                self.player.base_atk += atk
                self.add_message(f"攻击宝石, ATK +{atk}")
                return True
            elif item.item_type == "DEF_GEM":
                defend = random.randint(1, 4) * self.floor
                self.player.base_defense += defend
                self.add_message(f"防御宝石, DEF +{defend}")
                return True
            elif item.item_type == "ATK_GEM_LARGE":
                atk = random.randint(5, 10) * self.floor
                self.player.base_atk += atk
                self.add_message(f"大攻击宝石, ATK +{atk}")
                return True
            elif item.item_type == "DEF_GEM_LARGE":
                defend = random.randint(5, 10) * self.floor
                self.player.base_defense += defend
                self.add_message(f"大防御宝石, DEF +{defend}")
                return True

    def check_player_attack(self):
        # 获取攻击范围内的所有怪物
        targets = []
        for monster in self.monsters:
            distance = self.calculate_distance(
                (self.player.x, self.player.y),
                (monster.x, monster.y)
            )
            if distance <= self.player.attack_range:
                targets.append(monster)

        if targets:
            # 攻击所有在范围内的目标
            for target in targets:
                self.perform_attack(attacker=self.player, defender=target)
            self.player.attack_cooldown = 1.0 / self.player.attack_speed
            # 触发攻击动画
            self.show_attack_animation(self.player)

    def check_monster_attack(self, monster):
        # 计算与玩家的距离
        distance = self.calculate_distance(
            (monster.x, monster.y),
            (self.player.x, self.player.y)
        )

        if distance <= monster.attack_range:
            self.perform_attack(attacker=monster, defender=self.player)
            monster.attack_cooldown = 1.0 / monster.attack_speed
            # 触发攻击动画
            self.show_attack_animation(monster)
        if monster.hp <= 0:
            self.monsters.remove(monster)
    def calculate_distance(self, pos1, pos2):
        # 使用曼哈顿距离
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def perform_attack(self, attacker, defender):
        # 计算实际攻击属性
        if isinstance(attacker, Player):
            atk = attacker.atk * (0.6 if self.gold_fear or self.blue_fear or self.red_fear else 1)
            defense_type = 'defense'
        else:
            atk = attacker.atk
            defense_type = 'defense'  # 可根据需要区分物理/魔法防御

        # 计算伤害
        damage = max(0, atk - getattr(defender, defense_type, 0) * random.uniform(0.4, 1.6))
        damage = int(damage * random.uniform(0.6, 1.4))  # 加入随机浮动

        # 应用伤害
        defender.hp = max(0, defender.hp - damage)

        # 处理装备耐久
        if isinstance(attacker, Player):
            # 减少武器耐久
            if attacker.equipped_weapon:
                attacker.equipped_weapon["durability"] -= 1
                if attacker.equipped_weapon["durability"] <= 0:
                    self.add_message(f"{attacker.equipped_weapon['name']} 已损坏！")
                    attacker.equipped_weapon = None
        elif isinstance(defender, Player):
            # 减少护甲耐久
            if defender.equipped_armor:
                defender.equipped_armor["durability"] -= 1
                if defender.equipped_armor["durability"] <= 0:
                    self.add_message(f"{defender.equipped_armor['name']} 已损坏！")
                    defender.equipped_armor = None

        # 显示战斗信息
        if isinstance(attacker, Player):
            self.add_message(f"你对{defender.name}造成{damage}点伤害！")
            if defender.hp <= 0:
                self.add_message(f"击败{defender.name}，获得{defender.coin}金币")
                self.player.coins += defender.coin
        else:
            self.add_message(f"{attacker.name}对你造成{damage}点伤害！")
            if self.player.hp <= 0:
                self.game_state = "dead"
                self.death_screen = DeathScreen(self.screen, self.player, self.floor)

    def show_attack_animation(self, attacker):
        # 根据攻击者类型显示不同动画
        if isinstance(attacker, Player):
            # 玩家攻击动画
            self.skill_effects.append(WeaponSwingEffect(
                attacker.x, attacker.y,
                duration=0.2
            ))
        else:
            # 怪物攻击动画
            if "远程" in attacker.name:
                self.skill_effects.append(ProjectileEffect(
                    start=(attacker.x, attacker.y),
                    end=(self.player.x, self.player.y),
                    speed=500,
                    damage=attacker.atk
                ))
            else:
                self.skill_effects.append(ClawEffect(
                    attacker.x, attacker.y,
                    direction=(self.player.x - attacker.x,
                               self.player.y - attacker.y)
                ))

    def update(self):
        if self.is_animating:
            return  # 动画期间不更新游戏逻辑
        dt = self.clock.get_time() / 1000  # 获取每帧时间（秒）

        # 更新攻击冷却
        self.player.attack_cooldown = max(0, self.player.attack_cooldown - dt)
        for monster in self.monsters:
            monster.attack_cooldown = max(0, monster.attack_cooldown - dt)

        # 玩家技能释放冷却
        for skill in self.player.skills.values():
            if skill['current_cd'] > 0:
                skill['current_cd'] -= dt

        # ------------------------- 玩家攻击逻辑 -------------------------
        if self.player.attack_cooldown <= 0:
            self.check_player_attack()

        # ------------------------- 怪物攻击逻辑 -------------------------
        for monster in self.monsters:
            if monster.attack_cooldown <= 0:
                self.check_monster_attack(monster)

        # ------------------------- 路径特效更新 -------------------------
        self.set_path_effect()

        # ------------------------- 技能特效更新 -------------------------

        self.red_fear = False  # 血腥恐惧debuff
        self.blue_fear = False  # 血腥恐惧debuff
        self.gold_fear = False  # 血腥恐惧debuff
        # 更新所有技能特效
        for effect in self.skill_effects[:]:
            if isinstance(effect, (WeaponSwingEffect,
                                   ProjectileEffect, ClawEffect)):
                if not effect.update(dt):
                    self.skill_effects.remove(effect)
            elif isinstance(effect, IceBreathEffect):
                if not effect.update(dt):
                    self.skill_effects.remove(effect)
            elif isinstance(effect, PoisonBall):
                if effect.update(dt):
                    self.skill_effects.remove(effect)
                    # 触发中毒效果
                    self.player_debuff['poison_end'] = pygame.time.get_ticks() + 5000  # 5秒中毒
            elif isinstance(effect, CrackEffect):
                if not effect.update(dt):
                    self.skill_effects.remove(effect)
            elif isinstance(effect, ElectricEffect):
                if not effect.update(dt):
                    self.skill_effects.remove(effect)
            elif isinstance(effect, HolyBeamEffect):
                if not effect.update(dt):
                    self.skill_effects.remove(effect)
            elif isinstance(effect, FireStrikeEffect):
                if not effect.update(dt):
                    self.skill_effects.remove(effect)
            elif isinstance(effect, BlueFireStrikeEffect):
                if not effect.update(dt):
                    self.skill_effects.remove(effect)
            elif isinstance(effect, LightningEffect):
                if not effect.update(dt):
                    self.skill_effects.remove(effect)
            elif isinstance(effect, HolyBallEffect):
                still_active, damage_results = effect.update(dt, self.monsters)
                # Apply damage to monsters
                for monster, damage_multiplier in damage_results:
                    if monster in self.monsters:  # Ensure monster still exists
                        dmg = self.player.atk * damage_multiplier
                        actual_damage = max(dmg - monster.defense, 0)
                        monster.hp -= actual_damage
                        self.add_message(f"神圣球对{monster.name}造成{actual_damage}点伤害！")

                if not still_active:
                    self.skill_effects.remove(effect)

            elif isinstance(effect, TripleAttack):
                still_active, damage_results = effect.update(dt, self.monsters)

                for monster, damage_multiplier in damage_results:
                    if monster in self.monsters:  # Ensure monster still exists
                        dmg = self.player.atk * damage_multiplier
                        actual_damage = max(dmg - monster.defense, 0)
                        monster.hp -= actual_damage

                        if damage_multiplier == 0.8:
                            self.add_message(f"三连斩·一段 对{monster.name}造成{actual_damage}点伤害！")
                        elif damage_multiplier == 1.0:
                            self.add_message(f"三连斩·二段 对{monster.name}造成{actual_damage}点伤害！")
                        elif damage_multiplier == 1.5:
                            self.add_message(f"三连斩·终结 对{monster.name}造成{actual_damage}点伤害！")
                        else:
                            self.add_message(f"三连斩 对{monster.name}造成{actual_damage}点伤害！")

                if not still_active:
                    self.skill_effects.remove(effect)

        # ------------------------- 更新怪物移动 -------------------------
        self.update_monsters(dt)

        # ------------------- 召唤物更新 ------------------------------
        self.guardian_lightning_balls = [ball for ball in self.guardian_lightning_balls if ball.update(dt, self)] # 更新守护闪电球

        # ------------------------- 腐蚀效果更新 -------------------------
        # 在怪物移动添加腐蚀痕迹生成
        for monster in self.monsters[:]:
            if "腐蚀怪" in monster.name:
                # 添加新痕迹（限制最多100个注意不同实体不同）
                new_effect = CorrosionEffect(monster.x, monster.y)
                self.corrosion_effects.append(new_effect)
                if len(self.corrosion_effects) > 10000:
                    self.corrosion_effects.pop(0)

        # 更新腐蚀效果
        current_time = pygame.time.get_ticks()
        self.corrosion_effects = [effect for effect in self.corrosion_effects if effect.update(current_time)]

        # 检测玩家是否在腐蚀区域
        self.player_debuff['in_corrosion'] = any(
            effect.x == self.player.x and effect.y == self.player.y
            for effect in self.corrosion_effects
        )
        # 腐蚀区域扣血（每秒50 * FLOOR 点）
        if self.player_debuff['in_corrosion'] and current_time % 1000 < 50:
            self.player.hp -= 50 * self.floor
            self.add_message(f"腐蚀区域造成 {50 * self.floor} 点伤害！")

        # ------------------------- 怪物技能逻辑 -------------------------
        for monster in self.monsters:
            # 闪电BOSS技能
            if "闪电" in monster.name:
                distance = max(abs(self.player.x - monster.x), abs(self.player.y - monster.y))
                if distance <= 6:
                    if "纯青" in monster.name:
                        self.blue_fear = True
                    elif "金色" in monster.name:
                        self.gold_fear = True
                    elif "血腥" in monster.name:
                        self.red_fear = True
                    # 持续伤害
                    if pygame.time.get_ticks() % 1000 < 30:
                        self.player.hp -= 80
                continue

            # 闪电球技能
            elif "电击球" in monster.name:
                monster.skill_cd -= dt
                dist = abs(self.player.x - monster.x) + abs(self.player.y - monster.y)
                if dist <= monster.electric_range and monster.skill_cd <= 0:
                    # 计算伤害
                    damage = random.randint(monster.atk, monster.atk * 2)
                    self.player.hp -= max(damage - self.player.defense, 0)
                    self.add_message(f"电击球电击造成 {max(damage - self.player.defense, 0)} 伤害！")
                    # 设置麻痹效果
                    self.player_debuff['paralyze_end'] = pygame.time.get_ticks() + 1000
                    monster.skill_cd = monster.electric_cd
                    # 添加电击特效
                    self.skill_effects.append(ElectricEffect(self.player.x, self.player.y))
                continue

            # 魔王技能
            elif "魔王" in monster.name:
                monster.skill_cd -= dt
                dist = abs(self.player.x - monster.x) + abs(self.player.y - monster.y)
                if dist <= monster.crack_range and monster.skill_cd <= 0:
                    # 触发地裂技能
                    self.add_message("魔王使用了地裂技能！")
                    # 对玩家造成伤害
                    self.player.hp -= monster.crack_damage
                    self.add_message(f"受到 {monster.crack_damage} 点伤害！")
                    if self.player.hp <= 0:
                        self.player.hp = 0
                        self.add_message("你被锤成肉泥！游戏结束！")
                        self.game_state = "dead"
                        self.death_screen = DeathScreen(self.screen, self.player, self.floor)
                    # 眩晕效果
                    self.player_debuff['stun_end'] = pygame.time.get_ticks() + monster.stun_duration * 1000
                    # 重置技能冷却
                    monster.skill_cd = monster.crack_cd
                    # 绘制地裂效果
                    self.skill_effects.append(CrackEffect(self.player.x, self.player.y, 3))
                continue

            # 冰霜巨龙技能
            elif "冰霜巨龙" in monster.name:
                monster.skill_cd -= dt
                # 计算精确距离和方向
                dx = self.player.x - monster.x
                dy = self.player.y - monster.y
                dist = math.hypot(dx, dy)  # 使用欧几里得距离

                if dist <= monster.breath_range and monster.skill_cd <= 0:
                    # 计算吐息方向（单位向量）
                    if dist == 0:
                        direction = (1, 0)  # 防止除零错误
                    else:
                        direction = (dx / dist, dy / dist)
                    # 创建吐息效果
                    mouth_pos = (monster.x * TILE_SIZE + TILE_SIZE * 1.5,
                                 monster.y * TILE_SIZE + TILE_SIZE // 2)
                    self.skill_effects.append(IceBreathEffect(mouth_pos, direction))
                    monster.skill_cd = monster.breath_cd
                    self.add_message("冰霜巨龙使用冰霜吐息!")
                    # 对玩家造成伤害
                    self.player.hp -= monster.ice_damage
                    self.add_message(f"受到 {monster.ice_damage} 点伤害！")
                    if self.player.hp <= 0:
                        self.player.hp = 0
                        self.add_message("你被冰封！游戏结束！")
                        self.game_state = "dead"
                        self.death_screen = DeathScreen(self.screen, self.player, self.floor)
                continue

            # 魔法师技能
            elif "魔法师" in monster.name:
                monster.skill_cd -= dt
                dist = abs(self.player.x - monster.x) + abs(self.player.y - monster.y)
                if dist <= monster.magic_range and monster.skill_cd <= 0:
                    # 发射毒球
                    start = (monster.x * TILE_SIZE + TILE_SIZE // 2,
                             monster.y * TILE_SIZE + TILE_SIZE // 2)
                    target = (self.player.x * TILE_SIZE + TILE_SIZE // 2,
                              self.player.y * TILE_SIZE + TILE_SIZE // 2)
                    self.skill_effects.append(PoisonBall(start, target))
                    monster.skill_cd = monster.magic_cd
                    self.add_message("魔法师发射了毒液法术！")

            elif "火焰领主" in monster.name:
                monster.skill_cd -= dt
                dist = abs(self.player.x - monster.x) + abs(self.player.y - monster.y)
                if dist <= monster.strike_range and monster.skill_cd <= 0:
                    # 触发熔岩重击
                    if "纯" in monster.name:
                        self.skill_effects.append(BlueFireStrikeEffect(
                            self.player.x, self.player.y, 3))
                    else:
                        self.skill_effects.append(FireStrikeEffect(
                            self.player.x, self.player.y, 3))
                    self.player.hp -= monster.strike_damage
                    if "纯" in monster.name:
                        self.add_message(f"纯火焰领主发动纯青熔岩重击！")
                    else:
                        self.add_message(f"火焰领主发动熔岩重击！")
                    self.add_message(f"造成{monster.strike_damage}伤害！")
                    # 附加燃烧效果
                    self.player_debuff['poison_end'] = pygame.time.get_ticks() + 3000
                    monster.skill_cd = monster.strike_cd

            elif "神圣灾祸骑士" in monster.name:
                # 初始化技能冷却属性（如果不存在）
                if not hasattr(monster, 'holy_ball_cd'):
                    monster.holy_ball_cd = 0
                    monster.summon_ball_cd = 0
                    monster.heal_pulse_cd = 0
                    monster.holy_ball_range = 8
                    monster.holy_damage = monster.atk * 2
                    monster.heal_range = 8
                    monster.heal_amount = 100 * self.floor  # 每次恢复量

                # 更新技能冷却
                monster.holy_ball_cd = max(0, monster.holy_ball_cd - dt)
                monster.summon_ball_cd = max(0, monster.summon_ball_cd - dt)
                monster.heal_pulse_cd = max(0, monster.heal_pulse_cd - dt)

                # 计算与玩家距离
                dist = abs(self.player.x - monster.x) + abs(self.player.y - monster.y)

                # 使用神圣球技能
                if dist <= monster.holy_ball_range and monster.holy_ball_cd <= 0:
                    # 创建效果实例 - 显式标记为怪物技能并传入玩家为目标
                    effect = HolyBallEffect(
                        player_pos=(monster.x + 1, monster.y + 1),  # 从怪物中心位置发射
                        ball_count=monster.num_balls,
                        seek_range=monster.holy_ball_range,
                        damage_multiplier=1.5,
                        is_monster_skill=True,  # 标记为怪物技能
                        target=self.player,  # 传入玩家为目标
                        monster=monster  # 传入怪物自身以计算伤害
                    )
                    # 添加消息发送方法，以便在适当时机显示消息
                    effect.add_message = self.add_message

                    # 添加到技能效果列表
                    self.skill_effects.append(effect)
                    self.add_message("神圣灾祸骑士释放了神圣球！")

                    # 设置冷却时间
                    monster.holy_ball_cd = 6.0  # 6秒冷却

                # 使用神圣守护技能
                if dist <= monster.holy_ball_range * 1.5 and monster.summon_ball_cd <= 0:
                    # 创建围绕怪物自身的神圣光球，显式标记为怪物技能
                    holy_guardian = SummonHolyBall(
                        owner=monster,  # 怪物作为拥有者
                        ball_count=monster.num_balls,
                        duration=12.0,
                        attack_range=6,
                        attack_speed=1.0,
                        damage_multiple=1.0,
                        heal_percent=0,  # 怪物不需要治疗自己
                        is_monster_skill=True,  # 标记为怪物技能
                        target=self.player  # 传入玩家为目标
                    )

                    # 添加到守护球列表
                    self.guardian_lightning_balls.append(holy_guardian)
                    self.add_message("神圣灾祸骑士召唤了神圣守护光环！")

                    # 设置冷却时间
                    monster.summon_ball_cd = 15.0  # 15秒冷却

                # 治疗周围的友军
                if monster.heal_pulse_cd <= 0:
                    healed = False
                    # 检查周围的友军
                    for other_monster in self.monsters:
                        if other_monster is not monster:  # 不包括自己
                            distance = abs(monster.x - other_monster.x) + abs(monster.y - other_monster.y)
                            if distance <= monster.heal_range:
                                # 治疗友军
                                other_monster.hp = min(other_monster.hp + monster.heal_amount,
                                                       other_monster.hp * 1.5)  # 最多恢复到1.5倍初始血量
                                healed = True

                                # 添加治疗粒子效果
                                for _ in range(5):
                                    self.fear_particles.append({
                                        'pos': [other_monster.x * TILE_SIZE + TILE_SIZE // 2,
                                                other_monster.y * TILE_SIZE + TILE_SIZE // 2],
                                        'vel': [random.uniform(-2, 2), random.uniform(-5, -2)],
                                        'life': random.uniform(0.5, 1.0),
                                        'max_life': 1.0,
                                        'size': random.uniform(2, 4),
                                        'color': (255, 255, 200)  # 金色粒子
                                    })

                    if healed:
                        self.add_message("神圣灾祸骑士为周围怪物注入了神圣能量！")

                    # 设置治疗脉冲冷却
                    monster.heal_pulse_cd = 7.0  # 7秒冷却



        # ----------------- 更新粒子效果 ---------------------------
        for p in self.fear_particles[:]:
            p['pos'][0] += p['vel'][0]
            p['pos'][1] += p['vel'][1]
            p['life'] -= dt
            if p['life'] <= 0:
                self.fear_particles.remove(p)

        # ------------------------- 玩家状态检测 -------------------------
        current_time = pygame.time.get_ticks()
        # 寒冰区域检测
        player_pos = (self.player.x, self.player.y)
        frozen = False
        for effect in self.skill_effects:
            if isinstance(effect, IceBreathEffect) and player_pos in effect.area:
                frozen = True
                # 持续伤害
                if current_time % 1000 < dt * 1000:  # 每秒扣血
                    self.player.hp -= 100
                    self.add_message("受到寒冰侵蚀 HP-100！")
                    if self.player.hp <= 0:
                        self.player.hp = 0
                        self.add_message("你被寒冰吞噬！游戏结束！")
                        self.game_state = "dead"
                        self.death_screen = DeathScreen(self.screen, self.player, self.floor)
        self.player_debuff['frozen_area'] = frozen

        # 中毒效果
        if current_time < self.player_debuff['poison_end']:
            if current_time % 500 < dt * 1000:  # 每0.5秒扣血
                self.player.hp *= 0.95
                self.add_message(f"毒性发作 HP-{0.05 * self.player.hp}！")
                # 死亡检查
                if self.player.hp <= 0:
                    self.player.hp = 0
                    self.add_message("你已中毒身亡！游戏结束！")
                    self.game_state = "dead"
                    self.death_screen = DeathScreen(self.screen, self.player, self.floor)

        # ------------------------- 其他逻辑 -------------------------
        # 原有楼层切换和物品拾取逻辑
        if (self.player.x, self.player.y) == self.exit_pos:
            self.floor += 1
            self.clear_dynamic()
            self.item_system.update_floor_bonus(self.floor) # 楼层物品掉落偏好
            self.generate_floor()
            self.player.x, self.player.y = self.start_pos
            self.add_message(f"进入第 {self.floor} 层")

        for item in self.items[:]:
            if (self.player.x, self.player.y) == (item.x, item.y):
                self.handle_item_pickup(item)
                self.items.remove(item)


        # 怪物死亡检测
        for monster in self.monsters[:]:
            if monster.hp <= 0:
                self.add_message(f"击败{monster.name}，获得{monster.coin}金币")
                self.player.coins += monster.coin
                self.monsters.remove(monster)

        # 更新附近怪物列表
        self.nearby_monsters = []
        for monster in self.monsters:
            distance = abs(monster.x - self.player.x) + abs(monster.y - self.player.y)
            if distance <= 5:
                self.nearby_monsters.append(monster)



        # 喷泉房间生成史莱姆
        if self.fountain_room and self.player_in_fountain_room():
            current_time = pygame.time.get_ticks()
            if current_time - self.last_spawn_time > FOUNTAIN_SPAWN_INTERVAL:
                self.spawn_slime()
                self.last_spawn_time = current_time

        # 岩浆房伤害
        if self.lava_room and self.player_in_lava_room():
            if (self.player.x, self.player.y) in self.get_lava_tiles():
                self.player.hp -= LAVA_DAMAGE * dt
                if self.player.hp <= 0:
                    self.game_state = "dead"
                    self.death_screen = DeathScreen(self.screen, self.player, self.floor)

            # 生成红色史莱姆
            current_time = pygame.time.get_ticks()
            if current_time - self.last_lava_spawn > LAVA_SPAWN_INTERVAL:
                self.spawn_red_slime()
                self.last_lava_spawn = current_time

    def player_in_lava_room(self):
        if not self.lava_room:
            return False
        fr = self.lava_room
        return (fr['x1'] <= self.player.x < fr['x2'] and
                fr['y1'] <= self.player.y < fr['y2'])

    def get_lava_tiles(self):
        tiles = []
        for x in range(self.lava_room['x1'], self.lava_room['x2']):
            for y in range(self.lava_room['y1'], self.lava_room['y2']):
                if abs(x - self.lava_room['center'][0]) <= 1 and \
                        abs(y - self.lava_room['center'][1]) <= 1:
                    tiles.append((x, y))
        return tiles

    def spawn_red_slime(self):
        slime_data = next(m for m in monsters_data if m["name"] == "红史莱姆")
        fr = self.lava_room
        for _ in range(10):  # 一次生成3只
            x = random.randint(fr['x1'], fr['x2'] - 1)
            y = random.randint(fr['y1'], fr['y2'] - 1)
            if self.is_position_empty(x, y):
                self.monsters.append(Monster(x, y, slime_data, self.floor))
                self.add_message("岩浆中涌出了红色史莱姆！")
                break
    def player_in_fountain_room(self):
        if not self.fountain_room:
            return False
        fr = self.fountain_room
        return (fr['x1'] <= self.player.x < fr['x2'] and
                fr['y1'] <= self.player.y < fr['y2'])

    def spawn_slime(self):
        slime_data = monsters_data[6]
        # 寻找可用位置
        fr = self.fountain_room
        for _ in range(10):  # 最多尝试10次
            x = random.randint(fr['x1'], fr['x2'] - 1)
            y = random.randint(fr['y1'], fr['y2'] - 1)
            if self.is_position_empty(x, y) and self.maze[y][x] == 0:
                # 创建绿色史莱姆
                self.monsters.append(Monster(x, y, slime_data, self.floor))
                self.add_message("喷泉中涌出了绿色史莱姆！")
                break

    def add_message(self, message):
        self.message_log.append(message)
        if len(self.message_log) > self.max_log_lines:
            self.message_log.pop(0)

    def draw_stairs(self, screen, x, y, tile_size):
        # 获取当前动画时间
        anim_time = pygame.time.get_ticks()

        # ------ 基础背景 - 增加识别度 ------
        # 整个区域先绘制一个明显的底色
        bg_rect = pygame.Rect(x, y, tile_size, tile_size)
        pygame.draw.rect(screen, (100, 100, 170), bg_rect)  # 蓝紫色背景
        pygame.draw.rect(screen, (120, 120, 190), bg_rect, 3)  # 亮色边框

        # ------ 楼梯主体结构 - 更加突出 ------
        step_count = 5  # 增加台阶数量
        step_height = tile_size // 6

        # 明亮的台阶颜色
        step_color = (220, 220, 250)  # 亮色台阶
        step_border = (150, 150, 220)  # 边框色

        # 绘制台阶序列 - 清晰可见
        for i in range(step_count):
            # 明确的阶梯状结构
            step_width = tile_size - (i * tile_size // 12)  # 逐渐变窄的台阶
            step_x = x + (tile_size - step_width) // 2
            step_y = y + tile_size - (i + 1) * step_height - 5

            # 绘制凸起的台阶
            pygame.draw.rect(screen, step_color, (step_x, step_y, step_width, step_height))
            pygame.draw.rect(screen, step_border, (step_x, step_y, step_width, step_height), 1)

        # ------ 添加两侧微小火把效果 ------
        torch_size = tile_size // 6  # 火把大小

        # 在楼梯两侧各添加一个火把
        for side in [-1, 1]:  # 左右两侧
            # 火把位置
            torch_x = x + tile_size // 2 + side * (tile_size // 3)
            torch_y = y + tile_size - step_count * step_height + 5

            # 绘制火把柄
            pygame.draw.rect(screen, (90, 70, 60),
                             (torch_x - 1, torch_y, 3, torch_size))

            # 火焰动画效果 - 使用时间制作火焰抖动
            flame_offset = math.sin(anim_time / 100) * 1.5
            flame_size = torch_size + int(math.sin(anim_time / 200) * 2)

            # 绘制火焰底部 - 较大的橙色基础
            pygame.draw.circle(screen, (230, 120, 20),
                               (int(torch_x + flame_offset), int(torch_y - 2)),
                               flame_size // 2)

            # 绘制火焰中部 - 较小的亮橙色
            pygame.draw.circle(screen, (250, 170, 30),
                               (int(torch_x + flame_offset * 0.8), int(torch_y - 3)),
                               max(2, flame_size // 3))

            # 绘制火焰顶部 - 最小的黄色火焰尖
            pygame.draw.circle(screen, (255, 220, 50),
                               (int(torch_x + flame_offset * 0.5), int(torch_y - 4)),
                               max(1, flame_size // 4))

            # 添加火焰光晕效果
            glow_radius = flame_size
            glow_surf = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            for radius in range(glow_radius, 0, -1):
                alpha = max(0, min(150, int(100 * (radius / glow_radius))))
                pygame.draw.circle(glow_surf, (255, 180, 50, alpha),
                                   (glow_radius, glow_radius), radius)

            # 绘制光晕
            screen.blit(glow_surf,
                        (int(torch_x - glow_radius + flame_offset),
                         int(torch_y - glow_radius - 2)))

            # 火星效果 - 随机生成几个小火星
            if random.random() < 0.3:  # 30%概率生成火星
                for _ in range(2):
                    spark_x = torch_x + random.uniform(-2, 2) + flame_offset
                    spark_y = torch_y - random.uniform(2, 6)
                    spark_size = random.uniform(0.5, 1.5)
                    spark_alpha = random.randint(100, 200)

                    # 绘制火星
                    spark_surf = pygame.Surface((4, 4), pygame.SRCALPHA)
                    pygame.draw.circle(spark_surf, (255, 200, 50, spark_alpha),
                                       (2, 2), spark_size)
                    screen.blit(spark_surf, (int(spark_x - 2), int(spark_y - 2)))


    # ----------------- 墙壁绘制方法 ---------------------------
    def draw_wall(self, x, y, surface=None):
        """使用预先生成的样式绘制立体墙壁，添加凸起、凹陷和不规则边缘效果"""
        surface = surface or self.screen
        style = self.tile_styles[y][x]
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        # 为每个墙体生成一个稳定的随机种子，确保同一位置的墙体外观一致
        wall_seed = hash((x, y, self.floor))
        random.seed(wall_seed)

        # 墙体基础颜色 - 随机化程度略增
        base_color = (
            max(25, min(55, COLOR_STONE[0] + random.randint(-8, 8))),
            max(25, min(55, COLOR_STONE[1] + random.randint(-8, 8))),
            max(25, min(55, COLOR_STONE[2] + random.randint(-8, 8)))
        )

        # 填充基础深色背景 - 带有微妙的噪点
        darker_base = (max(15, base_color[0] - 15), max(15, base_color[1] - 15), max(15, base_color[2] - 15))
        pygame.draw.rect(surface, darker_base, rect)

        # 添加纹理噪点
        for _ in range(12):
            noise_x = rect.left + random.randint(0, TILE_SIZE - 1)
            noise_y = rect.top + random.randint(0, TILE_SIZE - 1)
            noise_color = (darker_base[0] + random.randint(-5, 5),
                           darker_base[1] + random.randint(-5, 5),
                           darker_base[2] + random.randint(-5, 5))
            pygame.draw.rect(surface, noise_color, (noise_x, noise_y, 1, 1))

        # 添加随机石块 - 更不规则的形状
        num_stones = random.randint(4, 7)  # 增加石块数量
        used_area = []  # 记录已使用的区域

        for _ in range(num_stones):
            # 随机石块尺寸 (更多变化)
            stone_width = random.randint(TILE_SIZE // 4, TILE_SIZE // 2 + 2)
            stone_height = random.randint(TILE_SIZE // 4, TILE_SIZE // 2 + 2)

            # 随机位置 (尝试12次找到不重叠的位置)
            for attempt in range(12):
                stone_x = rect.left + random.randint(-2, TILE_SIZE - stone_width + 2)  # 允许稍微超出边界
                stone_y = rect.top + random.randint(-2, TILE_SIZE - stone_height + 2)
                stone_rect = pygame.Rect(stone_x, stone_y, stone_width, stone_height)

                # 检查是否与已有石块重叠太多
                overlap = False
                for used in used_area:
                    if stone_rect.colliderect(used) and (
                            stone_rect.width * stone_rect.height > 0.6 * used.width * used.height):
                        overlap = True
                        break

                if not overlap or attempt == 11:  # 第12次尝试强制放置
                    used_area.append(stone_rect)

                    # 更明显的随机化石块颜色
                    stone_color_var = random.randint(-15, 15)
                    stone_color = (
                        max(25, min(75, base_color[0] + stone_color_var)),
                        max(25, min(75, base_color[1] + stone_color_var)),
                        max(25, min(75, base_color[2] + stone_color_var))
                    )

                    # 圆角矩形模拟石块，边缘更不规则
                    border_radius = random.randint(1, 5)  # 更多样的圆角半径

                    # 添加不规则性: 微妙的凹凸变形
                    if random.random() < 0.4:  # 40%的石块有不规则边缘
                        # 绘制基础石块
                        pygame.draw.rect(surface, stone_color, stone_rect, border_radius=border_radius)

                        # 添加凹凸不平的边缘效果
                        edge_count = random.randint(2, 4)
                        for i in range(edge_count):
                            edge_x = stone_rect.left + random.randint(0, stone_rect.width)
                            edge_y = stone_rect.top + random.randint(0, stone_rect.height)

                            # 只在边缘附近添加变形
                            distance_to_edge = min(
                                abs(edge_x - stone_rect.left),
                                abs(edge_x - stone_rect.right),
                                abs(edge_y - stone_rect.top),
                                abs(edge_y - stone_rect.bottom)
                            )

                            if distance_to_edge < 5:  # 只在边缘5像素内添加变形
                                # 随机突起或凹陷
                                bump_size = random.randint(1, 3)
                                if random.random() < 0.5:  # 突起
                                    bump_color = (min(255, stone_color[0] + 10),
                                                  min(255, stone_color[1] + 10),
                                                  min(255, stone_color[2] + 10))
                                else:  # 凹陷
                                    bump_color = (max(0, stone_color[0] - 10),
                                                  max(0, stone_color[1] - 10),
                                                  max(0, stone_color[2] - 10))
                                pygame.draw.circle(surface, bump_color, (edge_x, edge_y), bump_size)
                    else:
                        # 普通石块
                        pygame.draw.rect(surface, stone_color, stone_rect, border_radius=border_radius)

                    # 添加石块高光 (左上) - 更自然的边缘光效
                    highlight_width = random.randint(1, 2)
                    highlight_alpha = random.randint(60, 120)
                    highlight_color = (min(255, COLOR_HIGHLIGHT[0] + random.randint(-10, 10)),
                                       min(255, COLOR_HIGHLIGHT[1] + random.randint(-10, 10)),
                                       min(255, COLOR_HIGHLIGHT[2] + random.randint(-10, 10)))

                    # 高光不一定完整覆盖边缘
                    high_len1 = random.randint(int(stone_rect.width * 0.3), int(stone_rect.width * 0.9))
                    high_len2 = random.randint(int(stone_rect.height * 0.3), int(stone_rect.height * 0.9))

                    pygame.draw.line(surface, highlight_color,
                                     (stone_rect.left + border_radius, stone_rect.top + border_radius),
                                     (stone_rect.left + border_radius + high_len1, stone_rect.top + border_radius),
                                     highlight_width)
                    pygame.draw.line(surface, highlight_color,
                                     (stone_rect.left + border_radius, stone_rect.top + border_radius),
                                     (stone_rect.left + border_radius, stone_rect.top + border_radius + high_len2),
                                     highlight_width)

                    # 添加石块阴影 (右下) - 不均匀阴影
                    shadow_width = random.randint(1, 2)
                    shadow_alpha = random.randint(80, 140)
                    shadow_color = (max(0, COLOR_SHADOW[0] + random.randint(-10, 10)),
                                    max(0, COLOR_SHADOW[1] + random.randint(-10, 10)),
                                    max(0, COLOR_SHADOW[2] + random.randint(-10, 10)))

                    # 阴影也不完全规则
                    shadow_len1 = random.randint(int(stone_rect.width * 0.4), int(stone_rect.width * 0.9))
                    shadow_len2 = random.randint(int(stone_rect.height * 0.4), int(stone_rect.height * 0.9))

                    pygame.draw.line(surface, shadow_color,
                                     (stone_rect.left + border_radius, stone_rect.bottom - border_radius),
                                     (stone_rect.left + border_radius + shadow_len1, stone_rect.bottom - border_radius),
                                     shadow_width)
                    pygame.draw.line(surface, shadow_color,
                                     (stone_rect.right - border_radius, stone_rect.top + border_radius),
                                     (stone_rect.right - border_radius, stone_rect.top + border_radius + shadow_len2),
                                     shadow_width)

                    break  # 放置成功，跳出尝试循环

        # 根据预生成样式添加特殊效果
        if style['type'] == 'moss':
            self.draw_moss_stone_enhanced(x, y, style, surface, used_area)
        elif style['type'] == 'cracked':
            self.draw_cracked_stone_enhanced(x, y, style, surface, used_area)
        else:
            self.draw_basic_stone_enhanced(x, y, style, surface, used_area)

        # 石块缝隙细节 - 增加不规则的砂浆填充
        self._add_mortar_details(rect, used_area, surface)

        # 墙体边缘风化效果
        if random.random() < 0.3:  # 30%概率出现边缘风化
            self._add_weathered_edges(rect, surface)

        # 重置随机种子
        random.seed()

    def _add_mortar_details(self, rect, stone_areas, surface):
        mortar_color = (COLOR_SHADOW[0] + 15, COLOR_SHADOW[1] + 15, COLOR_SHADOW[2] + 15)

        # 在石块间隙处添加细小石粒和碎屑
        for _ in range(8):
            pebble_x = rect.left + random.randint(2, TILE_SIZE - 2)
            pebble_y = rect.top + random.randint(2, TILE_SIZE - 2)

            # 检查是否在石块缝隙中
            in_gap = True
            for stone in stone_areas:
                if stone.collidepoint(pebble_x, pebble_y):
                    in_gap = False
                    break

            if in_gap:
                # 随机碎屑类型: 小石粒或砂浆点
                if random.random() < 0.7:
                    # 小石粒 - 更多样化的颜色
                    pebble_size = random.randint(1, 2)
                    pebble_color = (
                        COLOR_STONE[0] - 20 + random.randint(0, 40),
                        COLOR_STONE[1] - 20 + random.randint(0, 40),
                        COLOR_STONE[2] - 20 + random.randint(0, 40)
                    )
                    pygame.draw.circle(surface, pebble_color, (pebble_x, pebble_y), pebble_size)
                else:
                    # 砂浆点 - 不规则形状
                    mortar_size = random.randint(2, 4)
                    mortar_color_var = (
                        mortar_color[0] + random.randint(-10, 10),
                        mortar_color[1] + random.randint(-10, 10),
                        mortar_color[2] + random.randint(-10, 10)
                    )
                    # 不规则形状的砂浆点
                    points = []
                    for i in range(5):
                        angle = i * 2 * math.pi / 5
                        dist = mortar_size * random.uniform(0.7, 1.0)
                        px = pebble_x + math.cos(angle) * dist
                        py = pebble_y + math.sin(angle) * dist
                        points.append((px, py))
                    pygame.draw.polygon(surface, mortar_color_var, points)

    def _add_weathered_edges(self, rect, surface):
        """添加墙体边缘风化和不规则效果"""
        # 选择一个边缘进行风化
        edge = random.choice(['top', 'right', 'bottom', 'left'])

        # 风化深度
        depth = random.randint(1, 3)

        # 风化长度和位置 - 确保范围有效
        if edge in ['top', 'bottom']:
            # 确保长度不会超出有效范围
            max_length = max(TILE_SIZE // 4, (TILE_SIZE * 3 // 4) - (TILE_SIZE // 4))
            length = random.randint(TILE_SIZE // 4, min(TILE_SIZE // 2, max_length))

            # 确保起始位置有足够空间
            max_start = max(TILE_SIZE // 4, (TILE_SIZE * 3 // 4) - length)
            if max_start <= TILE_SIZE // 4:  # 如果最大起始位置小于等于最小起始位置
                start_pos = rect.left + TILE_SIZE // 4
            else:
                start_pos = rect.left + random.randint(TILE_SIZE // 4, max_start)
        else:  # left or right
            # 确保长度不会超出有效范围
            max_length = max(TILE_SIZE // 4, (TILE_SIZE * 3 // 4) - (TILE_SIZE // 4))
            length = random.randint(TILE_SIZE // 4, min(TILE_SIZE // 2, max_length))

            # 确保起始位置有足够空间
            max_start = max(TILE_SIZE // 4, (TILE_SIZE * 3 // 4) - length)
            if max_start <= TILE_SIZE // 4:  # 如果最大起始位置小于等于最小起始位置
                start_pos = rect.top + TILE_SIZE // 4
            else:
                start_pos = rect.top + random.randint(TILE_SIZE // 4, max_start)

        # 安全检查 - 确保长度至少为1
        length = max(1, length)

        # 绘制风化效果 - 通过添加与背景色相近的细小碎片
        weathered_color = (50, 50, 50)  # 深色风化痕迹

        # 生成不规则风化纹理
        for i in range(length):
            for j in range(depth):
                # 更自然的风化退化
                if random.random() < (1 - j / max(1, depth)):  # 越靠近边缘概率越高，防止除以零
                    if edge == 'top':
                        wx = start_pos + i
                        wy = rect.top + j
                    elif edge == 'right':
                        wx = rect.right - j - 1
                        wy = start_pos + i
                    elif edge == 'bottom':
                        wx = start_pos + i
                        wy = rect.bottom - j - 1
                    else:  # left
                        wx = rect.left + j
                        wy = start_pos + i

                    # 确保坐标在有效范围内
                    if (rect.left <= wx < rect.right and
                            rect.top <= wy < rect.bottom):
                        # 随机化风化颜色
                        w_color = (
                            weathered_color[0] + random.randint(-10, 10),
                            weathered_color[1] + random.randint(-10, 10),
                            weathered_color[2] + random.randint(-10, 10)
                        )

                        # 绘制风化点
                        if random.random() < 0.8:  # 80%概率绘制
                            pygame.draw.rect(surface, w_color, (wx, wy, 1, 1))

    def draw_moss_stone_enhanced(self, x, y, style, surface, stone_areas):
        """绘制增强版青苔石墙，带有更自然的青苔生长模式"""
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        # 随机青苔密度
        moss_density = random.uniform(0.6, 1.2)  # 随机化青苔生长密度

        # 在石块之间的缝隙添加青苔 - 更多样化的青苔斑点
        for i in range(int(7 * moss_density)):
            # 随机位置和大小
            moss_x = rect.left + random.randint(2, TILE_SIZE - 2)
            moss_y = rect.top + random.randint(2, TILE_SIZE - 2)
            moss_size = random.randint(2, 6)  # 更大更明显的青苔斑点

            # 检查是否在石块缝隙中
            in_gap = True
            for stone in stone_areas:
                if stone.collidepoint(moss_x, moss_y):
                    in_gap = False
                    break

            if in_gap:
                # 随机化青苔颜色
                moss_color_var = random.randint(-20, 20)
                moss_color = (
                    max(0, COLOR_MOSS[0] + moss_color_var),
                    max(20, COLOR_MOSS[1] + moss_color_var),
                    max(0, COLOR_MOSS[2] + moss_color_var)
                )

                # 创建不规则的青苔形状 - 带有随机变形的多边形
                if random.random() < 0.7:  # 70%是不规则多边形
                    moss_points = []
                    for j in range(5 + random.randint(0, 3)):  # 5-8边形
                        angle = j * 2 * math.pi / (5 + random.randint(0, 3))
                        px = moss_x + math.cos(angle) * moss_size * random.uniform(0.6, 1.2)
                        py = moss_y + math.sin(angle) * moss_size * random.uniform(0.6, 1.2)
                        moss_points.append((px, py))
                    pygame.draw.polygon(surface, moss_color, moss_points)
                else:  # 30%是简单圆形
                    pygame.draw.circle(surface, moss_color, (moss_x, moss_y), moss_size)

                # 添加青苔高光和细节
                if random.random() < 0.5:  # 一半的青苔有高光
                    highlight_color = (moss_color[0] + 30, moss_color[1] + 30, moss_color[2] + 30)
                    highlight_size = max(1, moss_size // 3)
                    highlight_offset = random.randint(-2, 2)  # 随机偏移
                    pygame.draw.circle(surface, highlight_color,
                                       (int(moss_x + highlight_offset), int(moss_y - highlight_offset)),
                                       highlight_size)

        # 在一些石块上添加青苔覆盖 - 更自然的生长模式
        for stone in random.sample(stone_areas, min(3, len(stone_areas))):
            # 随机化青苔覆盖模式
            coverage_style = random.choice(['top', 'corner', 'side', 'partial'])

            # 检查石块大小，过小则使用简单覆盖
            if stone.width < 9 or stone.height < 9:
                # 简单覆盖，避免过复杂的计算
                moss_rect = pygame.Rect(
                    stone.left,
                    stone.top,
                    max(3, stone.width),
                    max(3, min(stone.height, int(stone.height * 0.3)))
                )
            else:
                if coverage_style == 'top':
                    # 顶部覆盖
                    coverage = random.uniform(0.2, 0.5)  # 覆盖比例
                    moss_height = max(3, int(stone.height * coverage))
                    moss_rect = pygame.Rect(stone.left, stone.top, stone.width, moss_height)
                elif coverage_style == 'corner':
                    # 角落覆盖 - 确保尺寸合理
                    corner_min = max(3, stone.width // 4)
                    corner_max = max(corner_min, stone.width // 2)
                    corner_size = random.randint(corner_min, corner_max)

                    corner = random.choice(['tl', 'tr', 'bl', 'br'])
                    if corner == 'tl':
                        moss_rect = pygame.Rect(stone.left, stone.top, corner_size, corner_size)
                    elif corner == 'tr':
                        moss_rect = pygame.Rect(stone.right - corner_size, stone.top, corner_size, corner_size)
                    elif corner == 'bl':
                        moss_rect = pygame.Rect(stone.left, stone.bottom - corner_size, corner_size, corner_size)
                    else:  # 'br'
                        moss_rect = pygame.Rect(stone.right - corner_size, stone.bottom - corner_size, corner_size,
                                                corner_size)
                elif coverage_style == 'side':
                    # 侧面覆盖 - 确保尺寸合理
                    side = random.choice(['left', 'right', 'top', 'bottom'])
                    if side in ['left', 'right']:
                        side_min = 3
                        side_max = max(side_min, stone.width // 3)
                        side_width = random.randint(side_min, side_max)
                        side_height = stone.height

                        if side == 'left':
                            moss_rect = pygame.Rect(stone.left, stone.top, side_width, side_height)
                        else:  # 'right'
                            moss_rect = pygame.Rect(stone.right - side_width, stone.top, side_width, side_height)
                    else:  # 'top' or 'bottom'
                        side_width = stone.width
                        side_min = 3
                        side_max = max(side_min, stone.height // 3)
                        side_height = random.randint(side_min, side_max)

                        if side == 'top':
                            moss_rect = pygame.Rect(stone.left, stone.top, side_width, side_height)
                        else:  # 'bottom'
                            moss_rect = pygame.Rect(stone.left, stone.bottom - side_height, side_width, side_height)
                else:  # 'partial'
                    # 不规则部分覆盖 - 确保宽高都是正数
                    max_width_offset = max(0, stone.width // 3 - 1)  # 确保留有空间
                    max_height_offset = max(0, stone.height // 3 - 1)  # 确保留有空间

                    start_x = stone.left + random.randint(0, max_width_offset)
                    start_y = stone.top + random.randint(0, max_height_offset)

                    # 确保宽高至少为3像素
                    width = max(3, stone.width - random.randint(0, stone.width // 3))
                    height = max(3, stone.height - random.randint(0, stone.height // 3))

                    moss_rect = pygame.Rect(start_x, start_y, width, height)

            # 随机化青苔颜色 - 更多变化
            moss_color_var = random.randint(-15, 15)
            moss_color = (
                max(0, COLOR_MOSS[0] + moss_color_var),
                max(20, COLOR_MOSS[1] + moss_color_var),
                max(0, COLOR_MOSS[2] + moss_color_var)
            )

            # 使用半透明叠加效果 - 多层渐变
            for i in range(3):
                layer_height = max(1, moss_rect.height - i * 2)  # 确保高度至少为1
                if layer_height <= 0:
                    continue

                alpha = random.randint(130, 170) - i * 30  # 随机透明度
                moss_layer = pygame.Surface((moss_rect.width, layer_height), pygame.SRCALPHA)
                moss_layer.fill((moss_color[0], moss_color[1], moss_color[2], alpha))
                surface.blit(moss_layer, (moss_rect.left, moss_rect.top + i * 2))

                # 添加青苔细节纹理，但只在足够大的区域添加
            if moss_rect.width > 5 and moss_rect.height > 5:
                for _ in range(random.randint(2, 4)):  # 减少详细纹理数量
                    # 防止无效的随机范围
                    x_max = max(2, moss_rect.width - 3)
                    y_max = max(2, moss_rect.height - 3)

                    detail_x = moss_rect.left + random.randint(2, x_max)
                    detail_y = moss_rect.top + random.randint(2, y_max)
                    detail_size = random.randint(1, 2)  # 减小纹理尺寸
                    detail_type = random.choice(['dot', 'line'])

                    # 青苔纹理细节颜色
                    detail_color = (
                        max(0, moss_color[0] - random.randint(10, 30)),
                        max(20, moss_color[1] - random.randint(10, 30)),
                        max(0, moss_color[2] - random.randint(10, 30))
                    )

                    if detail_type == 'dot':
                        pygame.draw.circle(surface, detail_color, (detail_x, detail_y), detail_size)
                    else:  # 'line'
                        line_length = random.randint(2, 4)  # 减小线长
                        line_angle = random.randint(0, 180)
                        end_x = detail_x + int(math.cos(math.radians(line_angle)) * line_length)
                        end_y = detail_y + int(math.sin(math.radians(line_angle)) * line_length)
                        pygame.draw.line(surface, detail_color, (detail_x, detail_y), (end_x, end_y), 1)

    def draw_cracked_stone_enhanced(self, x, y, style, surface, stone_areas):
        """绘制增强版裂缝石墙，带有更自然的裂缝纹理和应力线"""
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        # 随机裂缝复杂度
        crack_complexity = random.uniform(0.8, 1.2)  # 随机化裂缝复杂度

        # 绘制贯穿整个墙体的主裂缝
        crack_width = max(1, min(3, int(random.randint(1, 3) * crack_complexity)))

        # 更自然的裂缝起点和终点
        edge_start = random.choice(['top', 'left', 'right'])
        if edge_start == 'top':
            crack_start = (rect.left + random.randint(TILE_SIZE // 4, TILE_SIZE * 3 // 4),
                           rect.top)
        elif edge_start == 'left':
            crack_start = (rect.left,
                           rect.top + random.randint(TILE_SIZE // 4, TILE_SIZE * 3 // 4))
        else:  # 'right'
            crack_start = (rect.right,
                           rect.top + random.randint(TILE_SIZE // 4, TILE_SIZE * 3 // 4))

        # 裂缝终点通常在下方或对面边缘
        if random.random() < 0.7:  # 70%几率终点在底部
            crack_end = (rect.left + random.randint(TILE_SIZE // 4, TILE_SIZE * 3 // 4),
                         rect.bottom)
        else:  # 30%几率终点在侧面
            if edge_start == 'left':
                crack_end = (rect.right,
                             rect.top + random.randint(TILE_SIZE // 4, TILE_SIZE * 3 // 4))
            else:
                crack_end = (rect.left,
                             rect.top + random.randint(TILE_SIZE // 4, TILE_SIZE * 3 // 4))

        # 使用贝塞尔曲线绘制更自然的裂缝
        control_points = []
        num_segments = max(3, min(7, int(random.randint(3, 5) * crack_complexity)))

        # 生成控制点
        control_points.append(crack_start)

        # 确保裂缝穿过一些石块 - 增加故事性
        stones_on_path = []
        for stone in stone_areas:
            # 检查石块是否在裂缝可能路径上
            if (min(crack_start[0], crack_end[0]) <= stone.centerx <= max(crack_start[0], crack_end[0]) and
                    min(crack_start[1], crack_end[1]) <= stone.centery <= max(crack_start[1], crack_end[1])):
                stones_on_path.append(stone)

        # 如果路径上有石块，优先穿过它们
        if stones_on_path:
            # 按照从开始到结束的顺序排序石块
            if abs(crack_end[0] - crack_start[0]) > abs(crack_end[1] - crack_start[1]):
                # 主要是水平裂缝
                stones_on_path.sort(key=lambda s: s.centerx)
                if crack_start[0] > crack_end[0]:  # 确保排序方向正确
                    stones_on_path.reverse()
            else:
                # 主要是垂直裂缝
                stones_on_path.sort(key=lambda s: s.centery)
                if crack_start[1] > crack_end[1]:  # 确保排序方向正确
                    stones_on_path.reverse()

            # 穿过所选石块
            for stone in stones_on_path:
                control_points.append((stone.centerx + random.randint(-5, 5),
                                       stone.centery + random.randint(-5, 5)))

        # 添加中间控制点，确保足够的弯曲
        remaining_segments = num_segments - len(control_points)
        for i in range(remaining_segments):
            # 更自然的控制点分布
            ratio = (i + 1) / (remaining_segments + 1)
            base_x = crack_start[0] + (crack_end[0] - crack_start[0]) * ratio
            base_y = crack_start[1] + (crack_end[1] - crack_start[1]) * ratio

            # 随机偏移，越靠近中间的控制点偏移越大
            offset_factor = ratio * (1 - ratio) * 4  # 在中心处达到最大
            offset_range = int(TILE_SIZE // 4 * offset_factor)
            offset_x = random.randint(-offset_range, offset_range)
            offset_y = random.randint(-offset_range, offset_range)

            control_points.append((base_x + offset_x, base_y + offset_y))

        # 添加终点
        control_points.append(crack_end)

        # 绘制裂缝段 - 多层次细节
        for i in range(len(control_points) - 1):
            start_point = control_points[i]
            end_point = control_points[i + 1]

            # 添加微小的随机扰动，使裂缝更自然
            mid_segments = random.randint(2, 4)  # 中间分段，增加自然曲折感
            last_point = start_point

            for j in range(mid_segments):
                # 确定段落点
                t = (j + 1) / (mid_segments + 1)
                mid_x = start_point[0] * (1 - t) + end_point[0] * t
                mid_y = start_point[1] * (1 - t) + end_point[1] * t

                # 添加随机扰动，模拟自然裂缝的不规则性
                noise_factor = min(10, max(2, int((TILE_SIZE // 10) * crack_complexity)))
                noise_x = random.randint(-noise_factor, noise_factor)
                noise_y = random.randint(-noise_factor, noise_factor)

                # 裂缝颜色随机变化
                crack_color = (
                    max(10, COLOR_CRACK[0] + random.randint(-20, 10)),
                    max(10, COLOR_CRACK[1] + random.randint(-20, 10)),
                    max(10, COLOR_CRACK[2] + random.randint(-20, 10))
                )

                # 当前段点
                current_point = (mid_x + noise_x, mid_y + noise_y)

                # 绘制段落，线宽有细微变化
                segment_width = max(1, int(crack_width * (1 - 0.3 * random.random())))
                pygame.draw.line(surface, crack_color, last_point, current_point, segment_width)

                # 记录上一点
                last_point = current_point

            # 连接到终点
            pygame.draw.line(surface, COLOR_CRACK, last_point, end_point, crack_width)

            # 在裂缝周围添加阴影和碎石效果
            for j in range(random.randint(1, 3)):
                edge_x = (start_point[0] + end_point[0]) / 2 + random.randint(-10, 10)
                edge_y = (start_point[1] + end_point[1]) / 2 + random.randint(-10, 10)

                # 裂缝边缘碎石
                if random.random() < 0.6:
                    debris_size = random.randint(1, 2)
                    debris_color = (
                        max(0, COLOR_SHADOW[0] - 10 + random.randint(0, 20)),
                        max(0, COLOR_SHADOW[1] - 10 + random.randint(0, 20)),
                        max(0, COLOR_SHADOW[2] - 10 + random.randint(0, 20))
                    )
                    pygame.draw.circle(surface, debris_color,
                                       (int(edge_x), int(edge_y)), debris_size)

                # 裂缝阴影效果
                if random.random() < 0.4:
                    shadow_offset = random.randint(1, 3)
                    shadow_color = (COLOR_SHADOW[0], COLOR_SHADOW[1], COLOR_SHADOW[2], 120)
                    shadow_surface = pygame.Surface((3, 3), pygame.SRCALPHA)
                    pygame.draw.circle(shadow_surface, shadow_color, (1, 1), 1)
                    surface.blit(shadow_surface, (int(edge_x - 1), int(edge_y - 1 + shadow_offset)))

        # 添加小裂缝分支 - 更随机的分布
        branch_count = max(2, min(5, int(random.randint(2, 4) * crack_complexity)))
        for _ in range(branch_count):
            # 从控制点中随机选择一个作为分支起点
            if len(control_points) >= 2:
                branch_idx = random.randint(0, len(control_points) - 2)
                branch_start = control_points[branch_idx]

                # 分支属性
                branch_length = random.randint(5, 15)
                branch_width = max(1, crack_width - 1)  # 分支略细于主裂缝

                # 分支方向 - 与主裂缝形成一定角度
                if branch_idx < len(control_points) - 1:
                    main_dx = control_points[branch_idx + 1][0] - control_points[branch_idx][0]
                    main_dy = control_points[branch_idx + 1][1] - control_points[branch_idx][1]

                    # 计算垂直方向
                    if abs(main_dx) + abs(main_dy) > 0.001:  # 避免除零
                        # 垂直于主裂缝方向
                        perp_dx = -main_dy
                        perp_dy = main_dx
                        # 归一化
                        length = math.sqrt(perp_dx ** 2 + perp_dy ** 2)
                        perp_dx /= length
                        perp_dy /= length

                        # 添加随机角度偏移
                        branch_angle = random.uniform(-math.pi / 3, math.pi / 3)  # 相对垂直±60度
                        cos_angle = math.cos(branch_angle)
                        sin_angle = math.sin(branch_angle)
                        final_dx = (perp_dx * cos_angle - perp_dy * sin_angle) * branch_length
                        final_dy = (perp_dx * sin_angle + perp_dy * cos_angle) * branch_length

                        branch_end = (branch_start[0] + final_dx, branch_start[1] + final_dy)

                        # 检查分支是否超出墙体范围
                        if (rect.left <= branch_end[0] <= rect.right and
                                rect.top <= branch_end[1] <= rect.bottom):
                            # 绘制分支
                            branch_color = (
                                max(10, COLOR_CRACK[0] + random.randint(-10, 10)),
                                max(10, COLOR_CRACK[1] + random.randint(-10, 10)),
                                max(10, COLOR_CRACK[2] + random.randint(-10, 10))
                            )

                            # 更自然的分叉裂缝
                            if random.random() < 0.7:  # 70%概率绘制曲折分支
                                # 添加中间点使分支更曲折
                                mid_x = branch_start[0] + final_dx * 0.5 + random.randint(-4, 4)
                                mid_y = branch_start[1] + final_dy * 0.5 + random.randint(-4, 4)
                                mid_point = (mid_x, mid_y)

                                pygame.draw.line(surface, branch_color, branch_start, mid_point, branch_width)
                                pygame.draw.line(surface, branch_color, mid_point, branch_end, branch_width)
                            else:  # 30%概率绘制直线分支
                                pygame.draw.line(surface, branch_color, branch_start, branch_end, branch_width)

                            # 添加微小的碎石碎片
                            if random.random() < 0.5:
                                debris_x = branch_end[0] + random.randint(-3, 3)
                                debris_y = branch_end[1] + random.randint(-3, 3)
                                debris_size = random.randint(1, 2)
                                pygame.draw.circle(surface, branch_color,
                                                   (int(debris_x), int(debris_y)), debris_size)

    def draw_basic_stone_enhanced(self, x, y, style, surface, stone_areas):
        """绘制增强版基础石墙，带有更丰富的纹理细节"""
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        # 在石块上添加细节纹理 - 随机增加多种纹理类型
        for stone in stone_areas:
            texture_type = random.choice(['lines', 'dots', 'bands', 'none'])

            if texture_type == 'lines':
                # 随机数量的石纹线条
                num_lines = random.randint(2, 4)
                for _ in range(num_lines):
                    # 随机线条位置和属性
                    line_y = stone.top + random.randint(stone.height // 5, stone.height * 4 // 5)
                    line_width = random.randint(1, 2)
                    line_alpha = random.randint(100, 180)
                    line_color = (max(0, COLOR_SHADOW[0] - 5),
                                  max(0, COLOR_SHADOW[1] - 5),
                                  max(0, COLOR_SHADOW[2] - 5))

                    # 随机线条长度和位置
                    line_start_x = stone.left + random.randint(1, stone.width // 3)
                    line_end_x = stone.right - random.randint(1, stone.width // 3)

                    # 带有微小弯曲和不规则的线条
                    if random.random() < 0.7:  # 70%概率是弯曲线条
                        mid_y_offset = random.randint(-3, 3)
                        mid_x = (line_start_x + line_end_x) // 2
                        mid_y = line_y + mid_y_offset

                        pygame.draw.line(surface, line_color,
                                         (line_start_x, line_y), (mid_x, mid_y), line_width)
                        pygame.draw.line(surface, line_color,
                                         (mid_x, mid_y), (line_end_x, line_y), line_width)
                    else:  # 30%概率是直线
                        pygame.draw.line(surface, line_color,
                                         (line_start_x, line_y), (line_end_x, line_y), line_width)

            elif texture_type == 'dots':
                # 石块上的斑点纹理
                num_dots = random.randint(4, 8)
                for _ in range(num_dots):
                    dot_x = stone.left + random.randint(2, stone.width - 3)
                    dot_y = stone.top + random.randint(2, stone.height - 3)
                    dot_size = random.randint(1, 2)
                    dot_color = (max(0, COLOR_SHADOW[0] - 10 + random.randint(0, 20)),
                                 max(0, COLOR_SHADOW[1] - 10 + random.randint(0, 20)),
                                 max(0, COLOR_SHADOW[2] - 10 + random.randint(0, 20)))

                    pygame.draw.circle(surface, dot_color, (dot_x, dot_y), dot_size)

            elif texture_type == 'bands':
                # 条带纹理 - 模拟自然石层
                num_bands = random.randint(2, 3)
                band_height = stone.height // (num_bands + 1)

                for i in range(num_bands):
                    band_y = stone.top + (i + 1) * band_height
                    band_width = max(1, min(2, int(stone.width * random.uniform(0.6, 0.9))))
                    band_color = (max(0, COLOR_SHADOW[0] - 5 + random.randint(-10, 10)),
                                  max(0, COLOR_SHADOW[1] - 5 + random.randint(-10, 10)),
                                  max(0, COLOR_SHADOW[2] - 5 + random.randint(-10, 10)))

                    # 随机带偏移
                    start_offset = random.randint(1, stone.width // 4)
                    end_offset = random.randint(1, stone.width // 4)
                    band_start_x = stone.left + start_offset
                    band_end_x = stone.right - end_offset

                    pygame.draw.line(surface, band_color,
                                     (band_start_x, band_y), (band_end_x, band_y), band_width)

        # 添加石块之间的灰浆线 - 更不规则的灰浆纹理
        mortar_color = (COLOR_SHADOW[0] + 20, COLOR_SHADOW[1] + 20, COLOR_SHADOW[2] + 20)

        # 水平灰浆线 - 不再完全水平
        for y_base in range(rect.top + TILE_SIZE // 3, rect.bottom, TILE_SIZE // 3):
            # 检查是否穿过石块中部
            crosses_stone = False
            for stone in stone_areas:
                if (y_base > stone.top + 5 and y_base < stone.bottom - 5):
                    crosses_stone = True
                    break

            if not crosses_stone:
                # 分段绘制，实现不规则灰浆线
                segments = random.randint(2, 4)
                segment_width = TILE_SIZE / segments

                for s in range(segments):
                    line_width = random.randint(1, 2)
                    # 随机化线段Y坐标
                    y_pos = y_base + random.randint(-2, 2)

                    # 计算线段起止X坐标
                    start_x = rect.left + int(s * segment_width)
                    end_x = start_x + int(segment_width)

                    # 随机墙缝颜色
                    mortar_var = random.randint(-10, 10)
                    current_mortar_color = (
                        max(20, mortar_color[0] + mortar_var),
                        max(20, mortar_color[1] + mortar_var),
                        max(20, mortar_color[2] + mortar_var)
                    )

                    pygame.draw.line(surface, current_mortar_color,
                                     (start_x, y_pos), (end_x, y_pos), line_width)

                    # 添加随机灰浆碎屑
                    if random.random() < 0.3:
                        debris_x = random.randint(start_x, end_x)
                        debris_y = y_pos + random.randint(-3, 3)
                        pygame.draw.circle(surface, current_mortar_color,
                                           (debris_x, debris_y), 1)

        # 垂直灰浆线 - 不再完全垂直
        for x_base in range(rect.left + TILE_SIZE // 3, rect.right, TILE_SIZE // 3):
            # 检查是否穿过石块中部
            crosses_stone = False
            for stone in stone_areas:
                if (x_base > stone.left + 5 and x_base < stone.right - 5):
                    crosses_stone = True
                    break

            if not crosses_stone:
                # 分段绘制，实现不规则灰浆线
                segments = random.randint(2, 4)
                segment_height = TILE_SIZE / segments

                for s in range(segments):
                    line_width = random.randint(1, 2)
                    # 随机化线段X坐标
                    x_pos = x_base + random.randint(-2, 2)

                    # 计算线段起止Y坐标
                    start_y = rect.top + int(s * segment_height)
                    end_y = start_y + int(segment_height)

                    # 随机墙缝颜色
                    mortar_var = random.randint(-10, 10)
                    current_mortar_color = (
                        max(20, mortar_color[0] + mortar_var),
                        max(20, mortar_color[1] + mortar_var),
                        max(20, mortar_color[2] + mortar_var)
                    )

                    pygame.draw.line(surface, current_mortar_color,
                                     (x_pos, start_y), (x_pos, end_y), line_width)

                    # 添加随机灰浆碎屑
                    if random.random() < 0.3:
                        debris_x = x_pos + random.randint(-3, 3)
                        debris_y = random.randint(start_y, end_y)
                        pygame.draw.circle(surface, current_mortar_color,
                                           (debris_x, debris_y), 1)

    # 地面绘画方法
    def draw_floor(self, x, y, surface=None):
        surface = surface or self.screen
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        style = self.tile_styles[y][x]

        # 处理特殊区域（喷泉房间、岩浆房间等）
        if self.fountain_room and self._is_in_fountain_room(x, y):
            self._draw_fountain_floor(rect, surface)
            return
        elif self.lava_room and self._is_in_lava_room(x, y):
            if self.maze[y][x] == 3:  # 岩浆
                self._draw_lava_floor(rect, surface)
                return
            elif self.maze[y][x] == 5 or self.maze[y][x] == 4:  # 地狱地板
                self._draw_hell_floor(rect, surface)
                return

        # 基础地板颜色 - 微妙的变化使其更自然
        base_color_var = random.randint(-10, 10)
        base_color = (
            max(130, min(170, COLOR_FLOOR[0] + base_color_var)),
            max(130, min(170, COLOR_FLOOR[1] + base_color_var)),
            max(130, min(170, COLOR_FLOOR[2] + base_color_var))
        )
        pygame.draw.rect(surface, base_color, rect)

        # 添加纹理噪点以增强真实感
        for _ in range(5):
            noise_x = rect.left + random.randint(0, TILE_SIZE - 1)
            noise_y = rect.top + random.randint(0, TILE_SIZE - 1)
            noise_color = (
                base_color[0] + random.randint(-5, 5),
                base_color[1] + random.randint(-5, 5),
                base_color[2] + random.randint(-5, 5)
            )
            pixel_size = random.randint(1, 2)
            pygame.draw.rect(surface, noise_color, (noise_x, noise_y, pixel_size, pixel_size))

        # 绘制边缘暗影以增加深度感
        edge_shadow = (base_color[0] - 15, base_color[1] - 15, base_color[2] - 15)
        shadow_width = 2

        # 右边缘阴影
        pygame.draw.rect(surface, edge_shadow,
                         (rect.right - shadow_width, rect.top, shadow_width, rect.height))
        # 底部阴影
        pygame.draw.rect(surface, edge_shadow,
                         (rect.left, rect.bottom - shadow_width, rect.width, shadow_width))

        # 绘制水平裂缝
        if style['crack_h']:
            crack_y = rect.centery + random.randint(-2, 2)  # 位置随机化
            crack_width = random.randint(TILE_SIZE // 2, TILE_SIZE - 4)  # 长度随机化
            crack_start = rect.left + random.randint(2, (TILE_SIZE - crack_width) // 2)

            # 主裂缝
            pygame.draw.line(surface, COLOR_FLOOR_CRACK,
                             (crack_start, crack_y),
                             (crack_start + crack_width, crack_y),
                             random.randint(1, 2))  # 宽度随机化

            # 裂缝分支(小概率)
            if random.random() < 0.3:
                branch_start = crack_start + random.randint(crack_width // 4, 3 * crack_width // 4)
                branch_length = random.randint(3, 7)
                branch_angle = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
                branch_end = (
                    branch_start + branch_length * math.cos(branch_angle),
                    crack_y + branch_length * math.sin(branch_angle)
                )
                pygame.draw.line(surface, COLOR_FLOOR_CRACK,
                                 (branch_start, crack_y), branch_end, 1)

        # 绘制垂直裂缝
        if style['crack_v']:
            crack_x = rect.centerx + random.randint(-2, 2)  # 位置随机化
            crack_height = random.randint(TILE_SIZE // 2, TILE_SIZE - 4)  # 长度随机化
            crack_start = rect.top + random.randint(2, (TILE_SIZE - crack_height) // 2)

            # 主裂缝
            pygame.draw.line(surface, COLOR_FLOOR_CRACK,
                             (crack_x, crack_start),
                             (crack_x, crack_start + crack_height),
                             random.randint(1, 2))  # 宽度随机化

            # 裂缝分支(小概率)
            if random.random() < 0.3:
                branch_start = crack_start + random.randint(crack_height // 4, 3 * crack_height // 4)
                branch_length = random.randint(3, 7)
                branch_angle = random.choice([-1, 1]) * random.uniform(0.5, 1.5)
                branch_end = (
                    crack_x + branch_length * math.cos(branch_angle),
                    branch_start + branch_length * math.sin(branch_angle)
                )
                pygame.draw.line(surface, COLOR_FLOOR_CRACK,
                                 (crack_x, branch_start), branch_end, 1)

        # 额外的小裂缝 (如果存在)
        if style.get('extra_cracks', 0) > 0:
            for _ in range(style['extra_cracks']):
                start_x = rect.left + random.randint(3, TILE_SIZE - 3)
                start_y = rect.top + random.randint(3, TILE_SIZE - 3)
                length = random.randint(3, 8)
                angle = random.uniform(0, 2 * math.pi)
                end_x = start_x + length * math.cos(angle)
                end_y = start_y + length * math.sin(angle)

                pygame.draw.line(surface, COLOR_FLOOR_CRACK,
                                 (start_x, start_y), (end_x, end_y), 1)

        # 污渍 (更自然的形状)
        if style['stain_pos']:
            sx, sy = style['stain_pos']
            stain_color = (base_color[0] - 20, base_color[1] - 20, base_color[2] - 20, 40)
            stain_size = random.randint(4, 8)
            stain_surf = pygame.Surface((stain_size * 2, stain_size * 2), pygame.SRCALPHA)

            # 生成不规则形状污渍
            for i in range(random.randint(2, 4)):
                angle = random.uniform(0, 2 * math.pi)
                distance = random.uniform(0.3, 1.0) * stain_size
                px = stain_size + distance * math.cos(angle)
                py = stain_size + distance * math.sin(angle)
                spot_size = random.randint(2, stain_size - 1)
                pygame.draw.circle(stain_surf, stain_color, (px, py), spot_size)

            surface.blit(stain_surf, (rect.left + sx, rect.top + sy))

        # 青苔小块 (如果与青苔墙壁相邻)
        if style.get('moss_patches', False):
            moss_color = style.get('moss_color', (34, 139, 34))
            for _ in range(random.randint(1, 3)):
                moss_x = rect.left + random.randint(2, TILE_SIZE - 4)
                moss_y = rect.top + random.randint(2, TILE_SIZE - 4)
                moss_size = random.randint(2, 4)
                moss_alpha = random.randint(30, 80)

                moss_surface = pygame.Surface((moss_size * 2, moss_size * 2), pygame.SRCALPHA)
                pygame.draw.circle(moss_surface, (*moss_color, moss_alpha),
                                   (moss_size, moss_size), moss_size)
                surface.blit(moss_surface, (moss_x, moss_y))

        # 磨损模式 - 根据房间位置和行走路径添加磨损效果
        if style.get('wear_pattern', 'none') != 'none':
            wear_alpha = int(70 * style.get('dust_level', 0.3))
            wear_color = (0, 0, 0, wear_alpha)

            if style['wear_pattern'] == 'corner':
                # 角落磨损
                corner = random.choice(['tl', 'tr', 'bl', 'br'])
                if corner == 'tl':
                    wear_rect = pygame.Rect(rect.left, rect.top, TILE_SIZE // 3, TILE_SIZE // 3)
                elif corner == 'tr':
                    wear_rect = pygame.Rect(rect.right - TILE_SIZE // 3, rect.top, TILE_SIZE // 3, TILE_SIZE // 3)
                elif corner == 'bl':
                    wear_rect = pygame.Rect(rect.left, rect.bottom - TILE_SIZE // 3, TILE_SIZE // 3, TILE_SIZE // 3)
                else:  # 'br'
                    wear_rect = pygame.Rect(rect.right - TILE_SIZE // 3, rect.bottom - TILE_SIZE // 3, TILE_SIZE // 3,
                                            TILE_SIZE // 3)

                wear_surf = pygame.Surface((wear_rect.width, wear_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(wear_surf, wear_color, (0, 0, wear_rect.width, wear_rect.height))
                surface.blit(wear_surf, wear_rect)

            elif style['wear_pattern'] == 'edge':
                # 边缘磨损
                edge = random.choice(['top', 'right', 'bottom', 'left'])
                if edge == 'top':
                    wear_rect = pygame.Rect(rect.left, rect.top, rect.width, TILE_SIZE // 3)
                elif edge == 'right':
                    wear_rect = pygame.Rect(rect.right - TILE_SIZE // 3, rect.top, TILE_SIZE // 3, rect.height)
                elif edge == 'bottom':
                    wear_rect = pygame.Rect(rect.left, rect.bottom - TILE_SIZE // 3, rect.width, TILE_SIZE // 3)
                else:  # 'left'
                    wear_rect = pygame.Rect(rect.left, rect.top, TILE_SIZE // 3, rect.height)

                wear_surf = pygame.Surface((wear_rect.width, wear_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(wear_surf, wear_color, (0, 0, wear_rect.width, wear_rect.height))
                surface.blit(wear_surf, wear_rect)

        # 潮湿效果 (在角落或墙边)
        if style.get('moisture', False):
            moisture_alpha = random.randint(20, 40)
            moisture_color = (0, 0, 100, moisture_alpha)  # 蓝色调潮湿

            # 随机选择一个角落或边缘
            position = random.choice(['tl', 'tr', 'bl', 'br', 'top', 'bottom', 'left', 'right'])

            if position in ['tl', 'tr', 'bl', 'br']:  # 角落
                if position == 'tl':
                    moisture_rect = pygame.Rect(rect.left, rect.top, TILE_SIZE // 3, TILE_SIZE // 3)
                elif position == 'tr':
                    moisture_rect = pygame.Rect(rect.right - TILE_SIZE // 3, rect.top, TILE_SIZE // 3, TILE_SIZE // 3)
                elif position == 'bl':
                    moisture_rect = pygame.Rect(rect.left, rect.bottom - TILE_SIZE // 3, TILE_SIZE // 3, TILE_SIZE // 3)
                else:  # 'br'
                    moisture_rect = pygame.Rect(rect.right - TILE_SIZE // 3, rect.bottom - TILE_SIZE // 3,
                                                TILE_SIZE // 3, TILE_SIZE // 3)

                moisture_surf = pygame.Surface((moisture_rect.width, moisture_rect.height), pygame.SRCALPHA)
                for _ in range(5):  # 创建多个小水滴以形成不规则形状
                    drop_x = random.randint(0, moisture_rect.width)
                    drop_y = random.randint(0, moisture_rect.height)
                    drop_size = random.randint(2, 5)
                    pygame.draw.circle(moisture_surf, moisture_color, (drop_x, drop_y), drop_size)

                surface.blit(moisture_surf, moisture_rect)
            else:  # 边缘
                if position == 'top':
                    moisture_rect = pygame.Rect(rect.left + rect.width // 4, rect.top, rect.width // 2, TILE_SIZE // 4)
                elif position == 'right':
                    moisture_rect = pygame.Rect(rect.right - TILE_SIZE // 4, rect.top + rect.height // 4,
                                                TILE_SIZE // 4, rect.height // 2)
                elif position == 'bottom':
                    moisture_rect = pygame.Rect(rect.left + rect.width // 4, rect.bottom - TILE_SIZE // 4,
                                                rect.width // 2, TILE_SIZE // 4)
                else:  # 'left'
                    moisture_rect = pygame.Rect(rect.left, rect.top + rect.height // 4, TILE_SIZE // 4,
                                                rect.height // 2)

                moisture_surf = pygame.Surface((moisture_rect.width, moisture_rect.height), pygame.SRCALPHA)
                pygame.draw.rect(moisture_surf, moisture_color, (0, 0, moisture_rect.width, moisture_rect.height),
                                 border_radius=3)
                surface.blit(moisture_surf, moisture_rect)

    def _draw_fountain_floor(self, rect, surface):
        # 更丰富的大理石底色 - 使用微妙渐变
        base_colors = [(90, 90, 110), (100, 100, 120), (110, 110, 130)]
        base_color = random.choice(base_colors)
        pygame.draw.rect(surface, base_color, rect)

        # 创建有组织的大理石纹理网格
        tile_div = 4  # 将地砖分成4x4的小网格
        cell_size = TILE_SIZE // tile_div

        # 绘制网格线 - 更精细的大理石纹路
        for i in range(1, tile_div):
            # 水平线
            line_y = rect.top + i * cell_size
            line_color = (180, 180, 200, 30)  # 更淡的线条
            pygame.draw.line(surface, line_color,
                             (rect.left, line_y), (rect.right, line_y), 1)

            # 垂直线
            line_x = rect.left + i * cell_size
            pygame.draw.line(surface, line_color,
                             (line_x, rect.top), (line_x, rect.bottom), 1)

        # 添加细致的大理石纹理
        for i in range(tile_div):
            for j in range(tile_div):
                # 每个小网格内添加随机的大理石纹理
                if random.random() < 0.7:  # 70%的小格子有纹理
                    cell_x = rect.left + j * cell_size
                    cell_y = rect.top + i * cell_size

                    # 随机选择纹理类型
                    texture_type = random.choice(['vein', 'spot', 'wave'])

                    if texture_type == 'vein':
                        # 大理石脉络
                        vein_start = (cell_x + random.randint(1, cell_size - 1),
                                      cell_y + random.randint(1, cell_size - 1))
                        vein_length = random.randint(3, cell_size - 1)
                        vein_angle = random.uniform(0, 2 * math.pi)
                        vein_end_x = vein_start[0] + vein_length * math.cos(vein_angle)
                        vein_end_y = vein_start[1] + vein_length * math.sin(vein_angle)

                        vein_color = (200, 200, 220, 40)
                        pygame.draw.line(surface, vein_color, vein_start,
                                         (vein_end_x, vein_end_y), 1)

                    elif texture_type == 'spot':
                        # 大理石斑点
                        spot_x = cell_x + cell_size // 2
                        spot_y = cell_y + cell_size // 2
                        spot_size = random.randint(1, 3)
                        spot_color = (200, 200, 220, 30)

                        pygame.draw.circle(surface, spot_color,
                                           (spot_x, spot_y), spot_size)

                    else:  # 'wave'
                        # 波浪纹路
                        wave_points = []
                        wave_y_base = cell_y + cell_size // 2
                        for w in range(0, cell_size + 1, 2):
                            wave_x = cell_x + w
                            wave_y = wave_y_base + random.randint(-1, 1)
                            wave_points.append((wave_x, wave_y))

                        if len(wave_points) >= 2:
                            wave_color = (200, 200, 220, 20)
                            pygame.draw.lines(surface, wave_color, False, wave_points, 1)

        # 更精致的裂缝网络 - 主裂缝和支裂缝
        # 主裂缝 - 更有规律
        if random.random() < 0.8:  # 80%的地砖有主裂缝
            crack_dir = random.choice(['h', 'v', 'diag'])
            crack_color = (80, 80, 100, 80)

            if crack_dir == 'h':
                # 水平裂缝
                crack_y = rect.top + random.randint(TILE_SIZE // 3, 2 * TILE_SIZE // 3)
                # 稍微不规则的水平线
                crack_points = []
                for x in range(rect.left, rect.right + 1, 2):
                    y_var = random.randint(-1, 1)
                    crack_points.append((x, crack_y + y_var))

                if len(crack_points) >= 2:
                    pygame.draw.lines(surface, crack_color, False, crack_points, 1)

            elif crack_dir == 'v':
                # 垂直裂缝
                crack_x = rect.left + random.randint(TILE_SIZE // 3, 2 * TILE_SIZE // 3)
                # 稍微不规则的垂直线
                crack_points = []
                for y in range(rect.top, rect.bottom + 1, 2):
                    x_var = random.randint(-1, 1)
                    crack_points.append((crack_x + x_var, y))

                if len(crack_points) >= 2:
                    pygame.draw.lines(surface, crack_color, False, crack_points, 1)

            else:  # 'diag'
                # 对角线裂缝
                start_corner = random.choice(['tl', 'tr', 'bl', 'br'])
                if start_corner == 'tl':
                    start, end = (rect.left, rect.top), (rect.right, rect.bottom)
                elif start_corner == 'tr':
                    start, end = (rect.right, rect.top), (rect.left, rect.bottom)
                elif start_corner == 'bl':
                    start, end = (rect.left, rect.bottom), (rect.right, rect.top)
                else:  # 'br'
                    start, end = (rect.right, rect.bottom), (rect.left, rect.top)

                # 稍微不规则的对角线
                crack_points = []
                steps = TILE_SIZE // 2
                for i in range(steps + 1):
                    t = i / steps
                    x = int(start[0] + (end[0] - start[0]) * t)
                    y = int(start[1] + (end[1] - start[1]) * t)
                    var = random.randint(-1, 1)
                    if start_corner in ['tl', 'br']:
                        crack_points.append((x + var, y + var))
                    else:
                        crack_points.append((x + var, y - var))

                pygame.draw.lines(surface, crack_color, False, crack_points, 1)

            # 添加微小的支裂缝
            if random.random() < 0.5:  # 50%概率添加支裂缝
                branch_count = random.randint(1, 2)
                for _ in range(branch_count):
                    if len(crack_points) > 2:
                        # 从主裂缝上随机选一点作为分支起点
                        branch_idx = random.randint(1, len(crack_points) - 2)
                        branch_start = crack_points[branch_idx]

                        # 分支属性
                        branch_length = random.randint(3, 5)
                        branch_angle = random.uniform(0, 2 * math.pi)
                        branch_end = (
                            branch_start[0] + branch_length * math.cos(branch_angle),
                            branch_start[1] + branch_length * math.sin(branch_angle)
                        )

                        # 绘制分支
                        branch_color = (80, 80, 100, 60)  # 略淡于主裂缝
                        pygame.draw.line(surface, branch_color,
                                         branch_start, branch_end, 1)

    def _draw_lava_floor(self, rect, surface):
        anim_time = pygame.time.get_ticks()

        # 为每个地板格子提供唯一且固定的随机种子
        tile_x, tile_y = rect.x // TILE_SIZE, rect.y // TILE_SIZE
        tile_seed = hash((tile_x, tile_y, self.floor))

        # 岩浆基底颜色动态变化 - 使用anim_time确保动画流畅
        lava_color = (
            200 + int(55 * math.sin(anim_time / 300)),
            80 + int(40 * math.cos(anim_time / 400)),
            0,
            200
        )
        pygame.draw.rect(surface, lava_color, rect)

        # 岩浆流动纹理 - 基于固定随机种子
        random.seed(tile_seed)
        flow_seeds = [(random.randint(2, TILE_SIZE - 2), random.randint(0, 39)) for _ in range(8)]
        random.seed()  # 重置随机种子

        # 使用固定起点，但动态偏移
        for i, (base_x, offset) in enumerate(flow_seeds):
            flow_x = rect.left + base_x
            flow_y = rect.top + ((anim_time // 30 + offset) % (TILE_SIZE + 40))
            pygame.draw.line(surface, (255, 140, 0),
                             (flow_x, flow_y - 5), (flow_x, flow_y + 5), 3)

        # 随机气泡 - 基于时间和位置的伪随机
        bubble_chance = (anim_time // 100 + tile_x * 17 + tile_y * 23) % 100
        if bubble_chance < 10:  # 10%概率出现气泡
            # 对每个瓦片使用固定的气泡位置，但随时间变化
            random.seed(tile_seed + (anim_time // 500))  # 每500ms变化一次
            bubble_x = rect.left + random.randint(5, TILE_SIZE - 5)
            bubble_y = rect.top + random.randint(5, TILE_SIZE - 5)
            bubble_size = random.randint(2, 4)
            random.seed()  # 重置随机种子

            # 气泡内部
            pygame.draw.circle(surface, (255, 200, 50),
                               (bubble_x, bubble_y), bubble_size)
            # 气泡高光
            pygame.draw.circle(surface, (255, 255, 200),
                               (bubble_x - 1, bubble_y - 1), bubble_size // 2)

        # 岩浆边缘结壳效果 - 基于瓦片的固定位置
        # 每个瓦片最多3个结壳点，位置固定
        random.seed(tile_seed)
        num_crusts = random.randint(0, 3)
        crust_positions = []

        for _ in range(num_crusts):
            crust_x = rect.left + random.randint(2, TILE_SIZE - 5)
            crust_y = rect.top + random.randint(2, TILE_SIZE - 5)
            crust_size = random.randint(4, 8)
            crack_offset_x = random.randint(-3, 3)
            crack_offset_y = random.randint(-3, 3)
            crust_positions.append((crust_x, crust_y, crust_size, crack_offset_x, crack_offset_y))

        random.seed()  # 重置随机种子

        # 绘制结壳，使其随时间略微变化但保持位置
        for crust_x, crust_y, crust_size, crack_dx, crack_dy in crust_positions:
            # 结壳颜色随时间轻微变化
            brightness = int(20 * math.sin(anim_time / 1000))
            crust_color = (100 + brightness, 40 + brightness // 2, 0)
            pygame.draw.rect(surface, crust_color,
                             (crust_x, crust_y, crust_size, crust_size), 1)

            # 裂纹
            crack_x = crust_x + crust_size // 2
            crack_y = crust_y + crust_size // 2
            # 裂纹位置保持固定，但可能随时间轻微变化
            pygame.draw.line(surface, (150, 50, 0),
                             (crack_x, crack_y), (crack_x + crack_dx, crack_y + crack_dy), 1)

    def _draw_hell_floor(self, rect, surface):
        """绘制地狱地板 - 修复随机性问题"""
        # 为每个地板格子提供唯一且固定的随机种子
        tile_x, tile_y = rect.x // TILE_SIZE, rect.y // TILE_SIZE
        tile_seed = hash((tile_x, tile_y, self.floor))
        anim_time = pygame.time.get_ticks()

        # 焦黑基底 - 更暗淡的色调
        base_color = (60, 30, 30)
        pygame.draw.rect(surface, base_color, rect)

        # 灰烬效果 - 固定的随机斑点
        random.seed(tile_seed)
        ash_positions = [(
            rect.left + random.randint(2, TILE_SIZE - 2),
            rect.top + random.randint(2, TILE_SIZE - 2),
            random.randint(1, 3),
            (40 + random.randint(0, 20), 20 + random.randint(0, 10), 20 + random.randint(0, 10))
        ) for _ in range(5)]
        random.seed()  # 重置随机种子

        # 绘制灰烬
        for ash_x, ash_y, ash_size, ash_color in ash_positions:
            pygame.draw.circle(surface, ash_color, (ash_x, ash_y), ash_size)

        # 裂纹 - 固定位置
        random.seed(tile_seed + 1)  # 不同的种子以产生不同的裂纹模式
        crack_positions = [(
            rect.left + random.randint(2, TILE_SIZE - 2),
            rect.top + random.randint(2, TILE_SIZE - 2),
            random.randint(-8, 8),
            random.randint(-8, 8)
        ) for _ in range(3)]
        random.seed()  # 重置随机种子

        # 绘制裂纹
        for start_x, start_y, dx, dy in crack_positions:
            pygame.draw.line(surface, (80, 40, 40),
                             (start_x, start_y), (start_x + dx, start_y + dy), 2)

        # 随机火焰 - 只在特定瓦片上出现，位置固定
        # 但动画效果随时间变化
        random.seed(tile_seed)
        has_flame = random.random() < 0.2  # 20%概率有火焰
        flame_base_x = rect.centerx + random.randint(-2, 2)
        flame_h = random.randint(8, 15)
        flame_w = random.randint(6, 10)
        random.seed()  # 重置随机种子

        if has_flame:
            # 火焰位置轻微抖动，但基于固定位置
            flame_x = flame_base_x + int(2 * math.sin(anim_time / 100))

            # 火焰高度随时间变化，使其看起来在燃烧
            current_height = flame_h * (0.7 + 0.3 * math.sin(anim_time / 200))

            # 火焰形状 - 稍微抖动但基本固定
            flame_points = [
                (flame_x, rect.bottom - current_height),
                (flame_x - flame_w // 2, rect.bottom - current_height // 2),
                (flame_x - flame_w // 3, rect.bottom - current_height // 3),
                (flame_x + flame_w // 3, rect.bottom - current_height // 3),
                (flame_x + flame_w // 2, rect.bottom - current_height // 2)
            ]

            # 火焰颜色 - 由内到外渐变，并随时间变化
            inner_brightness = 200 + int(55 * math.sin(anim_time / 150))
            inner_color = (255, inner_brightness, 0)  # 内部明亮颜色
            outer_color = (139, 0, 0)  # 外部暗红色

            # 绘制外部火焰
            pygame.draw.polygon(surface, outer_color, flame_points)

            # 内部火焰 - 稍小，并且颜色更加活跃
            inner_points = []
            for i, point in enumerate(flame_points):
                inner_x = flame_x + (point[0] - flame_x) * 0.7
                inner_y = rect.bottom - (rect.bottom - point[1]) * 0.7
                inner_points.append((inner_x, inner_y))

            pygame.draw.polygon(surface, inner_color, inner_points)

            # 火焰中心 - 最亮，随时间闪烁
            center_brightness = 150 + int(105 * math.sin(anim_time / 100))
            center_x = flame_x
            center_y = rect.bottom - current_height * 0.6
            pygame.draw.circle(surface, (255, center_brightness, 0),
                               (int(center_x), int(center_y)), 2)

    def _is_in_fountain_room(self, x, y):
        """检查位置是否在喷泉房间内"""
        if not self.fountain_room:
            return False
        fr = self.fountain_room
        return (fr['x1'] <= x < fr['x2'] and fr['y1'] <= y < fr['y2'])

    def _is_near_fountain_center(self, x, y):
        """检查位置是否靠近喷泉中心"""
        if not self.fountain_room:
            return False
        center = self.fountain_room['center']
        return abs(x - center[0]) <= 1 and abs(y - center[1]) <= 1

    def _is_in_lava_room(self, x, y):
        """检查位置是否在岩浆房间内"""
        if not self.lava_room:
            return False
        lr = self.lava_room
        return (lr['x1'] <= x < lr['x2'] and lr['y1'] <= y < lr['y2'])

    # ----------------------- 右侧绘画怪物动态属性面板 -----------------------
    def draw_side_panel(self):
        panel = self.side_panel
        panel.fill((30, 30, 40))  # 深蓝灰底色

        # 标题设计
        title_font = pygame.font.SysFont("SimHei", 24, bold=True)
        title = title_font.render("附近敌方单位", True, (255, 80, 80))
        panel.blit(title, (20, 20))

        # 分割线
        pygame.draw.line(panel, (80, 80, 100), (10, 60), (SIDEBAR_WIDTH - 10, 60), 2)

        if self.nearby_monsters:
            content_y = 80
            info_font = pygame.font.SysFont("SimSun", 20)

            for i, monster in enumerate(self.nearby_monsters):
                m = monster
                # 怪物名称（动态颜色）
                name_color = (255, 120, 120) if "巨龙" in m.name else (160, 220, 255)
                name_text = info_font.render(f"{i + 1}. {m.name}", True, name_color)
                panel.blit(name_text, (20, content_y))

                # ATK显示（带火焰图标）
                atk_surface = pygame.Surface((200, 30), pygame.SRCALPHA)
                pygame.draw.rect(atk_surface, (200, 50, 50, 100), (0, 5, 200, 20))  # 红色背景条
                atk_text = info_font.render(f"ATK：{m.atk}", True, (255, 180, 180))
                atk_surface.blit(atk_text, (0, 0))
                # 添加火焰图标
                fire_icon = [
                    (180, 5), (185, 0), (190, 5),
                    (185, 10), (180, 5)
                ]
                pygame.draw.polygon(atk_surface, (255, 80, 0), fire_icon)
                panel.blit(atk_surface, (20, content_y + 30))

                # DEF显示（带盾牌图标）
                def_surface = pygame.Surface((200, 30), pygame.SRCALPHA)
                pygame.draw.rect(def_surface, (50, 100, 200, 100), (0, 5, 200, 20))  # 蓝色背景条
                def_text = info_font.render(f"DEF：{m.defense}", True, (180, 200, 255))
                def_surface.blit(def_text, (0, 0))
                # 盾牌图标
                shield_points = [
                    (180, 8), (185, 5), (190, 8),
                    (190, 15), (185, 18), (180, 15)
                ]
                pygame.draw.polygon(def_surface, (200, 200, 200), shield_points)
                panel.blit(def_surface, (20, content_y + 70))

                # HP显示（动态进度条）
                hp_width = 200
                hp_bg = pygame.Surface((hp_width, 25), pygame.SRCALPHA)
                pygame.draw.rect(hp_bg, (50, 50, 50, 150), (0, 0, hp_width, 20), border_radius=5)
                pygame.draw.rect(hp_bg, (200, 50, 50, 200),
                                 (0, 0, hp_width * (m.hp / (m.hp + 100)), 20),  # 比例显示
                                 border_radius=5)
                hp_text = info_font.render(f"HP：{m.hp}", True, (255, 120, 120))
                hp_bg.blit(hp_text, (5, 2))
                panel.blit(hp_bg, (20, content_y + 110))

                # 分割线（每个怪物信息之间）
                pygame.draw.line(panel, (80, 80, 100),
                                 (10, content_y + 150), (SIDEBAR_WIDTH - 10, content_y + 150), 1)

                # 更新下一个怪物的起始位置
                content_y += 160
        else:
            prompt_font = pygame.font.SysFont("SimHei", 24)
            prompt = prompt_font.render("附近无敌方单位", True, (150, 150, 180))
            panel.blit(prompt, (SIDEBAR_WIDTH // 2 - 90, 200))

        # 添加到主屏幕右侧
        self.screen.blit(panel, (SCREEN_WIDTH - SIDEBAR_WIDTH, 0))

    # 右侧玩家状态栏及日志
    def draw_left_panel(self):
        panel_width = SIDEBAR_WIDTH
        panel = pygame.Surface((panel_width, SCREEN_HEIGHT), pygame.SRCALPHA)
        panel.fill((30, 30, 40, 200))  # 半透明深蓝灰底色

        # 动态布局参数
        current_y = int(panel_width * 0.05)  # 当前绘制Y坐标 - 基于面板宽度的百分比
        section_gap = int(panel_width * 0.025)  # 模块间距 - 基于面板宽度的百分比
        module_padding = int(panel_width * 0.038)  # 模块内边距 - 基于面板宽度的百分比

        # 内容区域宽度 - 适配面板宽度
        content_width = panel_width - (module_padding * 2)

        # ------ 状态栏标题 ------
        title_font_size = int(panel_width * 0.09)  # 字体大小基于面板宽度
        title_font = pygame.font.SysFont("SimHei", title_font_size, bold=True)
        title = title_font.render("勇者状态", True, (255, 215, 0))
        title_rect = title.get_rect(midtop=(panel_width / 2, current_y))
        panel.blit(title, title_rect)
        current_y += title_rect.height + int(panel_width * 0.06)  # 标题高度+间距（基于百分比）

        # ------ 核心属性区域 ------
        attr_height = int(panel_width * 0.38)  # 基于宽度的百分比
        attr_bg = pygame.Surface((content_width, attr_height), pygame.SRCALPHA)
        attr_bg.fill((40, 40, 60, 150))
        pygame.draw.rect(attr_bg, (80, 80, 100), (0, 0, content_width, attr_height), 2)

        # 数值显示
        info_font_size = int(panel_width * 0.075)  # 字体大小基于面板宽度
        info_font = pygame.font.SysFont("SimSun", info_font_size, bold=True)

        # 计算文本垂直间距
        text_y_gap = attr_height // 5

        # 计算文本起始x坐标 - 基于面板宽度的百分比
        text_x = int(content_width * 0.15)

        attr_bg.blit(info_font.render(f"ATK: {self.player.atk}", True, (255, 180, 180)),
                     (text_x, text_y_gap - info_font_size // 2))
        attr_bg.blit(info_font.render(f"DEF: {self.player.defense}", True, (180, 200, 255)),
                     (text_x, 2 * text_y_gap - info_font_size // 2))

        hp_color = (50, 200, 50)
        attr_bg.blit(info_font.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, hp_color),
                     (text_x, 3 * text_y_gap - info_font_size // 2))
        mp_color = (50, 150, 255)
        attr_bg.blit(info_font.render(f"MP: {self.player.mp}/{self.player.max_mp}", True, mp_color),
                     (text_x, 4 * text_y_gap - info_font_size // 2))
        # 居中放置属性背景
        panel.blit(attr_bg, (module_padding, current_y))
        current_y += attr_height + section_gap

        # ------ 金币和楼层信息 ------
        meta_height = int(panel_width * 0.19)  # 基于宽度的百分比
        meta_bg = pygame.Surface((content_width, meta_height), pygame.SRCALPHA)
        meta_bg.fill((60, 60, 80, 150))
        pygame.draw.rect(meta_bg, (80, 80, 100), (0, 0, content_width, meta_height), 2)

        # 金币和楼层信息的水平间距 - 基于背景宽度划分
        coin_section_width = content_width // 2
        floor_section_width = content_width // 2

        # 垂直居中
        icon_y = meta_height // 2

        # 金币图标尺寸 - 基于面板宽度
        coin_radius = int(panel_width * 0.045)
        coin_x = int(coin_section_width * 0.2)

        # 金币图标
        pygame.draw.circle(meta_bg, (255, 215, 0), (coin_x, icon_y), coin_radius)
        pygame.draw.line(meta_bg, (200, 160, 0),
                         (coin_x - coin_radius // 2, icon_y),
                         (coin_x + coin_radius // 2, icon_y),
                         max(1, coin_radius // 4))

        # 金币数量
        coin_text = info_font.render(f"{self.player.coins}", True, (255, 215, 0))
        coin_text_pos = (coin_x + coin_radius * 1.5, icon_y - info_font_size // 2)
        meta_bg.blit(coin_text, coin_text_pos)

        # 楼层图标尺寸 - 基于面板宽度
        floor_icon_size = int(panel_width * 0.11)
        floor_x = coin_section_width + int(floor_section_width * 0.2)

        # 楼层图标
        floor_icon_rect = pygame.Rect(
            floor_x,
            icon_y - floor_icon_size // 2,
            floor_icon_size,
            floor_icon_size
        )
        pygame.draw.rect(meta_bg, (147, 112, 219), floor_icon_rect, border_radius=floor_icon_size // 5)

        # 楼层数字
        floor_text = info_font.render(f"{self.floor}F", True, (200, 180, 255))
        floor_text_pos = (floor_x + floor_icon_size * 1.2, icon_y - info_font_size // 2)
        meta_bg.blit(floor_text, floor_text_pos)

        panel.blit(meta_bg, (module_padding, current_y))
        current_y += meta_height + section_gap

        # ------ 装备信息区域 ------
        equip_height = int(panel_width * 0.38)  # 基于宽度的百分比
        equip_bg = pygame.Surface((content_width, equip_height), pygame.SRCALPHA)
        equip_bg.fill((40, 40, 60, 150))
        pygame.draw.rect(equip_bg, (80, 80, 100), (0, 0, content_width, equip_height), 2)

        # 字体设置 - 基于宽度的百分比
        eq_font_size = int(panel_width * 0.06)
        dur_font_size = int(panel_width * 0.05)  # 耐久度字体小一号
        eq_font = pygame.font.SysFont("SimSun", eq_font_size)
        dur_font = pygame.font.SysFont("SimSun", dur_font_size)

        # 内边距和栏位尺寸 - 基于容器尺寸的百分比
        padding_x = int(content_width * 0.08)
        padding_y = int(equip_height * 0.1)
        item_height = (equip_height - padding_y * 3) // 2  # 两个装备项目，平均分配高度

        # 耐久度条参数 - 基于容器尺寸
        bar_width = int(content_width * 0.4)
        bar_height = max(1, int(panel_width * 0.03))
        bar_radius = max(1, int(bar_height * 0.25))

        # 武器信息
        weapon = self.player.equipped_weapon
        weapon_text = f"武: {weapon['name']}" if weapon else "武: 无"
        weapon_color = (200, 200, 200) if weapon else (150, 150, 150)

        # 武器名称文本
        weapon_label = eq_font.render(weapon_text, True, weapon_color)
        equip_bg.blit(weapon_label, (padding_x, padding_y))

        # 武器耐久度显示
        if weapon:
            # 耐久度条位置计算
            bar_y = padding_y + eq_font_size + padding_y // 2

            # 耐久度条背景
            pygame.draw.rect(equip_bg, (60, 60, 60),
                             (padding_x, bar_y, bar_width, bar_height),
                             border_radius=bar_radius)

            # 计算耐久度百分比
            max_dur = EQUIPMENT_TYPES[weapon['tag']]['durability']
            dur_percent = weapon['durability'] / max_dur

            # 确定耐久度颜色
            if dur_percent > 0.6:
                dur_color = (50, 200, 50)  # 绿色
            elif dur_percent > 0.3:
                dur_color = (220, 220, 50)  # 黄色
            else:
                dur_color = (200, 50, 50)  # 红色

            # 绘制耐久度条
            if dur_percent > 0:  # 确保有耐久度时才绘制
                pygame.draw.rect(equip_bg, dur_color,
                                 (padding_x, bar_y,
                                  int(bar_width * dur_percent), bar_height),
                                 border_radius=bar_radius)

            # 显示耐久度数值
            dur_text = f"耐久: {weapon['durability']}/{max_dur}"
            dur_label = dur_font.render(dur_text, True, dur_color)

            # 耐久度文本放在条形图右侧
            text_x = padding_x + bar_width + padding_x // 2
            text_y = bar_y - (dur_font_size - bar_height) // 2
            equip_bg.blit(dur_label, (text_x, text_y))

        # 护甲信息 - 第二行
        armor = self.player.equipped_armor
        armor_text = f"甲: {armor['name']}" if armor else "甲: 无"
        armor_color = (200, 200, 200) if armor else (150, 150, 150)

        # 计算护甲信息的Y坐标 - 位于容器一半高度处
        armor_y = equip_height // 2 + padding_y // 2

        # 护甲名称文本
        armor_label = eq_font.render(armor_text, True, armor_color)
        equip_bg.blit(armor_label, (padding_x, armor_y))

        # 护甲耐久度显示
        if armor:
            # 耐久度条位置计算
            bar_y = armor_y + eq_font_size + padding_y // 2

            # 耐久度条背景
            pygame.draw.rect(equip_bg, (60, 60, 60),
                             (padding_x, bar_y, bar_width, bar_height),
                             border_radius=bar_radius)

            # 计算耐久度百分比
            max_dur = EQUIPMENT_TYPES[armor['tag']]['durability']
            dur_percent = armor['durability'] / max_dur

            # 确定耐久度颜色
            if dur_percent > 0.6:
                dur_color = (50, 200, 50)  # 绿色
            elif dur_percent > 0.3:
                dur_color = (220, 220, 50)  # 黄色
            else:
                dur_color = (200, 50, 50)  # 红色

            # 绘制耐久度条
            if dur_percent > 0:  # 确保有耐久度时才绘制
                pygame.draw.rect(equip_bg, dur_color,
                                 (padding_x, bar_y,
                                  int(bar_width * dur_percent), bar_height),
                                 border_radius=bar_radius)

            # 显示耐久度数值
            dur_text = f"耐久: {armor['durability']}/{max_dur}"
            dur_label = dur_font.render(dur_text, True, dur_color)

            # 耐久度文本放在条形图右侧
            text_x = padding_x + bar_width + padding_x // 2
            text_y = bar_y - (dur_font_size - bar_height) // 2
            equip_bg.blit(dur_label, (text_x, text_y))

        panel.blit(equip_bg, (module_padding, current_y))
        current_y += equip_height + section_gap

        # ------ 技能面板（重新设计）------
        skill_height = int(panel_width * 0.75)  # 基于宽度的百分比
        skill_bg = pygame.Surface((content_width, skill_height), pygame.SRCALPHA)
        skill_bg.fill((40, 40, 60, 200))
        pygame.draw.rect(skill_bg, (80, 80, 100), (0, 0, content_width, skill_height), 2)

        # 技能字体尺寸 - 基于宽度
        skill_font_size = int(panel_width * 0.06)
        skill_font = pygame.font.SysFont("SimSun", skill_font_size)
        skill_keys = list(self.player.skills.keys())

        # 技能布局参数 - 基于容器尺寸自适应
        skill_panel_padding = int(content_width * 0.04)
        available_width = content_width - (skill_panel_padding * 3)  # 内容区域减去左右边距
        available_height = skill_height - (skill_panel_padding * 4)  # 内容区域减去上下边距

        # 每行2个技能，共3行
        columns = 2
        rows = 3

        # 计算单个技能区域尺寸
        skill_width = available_width // columns
        skill_height_item = available_height // rows

        # 计算水平和垂直间距
        horizontal_gap = skill_panel_padding
        vertical_gap = skill_panel_padding

        # 绘制技能网格
        for i, key in enumerate(skill_keys):
            if i >= 6:  # 最多显示6个技能
                break

            skill = self.player.skills[key]

            # 计算技能在网格中的位置
            row = i // columns  # 每行2个技能
            col = i % columns  # 0或1列

            # 计算技能绘制的起始位置
            skill_x = skill_panel_padding + col * (skill_width + horizontal_gap // 2)
            skill_y = skill_panel_padding + row * (skill_height_item + vertical_gap // 2)

            # 计算冷却状态
            cd_ratio = skill['current_cd'] / skill['cooldown'] if skill['current_cd'] > 0 else 0
            name_color = (255, 255, 0) if cd_ratio == 0 else (100, 100, 100)

            # 技能名区域 - 适配文本长度
            key_name = pygame.key.name(skill['key']).upper()
            key_text = f"{key_name}: {skill['name']}"
            skill_label = skill_font.render(key_text, True, name_color)

            # 绘制技能名称和按键
            skill_bg.blit(skill_label, (skill_x, skill_y))

            # 冷却条尺寸 - 基于技能区域尺寸
            cooldown_width = int(skill_width * 0.85)  # 条宽为技能区块的85%
            cooldown_height = max(1, int(skill_height_item * 0.15))  # 高度为技能区块的15%
            cooldown_y = skill_y + skill_font_size + skill_panel_padding // 2

            # 绘制冷却条
            pygame.draw.rect(skill_bg, (80, 80, 80),
                             (skill_x, cooldown_y, cooldown_width, cooldown_height),
                             border_radius=cooldown_height // 3)

            if cd_ratio < 1:  # 只有当冷却不完全时才绘制前景条
                pygame.draw.rect(skill_bg, (0, 200, 0),
                                 (skill_x, cooldown_y,
                                  int(cooldown_width * (1 - cd_ratio)), cooldown_height),
                                 border_radius=cooldown_height // 3)

        # ------ 消息日志区域 ------
        # 动态计算日志区域高度 - 使用剩余屏幕空间
        log_height = max(int(panel_width * 0.5), SCREEN_HEIGHT - current_y - int(panel_width * 0.08))
        log_bg = pygame.Surface((content_width, log_height), pygame.SRCALPHA)
        log_bg.fill((40, 40, 60, 200))
        pygame.draw.rect(log_bg, (80, 80, 100), (0, 0, content_width, log_height), 2)

        # 日志字体大小 - 基于面板宽度
        log_font_size = int(panel_width * 0.06)
        log_font = pygame.font.SysFont("SimSun", log_font_size)

        # 计算可见行数 - 基于日志区域高度和字体大小
        log_line_height = int(log_font_size * 1.2)  # 行高略大于字体大小，增加可读性
        visible_line_count = (log_height - module_padding * 2) // log_line_height

        # 获取最近的消息
        visible_messages = self.message_log[-min(visible_line_count, self.max_log_lines):]

        # 绘制消息
        for i, msg in enumerate(visible_messages):
            # 颜色逻辑保持不变
            text_surface = log_font.render(msg, True, self._get_message_color(msg))

            # 计算文本位置 - 保持适当边距
            text_x = module_padding
            text_y = module_padding + i * log_line_height

            # 确保文本不会超出日志区域
            if text_y + log_font_size < log_height - module_padding:
                log_bg.blit(text_surface, (text_x, text_y))

        panel.blit(log_bg, (module_padding, current_y))

        # 绘制到主屏幕左侧 (基于地图尺寸自适应)
        panel_x = MAP_WIDTH * TILE_SIZE
        self.screen.blit(panel, (panel_x, 0))


    def _get_message_color(self, msg):
        """根据消息类型返回颜色"""
        if "获得" in msg.lower():
            return (50, 200, 50)  # 绿色
        elif "伤害" in msg.lower():
            return (200, 50, 50)  # 红色
        elif "释放" in msg.lower():
            return (255, 215, 0)  # 金色
        elif "传送" in msg:
            return (100, 200, 255)  # 蓝色
        return (200, 200, 200)  # 默认灰色

    def draw_equipment(self, item):
        """绘制优化后的装备图像，保持单位格的比例一致"""
        x = item.x * TILE_SIZE
        y = item.y * TILE_SIZE
        anim_time = pygame.time.get_ticks()

        # 统一装备中心点与尺寸比例
        center_x = x + TILE_SIZE // 2
        center_y = y + TILE_SIZE // 2
        item_scale = min(TILE_SIZE - 6, 30)  # 装备基础尺寸，确保不会溢出格子

        # 根据装备类型确定基础参数
        is_weapon = "SWORD" in item.item_type or "DAGGER" in item.item_type or "SPEAR" in item.item_type
        is_armor = "ARMOR" in item.item_type

        # --------- 武器类 ---------
        if is_weapon:
            # 基础武器参数
            blade_length = item_scale * 0.75
            blade_width = item_scale * 0.18
            handle_length = item_scale * 0.4
            handle_width = item_scale * 0.12

            # 武器朝向 - 右上角
            angle = -30 if "DAGGER" in item.item_type else -45
            blade_dir = pygame.math.Vector2(math.cos(math.radians(angle)), math.sin(math.radians(angle)))

            # 计算刀刃终点
            blade_end = (
                center_x + blade_dir.x * blade_length,
                center_y + blade_dir.y * blade_length
            )

            # 计算刀柄终点 - 方向相反
            handle_end = (
                center_x - blade_dir.x * handle_length,
                center_y - blade_dir.y * handle_length
            )

            # 根据特定武器类型进行定制
            if item.item_type == "WOOD_SWORD":
                # 木剑 - 简朴的棕色系
                # 剑柄
                pygame.draw.line(self.screen, (101, 67, 33), (center_x, center_y), handle_end, int(handle_width))
                # 护手
                guard_width = handle_width * 2.5
                guard_dir = pygame.math.Vector2(-blade_dir.y, blade_dir.x)  # 垂直于剑身方向
                guard_start = (center_x + guard_dir.x * guard_width / 2, center_y + guard_dir.y * guard_width / 2)
                guard_end = (center_x - guard_dir.x * guard_width / 2, center_y - guard_dir.y * guard_width / 2)
                pygame.draw.line(self.screen, (139, 69, 19), guard_start, guard_end, int(handle_width * 0.8))
                # 剑身
                pygame.draw.line(self.screen, (160, 120, 80), (center_x, center_y), blade_end, int(blade_width))
                # 剑身纹理
                texture_dir = pygame.math.Vector2(blade_dir.x * 0.9, blade_dir.y * 0.9)
                texture_length = blade_length * 0.8
                texture_pos = (
                center_x + texture_dir.x * texture_length / 3, center_y + texture_dir.y * texture_length / 3)
                pygame.draw.line(self.screen, (139, 69, 19), texture_pos,
                                 (texture_pos[0] + texture_dir.x * texture_length / 2,
                                  texture_pos[1] + texture_dir.y * texture_length / 2), 1)

            # 绘制格斯大剑
            elif item.item_type == "GUTS_GREATSWORD":
                # 调整绘制位置让剑居中
                x = item.x * TILE_SIZE + TILE_SIZE // 3  # 稍微右移一点
                y = item.y * TILE_SIZE + TILE_SIZE // 10  # 稍微下移

                # 剑身 - 更窄更短
                blade_color = (60, 60, 60)  # 深灰色的剑身
                blade_width = TILE_SIZE // 3  # 更窄的剑身
                blade_length = TILE_SIZE * 0.65  # 更短的剑身

                # 剑身主体 - 用多边形绘制
                blade_points = [
                    (x, y + TILE_SIZE * 0.1),  # 左上
                    (x + blade_width, y + TILE_SIZE * 0.1),  # 右上
                    (x + blade_width, y + TILE_SIZE * 0.1 + blade_length),  # 右下
                    (x, y + TILE_SIZE * 0.1 + blade_length)  # 左下
                ]
                pygame.draw.polygon(self.screen, blade_color, blade_points)

                # 剑尖 - 三角形
                tip_points = [
                    (x, y + TILE_SIZE * 0.1),  # 左上连接点
                    (x + blade_width, y + TILE_SIZE * 0.1),  # 右上连接点
                    (x + blade_width // 2, y),  # 尖端
                ]
                pygame.draw.polygon(self.screen, blade_color, tip_points)

                # 剑刃高光
                pygame.draw.line(self.screen, (120, 120, 120),
                                 (x, y + TILE_SIZE * 0.1),
                                 (x, y + TILE_SIZE * 0.1 + blade_length), 2)

                # 剑身中央凹槽
                groove_x = x + blade_width // 3
                pygame.draw.line(self.screen, (40, 40, 40),
                                 (groove_x, y + TILE_SIZE * 0.15),
                                 (groove_x, y + TILE_SIZE * 0.1 + blade_length - 0.05 * TILE_SIZE), 2)

                # 护手 - 紧凑一些
                guard_width = blade_width + TILE_SIZE // 6  # 小一点的护手
                guard_height = TILE_SIZE // 7  # 更扁的护手
                guard_y = y + TILE_SIZE * 0.1 + blade_length
                pygame.draw.rect(self.screen, (100, 70, 40),
                                 (x - (guard_width - blade_width) // 2,
                                  guard_y,
                                  guard_width, guard_height))

                # 剑柄 - 短而粗
                hilt_width = blade_width // 2
                hilt_height = TILE_SIZE // 5  # 更短的剑柄
                hilt_y = guard_y + guard_height
                pygame.draw.rect(self.screen, (80, 50, 30),
                                 (x + blade_width // 2 - hilt_width // 2,
                                  hilt_y,
                                  hilt_width, hilt_height))

                # 剑柄纹理
                for i in range(2):  # 减少纹理线条
                    wrap_y = hilt_y + i * (hilt_height // 2) + hilt_height // 4
                    pygame.draw.line(self.screen, (60, 40, 20),
                                     (x + blade_width // 2 - hilt_width // 2, wrap_y),
                                     (x + blade_width // 2 + hilt_width // 2, wrap_y), 1)

                # 剑柄结尾球形装饰 - 小一点
                pommel_radius = hilt_width // 2
                pommel_y = hilt_y + hilt_height + pommel_radius // 2
                pygame.draw.circle(self.screen, (120, 100, 50),
                                   (x + blade_width // 2, pommel_y), pommel_radius)

                # 血迹效果(可选)
                if random.random() < 0.3:  # 30%概率显示血迹
                    blood_points = []
                    for _ in range(2):  # 减少血迹数量
                        blood_x = x + random.randint(0, int(blade_width))
                        blood_y = y + TILE_SIZE * 0.1 + random.randint(0, int(blade_length))
                        blood_points.append((blood_x, blood_y))
                        pygame.draw.circle(self.screen, (139, 0, 0, 150),
                                           (blood_x, blood_y), random.randint(1, 2))  # 更小的血迹

            elif "DAGGER" in item.item_type:
                # 匕首系列 - 更短、更锋利
                blade_color = (192, 192, 192)  # 默认钢色
                handle_color = (101, 67, 33)  # 默认木质手柄

                if "BRONZE" in item.item_type:
                    blade_color = (184, 115, 51)  # 青铜色
                elif "STEEL" in item.item_type:
                    blade_color = (200, 200, 210)  # 钢色
                    if "FINE" in item.item_type:
                        blade_color = (220, 220, 230)  # 精钢更亮

                # 匕首刀刃 - 小型三角形
                blade_points = [
                    center_x, center_y,
                    blade_end[0] - blade_dir.y * blade_width / 2, blade_end[1] + blade_dir.x * blade_width / 2,
                    blade_end[0], blade_end[1],
                    blade_end[0] + blade_dir.y * blade_width / 2, blade_end[1] - blade_dir.x * blade_width / 2
                ]
                # 转换为坐标点列表
                point_list = []
                for i in range(0, len(blade_points), 2):
                    point_list.append((blade_points[i], blade_points[i + 1]))
                pygame.draw.polygon(self.screen, blade_color, point_list)

                # 匕首手柄
                pygame.draw.line(self.screen, handle_color, (center_x, center_y), handle_end, int(handle_width))

                # 装饰物
                if "FINE" in item.item_type:
                    # 宝石装饰
                    pygame.draw.circle(self.screen, (255, 0, 0),
                                       (int(handle_end[0] + (center_x - handle_end[0]) * 0.3),
                                        int(handle_end[1] + (center_y - handle_end[1]) * 0.3)),
                                       int(handle_width * 0.8))

                # 刀刃闪光
                if anim_time % 800 < 400:
                    glint_pos = (blade_end[0] - blade_dir.x * blade_length * 0.3,
                                 blade_end[1] - blade_dir.y * blade_length * 0.3)
                    pygame.draw.circle(self.screen, (255, 255, 255),
                                       (int(glint_pos[0]), int(glint_pos[1])), 2)

            elif "SWORD" in item.item_type:
                # 定义剑的基本颜色
                blade_color = (160, 160, 170)  # 默认剑刃色
                handle_color = (101, 67, 33)  # 默认木质手柄
                guard_color = (184, 115, 51)  # 默认护手色

                # 根据具体类型定制颜色
                if "COPPER" in item.item_type:
                    blade_color = (184, 115, 51)  # 铜色
                elif "IRON" in item.item_type:
                    blade_color = (180, 180, 190)  # 铁色
                    if "FINE" in item.item_type:
                        blade_color = (200, 200, 210)  # 精铁更亮
                        guard_color = (220, 220, 100)  # 金色护手

                # 绘制剑刃
                pygame.draw.line(self.screen, blade_color, (center_x, center_y), blade_end, int(blade_width))

                # 护手 - 更大更明显
                guard_width = blade_width * 3  # 更宽的护手
                guard_dir = pygame.math.Vector2(-blade_dir.y, blade_dir.x)  # 垂直于剑身方向
                guard_start = (center_x + guard_dir.x * guard_width / 2, center_y + guard_dir.y * guard_width / 2)
                guard_end = (center_x - guard_dir.x * guard_width / 2, center_y - guard_dir.y * guard_width / 2)
                pygame.draw.line(self.screen, guard_color, guard_start, guard_end, int(blade_width * 0.8))

                # 剑柄
                pygame.draw.line(self.screen, handle_color, (center_x, center_y), handle_end, int(handle_width))

                # 特殊装饰和效果

            elif "SPEAR" in item.item_type:
                spear_dir = pygame.math.Vector2(0.1, -0.9).normalize()  # 垂直略带倾斜
                spear_length = item_scale * 1.2  # 更长的矛
                spear_width = item_scale * 0.08  # 更细的矛杆
                spear_end = (center_x + spear_dir.x * spear_length,
                             center_y + spear_dir.y * spear_length)
                handle_end = (center_x - spear_dir.x * handle_length,
                              center_y - spear_dir.y * handle_length)
                pygame.draw.line(self.screen, (101, 67, 33), (center_x, center_y), handle_end, int(handle_width * 0.8))
                pygame.draw.line(self.screen, (110, 95, 70), (center_x, center_y), spear_end, int(spear_width))

                spear_head_size = spear_width * 2  # 更小的矛头
                perp_dir = pygame.math.Vector2(-spear_dir.y, spear_dir.x)
                tip_length = spear_width * 5  # 矛尖长度
                side_width = spear_width * 1.5  # 侧面宽度
                tip_point = spear_end  # 矛尖
                back_point = (spear_end[0] - spear_dir.x * tip_length,
                              spear_end[1] - spear_dir.y * tip_length)  # 矛尾
                left_point = (back_point[0] + perp_dir.x * side_width,
                              back_point[1] + perp_dir.y * side_width)  # 左侧
                right_point = (back_point[0] - perp_dir.x * side_width,
                               back_point[1] - perp_dir.y * side_width)  # 右侧

                spear_head_points = [tip_point, left_point, back_point, right_point]
                pygame.draw.polygon(self.screen, (180, 180, 190), spear_head_points)
                pygame.draw.line(self.screen, (100, 100, 110),
                                 spear_end,
                                 back_point, 1)
                # 装饰带 - 在手柄下方
                band_pos_y = center_y - spear_dir.y * handle_length * 0.3
                band_pos_x = center_x - spear_dir.x * handle_length * 0.3
                band_dir = perp_dir  # 垂直于矛杆
                band_start = (band_pos_x + band_dir.x * handle_width * 0.8,
                              band_pos_y + band_dir.y * handle_width * 0.8)
                band_end = (band_pos_x - band_dir.x * handle_width * 0.8,
                            band_pos_y - band_dir.y * handle_width * 0.8)
                pygame.draw.line(self.screen, (180, 0, 0), band_start, band_end, 2)
                # 小金属链接件 - 在矛头与杆连接处
                connector_pos = (back_point[0] + spear_dir.x * 2,
                                 back_point[1] + spear_dir.y * 2)
                pygame.draw.circle(self.screen, (160, 140, 60),
                                   (int(connector_pos[0]), int(connector_pos[1])),
                                   int(spear_width * 0.8))

        # --------- 护甲类 ---------
        elif is_armor:
            armor_width = item_scale * 0.8
            armor_height = item_scale * 1.0

            # 基础护甲轮廓
            armor_rect = pygame.Rect(
                center_x - armor_width / 2,
                center_y - armor_height / 2,
                armor_width, armor_height
            )

            # 基本颜色与材质
            primary_color = (100, 100, 110)  # 默认护甲颜色
            accent_color = (150, 150, 160)  # 装饰颜色

            if "WOOD" in item.item_type:
                primary_color = (101, 67, 33)  # 木色
                accent_color = (139, 69, 19)  # 深木色
            elif "COPPER" in item.item_type:
                primary_color = (184, 115, 51)  # 铜色
                accent_color = (150, 90, 40)  # 深铜色
            elif "IRON" in item.item_type:
                primary_color = (120, 120, 130)  # 铁色
                accent_color = (90, 90, 100)  # 深铁色
            elif "STEEL" in item.item_type:
                primary_color = (180, 180, 190)  # 钢色
                accent_color = (140, 140, 150)  # 深钢色

            # 闪电护甲特殊处理
                # 红色闪电甲
            if item.item_type == "LIGHTNING_ARMOR_RED":
                # 盔甲基底
                armor_color = (139, 0, 0) if (anim_time % 1000 < 500) else (178, 34, 34)
                pygame.draw.rect(self.screen, armor_color,
                                 (x + 5, y + 5, 22, 22), border_radius=5)

                # 闪电核心纹路
                lightning_points = [
                    (x + 15, y + 8), (x + 20, y + 15),
                    (x + 15, y + 22), (x + 10, y + 15)
                ]
                pygame.draw.polygon(self.screen, (255, 50, 50), lightning_points)

                # 动态电弧效果
                for i in range(3):
                    angle = anim_time / 200 + i * 120
                    start = (x + 15 + math.cos(math.radians(angle)) * 8,
                             y + 15 + math.sin(math.radians(angle)) * 8)
                    end = (start[0] + random.randint(-5, 5),
                           start[1] + random.randint(-5, 5))
                    pygame.draw.line(self.screen, (255, 100, 100),
                                     start, end, 2)

            # 蓝色闪电甲
            elif item.item_type == "LIGHTNING_ARMOR_BLUE":
                # 盔甲基底
                base_color = (30, 144, 255)
                glow_color = (100, 149, 237) if (anim_time % 800 < 400) else (70, 130, 180)

                # 多层渐变
                for i in range(3):
                    alpha = 200 - i * 50
                    layer = pygame.Surface((22, 22), pygame.SRCALPHA)
                    pygame.draw.rect(layer, (*base_color, alpha),
                                     (0, 0, 22, 22), border_radius=5 - i * 2)
                    self.screen.blit(layer, (x + 5 + i, y + 5 + i))

                # 冰裂纹效果
                for _ in range(8):
                    crack_start = (x + 5 + random.randint(2, 20),
                                   y + 5 + random.randint(2, 20))
                    crack_end = (crack_start[0] + random.randint(-4, 4),
                                 crack_start[1] + random.randint(-4, 4))
                    pygame.draw.line(self.screen, (200, 230, 255),
                                     crack_start, crack_end, 1)

                # 闪电核心
                core_points = [
                    (x + 16, y + 8), (x + 22, y + 16), (x + 16, y + 24),
                    (x + 10, y + 16), (x + 16, y + 8)
                ]
                pygame.draw.polygon(self.screen, (30, 144, 255), core_points, 2)

            # 黄色闪电甲
            elif item.item_type == "LIGHTNING_ARMOR_YELLOW":
                # 黄金基底
                gold_color = (218, 165, 32)
                pygame.draw.rect(self.screen, gold_color,
                                 (x + 5, y + 5, 22, 22), border_radius=5)

                # 浮雕装饰
                pygame.draw.rect(self.screen, (139, 69, 19),
                                 (x + 9, y + 9, 14, 14), border_radius=3)

                # 动态闪电
                for i in range(3):
                    phase = (anim_time + i * 300) % 1000
                    if phase < 500:
                        alpha = int(255 * (1 - phase / 500))
                        lightning_points = [
                            (x + 5 + phase // 25, y + 5),
                            (x + 20, y + 15),
                            (x + 5 + phase // 25, y + 25)
                        ]
                        pygame.draw.lines(self.screen, (255, 215, 0, alpha),
                                          False, lightning_points, 3)

                # 神圣光晕
                if anim_time % 1000 < 500:
                    halo = pygame.Surface((30, 30), pygame.SRCALPHA)
                    radius = 15 + int(5 * math.sin(anim_time / 200))
                    pygame.draw.circle(halo, (255, 255, 0, 50),
                                       (15, 15), radius)
                    self.screen.blit(halo, (x - 2, y - 2))
            else:
                # 非闪电护甲标准绘制
                pygame.draw.rect(self.screen, primary_color, armor_rect, border_radius=int(armor_width * 0.15))

                # 添加装饰条纹
                stripe_count = 3
                stripe_height = armor_height / (stripe_count + 1)

                for i in range(stripe_count):
                    stripe_y = armor_rect.y + (i + 1) * stripe_height
                    pygame.draw.line(self.screen, accent_color,
                                     (armor_rect.x + armor_width * 0.2, stripe_y),
                                     (armor_rect.x + armor_width * 0.8, stripe_y),
                                     max(1, int(armor_width * 0.06)))

                # 铆钉装饰
                rivet_size = max(1, int(armor_width * 0.08))
                for i in range(2):
                    for j in range(2):
                        rivet_x = armor_rect.x + armor_width * (0.25 + i * 0.5)
                        rivet_y = armor_rect.y + armor_height * (0.25 + j * 0.5)
                        pygame.draw.circle(self.screen, (200, 200, 200), (int(rivet_x), int(rivet_y)), rivet_size)

                # 特殊材质效果
                if "WOOD" in item.item_type:
                    # 木纹
                    for i in range(4):
                        grain_y = armor_rect.y + i * armor_height / 4 + armor_height / 8
                        grain_curve = math.sin(i + anim_time / 2000) * armor_width / 8
                        pygame.draw.line(self.screen, (139, 69, 19),
                                         (armor_rect.x + armor_width * 0.2, grain_y + grain_curve),
                                         (armor_rect.x + armor_width * 0.8, grain_y - grain_curve),
                                         1)

                elif "COPPER" in item.item_type:
                    # 铜锈斑点
                    if anim_time % 2000 < 1000:
                        for _ in range(3):
                            patina_x = armor_rect.x + random.uniform(0, armor_width)
                            patina_y = armor_rect.y + random.uniform(0, armor_height)
                            pygame.draw.circle(self.screen, (0, 150, 100),
                                               (int(patina_x), int(patina_y)),
                                               max(1, int(armor_width * 0.06)))

    def draw(self):
        # 绘制静态背景
        self.screen.blit(self.background_surface, (0, 0))

        # 绘制向上的楼梯
        self.draw_stairs(self.screen, self.exit_pos[0] * TILE_SIZE, self.exit_pos[1] * TILE_SIZE, TILE_SIZE)

        self.draw_fountain_room()

        # 绘制路径
        self.draw_path()

        # 绘制技能特效
        for effect in self.skill_effects:
            effect.draw(self.screen)

        # 绘制中毒屏幕特效
        if pygame.time.get_ticks() < self.player_debuff['poison_end']:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            alpha = int(50 + 50 * math.sin(pygame.time.get_ticks() / 200))
            overlay.fill((50, 205, 50, alpha))
            self.screen.blit(overlay, (0, 0))
        # 绘制眩晕效果
        if pygame.time.get_ticks() < self.player_debuff.get('stun_end', 0):
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((255, 255, 0, 50))  # 半透明黄色
            self.screen.blit(overlay, (0, 0))
        # 红色恐惧特效
        if self.red_fear:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            # 整体红晕
            overlay.fill((150, 0, 0, 30))
            self.screen.blit(overlay, (0, 0))
        # 纯青闪电特效
        if self.blue_fear:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            # 整体蓝晕
            overlay.fill((0, 0, 150, 30))
            self.screen.blit(overlay, (0, 0))

        # 金色闪电特效
        if self.gold_fear:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            # 整体金晕
            overlay.fill((255, 215, 0, 30))
            self.screen.blit(overlay, (0, 0))

        for item in self.items:

            self.draw_equipment(item)
            self.draw_item_with_rarity(item)

        for monster in self.monsters:
            x = monster.x * TILE_SIZE
            y = monster.y * TILE_SIZE
            w = monster.size[0] * TILE_SIZE
            h = monster.size[1] * TILE_SIZE
            # ---------- 各怪物专属造型 ----------
            # 小蝙蝠
            if "蝙蝠" in monster.name:
                self.draw_bat(monster)
                continue

            # 骷髅
            elif "骷髅" in monster.name:
                self.draw_skeleton(monster)
                continue

            # 史莱姆
            elif "史莱姆" in monster.name:
                self.draw_slim(monster)
                continue

            elif "腐蚀怪" in monster.name:
                self.draw_corrosion_monster(monster)
                continue

            elif "魔法师" in monster.name:
                self.draw_magician_evil(monster)
                continue

            elif "魔王" in monster.name:
                self.draw_monster_knight_boss(monster)
                continue

            elif "火焰骑士" in monster.name:
                self.draw_fire_knight(monster)
                continue

            elif "普通巨龙" in monster.name:
                self.draw_dragon_boss(monster)
                continue

            elif "电击球" in monster.name:
                self.draw_lightning_ball(monster)
                continue

            elif "冰霜巨龙" in monster.name:
                self.draw_dragon_ice(monster)
                continue

            elif "闪电" in monster.name:
                self.draw_lightning_boss(monster)
                self.lightning_balls = []
                continue

            elif "火焰领主" in monster.name:
                self.draw_fire_lord(monster)

            elif "神圣灾祸骑士" in monster.name:
                self.draw_holy_knight(monster, holy_ball_count= monster.num_balls)
                continue

            # 默认怪物造型（史莱姆等）
            else:
                pygame.draw.ellipse(self.screen, COLOR_MONSTER,
                                    (x + 2, y + 2, w - 4, h - 4))
                # 危险标识
                pygame.draw.line(self.screen, (255, 0, 0),
                                 (x + w * 0.2, y + h * 0.2),
                                 (x + w * 0.8, y + h * 0.8), 2)
                pygame.draw.line(self.screen, (255, 0, 0),
                                 (x + w * 0.8, y + h * 0.2),
                                 (x + w * 0.2, y + h * 0.8), 2)

        self.draw_player()  # 绘制玩家

        for ball in self.guardian_lightning_balls: # 绘制守护闪电球
            ball.draw(self.screen)

        self.draw_path()  # 绘制传送路径

        self.draw_side_panel()  # 右侧边栏怪物信息系统

        self.draw_left_panel()  # 绘制左侧面板

        # ---------------------------- 开场动画 --------------------------

        if self.is_animating:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 255))  # 不透明黑色背景
            pygame.draw.circle(overlay, (0, 0, 0, 0),  # 完全透明的圆
                               self.animation_center,
                               int(self.animation_radius))
            self.screen.blit(overlay, (0, 0))

        # 腐蚀效果绘制
        for effect in self.corrosion_effects:
            effect.draw(self.screen)

        # 绘制离子火花
        for p in self.fear_particles:
            if 'color' in p:  # 离子火花有颜色属性
                alpha = int(255 * (p['life'] / p['max_life']))  # 根据生命周期计算透明度
                pygame.draw.circle(self.screen, p['color'],
                                   (int(p['pos'][0]), int(p['pos'][1])),
                                   int(p['size']))

        pygame.display.flip()

    # 检查所有占据的格子是否可通行
    def can_monster_move_to(self, monster, new_x, new_y):
        """检查怪物能否移动到(new_x, new_y)位置"""
        # 检查所有占据的格子是否可通行
        for dx in range(monster.size[0]):
            for dy in range(monster.size[1]):
                x = new_x + dx
                y = new_y + dy

                # 检查边界
                if not (0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT):
                    return False

                # 检查地形
                if self.maze[y][x] in [1, 2, 3, 4]:  # 墙壁和特殊地形
                    return False

                # 检查是否会与玩家重叠
                if x == self.player.x and y == self.player.y:
                    return False

        # 检查与其他怪物的碰撞
        for other in self.monsters:
            if other is monster:
                continue

            # 计算双方的覆盖区域
            if (new_x < other.x + other.size[0] and
                    new_x + monster.size[0] > other.x and
                    new_y < other.y + other.size[1] and
                    new_y + monster.size[1] > other.y):
                return False

        return True

    def is_position_empty(self, x, y):
        """检查目标位置是否为空（没有怪物、道具、墙壁）"""
        if not self.is_walkable(x, y):
            return False
        for monster in self.monsters:
            if (x, y) == (monster.x, monster.y):
                return False
        for item in self.items:
            if (x, y) == (item.x, item.y):
                return False
        return True

    def find_path(self, start, end):
        """使用BFS算法查找从start到end的路径，不能穿越怪物方块"""
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 上下左右
        queue = deque([start])
        visited = {start: None}  # 记录访问过的节点及其父节点

        # 获取所有怪物位置
        monster_positions = set()
        for m in self.monsters:
            for dx in range(m.size[0]):
                for dy in range(m.size[1]):
                    monster_positions.add((m.x + dx, m.y + dy))

        while queue:
            current = queue.popleft()
            if current == end:
                # 重建路径
                path = []
                while current is not None:
                    path.append(current)
                    current = visited[current]
                return path[::-1]  # 反转路径

            for dx, dy in directions:
                next_pos = (current[0] + dx, current[1] + dy)
                if (0 <= next_pos[0] < MAP_WIDTH and
                        0 <= next_pos[1] < MAP_HEIGHT and
                        self.is_walkable(next_pos[0], next_pos[1]) and
                        next_pos not in visited and
                        next_pos not in monster_positions):  # 检查是否在怪物位置
                    queue.append(next_pos)
                    visited[next_pos] = current

        return None  # 没有找到路径

    def handle_mouse_click(self, pos):
        """处理鼠标点击事件"""
        if self.player_debuff['frozen_area']:
            self.add_message("寒冰束缚无法传送！")
            return
        if pygame.time.get_ticks() < self.player_debuff.get('stun_end', 0):
            self.add_message("眩晕中无法传送！")
            return
        if pygame.time.get_ticks() < self.player_debuff.get('paralyze_end', 0):
            self.add_message("麻痹状态无法传送！")
            return
        if self.player_debuff['in_corrosion']:
            self.add_message("腐蚀区域无法传送！")
            return
        if self.red_fear:
            self.add_message("红色恐惧笼罩，无法传送！")
            return
        if self.blue_fear:
            self.add_message("青蓝恐惧笼罩，无法传送！")
            return
        if self.gold_fear:
            self.add_message("金色恐惧笼罩，无法传送！")
            return
        # 将屏幕坐标转换为地图坐标
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE

        # 检查目标位置是否合法
        if not (0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT):
            self.add_message("地图范围外！")
            return

        # 检查目标位置是否为空
        if not self.is_position_empty(x, y):
            self.add_message("该区块被占据！")
            return

        # 查找路径
        start = (self.player.x, self.player.y)
        end = (x, y)
        path = self.find_path(start, end)

        if path:
            # 记录路径并开始计时
            self.path = path
            self.path_timer = PATHTIME  * 30
            # 传送玩家
            self.player.x, self.player.y = x, y
            self.add_message(f"传送至 ({x}, {y})")
        else:
            self.add_message("无法抵达！")

    # ------------- 游戏运行 -----------
    def run(self):
        while True:
            dt = self.clock.tick(60) / 1000  # 获取帧间隔时间（秒），并转换为秒
            if self.game_state == "menu":
                action = self.handle_main_menu()
                if action == "settings":
                    self.game_state = "settings"
            elif self.game_state == "settings":
                action = self.handle_settings()
                if action == "menu":
                    self.game_state = "menu"
                elif action == "apply":
                    self.restart_game()
            elif self.game_state == "playing":
                self.handle_game_loop(dt)
            elif self.game_state == "dead":
                self.handle_death_screen()

    def handle_main_menu(self):
        """处理主菜单的更新和绘制"""
        dt = self.clock.tick(60) / 1000  # 获取以秒为单位的帧时间

        # 更新菜单状态
        self.main_menu.update(dt)

        # 绘制菜单
        button_rects = self.main_menu.draw()

        # 处理输入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键点击
                    # 检查开始按钮
                    if self.main_menu.start_button['rect'].collidepoint(event.pos):
                        # 按钮按下效果
                        self.main_menu.start_button['active'] = True
                        self.game_state = "playing"
                        return "playing"
                    # 检查设置按钮
                    elif self.main_menu.settings_button['rect'].collidepoint(event.pos):
                        # 按钮按下效果
                        self.main_menu.settings_button['active'] = True
                        self.game_state = "settings"
                        return "settings"
            elif event.type == pygame.MOUSEBUTTONUP:
                # 重置按钮状态
                self.main_menu.start_button['active'] = False
                self.main_menu.settings_button['active'] = False

        # 更新显示
        pygame.display.flip()

        return "menu"  # 继续在主菜单状态

    def handle_settings(self):
        settings_menu = SettingsMenu(self.screen)
        return settings_menu.run()

    def restart_game(self):
        self.apply_config()
        self.__init__()  # 重新初始化游戏

    def handle_game_loop(self, dt):
        # 原有游戏主循环逻辑
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if pygame.time.get_ticks() < self.player_debuff.get('stun_end', 0):  # 动画期间跳过输入处理
                    self.add_message("眩晕中无法移动")
                    continue
                if pygame.time.get_ticks() < self.player_debuff.get('paralyze_end', 0):  # 动画期间跳过输入处理
                    self.add_message("麻痹中无法移动")
                    continue
                if event.key == pygame.K_b:
                    shop_screen(self.screen, self.player, self.floor)
                if event.key == pygame.K_n:
                    self.show_encyclopedia()
                elif event.key == pygame.K_w:
                    self.player.move(0, -1, self)
                elif event.key == pygame.K_s:
                    self.player.move(0, 1, self)
                elif event.key == pygame.K_a:
                    self.player.move(-1, 0, self)
                elif event.key == pygame.K_d:
                    self.player.move(1, 0, self)
                # 技能释放
                for skill in self.player.skills:
                    if event.key == self.player.skills[skill]['key']:
                        self.cast_skill(skill)
            elif event.type == pygame.MOUSEBUTTONDOWN:  # 处理鼠标点击
                if event.button == 1:  # 左键点击
                    self.handle_mouse_click(event.pos)

        # 玩家死亡检测
        if self.player.hp <= 0:
            self.game_state = "dead"
            self.death_screen = DeathScreen(self.screen, self.player, self.floor)

        # 更新动画状态
        if self.is_animating:
            self.animation_radius += self.animation_speed * dt  # 更新动画半径
            if self.animation_radius >= self.animation_max_radius / 8:
                self.is_animating = False  # 动画结束
        else:
            self.update()  # 动画结束后更新游戏逻辑

        self.draw()  # 绘制游戏画面

    def handle_death_screen(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    button_rect = self.death_screen.draw()
                    if button_rect.collidepoint(event.pos):
                        self.game_state = "menu"
                        self.__init__()  # 重置游戏

        if self.game_state == "dead":
            self.death_screen.draw()
        pygame.display.flip()


# -------- 程序入口 --------
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("魔塔地牢")
    game = Game()
    game.run()
