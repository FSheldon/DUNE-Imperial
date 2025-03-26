import pygame
import os
import random

# 初始化 Pygame
pygame.init()

# 设置窗口大小
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("桌游前端示例")

# 定义颜色
WHITE = (255, 255, 255)
ENEMY_COLOR = (100, 100, 100)

# 纯数据类：Card 只存储信息，不处理 Pygame 逻辑
class Card:
    def __init__(self, card_type):
        self.card_type = card_type
        self.used = False
    
    def trigger_event(self, enemy):
        if self.card_type == "attack":
            print("攻击卡牌生效！对敌人造成 20 点伤害。")
            enemy.take_damage(20)
        elif self.card_type == "defense":
            print("防御卡牌生效！减少即将受到的伤害。")
        elif self.card_type == "magic":
            print("魔法卡牌生效！释放特殊技能。")
        self.used = True

# 处理卡片显示的类
class CardView(pygame.sprite.Sprite):
    def __init__(self, x, y, card, enemy):
        super().__init__()
        self.card = card
        self.enemy = enemy
        self.image = pygame.image.load(os.path.join("assets/cards", f"{card.card_type}.jpg")).convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 150))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.dragging = False
        self.animation_counter = 0

    def update(self, event_list):
        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                self.dragging = True
            elif event.type == pygame.MOUSEBUTTONUP:
                if self.dragging:
                    self.card.trigger_event(self.enemy)
                self.dragging = False
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self.rect.move_ip(event.rel)

    def draw(self, surface):
        if self.animation_counter > 0:
            effect = pygame.Surface((120, 170), pygame.SRCALPHA)
            effect.fill((255, 255, 255, 100))
            surface.blit(effect, (self.rect.x - 10, self.rect.y - 10))
            self.animation_counter -= 1
        surface.blit(self.image, self.rect)

# 敌人类
class Enemy:
    def __init__(self, health=100):
        self.health = health
    
    def take_damage(self, amount):
        self.health -= amount
        print(f"敌人受到 {amount} 点伤害，剩余血量: {self.health}")
        if self.health <= 0:
            print("敌人被击败！")

# 统一管理卡片的类
class CardManager:
    def __init__(self, enemy):
        self.cards = [
            CardView(200, 400, Card("attack"), enemy),
            CardView(350, 400, Card("defense"), enemy),
            CardView(500, 400, Card("magic"), enemy)
        ]
    
    def update(self, event_list):
        for card_view in self.cards:
            card_view.update(event_list)
    
    def draw(self, surface):
        for card_view in self.cards:
            card_view.draw(surface)

# 创建敌人和卡片管理器
enemy = Enemy()
card_manager = CardManager(enemy)

def main():
    running = True
    while running:
        screen.fill(WHITE)
        event_list = pygame.event.get()
        
        for event in event_list:
            if event.type == pygame.QUIT:
                running = False
        
        card_manager.update(event_list)  # 更新卡牌
        card_manager.draw(screen)  # 绘制卡牌
        pygame.display.flip()
    
    pygame.quit()

if __name__ == "__main__":
    main()

