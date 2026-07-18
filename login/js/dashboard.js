// گرفتن کاربر فعلی

const currentUser = JSON.parse(

localStorage.getItem("currentUser")

);




// اگر Login نکرده بود

if(!currentUser){


window.location.href="index.html";


}




// نمایش اطلاعات کاربر


document.getElementById("welcome").innerHTML =

`Welcome ${currentUser.username}`;





document.getElementById("username").innerHTML =

currentUser.username;





document.getElementById("email").innerHTML =

currentUser.email;






// Logout


document.getElementById("logout")

.addEventListener("click",()=>{



localStorage.removeItem(

"currentUser"

);



window.location.href="index.html";



});