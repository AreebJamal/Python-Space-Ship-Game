class Gamestats:
    """Track statistic for alien invasion"""

    def __init__(self , ai_game) -> None:
        """Initialize statistic"""
        self.settings = ai_game.settings
        self.reset_stats()
        #Start alien invasion in inactive state.
        self.game_active = False
    
    
    def reset_stats(self):
        """Initialize statistic that can change during the game"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        
    

        
