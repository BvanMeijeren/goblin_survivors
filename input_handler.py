import pyglet

class InputHandler:
    def __init__(self):
        self.game_mode = "gameplay"  # Default mode
        self.pressed_keys = {}

    def set_mode(self, mode):
        self.game_mode = mode

    # General function that chooses keys for the active game mode
    def handle_key_press(self, symbol, modifiers, player=None, upgrade_menu=None):
        self.pressed_keys[symbol] = True

        if self.game_mode == "gameplay" and player:
            self._handle_gameplay_key_press(symbol, player)

        if self.game_mode == "upgrade_menu" and upgrade_menu:
            self._handle_upgrade_key_press(symbol, upgrade_menu)

    # General key release function
    def handle_key_release(self, symbol, modifiers):
        self.pressed_keys[symbol] = False

    # gameplay specific actions based on single key press
    def _handle_gameplay_key_press(self, symbol, player):
        """Trigger player actions based on pressed keys."""
        if symbol == pyglet.window.key.SPACE:
            print("Player triggered an action!")  # Example: Shooting
            player.shoot()  # Call a shoot method if it exists

    # Gameplay inputs based on press and hold (continuous) 
    def update_gameplay_inputs(self, dt, player):
        """Handle continuous gameplay inputs (WASD movement)."""
        if self.pressed_keys.get(pyglet.window.key.W, False):
            player.move_up(dt)
        if self.pressed_keys.get(pyglet.window.key.S, False):
            player.move_down(dt)
        if self.pressed_keys.get(pyglet.window.key.A, False):
            player.move_left(dt)
        if self.pressed_keys.get(pyglet.window.key.D, False):
            player.move_right(dt)

    def _handle_upgrade_key_press(self, symbol, upgrade_menu):
        """Trigger upgrades based on key presses."""
        if symbol == pyglet.window.key._1:
            upgrade_menu.apply_upgrade(0)
            self.game_mode = "gameplay"
        
        elif symbol == pyglet.window.key._2:
            upgrade_menu.apply_upgrade(1)
            self.game_mode = "gameplay"

