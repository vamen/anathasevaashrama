function register_attendance_table_click(datatable){
    datatable.on('click','tbody td button',function(){
            // console.log("button click");
            // console.log(datatable.id)
            // // this.parent.parent.id
            // // this.
            subCode=datatable.table().node().id.split("-")[1]
            var data=datatable.row($(this).closest('tr')).data()
            // var idx = datatable.cell('.selected', 0).index();
            // var data = datatable.row( idx.row ).data();
            secName=data[0]
            year=data[1]
            
            date=$("#datepick"+subCode+secName+year).find("input").val();
            from=$("#timepick1"+subCode+secName+year).find("input").val();
            to=$("#timepick2"+subCode+secName+year).find("input").val();
            console.log("date :"+"#datepick"+subCode+secName+year)
            console.log(date)
            if(data==""||from==""||to==""){
                    alert("please provide valid date or time")
                    return;
            }
            college_code=Cookies.get('collegeCode');
            userid=Cookies.get('userid');
            $.ajax({
                type: "POST",
                url: "/openAttendance",
    
                data: JSON.stringify({"collegeCode":college_code,"userID":userid,"subCode":subCode,"secName":secName,"year":year,"Date":date,"From":from,"To":to}),
                success: function(msg){
                    
                   console.log(msg)    
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
      
       row+="<tr><td>"+secName+
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


function  update_attendenc_display(temp_data){
    
    
    $("#attendance-content-body").empty()

    sectionHandler
    for(i=0;i<temp_data.length;i++){
        console.log(temp_data)
        subCode=temp_data[i]['subCode']
        subName=temp_data[i]['subName']
        

        child1=$("<span>",{id:subCode,"class":"sub-heading"}).text(subCode+" | "+subName)
        child2=$("<div>",{id:"attendance-info-"+subCode}).text("Loading ...")

        attendance=$("<div>",{"class":"bar attendance","data-toggle":"collapse","data-target":"#attendance-info-"+subCode})
        attendance.append(child1)
        
        
        attendance=$("<div>",{"class":"subject-bar-wrapper"}).append(attendance)
        attendance.append(child2)
        
        $("#attendance-content-body").append(attendance)
        
        
        table="<table id=\"table-"+subCode+"\"><thead><tr><th>Section </th><th>Year </th>\
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
                $(this).datetimepicker({format: 'DD-MM-YY'});
            });

            $(".timepick").each(function(){
                
                $(this).datetimepicker({
                    format: 'HH:mm'
                });
            });

            
       });

    }
    



    





}

$(document).ready(function(){
    
    window.history.forward();
    $("#datepicker").datetimepicker();
    // var marks_table=$('#marks-table').DataTable();

    var attendance_table=$('#attendance-table').DataTable({
        searching: false,
        paging: false
    });

    college_code=Cookies.get('collegeCode');
    userid=Cookies.get('userid');

    temp_data=[{'subCode': '501', 'subName': 'ADA', 'sections': [{'subYear': 1, 'secName': 'A', 'year': 1},{'subYear': 1, 'secName': 'A', 'year': 2}]}, {'subCode': '502', 'subName': 'OS', 'sections': [{'subYear': 2, 'secName': 'A', 'year': 2}]}]
    console.log(temp_data.length)
    

    $("#attendance").click(function(){
        console.log("clicked")
        $.ajax({
            type: "POST",
            url: "/subjectHandler",

            data: JSON.stringify({"collegeCode":college_code,"userID":userid}),
            success: function(msg){
                console.log(msg)    
                update_attendenc_display(temp_data);


            },
            error:function(msg){
                console.log("response error")
            },
            dataType: "json"
          });

        
    })

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

    $("#attendance").trigger("click");

})
