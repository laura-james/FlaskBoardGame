function checkSquare(row,col){
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
//TODO check the 3x3 square for duplicate too
function checkBox(currentrow,currentcol,value){    
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








