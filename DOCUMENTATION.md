# Documentation: Routes and JavaScript References in `main.py`

## Routes in `main.py` and Their Functions

### 1. `/`
- **Python Definition**:
  ```python
  @web_site.route('/')
  def home():
      return render_template("home.html")
  ```
- **Purpose**: Renders the `home.html` template, which displays the home page with navigation and Sudoku options.

---

### 2. `/startpuzzle/<difficulty>`
- **Python Definition**:
  ```python
  @web_site.route('/startpuzzle/<difficulty>')
  def puzzleadd(difficulty):
      # Fetches a Sudoku puzzle and solution from an external API and stores them in the database
      # Redirects to a puzzle solving page for the generated puzzle.
  ```
- **Purpose**: Generates a new Sudoku puzzle based on difficulty (`easy`, `medium`, `hard`) and redirects to `/do_puzzle/<puzzle_id>`.

---

### 3. `/do_puzzle/<puzzle_id>`
- **Python Definition**:
  ```python
  @web_site.route('/do_puzzle/<puzzle_id>')
  def get_puzzle(puzzle_id):
      # Retrieves a puzzle from the database; renders it for interaction.
  ```
- **Purpose**: Fetches the puzzle from the database and allows solving or rendering as Sudoku.

---

### 4. `/save_puzzle/<int:puzzle_id>`
- **Python Definition**:
  ```python
  @web_site.route('/save_puzzle/<int:puzzle_id>', methods=['POST'])
  def save_puzzle(puzzle_id):
      # Updates the puzzle state in the database.
  ```
- **Purpose**: Saves the user's puzzle progress via a POST request.

---

### 5. `/tictactoe`
- **Python Definition**:
  ```python
  @web_site.route('/tictactoe')
  def tictactoe():
      return render_template("tictactoe.html")
  ```
- **Purpose**: Renders a Tic Tac Toe game page.

---

### 6. `/get_hint/<user_id>/<puzzle_id>`
- **Python Definition**:
  ```python
  @web_site.route('/get_hint/<user_id>/<puzzle_id>')
  def get_hint(puzzle_id, user_id):
      # Adds a hint to the specified puzzle for the user.
  ```
- **Purpose**: Requests and records a new hint for a Sudoku puzzle.

---

## JavaScript References to Routes

### 1. `/save_puzzle/<int:puzzle_id>`
- **JavaScript Function**:
  ```javascript
  async function save_puzzle(puzzle_id) {
      const puzzleData = getPuzzleData();
      const response = await fetch('/save_puzzle/' + puzzle_id, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ puzzle: puzzleData })
      });
      const status = await response.text();
      if (status === "OK") alert("Game Saved!");
  }
  ```
- **Purpose**: This function runs when saving a puzzle game's progress via the `/save_puzzle` POST route.

---

### 2. Template and Navigation Links
- **HTML Snippet** (from `templates/base.html` and `templates/home.html`):
  ```html
  <li><a href="/startpuzzle/easy">Easy</a></li>
  <li><a href="/mypuzzles">My Puzzles</a></li>
  ```
- **References**:
  - `/startpuzzle/<difficulty>` is directly linked here for `easy`, `medium`, and `hard`.
  - `/mypuzzles` and other routes may rely on direct navigation rather than JavaScript.

---

### 3. `/do_puzzle/<puzzle_id>`
This route is accessed via redirects in Python after generating new puzzles. No direct JavaScript calls are evident here.

---

## Summary
This document outlines the functionality of Flask routes in `main.py` and how they are referenced or called using JavaScript or HTML templates in the project.