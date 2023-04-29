import pygame

pygame.init()
goomba_l=pygame.image.load("assets/enemy/goomba/goomba_l.gif")
goomba_r=pygame.image.load("assets/enemy/goomba/goomba_r.gif")
goomba_killed=pygame.image.load("assets/enemy/goomba/goomba_killed.gif")
goomba_killed_s=pygame.mixer.Sound("assets/sounds/smw_kick.wav")

class goomba(pygame.sprite.Sprite):
    def __init__(self,pos,group,col_sprites,player):
        super().__init__(group)
        self.group=group
        self.col_sprites=col_sprites
        self.player=player
        self.walk=[goomba_l,goomba_r]
        self.image=self.walk[0]
        self.rect=self.image.get_rect(topleft=pos)
        self.direction=pygame.math.Vector2(1,0)
        self.speed=1
        self.gravity=0.2
        self.ind=0
        self.got_killed=False
        self.got_smashed=False
        self.kill_time=0
        
        
    def apply_gravity(self):
        self.direction.y+=self.gravity   
        self.rect.y+=self.direction.y
    
    def horizontal_col(self):
        for i in self.col_sprites:
            if self.rect.colliderect(i.rect):
                if self.direction.x<0:
                    self.direction.x=1
                    self.rect.left=i.rect.right
                else:
                    self.direction.x=-1
                    self.rect.right=i.rect.left
                    
    def vertical_col(self):
        for i in self.col_sprites:
            if self.rect.colliderect(i.rect):
                if self.direction.y<0:
                    self.direction.y=0
                    self.rect.top=i.rect.bottom
                else:
                    self.direction.y=0
                    self.rect.bottom=i.rect.top
        
    
    def update(self):
        self.rect.x+=self.direction.x*self.speed
        if not self.got_smashed:
            self.image=self.walk[self.ind]
        self.ind+=1
        if self.ind>=len(self.walk):
            self.ind=0
         
        if not self.got_killed:   
            self.horizontal_col()
            
        self.apply_gravity()
        if not self.got_killed:
            self.vertical_col()
        
        if self.rect.y>800:
            self.player.score+=5
            self.kill()
        self.kill_time+=1
        
        if self.got_smashed and self.kill_time>=10:
            goomba_killed_s.play()
            self.player.score+=5
            self.kill()
        
        if self.player.rect.colliderect(self.rect) and not self.got_smashed:
            if self.rect.top+40>self.player.rect.bottom:
                self.player.direction.y=-5
                self.image=goomba_killed
                self.got_smashed=True
                self.direction.x=0
                self.kill_time=0
            else:
                if not self.got_killed and not self.got_smashed:
                    self.player.got_killed=True
                    
        
        for i in self.player.bullet_group:
            if self.rect.colliderect(i.rect) and not self.got_killed:
                i.kill()
                goomba_killed_s.play()
                self.direction.y=-5
                self.direction.x=0
                self.got_killed=True
                
                
                
        
        