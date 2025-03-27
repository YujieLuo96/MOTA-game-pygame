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

# 怪物追踪距离
MONSTER_DISTANCE = 6

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

N = 3
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
MONSTER_WEIGHT = [10, 10, 5, 5, 5, 12, 16, 12, 8, 6, 5, 5, 8, 2, 1, 1, 1, 1, 1, 1, 1]  # [0,0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1]

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
     "attack_range": 3, "attack_speed": 0.7, "coin": 1900, "speed": 50, "level": 8}
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
        self.font = pygame.font.Font(None, 36)
        self.back_button = pygame.Rect(50, 400, 200, 50)
        self.apply_button = pygame.Rect(300, 400, 200, 50)
        self.sliders = [
            {"label": "Map Width", "value": CONFIG["MAP_WIDTH"], "min": 21, "max": 51,
             "rect": pygame.Rect(100, 100, 400, 20)},
            {"label": "Map Height", "value": CONFIG["MAP_HEIGHT"], "min": 21, "max": 51,
             "rect": pygame.Rect(100, 150, 400, 20)},
            {"label": "Tile Size", "value": CONFIG["TILE_SIZE"], "min": 20, "max": 80,
             "rect": pygame.Rect(100, 200, 400, 20)}
        ]
        self.dragging = None

    def draw_slider(self, slider, y):
        pygame.draw.rect(self.screen, (200, 200, 200), slider["rect"])
        ratio = (slider["value"] - slider["min"]) / (slider["max"] - slider["min"])
        handle_x = slider["rect"].x + ratio * (slider["rect"].width - 20)
        pygame.draw.rect(self.screen, (0, 128, 255), (handle_x, slider["rect"].y - 10, 20, 40))

        label = self.font.render(f"{slider['label']}: {slider['value']}", True, (255, 255, 255))
        self.screen.blit(label, (slider["rect"].x, slider["rect"].y - 40))

    def draw(self):
        self.screen.fill((30, 30, 50))
        for slider in self.sliders:
            self.draw_slider(slider, slider["rect"].y)

        # 绘制按钮
        pygame.draw.rect(self.screen, (70, 70, 70), self.back_button)
        back_text = self.font.render("Back", True, (255, 255, 255))
        self.screen.blit(back_text, (self.back_button.x + 70, self.back_button.y + 15))

        pygame.draw.rect(self.screen, (70, 70, 70), self.apply_button)
        apply_text = self.font.render("Apply", True, (255, 255, 255))
        self.screen.blit(apply_text, (self.apply_button.x + 70, self.apply_button.y + 15))

        pygame.display.flip()

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, slider in enumerate(self.sliders):
                if slider["rect"].collidepoint(event.pos):
                    self.dragging = i
            if self.back_button.collidepoint(event.pos):
                return "menu"
            elif self.apply_button.collidepoint(event.pos):
                CONFIG["SCREEN_WIDTH"] = self.sliders[0]["value"] * self.sliders[2]["value"] + 600
                CONFIG["SCREEN_HEIGHT"] = self.sliders[1]["value"] * self.sliders[2]["value"]
                CONFIG["TILE_SIZE"] = self.sliders[2]["value"]
                CONFIG["MAP_WIDTH"] = self.sliders[0]["value"]
                CONFIG["MAP_HEIGHT"] = self.sliders[1]["value"]
                return "apply"

        elif event.type == pygame.MOUSEBUTTONUP:
            self.dragging = None

        elif event.type == pygame.MOUSEMOTION and self.dragging is not None:
            slider = self.sliders[self.dragging]
            x = min(max(event.pos[0], slider["rect"].x), slider["rect"].x + slider["rect"].width)
            ratio = (x - slider["rect"].x) / slider["rect"].width
            slider["value"] = int(slider["min"] + ratio * (slider["max"] - slider["min"]))

        return "settings"


class DungeonButton:
    def __init__(self, rect, text, font_size=32):
        self.rect = rect
        self.text = text
        self.font = pygame.font.Font(None, font_size)
        self.hover = False
        self.flame_offset = 0  # 火焰动画偏移量

    def draw(self, surface):
        # 动态更新火焰偏移
        self.flame_offset = (self.flame_offset + 2) % 20

        # 基础石板
        self._draw_stone_base(surface)

        # 金属镶边
        self._draw_metal_trim(surface)

        # 动态火焰效果（仅悬停时）
        if self.hover:
            self._draw_flame_effect(surface)

        # 按钮文字
        self._draw_text(surface)

    def _draw_stone_base(self, surface):
        # 石板基底
        base_color = (60, 60, 60) if not self.hover else (80, 80, 80)
        pygame.draw.rect(surface, base_color, self.rect, border_radius=8)

        # 石头纹理
        for _ in range(40):  # 随机石纹斑点
            x = self.rect.x + random.randint(2, self.rect.w - 4)
            y = self.rect.y + random.randint(2, self.rect.h - 4)
            size = random.choice([1, 1, 1, 2])
            color = random.choice([(70, 70, 70), (50, 50, 50), (90, 90, 90)])
            pygame.draw.circle(surface, color, (x, y), size)

        # 立体凹痕
        pygame.draw.line(surface, (40, 40, 40),
                         (self.rect.left + 5, self.rect.centery),
                         (self.rect.right - 5, self.rect.centery), 3)
        pygame.draw.line(surface, (40, 40, 40),
                         (self.rect.centerx, self.rect.top + 5),
                         (self.rect.centerx, self.rect.bottom - 5), 3)

    def _draw_metal_trim(self, surface):
        # 青铜镶边
        trim_color1 = (198, 155, 93)  # 青铜色
        trim_color2 = (150, 120, 70)  # 暗部
        border_rect = self.rect.inflate(-4, -4)

        # 渐变金属效果
        for i in range(4):
            color = (
                trim_color1[0] + (trim_color2[0] - trim_color1[0]) * i / 4,
                trim_color1[1] + (trim_color2[1] - trim_color1[1]) * i / 4,
                trim_color1[2] + (trim_color2[2] - trim_color1[2]) * i / 4
            )
            pygame.draw.rect(surface, color, border_rect.inflate(-i * 2, -i * 2),
                             border_radius=8 - i, width=2)

        # 铆钉装饰
        for x in [border_rect.left + 8, border_rect.right - 8]:
            for y in [border_rect.top + 8, border_rect.bottom - 8]:
                pygame.draw.circle(surface, (250, 250, 200), (x, y), 3)
                pygame.draw.circle(surface, (150, 150, 100), (x, y), 3, 1)

    def _draw_flame_effect(self, surface):
        # 火焰粒子效果
        for i in range(3):
            offset = self.flame_offset + i * 7
            if offset > 20: continue

            # 火焰主体
            flame_rect = pygame.Rect(
                self.rect.centerx - 15 + offset,
                self.rect.top - 15,
                30, 30
            )

            # 火焰颜色渐变
            for j, color in enumerate([(255, 100, 0, 150), (255, 200, 0, 80), (255, 255, 200, 40)]):
                temp_surf = pygame.Surface((30, 30), pygame.SRCALPHA)
                pygame.draw.ellipse(temp_surf, color, (0, j * 5, 30, 30 - j * 10))
                surface.blit(temp_surf, flame_rect)

            # 火星粒子
            for _ in range(5):
                x = flame_rect.centerx + random.randint(-8, 8)
                y = flame_rect.centery + random.randint(-5, 5)
                pygame.draw.circle(surface, (255, 255, 200, 150), (x, y), 1)

    def _draw_text(self, surface):
        # 文字阴影效果
        text_surf = self.font.render(self.text, True, (30, 30, 30))
        shadow_rect = text_surf.get_rect(center=(self.rect.centerx + 2, self.rect.centery + 2))
        surface.blit(text_surf, shadow_rect)

        # 主文字
        text_color = (200, 160, 60) if not self.hover else (255, 200, 100)
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)


class MainMenu:
    def __init__(self, screen):
        self.screen = screen
        self.font_title = pygame.font.Font(None, 72)  # 使用默认字体
        self.background = self.create_stone_texture()
        self.torch_frames = self.create_torch_frames()  # 动态生成火炬动画帧
        self.torch_index = 0
        self.torch_timer = 0

        # 使用 DungeonButton 创建按钮
        self.start_button = DungeonButton(
            pygame.Rect(0, 0, 300, 80), "Enter the Dungeon", 36
        )
        self.start_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 2 // 3)

        self.settings_button = DungeonButton(
            pygame.Rect(0, 0, 280, 70), "Settings", 32
        )
        self.settings_button.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT * 3 // 4)

    # --------绘制火炬 -------
    def create_torch_frames(self):
        torch_width = 4 * TILE_SIZE  # 3格宽
        torch_height = 8 * TILE_SIZE  # 6格高
        frames = []

        for i in range(8):  # 8帧动画
            frame = pygame.Surface((torch_width, torch_height), pygame.SRCALPHA)

            # ------ 火焰核心 -------
            # 动态火焰形状参数
            flame_radius = 30 + i * 5  # 火焰半径动态变化
            flame_points = []
            for angle in range(0, 360, 10):
                # 动态扭曲效果
                distortion = math.sin(math.radians(angle * 2 + i * 45)) * 10
                x = torch_width // 2 + math.cos(math.radians(angle)) * (flame_radius + distortion)
                y = torch_height - 50 - angle / 3  # 火焰向上延伸
                flame_points.append((x, y))

            # 多层火焰（从内到外）
            flame_layers = [
                {'color': (255, 200, 50, 200), 'offset': 0},  # 核心亮黄色
                {'color': (255, 100, 0, 150), 'offset': 5},  # 中层橙色
                {'color': (200, 50, 0, 100), 'offset': 10},  # 外围深红色
                {'color': (100, 20, 0, 50), 'offset': 15}  # 边缘暗红色
            ]

            for layer in flame_layers:
                offset_points = [(x + random.randint(-2, 2), y + layer['offset'] + random.randint(-2, 2))
                                 for x, y in flame_points]
                pygame.draw.polygon(frame, layer['color'], offset_points)

            # ------ 火星粒子系统 -------
            for _ in range(20):  # 增加粒子数量
                life = random.randint(0, 3)
                if life > 0:
                    alpha = 200 - life * 50
                    # 粒子起始位置在火焰底部
                    start_x = torch_width // 2 + random.randint(-15, 15)
                    start_y = torch_height - 50 - life * 5 + i * 3  # 粒子向上运动
                    # 粒子拖影效果
                    end_x = start_x + random.randint(-4, 4)
                    end_y = start_y + random.randint(-4, 4)
                    pygame.draw.line(frame, (255, 150, 50, alpha),
                                     (start_x, start_y), (end_x, end_y), 2)

            # ------ 光晕效果 -------
            glow = pygame.Surface((torch_width, torch_height), pygame.SRCALPHA)
            radius = 25 + i * 2  # 动态光晕半径
            for r in range(radius, 0, -2):
                alpha = max(0, 30 - r)  # 透明度递减
                glow_color = (255, 200, 100, alpha)
                temp_surface = pygame.Surface((r * 2, r * 2), pygame.SRCALPHA)
                pygame.draw.circle(temp_surface, glow_color, (r, r), r)
                glow.blit(temp_surface, (torch_width // 2 - r, torch_height - 50 - r))

            frame.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

            # ------ 随机闪烁亮点 -------
            for _ in range(3):
                x = torch_width // 2 + random.randint(-15, 15)
                y = torch_height - random.randint(50, 80)
                pygame.draw.circle(frame, (255, 255, 200, 100),
                                   (x, y), random.randint(2, 4))

            # ------ 火炬金属支架 -------
            # 垂直支架
            pygame.draw.rect(frame, (80, 80, 80),
                             (torch_width // 2 - 5, torch_height - 50, 10, 50))
            # 支架底座
            pygame.draw.polygon(frame, (100, 100, 100), [
                (torch_width // 2 - 15, torch_height - 40),
                (torch_width // 2 + 15, torch_height - 40),
                (torch_width // 2 + 20, torch_height - 30),
                (torch_width // 2 - 20, torch_height - 30)
            ])
            # 支架装饰
            for j in range(3):
                pygame.draw.circle(frame, (120, 120, 120),
                                   (torch_width // 2, torch_height - 50 + j * 15), 3)

            frames.append(frame)
        return frames

    def create_stone_texture(self):
        texture = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        # 绘制石头纹理
        for i in range(0, SCREEN_WIDTH, 20):
            for j in range(0, SCREEN_HEIGHT, 20):
                color = random.choice([(80, 80, 80), (70, 70, 70), (90, 90, 90)])
                pygame.draw.rect(texture, color, (i, j, 20, 20), border_radius=3)
                # 添加苔藓斑点
                if random.random() < 0.1:
                    pygame.draw.circle(texture, COLOR_MOSS,
                                       (i + random.randint(2, 18), j + random.randint(2, 18)),
                                       random.randint(2, 4))
        return texture

    def draw(self):
        # 绘制背景纹理
        self.screen.blit(self.background, (0, 0))

        # 绘制标题
        title_surf = self.font_title.render("Dungeon Tower", True, COLOR_UI_TEXT)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        self.screen.blit(title_surf, title_rect)

        # 按钮悬停状态
        mouse_pos = pygame.mouse.get_pos()
        self.start_button.hover = self.start_button.rect.collidepoint(mouse_pos)
        self.settings_button.hover = self.settings_button.rect.collidepoint(mouse_pos)

        # 绘制按钮
        self.start_button.draw(self.screen)
        self.settings_button.draw(self.screen)

        # 计算火炬位置
        torch_spacing = 50  # 标题与火炬间距

        # 左侧火炬
        torch_left_x = title_rect.left - torch_spacing - 3 * TILE_SIZE
        torch_left_y = title_rect.centery - 3 * TILE_SIZE  # 垂直居中

        # 右侧火炬
        torch_right_x = title_rect.right + torch_spacing

        # 绘制动态火炬
        self.torch_timer += 1
        if self.torch_timer >= 5:  # 加快动画速度
            self.torch_index = (self.torch_index + 1) % 8
            self.torch_timer = 0

        # 左侧火炬
        self.screen.blit(self.torch_frames[self.torch_index],
                         (torch_left_x, torch_left_y))

        # 右侧火炬（镜像）
        flipped_torch = pygame.transform.flip(self.torch_frames[self.torch_index], True, False)
        self.screen.blit(flipped_torch,
                         (torch_right_x, torch_left_y))

        # 添加标题装饰
        pygame.draw.line(self.screen, COLOR_UI_TEXT,
                         (title_rect.left - 50, title_rect.centery),
                         (title_rect.right + 50, title_rect.centery), 3)

        # 返回按钮区域用于点击检测
        return [self.start_button.rect, self.settings_button.rect]


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
        self.base_defense = 25  # 基础防御力
        self.base_attack_speed = 1.0  # 基础攻击速度
        self.base_attack_range = 1   # 基础攻击范围
        self.attack_cooldown = 0
        self.coins = 0
        self.equipped_weapon = None  # 当前装备的武器
        self.equipped_armor = None  # 当前装备的护甲
        self.skills = {
            'Q': {
                'name': "火球术",
                'cooldown': 5,
                'current_cd': 0,
                'range': 6,
                'radius': 2,
                'damage_multiple': 2.2,
                'effect': FireStrikeEffect
            },
            'E': {
                'name': "闪电链",
                'cooldown': 0.1,
                'current_cd': 0,
                'range': 8,
                'max_targets': 3,
                'damage_multiple': 1.8,
                'effect': LightningEffect
            },
            'R': {
                'name': "神圣球",
                'cooldown': 8,
                'current_cd': 0,
                'seek_range': 10,
                'ball_count': 12,
                'damage_multiple': 2.5,
                'effect': HollyBallEffect
            },
            'T': {
                'name': "三连斩",
                'cooldown': 6,
                'current_cd': 0,
                'range': 2,
                'damage_multipliers': [0.8, 1.0, 1.5],  # 三连斩伤害系数
                'effect': TripleAttack
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
            if random.random() < 0.4 and i < len(self.main_points) - 2:
                mid_point = (
                    (start_pos[0] + end_pos[0]) // 2 + random.randint(-5, 5),
                    (start_pos[1] + end_pos[1]) // 2 + random.randint(-5, 5)
                )
                branch_end = (
                    mid_point[0] + random.randint(-35, 35),
                    mid_point[1] + random.randint(-35, 35)
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

# ---------------- 圣光球 -------------------------


class HollyBallEffect:
    def __init__(self, player_pos, ball_count=6, seek_range=10, damage_multiplier=2.5):
        self.player_pos = player_pos
        self.ball_count = ball_count
        self.seek_range = seek_range
        self.damage_multiplier = damage_multiplier
        self.duration = 5.0
        self.progress = 0.0

        # Lightning balls data
        self.balls = []
        self.targets = []
        self.explosions = []

        # Initialize the balls with random positions around the player
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
                'particles': []
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

    def update(self, dt, monsters):
        self.progress += dt / self.duration
        damage_results = []

        # Process each ball
        for ball in self.balls:
            if ball['state'] == 'exploded':
                continue

            # Update particles for all balls
            self._update_ball_particles(ball, dt)

            # Seeking logic - find a target if needed
            if ball['state'] == 'seeking':
                if not ball['target']:
                    # Find nearby monsters within seek_range
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
                        # If no target, move in a circular pattern around player
                        self._update_seeking_movement(ball, dt)
                else:
                    ball['state'] = 'attacking'

            # Attacking logic - move toward target
            if ball['state'] == 'attacking' and ball['target']:
                monster = ball['target']

                # Check if monster still exists and is alive
                if monster not in monsters or monster.hp <= 0:
                    ball['target'] = None
                    ball['state'] = 'seeking'
                    continue

                # Calculate movement vector toward target
                target_pos = [
                    monster.x * TILE_SIZE + TILE_SIZE // 2,
                    monster.y * TILE_SIZE + TILE_SIZE // 2
                ]
                current_pos = ball['screen_pos']

                # Direction vector
                dx = target_pos[0] - current_pos[0]
                dy = target_pos[1] - current_pos[1]
                distance = math.hypot(dx, dy)

                # If reached the target, explode and damage
                if distance < TILE_SIZE:
                    # Record explosion
                    self.explosions.append({
                        'pos': (monster.x, monster.y),
                        'screen_pos': target_pos,
                        'time': 0.5,  # Explosion duration
                        'size': TILE_SIZE * 2,
                        'color': ball['color']
                    })

                    # Calculate damage
                    dmg = self.damage_multiplier * random.uniform(0.8, 1.2)
                    damage_results.append((monster, dmg))

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

    def _update_ball_particles(self, ball, dt):
        """Update the particles for a ball"""
        # Add new particles
        if ball['state'] != 'exploded' and random.random() < 0.3:
            angle = random.uniform(0, math.pi * 2)
            speed = random.uniform(0.5, 2.0)
            ball['particles'].append({
                'pos': ball['screen_pos'].copy(),
                'vel': [math.cos(angle) * speed, math.sin(angle) * speed],
                'life': random.uniform(0.3, 0.7),
                'max_life': 0.7,
                'size': random.uniform(1, 3),
                'color': self._lighten_color(ball['color'])
            })

        # Update existing particles
        for particle in ball['particles'][:]:
            particle['pos'][0] += particle['vel'][0]
            particle['pos'][1] += particle['vel'][1]
            particle['life'] -= dt

            # Remove dead particles
            if particle['life'] <= 0:
                ball['particles'].remove(particle)

    def _update_seeking_movement(self, ball, dt):
        """Update movement for a ball in seeking state"""
        # Orbit around the player's position with some randomness
        time = pygame.time.get_ticks() / 1000
        radius = 3 * TILE_SIZE

        # Calculate new position in a circular path
        ball['screen_pos'][0] = self.player_pos[0] * TILE_SIZE + TILE_SIZE // 2 + math.cos(
            time + ball['phase']) * radius
        ball['screen_pos'][1] = self.player_pos[1] * TILE_SIZE + TILE_SIZE // 2 + math.sin(
            time + ball['phase']) * radius

        # Add some randomness to make it look more dynamic
        ball['screen_pos'][0] += random.uniform(-5, 5)
        ball['screen_pos'][1] += random.uniform(-5, 5)

        # Update grid position
        ball['pos'][0] = ball['screen_pos'][0] // TILE_SIZE
        ball['pos'][1] = ball['screen_pos'][1] // TILE_SIZE

    def _calculate_distance(self, pos1, pos2):
        """Calculate Manhattan distance between two grid positions"""
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def _lighten_color(self, color):
        """Create a lighter version of the color for particles"""
        return tuple(min(c + 50, 255) for c in color)

    def draw(self, screen):
        """Draw the holy ball effect"""
        # Draw explosions (behind balls)
        for explosion in self.explosions:
            self._draw_explosion(screen, explosion)

        # Draw each holy ball
        for ball in self.balls:
            if ball['state'] == 'exploded':
                continue

            # Draw particles first (behind the ball)
            for particle in ball['particles']:
                alpha = int(255 * (particle['life'] / particle['max_life']))
                particle_color = (*particle['color'], alpha)

                # Draw particle
                pygame.draw.circle(
                    screen,
                    particle_color,
                    (int(particle['pos'][0]), int(particle['pos'][1])),
                    int(particle['size'] * (particle['life'] / particle['max_life']))
                )

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
                (int(ball['screen_pos'][0] - size * 1.25),
                 int(ball['screen_pos'][1] - size * 1.25))
            )

            # Draw core of the ball
            pygame.draw.circle(
                screen,
                ball['color'],
                (int(ball['screen_pos'][0]), int(ball['screen_pos'][1])),
                int(size)
            )

            # Draw inner light
            inner_color = (255, 255, 255)  # White center
            pygame.draw.circle(
                screen,
                inner_color,
                (int(ball['screen_pos'][0]), int(ball['screen_pos'][1])),
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

        # Draw random lightning bolts emanating from explosion center
        if random.random() < 0.4:
            for _ in range(2):
                angle = random.uniform(0, math.pi * 2)
                length = explosion['size'] * progress
                end_x = explosion['screen_pos'][0] + math.cos(angle) * length
                end_y = explosion['screen_pos'][1] + math.sin(angle) * length

                # Draw jagged lightning line
                points = self._generate_lightning_points(
                    explosion['screen_pos'],
                    (end_x, end_y),
                    4
                )

                if len(points) > 1:
                    for i in range(len(points) - 1):
                        pygame.draw.line(
                            screen,
                            explosion['color'],
                            points[i],
                            points[i + 1],
                            2
                        )

    def _draw_electric_arc(self, screen, ball):
        """Draw electric arcs from ball to target"""
        if not ball['target']:
            return

        # Get target position
        target_pos = [
            ball['target'].x * TILE_SIZE + TILE_SIZE // 2,
            ball['target'].y * TILE_SIZE + TILE_SIZE // 2
        ]

        # Generate lightning path
        points = self._generate_lightning_points(
            ball['screen_pos'],
            target_pos,
            5  # Number of segments
        )

        # Draw the lightning path
        if len(points) > 1:
            for i in range(len(points) - 1):
                # Alternate colors for more dynamic effect
                color = ball['color'] if i % 2 == 0 else (255, 255, 255)

                pygame.draw.line(
                    screen,
                    color,
                    points[i],
                    points[i + 1],
                    max(1, int(ball['size'] * 0.15))  # Line thickness
                )

    def _generate_lightning_points(self, start, end, segments):
        """Generate points for a jagged lightning effect"""
        points = [tuple(map(int, start))]

        dx = end[0] - start[0]
        dy = end[1] - start[1]

        for i in range(1, segments):
            # Calculate point along straight line
            t = i / segments
            x = start[0] + dx * t
            y = start[1] + dy * t

            # Add random displacement
            displacement = (1 - t) * 15  # More displacement near start
            x += random.uniform(-displacement, displacement)
            y += random.uniform(-displacement, displacement)

            points.append((int(x), int(y)))

        points.append(tuple(map(int, end)))
        return points

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


# -------------------------- 商店界面 -------------------------
def shop_screen(screen, player, floor):
    # 使用半透明遮罩层实现模态对话框效果
    font = pygame.font.SysFont("Arial", 24)
    clock = pygame.time.Clock()
    running = True

    overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 128))  # 半透明黑色背景

    shop_window = pygame.Surface((400, 380))
    shop_rect = shop_window.get_rect(center=screen.get_rect().center)
    while running:
        clock.tick(15)

        # 绘制背景遮罩
        # screen.blit(overlay, (0, 0))
        # 将商店窗口居中显示
        screen.blit(shop_window, shop_rect.topleft)
        pygame.display.flip()

        # 绘制商店窗口
        shop_window.fill((50, 50, 50))
        title = font.render("[Game Shop]", True, COLOR_TEXT)
        shop_window.blit(title, (20, 20))
        # 显示商店选项
        option1 = font.render(f"1. HP +{1000 * floor} (Costs {100 * floor} Coin)", True, COLOR_TEXT)
        option2 = font.render(f"2. ATK +{5 * floor} (Costs {100 * floor} Coin)", True, COLOR_TEXT)
        option3 = font.render(f"3. DEF +{5 * floor} (Costs {100 * floor} Coin)", True, COLOR_TEXT)
        option4 = font.render(f"4. HP +{10000 * floor} (Costs {1000 * floor} Coin)", True, COLOR_TEXT)
        option5 = font.render(f"5. ATK +{50 * floor} (Costs {1000 * floor} Coin)", True, COLOR_TEXT)
        option6 = font.render(f"6. DEF +{50 * floor} (Costs {1000 * floor} Coin)", True, COLOR_TEXT)
        shop_window.blit(option1, (20, 60))
        shop_window.blit(option2, (20, 100))
        shop_window.blit(option3, (20, 140))
        shop_window.blit(option4, (20, 180))
        shop_window.blit(option5, (20, 220))
        shop_window.blit(option6, (20, 260))
        info = font.render(f"Current Coin: [{player.coins}]", True, (255, 255, 0))
        shop_window.blit(info, (20, 300))
        prompt = font.render("Press Number Button Buy, Press ESC Exit", True, COLOR_TEXT)
        shop_window.blit(prompt, (20, 340))
        pygame.display.flip()

        # s商店选项
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_1:
                    if player.coins >= 100 * floor:
                        player.hp = min(player.hp + 1000 * floor, player.max_hp)
                        player.coins -= 100 * floor
                elif event.key == pygame.K_2:
                    if player.coins >= 100 * floor:
                        player.base_atk += 5 * floor
                        player.coins -= 100 * floor
                elif event.key == pygame.K_3:
                    if player.coins >= 100 * floor:
                        player.base_defense += 5 * floor
                        player.coins -= 100 * floor
                elif event.key == pygame.K_4:
                    if player.coins >= 1000 * floor:
                        player.hp = min(player.hp + 10000 * floor, player.max_hp)
                        player.coins -= 1000 * floor
                elif event.key == pygame.K_5:
                    if player.coins >= 1000 * floor:
                        player.base_atk += 50 * floor
                        player.coins -= 1000 * floor
                elif event.key == pygame.K_6:
                    if player.coins >= 1000 * floor:
                        player.base_defense += 50 * floor
                        player.coins -= 1000 * floor


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

        # 火球术（Q技能）
        if skill_key == 'Q':
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

        # 闪电链（R技能）
        elif skill_key == 'E':
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

        elif skill_key == 'R':
            # Create holy balls effect
            effect = HollyBallEffect(
                player_pos=(self.player.x, self.player.y),
                ball_count=skill['ball_count'],
                seek_range=skill['seek_range'],
                damage_multiplier=skill['damage_multiple']
            )
            self.skill_effects.append(effect)
            self.add_message(f"释放{skill['name']}!")

        elif skill_key == 'T':
            effect = TripleAttack(
                player_pos=(self.player.x, self.player.y),
                attack_range=skill['range'],
                damage_multiplier=skill['damage_multipliers']
            )
            self.skill_effects.append(effect)
            self.add_message(f"释放{skill['name']}!")

        skill['current_cd'] = skill['cooldown']

    # --------------- 游戏怪物绘制 -----------------

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

        # ------------------------- 攻击特效更新 -------------------------
        for effect in self.skill_effects[:]:
            if isinstance(effect, (WeaponSwingEffect,
                                   ProjectileEffect, ClawEffect)):
                if not effect.update(dt):
                    self.skill_effects.remove(effect)

        # ------------------------- 技能特效更新 -------------------------

        self.red_fear = False  # 血腥恐惧debuff
        self.blue_fear = False  # 血腥恐惧debuff
        self.gold_fear = False  # 血腥恐惧debuff
        # 更新所有技能特效
        for effect in self.skill_effects[:]:
            if isinstance(effect, IceBreathEffect):
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
            elif isinstance(effect, FireStrikeEffect):
                if not effect.update(dt):
                    self.skill_effects.remove(effect)
            elif isinstance(effect, BlueFireStrikeEffect):
                if not effect.update(dt):
                    self.skill_effects.remove(effect)
            elif isinstance(effect, LightningEffect):
                if not effect.update(dt):
                    self.skill_effects.remove(effect)
            elif isinstance(effect, HollyBallEffect):
                still_active, damage_results = effect.update(dt, self.monsters)
                # Apply damage to monsters
                for monster, damage_multiplier in damage_results:
                    if monster in self.monsters:  # Ensure monster still exists
                        dmg = self.player.atk * damage_multiplier
                        actual_damage = max(dmg - monster.defense, 0)
                        monster.hp -= actual_damage
                        self.add_message(f"神圣球对{monster.name}造成{actual_damage}点伤害！")

                        # Handle monster death
                        if monster.hp <= 0:
                            self.add_message(f"击败{monster.name}，获得{monster.coin}金币")
                            self.player.coins += monster.coin
                            self.monsters.remove(monster)
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

                        if monster.hp <= 0:
                            self.add_message(f"击败{monster.name}，获得{monster.coin}金币")
                            self.player.coins += monster.coin
                            self.monsters.remove(monster)
                if not still_active:
                    self.skill_effects.remove(effect)

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

        # 怪物移动逻辑，玩家在三个以内朝向玩家
        for monster in list(self.monsters):  # 使用副本遍历
            # 更新移动计数器
            monster.move_counter += 1
            if monster.move_counter < monster.speed:
                continue  # 未达到移动频率，跳过本次移动

            # 重置计数器
            monster.move_counter = 0

            # 计算与玩家的曼哈顿距离
            distance = abs(self.player.x - monster.x) + abs(self.player.y - monster.y)
            # 生成可能的移动方向
            directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
            random.shuffle(directions)  # 随机顺序尝试

            # 如果玩家在3格内，优先向玩家方向移动
            if distance <= MONSTER_DISTANCE:
                # 计算最佳移动方向（向玩家靠近）
                best_dir = None
                min_distance = float('inf')
                original_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
                for dx, dy in original_directions:
                    new_x = monster.x + dx
                    new_y = monster.y + dy
                    if self.can_monster_move_to(monster, new_x, new_y):
                        new_dist = abs(self.player.x - new_x) + abs(self.player.y - new_y)
                        if new_dist < min_distance:
                            min_distance = new_dist
                            best_dir = (dx, dy)
                if best_dir:
                    directions.insert(0, best_dir)  # 将最佳方向插入最前面

            for dx, dy in directions:
                new_x = monster.x + dx
                new_y = monster.y + dy
                if self.can_monster_move_to(monster, new_x, new_y):
                    monster.x = new_x
                    monster.y = new_y
                    break

        # 更新附近怪物列表
        self.nearby_monsters = []
        for monster in self.monsters:
            distance = abs(monster.x - self.player.x) + abs(monster.y - self.player.y)
            if distance <= 3:
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

        # ------ 技能面板 ------
        skill_height = 150  # 固定高度
        skill_bg = pygame.Surface((260, skill_height), pygame.SRCALPHA)
        skill_bg.fill((40, 40, 60, 200))
        pygame.draw.rect(skill_bg, (80, 80, 100), (0, 0, 260, skill_height), 2)

        skill_font = pygame.font.SysFont("SimSun", 18)
        for i, (key, skill) in enumerate(self.player.skills.items()):
            y_pos = 10 + i * 50
            # 技能名称
            name_color = (255, 255, 0) if skill['current_cd'] <= 0 else (100, 100, 100)
            skill_bg.blit(skill_font.render(f"{key}: {skill['name']}", True, name_color), (10, y_pos))
            # 冷却条
            cd_ratio = skill['current_cd'] / skill['cooldown'] if skill['current_cd'] > 0 else 0
            pygame.draw.rect(skill_bg, (80, 80, 80), (10, y_pos + 25, 240, 12))
            pygame.draw.rect(skill_bg, (0, 200, 0), (10, y_pos + 25, 240 * (1 - cd_ratio), 12))

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
                if not (0 <= x < MAP_WIDTH and 0 <= y < MAP_HEIGHT):
                    return False
                if self.maze[y][x] in [1, 2, 3, 4]:  # 墙壁
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
        button_rects = self.main_menu.draw()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_rects[0].collidepoint(event.pos):  # 开始按钮
                    self.game_state = "playing"
                elif button_rects[1].collidepoint(event.pos):  # 设置按钮
                    self.game_state = "settings"
        pygame.display.flip()

    def handle_settings(self):
        settings_menu = SettingsMenu(self.screen)
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                result = settings_menu.handle_event(event)
                if result == "menu":
                    return "menu"
                elif result == "apply":
                    return "apply"
            settings_menu.draw()

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
                elif event.key == pygame.K_b:
                    shop_screen(self.screen, self.player, self.floor)
                elif event.key == pygame.K_w:
                    self.player.move(0, -1, self)
                elif event.key == pygame.K_s:
                    self.player.move(0, 1, self)
                elif event.key == pygame.K_a:
                    self.player.move(-1, 0, self)
                elif event.key == pygame.K_d:
                    self.player.move(1, 0, self)
                elif event.key == pygame.K_q:
                    self.cast_skill('Q')
                elif event.key == pygame.K_e:
                    self.cast_skill('E')
                elif event.key == pygame.K_r:
                    self.cast_skill('R')
                elif event.key == pygame.K_t:
                    self.cast_skill('T')
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
