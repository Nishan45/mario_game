#press f in key board to shoot fire balls, left and right key for going left and right, up key for jump, s key for start

import pygame,sys
import player
import levels
import enemy
import random

pygame.init()
SCREEN_WIDTH=1200
SCREEN_HEIGHT=800
font=pygame.font.Font(None,80)

Tile_size=80
clock=pygame.time.Clock()
tile_image=pygame.image.load("assets/objects/mario_tiles.jpg")
tile_piece=pygame.image.load("assets/objects/mario_tile_piece.png")
wall=pygame.image.load("assets/objects/mario_wall.jpg")
chest=pygame.image.load("assets/objects/mario_chest.jpg")
coins=pygame.image.load("assets/objects/gold.png")
pipe=pygame.image.load("assets/objects/pipe.png")
cloud=pygame.image.load("assets/objects/cloud.png")
flag=pygame.image.load("assets/objects/flag.png")
start=pygame.image.load("assets/objects/Start screen_1.png")

wall_busrsting_s=pygame.mixer.Sound("assets/sounds/smw_break_block.wav")
coin_s=pygame.mixer.Sound("assets/sounds/smw_coin.wav")
lost_s=pygame.mixer.Sound("assets/sounds/smw_lost_a_life.wav")
level_clear_s=pygame.mixer.Sound("assets/sounds/smw_course_clear.wav")


red=(255,0,0)
white=(255,255,255)
player_score=0
player_coins=0

screen=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))


def Text(text,color,pos):
    x=pos[0]-(len(text)/2)*30
    text=font.render(text,True,color)
    screen.blit(text,(x,pos[1]))


class Tile_piece(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image=tile_piece
        self.rect=self.image.get_rect(topleft=pos)
        self.direction=pygame.math.Vector2(0,0)
        self.speed=1
        self.gravity=0.2
        self.ind=0
        self.direction.y=-4
        self.col_sprites=groups
    
    def horizontal_col(self):
        for j in self.col_sprites:
            for i in j:
                if i is not self and i.rect.colliderect(self.rect):
                    if self.direction.x>0:
                        self.rect.right=i.rect.left
                        self.direction.x=-1
                    elif self.direction.x<0:
                        self.direction.x=1
                        self.rect.left=i.rect.right
    
    def vertical_col(self):
        for j in self.col_sprites:
            for i in j:
                if i is not self and i.rect.colliderect(self.rect):
                    if self.direction.y>0:
                        self.direction.y=0
                        self.rect.bottom=i.rect.top
                          
                    if self.direction.y<0 :
                        self.direction.y=0
                        self.rect.top=i.rect.bottom      
                  
    def apply_gravity(self):
        self.direction.y+=self.gravity   
        self.rect.y+=self.direction.y
    
    def update(self):
        self.rect.x+=self.direction.x*self.speed
        self.ind+=1
        self.horizontal_col()
        self.apply_gravity()
        self.vertical_col()
        if self.ind>100:
            self.kill()   
    

class Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups,img):
        super().__init__(groups)
        self.image=img
        self.rect=self.image.get_rect(topleft=pos)
        self.col=False
        self.group=groups
        self.tile=True
       
    
    def update(self):
        if self.col:
            wall_busrsting_s.play()
            Tile_piece(self.rect.topleft,self.group).direction.x=-1
            Tile_piece([self.rect.x+40,self.rect.y],self.group).direction.x=1
            T=Tile_piece([self.rect.x,self.rect.y+40],self.group)
            T.direction.x=-1
            T.direction.y=-3
            T=Tile_piece([self.rect.x+40,self.rect.y+40],self.group)
            T.direction.x=1
            T.direction.y=-3
            self.kill()
            
        
class E_Tile(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image=pygame.Surface((Tile_size,Tile_size))
        self.rect=self.image.get_rect(topleft=pos)

class Pipe(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image=pipe
        self.rect=self.image.get_rect(topleft=pos)

class Cloud(pygame.sprite.Sprite):
    def __init__(self,pos,groups):
        super().__init__(groups)
        self.image=cloud
        self.rect=self.image.get_rect(topleft=pos)

class Flag(pygame.sprite.Sprite):
    def __init__(self,pos,groups,player):
        super().__init__(groups)
        self.image=flag
        self.rect=self.image.get_rect(bottomleft=pos)
        self.player=player
    def update(self):
        global win_game,start_game,ind
        if self.rect.colliderect(self.player.rect):
            win_game=True
            start_game=False
            ind+=1
            level_clear_s.play()
            

class Coins(pygame.sprite.Sprite):
    def __init__(self,pos,groups,player):
        super().__init__(groups)
        self.image=coins
        self.player=player
        self.rect=self.image.get_rect(center=pos)
        self.speed=3
        self.ind=self.rect.y
        self.d=0
    
    def update(self):
        if self.rect.colliderect(self.player.rect):
            if self.rect.y==self.ind:
                coin_s.play()
                self.player.coins_count+=1
            self.d=1
        self.rect.y-=self.speed*self.d
        if self.rect.y<self.ind-150:
            self.kill()
        
    
class Chest(pygame.sprite.Sprite):
    def __init__(self,pos,groups,player,ind):
        super().__init__([groups,player.col_sprites])
        self.image=chest
        self.player=player
        self.v_sprites=groups
        self.group=groups
        self.group.append(self.player.col_sprites)
        self.rect=self.image.get_rect(topleft=pos)
        self.col=False
        self.ind=ind
        if self.ind=='b':
            self.n=random.randint(1,6)
        else:
            self.n=1
            
    def update(self):
        if self.col and self.player.direction.y>0 and self.n>0:
            self.col=False
            self.n-=1
            if self.player.p==2:
                self.ind='b'
            if self.ind=='b':
                Coins(self.rect.center,self.v_sprites,self.player).d=1
                coin_s.play()
                self.player.coins_count+=1
            else:
                if self.player.p==0:
                    player.food(self.rect.topleft,self.v_sprites,self.player)
                elif self.player.p==1:
                    player.Flower(self.rect.topleft,self.v_sprites,self.player)
            if self.n>0:
                Chest(self.rect.topleft,self.v_sprites,self.player,self.ind).n=self.n
            self.kill()
            
        if self.n==0:
            Tile(self.rect.topleft,self.group,tile_image)
            self.kill()
            

class level(pygame.sprite.Sprite):
    def __init__(self,map):
        super().__init__()
        self.display_surface=pygame.display.get_surface()
        self.map=map
        self.v_sprites=camera()
        self.a_sprites=pygame.sprite.Group()
        self.e_sprites=pygame.sprite.Group()
        self.col_sprites=pygame.sprite.Group()
        self.set_up()
        
    def set_up(self):
        for i,v in enumerate(self.map):
            for j,h in enumerate(v):
                x=Tile_size*j
                y=Tile_size*i  
                if h=='1':
                    Cloud((x,y),[self.v_sprites])
                
                      
        for i,v in enumerate(self.map):
            for j,h in enumerate(v):
                x=Tile_size*j
                y=Tile_size*i
                if h=='x':
                    Tile((x,y),[self.v_sprites,self.col_sprites,self.e_sprites,self.a_sprites],tile_image)
                if h=='w':
                    Tile((x,y),[self.v_sprites,self.col_sprites,self.e_sprites],wall)
                if h=='e':
                    E_Tile((x,y),[self.e_sprites])
                if h=='P':
                    self.player=player.Player((x,y),[self.v_sprites,self.a_sprites],self.col_sprites)
                if h=='p':
                    Pipe((x,y),[self.v_sprites,self.col_sprites,self.e_sprites])
        
        for i,v in enumerate(self.map):
            for j,h in enumerate(v):
                x=Tile_size*j
                y=Tile_size*i  
                if h=='c':
                    Coins((x+(Tile_size/2),y+(Tile_size/2)),[self.v_sprites,self.a_sprites],self.player)  
                if h=='g':
                    enemy.goomba((x,y),[self.v_sprites,self.a_sprites],self.e_sprites,self.player)
                if h=='b':
                    Chest((x,y),[self.v_sprites,self.a_sprites],self.player,'b')
                if h=='m':
                    Chest((x,y),[self.v_sprites,self.a_sprites],self.player,'m')
                if h=='f':
                    Flag((x+30,y+80),[self.v_sprites,self.a_sprites],self.player)
                  
                    
    def run(self):
        global start_game,Lose_game,win_game,player_score,player_coins
        
        player_coins=self.player.coins_count
        player_score=self.player.score
    
        self.a_sprites.update()
        self.v_sprites.draw(self.player)
        if self.player.got_killed and not self.player.change:
            if self.player.p==0:
                lost_s.play()
                Lose_game=True
                start_game=False
            else:
                self.player.p-=1
                self.player.change=True
                player.power_down_s.play()
            

class camera(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface=pygame.display.get_surface()
        self.offset=pygame.math.Vector2(0,0)
        self.rect=pygame.Rect(400,200,SCREEN_WIDTH-800,SCREEN_HEIGHT-400)
        
        
    def draw(self,player):
        
        if player.rect.left<self.rect.left:
            self.rect.left=player.rect.left
        if player.rect.right>self.rect.right:
            self.rect.right=player.rect.right
        if player.rect.top<self.rect.top:
            self.rect.top=player.rect.top
        if player.rect.bottom>self.rect.bottom:
            self.rect.bottom=player.rect.bottom
            
        self.offset=pygame.math.Vector2(self.rect.left-400,0)
        
        for sprite in self.sprites():
            offset_pos=sprite.rect.topleft-self.offset
            if offset_pos.x>=-200 and offset_pos.x<=SCREEN_WIDTH:
                self.display_surface.blit(sprite.image,offset_pos)
        Text("score "+"x"+str(player.score),(0,0,0),(150,10))  
        Text("coins "+"x"+str(player.coins_count),(0,0,0),(550,10))  
        Text("level "+"x"+str(ind+1),(0,0,0),(950,10))  
        
Level=level(levels.map[0])
display_group=pygame.sprite.Group()


start_game=False
win_game=False
Lose_game=False
ind=0

def starting_screen():
    global start_game,win_game,Lose_game,Level,ind,player_coins,player_score
    
    screen.blit(start,(360,100))
    text1="WELCOME TO LEVEL "+str(ind+1)
    text2="PRESS 'S' TO START THE GAME"
    text_s=""
    text_c=""
    if win_game:
        text1="YOU WON LEVEL "+str(ind)
        text2="PRESS 'S' TO GO NEXT LEVEL"
        text_s="score x"+str(player_score)
        text_c="coins x"+str(player_coins)
        if ind>=len(levels.map):
            text1="YOU WON THE GAME"
            text2="PRESS 'S' TO GO TO LEVEL 1"
            
    elif Lose_game:
        text1="YOU LOSE"
        text2="PRESS 'S' TO RESTART THE GAME"
        text_s="score x"+str(player_score)
        text_c="coins x"+str(player_coins)
        
     
    Text(text1,red,(SCREEN_WIDTH/2,SCREEN_HEIGHT/2))
    Text(text2,(0,0,0),(SCREEN_WIDTH/2,SCREEN_HEIGHT/2+100))
    Text(text_s,(0,0,0),(SCREEN_WIDTH/2,SCREEN_HEIGHT/2+200))
    Text(text_c,(0,0,0),(SCREEN_WIDTH/2,SCREEN_HEIGHT/2+250))
    
    screen.blit(player.player_r,(SCREEN_WIDTH/2+200,SCREEN_HEIGHT/2+200))
    screen.blit(player.player_l,(SCREEN_WIDTH/2-200,SCREEN_HEIGHT/2+200))
    
    key=pygame.key.get_pressed()
    if key[pygame.K_s]:
        lost_s.stop()
        level_clear_s.stop()
        start_game=True
        win_game=False
        Lose_game=False
        if ind>=len(levels.map):
            ind=0
        p=0 
        try:
            p=Level.player.p
        except:
            pass
        Level=level(levels.map[ind])
        if ind>0:
            Level.player.p=p
        Level.player.change=True
        player_score=0
        player_coins=0
        

while True:
    screen.fill((0,150,255))
    if not start_game:
        starting_screen()
    if start_game:
        Level.run()
        
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        
    clock.tick(201)
    pygame.display.update()
