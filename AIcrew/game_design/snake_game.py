import pygame                                                                                                                                                                            
import random                                                                                                                                                                            
import os                                                                                                                                                                                
                                                                                                                                                                                        
# --- Constantes do Jogo ---                                                                                                                                                             
# Dimensões da tela                                                                                                                                                                      
WIDTH, HEIGHT = 600, 400                                                                                                                                                                 
GRID_SIZE = 20  # Tamanho de cada segmento da cobra / bloco de comida                                                                                                                    
GRID_WIDTH = WIDTH // GRID_SIZE  # Número de blocos na largura                                                                                                                           
GRID_HEIGHT = HEIGHT // GRID_SIZE # Número de blocos na altura                                                                                                                           
                                                                                                                                                                                        
# Cores                                                                                                                                                                                  
BLACK = (0, 0, 0)                                                                                                                                                                        
WHITE = (255, 255, 255)                                                                                                                                                                  
GREEN = (0, 255, 0)                                                                                                                                                                      
RED = (255, 0, 0)                                                                                                                                                                        
GRAY = (100, 100, 100)                                                                                                                                                                   
                                                                                                                                                                                        
# Direções de movimento da cobra                                                                                                                                                         
UP = (0, -1)                                                                                                                                                                             
DOWN = (0, 1)                                                                                                                                                                            
LEFT = (-1, 0)                                                                                                                                                                           
RIGHT = (1, 0)                                                                                                                                                                           
                                                                                                                                                                                        
# Nome do arquivo de recorde                                                                                                                                                             
HIGH_SCORE_FILE = "highscore.txt"                                                                                                                                                        
                                                                                                                                                                                        
# Pontuação por comida                                                                                                                                                                   
POINTS_PER_FOOD = 10                                                                                                                                                                     
# Incremento de velocidade por comida                                                                                                                                                    
SPEED_INCREMENT_PER_FOOD = 0.5                                                                                                                                                           
# Velocidade inicial do jogo                                                                                                                                                             
INITIAL_GAME_SPEED = 10 # frames por segundo                                                                                                                                             
                                                                                                                                                                                        
# --- Inicialização do Pygame ---                                                                                                                                                        
pygame.init()                                                                                                                                                                            
pygame.display.set_caption("Jogo da Cobra (Snake Game)")                                                                                                                                 
screen = pygame.display.set_mode((WIDTH, HEIGHT))                                                                                                                                        
clock = pygame.time.Clock()                                                                                                                                                              
                                                                                                                                                                                        
# Tenta encontrar uma fonte padrão, caso 'arial' não esteja disponível                                                                                                                   
try:                                                                                                                                                                                     
    font_path = pygame.font.match_font('arial')                                                                                                                                          
    font = pygame.font.Font(font_path, 24)                                                                                                                                               
    game_over_font = pygame.font.Font(font_path, 48)                                                                                                                                     
except:                                                                                                                                                                                  
    # Fallback para fonte padrão se nenhuma for encontrada                                                                                                                               
    # Adicionando verificação para garantir que SysFont está disponível                                                                                                                  
    if pygame.font:                                                                                                                                                                      
        font = pygame.font.SysFont(None, 24)                                                                                                                                             
        game_over_font = pygame.font.SysFont(None, 48)                                                                                                                                   
    else:                                                                                                                                                                                
        # Se SysFont também falhar (muito improvável), usar uma fonte dummy                                                                                                              
        # Isso pode gerar erros de renderização, mas evita um crash imediato                                                                                                             
        print("Warning: Could not load any font. Text rendering might fail.")                                                                                                            
        class DummyFont:                                                                                                                                                                 
            # Implementa os métodos básicos esperados por pygame.Font                                                                                                                    
            def render(self, text, antialias, color):                                                                                                                                    
                # Retorna uma superfície vazia para evitar erros                                                                                                                         
                # antialias é um booleano, color é uma tupla RGB                                                                                                                         
                return pygame.Surface((10, 10)) # Retorna uma superfície pequena para placeholder                                                                                        
            def get_width(self, text=""): # Adiciona um parâmetro text para compatibilidade                                                                                              
                return 10 # Largura dummy                                                                                                                                                
            def get_height(self):                                                                                                                                                        
                return 10 # Altura dummy                                                                                                                                                 
        font = DummyFont()                                                                                                                                                               
        game_over_font = DummyFont()                                                                                                                                                     
                                                                                                                                                                                        
                                                                                                                                                                                        
# --- Funções de Recorde (High Score) ---                                                                                                                                                
def load_high_score():                                                                                                                                                                   
    """Carrega o recorde salvo em arquivo."""                                                                                                                                            
    if os.path.exists(HIGH_SCORE_FILE):                                                                                                                                                  
        with open(HIGH_SCORE_FILE, "r") as file:                                                                                                                                         
            try:                                                                                                                                                                         
                return int(file.read())                                                                                                                                                  
            except ValueError:                                                                                                                                                           
                # Caso o arquivo esteja corrompido ou vazio, retorna 0                                                                                                                   
                print(f"Warning: High score file '{HIGH_SCORE_FILE}' is corrupted or empty. Resetting high score to 0.")                                                                 
                return 0                                                                                                                                                                 
            except Exception as e:                                                                                                                                                       
                # Captura outras exceções inesperadas na leitura do arquivo                                                                                                              
                print(f"Error reading high score file '{HIGH_SCORE_FILE}': {e}. Resetting high score to 0.")                                                                             
                return 0                                                                                                                                                                 
    return 0                                                                                                                                                                             
                                                                                                                                                                                        
def save_high_score(score):                                                                                                                                                              
    """Salva o recorde atual em arquivo."""                                                                                                                                              
    try:                                                                                                                                                                                 
        with open(HIGH_SCORE_FILE, "w") as file:                                                                                                                                         
            file.write(str(score))                                                                                                                                                       
    except IOError as e:                                                                                                                                                                 
        print(f"Error saving high score to '{HIGH_SCORE_FILE}': {e}")                                                                                                                    
                                                                                                                                                                                        
# --- Classe da Cobra ---                                                                                                                                                                
class Snake:                                                                                                                                                                             
    def __init__(self):                                                                                                                                                                  
        """Inicializa a cobra com uma posição, direção e comprimento padrão."""                                                                                                          
        # Corpo inicial da cobra, garantindo que não saia das bordas em grades pequenas                                                                                                  
        initial_head_x = GRID_WIDTH // 2                                                                                                                                                 
        initial_head_y = GRID_HEIGHT // 2                                                                                                                                                
                                                                                                                                                                                        
        # Certifica-se que há espaço suficiente para o corpo inicial de 3 segmentos                                                                                                      
        # Se a grade for muito pequena para 3 segmentos horizontais, inicializa com 1 segmento                                                                                           
        if GRID_WIDTH < 3:                                                                                                                                                               
            self.body = [(0, 0)]                                                                                                                                                         
            print("Warning: GRID_WIDTH is too small for default snake body (3 segments). Initializing with a single segment at (0,0).")                                                  
        else:                                                                                                                                                                            
            self.body = [(initial_head_x, initial_head_y),                                                                                                                               
                        (initial_head_x - 1, initial_head_y),                                                                                                                           
                        (initial_head_x - 2, initial_head_y)]                                                                                                                           
                                                                                                                                                                                        
                                                                                                                                                                                        
        self.direction = RIGHT                                                                                                                                                           
        self.grow = False  # Flag para indicar se a cobra deve crescer no próximo movimento                                                                                              
                                                                                                                                                                                        
    def change_direction(self, new_direction):                                                                                                                                           
        """                                                                                                                                                                              
        Altera a direção da cobra, impedindo que ela se mova na direção oposta à sua atual.                                                                                              
        Ex: se estiver indo para a direita, não pode ir imediatamente para a esquerda.                                                                                                   
        """                                                                                                                                                                              
        # Verifica se a nova direção é a oposta à atual                                                                                                                                  
        # Calcula a direção oposta: (dx * -1, dy * -1)                                                                                                                                   
        opposite_direction = (self.direction[0] * -1, self.direction[1] * -1)                                                                                                            
        if new_direction == opposite_direction:                                                                                                                                          
            return # Não permite a mudança                                                                                                                                               
        self.direction = new_direction                                                                                                                                                   
                                                                                                                                                                                        
    def move(self):                                                                                                                                                                      
        """Move a cobra um passo na sua direção atual."""                                                                                                                                
        head_x, head_y = self.body[0]                                                                                                                                                    
        new_head = (head_x + self.direction[0], head_y + self.direction[1])                                                                                                              
                                                                                                                                                                                        
        self.body.insert(0, new_head)  # Adiciona a nova cabeça ao início do corpo                                                                                                       
                                                                                                                                                                                        
        if not self.grow:                                                                                                                                                                
            self.body.pop()  # Remove a cauda se a cobra não estiver crescendo                                                                                                           
        else:                                                                                                                                                                            
            self.grow = False  # Reseta a flag de crescimento após crescer                                                                                                               
                                                                                                                                                                                        
    def draw(self, screen):                                                                                                                                                              
        """Desenha a cobra na tela."""                                                                                                                                                   
        for segment in self.body:                                                                                                                                                        
            # Verifica se o segmento está dentro dos limites da tela antes de desenhar                                                                                                   
            # Isso é uma precaução para não tentar desenhar segmentos completamente fora da área visível                                                                                 
            # após uma colisão com a parede, o que visualmente pode ser mais limpo.                                                                                                      
            if 0 <= segment[0] < GRID_WIDTH and 0 <= segment[1] < GRID_HEIGHT:                                                                                                           
                pygame.draw.rect(screen, GREEN, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))                                                                  
                # Desenha um contorno preto para cada segmento para melhor visibilidade                                                                                                  
                pygame.draw.rect(screen, BLACK, (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)                                                               
                                                                                                                                                                                        
    def check_collision(self):                                                                                                                                                           
        """                                                                                                                                                                              
        Verifica colisões com as paredes do jogo ou com o próprio corpo da cobra.                                                                                                        
        Retorna True se houver colisão, False caso contrário.                                                                                                                            
        """                                                                                                                                                                              
        head = self.body[0]                                                                                                                                                              
        # Colisão com as paredes                                                                                                                                                         
        if not (0 <= head[0] < GRID_WIDTH and 0 <= head[1] < GRID_HEIGHT):                                                                                                               
            return True                                                                                                                                                                  
        # Colisão com o próprio corpo (verifica a cabeça contra o resto do corpo)                                                                                                        
        # É importante que a cabeça não seja comparada consigo mesma, daí o [1:]                                                                                                         
        if head in self.body[1:]:                                                                                                                                                        
            return True                                                                                                                                                                  
        return False                                                                                                                                                                     
                                                                                                                                                                                        
    def eat_food(self, food_pos):                                                                                                                                                        
        """                                                                                                                                                                              
        Verifica se a cabeça da cobra colidiu com a comida.                                                                                                                              
        Se sim, define a flag 'grow' como True e retorna True.                                                                                                                           
        """                                                                                                                                                                              
        if self.body[0] == food_pos:                                                                                                                                                     
            self.grow = True                                                                                                                                                             
            return True                                                                                                                                                                  
        return False                                                                                                                                                                     
                                                                                                                                                                                        
# --- Funções de Comida ---                                                                                                                                                              
def spawn_food(snake_body):                                                                                                                                                              
    """                                                                                                                                                                                  
    Gera uma nova posição aleatória para a comida que não esteja sobre o corpo da cobra.                                                                                                 
    Retorna as coordenadas (x, y) da nova comida ou None se não houver posições disponíveis.                                                                                             
    """                                                                                                                                                                                  
    # Lista de todas as posições possíveis no grid                                                                                                                                       
    all_possible_positions = set((x, y) for x in range(GRID_WIDTH) for y in range(GRID_HEIGHT))                                                                                          
                                                                                                                                                                                        
    # Converte o corpo da cobra para um conjunto para busca mais eficiente                                                                                                               
    occupied_positions = set(snake_body)                                                                                                                                                 
                                                                                                                                                                                        
    # Encontra posições disponíveis (todas - ocupadas)                                                                                                                                   
    available_positions = list(all_possible_positions - occupied_positions)                                                                                                              
                                                                                                                                                                                        
    if not available_positions:                                                                                                                                                          
        # Se não houver posições disponíveis (cobra preenche a tela),                                                                                                                    
        # o jogo pode ser considerado "ganho" ou travado.                                                                                                                                
        print("No available positions for food! Snake might have filled the screen (Game Won?).")                                                                                        
        return None                                                                                                                                                                      
                                                                                                                                                                                        
    return random.choice(available_positions)                                                                                                                                            
                                                                                                                                                                                        
                                                                                                                                                                                        
def draw_food(screen, food_pos):                                                                                                                                                         
    """Desenha a comida na tela."""                                                                                                                                                      
    # Apenas desenha se food_pos não for None (caso raro de não haver espaço para comida)                                                                                                
    if food_pos:                                                                                                                                                                         
        pygame.draw.rect(screen, RED, (food_pos[0] * GRID_SIZE, food_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE))                                                                          
        # Adiciona um contorno para a comida também para melhor visibilidade                                                                                                             
        pygame.draw.rect(screen, BLACK, (food_pos[0] * GRID_SIZE, food_pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE), 1)                                                                     
                                                                                                                                                                                        
                                                                                                                                                                                        
# --- Funções de Exibição do Jogo ---                                                                                                                                                    
def draw_score(screen, score, high_score):                                                                                                                                               
    """Desenha a pontuação atual e o recorde na tela."""                                                                                                                                 
    score_text = font.render(f"Pontos: {score}", True, WHITE)                                                                                                                            
    high_score_text = font.render(f"Recorde: {high_score}", True, WHITE)                                                                                                                 
    screen.blit(score_text, (5, 5))                                                                                                                                                      
    screen.blit(high_score_text, (WIDTH - high_score_text.get_width() - 5, 5))                                                                                                           
                                                                                                                                                                                        
def draw_game_over_screen(screen, score, high_score):                                                                                                                                    
    """Desenha a tela de 'Game Over' com pontuações e opção de reiniciar."""                                                                                                             
    screen.fill(BLACK)                                                                                                                                                                   
                                                                                                                                                                                        
    game_over_text = game_over_font.render("FIM DE JOGO!", True, RED)                                                                                                                    
    final_score_text = font.render(f"Sua Pontuação Final: {score}", True, WHITE)                                                                                                         
    high_score_text = font.render(f"Recorde: {high_score}", True, WHITE)                                                                                                                 
    restart_text = font.render("Pressione 'R' para Reiniciar ou 'Q' para Sair", True, GRAY)                                                                                              
                                                                                                                                                                                        
    # Centraliza os textos na tela                                                                                                                                                       
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))                                                                                       
    screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 20))                                                                                    
    screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 20))                                                                                      
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 70))                                                                                            
    pygame.display.flip()                                                                                                                                                                
                                                                                                                                                                                        
# --- Loop Principal do Jogo ---                                                                                                                                                         
def main_game_loop():                                                                                                                                                                    
    """                                                                                                                                                                                  
    Função principal que gerencia o estado do jogo, loop de eventos,                                                                                                                     
    atualizações e renderização.                                                                                                                                                         
    """                                                                                                                                                                                  
    current_high_score = load_high_score()                                                                                                                                               
                                                                                                                                                                                        
    snake = Snake()                                                                                                                                                                      
    food_pos = spawn_food(snake.body)                                                                                                                                                    
    score = 0                                                                                                                                                                            
    game_over = False                                                                                                                                                                    
    speed = INITIAL_GAME_SPEED  # Velocidade inicial da cobra (frames por segundo)                                                                                                       
                                                                                                                                                                                        
    running = True                                                                                                                                                                       
    while running:                                                                                                                                                                       
        for event in pygame.event.get():                                                                                                                                                 
            if event.type == pygame.QUIT:                                                                                                                                                
                running = False                                                                                                                                                          
            elif event.type == pygame.KEYDOWN:                                                                                                                                           
                if game_over:                                                                                                                                                            
                    # Permite reiniciar ou sair apenas quando o jogo acabou                                                                                                              
                    if event.key == pygame.K_r:                                                                                                                                          
                        # Reinicia o jogo                                                                                                                                                
                        snake = Snake()                                                                                                                                                  
                        food_pos = spawn_food(snake.body)                                                                                                                                
                        score = 0                                                                                                                                                        
                        game_over = False                                                                                                                                                
                        speed = INITIAL_GAME_SPEED  # Reseta a velocidade para o valor inicial                                                                                           
                    elif event.key == pygame.K_q:                                                                                                                                        
                        running = False # Sai do jogo                                                                                                                                    
                else:                                                                                                                                                                    
                    # Se o jogo está rodando, permite mudar a direção da cobra                                                                                                           
                    if event.key == pygame.K_UP:                                                                                                                                         
                        snake.change_direction(UP)                                                                                                                                       
                    elif event.key == pygame.K_DOWN:                                                                                                                                     
                        snake.change_direction(DOWN)                                                                                                                                     
                    elif event.key == pygame.K_LEFT:                                                                                                                                     
                        snake.change_direction(LEFT)                                                                                                                                     
                    elif event.key == pygame.K_RIGHT:                                                                                                                                    
                        snake.change_direction(RIGHT)                                                                                                                                    
                                                                                                                                                                                        
        if not game_over:                                                                                                                                                                
            snake.move()                                                                                                                                                                 
                                                                                                                                                                                        
            if snake.check_collision():                                                                                                                                                  
                game_over = True                                                                                                                                                         
                # Atualiza o recorde se a pontuação atual for maior                                                                                                                      
                if score > current_high_score:                                                                                                                                           
                    current_high_score = score                                                                                                                                           
                    save_high_score(current_high_score)                                                                                                                                  
                                                                                                                                                                                        
            # Só tenta comer comida se houver uma comida válida (food_pos não é None)                                                                                                    
            if food_pos and snake.eat_food(food_pos):                                                                                                                                    
                score += POINTS_PER_FOOD                                                                                                                                                 
                food_pos = spawn_food(snake.body) # Gera nova comida                                                                                                                     
                                                                                                                                                                                        
                # Se não houver mais espaço para comida (tela cheia), pode-se considerar o jogo "ganho"                                                                                  
                if food_pos is None:                                                                                                                                                     
                    game_over = True                                                                                                                                                     
                    print("You won! The snake has filled the screen.")                                                                                                                   
                                                                                                                                                                                        
                # Aumenta a velocidade gradualmente para aumentar a dificuldade                                                                                                          
                speed += SPEED_INCREMENT_PER_FOOD  # Cada comida torna o jogo um pouco mais rápido                                                                                       
                                                                                                                                                                                        
            # Desenha todos os elementos do jogo                                                                                                                                         
            screen.fill(BLACK)                                                                                                                                                           
            snake.draw(screen)                                                                                                                                                           
            draw_food(screen, food_pos) # Passa food_pos, que pode ser None em casos raros                                                                                               
            draw_score(screen, score, current_high_score)                                                                                                                                
        else:                                                                                                                                                                            
            # Se o jogo acabou, exibe a tela de Game Over                                                                                                                                
            draw_game_over_screen(screen, score, current_high_score)                                                                                                                     
                                                                                                                                                                                        
        pygame.display.flip()  # Atualiza a tela inteira                                                                                                                                 
        clock.tick(speed)      # Controla a taxa de quadros (velocidade do jogo)                                                                                                         
                                                                                                                                                                                        
    pygame.quit() # Encerra o Pygame ao sair do loop principal                                                                                                                           
                                                                                                                                                                                        
# --- Executa o Jogo ---                                                                                                                                                                 
if __name__ == "__main__":                                                                                                                                                               
    main_game_loop()                                                                                                                                                                     
