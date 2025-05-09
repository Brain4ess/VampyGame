import configparser as cfgp
from random import choice

import pygame as pg
from pygame.locals import *

import data.Constants as const
from classes.classBackground import BG
from classes.classCamera import Camera
from classes.classCharacter import Character
from classes.classTimer import Timer
from classes.EnemyHandler import EnemyHandler
from data.Abilities import ABILITIES, PASSIVES
from UI.classGameScreen import GameScreen
from UI.GameUI import UI

cfg = cfgp.ConfigParser()
cfg.read('data/config.ini')

class Game:
    def __init__(self, screen: GameScreen, mapImage: str, character: str, initui):
        self.mapImage = mapImage
        self.spriteGroup = pg.sprite.Group()
        self.enemyGroup = pg.sprite.Group()
        self.fps = const.FPS
        self.screen = screen
        self.bg = BG(self.mapImage, self.screen, spawnpoint=(500, 500))
        self.run = True
        self.timer = Timer(self.screen, const.PATHS["Fonts"]["Timer"], 'White', 30)
        self.camera = Camera(self.screen, self.bg.width, self.bg.height, self.bg)
        self.player = Character(self.bg, character, self.screen, 5, self.spriteGroup, self.enemyGroup, self.timer)
        self.__prev_Plevel = self.player.lvl
        self.clock = pg.time.Clock()
        self.timer.start()
        self.EnemyHandler = EnemyHandler(self.screen, self.camera, self.player, self.timer, self.spriteGroup, self.enemyGroup)
        self.ui = UI(self.screen, self.player, initui)
        self.ui.resume.at_unclick = self.togglePause
        self.paused = False
        self.chosen = True
        self.__escprev = 0

    def eventGame(self):
        for event in pg.event.get():
            if event.type == QUIT:
                self.run = False
        keys = pg.key.get_pressed()
        if keys[K_ESCAPE] and keys[K_ESCAPE] != self.__escprev:
            self.togglePause()
        self.__escprev = keys[K_ESCAPE]

    def togglePause(self, button = None):
        if button != None:
            button.state = "unclicked"
        if self.paused and self.chosen and self.player.hp > 0:
            self.paused = False
            pg.mixer.music.unpause()
            self.timer.pause(self.paused)
        elif not self.paused and self.chosen and self.player.hp > 0:
            self.paused = True
            self.ui.resume.set_text("Resume")
            pg.mixer.music.pause()
            self.timer.pause(self.paused)

    def runGame(self):
        pg.mixer.music.load(const.PATHS["Music"]["Game"])
        pg.mixer.music.set_volume(cfg.getint('Settings', 'musicvolume') / 100)
        pg.mixer.music.play(-1)
        while self.run:
            self.eventGame()
            if not self.run:
                return "QUIT"
            self.bg.blitBG(self.camera.getoffset())
            self.EnemyHandler.update()
            self.player.update(self.camera.getoffset())

            # Death mechanic
            deathScreen = self.deathScreenLoop()
            if deathScreen != True:
                return deathScreen

            levelUpLoop = self.levelUpLoop()
            if levelUpLoop != True:
                return levelUpLoop
            

            self.ui.update()
            self.camera.update(self.player)
            self.timer.update()

            pg.display.update()
            self.clock.tick(self.fps)

            while self.paused:
                pauseLoop = self.pauseLoop()
                if pauseLoop != True:
                    return pauseLoop

    def make_upgrades(self):
        upg_abilities = []
        for ability in self.player.abilities:
            if ability.level < ability.max_level and not 'mirrored' in ability.name:
                upg_abilities.append(ability.name)

        if len(self.player.abilities) < 5:
            all_abilities = list(ABILITIES.keys()).copy()
            for ability in self.player.abilities:
                if not 'mirrored' in ability.name:
                    all_abilities.remove(ability.name)
            abilities_random = []
            for i in range(3):
                if len(all_abilities) > 0:
                    temp = choice(all_abilities)
                    all_abilities.remove(temp)
                    abilities_random.append(temp)
            abilities_final = upg_abilities + abilities_random
        else:
            abilities_final = upg_abilities
        
        upg_passives = []
        for passive in self.player.passives:
            if passive.level < passive.max_level:
                upg_passives.append(passive.name)
        
        if len(self.player.passives) < 5:
            all_passives = list(PASSIVES.keys()).copy()
            for passive in self.player.passives:
                all_passives.remove(passive.name)
            passives_random = []
            for i in range(3):
                if len(all_passives) > 0:
                    temp = choice(all_passives)
                    all_passives.remove(temp)
                    passives_random.append(temp)
            passives_final = upg_passives + passives_random
        else:
            passives_final = upg_passives

        final_choices = abilities_final + passives_final
        self.abilities_final = []
        for i in range(3):
            if len(final_choices) > 0:
                temp = choice(final_choices)
                final_choices.remove(temp)
                self.abilities_final.append(temp)

        if len(self.abilities_final) > 0:
            for i in range(len(self.abilities_final)):
                self.ui.UpgButtons.children[i].set_invisible(False, True)
                if self.abilities_final[i] in list(ABILITIES.keys()):
                    self.ui.UpgButtons.children[i].children[1].set_text(ABILITIES[self.abilities_final[i]]['display_name'])
                    self.ui.UpgButtons.children[i].children[0].img = pg.transform.scale(pg.image.load(ABILITIES[self.abilities_final[i]]['icon']), (64, 64))
                else:
                    self.ui.UpgButtons.children[i].children[1].set_text(PASSIVES[self.abilities_final[i]]['display_name'])
                    self.ui.UpgButtons.children[i].children[0].img = pg.transform.scale(pg.image.load(PASSIVES[self.abilities_final[i]]['icon']), (64, 64))
                
                self.ui.UpgButtons.children[i].children[1].refresh_surfaces_build()   
                self.ui.UpgButtons.children[i].children[0].refresh_surfaces_build()
                self.ui.UpgButtons.children[i].refresh_surfaces_build()
                
            if len(self.abilities_final) < len(self.ui.UpgButtons.children):
                for i in range(len(self.abilities_final), len(self.ui.UpgButtons.children)):
                    self.ui.UpgButtons.children[i].set_invisible(True, True)

    def pauseLoop(self):
        self.eventGame()
        self.ui.update_Pause()
        if self.ui.exit_to_menu.state == "unclicked":
            self.ui.resume.at_unclick = None
            self.attempt_suicide()
            return "ToMenu"
        if self.ui.quit.state == "unclicked":
            return "QUIT"
        if not self.run:
            return "QUIT"
        pg.display.update()
        self.clock.tick(self.fps)
        return True

    def deathScreenLoop(self):
        if self.player.hp <= 0:
                self.ui.resume.set_text(f'Revive (left: {self.player.lives})')
                self.timer.pause(True)
                while True:
                    self.eventGame()
                    self.ui.update_Pause()
                    if self.ui.resume.state == "unclicked":
                        if self.player.lives > 0:
                            self.player.hp = self.player.maxhp
                            self.player.lives -= 1
                            self.timer.pause(False)
                            break
                    if self.ui.exit_to_menu.state == "unclicked":
                        self.ui.resume.at_unclick = None
                        self.attempt_suicide()
                        return "ToMenu"
                    if self.ui.quit.state == "unclicked":
                        return "QUIT"
                    if not self.run:
                        return "QUIT"
                    pg.display.update()
                    self.clock.tick(self.fps)
        return True

    def levelUpLoop(self):
        if self.player.lvl > self.__prev_Plevel:
            self.__prev_Plevel = self.player.lvl
            self.make_upgrades()
            if len(self.abilities_final) > 0:
                self.chosen = False
                self.timer.pause(not self.chosen)
                while not self.chosen:
                    self.eventGame()
                    self.ui.update_Upgrade()
                    for i in range(len(self.ui.UpgButtons.children)):
                        if self.ui.UpgButtons.children[i].state == "unclicked":
                            if '[•]' in self.ui.UpgButtons.children[i].children[1].text:
                                if self.player.get_passive(self.abilities_final[i]) != None:
                                    self.player.get_passive(self.abilities_final[i]).onlevelup()
                                else:
                                    self.player.add_passive(self.abilities_final[i])
                                    if len(self.player.passives) > 1:
                                        for i in range(len(self.player.passives) - 1):
                                            self.player.passives[i].onPassiveAdd(self.player.passives[-1])
                            else:
                                if self.player.get_ability(self.abilities_final[i]) != None:
                                    self.player.get_ability(self.abilities_final[i]).level += 1
                                else:
                                    self.player.add_ability(self.abilities_final[i])
                                    if len(self.player.passives) > 0:
                                        for i in range(len(self.player.passives)):
                                            self.player.passives[i].onAbilityAdd(self.player.abilities[-1])
                            self.chosen = True
                            self.timer.pause(not self.chosen)
                            break
                    if not self.run:
                        return "QUIT"
                    pg.display.update()
                    self.clock.tick(self.fps)
        return True
    def attempt_suicide(self):
        del self.bg.bg
        del self.bg.mapImage
        self.ui.resume.at_unclick = None
        self.ui.exit_to_menu.at_unclick = None
        self.ui.quit.at_unclick = None
        self.spriteGroup.empty()
        self.enemyGroup.empty()

    def __del__(self):
        del self.camera.bg
        del self.player.bg
        del self.player.timer
        del self.EnemyHandler.timer
        for i in self.player.abilities:
            del i.timer
            del i.player
        del self.EnemyHandler.camera
        del self.bg
        del self.mapImage
        del self.player
        del self.timer
        del self.camera
        del self.EnemyHandler
        del self.ui.lvlBar
        del self.ui.healthBar
        del self.ui.healthBarUpdater
        del self.ui.lvlBarUpdater
        del self.ui.resume
        del self.ui.exit_to_menu
        del self.ui.quit
        del self.ui
