import pygame


class SoundEffects:
    def __init__(self):
        self.memorise_sound = pygame.mixer.Sound("./sounds/memorise.wav")

        self.left_btn_sound = pygame.mixer.Sound("./sounds/left_btn.wav")
        self.right_btn_sound = pygame.mixer.Sound("./sounds/right_btn.wav")

        self.fly_right_sound = pygame.mixer.Sound("./sounds/fly_right.wav")
        self.fly_left_sound = pygame.mixer.Sound("./sounds/fly_left.wav")
        self.fly_upwards_sound = pygame.mixer.Sound("./sounds/fly_upwards.wav")
        self.fly_downwards_sound = pygame.mixer.Sound("./sounds/fly_downwards.wav")
        self.fly_step_sounds = [self.fly_left_sound, self.fly_upwards_sound,
                                self.fly_right_sound, self.fly_downwards_sound]

        self.win_sound = pygame.mixer.Sound("./sounds/won.wav")
        self.lose_sound = pygame.mixer.Sound("./sounds/lose.wav")

    def play_step(self, character, direction):
        if character == "fly":
            pygame.mixer.Sound.play(self.fly_step_sounds[direction])
            # pygame.mixer.music.stop()

    def play_result(self, result):
        if result:
            pygame.mixer.Sound.play(self.win_sound)
        else:
            pygame.mixer.Sound.play(self.lose_sound)

    def play_memorise(self):
        pygame.mixer.Sound.play(self.memorise_sound)

    def play_left_btn(self):
        pygame.mixer.Sound.play(self.left_btn_sound)

    def play_right_btn(self):
        pygame.mixer.Sound.play(self.right_btn_sound)