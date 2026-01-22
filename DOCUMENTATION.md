# Documentation: Routes and JavaScript references in `main.py`

## Routes in `main.py` and their functions

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
      num_hints = get_num_hints(puzzle_id, user_id)  # Gets number of hints used for this puzzle
      return render_template("suduko.html", puzzle_id=puzzle_id, puzzle=puzzle, solution=solution, num_hints=num_hints, attempt=attempt)
  ```
- **Purpose**: Fetches the puzzle from the database and allows solving or rendering as Sudoku.

---

### 4. `/save_puzzle/<int:puzzle_id>`
- **Python Definition**:
  ```python
  @web_site.route('/save_puzzle/<int:puzzle_id>', methods=['POST'])
  def save_puzzle(puzzle_id):
      data = request.get_json()
      # Updates the user-provided attempt JSON in the database.
  ```
- **Purpose**: Saves the user's Sudoku attempt (progress) via a POST request.

---

### 5. `/get_hint/<user_id>/<puzzle_id>`
- **Python Definition**:
  ```python
  @web_site.route('/get_hint/<user_id>/<puzzle_id>')
  def get_hint(puzzle_id, user_id):
      # Adds a hint for the user for a specific puzzle.
  ```
- **Purpose**: Facilitates hint functionality for a Sudoku puzzle.

---

### 6. `/puzzle_finished/<int:puzzle_id>`
- **Python Definition**:
  ```python
  @web_site.route('/puzzle_finished/<int:puzzle_id>')
  def puzzle_finished(puzzle_id):
      # Sets the isFinished flag for a completed puzzle.
  ```
- **Purpose**: Marks a Sudoku puzzle as completed when all entries match the solution.


---

## JavaScript references to routes

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
- **Purpose**: Saves the game's progress

# THERE ARE OTHERS...

# JavaScript Functions in `script.js`

## 1. `checkSquare(row, col, puzzle_id)`
- **Definition**:
  ```javascript
  async function checkSquare(row, col, puzzle_id) {
      // Runs on every key up in the puzzle.
      // Allows one valid character input and checks row, column, or 3x3 grids for conflicts.
      if (checkFinished(puzzle_id)) {
          alert("Congratulations! Puzzle completed.");
          const response = await fetch('/puzzle_finished/' + puzzle_id);
          const result = await response.text();
          console.log(result);
      }
  }
  ```
- **Purpose**: Validates the user input in the Sudoku grid, giving visual feedback for errors and checking if the puzzle is complete.

---

## 2. `checkRow(row, currentCol, value)`
- **Definition**:
  ```javascript
  function checkRow(row, currentCol, value) {
      for (let col = 0; col < 9; col++) {
          if (document.getElementById("boxR" + row + "C" + col).innerText == value && currentCol != col) {
              return true;
          }
      }
      return false;
  }
  ```
- **Purpose**: Checks for duplicate entries in the same row in the Sudoku grid.

---

## 3. `checkCol(currentRow, col, value)`
- **Definition**:
  ```javascript
  function checkCol(currentRow, col, value) {
      for (let row = 0; row < 9; row++) {
          if (document.getElementById("boxR" + row + "C" + col).innerText == value && currentRow != row) {
              return true;
          }
      }
      return false;
  }
  ```
- **Purpose**: Checks for duplicate entries in the same column in the Sudoku grid.

---

## 4. `checkBox(currentRow, currentCol, value)`
- **Definition**:
  ```javascript
  function checkBox(currentRow, currentCol, value) {
      const boxStartRow = Math.floor(currentRow / 3) * 3;
      const boxStartCol = Math.floor(currentCol / 3) * 3;
      for (let row = boxStartRow; row < boxStartRow + 3; row++) {
          for (let col = boxStartCol; col < boxStartCol + 3; col++) {
              if (document.getElementById("boxR" + row + "C" + col).innerText == value && currentCol != col && currentRow != row) {
                  return true;
              }
          }
      }
      return false;
  }
  ```
- **Purpose**: Ensures no duplicates exist within the local 3x3 sub-grid of the Sudoku.

---

## 5. `checkFinished(puzzle_id)`
- **Definition**:
  ```javascript
  function checkFinished(puzzle_id) {
      for (let row = 0; row < 9; row++) {
          for (let col = 0; col < 9; col++) {
              // Checks each square to ensure all match the solution.
          }
      }
  }
  ```
- **Purpose**: Determines whether the Sudoku puzzle is completely and correctly solved and triggers backend updates.

---

**Note**: The `script.js` file referenced in this export may contain additional functions or further details not captured here, as the results are limited. You can view more results [here on GitHub](https://github.com/laura-james/FlaskBoardGame/blob/b952610674e80612d654b1abf7b1b8d5266c3d2f/static/script.js).