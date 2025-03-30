# ASCII Tetris 🎮

Minimal terminal-based Tetris game written in Python and containerized with Docker.

## Controls

- ← / →: Move left/right
- ↓: Soft drop
- W: Rotate
- Q: Quit

## To Run (WSL Native Docker)

```bash
docker build -t ascii-tetris .
docker run -it --rm ascii-tetris
