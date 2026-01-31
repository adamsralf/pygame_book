from random import randint
from time import time
from typing import Any

import config as cfg
import pygame
from continent_polygons import continent_polygons


class MyEvents:                                 
    LANDED = pygame.USEREVENT + 1
    CRASHED = pygame.USEREVENT + 2



class Sky:
    def __init__(self, screen:pygame.surface.Surface, star_count: int=200) -> None:
        top = 0 
        left = 0
        width = cfg.WINDOW.width
        height = cfg.WINDOW.height - cfg.HORIZONT
        self.rect = pygame.rect.Rect(top, left, width, height)
        self.screen = screen
        self.stars = []         
        for _ in range(star_count):
            self.stars.append({"pos":(randint(2, self.rect.right-1), 
                                       randint(2, self.rect.right-1)),
                                "size":randint(1, 3),
                                "duration": randint(200, 600),
                                "counter":0,
                                "color":randint(10, 255)})
    
    def update(self) -> None:
        for star in self.stars:
            star["counter"] = (star["counter"] + 1) % (star["duration"] + 1) 
            if star["counter"] == 0:          
                star["color"] = (star["color"] + randint(0, 70)) % 256
                star["size"] = (star["size"] + 1) % 4

    def draw(self) -> None:
        pygame.draw.rect(self.screen, "black", self.rect)
        for star in self.stars:
            pygame.draw.circle(self.screen, (255,255,star["color"]), star["pos"], star["size"])

class Moon:
    def __init__(self, screen: pygame.surface.Surface, layer_count:int=5, peaks: int=35):
        self.screen = screen
        self.surface = pygame.surface.Surface((cfg.WINDOW.width, 
                                                cfg.HORIZONT + layer_count*30),
                                                pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.left = cfg.WINDOW.left
        self.rect.bottom = cfg.WINDOW.bottom
        landingarea = pygame.rect.Rect(0, self.rect.height - cfg.HORIZONT, 
                                     cfg.WINDOW.width, cfg.HORIZONT) 

        layers = []
        for layer_index in range(layer_count):
            mypeaks = randint(peaks//2, peaks)
            dist = landingarea.width // mypeaks
            mycolor = 180 - layer_index * 20  
            y = landingarea.top - 10 - randint(5, 10)*layer_index 
            x = landingarea.left               
            lofPeaks = [(x, landingarea.top)]  
            for i in range(mypeaks):           
                lofPeaks.append((x, y + randint(-5, 20))) 
                x += dist                      
            lofPeaks.append((landingarea.right, y)) 
            lofPeaks.append((landingarea.right, landingarea.top)) 

            poly = []                          
            for index in range(len(lofPeaks)-1):
                p1 = lofPeaks[index]
                p2 = lofPeaks[index+1]
                p3 = (lofPeaks[index+1][0], landingarea.top)
                p4 = (lofPeaks[index][0], landingarea.top)
                r = randint(-5,5)
                c =  [mc +  r for mc in (mycolor, mycolor, mycolor)]
                poly.append({"points":(p1, p2, p3, p4), "color":c})
            layers.append(poly)

        pygame.draw.rect(self.surface, (230, 230, 230), landingarea)
        for layer in reversed(layers):
            for poly in layer:
                pygame.draw.polygon(
                    self.surface,
                    poly["color"],
                    poly["points"])

    def draw(self):
        self.screen.blit(self.surface, self.rect.topleft)
 
class Earth:
    def __init__(self, screen:pygame.surface.Surface) -> None:
        self.radius = 80
        d = 2*self.radius
        self.surface = pygame.surface.Surface((d, d), pygame.SRCALPHA)
        self.rect = self.surface.get_rect()
        self.rect.left = cfg.WINDOW.right - 200
        self.rect.top = cfg.WINDOW.top + 50
        self.screen = screen

        for a in range(20, 1, -1):
            pygame.draw.circle(self.surface, 
                               (135, 206, 250, 210-a*10),    
                               (self.radius, self.radius), 
                               self.radius-20+a)             
        pygame.draw.circle(self.surface, 
                           (30, 144, 255), 
                           (self.radius, self.radius), 
                           self.radius-20)
        
        for continent in continent_polygons:
            poly = [(self.radius + (0.5*x), self.radius + (0.5*y)) for (x, y) in continent]
            pygame.draw.polygon(self.surface, (181, 150, 116), poly)


    def draw(self) -> None:
        self.screen.blit(self.surface, self.rect.topleft)

class Lander:
    def __init__(self, window: pygame.window.Window) -> None: 
        self.screen = window.get_surface()
        self.surface = pygame.surface.Surface((90,81), pygame.SRCALPHA)
        self.surface_thrusting = pygame.surface.Surface((90,81), pygame.SRCALPHA)
        self.rect = self.surface.get_frect()
        self.rect.centerx = cfg.WINDOW.centerx 
        self.rect.top = self.rect.height       
        self.create_lander()                   
        self.create_lander_thrusting()         
        self.mode = "landing"                  
        self.thrusting = False                 
        self.velocity = 0                      
        self.fuel_initial = cfg.LEVEL["fair"]  
        self.fuel = self.fuel_initial          
        self.fuel_consumption = 20             
        self.ai = False                             # AI flag
        self.create_status_window(window)

    def create_lander(self) -> None:
        # A few abbreviations
        cx = self.rect.width // 2
        cy = self.rect.height //2
        s = self.rect.width // 2
        sur = self.surface

        # Antenna
        pygame.draw.line(sur, (220, 220, 220), (cx, cy - s//2), (cx, cy - s//1.2), 2)
        pygame.draw.circle(sur, (255, 255, 255), (cx, cy - s//1.2), 3)

        # Upper crew module (narrower)
        pygame.draw.polygon(
            sur, (160, 160, 160),
            [(cx - s//4, cy - s//2),
             (cx - s//6, cy - s//3),
             (cx + s//6, cy - s//3),
             (cx + s//4, cy - s//2)]
        )

        # Connector between base and crew module
        conn_color = (160, 160, 160)
        pygame.draw.line(sur, conn_color, (cx - s//3, cy), (cx - s//6, cy - s//3), 2)
        pygame.draw.line(sur, conn_color, (cx, cy), (cx, cy - s//3), 2)
        pygame.draw.line(sur, conn_color, (cx + s//3, cy), (cx + s//6, cy - s//3), 2)

        # Module base (central capsule, light gray)
        pygame.draw.polygon(
            sur, (200, 200, 200),
            [(cx - s//3, cy),
             (cx - s//2, cy + s//2),
             (cx + s//2, cy + s//2),
             (cx + s//3, cy)]
        )

        # Windows in module
        r = 5
        window_color = (50, 50, 50)
        pygame.draw.circle(sur, window_color, (cx, cy+(s//4)), r)
        pygame.draw.circle(sur, window_color, (cx-(s//4), cy+(s//4)), r)
        pygame.draw.circle(sur, window_color, (cx+(s//4), cy+(s//4)), r)

        # Landing legs
        leg_color = (100, 100, 100)
        pygame.draw.line(sur, leg_color, (cx - s//2, cy + s//2), (cx - s, cy + s), 3)
        pygame.draw.line(sur, leg_color, (cx + s//2, cy + s//2), (cx + s, cy + s), 3)
        pygame.draw.line(sur, leg_color, (cx - s//4, cy + s//2), (cx - s//3, cy + s), 3)
        pygame.draw.line(sur, leg_color, (cx + s//4, cy + s//2), (cx + s//3, cy + s), 3)

        # Feet
        feet_color = (150, 150, 150)
        pygame.draw.circle(sur, feet_color, (cx - s + (r+2), cy + s - (r+2)), r-1)
        pygame.draw.circle(sur, feet_color, (cx + s - (r+2), cy + s - (r+2)), r-1)
        pygame.draw.circle(sur, feet_color, (cx - s//3 + (r-4), cy + s - (r+2)), r-1)
        pygame.draw.circle(sur, feet_color, (cx + s//3 - (r-4), cy + s - (r+2)), r-1)
      
    def create_lander_thrusting(self) -> None:
        # A few abbreviations
        cx = self.rect.width // 2
        cy = self.rect.height //2
        s = self.rect.width // 2
        sur = self.surface

        # Thruster exhaust
        self.surface_thrusting.blit(sur, (0,0))
        pygame.draw.polygon(self.surface_thrusting, (255, 140, 0), [
            (cx - 5, cy + s//2),
            (cx + 5, cy + s//2),
            (cx, cy + s//2 + 20)
        ])

    def create_status_window(self, window: pygame.window.Window) -> None:
        self.status_window = pygame.Window(size=(300, 140), title="Status")
        self.status_screen = self.status_window.get_surface()
        top = window.position[1]
        left = window.position[0] + cfg.WINDOW.width + 10
        self.status_window.position = (left, top)

    def update(self, *args: Any, **kwargs: Any) -> None:
        if "action" in kwargs.keys():
            if kwargs["action"] == "thrust":
                self.thrust(True)
            elif kwargs["action"] == "unthrust":
                self.thrust(False)
            elif kwargs["action"] == "toggle_ai":       # AI on/off§\label{moonlander0901}§
                self.ai = not self.ai
                if not self.ai:
                    self.thrust(False)
            elif kwargs["action"] == "move":
                if self.mode == "landing":
                    if self.ai > 0:                     # AI active?§\label{moonlander0902}§
                        self.controller()
                    self.move()
        if "mode" in kwargs.keys():                 
            self.mode = kwargs["mode"]
            if self.mode in ("landed", "crashed"):
                self.thrust(False)

    def controller(self):
        if self.mode in ("landed", "crashed"):          # Landing finished?§\label{moonlander0903}§
            self.thrust(False)
            return

        acc = -1 * (cfg.THRUST + cfg.GRAVITY)           # Net acceleration§\label{moonlander0904}§
        v_save = cfg.SAVE_SPEED_LANDING * 0.5           # 50% buffer
        if self.velocity <= v_save:                     # Already slow?§\label{moonlander0905}§
            self.thrust(False)
            return

        brake_distance = self.velocity ** 2 / (2 * acc)
        ground_distance = (cfg.WINDOW.height - 50) - self.rect.bottom
        self.thrust(ground_distance <= brake_distance)  # Required braking distance >= remaining height?§\label{moonlander0906}§
    
    def thrust(self, thrusting:bool) -> None:
            self.thrusting = thrusting and self.fuel > 0

    def draw(self) -> None:
        if self.thrusting:
            self.screen.blit(self.surface_thrusting, self.rect.topleft)
        else:
            self.screen.blit(self.surface, self.rect.topleft)
        self.draw_status()

    def draw_status(self) -> None:
        if self.ai:
            self.status_screen.fill("darkgrey")
        else:
            self.status_screen.fill("black")

        # Text output 
        h = -1*(self.rect.bottom - (cfg.WINDOW.bottom - cfg.HORIZONT))
        font = pygame.font.SysFont("Consolas", 14, bold=True)
        labels = "Maximal velocity (m/s):"
        labels += "\nVelocity (m/s):"
        labels += "\nHeight (m):"
        values = f"{cfg.SAVE_SPEED_LANDING/cfg.PIXELS_PER_METER:>7.2f}"
        values += f"\n{self.velocity/cfg.PIXELS_PER_METER:>7.2f}"
        values += f"\n{h/cfg.PIXELS_PER_METER:>7.2f}"
        text_labels = font.render(labels, True, "white")
        text_values = font.render(values, True, "white")
        if self.mode == "landed":
            text_mode = font.render(f"Status: {self.mode}", True, "green")
        elif self.mode == "crashed":
            text_mode = font.render(f"Status: {self.mode}", True, "red")
        else:
            text_mode = font.render(f"Status: {self.mode}", True, "white")
        text_mode_rect = text_mode.get_rect(top=120)
        text_mode_rect.left = self.status_screen.get_rect().centerx - text_mode_rect.centerx 
        self.status_screen.blit(text_labels, (5, 10))
        self.status_screen.blit(text_values, (230, 10))
        self.status_screen.blit(text_mode, text_mode_rect.topleft)

        # Bar display 
        if self.thrusting:
            pygame.draw.rect(self.status_screen, (255, 140, 0), (5, 90, 290, 20))
        pygame.draw.rect(self.status_screen, "grey", (5, 65, 290, 20))
        ratio = int(290 * self.fuel / self.fuel_initial)
        pygame.draw.rect(self.status_screen, "green", (5, 65, ratio, 20))
        self.status_window.flip()
        
    def move(self) -> None:
        if self.thrusting and self.fuel > 0:                     
            self.velocity += cfg.THRUST * cfg.DELTATIME
            self.fuel -= self.fuel_consumption * cfg.DELTATIME   
            if self.fuel < 0:
                self.thrusting = False
                self.fuel = 0
        self.velocity += cfg.GRAVITY * cfg.DELTATIME
        self.rect.top += self.velocity * cfg.DELTATIME
        if self.rect.bottom >= cfg.WINDOW.bottom - cfg.HORIZONT:
            self.rect.bottom = cfg.WINDOW.bottom -cfg.HORIZONT
            
    def get_velocity(self) -> float:
        return self.velocity

    def is_landed(self) -> bool:
        return self.rect.bottom >= cfg.WINDOW.bottom - cfg.HORIZONT

class Question:
    def __init__(self, screen:pygame.surface.Surface) -> None:
        self.font = pygame.font.Font(None, 24)
        self.screen = screen
        self.surface = self.font.render("(Q)uit or (R)estart?", True, "red")
        self.rect = self.surface.get_rect()
        self.rect.centerx = cfg.WINDOW.centerx
        self.rect.bottom = cfg.WINDOW.bottom - 10

    def draw(self) -> None:
        self.screen.blit(self.surface, self.rect.topleft)

class Game:
    def __init__(self) -> None:
        pygame.init()
        self.window = pygame.Window(size=cfg.WINDOW.size, title="MyMoonlander", position=pygame.WINDOWPOS_CENTERED)
        self.screen = self.window.get_surface()
        self.clock = pygame.time.Clock()
        self.landing = True

    def run(self) -> None:
        self.restart()
        time_previous = time()
        while self.running:
            self.watch_for_events()
            self.update()
            if self.running:
                self.draw()
            self.clock.tick(cfg.FPS)
            time_current = time()
            cfg.DELTATIME = time_current - time_previous
            time_previous = time_current
        pygame.quit()

    def watch_for_events(self) -> None:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.WINDOWCLOSE:  
                self.running = False
                event.window.destroy()
            elif event.type == MyEvents.LANDED:         
                self.landing = False
                self.lander.update(mode="landed", velocity=event.volocity)
            elif event.type == MyEvents.CRASHED:        
                self.landing = False
                self.lander.update(mode="crashed", velocity=event.volocity)
            elif event.type == pygame.KEYDOWN:
                if self.landing:                      
                    if event.key == pygame.K_SPACE:
                        self.lander.update(action="thrust")
                    elif event.key == pygame.K_h:
                        self.lander.update(action="toggle_ai")
                else:               
                    if event.key == pygame.K_q:         
                        self.running = False
                    elif event.key == pygame.K_r:       
                        self.restart()
                if event.key == pygame.K_ESCAPE:
                    self.running = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_SPACE:
                    self.lander.update(action="unthrust")

    def update(self) -> None:
        self.background.update()
        self.lander.update(action="move")          
        self.ckeck_landing()

    def draw(self) -> None:
        self.background.draw()                         
        self.moon.draw()
        self.earth.draw()
        self.lander.draw()
        if not self.landing:
            self.question.draw()
        self.window.flip()

    def restart(self) -> None:
        self.landing = True                            
        self.background = Sky(self.screen)
        self.moon = Moon(self.screen)
        self.earth = Earth(self.screen)
        self.lander = Lander(self.window)          
        self.question = Question(self.screen)
        self.running = True

    def ckeck_landing(self) -> None:
        velocity = self.lander.get_velocity()
        if self.lander.is_landed():
            velocity = self.lander.get_velocity()
            if velocity > cfg.SAVE_SPEED_LANDING:
                evt = pygame.event.Event(MyEvents.CRASHED, volocity=velocity)
                pygame.event.post(evt)
            else:
                evt = pygame.event.Event(MyEvents.LANDED, volocity=velocity)
                pygame.event.post(evt)


def main():
    Game().run()

if __name__ == "__main__":
    main()






