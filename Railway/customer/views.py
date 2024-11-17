import decimal

import cx_Oracle
from django.http import HttpResponse
from django.shortcuts import render, redirect, reverse
from django.db import connection
import hashlib

global is_logged_in
is_logged_in = 0


# Create your views here.
# request handler


def make_pw_hash(password):
    return hashlib.sha256(str.encode(password)).hexdigest()


def check_pw_hash(password, hash):
    if make_pw_hash(password) == hash:
        return True
    return False


def startpage(request):
    if request.session.get('is_logged_in') == "1":
        return redirect('/userhome')
    else:
        return render(request, 'startpage.html')


def userhome(request):
    if request.session.get('is_logged_in') != "1":
        return redirect('/startpage')
    else:
        fullname = request.session.get('first') + ' ' + request.session.get('last')
        return render(request, 'userhome.html',{'username': fullname})


def logout(request):
    if (request.session.get('is_logged_in') != "1"):
        print('You are not logged in yet. Please log in first.')
        msg = 'You are not logged in yet. Please log in first.'
        return redirect('/startpage', {"statusred": msg})  # if (request.GET.logged_out == '1'):
    else:
        request.session['is_logged_in'] = 0
        request.session.flush()
        print('You have successfully logged out')
        msg = 'You have successfully logged out'
        return redirect('/startpage', {"statusgreen": msg})


def login(request):
    # print('intologin')
    if request.method == "POST":
        # print("from log in")
        print(request.POST)
        if request.session.get('is_logged_in') == "1":
            print('already logged in')
            # redirect to home page of own
            msg = 'already logged in'
            return render(request, 'userhome.html', {"statusred": msg})

        mail = request.POST["email"]
        pas = request.POST["pass"]

        print(make_pw_hash(pas))

        cursor = connection.cursor()
        sql = "SELECT PASSWORD FROM ACCOUNTS WHERE EMAIL=%s;"
        cursor.execute(sql, [mail])
        result = cursor.fetchall()
        cursor.close()

        print(result)

        if (result):
            for r in result:
                hash = r[0]
            if (check_pw_hash(pas, hash)):

                is_logged_in = 1
                request.session['usermail'] = mail
                request.session['is_logged_in'] = "1"
                # user = authenticate(request, username=username, password=password)

                cursor1 = connection.cursor()
                sql1 = "SELECT FIRST_NAME,LAST_NAME,DOB,GENDER,ID_NUMBER,ADRESS,PHONE,USER_ID,PASSWORD FROM ACCOUNTS WHERE EMAIL=%s;"
                cursor1.execute(sql1, [mail])
                result1 = cursor1.fetchall()
                cursor1.close()
                print('printline1111111111111111111111111111')

                fullname = ""
                for r in result1:
                    # fullname=r[0]
                    request.session['first'] = r[0]
                    request.session['last'] = r[1]
                    request.session['dob'] = str(r[2])
                    request.session['gender'] = r[3]
                    request.session['nid'] = r[4]
                    request.session['address'] = r[5]
                    request.session['phone'] = r[6]
                    request.session['user_id'] = r[7]
                    request.session['password'] = r[8]
                fullname = request.session.get('first') + ' ' + request.session.get('last')
                request.session['fullname'] = fullname;

                print('successful login detected                1111')
                # return page to be redirected
                msg = 'Successfully logged in'
                return render(request, "userhome.html", {"statusgreen": msg})
            else:
                print(make_pw_hash(pas))
                print('wrong password detected              1111')
                msg = "Login Denied. Wrong Password."
                return render(request, "login.html", {"statusred": msg})
        else:
            print('invalid email detected               1111')
            msg = "Login Denied. Invalid E-mail."
            return render(request, "login.html", {"statusred": msg})
    else:
        if request.session.get('is_logged_in') == "1":
            print('already logged in')
            # redirect to home page of own
            msg = 'already logged in'
            return render(request, 'userhome.html', {"statusred": msg})
        else:
            return render(request, 'login.html')
        # if (request.GET.get('logged_out')):
        #     if (request.session.get('is_logged_in') != "1"):
        #         response = "You are not logged in yet. Please log in first."  # if (request.GET.logged_out == '1'):
        #     else:
        #         request.session['logged_in'] = 0
        #         request.session.flush()
        #         response = "You have successfully logged out."
        #         print('loged out')
        #     return render(request, 'login.html')
        # else:
        #     return render(request, 'login.html')


def signup(request):
    if request.session.get('is_logged_in') == "1":
        msg = 'already logged in. Logout first'
        return render(request, 'userhome.html', {"statusred": msg})
    if request.method == "POST":
        print(request.POST)
        mail = request.POST.get('email')
        ps = request.POST.get('password')
        first = request.POST.get('first')
        last = request.POST.get('last')
        contact = request.POST.get('contact')
        nid = request.POST.get('nid')
        gender = request.POST.get('gender')
        address = request.POST.get('adress')
        dob = request.POST.get('dob')

        print(ps)
        print('hhhhhhhhhhhhhhhhhhhhhhhhhhhh')

        cursor1 = connection.cursor()
        sql1 = "SELECT EMAIL FROM ACCOUNTS WHERE EMAIL=%s;"
        cursor1.execute(sql1, [mail])
        result1 = cursor1.fetchall()
        cursor1.close()

        if (result1):
            print('11111111111111111111111111111111111')
            msg = "This E-mail ID is already registered."
            return render(request, 'signup.html', {"statusred": msg})
        else:
            print('2222222222222222222222222222222222')
            cursor2 = connection.cursor()
            sql2 = "SELECT ID_NUMBER FROM ACCOUNTS WHERE ID_NUMBER=%s;"
            cursor2.execute(sql2, [nid])
            result2 = cursor2.fetchall()
            cursor2.close()

            if (result2):
                print('3333333333333333333')
                msg = "This NID number is already registered."
                return render(request, 'signup.html', {"statusred": msg})
            else:
                print('444444444444444444444444444444')
                cursor3 = connection.cursor()
                sql3 = "SELECT PHONE FROM ACCOUNTS WHERE PHONE='+880'||%s;"
                cursor3.execute(sql3, [contact])
                result3 = cursor3.fetchall()
                cursor3.close()

                if (result3):
                    print('5555555555555555555555555')
                    msg = "This contact number is already registered."
                    return render(request, 'signup.html', {"statusred": msg})
                else:
                    print('666666666666666666666')
                    print(ps)
                    pw_hash = make_pw_hash(ps)
                    print(pw_hash)
                    cursor = connection.cursor()
                    txt = cursor.var(cx_Oracle.STRING).var
                    cursor.callproc('agecheck',[dob,txt])
                    cursor.close()
                    print()


                    print(txt,type(txt))
                    txtm=str(txt.getvalue())
                    print(txtm)

                    if txtm =='not eignteen yet':

                        return render(request,'signup.html',{'statusred' : txtm})

                    cursor = connection.cursor()
                    sql = "INSERT INTO ACCOUNTS VALUES(NVL((SELECT MAX(USER_ID)+1 FROM ACCOUNTS),1),%s,%s,%s,%s,CONCAT('+880',%s),%s,%s,%s,TO_DATE(%s,'YYYY-MM-DD'));"
                    cursor.execute(sql, [first, last, pw_hash, mail, contact, nid, gender, address, dob])
                    # result = cursor.fetchall()
                    cursor.close()
                    msg = "Successfully Sign up completed"
                    return render(request, 'login.html', {"statusrgreen": msg})
                    # return render(request, 'login.html')
    return render(request, 'signup.html')


def search_trains(request):
    print('00000000000000000000000000000')
    print(request)
    print(request.method)
    if request.method == "POST":
        if request.session.get('is_logged_in') != "1":
            return redirect("/" + "?not_logged_in=" + str(0))

        fro = request.POST["from"]
        to = request.POST["to"]
        date = request.POST["journey_date"]
        print('checking search result,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,,, ', date)
        date = str(date)
        print(date, type(date))
        adult = request.POST["adult"]
        child = request.POST["child"]
        clas = request.POST["seat"]
        temp = int(child) + int(adult)

        print(fro)
        print(to)

        if temp > 4:
            return redirect("/" + "?max_seat_exceeded=1")
        request.session['adult'] = str(adult)
        request.session['child'] = str(child)
        request.session['total_seats'] = str(temp)
        request.session['doj'] = date
        request.session['class'] = clas
        request.session['from'] = fro
        request.session['to'] = to
        global details
        details = {'from': fro, 'to': to, 'date': date, 'adult': adult, 'child': child, 'class': clas}

        cursor0 = connection.cursor()
        sql0 = "SELECT TO_CHAR(SYSDATE,'YYYY-MM-DD') FROM DUAL;"
        cursor0.execute(sql0)
        result0 = cursor0.fetchall()
        cursor0.close()
        for re0 in result0:
            sdate = str(re0[0])

        print(sdate,type(sdate))
        if date == sdate:
            cursor = connection.cursor()
            sql = "SELECT TT1.TRAIN_ID,(SELECT TRAIN_NAME FROM TRAIN T1 WHERE T1.TRAIN_ID=TT1.TRAIN_ID) NAME1,TO_TIMESTAMP( concat(concat(TO_CHAR((SELECT SYSDATE FROM DUAL),'YYYY-MM-DD'),' '),TO_CHAR(TT1.DEPARTURE_TIME,'HH24:MI:SS')),'YYYY-MM-DD HH24:MI:SS') ,TO_CHAR(TT2.DEPARTURE_TIME,'HH24:MI:SS'),ROW_NUMBER() Over (ORDER BY TO_TIMESTAMP(TO_CHAR(TT1.DEPARTURE_TIME,'HH24:MI:SS'),'HH24:MI:SS')) As SN " \
                  "FROM TRAIN_TIMETABLE TT1,TRAIN_TIMETABLE TT2 " \
                  "WHERE (TT1.DIRECTION=TT2.DIRECTION ) AND TT1.STATION_ID=(SELECT STATION_ID FROM STATION WHERE STATION_NAME=%s)  AND TT2.STATION_ID=(SELECT STATION_ID FROM STATION WHERE STATION_NAME=%s)  AND (TT1.TRAIN_ID=TT2.TRAIN_ID) AND TT1.DEPARTURE_TIME<TT2.DEPARTURE_TIME AND TO_DATE(CONCAT(CONCAT(TO_CHAR(SYSDATE, 'YYYY-MM-DD'),' '),TO_CHAR(TT1.DEPARTURE_TIME,'HH24:MI:SS')),'YYYY-MM-DD HH24:MI:SS')>SYSDATE  " \
                  "ORDER BY TO_TIMESTAMP(TO_CHAR(TT1.DEPARTURE_TIME,'HH24:MI:SS'),'HH24:MI:SS');"
            cursor.execute(sql, [fro, to])
            result = cursor.fetchall()
            cursor.close()
        else:
            cursor = connection.cursor()
            sql = "SELECT TT1.TRAIN_ID,(SELECT TRAIN_NAME FROM TRAIN T1 WHERE T1.TRAIN_ID=TT1.TRAIN_ID) NAME1,TO_TIMESTAMP( concat(concat(TO_CHAR((SELECT SYSDATE FROM DUAL),'YYYY-MM-DD'),' '),TO_CHAR(TT1.DEPARTURE_TIME,'HH24:MI:SS')),'YYYY-MM-DD HH24:MI:SS'),TO_CHAR(TT2.DEPARTURE_TIME,'HH24:MI:SS'),ROW_NUMBER() Over (ORDER BY TO_TIMESTAMP(TO_CHAR(TT1.DEPARTURE_TIME,'HH24:MI:SS'),'HH24:MI:SS')) As SN " \
                  "FROM TRAIN_TIMETABLE TT1,TRAIN_TIMETABLE TT2 " \
                  "WHERE (TT1.DIRECTION=TT2.DIRECTION ) AND TT1.STATION_ID=(SELECT STATION_ID FROM STATION WHERE STATION_NAME=%s)  AND TT2.STATION_ID=(SELECT STATION_ID FROM STATION WHERE STATION_NAME=%s)  AND (TT1.TRAIN_ID=TT2.TRAIN_ID) AND TT1.DEPARTURE_TIME<TT2.DEPARTURE_TIME  " \
                  "ORDER BY TO_TIMESTAMP(TO_CHAR(TT1.DEPARTURE_TIME,'HH24:MI:SS'),'HH24:MI:SS');"
            cursor.execute(sql, [fro, to])
            result = cursor.fetchall()
            cursor.close()
        for r in result:
            print(r[0])
            print(r[1])
            print(r[2])
            print(r[3])
            print(r[4])
        print(type(adult))

        cursor1 = connection.cursor()
        sql1 = "select NVL((TRUNC(FARE*%s)+TRUNC(FARE*%s*0.5)),0) " \
               "FROM COST " \
               "WHERE FROM_STATION_ID=(SELECT STATION_ID from STATION where STATION_NAME=%s) AND TO_STATION_ID=(SELECT STATION_ID from STATION where STATION_NAME=%s) AND SEAT_CLASS=%s "
        cursor1.execute(sql1, [adult, child, fro, to, clas])
        result1 = cursor1.fetchall()
        cursor1.close()

        print(result1)
        st = "";
        for re in result1:
            st = re[0]
        print(st, 'yeeeeeeeeeeeeeeeeeeeeeeeee cost printed')
        if st != "":
            request.session['vat'] = str(int(st * 0.15))
            st = st + (st * 0.15)

        else:
            st = "0"

        cursor2 = connection.cursor()
        sql2 = "select NVL(FARE,0) " \
               "FROM COST " \
               "WHERE   FROM_STATION_ID=(SELECT STATION_ID from STATION where STATION_NAME=%s) AND TO_STATION_ID=(SELECT STATION_ID from STATION where STATION_NAME=%s) AND SEAT_CLASS=%s "
        cursor2.execute(sql2, [fro, to, clas])
        result2 = cursor2.fetchall()
        cursor2.close()
        st1 = ""
        st2 = ""
        st3 = ""
        st4 = ""
        st5 = ""
        st6 = ""
        for re2 in result2:
            st1 = int(re2[0])
            st2 = int(re2[0])
            st3 = int(re2[0])
            st4 = int(re2[0])
            st5 = int(re2[0])
            st6 = int(re2[0])

        fare_list = []
        fare_list.append(str(st1))
        fare_list.append(str(st2))
        fare_list.append(str(st3))
        fare_list.append(str(st4))
        fare_list.append(str(st5))
        fare_list.append(str(st6))

        dict_result = []
        doj = request.session.get('doj')
        traincnt = 0
        for r in result:
            traincnt = traincnt + 1
            TRAIN_ID = r[0]
            NAME = r[1]
            departure = r[2]
            arrival = r[3]
            sn = r[4]

            leftright = str(sn % 2)
            delay = (sn - 1) * 200

            cursor = connection.cursor()
            sql = "SELECT 78-COUNT(*) FROM BOOKED_SEATS WHERE TRAIN_ID=%s AND SEAT_CLASS='SNIGDHA' AND TRUNC(DATE_OF_JOURNEY)= TO_DATE(%s,'YYYY-MM-DD');"
            cursor.execute(sql, [TRAIN_ID, doj])
            result = cursor.fetchall()
            for r in result:
                snigdha = r[0];
            print(snigdha)
            cursor1 = connection.cursor()
            sql1 = "SELECT 78-COUNT(*) FROM BOOKED_SEATS WHERE TRAIN_ID=%s AND SEAT_CLASS='S_CHAIR' AND TRUNC(DATE_OF_JOURNEY)= TO_DATE(%s,'YYYY-MM-DD');"
            cursor1.execute(sql1, [TRAIN_ID, doj])
            result1 = cursor1.fetchall()
            for r1 in result1:
                s_chair = r1[0];
            print(s_chair)
            cursor2 = connection.cursor()
            sql2 = "SELECT 78-COUNT(*) FROM BOOKED_SEATS WHERE TRAIN_ID=%s AND SEAT_CLASS='SHOVAN' AND TRUNC(DATE_OF_JOURNEY)= TO_DATE(%s,'YYYY-MM-DD');"
            cursor2.execute(sql2, [TRAIN_ID, doj])
            result2 = cursor2.fetchall()
            for r2 in result2:
                shovan = r2[0];
            row = {'sn': sn, 'lr': leftright, 'delay': delay, 'TRAIN_ID': TRAIN_ID, 'NAME': NAME,
                   'DEPARTURE_TIME': str(departure), 'ARRIVAL_TIME': str(arrival),
                   's_chairfair': fare_list[0], 'snigdhafair': fare_list[1], 'shovanfair': fare_list[2],
                   'f_chairfare': fare_list[3], 'ac_seatfair': fare_list[4], 'f_berthfair': fare_list[5],
                   's_chairseat': snigdha, 'snigdhaseat': s_chair, 'shovanseat': shovan, 'f_chairseat': snigdha,
                   'ac_seatseat': s_chair, 'f_berthseat': shovan}
            dict_result.append(row)
        request.session['trains'] = dict_result
        request.session['cost'] = st
        request.session['snigdha_fare'] = fare_list
        print(details, type(details))

        return render(request, 'train_result.html',
                      {'tcount': traincnt, 'trains': dict_result, 'cost': st,
                       'details': details})
    else:
        cursor = connection.cursor()
        sql="SELECT TO_CHAR(SYSDATE,'YYYY-MM-DD') FROM DUAL;"
        cursor.execute(sql)
        result = cursor.fetchall()
        cursor.close()
        cursor = connection.cursor()
        sql = "SELECT TO_CHAR(SYSDATE+10,'YYYY-MM-DD') FROM DUAL;"
        cursor.execute(sql)
        result1 = cursor.fetchall()
        cursor.close()
        cursor = connection.cursor()
        sql = "SELECT STATION_NAME FROM STATION"
        cursor.execute(sql)
        result2 = cursor.fetchall()
        cursor.close()
        dict = []
        for r in result2:
            NAME = r[0]
            row = {'NAME': NAME}
            dict.append(row)
        for r in result:
            startdate=r[0]
            print(startdate)
        for r in result1:
            enddate=r[0]
            print(enddate)

        fullname=request.session.get('first')+' '+request.session.get('last')
        return render(request, 'search_train.html',{'max': enddate,'min': startdate,'names':dict,'username':fullname})


def seatselection(request):
    print("aise")
    print(request.POST)
    print("aise2")

    id = request.POST.get('train_id')
    request.session["train_id"] = id
    fro = request.session.get('from')
    print(id, fro)
    cursor0 = connection.cursor()
    sql0 = "SELECT (SELECT TRAIN_NAME FROM TRAIN T WHERE T.TRAIN_ID=TT.TRAIN_ID),TT.DEPARTURE_TIME " \
           "FROM TRAIN_TIMETABLE TT " \
           "WHERE TT.TRAIN_ID=TO_NUMBER(%s) AND STATION_ID=(SELECT STATION_ID FROM STATION WHERE STATION_NAME=%s);"
    cursor0.execute(sql0, [id, fro])
    result0 = cursor0.fetchall();
    cursor0.close()
    print(result0)
    for r in result0:
        request.session['train_name'] = r[0]
        request.session['dep_time'] = str(r[1])
    t = request.session.get('dep_time')
    print(t)
    # print(request.session.get('doj') + ' ' + t)
    # request.session["dtoj"] = request.session.get('doj')

    clas = request.session.get('class')
    adult = request.session.get('adult')
    child = request.session.get('child')
    date = request.session.get('doj')
    fro = request.session.get('from')
    to = request.session.get('to')
    address = request.session.get('address')
    doj = request.session.get('doj')
    print(type(doj))
    print('in seatselection 11111111111111111111111111111111111111111111111111111111111111111111111111')
    cursor = connection.cursor()
    sql = "SELECT SEAT_ID FROM BOOKED_SEATs WHERE TRAIN_ID=%s AND SEAT_CLASS=%s AND TRUNC(DATE_OF_JOURNEY)= TO_DATE(%s,'YYYY-MM-DD');"
    cursor.execute(sql, [id, clas, doj])
    result = cursor.fetchall();
    cursor.close()
    booked_seats = []
    for r in result:
        seat_no = r[0]
        booked_seats.append(seat_no)

    print(booked_seats)
    request.session['doj'] = str(date)
    request.session['class'] = clas
    request.session['from'] = fro
    request.session['to'] = to
    global details
    details = {'from': fro, 'to': to, 'date': date, 'adult': adult, 'child': child, 'class': clas}

    return render(request, 'seatdesign.html',
                  {'booked_seats': booked_seats, 'traindetails': details,
                   'mail': request.session.get('usermail'), 'mobile': str(request.session.get('contact')),
                   'full': request.session.get('first') + ' ' + request.session.get('last')})


def reservationofseat(request):
    print(request.POST)
    train_id = request.session.get('train_id')
    seat_class = request.session.get('class')
    compartment = 'A'
    doj = request.session.get('doj')
    user_id = request.session.get('user_id')
    no_of_tickets = 0
    payment = 'NULL'
    from_st = request.session.get('from')
    to_st = request.session.get('to')
    adult=request.session.get('adult')
    child = request.session.get('child')
    count=0
    reservedseat = []
    for i in range(1, 100):
        if (request.POST.get('seat' + str(i)) == 'on'):
            reservedseat.append(i)
            count=count+1
    print(reservedseat)
    if count!=int(adult)+int(child):
        return render(request,'userhome.html')
    for seatnum in reservedseat:
        cursor = connection.cursor()
        sql = "SELECT COUNT(*) FROM RESERVED_SEAT WHERE TRAIN_ID=%s AND SEAT_CLASS=%s AND SEAT_ID=%s AND TRAIN_COMPARTMENT=%s AND DATE_OF_JOURNEY= TO_DATE(%s,'YYYY-MM-DD');"
        cursor.execute(sql, [train_id, seat_class, seatnum, compartment, doj])
        result = cursor.fetchall();
        cursor.close()
        print(result)
        print(type(result))
        no_of_tickets = no_of_tickets + 1
        if (result != 0):
            redirect("customer:seatselection")
    train_id=request.session.get('train_id')
    print(train_id)
    cursor = connection.cursor()
    sql = "INSERT INTO RESERVATION VALUES(NVL((SELECT MAX(RESERVATION_ID)+1 FROM RESERVATION),1),(SELECT SYSDATE FROM DUAL),%s,%s,%s,%s,%s,%s,%s,%s);"
    cursor.execute(sql, [doj, no_of_tickets, seat_class, from_st, to_st, user_id, payment,train_id])
    # result = cursor.fetchall()
    cursor.close()

    for seatnum in reservedseat:
        print(seatnum)
        print(type(seatnum))
        print(train_id)
        print(type(train_id))
        print(doj)
        print(type(doj))
        print('55555555555555555555555555555555555')
        cursor = connection.cursor()
        sql = "INSERT INTO RESERVED_SEAT VALUES(%s,%s,%s,%s,%s,NVL((SELECT MAX(RESERVATION_ID) FROM RESERVATION),1),NVL((SELECT MAX(SL_NO) FROM RESERVED_SEAT)+1,1));"
        cursor.execute(sql, [seatnum, seat_class, train_id, compartment, doj])
        # result = cursor.fetchall();
        cursor.close()

    adult = request.session.get('adult')
    child = request.session.get('child')
    cursor1 = connection.cursor()
    sql1 = "select NVL((TRUNC(FARE*%s)+TRUNC(FARE*%s*0.5)),0) " \
           "FROM COST " \
           "WHERE FROM_STATION_ID=(SELECT STATION_ID from STATION where STATION_NAME=%s) AND TO_STATION_ID=(SELECT STATION_ID from STATION where STATION_NAME=%s) AND SEAT_CLASS=%s "
    cursor1.execute(sql1, [adult, child, from_st, to_st, seat_class])
    result1 = cursor1.fetchall()
    cursor1.close()
    st=""
    for re in result1:
        st = re[0] * 0.6
    print(st)
    if st != "":
        request.session['vat'] = str(int(st * 0.15))
        st = st + (st * 0.15)

    cursor2 = connection.cursor()
    sql2 = "SELECT MAX(RESERVATION_ID) FROM RESERVATION"
    cursor2.execute(sql2)
    result2 = cursor2.fetchall()
    cursor2.close()
    reservation_id = 0
    for r in result2:
        reservation_id = int(r[0])

    print(reservation_id, type(reservation_id))
    request.session['reservation_id']=reservation_id
    return render(request, 'paymentmethods.html',
                  {'from': from_st, 'to': to_st, 'reservation_id': reservation_id, 'cost': st,'child': child,'adult': adult})


def bkash(request):
    amount = request.session.get('cost')
    print('bkash payyyyyyyyyyyyyyyyyyyyyyyyyment')
    if request.method == "POST":
        num = request.POST["phonenum"]
        ps = request.POST["pin"]
        cursor = connection.cursor()
        sql = "SELECT PIN FROM BKASH WHERE PHONE_NUM=%s"
        cursor.execute(sql, [num])
        result=cursor.fetchall()
        cursor.close()
        for r in result:
            cod=r[0]
        if str(cod) == str(ps):
            doj = request.session.get('doj')
            doj = str(doj)
            adult = request.session.get('adult')
            child = request.session.get('child')
            cls = request.session.get('class')
            fro = request.session.get('from')
            to = request.session.get('to')
            tr = request.session.get('train_id')
            cursor4 = connection.cursor()
            sql4 = " SELECT TRAIN_NAME FROM TRAIN WHERE TRAIN_ID=%s;"
            cursor4.execute(sql4, [tr])
            result= cursor4.fetchall()
            cursor4.close()
            for r in result:
                train_name=r[0]
            print(tr)
            userid = request.session.get('user_id')
            print(userid)
            reservation_id=request.session.get('reservation_id')

            cursor4 = connection.cursor()
            sql4 = " SELECT SEAT_ID,SEAT_CLASS FROM RESERVED_SEAT WHERE RESERVATION_ID=%s;"
            cursor4.execute(sql4,[reservation_id])
            result4 = cursor4.fetchall()
            cursor4.close()
            print(reservation_id)
            print(result4)

            cursor3 = connection.cursor()
            for s in result4:
                seat = s[0]
                print(seat,type(seat))
                sql3 = "INSERT INTO BOOKED_SEATS VALUES(TO_NUMBER(%s),TO_NUMBER(%s),%s,TO_NUMBER(%s),%s,TO_DATE(%s,'YYYY-MM-DD'),NVL((SELECT MAX(SL_NO) FROM BOOKED_SEATS)+1,1));"
                cursor3.execute(sql3, [reservation_id,seat,cls,tr,'A', doj])
            cursor3.close()
            global details
            details = {'train_id': tr ,'name': train_name, 'from': fro, 'to': to, 'date': doj, 'class': cls,'total_seats': int(adult)+ int(child),'amount': amount,'reservation_id': reservation_id}
            return render(request, 'successful.html',{'det': details})
        else:
            msg='dgdhdhdfhfdgh'
            return render(request, 'bkash.html', {'cost': amount,'statusred': msg})
    else:
        return render(request, 'bkash.html', {'cost': amount})


def card(request):
    print('xvxxxx')
def nexus(request):
    print('xvxxxx')
def rocket(request):
    print('xvxxxx')
def paymentchecking(request):
    print('xvxxxx')
def success(request):
    return redirect('customer:userhome')
def verify(request):
    if request.method=="POST":
        phone_num=request.POST["phone"]
        ticket = request.POST["ticket_id"]
        cursor = connection.cursor()
        sql="SELECT COUNT(*) FROM RESERVATION R, ACCOUNTS A WHERE R.RESERVATION_ID=%s AND A.PHONE=%s AND R.USER_ID=A.USER_ID"
        cursor.execute(sql,[ticket,phone_num])
        result=cursor.fetchall()
        cursor.close()
        for r in result:
            out=r[0]
            if out!=0:
                print('rwerwerwewwree')
                return render(request, 'verification_success.html')
            else:
                return render(request, 'verification_fail.html')
        print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
        return render(request, 'verification_success.html')




    else:
        return render(request,'verify_ticket.html')
def contactus(request):
    return render(request, 'contactus.html')
def accounts(request):
    return redirect('accounts:userhome')
