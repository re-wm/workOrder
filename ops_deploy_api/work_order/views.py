from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
# from django.contrib.auth.decorators import login_required

from django.db import connection,transaction
cursor = connection.cursor()
# cursor.execute("select * from app01_userinfo")
# cursor.execute("update * from app01_userinfo")
# cursor.execute("delete * from app01_userinfo")
##一条一条取数据
# row = cursor.fetchone()
##取出所有数据，以元组的形式返回
# cursor.fetchall()
# connection.close()

def my_login_required(func):
    def check_login(request):
        if request.session.has_key('user'):
            return func(request)
        else:
            return redirect('/login/')
    return check_login

def login(request):
    if request.method == 'GET':
        return render(request,'login.html')
    else:
        user = request.POST.get('username')
        pwd = request.POST.get('password')
        if user in ('wood','alin','stone','lisi','michael'):
            # sql = "select is_admin from work_order_operator where name = '%s'" %(user)
            sql = "select passwd from work_order_operator where name = '%s'" %(user)
            cursor.execute(sql)
            pa = cursor.fetchone()
            if pa[0] == pwd :
                # 管理员登录成功
                request.session['user'] = user
                return redirect('/index2/')
        else:
            # 非管理员登录或用户登录失败
            sql2 = "select username from work_order_user"
            cursor.execute(sql2)
            # print('usrename:',cursor.fetchall(),type(cursor.fetchall()))
            invalid_name = cursor.fetchall()
            li = []
            for i in invalid_name:
                li.append(i[0])
            # print(li)
            if user in li:
                sql = "select password from work_order_user where username = '%s'" %(user)
                cursor.execute(sql)
                pa = cursor.fetchone()
                if pa[0] == pwd:
                # 普通用户登录成功
                    request.session['user'] = user
                    return redirect('/index/')
            else:
                # 用户登录失败
                return render(request,'login.html',{'msg':'登录失败 : {用户名或密码错误......}'})

@my_login_required
def index(request):
    print(request.method)
    if request.method == 'GET':
        return render(request, 'index.html', {'rep': '>>请选择一项进行查询：目前空空如也......<<'})
    else:
        order = request.POST.get('order')
        username = request.POST.get('username')
        company = request.POST.get('company')
        group = request.POST.get('group')
        print(order,type(order),username,type(username),company,type(company),group,type(group))
        if group != '':
            sql = "select * from  work_order_group where groupname = '%s'" %(group)
            cursor.execute(sql)
            group_l = cursor.fetchall()
            return render(request, 'index.html', {'rep_group': group,'group_l':group_l})
        elif company != '':
            sql = "select * from  work_order_company where c_name = '%s'" %(company)
            cursor.execute(sql)
            company_l = cursor.fetchall()
            return render(request, 'index.html', {'rep_company': company,'company_l':company_l})
        elif username != '':
            sql = "select * from  work_order_user where username = '%s'" %(username)
            cursor.execute(sql)
            user_l = cursor.fetchall()
            print(user_l,type(user_l))
            lu2 = []
            for user in user_l:
                lu = list(user)
                sql2 = "select groupname from  work_order_group where id = %s" %(lu[-1])
                cursor.execute(sql2)
                lu[-1] = cursor.fetchone()[0]
                # print(lu,type(lu))
                lu2.append(tuple(lu))
            # print(lu2)
            # print(username)
            return render(request, 'index.html', {'rep_username': username,'user_l':lu2})
        elif order != '':
            order_l = []
            sql = "select id,title,release_addr,release_content,release_attention,remark,status,is_update_db,create_time,end_time,ops_id,order_user_id from work_order_workorder where id = %s" %(int(order))
            cursor.execute(sql)
            onesql = cursor.fetchall()

            sql2 = "select company_id from work_order_workorder_company where workorder_id = %s" %(order)
            cursor.execute(sql2)
            twosql =cursor.fetchone()
            sql3 = "select c_name from work_order_company where id = %s" %(twosql[0])
            cursor.execute(sql3)
            threesql = cursor.fetchone()
            for a in onesql:
                la = list(a)
                la.append(threesql[0])
            order_l.append(tuple(la))
            return render(request,'index.html',{'rep_order':order,'order_l':order_l})

        elif group == '' and company == '' and username == '' and order == '':
            return render(request,'index.html',{'rep':'>>请选择一项进行查询：目前空空如也......<<'})

@my_login_required
def index2(request):
    # my = request.session['user']
    # print(my,type(my))
    if request.method == 'GET':
        return render(request, 'index2.html', {'rep': '>>请选择一项进行查询：目前空空如也......<<'})
    else:
        order = request.POST.get('order')
        username = request.POST.get('username')
        company = request.POST.get('company')
        group = request.POST.get('group')
        print(order,type(order),username,type(username),company,type(company),group,type(group))
        if group != '':
            sql = "select * from  work_order_group where groupname = '%s'" %(group)
            cursor.execute(sql)
            group_l = cursor.fetchall()
            return render(request, 'index2.html', {'rep_group': group,'group_l':group_l})
        elif company != '':
            sql = "select * from  work_order_company where c_name = '%s'" %(company)
            cursor.execute(sql)
            company_l = cursor.fetchall()
            return render(request, 'index2.html', {'rep_company': company,'company_l':company_l})
        elif username != '':
            sql = "select * from  work_order_user where username = '%s'" %(username)
            cursor.execute(sql)
            user_l = cursor.fetchall()
            print(user_l,type(user_l))
            lu2 = []
            for user in user_l:
                lu = list(user)
                sql2 = "select groupname from  work_order_group where id = %s" %(lu[-1])
                cursor.execute(sql2)
                lu[-1] = cursor.fetchone()[0]
                # print(lu,type(lu))
                lu2.append(tuple(lu))
            # print(lu2)
            # print(username)
            return render(request, 'index2.html', {'rep_username': username,'user_l':lu2})
        elif order != '':
            order_l = []
            sql = "select id,title,release_addr,release_content,release_attention,remark,status,is_update_db,create_time,end_time,ops_id,order_user_id from work_order_workorder where id = %s" %(int(order))
            cursor.execute(sql)
            onesql = cursor.fetchall()

            sql2 = "select company_id from work_order_workorder_company where workorder_id = %s" %(order)
            cursor.execute(sql2)
            twosql =cursor.fetchone()
            sql3 = "select c_name from work_order_company where id = %s" %(twosql[0])
            cursor.execute(sql3)
            threesql = cursor.fetchone()
            for a in onesql:
                la = list(a)
                la.append(threesql[0])
            order_l.append(tuple(la))
            return render(request,'index2.html',{'rep_order':order,'order_l':order_l})

        elif group == '' and company == '' and username == '' and order == '':
            return render(request,'index2.html',{'rep':'>>请选择一项进行查询：目前空空如也......<<'})

# 登录的普通用户处理的全部工单
def sub_order(request):
    sub_name = request.session['user']
    print(sub_name,type(sub_name))
    sql = "select id from work_order_user where username = '%s'" %(sub_name)
    cursor.execute(sql)
    na_id = cursor.fetchone()

    sql2 = "select id,title,release_addr,release_content,release_attention,remark,status,is_update_db,create_time,end_time,ops_id from work_order_workorder where order_user_id = %s" %(na_id[0])
    cursor.execute(sql2)
    sub_order_list = cursor.fetchall()
    sub_order_l = []
    for i in sub_order_list:
        ll = list(i)
        sql3 = "select name from work_order_operator where id = %s" %(ll[-1])
        cursor.execute(sql3)
        s3 = cursor.fetchone()[0]
        ll[-1] = s3
        sql4 = "select company_id from work_order_workorder_company where workorder_id = %s" %(ll[0])
        cursor.execute(sql4)
        s4 = cursor.fetchone()[0]
        sql5 = "select c_name from work_order_company where id = %s" %(s4)
        cursor.execute(sql5)
        s5_com_name = cursor.fetchone()[0]
        ll.append(s5_com_name)
        sub_order_l.append(tuple(ll))
    return render(request,'sub_order.html',{'sub_name':sub_name,'sub_order_l':sub_order_l})

# 普通用户未处理的工单
def no_order_sub(request):
    sub_name = request.session['user']
    sql = "select id from work_order_user where username = '%s'" %(sub_name)
    cursor.execute(sql)
    sub_id = cursor.fetchone()

    sql2 = "select id,title,release_addr,release_content,release_attention,remark,status,is_update_db,create_time,end_time,ops_id from work_order_workorder where order_user_id = %s" %(sub_id[0])
    cursor.execute(sql2)
    sub_order_list = cursor.fetchall()
    sub_order_l = []
    for i in sub_order_list:
        ll = list(i)
        if str(ll[9]) == '2200-01-01 00:00:00':
            # print('yes')
            sql3 = "select name from work_order_operator where id = %s" %(ll[-1])
            cursor.execute(sql3)
            s3 = cursor.fetchone()[0]
            ll[-1] = s3
            sql4 = "select company_id from work_order_workorder_company where workorder_id = %s" %(ll[0])
            cursor.execute(sql4)
            s4 = cursor.fetchone()[0]
            sql5 = "select c_name from work_order_company where id = %s" %(s4)
            cursor.execute(sql5)
            s5_com_name = cursor.fetchone()[0]
            ll.append(s5_com_name)
            sub_order_l.append(tuple(ll))
    return render(request,'no_order_sub.html',{'sub_name':sub_name,'sub_order_l':sub_order_l})

# 普通用户已经处理的工单
def yes_order_sub(request):
    sub_name = request.session['user']
    sql = "select id from work_order_user where username = '%s'" %(sub_name)
    cursor.execute(sql)
    sub_id = cursor.fetchone()

    sql2 = "select id,title,release_addr,release_content,release_attention,remark,status,is_update_db,create_time,end_time,ops_id from work_order_workorder where order_user_id = %s" %(sub_id[0])
    cursor.execute(sql2)
    sub_order_list = cursor.fetchall()
    sub_order_l = []
    for i in sub_order_list:
        ll = list(i)
        if str(ll[9]) != '2200-01-01 00:00:00':
            # print('yes')
            sql3 = "select name from work_order_operator where id = %s" %(ll[-1])
            cursor.execute(sql3)
            s3 = cursor.fetchone()[0]
            ll[-1] = s3
            sql4 = "select company_id from work_order_workorder_company where workorder_id = %s" %(ll[0])
            cursor.execute(sql4)
            s4 = cursor.fetchone()[0]
            sql5 = "select c_name from work_order_company where id = %s" %(s4)
            cursor.execute(sql5)
            s5_com_name = cursor.fetchone()[0]
            ll.append(s5_com_name)
            sub_order_l.append(tuple(ll))
    return render(request,'yes_order_sub.html',{'sub_name':sub_name,'sub_order_l':sub_order_l})

# 登录的运维用户处理的全部工单
def ops_order(request):
    # nani = request.COOKIES
    # print(nani)
    ops_name = request.session['user']
    sql = "select id from work_order_operator where name = '%s'" %(ops_name)
    cursor.execute(sql)
    na_id = cursor.fetchone()

    sql2 = "select id,title,release_addr,release_content,release_attention,remark,status,is_update_db,create_time,end_time,order_user_id from work_order_workorder where ops_id = %s" %(na_id[0])
    cursor.execute(sql2)
    ops_order_list = cursor.fetchall()
    ops_order_l = []
    for i in ops_order_list:
        ll = list(i)
        sql3 = "select username from work_order_user where id = %s" %(ll[-1])
        cursor.execute(sql3)
        s3 = cursor.fetchone()[0]
        ll[-1] = s3
        # print('end_time',ll[9],type(ll[9]))
        # if str(ll[9]) == '2200-01-01 00:00:00':
        #     print('yes')
        sql4 = "select company_id from work_order_workorder_company where workorder_id = %s" %(ll[0])
        cursor.execute(sql4)
        s4 = cursor.fetchone()[0]
        sql5 = "select c_name from work_order_company where id = %s" %(s4)
        cursor.execute(sql5)
        s5_com_name = cursor.fetchone()[0]
        ll.append(s5_com_name)
        ops_order_l.append(tuple(ll))
    return render(request,'ops_order.html',{'ops_name':ops_name,'ops_order_l':ops_order_l})

# 运维用户未处理的工单
def no_order_ops(request):
    # nani = request.COOKIES
    # print(nani)
    ops_name = request.session['user']
    sql = "select id from work_order_operator where name = '%s'" %(ops_name)
    cursor.execute(sql)
    na_id = cursor.fetchone()

    sql2 = "select id,title,release_addr,release_content,release_attention,remark,status,is_update_db,create_time,end_time,order_user_id from work_order_workorder where ops_id = %s" %(na_id[0])
    cursor.execute(sql2)
    ops_order_list = cursor.fetchall()
    ops_order_l = []
    for i in ops_order_list:
        ll = list(i)
        if str(ll[9]) == '2200-01-01 00:00:00':
            # print('yes')
            sql3 = "select username from work_order_user where id = %s" %(ll[-1])
            cursor.execute(sql3)
            s3 = cursor.fetchone()[0]
            ll[-1] = s3
            sql4 = "select company_id from work_order_workorder_company where workorder_id = %s" %(ll[0])
            cursor.execute(sql4)
            s4 = cursor.fetchone()[0]
            sql5 = "select c_name from work_order_company where id = %s" %(s4)
            cursor.execute(sql5)
            s5_com_name = cursor.fetchone()[0]
            ll.append(s5_com_name)
            ops_order_l.append(tuple(ll))
    return render(request,'no_order_ops.html',{'ops_name':ops_name,'ops_order_l':ops_order_l})

# 运维用户已经处理的工单
def yes_order_ops(request):
    ops_name = request.session['user']
    sql = "select id from work_order_operator where name = '%s'" %(ops_name)
    cursor.execute(sql)
    na_id = cursor.fetchone()

    sql2 = "select id,title,release_addr,release_content,release_attention,remark,status,is_update_db,create_time,end_time,order_user_id from work_order_workorder where ops_id = %s" %(na_id[0])
    cursor.execute(sql2)
    ops_order_list = cursor.fetchall()
    ops_order_l = []
    for i in ops_order_list:
        ll = list(i)
        if str(ll[9]) != '2200-01-01 00:00:00':
            # print('yes')
            sql3 = "select username from work_order_user where id = %s" %(ll[-1])
            cursor.execute(sql3)
            s3 = cursor.fetchone()[0]
            ll[-1] = s3
            sql4 = "select company_id from work_order_workorder_company where workorder_id = %s" %(ll[0])
            cursor.execute(sql4)
            s4 = cursor.fetchone()[0]
            sql5 = "select c_name from work_order_company where id = %s" %(s4)
            cursor.execute(sql5)
            s5_com_name = cursor.fetchone()[0]
            ll.append(s5_com_name)
            ops_order_l.append(tuple(ll))
    return render(request,'yes_order_ops.html',{'ops_name':ops_name,'ops_order_l':ops_order_l})

def order_list(request):
    from collections import OrderedDict
    if request.method == 'GET':
        sql = "select id,title,release_addr,release_content,release_attention,remark,status,is_update_db,create_time,end_time,ops_id,order_user_id from work_order_workorder"
        cursor.execute(sql)
        order_list = cursor.fetchall()
        # print(order_list,type(order_list))
        # print(order_list[0],list(order_list[0]),type(list(order_list[0])))
        li_order_list = []
        for i in order_list:
            li = list(i)
            sql_ops = "select name from work_order_operator where id = %s" %(i[10])
            sql_user = "select username from work_order_user where id = %s" %(i[11])
            cursor.execute(sql_ops)
            ops_name = cursor.fetchone()
            cursor.execute(sql_user)
            user_name = cursor.fetchone()

            print(li,type(li))
            print(li[0],type(li[0]))
            sql_com_id = "select company_id from work_order_workorder_company where workorder_id = %s" %(li[0])
            cursor.execute(sql_com_id)
            com_id = cursor.fetchone()
            print('com_id',com_id,type(com_id))
            sql_com_name = "select c_name from work_order_company where id = %s" %(com_id[0])
            cursor.execute(sql_com_name)
            com_name = cursor.fetchone()
            print('com_name',com_name,type(com_name))

            li[10] = ops_name[0]
            li[11] = user_name[0]
            # li[12] = com_name[0]    #index out of range
            li.append(com_name[0])
            li_order_list.append(tuple(li))
        print(li,type(li))
        print(li_order_list,type(li_order_list))
        di = OrderedDict({})
        for i,element in enumerate(li_order_list):
            di[i+1] = element
        print(di,type(di))

        # dic = OrderedDict({})
        # for k,v in di.items():
            # print('工单人：',v[10],type(v[10]))
            # print('用户：',v[11],type(v[11]))
            # sql_ops = "select name from work_order_operator where id = %s" %(v[10])
            # sql_user = "select username from work_order_user where id = %s" %(v[11])
            # cursor.execute(sql_ops)
            # ops_name = cursor.fetchone()
            # cursor.execute(sql_user)
            # user_name = cursor.fetchone()
            # print(ops_name,type(ops_name),ops_name[0],type(ops_name[0]))
            # print(user_name,type(user_name),user_name[0],type(user_name[0]))

        sql2 = "select id from work_order_operator"
        cursor.execute(sql2)
        ops_id_list = cursor.fetchall()
        print('qw',ops_id_list,type(ops_id_list))

        sql3 = "select id from work_order_user"
        cursor.execute(sql3)
        order_u_id_list = cursor.fetchall()
        print('wq',order_u_id_list,type(order_u_id_list))

        sql4 = "select id from work_order_company"
        cursor.execute(sql4)
        company_id_list = cursor.fetchall()
        print('ww',company_id_list,type(company_id_list))
        return render(request, 'order_list.html', {"order_list": di,"ops_id_list":ops_id_list,"order_u_id_list":order_u_id_list,"company_id_list":company_id_list})

def add_order(request):
    if request.method == 'GET':
        return render(request, 'order_list.html')
    else:
        title = request.POST.get('title')
        address = request.POST.get('address')
        content = request.POST.get('content')
        attention = request.POST.get('attention')
        remark = request.POST.get('remark')
        ostatus = int(request.POST.get('ostatus'))
        is_up_db = int(request.POST.get('is_up_db'))
        create_t = request.POST.get('create_t')
        end_t = '2200-01-01T00:00:00'
        ops_id = int(request.POST.get('ops_id'))
        order_u_id = int(request.POST.get('order_u_id'))
        company_id = int(request.POST.get('company_id'))
        print(title,type(title),address,type(address),content,type(content),attention,type(attention),remark,type(remark),ostatus,type(ostatus),is_up_db,type(is_up_db),create_t,type(create_t),end_t,type(end_t),ops_id,type(ops_id),order_u_id,type(order_u_id),company_id,type(company_id))
        sql = "insert into work_order_workorder(title,release_addr,release_content,release_attention,remark,status,is_update_db,create_time,end_time,ops_id,order_user_id) values('%s','%s','%s','%s','%s',%s,%s,'%s','%s',%s,%s)" %(title,address,content,attention,remark,ostatus,is_up_db,create_t,end_t,ops_id,order_u_id)
        cursor.execute(sql)

        sql2 = "select id from work_order_workorder where title = '%s'" %(title)
        cursor.execute(sql2)
        # dd = cursor.fetchone()
        w_o_id = int(cursor.fetchone()[0])
        print('w_o_id',w_o_id)

        sql3 = "insert into work_order_workorder_company(workorder_id,company_id) values('%s','%s')" %(w_o_id,company_id)
        cursor.execute(sql3)

        return redirect('/order_list/')

def delete_order(request):
    if request.method == 'POST':
        oid = request.POST.get('oid')
        print(oid,type(oid))
        oid = int(oid)
        sql = "delete from work_order_workorder_company where workorder_id = %s" %(oid)
        sql2 = "delete from work_order_workorder where id = %s" %oid
        try:
            with transaction.atomic():
                cursor.execute(sql)
                cursor.execute(sql2)
        except Exception as e:
            return JsonResponse({'statuscode':'409'})
        else:
            # cursor.close()
            # connection.close()
            ret = {"rey":"success"}
            return JsonResponse(ret)

def edit_order(request):
    if request.method == 'POST':
        oid = request.POST.get('oid')
        title = request.POST.get('title')
        addr = request.POST.get('addr')
        content = request.POST.get('content')
        attention = request.POST.get('attention')
        remark = request.POST.get('remark')
        status = int(request.POST.get('status'))
        is_up_db = int(request.POST.get('is_up_db'))
        create_ti = request.POST.get('create_ti')
        end_ti = request.POST.get('end_ti')
        # print(create_ti,type(create_ti))
        # print(end_ti,type(end_ti))
        company_name = request.POST.get('company_name')
        sql3 = "select id from  work_order_company where c_name = '%s'" %(company_name)
        cursor.execute(sql3)
        company_id = cursor.fetchone()[0]
        sql4 = "update work_order_workorder_company set company_id = %s where workorder_id = %s" %(company_id,oid)
        cursor.execute(sql4)

        ops_id_name = request.POST.get('ops_id')
        sql = "select id from work_order_operator where name = '%s'" %(ops_id_name)
        cursor.execute(sql)
        ops_id2 = cursor.fetchone()
        print(ops_id2,type(ops_id2))
        print(ops_id2[0],type(ops_id2[0]))
        ops_id = int(ops_id2[0])

        order_u_id_name = request.POST.get('order_u_id')
        sql2 = "select id from work_order_user where username = '%s'" %(order_u_id_name)
        cursor.execute(sql2)
        order_u_id2 = cursor.fetchone()
        print(order_u_id2,type(order_u_id2))
        print(order_u_id2[0],type(order_u_id2[0]))
        order_u_id = int(order_u_id2[0])

        sql = "update work_order_workorder set title='%s',release_addr='%s',release_content='%s',release_attention='%s',remark='%s',status='%s',is_update_db='%s',create_time='%s',end_time='%s',ops_id='%s',order_user_id='%s' where id = %s" %(title,addr,content,attention,remark,status,is_up_db,create_ti,end_ti,ops_id,order_u_id,oid)
        cursor.execute(sql)
        ret = {"rey":"success"}
        return JsonResponse(ret)

def user_list(request):
    from collections import OrderedDict
    if request.method == 'GET':
        sql = "select id,username,nickname,mailbox,password,status,group_id from work_order_user"
        cursor.execute(sql)
        user_list = cursor.fetchall()
        di = OrderedDict({})
        for i, element in enumerate(user_list):
            di[i + 1] = element
        print(di, type(di))

        sql2 = "select id from work_order_group"
        cursor.execute(sql2)
        u_group_list = cursor.fetchall()
        print(u_group_list,type(u_group_list))
        return render(request, 'user_list.html', {"user_list": di,"u_group_list":u_group_list})

def add_user(request):
    if request.method == 'GET':
        return render(request, 'user_list.html')
    else:
        uname = request.POST.get('uname')
        upassword = request.POST.get('upassword')
        unick = request.POST.get('unick')
        umailbox = request.POST.get('umailbox')
        ustatus = int(request.POST.get('ustatus'))
        u_group = int(request.POST.get('u_group'))
        print(uname,type(uname),upassword,type(upassword),unick,type(unick),umailbox,type(umailbox),ustatus,type(ustatus),u_group,type(u_group))
        sql = "insert into work_order_user(username,nickname,mailbox,password,status,group_id) values('%s','%s','%s','%s',%s,%s)" %(uname,unick,umailbox,upassword,ustatus,u_group)
        cursor.execute(sql)
        return redirect('/user_list/')

def edit_user(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        uname = request.POST.get('uname')
        upassword = request.POST.get('upass')
        unick = request.POST.get('unick')
        umailbox = request.POST.get('umail')
        ustatus = int(request.POST.get('ustatus'))
        u_group = int(request.POST.get('u_group'))
        sql = "update work_order_user set username='%s',nickname='%s',mailbox='%s',password='%s',status='%s',group_id='%s' where id = %s" %(uname,unick,umailbox,upassword,ustatus,u_group,uid)
        cursor.execute(sql)
        ret = {"rey":"success"}
        return JsonResponse(ret)

def delete_user(request):
    if request.method == 'POST':
        uid = request.POST.get('uid')
        print(uid,type(uid))
        uid = int(uid)
        sql = "delete from work_order_user where id = %s" %uid
        try:
            with transaction.atomic():
                cursor.execute(sql)
        except Exception as e:
            return JsonResponse({'statuscode':'409'})
        else:
            # cursor.close()
            # connection.close()
            ret = {"rey":"success"}
            return JsonResponse(ret)

def group_list(request):
    from collections import OrderedDict
    if request.method == 'GET':
        sql = "select id,groupname,status from work_order_group"
        cursor.execute(sql)
        group_list = cursor.fetchall()
        sql2 = "select count(1) from work_order_group"
        cursor.execute(sql2)
        group_list_count = cursor.fetchall()
        group_list_count = group_list_count[0][0]

        di = OrderedDict({})
        for i,element in enumerate(group_list):
            di[i+1] = element
        print(di,type(di))
        return render(request, 'group_list.html', {"group_list": di})

def add_group(request):
    if request.method == 'GET':
        return render(request, 'group_list.html')
    else:
        gname = request.POST.get('gname')
        gstatus = int(request.POST.get('gstatus'))
        sql = "insert into work_order_group(groupname,status) values('%s',%s)" %(gname,gstatus)
        cursor.execute(sql)
        # cursor.close()
        # connection.close()
        return redirect('/group_list/')

def delete_group(request):
    if request.method == 'POST':
        gid = request.POST.get('gid')
        print(gid,type(gid))
        gid = int(gid)
        sql = "delete from work_order_group where id=%s" %gid
        try:
            with transaction.atomic():
                cursor.execute(sql)
        except Exception as e:
            return JsonResponse({'statuscode':'409'})
        else:
            # cursor.close()
            # connection.close()
            ret = {"rey":"success"}
            return JsonResponse(ret)

def edit_group(request):
    if request.method == 'POST':
        gid = request.POST.get('gid')
        gname = request.POST.get('gname')
        gstatus = request.POST.get('gstatus')
        print(gid,type(gid),gname,type(gname),gstatus,type(gstatus))
        sql = "update work_order_group set groupname='%s',status='%s' where id='%s'" %(gname,int(gstatus),int(gid))
        cursor.execute(sql)
        # cursor.close()
        # connection.close()
        ret = {"rey":"success"}
        return JsonResponse(ret)

def company_list(request):
    from collections import OrderedDict
    if request.method == 'GET':
        sql = "select id,c_name,c_code,status from work_order_company"
        cursor.execute(sql)
        company_list = cursor.fetchall()
        sql2 = "select count(1) from work_order_company"
        cursor.execute(sql2)
        company_list_count = cursor.fetchall()
        company_list_count = company_list_count[0][0]

        di = OrderedDict({})
        for i,element in enumerate(company_list):
            di[i+1] = element
        print(di,type(di))
        # print(di[1])

        # result = []
        # for row in company_list:
        #     objDict = {}
        #     for index, value in enumerate(row):
        #         objDict[row[index]] = value
        #     result.append(objDict)
        # print(result)
        # cursor.close()
        # connection.close()
        # print(company_list,type(company_list))
        # print(company_list_count,type(company_list_count),company_list_count[0][0],type(company_list_count[0][0]))
        # return render(request, 'company_list.html', {"company_list": company_list,"company_list_count": di})
        return render(request, 'company_list.html', {"company_list": di})

def add_company(request):
    if request.method == 'GET':
        return render(request, 'company_list.html')
    else:
        cname = request.POST.get('cname')
        ccode = request.POST.get('ccode')
        cstatus = int(request.POST.get('cstatus'))
        # print(cname, ccode, cstatus)
        # print(type(cname), type(ccode), type(cstatus))
        sql = "insert into work_order_company(c_name,c_code,status) values('%s','%s',%s)" %(cname,ccode,cstatus)
        cursor.execute(sql)
        # cursor.close()
        # connection.close()
        return redirect('/company_list/')

def delete_company(request):
    import json
    if request.method == 'POST':
        cid = request.POST.get('cid')
        # print(cid,type(cid))
        cid = int(cid)
        sql = "delete from work_order_company where id=%s " %cid
        try:
            with transaction.atomic():
                cursor.execute(sql)
        except Exception as e:
            return JsonResponse({'statuscode':'409'})
        else:
            # cursor.close()
            # connection.close()
            ret = {"rey":"success"}
            return JsonResponse(ret)

def edit_company(request):
    if request.method == 'POST':
        cid = request.POST.get('cid')
        cname = request.POST.get('cname')
        ccode = request.POST.get('ccode')
        cstatus = request.POST.get('cstatus')
        print(cid,type(cid),cname,type(cname),ccode,type(ccode),cstatus,type(cstatus))
        sql = "update work_order_company set c_name='%s',c_code='%s',status='%s' where id='%s'" %(cname,ccode,int(cstatus),int(cid))
        cursor.execute(sql)
        # cursor.close()
        # connection.close()
        ret = {"rey":"success"}
        return JsonResponse(ret)

# def ops_on_set(request):
#     return render(request,'ops_on.html')

def ops_on(request):
    if request.method == 'GET':
        return render(request,'ops_on.html')
    else:
        day_ops = request.POST.getlist('day_ops')
        night_ops = request.POST.getlist('night_ops')
        print(day_ops,type(day_ops))
        print(night_ops,type(night_ops))
        li = []
        for a in day_ops:
            # sq = "select onduty from work_order_operator where id = %s" %(a)
            # cursor.execute(sq)
            # t = cursor.fetchone()
            # if t[0] == 0:
            sql = "select name from work_order_operator where id = %s" %(a)
            cursor.execute(sql)
            tt = cursor.fetchone()
            li.append(tt)
                # sqlc = "update work_order_operator set onduty = 1 where id = %s" %(a)
                # cursor.execute(sqlc)
        print(li,type(li))
        for i in li:
            print(i[0],type(i[0]))
        li2 = []
        for b in night_ops:
            # sq2 = "select onduty from work_order_operator where id = %s" %(b)
            # cursor.execute(sq2)
            # tt = cursor.fetchone()
            # if tt[0] == 0:
            sql2 = "select name from work_order_operator where id = %s" %(b)
            cursor.execute(sql2)
            tt2 = cursor.fetchone()
            li2.append(tt2)
                # sqlc2 = "update work_order_operator set onduty = 1 where id = %s" %(b)
                # cursor.execute(sqlc2)
        print(li2,type(li2))
        for j in li2:
            print(j[0],type(j[0]))
        return render(request, 'index.html', {'li':li,'li2':li2})

def logout(request):
    try:
        del request.session['user']
    except KeyError:
        pass
    return redirect('/login/')



