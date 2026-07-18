const registerForm =
document.getElementById("registerForm");


const username =
document.getElementById("username");


const email =
document.getElementById("email");


const password =
document.getElementById("password");


const confirmPassword =
document.getElementById("confirmPassword");


const message =
document.getElementById("message");



const togglePassword =
document.getElementById("togglePassword");




// نمایش و مخفی کردن رمز

togglePassword.addEventListener("click",()=>{


if(password.type==="password"){


password.type="text";


togglePassword.classList.remove("fa-eye");


togglePassword.classList.add("fa-eye-slash");


}

else{


password.type="password";


togglePassword.classList.remove("fa-eye-slash");


togglePassword.classList.add("fa-eye");


}


});






// ثبت نام

registerForm.addEventListener("submit",(e)=>{


e.preventDefault();



let userData={


username:username.value.trim(),

email:email.value.trim(),

password:password.value.trim()


};





if(password.value !== confirmPassword.value){


showMessage(
"Passwords do not match",
"error"
);


return;

}




let users = JSON.parse(

localStorage.getItem("users")

) || [];






// بررسی تکراری بودن Username


let exist = users.find(user=>


user.username === userData.username


);




if(exist){


showMessage(

"Username already exists",

"error"

);


return;


}





// ذخیره کاربر


users.push(userData);



localStorage.setItem(

"users",

JSON.stringify(users)

);





showMessage(

"Account created successfully",

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