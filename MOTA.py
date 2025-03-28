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

 # --------------------------- 实体列表 ------------------------------

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
     "attack_range": 2, "attack_speed": 0.4, "coin": 1200, "speed": 60, "level": 7},
    {"name": "冰霜巨龙", "HP": 5500, "ATK": 130, "DEF": 55, "size": (3, 3),
     "attack_range": 3, "attack_speed": 0.5, "coin": 1300, "speed": 60, "level": 8},
    {"name": "血腥闪电", "HP": 6000, "ATK": 200, "DEF": 110, "size": (3, 3),
     "attack_range": 4, "attack_speed": 0.3, "coin": 1500, "speed": 30, "level": 7},
    {"name": "纯青闪电", "HP": 7000, "ATK": 300, "DEF": 130, "size": (3, 3),
     "attack_range": 4, "attack_speed": 0.4, "coin": 2000, "speed": 30, "level": 8},
    {"name": "金色闪电", "HP": 8000, "ATK": 400, "DEF": 150, "size": (3, 3),
     "attack_range": 4, "attack_speed": 0.5, "coin": 2500, "speed": 30, "level": 9},
    {"name": "火焰领主", "HP": 6500, "ATK": 130, "DEF": 60, "size": (3, 3),
     "attack_range": 3, "attack_speed": 0.6, "coin": 1500, "speed": 60, "level": 7},
    {"name": "纯火焰领主", "HP": 7500, "ATK": 180, "DEF": 80, "size": (3, 3),
     "attack_range": 3, "attack_speed": 0.7, "coin": 1900, "speed": 50, "level": 8},
    {"name": "神圣灾祸骑士", "HP": 10000, "ATK": 250, "DEF": 180, "size": (3, 3),
     "attack_range": 7, "attack_speed": 0.7, "coin": 3000, "speed": 40, "level": 9}
]

# 道具类型
ITEM_TYPES = ["CHEST", "HP_SMALL", "HP_LARGE", "ATK_GEM", "DEF_GEM"]

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
        """更新动画和状态"""
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


# ----------------- 玩家类 -------------------

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 100000
        self.max_hp = 100000
        self.base_atk = 25  # 基础攻击力
        self.base_defense = 25000  # 基础防御力
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
                'key': pygame.K_f
            },
            'LightningEffect': {
                'name': "闪电链",
                'cooldown': 3,
                'current_cd': 0,
                'range': 8,
                'max_targets': 3,
                'damage_multiple': 1.8,
                'effect': LightningEffect,
                'key': pygame.K_e
            },
            'HolyBallEffect': {
                'name': "神圣球",
                'cooldown': 8,
                'current_cd': 0,
                'seek_range': 10,
                'ball_count': 6,
                'damage_multiple': 2.5,
                'effect': HolyBallEffect,
                'key': pygame.K_c
            },
            'TripleAttack': {
                'name': "三连斩",
                'cooldown': 6,
                'current_cd': 0,
                'range': 2,
                'damage_multipliers': [0.8, 1.0, 1.5],  # 三连斩伤害系数
                'effect': TripleAttack,
                'key': pygame.K_q
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
                'key': pygame.K_z
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
                'key': pygame.K_x
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
        self.window_height = 530
        self.window_x = (self.screen_width - self.window_width) // 2
        self.window_y = (self.screen_height - self.window_height) // 2

        # 字体和颜色 - 使用支持中文的字体
        try:
            # 尝试使用系统中文字体，调整字体大小
            self.title_font = pygame.font.SysFont("SimHei", 40, bold=True)  # 黑体标题
            self.item_font = pygame.font.SysFont("SimSun", 24)  # 宋体项目
            self.info_font = pygame.font.SysFont("SimSun", 20)  # 宋体描述
            self.price_font = pygame.font.SysFont("SimSun", 22, bold=True)  # 价格专用字体
        except:
            # 回退到默认字体
            self.title_font = pygame.font.Font(None, 48)
            self.item_font = pygame.font.Font(None, 32)
            self.info_font = pygame.font.Font(None, 28)
            self.price_font = pygame.font.Font(None, 30)

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

        # 商品项目列表
        self.items = [
            {
                "name": f"生命药剂",
                "description": f"恢复 {1000 * floor} 点生命值",
                "price": 100 * floor,
                "key": pygame.K_1,
                "label": "1",
                "icon": self._create_potion_icon((255, 0, 0)),  # 红色药水
                "action": self._buy_small_hp
            },
            {
                "name": f"力量宝石",
                "description": f"永久提升 {5 * floor} 点攻击力",
                "price": 100 * floor,
                "key": pygame.K_2,
                "label": "2",
                "icon": self._create_gem_icon((255, 100, 100)),  # 红色宝石
                "action": self._buy_small_atk
            },
            {
                "name": f"护盾宝石",
                "description": f"永久提升 {5 * floor} 点防御力",
                "price": 100 * floor,
                "key": pygame.K_3,
                "label": "3",
                "icon": self._create_gem_icon((100, 100, 255)),  # 蓝色宝石
                "action": self._buy_small_def
            },
            {
                "name": f"大生命药剂",
                "description": f"恢复 {10000 * floor} 点生命值",
                "price": 1000 * floor,
                "key": pygame.K_4,
                "label": "4",
                "icon": self._create_potion_icon((200, 0, 0), large=True),  # 深红色大药水
                "action": self._buy_large_hp
            },
            {
                "name": f"高级力量宝石",
                "description": f"永久提升 {50 * floor} 点攻击力",
                "price": 1000 * floor,
                "key": pygame.K_5,
                "label": "5",
                "icon": self._create_gem_icon((255, 50, 50), large=True),  # 深红色大宝石
                "action": self._buy_large_atk
            },
            {
                "name": f"高级护盾宝石",
                "description": f"永久提升 {50 * floor} 点防御力",
                "price": 1000 * floor,
                "key": pygame.K_6,
                "label": "6",
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

    def _add_shop_particle(self):
        """添加商店魔法粒子效果 - 已禁用"""
        pass

    def _update_particles(self, dt):
        """更新粒子效果 - 已禁用"""
        # 粒子效果已被禁用，此函数保留以维持接口一致性
        pass

    def _draw_item_card(self, item, x, y, width, height, hovered=False):
        """绘制商品卡片"""
        # 基础卡片背景
        card_color = self.COLOR_HIGHLIGHT if hovered else (50, 50, 70)
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(self.screen, card_color, card_rect, border_radius=8)
        pygame.draw.rect(self.screen, self.COLOR_BORDER, card_rect, 2, border_radius=8)

        # 物品图标 - 位置调整
        icon_rect = item['icon'].get_rect(topleft=(x + 15, y + (height - item['icon'].get_height()) // 2))
        self.screen.blit(item['icon'], icon_rect)

        # 键位示意
        key_size = 30
        key_rect = pygame.Rect(x + width - key_size - 15, y + 10, key_size, key_size)
        pygame.draw.rect(self.screen, (70, 70, 90), key_rect, border_radius=5)
        pygame.draw.rect(self.screen, self.COLOR_BORDER, key_rect, 1, border_radius=5)

        key_text = self.item_font.render(item['label'], True, self.COLOR_TEXT)
        key_text_rect = key_text.get_rect(center=key_rect.center)
        self.screen.blit(key_text, key_text_rect)

        # 物品名称 - 位置调整
        name_text = self.item_font.render(item['name'], True, self.COLOR_TEXT)
        name_rect = name_text.get_rect(topleft=(x + 60, y + 12))
        self.screen.blit(name_text, name_rect)

        # 物品描述 - 位置调整，颜色变淡
        desc_text = self.info_font.render(item['description'], True, self.COLOR_DESC)
        desc_rect = desc_text.get_rect(topleft=(x + 60, y + 42))
        self.screen.blit(desc_text, desc_rect)

        # 价格（根据玩家能否负担变色）- 移至底部
        affordable = self.player.coins >= item['price']
        price_color = self.COLOR_AFFORDABLE if affordable else self.COLOR_UNAFFORDABLE

        price_text = self.price_font.render(f"{item['price']} 金币", True, price_color)
        price_rect = price_text.get_rect(bottomright=(x + width - 15, y + height - 15))
        self.screen.blit(price_text, price_rect)

        # 金币图标
        coin_radius = 8
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

            # 更新粒子效果
            self._update_particles(dt)

            # 绘制界面
            self._draw_shop(current_time)

            pygame.display.flip()

    def _get_item_rect(self, index):
        """获取商品项目的矩形区域"""
        # 计算行和列
        row = index // 2
        col = index % 2

        # 计算卡片尺寸和位置 - 调整为更适合的尺寸
        card_width = (self.window_width - 80) // 2  # 增加间距
        card_height = 100  # 增加卡片高度，避免文字重叠
        card_x = self.window_x + 30 + col * (card_width + 20)
        card_y = self.window_y + 100 + row * (card_height + 20)

        return pygame.Rect(card_x, card_y, card_width, card_height)

    def _draw_shop(self, current_time):
        """绘制商店界面"""
        # 不使用遮罩，保留游戏背景

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
                        'color': slash['color']
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

        # Calculate slash line endpoints
        length = TILE_SIZE * 1.5
        start_x = pos[0] - math.cos(angle) * length / 2
        start_y = pos[1] - math.sin(angle) * length / 2
        end_x = pos[0] + math.cos(angle) * length / 2
        end_y = pos[1] + math.sin(angle) * length / 2
        alpha = int(255 * effect['time'] / 0.3)

        # Draw main slash line
        pygame.draw.line(
            screen,
            (*color, alpha),
            (int(start_x), int(start_y)),
            (int(end_x), int(end_y)),
            4
        )

        # Add simple hit mark
        pygame.draw.line(
            screen,
            (*color, alpha),
            (int(pos[0] - 5), int(pos[1] - 5)),
            (int(pos[0] + 5), int(pos[1] + 5)),
            3
        )
        pygame.draw.line(
            screen,
            (*color, alpha),
            (int(pos[0] - 5), int(pos[1] + 5)),
            (int(pos[0] + 5), int(pos[1] - 5)),
            3
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
        self.particles = []
        self.duration = 0.3  # 持续时间0.3秒
        # 生成随机闪电路径
        for _ in range(8):
            start = (px * TILE_SIZE + random.randint(5, 25), py * TILE_SIZE + random.randint(5, 25))
            end = (start[0] + random.randint(-20, 20), start[1] + random.randint(-20, 20))
            self.particles.append({
                'start': start,
                'end': end,
                'alpha': 255
            })

    def update(self, dt):
        self.duration -= dt
        for p in self.particles:
            p['alpha'] = max(0, p['alpha'] - 20)
        return self.duration > 0

    def draw(self, screen):
        for p in self.particles:
            color = (255, 255, 0, p['alpha']) if random.random() > 0.3 else (255, 165, 0, p['alpha'])
            pygame.draw.line(screen, color, p['start'], p['end'], 2)


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

    def create_impact_particles(self, game, target, count=10):  # Reduced from 15
        """Create minimal impact particles for a clean, compact effect"""
        # Determine impact center
        if hasattr(target, 'x') and hasattr(target, 'y'):
            impact_center = (target.x * TILE_SIZE + TILE_SIZE // 2,
                             target.y * TILE_SIZE + TILE_SIZE // 2)
        else:
            impact_center = target

        # Colors
        if self.color_scheme == "holy":
            colors = self.primary_colors
            explosion_color = (255, 215, 0)
            core_color = (255, 255, 220)
        else:  # lightning
            colors = self.primary_colors
            explosion_color = (30, 144, 255)
            core_color = (200, 240, 255)

        # Create single ring
        game.fear_particles.append({
            'pos': list(impact_center),
            'vel': [0, 0],
            'life': 0.3,
            'max_life': 0.3,
            'size': 15,
            'color': explosion_color,
            'is_ring': True,
            'ring_width': 2,
            'delay': 0
        })

        # Create flash
        game.fear_particles.append({
            'pos': list(impact_center),
            'vel': [0, 0],
            'life': 0.2,
            'max_life': 0.2,
            'size': 10,
            'color': core_color,
            'is_flash': True
        })

        # Add minimal particles
        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2.5, 10)
            size = random.uniform(1.5, 3)
            life = random.uniform(0.2, 0.7)

            particle = {
                'pos': [impact_center[0], impact_center[1]],
                'vel': [math.cos(angle) * speed, math.sin(angle) * speed],
                'life': life,
                'max_life': life,
                'size': size,
                'color': random.choice(colors),
                'gravity': 0,  # No gravity for cleaner effect
                'rotation': None  # No rotation for simpler particles
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
            holy_beam.create_impact_particles(game, target)

            game.add_message(f"神圣光球对{target.name}造成{int(actual_damage)}点伤害!")
            self.attack_cooldown = 1.0 / self.attack_speed  # 设置冷却时间

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

                # 根据技能类型选择颜色
                if self.is_monster_skill:
                    color = (255, 215, 0, alpha)  # 怪物技能偏金色
                else:
                    color = (0, 191, 255, alpha) if i % 2 == 0 else (100, 180, 255, alpha)

                pygame.draw.circle(temp_surf, color, (radius, radius), radius)
                screen.blit(temp_surf, (int(self.position[0] - radius), int(self.position[1] - radius)))

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
                    # 根据释放者选择不同颜色
                    if self.is_monster_skill:
                        line_color = (255, 215, 0, int(255 * life_ratio))  # 金色
                    else:
                        line_color = (150, 220, 255, int(255 * life_ratio))  # 蓝色

                    pygame.draw.line(screen, line_color, points[i], points[i + 1],
                                     max(1, int(3 * life_ratio)))


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

    # 法师毒液球


class PoisonBall:
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
        self.particles = []  # 腐蚀粒子效果
        # 初始化腐蚀粒子
        for _ in range(20):
            self.particles.append({
                'pos': (x * TILE_SIZE + random.randint(2, 29), y * TILE_SIZE + random.randint(2, 29)),
                'size': random.randint(2, 4),
                'alpha': 255,
                'speed': (random.uniform(-0.5, 0.5), random.uniform(-0.5, 0.5))
            })

    def update(self, current_time):
        # 更新粒子状态
        for p in self.particles:
            p['pos'] = (p['pos'][0] + p['speed'][0], p['pos'][1] + p['speed'][1])
            p['alpha'] = max(0, 255 - (current_time - self.create_time) * 85 // 1000)  # 3秒淡出
        return current_time - self.create_time < 3000  # 3秒后消失

    def draw(self, screen):
        # 绘制基底腐蚀效果
        base_alpha = max(0, 200 - (pygame.time.get_ticks() - self.create_time) // 15)
        base_rect = pygame.Rect(self.x * TILE_SIZE, self.y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(screen, (91, 13, 133, base_alpha), base_rect)  # 紫黑色基底

        # 绘制动态腐蚀粒子
        for p in self.particles:
            if p['alpha'] > 0:
                pygame.draw.circle(screen, (139, 0, 0, p['alpha']),  # 深红色粒子
                                   (int(p['pos'][0]), int(p['pos'][1])), p['size'])

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
        self.max_log_lines = 40  # 最大显示消息行数

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

        # ------ 基础造型参数 ------
        body_color = (30, 144, 255)  # 盔甲蓝色
        skin_color = (255, 218, 185)  # 肤色
        boots_color = (105, 105, 105)  # 靴子深灰
        sword_color = (192, 192, 192)  # 剑银灰色
        sword_highlights = (230, 230, 230)

        # ------ 头部绘制 ------
        head_radius = TILE_SIZE // 6
        pygame.draw.circle(self.screen, skin_color,
                           (px + TILE_SIZE // 2, py + head_radius + 2), head_radius)
        # 面部特征
        pygame.draw.arc(self.screen, (0, 0, 0),
                        (px + TILE_SIZE // 2 - head_radius, py + 2,
                         head_radius * 2, head_radius * 2),
                        math.radians(200), math.radians(340), 1)  # 微笑曲线

        # ------ 身体躯干 ------
        torso_height = TILE_SIZE // 3
        torso_rect = (px + TILE_SIZE // 4, py + head_radius * 2 + 4,
                      TILE_SIZE // 2, torso_height)
        pygame.draw.rect(self.screen, body_color, torso_rect)

        # ------ 腿部造型 ------
        leg_width = TILE_SIZE // 8
        # 左腿
        pygame.draw.rect(self.screen, boots_color,
                         (px + TILE_SIZE // 2 - leg_width * 2, py + torso_height + head_radius * 2 + 4,
                          leg_width, TILE_SIZE // 3))
        # 右腿
        pygame.draw.rect(self.screen, boots_color,
                         (px + TILE_SIZE // 2 + leg_width, py + torso_height + head_radius * 2 + 4,
                          leg_width, TILE_SIZE // 3))

        # ------ 手臂动态造型 ------
        arm_length = TILE_SIZE // 3
        # 左臂（握剑姿势）
        pygame.draw.line(self.screen, skin_color,
                         (px + TILE_SIZE // 4, py + head_radius * 2 + torso_height // 2),
                         (px + TILE_SIZE // 4 - arm_length // 2,
                          py + head_radius * 2 + torso_height // 2 + arm_length // 2),
                         3)
        # 右臂（自然下垂）
        pygame.draw.line(self.screen, skin_color,
                         (px + TILE_SIZE - TILE_SIZE // 4, py + head_radius * 2 + torso_height // 2),
                         (px + TILE_SIZE - TILE_SIZE // 4 + arm_length // 3,
                          py + head_radius * 2 + torso_height // 2 + arm_length // 3),
                         3)

        # ------ 精致长剑造型 ------
        sword_x = px + TILE_SIZE // 4 - arm_length // 2  # 剑柄起始位置
        sword_y = py + head_radius * 2 + torso_height // 2 + arm_length // 2

        # 剑刃（带渐细效果）
        blade_points = [
            (sword_x - 1, sword_y),
            (sword_x - TILE_SIZE // 3, sword_y - TILE_SIZE // 2),  # 剑尖
            (sword_x + 1, sword_y),
            (sword_x + TILE_SIZE // 8, sword_y + TILE_SIZE // 8)
        ]
        pygame.draw.polygon(self.screen, sword_color, blade_points)

        # 剑柄装饰
        hilt_rect = (sword_x - 2, sword_y - 3, 4, 6)
        pygame.draw.rect(self.screen, (139, 69, 19), hilt_rect)  # 木柄颜色
        pygame.draw.circle(self.screen, (255, 215, 0),  # 宝石装饰
                           (sword_x, sword_y - 1), 2)

        # 剑刃高光
        pygame.draw.line(self.screen, sword_highlights,
                         (sword_x - TILE_SIZE // 4, sword_y - TILE_SIZE // 3),
                         (sword_x - TILE_SIZE // 8, sword_y - TILE_SIZE // 6), 1)

        # ------ 盔甲细节 ------
        # 肩甲
        pygame.draw.arc(self.screen, (255, 255, 255),
                        (px + TILE_SIZE // 4 - 2, py + head_radius * 2 + 2,
                         TILE_SIZE // 2 + 4, torso_height // 2),
                        math.radians(180), math.radians(360), 2)
        # 腰带
        pygame.draw.rect(self.screen, (139, 69, 19),
                         (px + TILE_SIZE // 4, py + head_radius * 2 + torso_height - 3,
                          TILE_SIZE // 2, 3))

    # --------------- 玩家技能释放 -----------------

    def cast_skill(self, skill_key):
        skill = self.player.skills[skill_key]
        if skill['current_cd'] > 0:
            self.add_message(f"{skill['name']}冷却中!")
            return

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
        """更新所有怪物的状态和位置"""
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
        """绘制闪电BOSS（支持血腥、纯青、金色三种配色）"""
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
        body_color = (54, 54, 54)  # 身体颜色 深灰色
        wing_color = (40, 40, 40)  # 翅膀颜色 更深的灰色
        skeleton_color = (80, 80, 80)  # 骨架颜色

        # 颜色随机反转
        if "白色" in monster.name:
            body_color = self.color_reverse(body_color)
            wing_color = self.color_reverse(wing_color)
            skeleton_color = self.color_reverse(skeleton_color)

        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE
        # 蝙蝠主体（倒挂姿态）
        head_radius = TILE_SIZE // 6
        body_width = TILE_SIZE // 3
        body_height = TILE_SIZE // 2

        # 倒挂的身体
        pygame.draw.ellipse(self.screen, body_color,
                            (x + TILE_SIZE // 2 - body_width // 2,
                             y + TILE_SIZE // 2 - body_height // 2,
                             body_width, body_height))

        # 头部
        pygame.draw.circle(self.screen, body_color,
                           (x + TILE_SIZE // 2, y + TILE_SIZE // 3),
                           head_radius)

        # 耳朵
        ear_points = [
            (x + TILE_SIZE // 2 - head_radius // 2, y + TILE_SIZE // 3 - head_radius),
            (x + TILE_SIZE // 2, y + TILE_SIZE // 3 - head_radius * 1.5),
            (x + TILE_SIZE // 2 + head_radius // 2, y + TILE_SIZE // 3 - head_radius)
        ]
        pygame.draw.polygon(self.screen, body_color, ear_points)

        # 翅膀（双层设计）
        # 左翼
        left_wing = [
            (x + TILE_SIZE // 4, y + TILE_SIZE // 2),
            (x + TILE_SIZE // 2 - 2, y + TILE_SIZE // 3),
            (x, y + TILE_SIZE // 4)
        ]
        pygame.draw.polygon(self.screen, wing_color, left_wing)
        # 右翼
        right_wing = [
            (x + 3 * TILE_SIZE // 4, y + TILE_SIZE // 2),
            (x + TILE_SIZE // 2 + 2, y + TILE_SIZE // 3),
            (x + TILE_SIZE, y + TILE_SIZE // 4)
        ]
        pygame.draw.polygon(self.screen, wing_color, right_wing)

        # 翅膀骨架（增加细节）
        # 左翼骨架
        pygame.draw.line(self.screen, skeleton_color,
                         left_wing[0], left_wing[1], 2)
        pygame.draw.line(self.screen, skeleton_color,
                         left_wing[1], left_wing[2], 2)
        # 右翼骨架
        pygame.draw.line(self.screen, skeleton_color,
                         right_wing[0], right_wing[1], 2)
        pygame.draw.line(self.screen, skeleton_color,
                         right_wing[1], right_wing[2], 2)

        # 眼睛（红色发光效果）
        eye_radius = 2
        pygame.draw.circle(self.screen, (255, 0, 0),
                           (x + TILE_SIZE // 2 - eye_radius, y + TILE_SIZE // 3 - eye_radius),
                           eye_radius)
        pygame.draw.circle(self.screen, (255, 0, 0),
                           (x + TILE_SIZE // 2 + eye_radius, y + TILE_SIZE // 3 - eye_radius),
                           eye_radius)

        # 阴影效果
        shadow_color = (20, 20, 20)
        pygame.draw.arc(self.screen, shadow_color,
                        (x + TILE_SIZE // 4, y + TILE_SIZE // 2 - 2,
                         TILE_SIZE // 2, TILE_SIZE // 4),
                        math.radians(180), math.radians(360), 2)

    # -------------------- 腐蚀怪绘制 ---------------------
    def draw_corrosion_monster(self, monster):
        # 动态腐蚀肉块造型
        anim_time = pygame.time.get_ticks()
        body_color = (91, 13, 133)  # 紫黑色基底
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE

        # 主体（动态蠕动的椭圆）
        pygame.draw.ellipse(self.screen, body_color,
                            (x + math.sin(anim_time / 300) * 3,
                             y + math.cos(anim_time / 250) * 2,
                             TILE_SIZE, TILE_SIZE))

        # 血色斑点（随机分布）
        for _ in range(8):
            spot_x = x + random.randint(4, 27)
            spot_y = y + random.randint(4, 27)
            pygame.draw.circle(self.screen, (139, 0, 0),
                               (spot_x, spot_y), random.randint(2, 4))

        # 表面蠕动效果
        for i in range(3):
            wave_y = y + TILE_SIZE // 2 + math.sin(anim_time / 200 + i) * 8
            pygame.draw.arc(self.screen, (70, 0, 70),
                            (x + i * 8, wave_y - 4, 16, 8),
                            math.radians(180), math.radians(360), 2)

        # 环境互动：滴落粘液
        if random.random() < 0.05:
            drop_x = x + random.randint(8, 23)
            drop_y = y + TILE_SIZE
            pygame.draw.line(self.screen, (139, 0, 0, 150),
                             (drop_x, drop_y), (drop_x, drop_y + 8), 3)

    # -------------------- 火焰骑士绘制 ---------------------
    def draw_fire_knight(self, monster):
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE
        # 动画参数
        anim_time = pygame.time.get_ticks()
        hammer_swing = math.sin(anim_time / 300) * 0.5  # 锤子摆动弧度
        shield_glow = abs(math.sin(anim_time / 500))  # 盾牌发光强度

        # 基础体型（1x1格子）
        body_color = (30, 30, 30)  # 暗黑基底色
        if "纯" in monster.name:
            body_color = self.color_reverse(body_color)
        body_rect = (x + TILE_SIZE // 4, y + TILE_SIZE // 4, TILE_SIZE // 2, TILE_SIZE // 2)
        pygame.draw.rect(self.screen, body_color, body_rect)

        # 方形头部（较小）
        head_size = TILE_SIZE // 4
        head_center = (x + TILE_SIZE // 2, y + TILE_SIZE // 4)
        # 头盔主体
        pygame.draw.rect(self.screen, (40, 40, 40),
                         (head_center[0] - head_size // 2, head_center[1] - head_size // 2,
                          head_size, head_size))
        # 眼部红光
        pygame.draw.rect(self.screen, (200, 0, 0),
                         (head_center[0] - head_size // 4, head_center[1] - head_size // 6,
                          head_size // 2, head_size // 3))
        # 恶魔之角
        pygame.draw.polygon(self.screen, (60, 60, 60), [
            (head_center[0] - head_size // 2, head_center[1] - head_size // 2),
            (head_center[0] - head_size // 3, head_center[1] - head_size),
            (head_center[0] - head_size // 6, head_center[1] - head_size // 2)
        ])

        # 深渊铠甲系统（紧凑版）
        armor_color = (60, 60, 60)
        if "纯" in monster.name:
            armor_color = self.color_reverse(armor_color)
        # 肩甲
        pygame.draw.rect(self.screen, armor_color,
                         (x + TILE_SIZE // 4, y + TILE_SIZE // 3,
                          TILE_SIZE // 2, TILE_SIZE // 6))
        # 胸甲（带恶魔浮雕）
        pygame.draw.rect(self.screen, armor_color,
                         (x + TILE_SIZE // 3, y + TILE_SIZE // 2,
                          TILE_SIZE // 3, TILE_SIZE // 3))
        # 浮雕细节
        pygame.draw.arc(self.screen, (80, 80, 80),
                        (x + TILE_SIZE // 3 + 2, y + TILE_SIZE // 2 + 2,
                         TILE_SIZE // 3 - 4, TILE_SIZE // 3 - 4),
                        math.radians(0), math.radians(180), 2)

        # 地狱重锤系统（紧凑版）
        hammer_length = TILE_SIZE // 2
        # 锤柄
        pygame.draw.line(self.screen, (70, 70, 70),
                         (x + TILE_SIZE // 2, y + TILE_SIZE // 2),
                         (x + TILE_SIZE // 2 + int(hammer_length * math.cos(hammer_swing)),
                          y + TILE_SIZE // 2 + int(hammer_length * math.sin(hammer_swing))), 4)
        # 锤头
        hammer_head = (x + TILE_SIZE // 2 + int(hammer_length * math.cos(hammer_swing)),
                       y + TILE_SIZE // 2 + int(hammer_length * math.sin(hammer_swing)))
        if "纯" in monster.name:
            pygame.draw.circle(self.screen, (55, 205, 205), hammer_head, 6)
        else:
            pygame.draw.circle(self.screen, (200, 50, 50), hammer_head, 6)

        # 火焰粒子
        if "纯" in monster.name:
            for _ in range(4):
                fx = hammer_head[0] + random.randint(-5, 5)
                fy = hammer_head[1] + random.randint(-5, 5)
                pygame.draw.circle(self.screen, (0, 255-random.randint(100, 150), 255),
                                   (fx, fy), random.randint(1, 2))
        else:
            for _ in range(4):
                fx = hammer_head[0] + random.randint(-5, 5)
                fy = hammer_head[1] + random.randint(-5, 5)
                pygame.draw.circle(self.screen, (255, random.randint(100, 150), 0),
                                   (fx, fy), random.randint(1, 2))

        # 邪能盾牌系统（紧凑版）
        shield_center = (x + TILE_SIZE // 4, y + TILE_SIZE // 2)
        shield_size = TILE_SIZE // 4
        # 基底
        pygame.draw.polygon(self.screen, (80, 80, 80), [
            (shield_center[0], shield_center[1] - shield_size // 2),
            (shield_center[0] + shield_size // 2, shield_center[1]),
            (shield_center[0], shield_center[1] + shield_size // 2),
            (shield_center[0] - shield_size // 2, shield_center[1])
        ])
        # 发光符文
        rune_color = (50, 200, 50, int(200 * shield_glow))
        if "纯" in monster.name:
            rune_color = self.color_reverse(rune_color)
        pygame.draw.polygon(self.screen, rune_color, [
            (shield_center[0], shield_center[1] - shield_size // 4),
            (shield_center[0] + shield_size // 4, shield_center[1]),
            (shield_center[0], shield_center[1] + shield_size // 4),
            (shield_center[0] - shield_size // 4, shield_center[1])
        ], 2)

        # 地面阴影
        shadow = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 80),
                            (x + TILE_SIZE // 4, y + TILE_SIZE // 2,
                             TILE_SIZE // 2, TILE_SIZE // 4))
        self.screen.blit(shadow, (x, y))

    # -------------------- 骷髅绘制 ---------------------
    def draw_skeleton(self, monster):
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE
        # 骨骼颜色
        bone_color = (240, 240, 220)
        worn_color = (180, 180, 160)

        # 头部（带破损）
        head_center = (x + TILE_SIZE // 2, y + TILE_SIZE // 4)
        pygame.draw.circle(self.screen, bone_color, head_center, 10)
        # 眼部空洞
        pygame.draw.circle(self.screen, (30, 30, 30),
                           (head_center[0] - 4, head_center[1] - 2), 3)
        pygame.draw.circle(self.screen, (30, 30, 30),
                           (head_center[0] + 4, head_center[1] - 2), 3)
        # 下颚（动态开合）
        jaw_angle = math.sin(pygame.time.get_ticks() / 300) * 0.2
        jaw_points = [
            (head_center[0] - 8, head_center[1] + 5),
            (head_center[0] + 8, head_center[1] + 5),
            (head_center[0] + 6, head_center[1] + 10 + 3 * jaw_angle),
            (head_center[0] - 6, head_center[1] + 10 + 3 * jaw_angle)
        ]
        pygame.draw.polygon(self.screen, bone_color, jaw_points)

        # 脊椎（带破损效果）
        for i in range(5):
            seg_y = y + TILE_SIZE // 3 + i * 8
            if i % 2 == 0:
                pygame.draw.ellipse(self.screen, worn_color,
                                    (x + TILE_SIZE // 2 - 4, seg_y, 8, 6))
            else:
                pygame.draw.ellipse(self.screen, bone_color,
                                    (x + TILE_SIZE // 2 - 4, seg_y, 8, 6))

        # 肋骨（不对称破损）
        rib_points = [
            (x + TILE_SIZE // 2, y + TILE_SIZE // 2),
            (x + TILE_SIZE // 2 + 15, y + TILE_SIZE // 2 - 10),
            (x + TILE_SIZE // 2 + 10, y + TILE_SIZE // 2 + 20),
            (x + TILE_SIZE // 2 - 15, y + TILE_SIZE // 2 + 15)
        ]
        pygame.draw.polygon(self.screen, bone_color, rib_points, 2)

        # 手臂
        # 右臂
        pygame.draw.line(self.screen, bone_color,
                         (x + TILE_SIZE // 2, y + TILE_SIZE // 2),
                         (x + TILE_SIZE, y + TILE_SIZE // 3), 4)

        # 左臂
        pygame.draw.line(self.screen, bone_color,
                         (x + TILE_SIZE // 2, y + TILE_SIZE // 2),
                         (x, y + TILE_SIZE // 3), 4)

        # 骨盆
        pygame.draw.arc(self.screen, bone_color,
                        (x + TILE_SIZE // 2 - 15, y + TILE_SIZE - 20, 30, 20),
                        math.radians(180), math.radians(360), 4)

        # 飘散的灵魂残片
        for _ in range(3):
            px = x + random.randint(10, TILE_SIZE - 10)
            py = y + random.randint(10, TILE_SIZE - 10)
            pygame.draw.circle(self.screen, (150, 150, 255, 100), (px, py), 2)

    # -------------------- 史莱姆绘制 ---------------------
    def draw_slim(self, monster):
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE
        w = monster.size[0] * TILE_SIZE
        h = monster.size[1] * TILE_SIZE
        # 根据不同类型设置颜色
        if "红" in monster.name:
            base_color = (220, 20, 60)  # 红色
            highlight_color = (255, 99, 71)  # 番茄红
        elif "黑" in monster.name:
            base_color = (35, 35, 35)  # 暗黑色
            highlight_color = (105, 105, 105)  # 暗灰色
        elif "闪光" in monster.name:  # 闪光
            base_color = (50, 205, 50)
            highlight_color = (144, 238, 144)
            if random.random() < 0.6:
                base_color = (220, 20, 60)
                highlight_color = (255, 99, 71)
                if random.random() < 0.5:
                    base_color = (35, 35, 35)
                    highlight_color = (105, 105, 105)
        else:  # 普通史莱姆
            base_color = (50, 205, 50)
            highlight_color = (144, 238, 144)

        # 凝胶状身体
        body_rect = (x + 2, y + 2, w - 4, h - 4)
        pygame.draw.ellipse(self.screen, base_color, body_rect)

        # 高光效果
        pygame.draw.arc(self.screen, highlight_color, body_rect,
                        math.radians(30), math.radians(150), 2)

        # 特殊效果：红史莱姆添加火焰纹，黑史莱姆添加金属反光
        # if "红" in monster.name:
        # 火焰纹效果
        #    flame_points = [
        #        (x + w * 0.3, y + h * 0.7),
        #        (x + w * 0.5, y + h * 0.3),
        #        (x + w * 0.7, y + h * 0.7)
        #    ]
        #    pygame.draw.polygon(self.screen, (255, 165, 0), flame_points)
        if "黑" in monster.name:
            # 金属反光效果
            pygame.draw.line(self.screen, (169, 169, 169),
                             (x + w * 0.3, y + h * 0.3),
                             (x + w * 0.7, y + h * 0.7), 2)

        # 气泡效果（黑史莱姆不显示气泡）
        if "黑" not in monster.name:
            for i in range(3):
                bx = x + random.randint(3, w - 6)
                by = y + random.randint(3, h - 6)
                pygame.draw.circle(self.screen, highlight_color, (bx, by), 1)

    # -------------------- 电击球绘制 ---------------------

    def draw_lightning_ball(self, monster):
        anim_time = pygame.time.get_ticks()
        core_color = (255, 255, 0) if (anim_time // 200) % 2 else (255, 215, 0)  # 核心颜色
        side_tact_color = (255, 255, 100)  # 随机触手颜色
        lightning_curve_color = (255, 255, 0)  # 外围电弧颜色

        if "异色" in monster.name:
            core_color = (204, 0, 204)
            side_tact_color = (51, 51, 255)
            lightning_curve_color = (255, 0, 255)

        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE
        # 动态闪电核心
        pygame.draw.circle(self.screen, core_color,
                           (x + TILE_SIZE // 2, y + TILE_SIZE // 2), TILE_SIZE // 3)

        # 随机闪电触手
        for _ in range(6):
            angle = random.random() * math.pi * 2
            length = random.randint(8, 15)
            start = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)
            end = (start[0] + math.cos(angle) * length,
                   start[1] + math.sin(angle) * length)
            pygame.draw.line(self.screen, side_tact_color, start, end, 2)

        # 外围电弧
        if random.random() > 0.7:
            pygame.draw.arc(self.screen, lightning_curve_color,
                            (x - 5, y - 5, TILE_SIZE + 10, TILE_SIZE + 10),
                            random.random() * math.pi, random.random() * math.pi, 1)

    # -------------------- 魔法师绘制 ---------------------
    def draw_magician_evil(self, monster):
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE
        # 长袍主体
        robe_color = (80, 0, 80)  # 深紫色
        robe_highlight = (120, 0, 120)
        pygame.draw.ellipse(self.screen, robe_color,
                            (x + 5, y + TILE_SIZE // 2, TILE_SIZE - 10, TILE_SIZE))

        # 魔法纹饰
        for i in range(3):
            pygame.draw.arc(self.screen, robe_highlight,
                            (x + i * 5, y + TILE_SIZE // 2 + i * 3,
                             TILE_SIZE - 10, TILE_SIZE - 10),
                            math.radians(0), math.radians(180), 2)

        # 悬浮法杖
        staff_x = x + TILE_SIZE // 2
        staff_y = y + TILE_SIZE // 4
        pygame.draw.line(self.screen, (150, 150, 150),
                         (staff_x - 15, staff_y - 5), (staff_x + 15, staff_y + 5), 5)
        # 魔法水晶
        crystal_color = (0, 200, 200)
        pygame.draw.polygon(self.screen, crystal_color, [
            (staff_x + 15, staff_y + 5),
            (staff_x + 25, staff_y),
            (staff_x + 15, staff_y - 5)
        ])
        # 水晶辉光
        for _ in range(5):
            px = staff_x + 20 + random.randint(-3, 3)
            py = staff_y + random.randint(-3, 3)
            pygame.draw.circle(self.screen, (0, 200, 200, 100), (px, py), 2)

        # 毒雾环绕
        anim_time = pygame.time.get_ticks()
        for i in range(8):
            angle = math.radians(anim_time / 10 + i * 45)
            radius = 20 + 5 * math.sin(anim_time / 200 + i)
            px = x + TILE_SIZE // 2 + radius * math.cos(angle)
            py = y + TILE_SIZE // 2 + radius * math.sin(angle)
            pygame.draw.circle(self.screen, (50, 200, 50, 100), (int(px), int(py)), 3)

        # 兜帽阴影
        pygame.draw.arc(self.screen, (30, 30, 30),
                        (x + TILE_SIZE // 4, y, TILE_SIZE // 2, TILE_SIZE // 2),
                        math.radians(180), math.radians(360), 10)

        # 发光的双眼
        pygame.draw.circle(self.screen, (0, 200, 200),
                           (x + TILE_SIZE // 2 - 8, y + TILE_SIZE // 3), 4)
        pygame.draw.circle(self.screen, (0, 200, 200),
                           (x + TILE_SIZE // 2 + 8, y + TILE_SIZE // 3), 4)

    # -------------------- 魔王绘制 ---------------------
    def draw_monster_knight_boss(self, monster):
        body_color = (30, 30, 30)  # 黑铁色基底
        trim_color = (80, 80, 80)  # 盔甲镶边
        if "圣洁" in monster.name:
            body_color = self.color_reverse(body_color)
            trim_color = self.color_reverse(trim_color)

        # 动画参数
        anim_time = pygame.time.get_ticks()
        hammer_swing = math.sin(anim_time / 300) * 0.5  # 锤子摆动弧度
        shield_glow = abs(math.sin(anim_time / 500))  # 盾牌发光强度
        eye_glow = 100 + int(155 * abs(math.sin(anim_time / 200)))  # 眼部红光波动

        # ---- 基础体型 ----
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE

        # ---- 头部系统 ----
        # 带角巨盔
        helmet_points = [
            (x + 15, y + 8),  # 左耳
            (x + 15, y + 4),  # 左角根
            (x + 8, y - 2),  # 左角尖
            (x + 24, y - 2),  # 右角尖
            (x + 17, y + 4),  # 右角根
            (x + 17, y + 8)  # 右耳
        ]
        pygame.draw.polygon(self.screen, (60, 60, 60), helmet_points)

        # 面甲细节
        pygame.draw.arc(self.screen, (100, 100, 100),
                        (x + 10, y + 5, 12, 15),
                        math.radians(220), math.radians(320), 3)  # 面甲开口
        # 发光红眼
        pygame.draw.circle(self.screen, (eye_glow, 0, 0),
                           (x + 16, y + 12), 3)

        # ---- 肩甲系统 ----
        # 左肩甲（带尖刺）
        left_pauldron = [
            (x + 2, y + 18),
            (x + 8, y + 22),
            (x + 2, y + 26),
            (x - 4, y + 22),
            (x + 2, y + 18)
        ]
        pygame.draw.polygon(self.screen, body_color, left_pauldron)
        pygame.draw.line(self.screen, trim_color,
                         (x + 2, y + 18), (x + 8, y + 22), 2)

        # 右肩甲（带恶魔浮雕）
        pygame.draw.rect(self.screen, body_color,
                         (x + 22, y + 18, 8, 10))
        # 浮雕细节
        pygame.draw.line(self.screen, trim_color,
                         (x + 24, y + 20), (x + 26, y + 24), 2)
        pygame.draw.line(self.screen, trim_color,
                         (x + 26, y + 24), (x + 28, y + 20), 2)

        # ---- 身体主装甲 ----
        # 胸甲主体
        pygame.draw.rect(self.screen, body_color,
                         (x + 10, y + 15, 12, 20))
        # 装甲接缝
        for i in range(3):
            y_pos = y + 17 + i * 6
            pygame.draw.line(self.screen, trim_color,
                             (x + 10, y_pos), (x + 22, y_pos), 1)

        # 中央符文
        rune_points = [
            (x + 16, y + 18), (x + 18, y + 20),
            (x + 16, y + 22), (x + 14, y + 20)
        ]
        pygame.draw.polygon(self.screen, (200, 0, 0), rune_points)

        # ---- 毁灭重锤 ----
        # 锤柄（带动态摆动）
        hammer_length = 25
        hammer_angle = math.radians(30 + hammer_swing * 15)
        hammer_base = (x + 28, y + 28)  # 右手位置
        hammer_head = (
            hammer_base[0] + math.cos(hammer_angle) * hammer_length,
            hammer_base[1] + math.sin(hammer_angle) * hammer_length
        )

        # 锤柄
        pygame.draw.line(self.screen, (50, 50, 50),
                         hammer_base, hammer_head, 5)

        # 锤头（带尖刺）
        pygame.draw.circle(self.screen, (60, 60, 60),
                           hammer_head, 10)
        # 尖刺
        for angle in [0, 90, 180, 270]:
            spike_end = (
                hammer_head[0] + math.cos(math.radians(angle)) * 15,
                hammer_head[1] + math.sin(math.radians(angle)) * 15
            )
            pygame.draw.line(self.screen, (80, 80, 80),
                             hammer_head, spike_end, 3)

        # 锤头裂纹
        pygame.draw.line(self.screen, (30, 30, 30),
                         (hammer_head[0] - 5, hammer_head[1] - 5),
                         (hammer_head[0] + 5, hammer_head[1] + 5), 2)

        # ---- 魔能护盾 ----
        shield_size = 40 * shield_glow
        shield_surface = pygame.Surface((40, 40), pygame.SRCALPHA)
        pygame.draw.ellipse(shield_surface, (100, 0, 0, 100),
                            (20 - shield_size // 2, 20 - shield_size // 2,
                             shield_size, shield_size))
        self.screen.blit(shield_surface, (x - 10, y - 10))

        # ---- 环境互动 ----
        # 地面裂纹
        pygame.draw.arc(self.screen, (60, 60, 60),
                        (x + 5, y + 35, 20, 10),
                        math.radians(180), math.radians(360), 3)
        # 环绕黑雾
        for i in range(3):
            fog_x = x + random.randint(-5, 35)
            fog_y = y + random.randint(-5, 35)
            pygame.draw.circle(self.screen, (30, 30, 30, 80),
                               (fog_x, fog_y), random.randint(3, 6))

    # -------------------- 普通巨龙绘制 ---------------------
    def draw_dragon_boss(self, monster):
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE
        # 动画参数
        anim_time = pygame.time.get_ticks()
        wing_angle = math.sin(anim_time / 200) * 0.3  # 翅膀摆动弧度
        flame_phase = int((anim_time % 300) / 100)  # 三阶段火焰循环
        eye_glow = abs(math.sin(anim_time / 500))  # 眼睛发光强度

        # ---- 基础体型(3x3) ----
        # 身体主骨架
        body_color = (80, 20, 30)  # 暗红色基底
        pygame.draw.ellipse(self.screen, body_color,
                            (x + TILE_SIZE, y + TILE_SIZE, TILE_SIZE, TILE_SIZE))  # 躯干

        # ---- 动态双翼系统 ----
        # 左翼
        left_wing = [
            (x + TILE_SIZE, y + TILE_SIZE),  # 翼根
            (x + int(TILE_SIZE * 0.5), y + int(TILE_SIZE * 0.5) + int(10 * wing_angle)),  # 翼尖
            (x + TILE_SIZE, y + TILE_SIZE * 2)
        ]
        # 右翼
        right_wing = [
            (x + TILE_SIZE * 2, y + TILE_SIZE),
            (x + int(TILE_SIZE * 2.5), y + int(TILE_SIZE * 0.5) + int(10 * wing_angle)),
            (x + TILE_SIZE * 2, y + TILE_SIZE * 2)
        ]

        # 翼膜绘制（带渐变透明）
        for wing in [left_wing, right_wing]:
            pygame.draw.polygon(self.screen, (150, 40, 40), wing)  # 翼膜
            pygame.draw.polygon(self.screen, (100, 20, 20), wing, 2)  # 翼骨

        # ---- 头部细节 ----
        # 龙头
        head_radius = TILE_SIZE // 3
        head_center = (x + TILE_SIZE * 2, y + TILE_SIZE // 2)
        pygame.draw.circle(self.screen, body_color, head_center, head_radius)

        # 龙眼
        eye_radius = head_radius // 3
        eye_center = (head_center[0] - eye_radius, head_center[1] - eye_radius)
        pygame.draw.circle(self.screen, (255, 240, 200), eye_center, eye_radius)  # 眼白
        pygame.draw.circle(self.screen, (200 * eye_glow, 0, 0), eye_center, eye_radius // 2)  # 瞳孔

        # 龙角
        pygame.draw.polygon(self.screen, (100, 80, 60), [
            (head_center[0] - head_radius, head_center[1] - head_radius),
            (head_center[0] - head_radius // 2, head_center[1] - head_radius * 2),
            (head_center[0], head_center[1] - head_radius)
        ])

        # ---- 火焰喷射系统 ----
        if flame_phase > 0:  # 脉冲式火焰
            flame_length = TILE_SIZE // 2 * (1 + 0.5 * flame_phase)
            flame_points = [
                (head_center[0], head_center[1] + head_radius),
                (head_center[0] - flame_length // 2, head_center[1] + head_radius + flame_length),
                (head_center[0] + flame_length // 2, head_center[1] + head_radius + flame_length)
            ]
            pygame.draw.polygon(self.screen, (255, 80 + flame_phase * 50, 0), flame_points)

        # ---- 尾部细节 ----
        tail_points = [
            (x + TILE_SIZE, y + TILE_SIZE * 2),
            (x + TILE_SIZE // 2, y + TILE_SIZE * 3),
            (x + TILE_SIZE * 1.5, y + TILE_SIZE * 3)
        ]
        pygame.draw.polygon(self.screen, body_color, tail_points)

        # ---- 地面阴影 ----
        shadow = pygame.Surface((TILE_SIZE * 3, TILE_SIZE * 3), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 80),
                            (x + TILE_SIZE // 2, y + TILE_SIZE * 2, TILE_SIZE * 2, TILE_SIZE // 2))
        self.screen.blit(shadow, (x, y))

    # -------------------- 冰霜巨龙绘制 ---------------------
    def draw_dragon_ice(self, monster):
        x = monster.x * TILE_SIZE
        y = monster.y * TILE_SIZE
        # 动画参数
        anim_time = pygame.time.get_ticks()
        wing_angle = math.sin(anim_time / 200) * 0.3  # 翅膀摆动弧度
        breath_phase = int((anim_time % 400) / 100)  # 四阶段冰霜呼吸循环
        eye_glow = abs(math.sin(anim_time / 500))  # 眼睛发光强度

        # ---- 基础体型(3x3) ----
        # 身体主骨架
        body_color = (70, 130, 180)  # 钢蓝色基底
        pygame.draw.ellipse(self.screen, body_color,
                            (x + TILE_SIZE, y + TILE_SIZE, TILE_SIZE, TILE_SIZE))  # 躯干

        # ---- 动态双翼系统 ----
        # 左翼（覆盖冰晶）
        left_wing = [
            (x + TILE_SIZE, y + TILE_SIZE),  # 翼根
            (x + int(TILE_SIZE * 0.5), y + int(TILE_SIZE * 0.5) + int(10 * wing_angle)),  # 翼尖
            (x + TILE_SIZE, y + TILE_SIZE * 2)
        ]
        # 右翼
        right_wing = [
            (x + TILE_SIZE * 2, y + TILE_SIZE),
            (x + int(TILE_SIZE * 2.5), y + int(TILE_SIZE * 0.5) + int(10 * wing_angle)),
            (x + TILE_SIZE * 2, y + TILE_SIZE * 2)
        ]

        # 翼膜绘制（带冰晶纹理）
        for wing in [left_wing, right_wing]:
            pygame.draw.polygon(self.screen, (135, 206, 235), wing)  # 淡蓝色翼膜
            pygame.draw.polygon(self.screen, (70, 130, 180), wing, 2)  # 深蓝色翼骨
            # 添加随机冰晶
            for _ in range(6):
                ice_x = random.randint(wing[1][0] - 10, wing[1][0] + 10)
                ice_y = random.randint(wing[1][1] - 10, wing[1][1] + 10)
                pygame.draw.polygon(self.screen, (240, 255, 255), [
                    (ice_x, ice_y),
                    (ice_x + 3, ice_y + 2),
                    (ice_x + 1, ice_y + 5),
                    (ice_x - 2, ice_y + 3)
                ])

        # ---- 头部细节 ----
        # 龙头
        head_radius = TILE_SIZE // 3
        head_center = (x + TILE_SIZE * 2, y + TILE_SIZE // 2)
        pygame.draw.circle(self.screen, body_color, head_center, head_radius)

        # 龙眼（发光蓝眼）
        eye_radius = head_radius // 3
        eye_center = (head_center[0] - eye_radius, head_center[1] - eye_radius)
        pygame.draw.circle(self.screen, (240, 255, 255), eye_center, eye_radius)  # 冰白色眼白
        pygame.draw.circle(self.screen, (0, 191, 255, int(255 * eye_glow)), eye_center,
                           eye_radius // 2)  # 动态发光的瞳孔

        # 冰晶龙角
        pygame.draw.polygon(self.screen, (240, 255, 255), [
            (head_center[0] - head_radius, head_center[1] - head_radius),
            (head_center[0] - head_radius // 2, head_center[1] - head_radius * 2),
            (head_center[0], head_center[1] - head_radius)
        ])

        # ---- 冰霜呼吸特效 ----
        if breath_phase > 0:
            breath_length = TILE_SIZE * (0.5 + 0.3 * breath_phase)
            breath_points = [
                (head_center[0], head_center[1] + head_radius),
                (head_center[0] - breath_length // 2, head_center[1] + head_radius + breath_length),
                (head_center[0] + breath_length // 2, head_center[1] + head_radius + breath_length)
            ]
            # 半透明冰雾效果
            breath_surface = pygame.Surface((TILE_SIZE * 3, TILE_SIZE * 3), pygame.SRCALPHA)
            pygame.draw.polygon(breath_surface, (135, 206, 235, 150), breath_points)
            self.screen.blit(breath_surface, (x, y))

            # 冰锥效果
            for i in range(3):
                icicle_x = head_center[0] - breath_length // 4 + i * breath_length // 2
                icicle_y = head_center[1] + head_radius + breath_length - 10
                pygame.draw.polygon(self.screen, (240, 255, 255), [
                    (icicle_x, icicle_y),
                    (icicle_x + 3, icicle_y + 15),
                    (icicle_x - 3, icicle_y + 15)
                ])

        # ---- 尾部冰晶链 ----
        tail_points = [
            (x + TILE_SIZE, y + TILE_SIZE * 2),
            (x + TILE_SIZE // 2, y + TILE_SIZE * 3),
            (x + TILE_SIZE * 1.5, y + TILE_SIZE * 3)
        ]
        pygame.draw.polygon(self.screen, body_color, tail_points)
        # 尾部冰晶装饰
        for i in range(4):
            ice_x = x + TILE_SIZE + (i * 10)
            ice_y = y + TILE_SIZE * 2 + (i % 2) * 8
            pygame.draw.polygon(self.screen, (240, 255, 255), [
                (ice_x, ice_y), (ice_x + 4, ice_y + 3), (ice_x + 2, ice_y + 6), (ice_x - 2, ice_y + 4)
            ])

        # ---- 环境互动 ----
        # 地面冰霜特效
        frost_radius = TILE_SIZE // 4
        for _ in range(8):
            fx = x + random.randint(TILE_SIZE // 2, TILE_SIZE * 2)
            fy = y + random.randint(TILE_SIZE * 2, TILE_SIZE * 3)
            pygame.draw.circle(self.screen, (175, 238, 238, 80), (fx, fy), frost_radius // 2)
            pygame.draw.circle(self.screen, (240, 255, 255, 120), (fx, fy), frost_radius // 4)

    # ----------------- 神圣骑士绘制 -------------------

    def draw_holy_knight(self, monster):
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
        for i in range(5):
            # 计算基础轨道位置 (轨道半径按比例缩小)
            angle = anim_time / 800 + i * math.pi * 2 / 5
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
        # 动画参数
        anim_time = pygame.time.get_ticks()
        lid_offset = int(2 * math.sin(anim_time / 300))  # 箱盖微微浮动
        gem_glow = abs(math.sin(anim_time / 200)) * 255  # 宝石发光强度

        # ---- 箱体主体 ----
        # 木质箱体
        pygame.draw.rect(self.screen, (101, 67, 33),
                         (x + 4, y + 4 + lid_offset, TILE_SIZE - 8, TILE_SIZE - 8),
                         border_radius=4)
        # 木质纹理
        for i in range(3):
            line_y = y + 8 + i * 8 + lid_offset
            pygame.draw.line(self.screen, (81, 53, 28),
                             (x + 6, line_y), (x + TILE_SIZE - 6, line_y), 2)

        # ---- 金属包角 ----
        metal_color = (198, 155, 93)  # 古铜色
        # 四角装饰
        corners = [
            (x + 2, y + 2), (x + TILE_SIZE - 8, y + 2),
            (x + 2, y + TILE_SIZE - 8), (x + TILE_SIZE - 8, y + TILE_SIZE - 8)
        ]
        for cx, cy in corners:
            # 金属浮雕
            pygame.draw.polygon(self.screen, metal_color, [
                (cx, cy), (cx + 6, cy), (cx + 6, cy + 3), (cx + 3, cy + 6), (cx, cy + 6)
            ])
            # 高光
            pygame.draw.line(self.screen, (230, 200, 150),
                             (cx + 1, cy + 1), (cx + 5, cy + 1), 2)

        # ---- 锁具系统 ----
        lock_x, lock_y = x + TILE_SIZE // 2, y + TILE_SIZE // 2 + lid_offset
        # 锁体
        pygame.draw.rect(self.screen, (60, 60, 60),
                         (lock_x - 6, lock_y - 4, 12, 8), border_radius=2)
        # 锁孔
        pygame.draw.line(self.screen, (120, 120, 120),
                         (lock_x, lock_y - 2), (lock_x, lock_y + 2), 3)
        # 动态锁环
        pygame.draw.circle(self.screen, metal_color,
                           (lock_x, lock_y - 8), 4, width=2)

        # ---- 宝石装饰 ----
        gem_positions = [
            (x + 10, y + 10), (x + TILE_SIZE - 14, y + 10),
            (x + 10, y + TILE_SIZE - 14), (x + TILE_SIZE - 14, y + TILE_SIZE - 14)
        ]
        for gx, gy in gem_positions:
            # 宝石底座
            pygame.draw.circle(self.screen, (50, 50, 50), (gx, gy), 5)
            # 动态发光宝石
            pygame.draw.circle(self.screen,
                               (255, 215, 0, int(gem_glow)),
                               (gx, gy), 3)

        # ---- 环境光效 ----
        # 底部阴影
        shadow = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        pygame.draw.ellipse(shadow, (0, 0, 0, 50),
                            (x, y + TILE_SIZE - 8, TILE_SIZE, 8))
        self.screen.blit(shadow, (x, y))

        # 顶部高光
        highlight_points = [
            (x + 8, y + 4 + lid_offset), (x + TILE_SIZE // 2, y),
            (x + TILE_SIZE - 8, y + 4 + lid_offset)
        ]
        pygame.draw.polygon(self.screen, (255, 255, 255, 80), highlight_points)

    # ------------- 小红药水 ----------------

    def draw_hp(self, item):
        x = item.x * TILE_SIZE
        y = item.y * TILE_SIZE
        # 药水瓶尺寸
        bottle_width = TILE_SIZE - 8
        bottle_height = TILE_SIZE * 0.8
        neck_width = bottle_width * 0.4
        neck_height = TILE_SIZE * 0.15

        # 药水颜色
        if "SMALL" in item.item_type:
            liquid_color = (200, 50, 50)  # 鲜红色
            highlight_color = (255, 100, 100)
        else:
            liquid_color = (150, 0, 0)  # 深红色
            highlight_color = (200, 50, 50)

        # 瓶身
        bottle_rect = (x + (TILE_SIZE - bottle_width) // 2,
                       y + TILE_SIZE - bottle_height,
                       bottle_width, bottle_height)
        pygame.draw.rect(self.screen, (150, 150, 200), bottle_rect, border_radius=8)  # 玻璃瓶

        # 液体
        liquid_level = bottle_height * 0.8 if "SMALL" in item.item_type else bottle_height * 0.9
        liquid_rect = (bottle_rect[0] + 2,
                       bottle_rect[1] + bottle_height - liquid_level,
                       bottle_width - 4, liquid_level - 2)
        pygame.draw.rect(self.screen, liquid_color, liquid_rect, border_radius=6)

        # 液体高光
        pygame.draw.line(self.screen, highlight_color,
                         (liquid_rect[0] + 4, liquid_rect[1] + 4),
                         (liquid_rect[0] + liquid_rect[2] - 8, liquid_rect[1] + 4), 2)

        # 瓶口
        neck_rect = (x + (TILE_SIZE - neck_width) // 2,
                     y + TILE_SIZE - bottle_height - neck_height,
                     neck_width, neck_height)
        pygame.draw.rect(self.screen, (180, 180, 220), neck_rect, border_radius=4)

        # 瓶塞
        cork_rect = (neck_rect[0] + 2, neck_rect[1] - 4,
                     neck_width - 4, 6)
        pygame.draw.rect(self.screen, (150, 100, 50), cork_rect, border_radius=2)

        # 玻璃反光
        pygame.draw.line(self.screen, (200, 200, 255),
                         (bottle_rect[0] + 4, bottle_rect[1] + 4),
                         (bottle_rect[0] + bottle_width // 2, bottle_rect[1] + 8), 2)

    # ------------- 攻击宝石 ----------------

    def draw_gem(self, item):
        x = item.x * TILE_SIZE
        y = item.y * TILE_SIZE
        # 宝石尺寸
        gem_size = TILE_SIZE * 0.8
        gem_center = (x + TILE_SIZE // 2, y + TILE_SIZE // 2)

        # 宝石颜色
        if item.item_type == "ATK_GEM":
            gem_color = (255, 80, 0)  # 橙红色
            highlight_color = (255, 180, 50)
        else:
            gem_color = (0, 100, 200)  # 深蓝色
            highlight_color = (100, 200, 255)

        # 宝石切面
        gem_points = [
            (gem_center[0], gem_center[1] - gem_size // 2),  # 上顶点
            (gem_center[0] + gem_size // 3, gem_center[1] - gem_size // 6),  # 右上
            (gem_center[0] + gem_size // 2, gem_center[1]),  # 右顶点
            (gem_center[0] + gem_size // 3, gem_center[1] + gem_size // 6),  # 右下
            (gem_center[0], gem_center[1] + gem_size // 2),  # 下顶点
            (gem_center[0] - gem_size // 3, gem_center[1] + gem_size // 6),  # 左下
            (gem_center[0] - gem_size // 2, gem_center[1]),  # 左顶点
            (gem_center[0] - gem_size // 3, gem_center[1] - gem_size // 6)  # 左上
        ]
        pygame.draw.polygon(self.screen, gem_color, gem_points)

        # 切面高光
        highlight_points = [
            (gem_center[0], gem_center[1] - gem_size // 3),
            (gem_center[0] + gem_size // 4, gem_center[1] - gem_size // 8),
            (gem_center[0] + gem_size // 3, gem_center[1]),
            (gem_center[0] + gem_size // 4, gem_center[1] + gem_size // 8),
            (gem_center[0], gem_center[1] + gem_size // 3)
        ]
        pygame.draw.polygon(self.screen, highlight_color, highlight_points)

        # 宝石底座
        base_rect = (x + (TILE_SIZE - gem_size) // 2,
                     y + TILE_SIZE - 8,
                     gem_size, 6)
        pygame.draw.rect(self.screen, (100, 100, 100), base_rect, border_radius=2)

        # 宝石闪光
        if random.random() < 0.2:  # 20%概率出现闪光
            flash_points = [
                (gem_center[0] - gem_size // 4, gem_center[1] - gem_size // 4),
                (gem_center[0] + gem_size // 4, gem_center[1] + gem_size // 4)
            ]
            pygame.draw.line(self.screen, (255, 255, 255),
                             flash_points[0], flash_points[1], 2)

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
        for _ in range(random.randint(ITEM_MIN, ITEM_MAX)):
            pos = self.get_random_tile(floor_tiles, occupied)
            if pos:
                item_type = random.choice(ITEM_TYPES)
                self.items.append(Item(pos[0], pos[1], item_type))
                occupied.add(pos)

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
                elif self.maze[y][x] == 5:  # 地狱地板
                    self.draw_hell_floor(x, y)

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
        anim_time = pygame.time.get_ticks()
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        # 岩浆基底颜色动态变化
        lava_color = (
            200 + int(55 * math.sin(anim_time / 300)),
            80 + int(40 * math.cos(anim_time / 400)),
            0,
            200
        )
        pygame.draw.rect(self.screen, lava_color, rect)

        # 岩浆流动纹理
        for i in range(8):
            flow_x = x * TILE_SIZE + random.randint(2, TILE_SIZE - 2)
            flow_y = y * TILE_SIZE + (anim_time // 30 + i * 40) % (TILE_SIZE + 40)
            pygame.draw.line(self.screen, (255, 140, 0),
                             (flow_x, flow_y - 5), (flow_x, flow_y + 5), 3)

        # 随机气泡
        if random.random() < 0.1:
            bubble_x = x * TILE_SIZE + random.randint(5, TILE_SIZE - 5)
            bubble_y = y * TILE_SIZE + random.randint(5, TILE_SIZE - 5)
            pygame.draw.circle(self.screen, (255, 80, 0),
                               (bubble_x, bubble_y), random.randint(2, 4))

    def draw_obsidian_statue(self, x, y):
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        # 雕像主体
        pygame.draw.polygon(self.screen, (20, 20, 20), [
            (rect.centerx, rect.top + 5),
            (rect.left + 8, rect.bottom - 5),
            (rect.right - 8, rect.bottom - 5)
        ])
        # 熔岩纹路
        lava_lines = [
            (rect.centerx - 5, rect.top + 15),
            (rect.centerx + 5, rect.top + 20),
            (rect.centerx, rect.top + 25)
        ]
        pygame.draw.lines(self.screen, (255, 80, 0), False, lava_lines, 3)

        # 恶魔之眼
        pygame.draw.circle(self.screen, (255, 0, 0),
                           (rect.centerx, rect.centery - 5), 6)
        pygame.draw.circle(self.screen, (0, 0, 0),
                           (rect.centerx, rect.centery - 5), 3)

    def draw_hell_floor(self, x, y):
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        # 焦黑基底
        pygame.draw.rect(self.screen, (60, 30, 30), rect)

        # 裂纹
        for _ in range(3):
            start = (rect.left + random.randint(2, TILE_SIZE - 2),
                     rect.top + random.randint(2, TILE_SIZE - 2))
            end = (start[0] + random.randint(-8, 8), start[1] + random.randint(-8, 8))
            pygame.draw.line(self.screen, (80, 40, 40), start, end, 2)

        # 随机火焰
        if random.random() < 0.2:
            flame_h = random.randint(8, 15)
            flame_points = [
                (rect.centerx, rect.bottom - flame_h),
                (rect.centerx - 5, rect.bottom - flame_h // 2),
                (rect.centerx + 5, rect.bottom - flame_h // 2)
            ]
            pygame.draw.polygon(self.screen, (255, 140, 0), flame_points)

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
        """生成地板的固定样式参数"""
        seed = hash((x, y, self.floor))
        random.seed(seed)

        return {
            'crack_h': random.random() < 0.45,  # 30%概率有水平裂缝
            'crack_v': random.random() < 0.45,  # 30%概率有垂直裂缝
            'stain_pos': (
                random.randint(2, TILE_SIZE - 6),
                random.randint(2, TILE_SIZE - 6)
            ) if random.random() < 0.1 else None  # 10%概率有污渍
        }

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

        elif item.item_type == "CHEST":
            coins = math.ceil(
                self.floor * random.randint(5, 50) * random.randint(1, 3) * random.randint(1, 3) / random.randint(1, 3))
            self.player.coins += coins
            self.add_message(f"Chest, gain {coins} coin")
        elif item.item_type == "HP_SMALL":
            self.player.hp = min(self.player.hp + 100 * self.floor, self.player.max_hp)
            self.add_message(f"Small HP portion, HP +{100 * self.floor}")
        elif item.item_type == "HP_LARGE":
            self.player.hp = min(self.player.hp + 500 * self.floor, self.player.max_hp)
            self.add_message(f"Large HP portion, HP +{500 * self.floor}")
        elif item.item_type == "ATK_GEM":
            atk = random.randint(1, 4) * self.floor
            self.player.base_atk += atk
            self.add_message(f"ATK gem, ATK +{atk}")
        elif item.item_type == "DEF_GEM":
            defend = random.randint(1, 4) * self.floor
            self.player.base_defense += defend
            self.add_message(f"DEF gem, DEF +{defend}")

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
                    monster.heal_range = 6
                    monster.heal_amount = 100  # 每次恢复量

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
                        ball_count=5,
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
                        ball_count=6,
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

                    # 检查周围6格内的友军
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
        """
        绘制向上的楼梯
        :param screen: pygame.Surface 对象
        :param x: 楼梯的左上角 x 坐标
        :param y: 楼梯的左上角 y 坐标
        :param tile_size: 每个格子的大小
        """
        # ------ 台阶绘制 ------
        step_height = tile_size // 4  # 每个台阶的高度
        step_width = tile_size  # 每个台阶的宽度
        num_steps = 4  # 台阶数量

        # 台阶颜色（石头质感）
        step_color = (120, 120, 120)  # 灰色
        highlight_color = (150, 150, 150)  # 高光
        shadow_color = (80, 80, 80)  # 阴影

        for i in range(num_steps):
            step_y = y + (num_steps - i - 1) * step_height
            step_x = x + i * (step_width // num_steps)

            # 绘制台阶主体
            pygame.draw.rect(screen, step_color,
                             (step_x, step_y, step_width - i * (step_width // num_steps), step_height))

            # 绘制台阶高光
            pygame.draw.line(screen, highlight_color,
                             (step_x, step_y),
                             (step_x + step_width - i * (step_width // num_steps), step_y), 2)

            # 绘制台阶阴影
            pygame.draw.line(screen, shadow_color,
                             (step_x, step_y + step_height),
                             (step_x + step_width - i * (step_width // num_steps), step_y + step_height), 2)

        # ------ 魔法符文装饰 ------
        # 符文颜色
        rune_color = (0, 255, 255)  # 青色
        # 符文位置（在台阶侧面）
        for i in range(num_steps):
            rune_x = x + i * (step_width // num_steps) + 5
            rune_y = y + (num_steps - i) * step_height - 5
            # 绘制符文（简单的几何图案）
            pygame.draw.circle(screen, rune_color, (rune_x, rune_y), 3)
            pygame.draw.line(screen, rune_color, (rune_x - 5, rune_y), (rune_x + 5, rune_y), 2)

        # ------ 顶部传送门 ------
        portal_radius = tile_size // 3
        portal_center_x = x + tile_size // 2
        portal_center_y = y - portal_radius

        # 传送门外圈
        pygame.draw.circle(screen, (255, 215, 0),  # 金色
                           (portal_center_x, portal_center_y), portal_radius, 2)

        # 传送门内圈（发光效果）
        for i in range(3):
            glow_radius = portal_radius - i * 2
            alpha = 100 - i * 30  # 透明度递减
            glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (255, 215, 0, alpha),
                               (glow_radius, glow_radius), glow_radius)
            screen.blit(glow_surface, (portal_center_x - glow_radius, portal_center_y - glow_radius))

        # 传送门中心（魔法漩涡）
        for i in range(4):
            angle = pygame.time.get_ticks() / 200 + i * 90  # 动态旋转效果
            start_pos = (
                portal_center_x + math.cos(math.radians(angle)) * portal_radius * 0.5,
                portal_center_y + math.sin(math.radians(angle)) * portal_radius * 0.5
            )
            end_pos = (
                portal_center_x + math.cos(math.radians(angle + 180)) * portal_radius * 0.5,
                portal_center_y + math.sin(math.radians(angle + 180)) * portal_radius * 0.5
            )
            pygame.draw.line(screen, (255, 255, 255), start_pos, end_pos, 2)

        # ------ 藤蔓装饰 ------
        vine_color = (34, 139, 34)  # 绿色
        # 左侧藤蔓
        pygame.draw.arc(screen, vine_color,
                        (x - tile_size // 2, y - tile_size // 2, tile_size, tile_size),
                        math.radians(180), math.radians(270), 2)
        # 右侧藤蔓
        pygame.draw.arc(screen, vine_color,
                        (x + tile_size // 2, y - tile_size // 2, tile_size, tile_size),
                        math.radians(270), math.radians(360), 2)

    # 墙壁绘制方法：
    def draw_wall(self, x, y, surface=None):
        surface = surface or self.screen
        """使用预先生成的样式绘制墙壁"""
        style = self.tile_styles[y][x]
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        # 绘制基础颜色
        pygame.draw.rect(surface, COLOR_STONE, rect)

        if style['type'] == 'moss':
            self.draw_moss_stone(x, y, style, surface)
        elif style['type'] == 'cracked':
            self.draw_cracked_stone(x, y, style, surface)
        else:
            self.draw_basic_stone(x, y, style, surface)

        self.draw_stone_shading(x, y, surface)

    def draw_basic_stone(self, x, y, style, surface=None):
        surface = surface or self.screen
        """绘制基础石墙（使用预生成高光点）"""
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        # 砖缝（保持不变）
        for i in range(0, TILE_SIZE, 6):
            pygame.draw.line(surface, COLOR_SHADOW,
                             (rect.left + i, rect.top),
                             (rect.left + i, rect.bottom), 1)
        # 使用预生成的高光点
        for px, py in style['highlights']:
            pygame.draw.circle(surface, COLOR_HIGHLIGHT,
                               (rect.left + px, rect.top + py), 1)

    def draw_moss_stone(self, x, y, style, surface=None):
        surface = surface or self.screen
        """绘制青苔石墙（使用预生成参数）"""
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        # 绘制预先生成的青苔点
        for px, py in style['moss_pos']:
            pygame.draw.circle(surface, COLOR_MOSS,
                               (rect.left + px, rect.top + py), 1)

        # 其他固定绘制（如底部青苔带）
        pygame.draw.rect(surface, COLOR_MOSS,
                         (rect.left + 2, rect.bottom - 4, TILE_SIZE - 4, 3))

    def draw_cracked_stone(self, x, y, style, surface=None):
        surface = surface or self.screen
        """绘制裂缝石墙（使用预生成参数）"""
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        # 主裂缝
        pygame.draw.line(surface, COLOR_CRACK,
                         (rect.left + style['crack_start'][0], rect.top + style['crack_start'][1]),
                         (rect.left + style['crack_end'][0], rect.top + style['crack_end'][1]), 2)

        # 细小裂痕
        for sx, sy in style['small_cracks']:
            ex = sx + random.randint(-4, 4)
            ey = sy + random.randint(-4, 4)
            pygame.draw.line(surface, COLOR_CRACK,
                             (rect.left + sx, rect.top + sy),
                             (rect.left + ex, rect.top + ey), 1)

    def draw_stone_shading(self, x, y, surface=None):
        surface = surface or self.screen
        """绘制石墙立体阴影效果"""
        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)

        # 左侧阴影
        shade = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        shade.fill((0, 0, 0, 40))
        self.screen.blit(shade, rect.topleft)

        # 砖块凸起效果
        for i in range(0, TILE_SIZE, 6):
            for j in range(0, TILE_SIZE, 6):
                if (i + j) % 12 == 0:
                    pygame.draw.line(surface, COLOR_HIGHLIGHT,
                                     (rect.left + i, rect.top + j),
                                     (rect.left + i + 4, rect.top + j), 1)
                    pygame.draw.line(surface, COLOR_HIGHLIGHT,
                                     (rect.left + i, rect.top + j),
                                     (rect.left + i, rect.top + j + 4), 1)

        # 顶部高光
        pygame.draw.line(surface, COLOR_HIGHLIGHT,
                         (rect.left, rect.top), (rect.right, rect.top), 2)
        # 左侧高光
        pygame.draw.line(surface, COLOR_HIGHLIGHT,
                         (rect.left, rect.top), (rect.left, rect.bottom), 2)

    # 地面绘画方法
    def draw_floor(self, x, y, surface=None):
        surface = surface or self.screen
        is_fountain_room = False
        if self.fountain_room:
            if (self.fountain_room['x1'] <= x < self.fountain_room['x2'] and
                    self.fountain_room['y1'] <= y < self.fountain_room['y2']):
                is_fountain_room = True

        rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        # 调整喷泉房间地板颜色和样式
        if is_fountain_room:
            base_color = tuple(c - 20 for c in COLOR_FLOOR)  # 更深的底色
            pygame.draw.rect(surface, base_color, rect)
            # 双倍裂缝密度
            pygame.draw.line(surface, COLOR_FLOOR_CRACK,
                             (rect.left + 2, rect.centery),
                             (rect.right - 2, rect.centery), 2)
            pygame.draw.line(surface, COLOR_FLOOR_CRACK,
                             (rect.centerx, rect.top + 2),
                             (rect.centerx, rect.bottom - 2), 2)
            # 添加额外对角线裂缝
            if random.random() < 0.4:
                start_x = rect.left + random.randint(2, TILE_SIZE - 2)
                start_y = rect.top + random.randint(2, TILE_SIZE - 2)
                end_x = start_x + random.randint(-8, 8)
                end_y = start_y + random.randint(-8, 8)
                pygame.draw.line(surface, COLOR_FLOOR_CRACK,
                                 (start_x, start_y), (end_x, end_y), 1)
        else:
            style = self.tile_styles[y][x]
            pygame.draw.rect(surface, COLOR_FLOOR, rect)

            # 水平裂缝
            if style['crack_h']:
                pygame.draw.line(surface, COLOR_FLOOR_CRACK,
                                 (rect.left + 2, rect.centery),
                                 (rect.right - 2, rect.centery), 1)

            # 垂直裂缝
            if style['crack_v']:
                pygame.draw.line(surface, COLOR_FLOOR_CRACK,
                                 (rect.centerx, rect.top + 2),
                                 (rect.centerx, rect.bottom - 2), 1)

            # 污渍
            if style['stain_pos']:
                sx, sy = style['stain_pos']
                pygame.draw.ellipse(surface, (175, 175, 175, 30),
                                    (rect.left + sx, rect.top + sy, 6, 6))

    # 右侧绘画怪物动态属性面板
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
    # 重新设计技能显示部分：每行两个技能，共三行
    def draw_left_panel(self):
        panel_width = SIDEBAR_WIDTH
        panel = pygame.Surface((panel_width, SCREEN_HEIGHT), pygame.SRCALPHA)
        panel.fill((30, 30, 40, 200))  # 半透明深蓝灰底色

        # 动态布局参数
        current_y = 15  # 当前绘制Y坐标
        section_gap = 20  # 模块间距
        module_padding = 10  # 模块内边距

        # ------ 状态栏标题 ------
        title_font = pygame.font.SysFont("SimHei", 24, bold=True)
        title = title_font.render("勇者状态", True, (255, 215, 0))
        panel.blit(title, (20, current_y))
        current_y += 40  # 标题高度+间距

        # ------ 核心属性区域 ------
        attr_height = 100
        attr_bg = pygame.Surface((260, attr_height), pygame.SRCALPHA)
        attr_bg.fill((40, 40, 60, 150))
        pygame.draw.rect(attr_bg, (80, 80, 100), (0, 0, 260, attr_height), 2)

        # 数值显示
        info_font = pygame.font.SysFont("SimSun", 20, bold=True)
        attr_bg.blit(info_font.render(f"ATK: {self.player.atk}", True, (255, 180, 180)), (40, 20))
        attr_bg.blit(info_font.render(f"DEF: {self.player.defense}", True, (180, 200, 255)), (40, 45))
        hp_color = (50, 200, 50) if self.player.hp / self.player.max_hp > 0.3 else (200, 50, 50)
        attr_bg.blit(info_font.render(f"HP: {self.player.hp}/{self.player.max_hp}", True, hp_color), (40, 70))

        panel.blit(attr_bg, (20, current_y))
        current_y += attr_height + section_gap

        # ------ 金币和楼层信息 ------
        meta_height = 50
        meta_bg = pygame.Surface((260, meta_height), pygame.SRCALPHA)
        meta_bg.fill((60, 60, 80, 150))
        pygame.draw.rect(meta_bg, (80, 80, 100), (0, 0, 260, meta_height), 2)

        # 金币图标
        pygame.draw.circle(meta_bg, (255, 215, 0), (30, 25), 12)
        pygame.draw.line(meta_bg, (200, 160, 0), (25, 25), (35, 25), 3)
        meta_bg.blit(info_font.render(f"{self.player.coins}", True, (255, 215, 0)), (50, 15))

        # 楼层图标
        pygame.draw.rect(meta_bg, (147, 112, 219), (160, 10, 30, 30), border_radius=5)
        meta_bg.blit(info_font.render(f"{self.floor}F", True, (200, 180, 255)), (200, 15))

        panel.blit(meta_bg, (20, current_y))
        current_y += meta_height + section_gap

        # ------ 装备信息区域 ------
        equip_height = 80
        equip_bg = pygame.Surface((260, equip_height), pygame.SRCALPHA)
        equip_bg.fill((40, 40, 60, 150))
        pygame.draw.rect(equip_bg, (80, 80, 100), (0, 0, 260, equip_height), 2)

        # 武器信息
        eq_font = pygame.font.SysFont("SimSun", 16)
        weapon = self.player.equipped_weapon
        weapon_text = f"武: {weapon['name']}" if weapon else "武: 无"
        equip_bg.blit(eq_font.render(weapon_text, True, (200, 200, 200) if weapon else (150, 150, 150)), (50, 10))

        # 护甲信息
        armor = self.player.equipped_armor
        armor_text = f"甲: {armor['name']}" if armor else "甲: 无"
        equip_bg.blit(eq_font.render(armor_text, True, (200, 200, 200) if armor else (150, 150, 150)), (160, 10))

        panel.blit(equip_bg, (20, current_y))
        current_y += equip_height + section_gap

        # ------ 技能面板（重新设计）------
        skill_height = 200  # 增加高度以容纳3行技能
        skill_bg = pygame.Surface((260, skill_height), pygame.SRCALPHA)
        skill_bg.fill((40, 40, 60, 200))
        pygame.draw.rect(skill_bg, (80, 80, 100), (0, 0, 260, skill_height), 2)

        skill_font = pygame.font.SysFont("SimSun", 16)  # 减小字体
        skill_keys = list(self.player.skills.keys())

        # 技能布局参数
        skill_width = 120  # 每个技能区域宽度
        skill_height_item = 60  # 每个技能区域高度
        horizontal_gap = 10  # 水平间距
        vertical_gap = 5  # 垂直间距

        # 绘制技能网格
        for i, key in enumerate(skill_keys):
            if i >= 6:  # 最多显示6个技能
                break

            skill = self.player.skills[key]

            # 计算技能在网格中的位置
            row = i // 2  # 每行2个技能
            col = i % 2  # 0或1列

            # 计算技能绘制的起始位置
            skill_x = 10 + col * (skill_width + horizontal_gap)
            skill_y = 10 + row * (skill_height_item + vertical_gap)

            # 计算冷却状态
            cd_ratio = skill['current_cd'] / skill['cooldown'] if skill['current_cd'] > 0 else 0
            name_color = (255, 255, 0) if cd_ratio == 0 else (100, 100, 100)

            # 绘制技能名称和按键
            skill_bg.blit(skill_font.render(f"{pygame.key.name(skill['key']).upper()}: {skill['name']}", True, name_color),
                          (skill_x, skill_y))

            # 绘制冷却条
            pygame.draw.rect(skill_bg, (80, 80, 80),
                             (skill_x, skill_y + 20, skill_width - 20, 10))
            pygame.draw.rect(skill_bg, (0, 200, 0),
                             (skill_x, skill_y + 20, (skill_width - 20) * (1 - cd_ratio), 10))

            # 如果技能有特殊参数，显示简短信息
            if 'damage_multiple' in skill:
                skill_bg.blit(skill_font.render(f"伤害: {skill['damage_multiple']}x", True, (200, 200, 200)),
                              (skill_x, skill_y + 35))
            elif 'heal_percent' in skill:
                skill_bg.blit(skill_font.render(f"治疗: {int(skill['heal_percent'] * 100)}%/秒", True, (100, 255, 100)),
                              (skill_x, skill_y + 35))

        panel.blit(skill_bg, (20, current_y))
        current_y += skill_height + section_gap

        # ------ 消息日志区域 ------
        log_height = SCREEN_HEIGHT - current_y - 20  # 动态计算剩余高度
        log_bg = pygame.Surface((260, log_height), pygame.SRCALPHA)
        log_bg.fill((40, 40, 60, 200))
        pygame.draw.rect(log_bg, (80, 80, 100), (0, 0, 260, log_height), 2)

        log_font = pygame.font.SysFont("SimSun", 16)
        visible_messages = self.message_log[-self.max_log_lines:]
        for i, msg in enumerate(visible_messages):
            # 颜色逻辑保持不变
            text_surface = log_font.render(msg, True, self._get_message_color(msg))
            log_bg.blit(text_surface, (10, 10 + i * 18))

        panel.blit(log_bg, (20, current_y))

        # 绘制到主屏幕左侧
        self.screen.blit(panel, (MAP_WIDTH * TILE_SIZE, 0))


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
        x = item.x * TILE_SIZE
        y = item.y * TILE_SIZE
        anim_time = pygame.time.get_ticks()  # 用于动画效果

        # 木剑
        if item.item_type == "WOOD_SWORD":
            # 剑柄 (深棕色)
            pygame.draw.rect(self.screen, (101, 67, 33),
                             (x + 12, y + 10, 6, 16))  # 垂直剑柄
            # 护手 (铜色)
            pygame.draw.rect(self.screen, (184, 115, 51),
                             (x + 8, y + 20, 14, 4))
            # 剑身 (木质纹理)
            for i in range(3):
                pygame.draw.line(self.screen, (139, 69, 19),
                                 (x + 15, y + 5 - i), (x + 15, y + 25 + i), 3)
            # 装饰绳结
            pygame.draw.circle(self.screen, (139, 0, 0),
                               (x + 15, y + 22), 3)
            # 剑身反光
            if anim_time % 1000 < 500:
                pygame.draw.line(self.screen, (200, 200, 200, 100),
                                 (x + 15, y + 5), (x + 15, y + 25), 1)

        # 青铜匕首
        elif item.item_type == "BRONZE_DAGGER":
            # 刀刃 (青铜色)
            blade_color = (97, 153, 59)
            blade_points = [
                (x + 15, y + 5), (x + 20, y + 15), (x + 15, y + 25), (x + 10, y + 15)
            ]
            pygame.draw.polygon(self.screen, blade_color, blade_points)
            # 刀柄 (木质)
            pygame.draw.rect(self.screen, (139, 69, 19), (x + 13, y + 12, 5, 6))
            # 刀柄装饰
            pygame.draw.line(self.screen, (184, 115, 51),
                             (x + 14, y + 13), (x + 17, y + 18), 2)
            # 刀刃反光
            if anim_time % 800 < 400:
                pygame.draw.line(self.screen, (200, 200, 200, 100),
                                 (x + 13, y + 10), (x + 17, y + 20), 1)

        # 钢匕首
        elif item.item_type == "STEEL_DAGGER":
            # 刀刃 (钢色)
            blade_color = (192, 192, 192)
            blade_points = [
                (x + 12, y + 5), (x + 18, y + 15), (x + 12, y + 25)
            ]
            pygame.draw.polygon(self.screen, blade_color, blade_points)
            # 刀柄 (皮革包裹)
            pygame.draw.rect(self.screen, (139, 69, 19), (x + 10, y + 12, 8, 8))
            # 刀柄装饰
            for i in range(3):
                pygame.draw.line(self.screen, (105, 105, 105),
                                 (x + 11 + i * 2, y + 13), (x + 11 + i * 2, y + 19), 2)
            # 动态反光
            if anim_time % 600 < 300:
                pygame.draw.line(self.screen, (255, 255, 255, 150),
                                 (x + 13, y + 7), (x + 15, y + 23), 2)

        # 铜剑
        elif item.item_type == "COPPER_SWORD":
            # 剑身 (铜色渐变)
            for i in range(15):
                color = (184, 115, 51, 255 - i * 10)
                pygame.draw.line(self.screen, color,
                                 (x + 12, y + 5 + i), (x + 18, y + 5 + i), 3)
            # 剑柄 (缠绕皮革)
            pygame.draw.rect(self.screen, (139, 69, 19), (x + 13, y + 20, 4, 8))
            # 剑柄装饰
            pygame.draw.line(self.screen, (105, 105, 105),
                             (x + 13, y + 22), (x + 16, y + 25), 2)
            # 动态铜锈效果
            if anim_time % 1000 < 500:
                for i in range(3):
                    spot_x = x + 12 + random.randint(0, 6)
                    spot_y = y + 10 + random.randint(0, 15)
                    pygame.draw.circle(self.screen, (50, 205, 50, 100),
                                       (spot_x, spot_y), 1)

        # 铁剑
        elif item.item_type == "IRON_SWORD":
            # 剑身 (铁灰色)
            pygame.draw.rect(self.screen, (105, 105, 105), (x + 12, y + 5, 6, 20))
            # 剑刃 (高光)
            pygame.draw.line(self.screen, (192, 192, 192),
                             (x + 12, y + 5), (x + 12, y + 25), 2)
            pygame.draw.line(self.screen, (192, 192, 192),
                             (x + 18, y + 5), (x + 18, y + 25), 2)
            # 剑柄 (皮革缠绕)
            pygame.draw.rect(self.screen, (139, 69, 19), (x + 13, y + 20, 4, 8))
            # 动态反光
            if anim_time % 800 < 400:
                pygame.draw.line(self.screen, (255, 255, 255, 150),
                                 (x + 13, y + 7), (x + 15, y + 23), 2)

        # 精钢匕首
        elif item.item_type == "FINE_STEEL_DAGGER":
            # 刀刃 (精钢)
            blade_color = (220, 220, 220)
            blade_points = [
                (x + 12, y + 5), (x + 18, y + 15), (x + 12, y + 25)
            ]
            pygame.draw.polygon(self.screen, blade_color, blade_points)
            # 刀柄 (镶嵌宝石)
            pygame.draw.rect(self.screen, (105, 105, 105), (x + 10, y + 12, 8, 8))
            # 宝石装饰
            pygame.draw.circle(self.screen, (255, 0, 0), (x + 14, y + 16), 2)
            # 动态反光
            if anim_time % 500 < 250:
                pygame.draw.line(self.screen, (255, 255, 255, 200),
                                 (x + 13, y + 7), (x + 15, y + 23), 3)

        # 精铁长剑
        elif item.item_type == "FINE_IRON_SWORD":
            # 剑身 (精铁)
            pygame.draw.rect(self.screen, (75, 75, 75), (x + 12, y + 5, 6, 20))
            # 剑刃 (高光)
            for i in range(3):
                pygame.draw.line(self.screen, (192, 192, 192),
                                 (x + 12 + i, y + 5 + i), (x + 12 + i, y + 25 - i), 1)
            # 剑柄 (镶嵌宝石)
            pygame.draw.rect(self.screen, (50, 50, 50), (x + 13, y + 20, 4, 8))
            pygame.draw.circle(self.screen, (0, 0, 255), (x + 15, y + 24), 2)
            # 动态反光
            if anim_time % 600 < 300:
                pygame.draw.line(self.screen, (255, 255, 255, 200),
                                 (x + 13, y + 7), (x + 15, y + 23), 3)

        # 格斯大剑
        elif item.item_type == "GUTS_GREATSWORD":
            # 剑身 (暗色)
            pygame.draw.rect(self.screen, (50, 50, 50), (x + 8, y + 5, 14, 25))
            # 剑刃 (锯齿状)
            for i in range(5):
                pygame.draw.line(self.screen, (105, 105, 105),
                                 (x + 8 + i * 3, y + 5), (x + 8 + i * 3, y + 30), 2)
            # 剑柄 (皮革缠绕)
            pygame.draw.rect(self.screen, (139, 69, 19), (x + 13, y + 25, 4, 10))
            # 动态血迹效果
            if anim_time % 1000 < 500:
                for i in range(3):
                    spot_x = x + 8 + random.randint(0, 14)
                    spot_y = y + 10 + random.randint(0, 20)
                    pygame.draw.circle(self.screen, (139, 0, 0, 150),
                                       (spot_x, spot_y), 2)

        # 木板甲
        elif item.item_type == "WOOD_ARMOR":
            # 主体 (木质)
            pygame.draw.rect(self.screen, (101, 67, 33), (x + 8, y + 8, 15, 20))
            # 木板纹理
            for i in range(3):
                pygame.draw.line(self.screen, (139, 69, 19),
                                 (x + 8, y + 10 + i * 6), (x + 23, y + 10 + i * 6), 3)
            # 铆钉装饰
            for i in range(2):
                for j in range(3):
                    pygame.draw.circle(self.screen, (184, 115, 51),
                                       (x + 10 + i * 10, y + 12 + j * 6), 2)

        # 铜板甲
        elif item.item_type == "COPPER_ARMOR":
            # 主体 (铜色)
            pygame.draw.rect(self.screen, (184, 115, 51), (x + 8, y + 8, 15, 20))
            # 装饰条纹
            for i in range(3):
                pygame.draw.line(self.screen, (139, 69, 19),
                                 (x + 8, y + 10 + i * 6), (x + 23, y + 10 + i * 6), 2)
            # 动态铜锈
            if anim_time % 1200 < 600:
                for i in range(3):
                    spot_x = x + 8 + random.randint(0, 15)
                    spot_y = y + 8 + random.randint(0, 20)
                    pygame.draw.circle(self.screen, (50, 205, 50, 100),
                                       (spot_x, spot_y), 2)

        # 铁板甲
        elif item.item_type == "IRON_ARMOR":
            # 主体 (铁灰色)
            pygame.draw.rect(self.screen, (105, 105, 105), (x + 8, y + 8, 15, 20))
            # 铆钉装饰
            for i in range(2):
                for j in range(3):
                    pygame.draw.circle(self.screen, (192, 192, 192),
                                       (x + 10 + i * 10, y + 12 + j * 6), 2)
            # 动态反光
            if anim_time % 800 < 400:
                pygame.draw.line(self.screen, (255, 255, 255, 100),
                                 (x + 8, y + 10), (x + 23, y + 25), 2)

        # 钢板甲
        elif item.item_type == "STEEL_ARMOR":
            # 主体 (钢色)
            pygame.draw.rect(self.screen, (192, 192, 192), (x + 8, y + 8, 15, 20))
            # 装饰条纹
            for i in range(3):
                pygame.draw.line(self.screen, (105, 105, 105),
                                 (x + 8, y + 10 + i * 6), (x + 23, y + 10 + i * 6), 2)
            # 动态反光
            if anim_time % 600 < 300:
                pygame.draw.line(self.screen, (255, 255, 255, 150),
                                 (x + 8, y + 10), (x + 23, y + 25), 3)

        # 红色闪电甲
        elif item.item_type == "LIGHTNING_ARMOR_RED":
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
            # 宝箱
            if item.item_type == "CHEST":
                self.draw_chest(item)
                continue

            # 药水
            elif "HP_" in item.item_type:
                self.draw_hp(item)
                continue

            # 宝石类
            elif "GEM" in item.item_type:
                self.draw_gem(item)

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
                self.draw_holy_knight(monster)
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
