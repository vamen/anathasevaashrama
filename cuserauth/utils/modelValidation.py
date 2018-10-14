StudentHeader = ['slno','name', 'class']
def check_students(excel, Course):
    print(excel.columns.values.tolist())
    print(StudentHeader)
    if(excel.columns.values.tolist() == StudentHeader):
        pass
    else:
        return
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