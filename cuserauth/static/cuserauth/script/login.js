$(document).ready(function(){

    // jQuery methods go here...
    $("#login-submit").click(function(){
            $("#Lerror").hide()
            $("#UNerror").hide()
            $("#Perror").hide()
            username=$("#username").val()
            college=$("#coll_drop_down").val()         
            password=$("#password").val()
            $("#u").value = "asd"
            var csrftoken = Cookies.get('csrftoken');
            
            if(college == null)
            {
                $("#Lerror").show()
                //document.error.value = "Select Option";
                //alert("Select Option")
                return
            }   
            if(username.length == 0)
            {
                $("#UNerror").show()
                //alert("Enter Username")
                //console.log("error")
                return
            }
            if(password.length == 0){
                $("#Perror").show()
                //alert("Enter Password")
                return
            }
            console.log(username.length)
            console.log(window.CSRF_TOKEN) 
            //alert(username+":::"+college)
           function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
                    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
            }
            
            $.ajaxSetup({
                beforeSend: function(xhr, settings) {
                    if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
                        xhr.setRequestHeader("X-CSRFToken", csrftoken);
                    }
                }
            
            });
            $.ajax({
                type: "POST",
                url: "/login",
                data: JSON.stringify({"username":username,"college":college,"password":password, csrfmiddlewaretoken: window.CSRF_TOKEN}),
                
                success: function(msg){
                    
                    if(msg.status == 0){
                        console.log(msg)
                        //alert("redirecting page ...")
                        url="/dashboard/"+msg.collegeCode+"/"+parseInt(msg.userid)
                        $(location).attr('href',url)
                        
                        Cookies.set('userid', msg.userid);		
		
                        Cookies.set('collegeCode', msg.collegeCode);		
                                
                        console.log(msg.token)    		
                        Cookies.set('token', msg.token);

                    }
                    else{
                        $("#Perror").show()
                        $("#Perror").text("Invalid Username or password")
                        //alert("Invalid Username or password")
                    }
                },
                error:function(msg){
                    console.log("response error")
                },
                dataType: "json"
              });
			  

        });

	$(".glyphicon-eye-open").on("click", function() {
	$(this).toggleClass("glyphicon-eye-close");
	var type = $("#password").attr("type");
	if (type == "text"){ 
		$("#password").prop('type','password');}
	else{ 
		$("#password").prop('type','text'); }
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