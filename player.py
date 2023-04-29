import pygame
pygame.init()

red=(255,0,0)

tile_image=pygame.image.load("assets/objects/mario_tiles.jpg")

player_l=pygame.image.load("assets/player/small_mario2.gif")
player_r=pygame.image.load("assets/player/small_mario.gif")
player_rr1=pygame.image.load("assets/player/small_mario_r3.gif")
player_rr2=pygame.image.load("assets/player/small_mario_r2.gif")
player_rr3=pygame.image.load("assets/player/small_mario_r1.gif")
player_lr1=pygame.image.load("assets/player/small_mario_l3.gif")
player_lr2=pygame.image.load("assets/player/small_mario_l2.gif")
player_lr3=pygame.image.load("assets/player/small_mario_l1.gif")
player_lj=pygame.image.load("assets/player/small_mario_lj.gif")
player_rj=pygame.image.load("assets/player/small_mario_rj.gif")

player1_l=pygame.image.load("assets/player/mario.gif")
player1_r=pygame.image.load("assets/player/mario2.gif")
player1_rr1=pygame.image.load("assets/player/mario_rr1.gif")
player1_rr2=pygame.image.load("assets/player/mario_rr2.gif")
player1_rr3=pygame.image.load("assets/player/mario_rr3.gif")
player1_lr1=pygame.image.load("assets/player/mario_lr1.gif")
player1_lr2=pygame.image.load("assets/player/mario_lr2.gif")
player1_lr3=pygame.image.load("assets/player/mario_lr3.gif")
player1_lj=pygame.image.load("assets/player/mario_lj.gif")
player1_rj=pygame.image.load("assets/player/mario_rj.gif")

player2_l=pygame.image.load("assets/player/fire_mario.gif")
player2_r=pygame.image.load("assets/player/fire_mario2.gif")
player2_rr1=pygame.image.load("assets/player/fire_mario_rr1.gif")
player2_rr2=pygame.image.load("assets/player/fire_mario_rr2.gif")
player2_rr3=pygame.image.load("assets/player/fire_mario_rr3.gif")
player2_lr1=pygame.image.load("assets/player/fire_mario_lr1.gif")
player2_lr2=pygame.image.load("assets/player/fire_mario_lr2.gif")
player2_lr3=pygame.image.load("assets/player/fire_mario_lr3.gif")
player2_lj=pygame.image.load("assets/player/fire_mario_lj.gif")
player2_rj=pygame.image.load("assets/player/fire_mario_rj.gif")

player_p=[[player_l,player_r],[player1_l,player1_r],[player2_l,player2_r]]
player_run_l=[[player_lr1,player_lr2,player_lr3],[player1_lr1,player1_lr2,player1_lr3],[player2_lr1,player2_lr2,player2_lr3]]
player_run_r=[[player_rr1,player_rr2,player_rr3],[player1_rr1,player1_rr2,player1_rr3],[player2_rr1,player2_rr2,player2_rr3]]
player_jump=[[player_lj,player_rj],[player1_lj,player1_rj],[player2_lj,player2_rj]]


fire_balls_r=pygame.image.load("assets/objects/fireballs.png")
fire_balls_l=pygame.image.load("assets/objects/fireballs_l.png")

fire_ball_s=pygame.mixer.Sound("assets/sounds/smw_fireball.wav")
jump_s=pygame.mixer.Sound("assets/sounds/smw_jump.wav")
power_up_s=pygame.mixer.Sound("assets/sounds/smw_power-up.wav")
power_down_s=pygame.mixer.Sound("assets/sounds/smb_bump.wav")

mashroom=pygame.image.load("assets/objects/mashroom.png")
flower=pygame.image.load("assets/objects/flower.png")



class bullet(pygame.sprite.Sprite):
    def __init__(self,pos,groups,col_sprites):
        super().__init__(groups)
        self.image=fire_balls_r
        self.rect=self.image.get_rect(center=pos)
        self.direction=pygame.math.Vector2(0,0)
        self.col_sprites=col_sprites
        self.speed=4
        self.gravity=0.2
    
    def horizontal_col(self):
        for i in self.col_sprites:
            if i.rect.colliderect(self.rect):
                if self.direction.x>0 and self.rect.x<i.rect.x+15:
                    self.kill()  
                elif self.direction.x<0 and self.rect.x>i.rect.x-15:
                    self.kill()
        
    def vertical_col(self):
        for i in self.col_sprites:
            if i.rect.colliderect(self.rect):
                if self.direction.y>0:
                    self.direction.y=-4
                    self.rect.bottom=i.rect.top
                    
                    
    def apply_gravity(self):
        self.direction.y+=self.gravity   
        self.rect.y+=self.direction.y
        
    def update(self):
        if self.direction.x>0:
            self.image=fire_balls_r
        if self.direction.x<0:
            self.image=fire_balls_l
            
        self.rect.x+=self.direction.x*self.speed
        self.horizontal_col()
        self.apply_gravity()
        self.vertical_col()
        if self.rect.y>1000:
            self.kill()
        

class Player(pygame.sprite.Sprite):
    def __init__(self,pos,groups,col_sprites):
        super().__init__(groups)
        self.group=groups
        self.pos=pos
        self.col_sprites=col_sprites
        self.direction=pygame.math.Vector2()
        self.p=0
        self.cur=player_p[self.p][1]
        self.cur_j=player_jump[self.p][1]
        self.image=self.cur
        self.run_l=player_run_l[self.p]
        self.run_r=player_run_r[self.p]
        self.ind=0
        self.rect=self.image.get_rect(topleft=pos)
        self.speed=2
        self.jump_speed=-6
        self.gravity=0.2
        self.jump_count=0
        self.fire=-1
        self.face=1
        self.bullet_group=pygame.sprite.Group()
        self.got_killed=False
        self.score=0
        self.coins_count=0
        self.change=False
        self.time=0
        
    def horizontal_col(self):
        for i in self.col_sprites:
            g=0.2
            try:
                g=i.gravity
            except:
                pass
            if i.rect.colliderect(self.rect) and g!=0.1:
                if self.direction.x>0:
                    self.rect.right=i.rect.left

                elif self.direction.x<0:
                    self.rect.left=i.rect.right
                
                self.ind=0
                self.image=self.cur
                    
    
    def vertical_col(self):
        
        for i in self.col_sprites:
            g=0.2
            try:
                g=i.gravity
            except:
                pass
            if i.rect.colliderect(self.rect) and g!=0.1:
                if self.direction.y>0:
                    self.direction.y=0
                    self.jump_count=0
                    self.rect.bottom=i.rect.top
                    
                    
                if self.direction.y<0 :
                    try:
                        if self.p>0 or i.ind=='b' or i.ind=='m':
                            i.col=True
                            
                            if i.tile:
                                self.score+=2
                    except:
                        pass
                    
                    self.direction.y=0
                    self.jump_count=50
                    self.rect.top=i.rect.bottom
           
     
    def apply_gravity(self):
        self.direction.y+=self.gravity   
        self.rect.y+=self.direction.y
    
    def switches(self):
        keys=pygame.key.get_pressed()
        
        if keys[pygame.K_RIGHT]:
            self.direction.x=1
            self.face=1
            
        elif keys[pygame.K_LEFT]:
            self.direction.x=-1
            self.face=-1
            
        else:
            self.direction.x=0
            self.ind=0
        
        if keys[pygame.K_UP] and self.jump_count<=40:
            self.direction.y=self.jump_speed
            self.jump_count+=1
            self.image=self.cur_j
            
        
        if keys[pygame.K_f] and self.p>1:
            self.fire+=1
            if self.face==1:
                self.image=player_run_r[self.p][0]
            else:
                self.image=player_run_l[self.p][0]
        else:
            self.fire=-1
            
            
            
    def update(self):
        
        self.switches()
        if self.fire%40==0:
            fire_ball_s.play()
            bullets=bullet(self.rect.center,self.group,self.col_sprites)
            bullets.direction.x=self.face
            self.bullet_group.add(bullets)
            
            
        if self.direction.x<0:
            
            self.image=self.run_l[self.ind]
            self.ind+=1
            self.cur=player_p[self.p][0]
            self.cur_j=player_jump[self.p][0]
            
        if self.direction.x>0:
            self.cur=player_p[self.p][1]
            self.cur_j=player_jump[self.p][1]
            self.image=self.run_r[self.ind]
            self.ind+=1
            
        if self.ind>=len(self.run_l):
            self.ind=0 
        if self.direction.x==0 and self.direction.y==0:
            if self.face==1:
                self.cur=player_p[self.p][1]
            else:
                self.cur=player_p[self.p][0]
            self.image=self.cur
        
            
        self.rect.x+=self.direction.x*self.speed
        self.horizontal_col()
        self.apply_gravity()
        self.vertical_col()
        
        if self.direction.y<0:
            self.image=self.cur_j
        
        if self.rect.y>=800:
            self.got_killed=True
            self.p=0
        self.run_l=player_run_l[self.p]
        self.run_r=player_run_r[self.p]
        
        if self.change:
            self.time+=1
            self.rect=self.image.get_rect(bottomleft=self.rect.bottomleft)
            self.direction.x=0
        
        if self.time>200:
            self.time=0
            self.got_killed=False
            self.change=False
    

class food(pygame.sprite.Sprite):
    def __init__(self,pos,groups,player):
        super().__init__(groups)
        self.image=mashroom
        self.col_sprites=player.col_sprites
        self.player=player
        self.rect=self.image.get_rect(topleft=pos)
        self.direction=pygame.math.Vector2(0,0)
        self.ind=self.rect.y
        self.speed=1
        self.gravity=0.1
        
    def apply_gravity(self):
        self.direction.y+=self.gravity   
        self.rect.y+=self.direction.y
    
    def horizontal_col(self):
        for i in self.col_sprites:
            if i is not self and i.rect.colliderect(self.rect):
                if self.direction.x>0:
                    self.direction.x=-1
                    self.rect.right=i.rect.left
                elif self.direction.x<0:
                    self.direction.x=1
                    self.rect.left=i.rect.right
                    
    def vertical_col(self):
        for i in self.col_sprites:
            if i is not self and i.rect.colliderect(self.rect):
                if self.direction.y>0:
                    self.direction.y=0
                    self.rect.bottom=i.rect.top
   
    def update(self):
        self.rect.x+=self.direction.x*self.speed
        if self.player.rect.colliderect(self.rect):
            power_up_s.play()
            self.player.p=1
            self.player.change=True
            self.kill()
        if self.rect.y>=self.ind-80:
            self.rect.y-=1
        else:
            self.ind=10000
            if self.direction.x==0:
                self.direction.x=1
            self.horizontal_col()
            self.apply_gravity()
            self.vertical_col()
            
        if self.rect.y>800:
            self.kill()
        
class Flower(pygame.sprite.Sprite):
    def __init__(self,pos,groups,player):
        super().__init__(groups)
        self.image=flower
        self.player=player
        self.rect=self.image.get_rect(topleft=pos)
        self.ind=self.rect.y
        self.speed=1
        self.gravity=0.1
    
    def update(self):
        if self.rect.y>=self.ind-80:
            self.rect.y-=1 
        else:
            self.ind=10000      
            
        if self.rect.colliderect(self.player.rect):
            power_up_s.play()
            self.player.p=2
            self.player.change=True
            self.kill()
        
        
             
    