# Rule-Based Heuristic AI Agent for N×N Connect-style TicTacToe

An rule-based search AI agent designed to play a variable-grid ($N \times N$, $N \in [3, 10]$) Connect-style TicTacToe game under strict time constraints ($< 1\text{s}$ per move). 

Developed for the **INTROPROG / MAR-IP** course assignment at Stockholm / Marseille.

---

## 📌 Project Overview

This variant of TicTacToe introduces dynamic game rules:
- **Grid Size ($N$):** $N \times N$, where $3 \le N \le 10$.
- **Win Target ($M$):** $M$ adjacent pieces horizontally, vertically, or diagonally ($3 \le M \le N$).
- **Gravity Rule:** Pieces are dropped into columns, stacking from the bottom up.
- **Turn Time Limit:** Maximum **1 second** decision time per turn.

The agent evaluates board states dynamically to win, block opponent tactics, create double threats, and avoid catastrophic trap moves.

---
losses

🏗️ Project Architecture

tictactoe-ai-agent/
├── game.py                     # Provided base game script
├── player_ai_agent.py          # Your AI agent code
├── player_human.py             # Provided human player script
├── LICENSE                     # Standard MIT License
└── README.md                   # Project documentation


## 🧠 Decision Hierarchy Strategy

The AI evaluates potential moves through a prioritized rule-based search hierarchy:

1. **Immediate Win Check:** Detects and executes any immediate winning column move for the current turn.
2. **Immediate Block Check:** Scans and blocks any single move that allows the opponent to win on their next turn.
3. **Double Threat Creation:** Simulates potential moves to identify setups that yield two simultaneous winning paths on the subsequent turn, guaranteeing a victory.
4. **Best Heuristic Move (Sequence Maximization):** 
   - Evaluates all legal moves by calculating the maximum length of adjacent matching pieces formed.
   - **Look-Ahead Safety Filter:** Filters out candidate moves that would allow the opponent to stack a winning piece directly on top in the subsequent turn.

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8+
- No third-party packages required (uses Python standard libraries only).

### Running the Game

1. Clone this repository:
   ```bash
   git clone [https://github.com/YOUR_USERNAME/tictactoe-ai-agent.git](https://github.com/YOUR_USERNAME/tictactoe-ai-agent.git)
   cd tictactoe-ai-agent