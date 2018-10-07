$(document).ready(function(){

    // jQuery methods go here...


    $("#login-submit").click(function(){
            username=$("#username").val()
            college=$("#coll_drop_down").val()         
            password=$("#password").val()

            $.ajax({
                type: "POST",
                url: "/login",
                data: JSON.stringify({"username":username,"college":college,"password":password}),
                success: function(msg){
                    
                    if(msg.status == 0){
                        
                        alert("redirecting page ...")
                        url="/dashboard/"+msg.collegeCode+"/"+parseInt(msg.userid)
                        
                        Cookies.set('userid', msg.userid);

                        Cookies.set('collegeCode', msg.collegeCode);
                        
                        console.log(msg.token)    
                        Cookies.set('token', msg.token);
                           
                        $(location).attr('href',url)
                    }
                    else{
                        alert("error in login data :"+msg.message)
                    }
                },
                error:function(msg){
                    console.log("response error")
                },
                dataType: "json"
              });

        });


    
 });
