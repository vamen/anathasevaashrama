$(document).ready(function(){
    
    window.history.forward();
    
    var marks_table=$('#marks-table').DataTable();

    var attendance_table=$('#attendance-table').DataTable();

    $('#attendance-table tbody').on('click', 'tr', function() {
        console.log('API row values : ', attendance_table.row(this).data());
        subCode=attendance_table.row(this).data()["DT_RowId"]
        
        college_code=Cookies.get('collegeCode');
        userid=Cookies.get('userid');
        // token=Cookies.get("token")
       
        $.ajax({
            type: "GET",
            url: "/sectionHandler",

            data: JSON.stringify({"collegeCode":college_code,"userID":userid,"subCode":subCode}),
            success: function(msg){
                
                   console.log(msg) 
            },
            error:function(msg){
                console.log("response error")
            },
            dataType: "json"
          });
    })


})
