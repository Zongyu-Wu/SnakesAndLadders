function checkUsername(){
    $.ajax({
        type:"GET",
        url: "database.json",
        success: function(response){
            const username = document.getElementById("inputUsername").value;
            const hasValue = Object.values(response).includes(username);
            if(hasValue){
                $("#usersuccess").html("");
                document.getElementById("signup").disabled = true;
                $("#usererror").html("User already exists");
            }
            else{
                $("#usererror").html("");
                document.getElementById("signup").disabled = false;
                $("#usersuccess").html("Username available");
            }
        }
    });
}

function checkEmail(){
    $.ajax({
        type:"GET",
        url: "database.json",
        success: function(response){
            const email = document.getElementById("inputEmail").value;
            const hasValue = Object.values(response).includes(email);
            if(hasValue){
                $("#usersuccess").html("");
                document.getElementById("signup").disabled = true;
                $("#usererror").html("Email already exists");
            }
            else{
                $("#usererror").html("");
                document.getElementById("signup").disabled = false;
                $("#usersuccess").html("Email available");
            }
        }
    });
}

