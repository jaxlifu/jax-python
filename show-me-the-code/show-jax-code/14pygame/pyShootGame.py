#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pygame
from random import randint
from pygame.locals import *
from sys import exit

SCREEN_WIDTH = 480
SCREEN_HEIGHT = 800
TYPE_SMALL = 1
TYPE_MIDDLE = 2
TYPE_BIG = 3


class ShootGame(object):
    def __init__(self):
        pygame.init()
        # 设置屏幕大小
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        # 设置标题
        pygame.display.set_caption('飞机大战')
        # 加载背景图片
        background = pygame.image.load('resources/image/background.png')
        game_over = pygame.image.load('resources/image/gameover.png')
        # 加载飞机图片
        plane_img = pygame.image.load('resources/image/shoot.png')
        # 加载背景音乐
        bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
        enemy1_down_sound = pygame.mixer.Sound(
            'resources/sound/enemy1_down.wav')
        game_ove_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
        bullet_sound.set_volume(0.3)
        enemy1_down_sound.set_volume(0.3)
        game_ove_sound.set_volume(0.3)
        pygame.mixer.music.load('resources/sound/game_music.wav')
        pygame.mixer.music.play(-1, 0.0)
        pygame.mixer.music.set_volume(0.25)

        # 设置玩家相关区域
        play_rect = []
        play_rect.append(pygame.Rect(0, 99, 102, 126))
        play_rect.append(pygame.Rect(165, 360, 102, 126))
        play_rect.append(pygame.Rect(165, 234, 102, 126))
        play_rect.append(pygame.Rect(330, 624, 102, 126))
        play_rect.append(pygame.Rect(330, 498, 102, 126))
        play_rect.append(pygame.Rect(432, 624, 102, 126))
        player_pos = [200, 600]
        player = Player(plane_img, play_rect, player_pos)

        # 设置子弹先关参数
        bullet_rect = pygame.Rect(1004, 987, 9, 21)
        bullet_img = plane_img.subsurface(bullet_rect)

        # 设置敌人先关参数
        enemy1_rect = pygame.Rect(534, 612, 57, 43)
        enemy1_img = plane_img.subsurface(enemy1_rect)
        enemy1_down_imgs = []
        enemy1_down_imgs.append(plane_img.subsurface(
            pygame.Rect(267, 347, 57, 43)))
        enemy1_down_imgs.append(plane_img.subsurface(
            pygame.Rect(873, 697, 57, 43)))
        enemy1_down_imgs.append(plane_img.subsurface(
            pygame.Rect(267, 296, 57, 43)))
        enemy1_down_imgs.append(plane_img.subsurface(
            pygame.Rect(930, 697, 57, 43)))

        enemies1 = pygame.sprite.Group()
        # 存储被击毁的飞机,用来渲染击毁精灵动画
        enemies_down = pygame.sprite.Group()

        shoot_frequency = 0
        enemy_frequency = 0
        player_down_index = 16
        score = 0
        clock = pygame.time.Clock()

        running = True
        while running:
            # 控制最大显示帧率
            clock.tick(60)
            # 控制子弹发射频率,发射子弹
            if not player.is_hit:
                if shoot_frequency % 15 == 0:
                    bullet_sound.play()
                    player.shoot(bullet_img)
                shoot_frequency += 1
                if shoot_frequency >= 15:
                    shoot_frequency = 0

            # 生成敌机
            if enemy_frequency % 50 == 0:
                enemy1_pos = [randint(0, SCREEN_WIDTH - enemy1_rect.width), 0]
                enemy1 = Enemy(enemy1_img, enemy1_down_imgs, enemy1_pos)
                enemies1.add(enemy1)
            enemy_frequency += 1
            if enemy_frequency >= 100:
                enemy_frequency = 0
            # 移动子弹,若超出屏幕范围就删除
            for bullet in player.bullets:
                bullet.move()
                if bullet.rect.bottom < 0:
                    player.bullets.remove(bullet)
            # 移动敌机,若超出窗口范围就删除
            for enemy in enemies1:
                enemy.move()
                # 判断是否击中玩家
                if pygame.sprite.collide_circle(enemy, player):
                    enemies_down.add(enemy)
                    enemies1.remove(enemy)
                    player.is_hit = True
                    game_ove_sound.play()
                    break
                if enemy.rect.top > SCREEN_HEIGHT:
                    enemies1.remove(enemy)
            # 将被击中的敌机对象添加到击毁敌机Group中,用来渲染击毁动画
            enemies1_down = pygame.sprite.groupcollide(
                enemies1, player.bullets, 1, 1)
            for enemy_down in enemies1_down:
                enemies_down.add(enemy_down)
            # 填充背景
            screen.fill(0)
            screen.blit(background, (0, 0))

            # 给玩家绘制飞机
            try:
                if not player.is_hit:
                    screen.blit(player.image[player.img_index], player.rect)
                    # 更换图片让飞机移动时有动画效果
                    player.img_index = shoot_frequency // 8
                else:
                    player.img_index = player_down_index // 8
                    screen.blit(player.image[player.img_index], player.rect)
                    player_down_index += 1
                    if player_down_index > 47:
                        running = False
            except Exception as e:
                print(e)

            # 绘制击毁动画
            for enemy_down in enemies_down:
                if enemy_down.down_index == 0:
                    enemy1_down_sound.play()
                if enemy_down.down_index >= 4:
                    enemies_down.remove(enemy_down)
                    score += 1000
                    continue
                screen.blit(
                    enemy_down.down_imgs[enemy_down.down_index], enemy_down.rect)
                enemy_down.down_index += 1

            # 绘制子弹和敌机
            player.bullets.draw(screen)
            enemies1.draw(screen)
            # 绘制得分
            score_font = pygame.font.Font(None, 36)
            score_text = score_font.render(str(score), True, (128, 128, 128))
            text_rect = score_text.get_rect()
            text_rect.topleft = [10, 10]
            screen.blit(score_text, text_rect)

            # 更新游戏界面
            pygame.display.update()

            key_pressed = pygame.key.get_pressed()
            if not player.is_hit:
                if key_pressed[K_UP] or key_pressed[K_w]:
                    player.moveUp()
                elif key_pressed[K_DOWN] or key_pressed[K_s]:
                    player.moveDown()
                elif key_pressed[K_LEFT] or key_pressed[K_a]:
                    player.moveLeft()
                elif key_pressed[K_RIGHT] or key_pressed[K_d]:
                    player.moveRight()
            # 获取退出事件
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

        font = pygame.font.Font(None, 48)
        text = font.render('Score%d' % score, True,
                           (250, 0, 0))
        text_rect = text.get_rect()
        text_rect.centerx = screen.get_rect().centerx
        text_rect.centery = screen.get_rect().centery + 24
        screen.blit(game_over, (0, 0))
        screen.blit(text, text_rect)

        pass
    pass


class Bullet(pygame.sprite.Sprite):
    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10
        pass

    def move(self):
        self.rect.top -= self.speed
        pass
    pass


class Player(pygame.sprite.Sprite):
    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = []

        for i in range(len(player_rect)):
            self.image.append(plane_img.subsurface(
                player_rect[i]).convert_alpha())
        self.rect = player_rect[0]
        self.rect.topleft = init_pos
        self.speed = 8
        self.bullets = pygame.sprite.Group()
        self.img_index = 0
        self.is_hit = False
        pass

    def moveUp(self):
        if self.rect.top - self.speed >= 0:
            self.rect.top -= self.speed
        pass

    def moveDown(self):
        if self.rect.top + self.speed < SCREEN_HEIGHT - self.rect.height:
            self.rect.top += self.speed
        pass

    def moveLeft(self):
        if self.rect.left - self.speed >= 0:
            self.rect.left -= self.speed
        pass

    def moveRight(self):
        if self.rect.left + self.speed < SCREEN_WIDTH - self.rect.width:
            self.rect.left += self.speed
        pass

    def shoot(self, bullet_img):
        bullet = Bullet(bullet_img, self.rect.midtop)
        self.bullets.add(bullet)
        pass
    pass


class Enemy(pygame.sprite.Sprite):

    def __init__(self, enemy_image, enemy_down_imgs, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.topleft = init_pos
        self.down_imgs = enemy_down_imgs
        self.speed = 2
        self.down_index = 0
        pass

    def move(self):
        self.rect.top += self.speed
        pass
    pass


if __name__ == '__main__':
    game = ShootGame()
