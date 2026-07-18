// گرفتن عناصر صفحه

const loginForm = document.getElementById("loginForm");

const username = document.getElementById("username");

const password = document.getElementById("password");

const message = document.getElementById("message");

const togglePassword = document.getElementById("togglePassword");



// نمایش و مخفی کردن رمز عبور

togglePassword.addEventListener("click", function(){

    if(password.type === "password"){

        password.type = "text";

        togglePassword.classList.remove("fa-eye");

        togglePassword.classList.add("fa-eye-slash");

    }

    else{

        password.type = "password";

        togglePassword.classList.remove("fa-eye-slash");

        togglePassword.classList.add("fa-eye");

    }

});




// رویداد Login

loginForm.addEventListener("submit", function(e){


    // جلوگیری از Refresh شدن صفحه

    e.preventDefault();



    let user = username.value.trim();

    let pass = password.value.trim();



    // بررسی خالی بودن فیلدها

    if(user === "" || pass === ""){


        showMessage(
            "Please fill all fields",
            "error"
        );

        return;

    }




    // گرفتن کاربران ثبت نام شده

    let users = JSON.parse(
        localStorage.getItem("users")
    ) || [];



    // پیدا کردن کاربر

    let foundUser = users.find(function(item){

        return item.username === user &&
               item.password === pass;

    });



    if(foundUser){


        // ذخیره وضعیت Login

        localStorage.setItem(
            "currentUser",
            JSON.stringify(foundUser)
        );


        showMessage(
            "Login successful...",
            "success"
        );



        setTimeout(function(){


            window.location.href="dashboard.html";


        },1500);



    }

    else{


        showMessage(
            "Invalid username or password",
            "error"
        );


    }


});





// تابع نمایش پیام

function showMessage(text,type){


    message.innerHTML=text;



    if(type==="success"){

        message.style.color="#4ade80";

    }

    else{

        message.style.color="#f87171";

    }


}