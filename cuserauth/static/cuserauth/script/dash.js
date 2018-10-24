function update_attendance_modal(id,data,info){
    data=JSON.parse(data)
    subCode=info["subCode"]
    secName=info["secName"]
    date=info["Date"]
    from=info["From"]
    to=info["To"]

    console.log($("#"+subCode).text())
    subName=$("#"+subCode).text().split("|")[1]

    console.log(data)
    modal=$("#"+id).modal('show')
    modal.find(".modal-title").text("Mark attendance | "+subName+" ( Section : "+secName+")");
    modal_body=modal.find(".modal-body")
    table="<table id=\"attd-table\" class=\"table table-striped\"><thead><tr><th>Student Roll</th><th>Student Name</th><th><input  type=\"checkbox\" id=\"mark-all\"/> Mark all absent</th></tr></thead><tbody>"
    for(i=0;i<data.length;i++){
        table+="<tr><th>"+data[i]["studentID"]+"</th><th>"+data[i]["studentName"]+"</th><th><input class=\"mark\" name=\"mark\" type=\"checkbox\" id=\""+data[i]["studentID"]+"\"/></th></tr>"
    }
   table+="</tbody></table>";  
   modal_body.empty()
   modal_body.append("<span>date : "+date+" </span>")
   modal_body.append("<span>From : "+from+" </span>")
   modal_body.append("<span>To : "+to+" </span>") 
   modal_body.append(table)
    
    $("#mark-all").click(function(e){
        
        checkboxes = document.getElementsByName('mark');
        
        for(var i=0, n=checkboxes.length;i<n;i++) {
                checkboxes[i].checked = this.checked;
        }


    });

    $(".mark").change(function(){

        if(false == $(this).prop("checked")){ //if this item is unchecked
            $("#mark-all").prop('checked', false); //change "select all" checked status to false
        }
        //check "select all" if all checkbox items are checked
        
        if ($('.mark:checked').length == $('.mark').length ){
            
            $("#mark-all").prop('checked', true)
            
        }

    });

    $("#modal-submit-data").click(function(){
        
        console.log("cliecked on submit")       
        var mark_data=[]

        if ($('.mark:checked').length==0){
            status=0
        }else if(true==$("#mark-all").prop("checked")){

            status=2    
        }else{
            
            status=1
            console.log($('.mark:checked'))
            checkboxes = document.getElementsByName('mark');
            
            for(var i=0, n=checkboxes.length;i<n;i++) {
                if(checkboxes[i].checked == true){
                    mark_data.push(checkboxes[i].id)
                } 
            }
        }
        

        
        post_data={

            "status":status,
            "subCode":info["subCode"],
            "id":info["id"],
            "absenties":mark_data                
        }

        
         console.log(post_data)

        $.ajax({
                
            type: "POST",
                url: "/mark_attendance",
    
                data: JSON.stringify(post_data),
                success: function(msg){
                //    console.log(msg);   
                //    console.log($("#model1").find("h4.model-title"));
                   console.log(msg)
                    

                },
                error:function(msg){
                    console.log("response error")
                },
                dataType: "json"

            // 
        });

    });
}



function register_attendance_table_click(datatable){
    datatable.on('click','tbody td button',function(){
            // console.log("button click");
            // console.log(datatable.id)
            // // this.parent.parent.id
            // // this.

            
            subCode=datatable.table().node().id.split("-")[1]
            var data=datatable.row($(this).closest('tr')).data()
            var id=datatable.row($(this).closest('tr')).id().split("-")[1]
            // var idx = datatable.cell('.selected', 0).index();
            // var data = datatable.row( idx.row ).data();
            secName=data[0]
            year=data[1]
            
            date=$("#datepick"+subCode+secName+year).find("input").val();
            from=$("#timepick1"+subCode+secName+year).find("input").val();
            to=$("#timepick2"+subCode+secName+year).find("input").val();
            console.log("date :"+"#datepick"+subCode+secName+year)
            console.log(date)
            if(date==""||from==""||to==""){
                    alert("please provide valid date or time")
                    return;
            }
            college_code=Cookies.get('collegeCode');
            userid=Cookies.get('userid');
            post_data={"collegeCode":college_code,"userID":userid,"id":id,"subCode":subCode,"secName":secName,"year":year,"Date":date,"From":from,"To":to}
            $.ajax({
                type: "POST",
                url: "/openAttendance",
    
                data: JSON.stringify(post_data),
                success: function(msg){
                //    console.log(msg);   
                //    console.log($("#model1").find("h4.model-title"));
                   update_attendance_modal("modal1",msg,post_data);
                },
                error:function(msg){
                    console.log("response error")
                },
                dataType: "json"
              });


    });
}

function fill_data_table(subCode,data){

    console.log("filling row")
    console.log(data)
    date_elm=$("#datepicker").clone()
    time_elm1=$("#timepicker").clone()
    time_elm2=$("#timepicker").clone()
    


    date_elm=date_elm.css("display","");
    time_elm1=time_elm1.css("display","");
    time_elm2=time_elm2.css("display","");
    
    
    data_elm=date_elm.addClass("datepick");
    time_elm1=time_elm1.addClass("timepick");
    time_elm2=time_elm2.addClass("timepick");


    

    
    date_elm_html=date_elm.prop("outerHTML")
    
    console.log(date_elm)
    
    row=""        
    for(j=0;j<data.length;j++){
        
        secName=data[j]["secName"]
        year=data[j]["year"]
        data_elm=date_elm.attr("id","datepick"+subCode+secName+year);
        time_elm1=time_elm1.attr("id","timepick1"+subCode+secName+year);
        time_elm2=time_elm2.attr("id","timepick2"+subCode+secName+year);
   

      date_elm_html=date_elm.prop("outerHTML")
      time_elm1_html=time_elm1.prop("outerHTML")
      time_elm2_html=time_elm2.prop("outerHTML")
      
       row+="<tr id=\""+subCode+"-"+data[j]["id"]+"\"><td>"+secName+
       "</td><td>"+year+
       "</td><td>"+date_elm_html+
       "</td><td>"+time_elm1_html+
       "</td><td>"+time_elm2_html+
       "</td><td><button class=\"mark-btn btn\">Mark</button></td></tr>"     
        
      
       console.log("drawing row")
       
    //    datatable.row.add($(row)).draw()
       


    }

    return row
}


function clean_page_content(){

    console.log("cleaning")
    $("#content-body").empty()
    $("#content-header").text("")
}



function  update_attendenc_display(temp_data){
    
    
    $("#content-header").html("Attendance")


    for(i=0;i<temp_data.length;i++){
        console.log(temp_data)
        subCode=temp_data[i]['subCode']
        subName=temp_data[i]['subName']
        

        child1=$("<span>",{id:subCode,"class":"sub-heading"}).text(subCode+" | "+subName)
        child2=$("<div>",{id:"attendance-info-"+subCode})

        attendance=$("<div>",{"class":"bar attendance","data-toggle":"collapse","data-target":"#attendance-info-"+subCode})
        attendance.append(child1)
        
        
        attendance=$("<div>",{"class":"subject-bar-wrapper"}).append(attendance)
        attendance.append(child2)
        
        $("#content-body").append(attendance)
        
        
        table="<table class=\"table table-stripped\" id=\"table-"+subCode+"\"><thead><tr><th>Section </th><th>Year </th>\
        <th>Date</th><th>From</th><th>to</th><th>Mark</th></tr></thead><tbody>";

        
        table+=fill_data_table(subCode,temp_data[i]["sections"])
        table+="</tbody></table>"
        console.log(table)
        $("#attendance-info-"+subCode).append(table)
        subject_table=$("#table-"+subCode).DataTable({searching: false, paging: false, info: false});
        // console.log($("attendance-info"))
        
        console.log("hello")
        register_attendance_table_click(subject_table,subCode)
        $("#table-"+subCode).ready(function(){
            
            $(".datepick").each(function(){
                console.log("dedoed")
                $(this).datetimepicker({format: 'DD/MM/YYYY'});
            });

            $(".timepick").each(function(){
                
                $(this).datetimepicker({
                    format: 'HH:mm'
                });
            });

            
       });

    }
    


}




/////////////////////////////////////////////////////////////////////////////////


function update_marks_display(){
    $("#content-header").text("Marks");
    
}

////////////////////////////////////////////////////////////////////////////////

function update_notes_display(){
    $("#content-header").text("Notes");
    
}


///////////////////////////////////////////////////////////////////////////////

function update_assignment_display(){
    $("#content-header").text("Assignments");
    
}


///////////////////////////////////////////////////////////////////////////////
$(document).ready(function(){
    
    window.history.forward();
    // var marks_table=$('#marks-table').DataTable();



    college_code=Cookies.get('collegeCode');
    userid=Cookies.get('userid');

    // $("body").on('click','.datepick',function(){
    //     console.log(this)
        
    //     $(this).datetimepicker();


    // });

    


    $("#attendance").click(function(){
        if (document.getElementById("marks").classList.length >0)
            document.getElementById("marks").classList.remove('sidebar-selected-item');
        if (document.getElementById("notes").classList.length >0)
            document.getElementById("notes").classList.remove('sidebar-selected-item');
        if (document.getElementById("assignment").classList.length >0)
            document.getElementById("assignment").classList.remove('sidebar-selected-item');
        document.getElementById("attendance").classList.add('sidebar-selected-item');
    })

    $("#marks").click(function(){
        if (document.getElementById("attendance").classList.length >0)
            document.getElementById("attendance").classList.remove('sidebar-selected-item');
        if (document.getElementById("notes").classList.length >0)
            document.getElementById("notes").classList.remove('sidebar-selected-item');
        if (document.getElementById("assignment").classList.length >0)
            document.getElementById("assignment").classList.remove('sidebar-selected-item');
        document.getElementById("marks").classList.add('sidebar-selected-item');
    })

    $("#assignment").click(function(){
        if (document.getElementById("marks").classList.length >0)
            document.getElementById("marks").classList.remove('sidebar-selected-item');
        if (document.getElementById("notes").classList.length >0)
            document.getElementById("notes").classList.remove('sidebar-selected-item');
        if (document.getElementById("attendance").classList.length >0)
            document.getElementById("attendance").classList.remove('sidebar-selected-item');
        document.getElementById("assignment").classList.add('sidebar-selected-item');
    })

    $("#notes").click(function(){
        if (document.getElementById("marks").classList.length >0)
            document.getElementById("marks").classList.remove('sidebar-selected-item');
        if (document.getElementById("attendance").classList.length >0)
            document.getElementById("attendance").classList.remove('sidebar-selected-item');
        if (document.getElementById("assignment").classList.length >0)
            document.getElementById("assignment").classList.remove('sidebar-selected-item');
        document.getElementById("notes").classList.add('sidebar-selected-item');
    })

 
//////////////////////////////////

    temp_data=[{'subCode': '501', 'subName': 'ADA', 'sections': [{'subYear': 1, 'secName': 'A', 'year': 1},{'subYear': 1, 'secName': 'A', 'year': 2}]}, {'subCode': '502', 'subName': 'OS', 'sections': [{'subYear': 2, 'secName': 'A', 'year': 2}]}]
    console.log(temp_data.length)
    

    $("#attendance").click(function(){
        
        
        
        $.ajax({
            type: "POST",
            url: "/subject_handeled_info",

            data: JSON.stringify({"collegeCode":college_code,"userID":userid}),
            success: function(msg){
                console.log(msg)    
                clean_page_content()
                update_attendenc_display(msg);


            },
            error:function(msg){
                console.log("response error")
                clean_page_content()
                // update_attendenc_display(temp_data);
            },
            dataType: "json"
          });

        
    })

    
    
    $("#marks").click(function(){
        clean_page_content();
        update_marks_display();
    });


    $("#notes").click(function(){
        clean_page_content();
        update_notes_display();
    });

    $("#assignment").click(function(){
        clean_page_content();
        update_assignment_display();
    });


////////////////////////////////////////////////

    $("#attendance").trigger("click");


})

