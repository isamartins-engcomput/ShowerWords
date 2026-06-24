import pygame
import random
import math

QWERTY_MAP = {
    'q':(0,0), 'w':(1,0), 'e':(2,0), 'r':(3,0), 't':(4,0), 'y':(5,0), 'u':(6,0), 'i':(7,0), 'o':(8,0), 'p':(9,0),
    'a':(0.5,1), 's':(1.5,1), 'd':(2.5,1), 'f':(3.5,1), 'g':(4.5,1), 'h':(5.5,1), 'j':(6.5,1), 'k':(7.5,1), 'l':(8.5,1),
    'z':(1.5,2), 'x':(2.5,2), 'c':(3.5,2), 'v':(4.5,2), 'b':(5.5,2), 'n':(6.5,2), 'm':(7.5,2)
}

class WordInstance:
    def __init__(self, text, x, y, speed, color=(255, 255, 255), is_boss=False, points=10):
        self.text = text
        self.x = x
        self.y = y
        self.speed = speed
        self.color = color
        self.is_boss = is_boss
        self.points = points 

    def fall(self):
        self.y += self.speed

    def draw(self, surface, font, fallback_color=(255,255,255)):
        current_color = self.color
        if self.is_boss:
            current_color = (255, 255, 255) if (pygame.time.get_ticks() // 100) % 2 == 0 else (10, 246, 0)

        text_surface = font.render(self.text, True, current_color)
        text_rect = text_surface.get_rect(midtop=(self.x, self.y))
        surface.blit(text_surface, text_rect)

class WordFactory:
    def __init__(self, word_list, screen_width):
        self.word_list = word_list
        self.screen_width = screen_width
        
        self.easy_words = [w for w in self.word_list if len(w) <= 4]
        self.med_words  = [w for w in self.word_list if 4 < len(w) <= 8]
        self.hard_words = [w for w in self.word_list if len(w) > 8]

        self.easy_bag = []
        self.med_bag = []
        self.hard_bag = []

        self.last_difficulty = 'easy'

    def get_next_word(self, difficulty):
        """Puxa a palavra da sacola correta, reabastecendo quando esvazia"""
        if difficulty == 'hard':
            if not self.hard_bag:
                self.hard_bag = list(self.hard_words)
                random.shuffle(self.hard_bag)
            return self.hard_bag.pop() if self.hard_bag else "multithreading"
            
        elif difficulty == 'easy':
            if not self.easy_bag:
                self.easy_bag = list(self.easy_words)
                random.shuffle(self.easy_bag)
            return self.easy_bag.pop() if self.easy_bag else "bug"
            
        else:
            if not self.med_bag:
                self.med_bag = list(self.med_words)
                random.shuffle(self.med_bag)
            return self.med_bag.pop() if self.med_bag else "python"

    def calcular_bonus_de_velocidade(self, palavra):
        if len(palavra) <= 1 or "|" in palavra: return 0.0
        
        distancia_total = 0
        transicoes_validas = 0
        for i in range(len(palavra) - 1):
            char1, char2 = palavra[i], palavra[i+1]
            if char1 in QWERTY_MAP and char2 in QWERTY_MAP:
                x1, y1 = QWERTY_MAP[char1]
                x2, y2 = QWERTY_MAP[char2]
                distancia_total += math.hypot(x2 - x1, y2 - y1)
                transicoes_validas += 1
                
        distancia_media = (distancia_total / transicoes_validas) if transicoes_validas > 0 else 2.0
        bonus_tamanho = max(0.0, 5.0 - len(palavra)) * 0.2 
        bonus_proximidade = max(0.0, 3.0 - distancia_media) * 0.15 
        return bonus_tamanho + bonus_proximidade

    def spawn_word(self, current_score, shower_center_x, shower_bottom_y, is_troll=False, is_boss=False):
        base_speed = 0.8 
        acceleration_k = 0.006 
        color = (255, 255, 255) 

        if is_boss:
            self.last_difficulty = 'hard'
            random_word = self.get_next_word('hard') 
            calculated_speed = (base_speed + (acceleration_k * current_score)) * 0.6
            return WordInstance(random_word, shower_center_x, shower_bottom_y, calculated_speed, color, is_boss=True, points=20)
            
        elif is_troll:
            random_word = " | | | "
            calculated_speed = (base_speed + (acceleration_k * current_score)) * 1.8
            return WordInstance(random_word, shower_center_x, shower_bottom_y, calculated_speed, color, is_boss=False, points=0)
            
        else:
            if self.last_difficulty == 'hard':
                next_diff = 'easy' if random.random() < 0.6 else 'med'
                
            elif self.last_difficulty == 'easy':
                roleta = random.random()
                if roleta < 0.5: next_diff = 'med'
                elif roleta < 0.8: next_diff = 'easy'
                else: next_diff = 'hard'
                
            else:
                roleta = random.random()
                if roleta < 0.4: next_diff = 'easy'
                elif roleta < 0.8: next_diff = 'med'
                else: next_diff = 'hard'

            self.last_difficulty = next_diff
            random_word = self.get_next_word(next_diff)
            
            if next_diff == 'hard':
                calculated_speed = (base_speed + (acceleration_k * current_score)) * 0.6
                return WordInstance(random_word, shower_center_x, shower_bottom_y, calculated_speed, color, is_boss=True, points=20)
            else:
                word_bonus = self.calcular_bonus_de_velocidade(random_word)
                calculated_speed = base_speed + (acceleration_k * current_score) + word_bonus
                valor_em_pontos = 5 if next_diff == 'easy' else 10
                return WordInstance(random_word, shower_center_x, shower_bottom_y, calculated_speed, color, is_boss=False, points=valor_em_pontos)
            
class Particle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = random.uniform(-3, 3)
        self.vy = random.uniform(-2, -6) 
        self.color = color
        self.lifetime = random.randint(15, 30)
        self.size = random.randint(2, 4)

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.vy += 0.3
        self.lifetime -= 1

    def draw(self, surface):
        if self.lifetime > 0:
            pygame.draw.rect(surface, self.color, (int(self.x), int(self.y), self.size, self.size))