
import arcade
import os
import random
from config import *


class BaksoGame(arcade.Window):
    """Main game class"""
    
    def __init__(self):
        """Initialize the game"""
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.SKY_BLUE)
        
        # Game state
        self.scene = None
        self.background_list = None
        self.character_list = None
        self.character_sprite = None
        self.item_sprites = None
        
    def setup(self):
        """Set up the game here. Call this function to restart the game."""
        # Initialize SpriteLists
        self.background_list = arcade.SpriteList()
        self.item_sprites = arcade.SpriteList()

        # Load background
        try:
            self.background_sprite = arcade.Sprite(f"{BACKGROUNDS_PATH}/Background.png")
            
            # Position background at center of screen
            self.background_sprite.center_x = SCREEN_WIDTH // 2
            self.background_sprite.center_y = SCREEN_HEIGHT // 2
            
            # Calculate scale to cover the screen (1280x720)
            # Image is 1000x1000
            scale_x = SCREEN_WIDTH / self.background_sprite.width + 0.15
            scale_y = SCREEN_HEIGHT / self.background_sprite.height + 0.15
            self.background_sprite.scale = max(scale_x, scale_y)
            
            self.background_list.append(self.background_sprite)
        except Exception as e:
            print(f"Error loading background: {e}")

        # Load Gerobak
        try:
            # Load texture
            self.gerobak_sprite = arcade.Sprite(f"{ITEMS_PATH}/Gerobak.png")
            
            # Match background scale and position
            self.gerobak_sprite.scale = self.background_sprite.scale
            self.gerobak_sprite.center_x = self.background_sprite.center_x
            self.gerobak_sprite.center_y = self.background_sprite.center_y
            
            # Add to item list
            self.item_sprites.append(self.gerobak_sprite)
        except Exception as e:
            print(f"Error loading gerobak: {e}")

        # Load Character (Pembeli)
        try:
            # Get random pembeli image
            pembeli_path = f"{CHARACTERS_PATH}/Pembeli"
            pembeli_files = [f for f in os.listdir(pembeli_path) if f.endswith('.png')]
            
            if pembeli_files:
                selected_pembeli = random.choice(pembeli_files)
                print(f"Loading random pembeli: {selected_pembeli}")
                self.character_sprite = arcade.Sprite(f"{pembeli_path}/{selected_pembeli}", PEMBELI_SCALE)
            else:
                print("No pembeli images found!")
                return

            # Position character
            self.character_sprite.center_x = PEMBELI_POS_X
            self.character_sprite.center_y = PEMBELI_POS_Y
            
            # Create character list and add sprite
            self.character_list = arcade.SpriteList()
            self.character_list.append(self.character_sprite)
            
        except Exception as e:
            print(f"Error loading character: {e}")
            
    def on_draw(self):
        """Render the screen."""
        self.clear()
        
        # Draw background
        if self.background_list:
            self.background_list.draw()
        
        # Draw character
        if self.character_list:
            self.character_list.draw()
        
        # Draw items
        self.item_sprites.draw()
    
    def on_update(self, delta_time):
        """Movement and game logic"""
        # Update sprites
        self.item_sprites.update()
    
    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed."""
        if key == arcade.key.ESCAPE:
            arcade.close_window()
    
    def on_mouse_press(self, x, y, button, modifiers):
        """Called when the user presses a mouse button."""
        pass
