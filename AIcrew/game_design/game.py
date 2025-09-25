from crewai import Crew,Process
import os
from agents import game_dev_agent,revisor_agent,chief_revisor_agent
from tasks import game_dev_task,chief_revisor_task,revisor_task


game_team = Crew(
    agents=[game_dev_agent,revisor_agent,chief_revisor_agent],
    tasks=[game_dev_task,revisor_task,chief_revisor_task],
    process= Process.sequential,
    verbose= True
)


prompt = """
    Snake Game Description
    Objective:

    The objective of the Snake game is for the player to control a snake that moves across the game area, consuming food while avoiding obstacles, including its own tail. The snake grows longer each time it consumes food, and the game continues until the snake collides with the boundaries of the game area or its own body.
    Game Mechanics:

    Game Area:
        The game takes place in a rectangular grid, typically represented as a 2D matrix or array.
        The grid contains cells, where the snake can move and food can spawn.

    Snake Movement:
        The snake is controlled by the player, typically through arrow keys (Up, Down, Left, Right) or WASD keys.
        The snake moves continuously in one direction until the player changes its direction.
        Movement is discrete, with the snake advancing one cell per frame or tick.
        The snake's body consists of connected segments that follow the movement of the head, forming a continuous line.

    Growth Mechanism:
        The snake starts with a default length (e.g., 3 segments) and grows longer by one segment every time it eats food.
        The new segment is added to the end of the snake's body after consuming food.

    Food:
        Randomly spawns at an unoccupied position in the game area (i.e., not on the snake's body).
        Each piece of food can only be consumed once.
        After being consumed, a new piece of food spawns at another random position.

    Collisions:
        The game ends when the snake collides with any of the following:
            Walls: The boundaries of the game area.
            Self: The snake's own body.

    Game Rules:

    Movement:
        The snake moves continuously, and the player can change its direction using input keys.
        The snake cannot move in the opposite direction of its current movement (e.g., if moving right, it cannot immediately move left).

    Boundaries:
        The edges of the grid act as walls. If the snake crosses these boundaries, the game is over.

    Self-Collision:
        The snake's body grows as it consumes food, but if the snake's head touches any part of its body, the game ends.

    Scoring System:

    Food Consumption:
        Every time the snake eats a piece of food, the player earns points.
        The typical scoring system could be:
            10 points per food item consumed.
        The score increases with each successful food consumption.

    Time or Speed-Based Scoring (Optional):
        Additional points can be awarded based on how long the player survives, or the game can speed up as the snake grows, increasing difficulty over time.

    High Score:
        The player's current score is displayed during gameplay.
        A high-score system can be implemented to keep track of the highest score achieved. 
    """

game = {"game" : prompt}
game_output = game_team.kickoff(inputs=game)
