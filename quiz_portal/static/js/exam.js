let current = 1;

let total = document.querySelectorAll(".question").length;

showQuestion(1);

function showQuestion(n){

document.querySelectorAll(".question").forEach(q=>{
q.style.display="none";
});

document.getElementById("q"+n).style.display="block";

current=n;

}

function nextQuestion(){

if(current < total){

current++;

showQuestion(current);

}

}

function prevQuestion(){

if(current > 1){

current--;

showQuestion(current);

}

}

function markAnswered(n){

document.getElementById("btn"+n).style.background="green";
}
let time=120;

let timer=setInterval(function(){

time--;

document.getElementById("time").innerText=time;

if(time<=0){

clearInterval(timer);

alert("Time Over");

document.getElementById("quizForm").submit();

}

},1000);