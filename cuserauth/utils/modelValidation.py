from ..models import StudentInfo, Students
#StudentHeader = ['slno', 'rollno' , 'name', 'mother name', 'father name', 'email', 'father mail', 'phone', 'father phone']
StudentHeader = ['StudentRollNo', 'studentName', 'motherName', 'fatherName', 'email', 'fatherEmail', 'studentPhone', 'fatherPhone']
def check_students(excel, Course):
    header = [f.get_internal_type() for f in Students._meta.local_fields]
    stuInfoName = [f.name for f in StudentInfo._meta.local_fields]    
    stuName = [f.name for f in Students._meta.local_fields] 
    stuName = stuInfoName + stuName[1:]
    print(stuName)
    print(header)
    got_header = excel.columns.values.tolist()
    from django.apps import apps
    #Invoice = apps.get_model(app_label="cuserauth", model_name=stuName[0])
    c = getattr(StudentInfo, stuName[0])
    print(c.__init__(blank))
    if(got_header == stuInfoName):

        print("sucess")
    else:
        print("failed")
    
def check_cources(excel_File, model):
    if list(excel_File.dtypes) == ["int64", "O","O"]:
        print("sucess")
    else:
        print("Error")
        return
    courcelist = list(model.objects.values_list('courceName', 'courceDomain'))
    #print(courcelist)
    #print(excel.iloc[:,0:3].values.tolist())
    #data = list(excel.iloc[:,0:3])
    errorInfo = []
    itrator = 0
    val = [tuple(x) for x in excel_File.iloc[:,1:3].values.tolist()]
    for a in val:
        for  b in courcelist:
            if a == b:
                errorInfo.append(itrator)
                break              
        itrator += 1
    print(errorInfo)

    if (len(errorInfo) == 0):
        for a in val:   
            data = model.objects.get_or_create(courceName = a[0], courceDomain = a[1])
            print(data)
        print('updated sucessfully')
    else:
        print('All Cources already stored')