# Search Algorithms

This is a small Pac-Man game implemented in Python using Pygame with multiple AI search algorithms for controlling the player. The project includes implementations of: BFS, DFS, Uniform Cost Search (UCS / Dijkstra), A\* search, Minimax, and Alpha-Beta pruning.

## Features

- Play the classic Pac-Man-like game with dots and power pellets.
- Switch between AI modes (BFS, DFS, UCS, A\*) to see pathfinding in action.
- Minimax and Alpha-Beta modes provide simple adversarial decision-making against ghosts.
- Visualize the AI path and visited nodes (toggleable).

## Requirements

- Python 3.8+
- Pygame (>= 2.5.0) — declared in `pyproject.toml`.

## Installation

1. Create and activate a virtual environment (recommended):
```bash
   python -m venv .venv
   source .venv/bin/activate
```

2. Install dependencies:
```bash
   python -m pip install -U pip
   python -m pip install -r requirements.txt # optional if you add a requirements file
   python -m pip install pygame
```

This is a small Pac-Man game implemented in Python using Pygame with multiple AI search algorithms for controlling the player. The project includes implementations of: BFS, DFS, Uniform Cost Search (UCS / Dijkstra), A\* search, Minimax, and Alpha-Beta pruning.

## Quick start (using uv)

The project can be run with a modern lightweight Python workflow tool called `uv`. Below are recommended steps to install `uv`, create the project layout, install dependencies, and run the game.

1. Install `uv` (Choose one method)

   macOS/Linux:

   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

   Windows (PowerShell):

   ```powershell
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

   Using pip:

   ```bash
   pip install uv
   ```

2. Create Project

   ```bash
   # Create and enter directory
   mkdir pacman-ai && cd pacman-ai

   # Create necessary subdirectories
   mkdir -p assets/player_images assets/ghost_images
   ```

3. Copy Files

   Create these 6 files in your `pacman-ai` directory and paste the corresponding code into each file:

   1. `config.py` - Game settings
   2. `board.py` - Game board logic
   3. `entities.py` - Player and ghosts
   4. `algorithms.py` - AI algorithms
   5. `main.py` - Main game file
   6. `pyproject.toml` - Dependencies

4. Install Dependencies

   ```bash
   # Initialize and install
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install pygame
   ```

   Or use `uv run` (no activation needed):

   ```bash
   uv pip install pygame
   ```

5. Run Game

   ```bash
   # With activated environment
   python main.py

   # OR without activation
   uv run main.py
   ```

## Quick Controls Cheat Sheet

| Key        | Action                           |
| ---------- | -------------------------------- |
| Arrow Keys | Move Pac-Man (Manual mode)       |
| 1          | Manual Control                   |
| 2          | BFS Algorithm                    |
| 3          | DFS Algorithm                    |
| 4          | UCS (Dijkstra)                   |
| 5          | A\* Search                       |
| 6          | Minimax                          |
| 7          | Alpha-Beta Pruning               |
| V          | Toggle visited nodes (blue dots) |
| P          | Toggle path lines (green)        |
| R          | Restart (after game over)        |

## Understanding the Visualizations

Path Visualization (Green Lines)

- Shows the planned route to the nearest dot
- Updates dynamically as Pac-Man moves
- Toggle with **P** key

Visited Nodes (Blue Circles)

- Shows which positions the algorithm explored
- More dots = more exploration
- Toggle with **V** key

## Compare Algorithms

1. Press **2** for BFS - See it explore systematically
2. Press **5** for A\* - Notice less exploration (smarter!)
3. Press **6** for Minimax - Watch it avoid ghosts

## Algorithm Quick Reference

| Algorithm  | When to Use                   | Speed  | Path Quality |
| ---------- | ----------------------------- | ------ | ------------ |
| BFS        | Learning, guaranteed shortest | Medium | Optimal      |
| DFS        | Deep mazes                    | Fast   | Not optimal  |
| UCS        | Weighted costs                | Medium | Optimal      |
| A\*        | Best overall pathfinding      | Fast   | Optimal      |
| Minimax    | Avoid enemies                 | Slow   | Tactical     |
| Alpha-Beta | Avoid enemies faster          | Medium | Tactical     |

## Common Issues

Problem: "uv: command not found"
Solution:

```bash
# Restart terminal after installation, or add to PATH:
export PATH="$HOME/.local/bin:$PATH"  # macOS/Linux (adjust if needed)
# On Windows, restart PowerShell
```

Problem: "No module named 'pygame'"
Solution:

```bash
uv pip install pygame
# Or if that fails:
pip install pygame
```

## Problem: Assets not loading

Don't worry — the game works without images. You'll see colored circles instead of sprites.

To add images (optional):

- Download Pac-Man sprites and save as PNG files (45x45 px) in `assets/player_images/` and `assets/ghost_images/`.

## Problem: Game is too slow

Edit `config.py`:

```python
FPS = 30  # Reduce from 60
MINIMAX_DEPTH = 2  # Reduce from 3
```

## Problem: Black screen on start

Wait; there is a startup delay. Or edit `config.py`:

```python
STARTUP_DURATION = 60  # Reduce from 180
```

## Testing Your Installation

```bash
# Check uv is installed
uv --version

# Check Python version (should be 3.8+)
python --version

# Check pygame installed
python -c "import pygame; print(pygame.version.ver)"

# Run the game
python main.py
```

## Next Steps

1. Try all algorithms - Press keys 1-7 to see differences
2. Watch visualizations - Toggle with V and P
3. Understand the code - Read through each module
4. Modify parameters - Edit `config.py` to experiment
5. Add features - Try implementing new algorithms

## File Checklist

Before running, ensure you have:

- `config.py`
- `board.py`
- `entities.py`
- `algorithms.py`
- `main.py`
- `pyproject.toml`
- `assets/` folder (optional)

## Performance Tips

Faster AI:

- Use A\* (key 5) - most efficient
- Reduce search depth for Minimax/Alpha-Beta
- Increase FPS for faster gameplay

Better Visualization:

- Press V to see algorithm exploration
- Press P to see planned path
- Lower FPS to see algorithms work step-by-step

## Development Workflow with uv

```bash
# Add new dependencies
uv pip install package-name

# List installed packages
uv pip list

# Freeze dependencies
uv pip freeze > requirements.txt

# Run without activation
uv run python main.py

# Run with arguments
uv run python main.py --debug
```

## Learning Path

Day 1: Setup and Play

1. Install and run the game
2. Play in manual mode (key 1)
3. Try each AI algorithm (keys 2-7)
4. Observe differences in behavior

Day 2: Understand Code

1. Read `config.py` - understand constants
2. Read `board.py` - understand maze representation
3. Read `entities.py` - understand movement
4. Read `algorithms.py` - understand search

Day 3: Experiment

1. Modify speeds in `config.py`
2. Change scoring values
3. Adjust search depths
4. Try different heuristics in A\*

Day 4: Extend

1. Add a new search algorithm
2. Implement bidirectional search
3. Add new ghost behaviors
4. Create custom levels

## uv vs pip vs venv Comparison

| Feature      | uv                     | pip + venv     | Notes                     |
| ------------ | ---------------------- | -------------- | ------------------------- |
| Simplicity   | One tool for env & run | Multiple steps | uv is convenient          |
| Installation | Single command         | venv + pip     | pip + venv still standard |

## Why uv?

1. Fast and simple environment & run commands
2. Useful for rapid iteration on small projects

## Additional Resources

- uv docs: https://docs.astral.sh/uv/
- Pygame docs: https://www.pygame.org/docs/
- Algorithm tutorials: redblobgames, etc.

## Support

If you still have problems, check Python version, verify files are copied correctly, and ensure `uv` and `pygame` are installed.

Ready to start? Run `python main.py` and press different number keys to try algorithms.
