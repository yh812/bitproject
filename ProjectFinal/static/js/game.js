var playerScore=0;
var computerScore=0;
var rock= document.getElementById("rock");
var paper= document.getElementById("paper");
var scissors= document.getElementById("scissors");
var displayPlayerScore= document.getElementById("playerScore");
var displayComputerScore= document.getElementById("computerScore");
var gameStatus= document.getElementById("status");
var displayPlayerSelection= document.getElementById("playerSelection");
var displayComputerSelection= document.getElementById("computerSelection");
var reset= document.getElementById("reset");
var gamestart= document.getElementById("gamestart");
var button = document.getElementById("reset");




play = (playerSelection,computerSelection) => 
{
    if(playerSelection === computerSelection){
        gameStatus.textContent="비겼습니다!!!";
    }else if (playerSelection === '가위' && computerSelection === '보'){   
        playerScore ++;
        gameStatus.textContent=`컴퓨터 패배, ${playerSelection} 대 ${computerSelection} !!`;
    }else if(playerSelection === '가위' && computerSelection === '바위'){
        computerScore ++;
        gameStatus.textContent=`컴퓨터 승리, ${computerSelection} 대 ${playerSelection} !!`;
    }else if (playerSelection === '바위' && computerSelection === '보'){
        computerScore ++;
        gameStatus.textContent=`컴퓨터 승리, ${computerSelection} 대 ${playerSelection} !!`;
    }else if (playerSelection === '바위' && computerSelection === '가위'){
        playerScore ++;
        gameStatus.textContent=`컴퓨터 패배, ${playerSelection} 대 ${computerSelection} !!`;
    }else if (playerSelection === '보' && computerSelection === '가위'){
        computerScore ++;
        gameStatus.textContent=`컴퓨터 승리, ${computerSelection} 대 ${playerSelection} !!`;
    }else if (playerSelection === '보' && computerSelection === '바위'){
        playerScore ++;
        gameStatus.textContent=`컴퓨터 패배, ${playerSelection} 대 ${computerSelection} !!`;
    }
    

}



                  
                                   
                  



random = () => 
{
    return (Math.floor(Math.random() *(3)));
}

let value=["바위","보","가위"];

//computerPlay() returns random value from array value[] using random function

computerPlay = () =>
{
    return value[random()];
}


   
function refreshRe(){
   location.reload()
}


var darami = 0  //첫번째 판
var wincounter = 0   //연승 변수
var playerScore=0;
var computerScore=0;
var winplay=true;
function playRound(playerSelection) {
      console.log(winplay)   
   
   if($("#userpoint").val() < 20){
      alert("포인트가 부족합니다.")
      return false;
   }
     if (darami==0){
      if(playerSelection=="바위"){
         var question =confirm('게임을 시작하시겠습니까? 바위을 선택합니다')
      }
      if(playerSelection=="보"){
         var question =confirm('게임을 시작하시겠습니까? 보를 선택합니다')
      }
      if(playerSelection=="가위"){
         var question =confirm('게임을 시작하시겠습니까? 가위를 선택합니다')
      }
   
     if(question==true){
     let computerSelection = computerPlay();
     
     displayPlayerSelection.textContent = playerSelection;
     displayComputerSelection.textContent = computerSelection;
     play(playerSelection, computerSelection);
     displayPlayerScore.textContent = playerScore;
     displayComputerScore.textContent = computerScore;
     darami = 1;
   
     

     }}else{let computerSelection = computerPlay();
    
     displayPlayerSelection.textContent = playerSelection;
     displayComputerSelection.textContent = computerSelection;
     play(playerSelection, computerSelection);
     displayPlayerScore.textContent = playerScore;
     displayComputerScore.textContent = computerScore;
   
     
     
     if (playerScore === 3) {
/*       rock.style.visibility = "hidden";
       paper.style.visibility = "hidden";
       scissors.style.visibility = "hidden";*/
       var wincount = $("#wincount").val() 
       /*alert("승리");*/
       winplay = confirm("승리! 계속 도전?")
       wincounter++;
       console.log(winplay);
       $('#wincounthtml').html(wincounter+"승!");
         /*alert(wincounter);*/
        playerScore=0;
       computerScore=0;
       computerSelection.textContent= "-";
       playerSelection.textContent= "-";
       playerScore.textContent= playerScore;
       displayComputerScore.textContent= 0;
       displayPlayerScore.textContent= 0;
       gameStatus.textContent= "가위바위보 중 선택하세요!";       
       darami=0;
       
        
      
     } else if (computerScore === 3) {
       alert("패배!");
       wincounter = 0;
       
       $('#wincounthtml').html("");
       
/*       rock.style.visibility = "hidden";
       paper.style.visibility = "hidden";
       scissors.style.visibility = "hidden";  */ 

      darami=0;
   var game_start= 'chan'
      $.ajax({
           type:"POST",                          
           url:"game",   
           data:{"game_start":game_start},
           datatype:'json',
            success:function(response){               
                   $('#current_point').html(response.user_current_point)
                   refreshRe()
                   /*playerScore=0;
                    computerScore=0;
                computerSelection.textContent= "-";
                playerSelection.textContent= "-";
                playerScore.textContent= playerScore;
                displayComputerScore.textContent= 0;
                displayPlayerScore.textContent= 0;*/
                 
                
            },
            error : function(xhr,errmsg,err) {
               alert('포인트가 없습니다'); 
            }                                             
       })
       }else{
          return false;
       }}     
 
  if(wincounter >=10 || winplay == false){
             $.ajax({
               type:"POST",                          
               url:"game",   
               data: {'wincounter':wincounter},
               datatype:'json',
               success:function(response){              
                       $('#current_point').html(response.user_current_point)
                       playerScore=0;
                       computerScore=0;
                   computerSelection.textContent= "-";
                   playerSelection.textContent= "-";
                   playerScore.textContent= playerScore;
                   displayComputerScore.textContent= 0;
                   displayPlayerScore.textContent= 0;
                   refreshRe()
                },
                error : function(xhr,errmsg,err) {
                   alert('포인트가 없습니다') 
                }                                             
           })
      
      
   }
}





rock.addEventListener('click', () => playRound("바위"));
paper.addEventListener("click", () =>playRound("보"));
scissors.addEventListener("click", () =>playRound("가위"));