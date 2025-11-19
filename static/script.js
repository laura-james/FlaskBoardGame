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








