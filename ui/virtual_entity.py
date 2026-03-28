import os
import random

class VirtualEntity:
    def __init__(self, assets_path="ui/assets"):
        self.assets_path = assets_path
        self.states = [d for d in os.listdir(assets_path) if os.path.isdir(os.path.join(assets_path, d))]

    def get_new_animation(self, state_name):
        state = state_name.capitalize() 
        folder_path = os.path.join(self.assets_path, state)
        
        if not os.path.exists(folder_path):
            folder_path = os.path.join(self.assets_path, "Standby")

        all_gifs = [f for f in os.listdir(folder_path) if f.endswith('.gif')]
        
        if not all_gifs:
            return None
            
        chosen_gif = random.choice(all_gifs)
        return os.path.join(folder_path, chosen_gif)