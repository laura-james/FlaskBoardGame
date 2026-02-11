// had to make it async now that the mark completed function is added
// added puzzle_id as parameter
async function checkSquare(row,col,puzzle_id){
    // runs on every key up in the puzzle
    input = document.getElementById("boxR"+row+"C"+col);
    console.log(input.innerHTML);
    input.innerText = input.innerText.slice(0, 1);//only allows user to enter one character
    
    if (input.innerHTML==="<br>") { //remove error if blank
        input.classList.remove("error");
    //use regex to check if its a number between 1 and 9 inclusive
    } else if (!/^[1-9]$/.test(input.innerText)) {
        input.classList.add("error");
  
    }else if (checkRow(row, col, input.innerText)){
        input.classList.add("error");
    }else if (checkCol(row, col, input.innerText)){
        input.classList.add("error");
    }else if (checkBox(row, col, input.innerText)){
        input.classList.add("error");
    } else {
        input.classList.remove("error");
    }
    //NEW check if puzzle is the same as solution if so then say congrats and set isFinished to 1
    if (checkFinished(puzzle_id)){
        alert("congrats you have completed the puzzle! TODO - save puzzle and set isFinished to 1 - and what else...?")
        // TODO save puzzle and set isFinished to 1
        // Should the puzzle.....?
        const response = await fetch('/puzzle_finished/'+puzzle_id+'/1'); //TODO update user_id
        const result = await response.text();  
        console.log(result);
    }
}
function checkRow(row,currentcol,value){
    for (let col = 0; col < 9; col++) {
        if (document.getElementById("boxR"+row+"C"+col).innerText == value && currentcol!=col) {
            //console.log("found duplicate boxR"+row+"C"+col);
            return true;
        }
    }
    return false;
}

function checkCol(currentrow,col,value){
    for (let row = 0; row < 9; row++) {
        if (document.getElementById("boxR"+row+"C"+col).innerText == value && currentrow!=row) {
            //console.log("found duplicate boxR"+row+"C"+col);
            return true;
        }
    }
    return false;
}

function checkBox(currentrow,currentcol,value){    
    // check the 3x3 square for duplicate
    // Find top-left corner of the 3x3 box
    const boxStartRow = Math.floor(currentrow / 3) * 3;
    const boxStartCol = Math.floor(currentcol / 3) * 3;
    for (let row = boxStartRow; row < boxStartRow + 3; row++) {
        for (let col = boxStartCol; col < boxStartCol + 3; col++) {
            if (document.getElementById("boxR"+row+"C"+col).innerText == value && currentcol!=col && currentrow!=row) {
            //duplicate found in box
            return true;
            }
        }
    }
    return false;
}
function checkFinished(puzzle_id){
    // called from checkSquare() function which runs on each keyUp event
    // loops through all boxes in puzzle
    // checks against the solution
    // returns false as soon as it finds a mismatch
    // if no mismatch found it returns true
    console.log("hello!!!")
    for (let row = 0; row < 9; row++) {
        for (let col = 0; col < 9; col++) {
            let answer = document.querySelector(".solution_grid #boxR"+row+"C"+col).innerHTML;
            let attempt = document.querySelector(".puzzle_grid #boxR"+row+"C"+col).innerHTML;
            if (answer != attempt) {
                //incorrect answer found so return false
                console.log("row: "+ row +" col: "+ col +" answer: "+ answer + " attempt: " + attempt);
                return false;
            }
        }
    }
    console.log("all attempts correct - game complete")
    return true;
}



//HINTS
function showHintMenu(e, i , j, puzzle_id){
    e.preventDefault();
      console.log(i,j);
      // Position and show custom menu
      contextMenu.style.display = 'block';
      contextMenu.style.left = e.pageX + 'px';
      contextMenu.style.top = e.pageY + 'px';
      contextMenu.innerHTML = "<a href=\"javascript:acceptHint(" + i + "," + j + ","+puzzle_id+")\">Use hint for this cell</a>"
}

// Hide menu when clicking elsewhere
document.addEventListener('click', function() {
    contextMenu.style.display = 'none';
});

async function acceptHint(i, j, puzzle_id){
    let user_id = 1; //TODO get this from the logged in user
    const response = await fetch('/get_hint/'+ user_id+'/'+puzzle_id);
    const result = await response.text();  
    console.log(result);  // Prints the message that is returned from the get hint page
    alert("You've accepted hint for cell " + i + "," + j + " for puzzle id " + puzzle_id );
    // TODO show the correct answer in the cell!
    // NEW!!
    let answer = document.querySelector(".solution_grid #boxR"+i+"C"+j).innerHTML;
    console.log(answer);
    document.querySelector(".puzzle_grid #boxR"+i+"C"+j).innerHTML = answer;
    //NEW !!!! Use result above to write the new hint number to the place on the doc
    document.getElementById("num_hints").innerHTML = result;
}

async function save_puzzle(puzzle_id){
    //alert("TODO - save puzzle to db");
    //NEW!!
    // this runs the save_puzzle route in python
    const puzzleData = getPuzzleData(); 

    // Send the data to the Python route 'save_puzzle' - it uses POST at its sending data
    const response = await fetch('/save_puzzle/' + puzzle_id, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ puzzle: puzzleData })
    });

    // Check if Python sent back "OK"
    const status = await response.text();
    if (status === "OK") {
        alert("Game Saved!");
    }   
}

function clear_puzzle(puzzle_id){
  //alert("TODO - clear cells");
  //NEW!!
  // get all the cells that are in the puzzle grid
  let cells = document.querySelectorAll(".puzzle_grid .empty");
  //loop through each of these setting the innerHTML to blank
  for(let i = 0; i < cells.length; i++){
    cells[i].innerHTML = "";
    cells[i].classList.remove("error");//gets rid of the red error bg
  }
  // should it also save this to db??
  save_puzzle(puzzle_id);
}
function getPuzzleData() {
    /* helper function to get the puzzle data from teh screen and turn it into 2darray */
    let puzzleArray = [];

    for (let i = 0; i < 9; i++) {
        let row = [];
        for (let j = 0; j < 9; j++) {
            // Target the specific box using  ID 
            let cell = document.querySelector(".puzzle_grid #boxR" + i + "C" + j);
            let value = cell.innerText.trim();// get rid of unneeded spaces

            // Convert to integer if it's a number, otherwise null
            if (value === "" || isNaN(value)) {
                row.push(null);
            } else {
                row.push(parseInt(value));
            }
        }
        puzzleArray.push(row);
    }
    return puzzleArray;
}






//tic tac toe stuff here....
var playerTurn = "X";
var moves = ["","","","","","","","",""];
var gameFinished = false;
function clickSquare(num){

  if (gameFinished){
    return
  }
  if(checkifEmpty(num)){
    document.getElementById("box"+num).innerHTML=playerTurn;
    document.getElementById("box"+num).classList.add(playerTurn);
    moves[num-1]=playerTurn;
    console.log(moves);
    if (!checkWin()){
      if(playerTurn=="X"){
        playerTurn="O";
      }else{
        playerTurn="X";
      }//end if

      console.log(moves.join("").length);
      if (checkDraw()){
        document.getElementById("msg").innerHTML="Game is a DRAW";
      }else{      
       document.getElementById("msg").innerHTML="Player "+playerTurn+" goes next";
      }
     }
  }else{
   // alert("Invalid Move!");
    document.getElementById("msg").innerHTML="Invalid Move!";
  }//end if

}//end function
function checkifEmpty(num){
 if (moves[num-1]==""){
    return true;
 }
 return false;
}
function checkWin(){
 if((moves[0]==moves[1]) && (moves[1]==moves[2]) && (moves[0] !="") || 
 (moves[3]==moves[4]) && (moves[3]==moves[5]) && (moves[3] !="") || 
 (moves[6]==moves[7]) && (moves[6]==moves[8]) && (moves[6] !="") ||
 (moves[0]==moves[3]) && (moves[0]==moves[6]) && (moves[0] !="") ||
 (moves[1]==moves[4]) && (moves[1]==moves[7]) && (moves[1] !="") ||
 (moves[2]==moves[5]) && (moves[2]==moves[8]) && (moves[2] !="") ||
 (moves[0]==moves[4]) && (moves[0]==moves[8]) && (moves[8] !="") ||
 (moves[2]==moves[4]) && (moves[2]==moves[6]) && (moves[2] !="")
 ){
    document.getElementById("msg").innerHTML=playerTurn+" wins!!";
    gameFinished = true;
    return true;
  }
  return false;
}
function checkDraw(){
     if (moves.join("").length==9){
   return true;
   }
   return false;
}








