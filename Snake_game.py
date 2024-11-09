import tkinter as tk
import random

# Constants
width = 600  # Width of the game canvas
height = 400  # Height of the game canvas
snake_size = 20  # Size of each snake segment and food
initial_speed = 100  # Initial speed of the snake in milliseconds

# Colors
background_color = "black"  # Background color of the canvas
snake_head_color = "darkgreen"  # Color of the snake's head
snake_body_color = "green"  # Color of the snake's body
food_color = "red"  # Color of the food
text_color = "white"  # Color of text displayed on canvas

class SnakeGame:
    def __init__(self, window):
        # Initialize the game window and settings
        self.window = window
        self.window.title("Snake Game")

        # Setup canvas for drawing
        self.canvas = tk.Canvas(self.window, bg=background_color, width=width, height=height)
        self.canvas.pack()

        # Game state variables
        self.snake = [(width // 2, height // 2)]  # Initial snake position (center of canvas)
        self.snake_direction = "Right"  # Initial movement direction of the snake
        self.food_position = self.place_food()  # Place food randomly on the canvas
        self.score = 0  # Current score
        self.highest_score = 0  # Highest score achieved in a session
        self.speed = initial_speed  # Speed of the game (decreases as the game progresses)
        self.game_running = False  # Game is initially not running

        # Create Start Game button
        self.start_button = tk.Button(self.window, text="Start Game", command=self.start_game, font=("Arial", 16))
        self.start_button.pack(pady=20)

        # Bind keyboard controls for snake movement
        self.window.bind("<KeyPress>", self.change_direction)

        # Show the welcome screen
        self.show_start_screen()
        self.window.mainloop()

    def show_start_screen(self):
        """Display a welcome screen."""
        self.canvas.delete("all")
        self.canvas.create_text(
            width // 2, height // 2 - 20,
            text="Welcome to Snake Game", fill=text_color, font=("Arial", 24)
        )
        self.canvas.create_text(
            width // 2, height // 2 + 20,
            text="Press Start Game to begin",
            fill=text_color, font=("Arial", 16)
        )

    def start_game(self):
        """Start the game by initializing game state and hiding the Start button."""
        self.game_running = True
        self.start_button.pack_forget()  # Hide the start button
        self.update_snake()  # Begin updating snake position

    @staticmethod
    def place_food():
        """Place food randomly on the canvas grid."""
        x = random.randint(0, (width - snake_size) // snake_size) * snake_size
        y = random.randint(0, (height - snake_size) // snake_size) * snake_size
        return x, y  # Return new food position

    def change_direction(self, event):
        """Change the direction of the snake based on user input."""
        if not self.game_running:
            return  # Ignore input if the game hasn't started

        new_direction = event.keysym  # Get the key pressed
        all_directions = ["Up", "Down", "Left", "Right"]  # Valid directions
        opposites = {"Up": "Down", "Down": "Up", "Left": "Right", "Right": "Left"}

        # Change direction only if it's valid and not directly opposite to current
        if new_direction in all_directions and new_direction != opposites.get(self.snake_direction, ""):
            self.snake_direction = new_direction

    def update_snake(self):
        """Update the snake's position and check for events like eating food or collisions."""
        if not self.game_running:
            return

        # Move the snake in the current direction
        x, y = self.snake[0]
        if self.snake_direction == "Up":
            y -= snake_size
        elif self.snake_direction == "Down":
            y += snake_size
        elif self.snake_direction == "Left":
            x -= snake_size
        elif self.snake_direction == "Right":
            x += snake_size

        # Check for collisions with walls or itself
        new_head = (x, y)
        if (
            x < 0 or x >= width or y < 0 or y >= height  # Wall collision
            or new_head in self.snake  # Self-collision
        ):
            self.end_game()  # End game if collision occurs
            return

        # Check if snake eats the food
        self.snake.insert(0, new_head)  # Add new head to the snake
        if new_head == self.food_position:
            self.score += 1  # Increase score
            self.food_position = self.place_food()  # Place new food
            self.speed = max(50, self.speed - 2)  # Increase speed
        else:
            self.snake.pop()  # Remove last segment if food not eaten

        # Draw updated snake and food on canvas
        self.draw_elements()
        self.window.after(self.speed, self.update_snake)  # Call update at new speed

    def draw_elements(self):
        """Draw the snake, food, and score on the canvas."""
        self.canvas.delete("all")

        # Draw food
        self.canvas.create_oval(
            self.food_position[0], self.food_position[1],
            self.food_position[0] + snake_size, self.food_position[1] + snake_size,
            fill=food_color
        )

        # Draw snake
        for index, (x, y) in enumerate(self.snake):
            if index == 0:
                # Draw the snake's head with a distinct color
                self.canvas.create_oval(
                    x, y, x + snake_size, y + snake_size, fill=snake_head_color
                )
            else:
                # Draw the rest of the snake's body
                self.canvas.create_oval(
                    x, y, x + snake_size, y + snake_size, fill=snake_body_color
                )

        # Display current score and highest score
        self.canvas.create_text(
            90, 10, text=f"Score: {self.score} | Highest: {self.highest_score}", fill=text_color, font=("Arial", 14)
        )

    def end_game(self):
        """Handle game-over state by stopping the game and updating the high score."""
        self.game_running = False

        # Update the highest score if current score is greater
        if self.score > self.highest_score:
            self.highest_score = self.score

        # Display Game Over message and instructions to restart
        self.canvas.create_text(
            width // 2, height // 2,
            text="Game Over! Press R to Restart",
            fill=text_color, font=("Arial", 24)
        )
        self.window.bind("<KeyPress-r>", lambda _: self.restart_game())  # Bind "R" key to restart

    def restart_game(self):
        """Reset game state to restart the game."""
        self.snake = [(width // 2, height // 2)]  # Reset snake to initial position
        self.snake_direction = "Right"  # Reset direction
        self.food_position = self.place_food()  # Place food again
        self.score = 0  # Reset score
        self.speed = initial_speed  # Reset speed
        self.game_running = True  # Set game to running
        self.window.unbind("<KeyPress-r>")  # Unbind the restart key
        self.update_snake()  # Start the game loop again

# Initialize and run the game
root = tk.Tk()
game = SnakeGame(root)
