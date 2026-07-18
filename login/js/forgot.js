const forgotForm =
document.getElementById("forgotForm");


const email =
document.getElementById("email");


const newPassword =
document.getElementById("newPassword");


const message =
document.getElementById("message");





forgotForm.addEventListener("submit",(e)=>{


e.preventDefault();




let users = JSON.parse(

localStorage.getItem("users")

) || [];





let user = users.find(item =>


item.email === email.value.trim()


);





if(!user){


showMessage(

"Email not found",

"error"

);


return;


}






// تغییر رمز عبور


user.password = newPassword.value.trim();





localStorage.setItem(

"users",

JSON.stringify(users)

);






showMessage(

"Password changed successfully",

"success"

);





setTimeout(()=>{


window.location.href="index.html";


},1500);



});






function showMessage(text,type){



message.innerHTML=text;



if(type==="success"){


message.style.color="#4ade80";


}

else{


message.style.color="#f87171";


}



}