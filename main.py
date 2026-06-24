import pygame
import sys
import random
from rbtree import RedBlackTree
from entities import WordFactory, Particle

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Shower Words - Seminário ED2")

BLACK = (0, 0, 0)
TERMINAL_GREEN = (10, 246, 0)     
WHITE = (255, 255, 255)   

BASE_Y = HEIGHT - 90
SHOWER_CENTER_X = WIDTH // 2
SHOWER_Y = 20

try:
    pixel_font = pygame.font.Font("assets/pixel_font.ttf", 25)
    title_font = pygame.font.Font("assets/pixel_font.ttf", 40)
    small_pixel_font = pygame.font.Font("assets/pixel_font.ttf", 20)
    error_font = pygame.font.Font("assets/pixel_font.ttf", 14)
except FileNotFoundError:
    print("Aviso: 'assets/pixel_font.ttf' não encontrada.")
    pixel_font = pygame.font.Font(None, 36)
    title_font = pygame.font.Font(None, 64)
    small_pixel_font = pygame.font.Font(None, 20)
    error_font = pygame.font.Font(None, 14)

try:
    logo_img = pygame.image.load("assets/logo.png").convert_alpha()
except FileNotFoundError:
    logo_img = None

try:
    raw_hud_img = pygame.image.load("assets/hud_logo.png").convert_alpha()
    bounding_box = raw_hud_img.get_bounding_rect()
    if bounding_box.width > 0 and bounding_box.height > 0:
        hud_logo_img = raw_hud_img.subsurface(bounding_box).copy()
    else:
        hud_logo_img = raw_hud_img
        
    ref_surf = small_pixel_font.render("SCORE: 0", True, TERMINAL_GREEN)
    target_w = ref_surf.get_width() 
    
    orig_w, orig_h = hud_logo_img.get_size()
    target_h = int(orig_h * (target_w / orig_w))
    
    hud_logo_img = pygame.transform.scale(hud_logo_img, (target_w, target_h))
    
except FileNotFoundError:
    hud_logo_img = None

def draw_shower(surface, x, y):
    pillar_x = WIDTH - 20     
    pygame.draw.rect(surface, TERMINAL_GREEN, (x, y, pillar_x - x, 15))     
    pygame.draw.rect(surface, TERMINAL_GREEN, (pillar_x, y, 6, 3))
    pygame.draw.rect(surface, TERMINAL_GREEN, (pillar_x, y + 3, 10, 3))
    pygame.draw.rect(surface, TERMINAL_GREEN, (pillar_x, y + 6, 13, 3))
    pygame.draw.rect(surface, TERMINAL_GREEN, (pillar_x, y + 9, 15, 6))    
    pygame.draw.rect(surface, TERMINAL_GREEN, (pillar_x, y + 15, 15, BASE_Y - y - 15)) 
    pygame.draw.rect(surface, TERMINAL_GREEN, (x - 7, y, 15, 3))
    pygame.draw.rect(surface, TERMINAL_GREEN, (x - 10, y + 3, 18, 3))
    pygame.draw.rect(surface, TERMINAL_GREEN, (x - 13, y + 6, 21, 3))
    pygame.draw.rect(surface, TERMINAL_GREEN, (x - 15, y + 9, 23, 11))
    pygame.draw.rect(surface, TERMINAL_GREEN, (x - 15, y + 20, 30, 4))
    pygame.draw.rect(surface, TERMINAL_GREEN, (x - 22, y + 24, 44, 4))
    pygame.draw.rect(surface, TERMINAL_GREEN, (x - 30, y + 28, 60, 4))
    pygame.draw.rect(surface, TERMINAL_GREEN, (x - 40, y + 32, 80, 4))
    pygame.draw.rect(surface, TERMINAL_GREEN, (x - 50, y + 36, 100, 4))
    pygame.draw.rect(surface, TERMINAL_GREEN, (x - 58, y + 40, 116, 4))    
    pygame.draw.rect(surface, TERMINAL_GREEN, (x - 60, y + 44, 120, 6))
    pygame.draw.rect(surface, TERMINAL_GREEN, (x - 65, y + 55, 130, 12))

def load_dictionary(filepath, tree):
    word_list = []
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            for line in file:
                word = line.strip().lower()
                if word:
                    tree.insert(word)
                    word_list.append(word)
        return word_list
    except FileNotFoundError:
        print(f"Erro crítico: Arquivo '{filepath}' não encontrado.")
        sys.exit()

def draw_text(surface, text, font, color, x, y, align="left"):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    if align == "center": text_rect.center = (x, y)
    elif align == "right": text_rect.bottomright = (x, y)
    else: text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def main():
    word_tree = RedBlackTree()
    word_list = load_dictionary("words.txt", word_tree) 
    factory = WordFactory(word_list, WIDTH)
    
    pygame.mixer.init()
    try:
        pygame.mixer.music.load("assets/music.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    except pygame.error:
        print("Aviso: Arquivo de trilha sonora 'assets/music.mp3' não encontrado. O jogo rodará em modo silencioso.")
    
    clock = pygame.time.Clock()
    running = True
    game_state = "START" 
    current_input = ""
    score = 0
    
    lives = 3 
    
    active_words = []
    active_particles = []
    
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, 2500)

    error_timer = 0
    show_error = False
    
    damage_timer = 0
    show_damage = False
    
    last_milestone = 0
    congrats_timer = 0
    show_congrats = False
    last_boss_milestone = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_state == "START":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_state = "PLAYING" 
            
            elif game_state == "PLAYING":
                if event.type == SPAWN_EVENT:
                    current_boss_milestone = score // 50
                    
                    if current_boss_milestone > last_boss_milestone and score >= 50:
                        new_word = factory.spawn_word(score, SHOWER_CENTER_X, SHOWER_Y + 70, is_boss=True)
                        last_boss_milestone = current_boss_milestone
                    else:
                        troll_chance = random.random() < 0.25 
                        new_word = factory.spawn_word(score, SHOWER_CENTER_X, SHOWER_Y + 70, is_troll=troll_chance)
                    
                    active_words.append(new_word)
                    
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        palavra_digitada = current_input.lower().strip()
                        result = word_tree.search(palavra_digitada)
                        
                        word_removed = False 

                        if result != word_tree.TNULL:
                            for word_obj in active_words[:]:
                                if word_obj.text.lower().strip() == palavra_digitada:
                                    cor_explosao = (10, 246, 0) if word_obj.is_boss else WHITE
                                    for _ in range(15):
                                        active_particles.append(Particle(word_obj.x, word_obj.y, cor_explosao))
                                    
                                    active_words.remove(word_obj) 
                                    score += word_obj.points 
                                    word_removed = True
                                    
                                    current_milestone = score // 100
                                    if current_milestone > last_milestone:
                                        last_milestone = current_milestone
                                        show_congrats = True
                                        congrats_timer = pygame.time.get_ticks()
                                        
                                        novo_tempo = max(800, 2500 - (current_milestone * 200))
                                        pygame.time.set_timer(SPAWN_EVENT, novo_tempo)
                                    break
                        
                        if not word_removed and palavra_digitada != "":
                            show_error = True
                            error_timer = pygame.time.get_ticks() 
                            
                        current_input = ""
                    
                    elif event.key == pygame.K_BACKSPACE:
                        current_input = current_input[:-1]
                    else:
                        current_input += event.unicode
                        
            elif game_state == "GAME_OVER":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    game_state = "PLAYING"
                    score = 0
                    lives = 3
                    active_words.clear()
                    active_particles.clear()
                    current_input = ""
                    last_milestone = 0
                    last_boss_milestone = 0
                    show_congrats = False
                    pygame.time.set_timer(SPAWN_EVENT, 2500) 

        if game_state == "PLAYING":
            for word_obj in active_words[:]: 
                word_obj.fall()
                
                if "|" in word_obj.text:
                    if random.random() < 0.3:
                        gota = Particle(word_obj.x + random.randint(-40, 40), word_obj.y, WHITE)
                        gota.vy = random.uniform(1, 3) 
                        gota.lifetime = random.randint(5, 12)
                        active_particles.append(gota)
                
                if word_obj.y > BASE_Y:
                    if "|" not in word_obj.text:
                        for _ in range(15):
                            active_particles.append(Particle(word_obj.x, BASE_Y, TERMINAL_GREEN))
                        
                        lives -= 1
                        show_damage = True
                        damage_timer = pygame.time.get_ticks()
                        
                        if lives <= 0:
                            game_state = "GAME_OVER"
                    else:
                        for _ in range(12):
                            respingo = Particle(word_obj.x + random.randint(-40, 40), BASE_Y, WHITE)
                            respingo.vy = random.uniform(-1, -4)
                            active_particles.append(respingo)
                    
                    active_words.remove(word_obj)

            for p in active_particles[:]:
                p.update()
                if p.lifetime <= 0:
                    active_particles.remove(p)

        screen.fill(BLACK)
        
        if game_state == "START":
            if logo_img:
                screen.blit(logo_img, logo_img.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
            else:
                draw_text(screen, "SHOWER WORDS", title_font, TERMINAL_GREEN, WIDTH // 2, HEIGHT // 2 - 50, align="center")
            
            if pygame.time.get_ticks() % 1000 < 500:
                draw_text(screen, "PRESS ENTER TO START", pixel_font, WHITE, WIDTH // 2, HEIGHT // 2 + 150, align="center")
                
        elif game_state == "PLAYING":
            draw_shower(screen, SHOWER_CENTER_X, SHOWER_Y)

            draw_text(screen, "HP:", small_pixel_font, TERMINAL_GREEN, 20, 20)
            for i in range(3):
                rect_x = 85 + (i * 20)
                
                if i < lives:
                    pygame.draw.rect(screen, TERMINAL_GREEN, (rect_x, 22, 12, 12))
                else:
                    pygame.draw.rect(screen, TERMINAL_GREEN, (rect_x, 22, 12, 12), 1)

            if show_congrats and pygame.time.get_ticks() - congrats_timer < 2000:
                pisca_cor = WHITE if (pygame.time.get_ticks() // 100) % 2 == 0 else TERMINAL_GREEN
                mensagem_congrats = f"[OK] SYSTEM OVERCLOCK: {last_milestone * 100} PTS"
                draw_text(screen, mensagem_congrats, small_pixel_font, pisca_cor, WIDTH // 2, BASE_Y - 40, align="center")
                
            for p in active_particles:
                p.draw(screen)

            for word_obj in active_words:
                word_obj.draw(screen, pixel_font, WHITE)
                
            pygame.draw.line(screen, TERMINAL_GREEN, (0, BASE_Y), (WIDTH, BASE_Y), 2)

            alerta_y = HEIGHT - 70
            
            if show_damage and pygame.time.get_ticks() - damage_timer < 800:
                draw_text(screen, "WARNING: MEMORY LEAK DETECTED", error_font, WHITE, 20, alerta_y)
                alerta_y -= 15

            if show_error and pygame.time.get_ticks() - error_timer < 800:
                draw_text(screen, "SYNTAX ERROR: INVALID WORD", error_font, TERMINAL_GREEN, 20, alerta_y)
            
            cursor = "_" if pygame.time.get_ticks() % 1000 < 500 else " "
            input_surface = pixel_font.render(f"> {current_input}{cursor}", True, TERMINAL_GREEN)
            screen.blit(input_surface, (20, HEIGHT - 50))
            
            score_surf = small_pixel_font.render(f"SCORE: {score}", True, TERMINAL_GREEN)
            score_rect = score_surf.get_rect(bottomright=(WIDTH - 20, HEIGHT - 20))
            
            if hud_logo_img:
                hud_logo_rect = hud_logo_img.get_rect(bottomright=(WIDTH - 20, score_rect.top - 8))
                screen.blit(hud_logo_img, hud_logo_rect)
            else:
                hud_text = "SHOWER WORDS"
                hud_surf = small_pixel_font.render(hud_text, True, TERMINAL_GREEN)
                hud_rect = hud_surf.get_rect(bottomright=(WIDTH - 15, score_rect.top - 5))
                border_rect = hud_rect.inflate(10, 10) 
                pygame.draw.rect(screen, TERMINAL_GREEN, border_rect, 2, border_radius=5)
                screen.blit(hud_surf, hud_rect)
            
            screen.blit(score_surf, score_rect)
        
        elif game_state == "GAME_OVER":
            draw_text(screen, "CRITICAL SYSTEM", title_font, TERMINAL_GREEN, WIDTH // 2, HEIGHT // 2 - 50, align="center")
            draw_text(screen, f"FINAL SCORE: {score}", pixel_font, TERMINAL_GREEN, WIDTH // 2, HEIGHT // 2 + 20, align="center")
            
            if pygame.time.get_ticks() % 1000 < 500:
                draw_text(screen, "PRESS ENTER TO REBOOT", pixel_font, WHITE, WIDTH // 2, HEIGHT // 2 + 80, align="center")
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()