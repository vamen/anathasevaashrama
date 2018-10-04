$(document).ready(function(){

    // jQuery methods go here...

    alert("alert")
    $("#login-submit").click(function(){
            username=$("#username").val()
            college=$("#coll_drop_down").val()         
            password=$("#password").val()
            alert(username+":::"+college)
            $.ajax({
                type: "POST",
                url: "/login",
                data: JSON.stringify({"username":username,"college":college,"password":password}),
                success: function(msg){
                    console.log("data "+response)
                    if(msg.status == "success"){
                        alert("redirecting page ...")
                    }
                },
                error:function(msg){
                    console.log("response error")
                },
                dataType: "json"
              });

        });


    
 });

// function validate_and_submit()
// {
    
   
//     var user = document.getElementById("username")
//     var sel = document.getElementById("colLister")
//     var pass = document.getElementById("password")
    
//     username=user.value 
//     college=$("#dropdownList option:selected").text()
//     password=pass.value
    
//     alert("Enter Valid data"+college)
//     alert(username+password+college)
//     //validation goes here
    
//     $.ajax({
//         type: "POST",
//         url: "/login",
//         data: {"username":user,"college":sel},
//         success: function(msg){
//             console.log("data "+response)
//         },
//         error:function(msg){
//             console.log("response error")
//         },
//         dataType: "json"
//       });
    
//     return false
// }