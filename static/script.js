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








