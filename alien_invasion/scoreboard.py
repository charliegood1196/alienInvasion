import pygame.font

class Scoreboard():
    """A class to report scoring information"""
    
    def __init__(self,main_settings, screen, stats):
        """Initialize scorekeeping attributes."""
        self.screen = screen
        self.main_settings = main_settings
        self.screen_rect = screen.get_rect()
        self.stats = stats
        
        # Font settings for score information
        self.text_color = (30,30,30)
        font_path = "fonts/player-1-up-font/Player1UpHeavy-BwKl.ttf"
        self.font = pygame.font.Font(font_path, 48)
        
        # Prepare the initial score images
        self.prep_score()
        self.prep_high_score()
        
        
    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = int(round(self.stats.score, -1))
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True, self.text_color,
        self.main_settings.bg_color)
        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    
    def prep_high_score(self):
        """Turn the high score into a rendered image"""
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
        self.text_color, self.main_settings.bg_color)
        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top
        
    def show_score(self):
        """Draw score to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)