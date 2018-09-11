from django.shortcuts import render
from basic_app.models import Questions, UserProfileInfo, submissions
from basic_app.models import User
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse

import datetime
import os

from .forms import DocumentForm


path = 'data/users_code'
path2 = 'data/standard'
path3 = 'data/standard/testcaseScore'


def questions(request, id=1):
    if request.user.is_authenticated:
        if request.method == 'GET':
            a = Questions.objects.all()
            user = UserProfileInfo.objects.get(user=request.user)
            user.question_id = int(id)
            Q = a[user.question_id-1]
            q = Q.questions

            username = request.user.username

            if not os.path.exists('{}/{}/'.format(path, username)):
                user.attempts = 0   # this line should be exceuted only once
                os.system('mkdir {}/{}'.format(path, username))

                for i in range(1, 7):
                    os.system('mkdir {}/{}/question{}'.format(path, username, i))

            user.save()
            now = datetime.datetime.now()
            minutes = now.minute*60
            seconds = now.second
            count = minutes+seconds
            total_count = user.time-count

            dict = {'q': q, 't': total_count, 's': user.score}

            return render(request, 'basic_app/Codingg.html', context=dict)

        if 'submit' in request.POST:

            some_text = request.POST.get('editor')
            subb = submissions(user=request.user)
            subb.sub = some_text

            option = request.POST.get('lang')
            username = request.user.username
            user = UserProfileInfo.objects.get(user=request.user)
            user.option=option
            subb.qid = user.question_id
            subb.save()

            testlist = ['fail', 'fail', 'fail', 'fail', 'fail']

            juniorSenior = 'junior'  # temp
            myfile = open('{}/{}/{}.txt'.format(path3, str(user.question_id), str(user.question_id)))
            content = myfile.readlines()
            junior = [int(i.strip()) for i in content[0:5]]
            senior = [int(i.strip()) for i in content[5:10]]

            user.attempts += 1

            fo = open('{}/{}/question{}/{}{}.{}'.format(path, username, user.question_id, username, user.attempts, option), 'w')
            fo.write(some_text) # writes .c file
            fo.close()

            if os.path.exists('{}/{}/question{}/{}{}.{}'.format(path, username, user.question_id, username, user.attempts, option)):
                ans = os.popen("python data/main.py " + "{}/{}/question{}/{}{}.{}".format(path, username, user.question_id, username, user.attempts, option) + " " + username + " " + str(user.question_id) + " " + juniorSenior + " " + str(user.attempts)).read()
                ans = int(ans)  # saves like 9999899950
                print("THE SANDBOX CODE IS", ans)
                data = [1, 2, 3, 4, 5]
                tcOut = [0, 1, 2, 3, 4]
                switch = {

                    10: 0,
                    99: 1,
                    50: 2,
                    89: 3,
                    70: 4,
                    20: 5,
                }

                user.score = 0
                for i in range(0, 5):
                    data[i] = ans % 100	# stores output for each case but in reverse order
                    ans = int(ans / 100)

                    tcOut[i] = switch.get(data[i], 2)
                    if tcOut[i] == 0:  # if data[i] is 10 i.e correct answer
                        testlist[4 - i] = 'pass'
                        user.score = user.score + junior[i]

                cerror = " "

                if tcOut[4] == 3:
                    error = path + "/" + username + "/" + str("error{}.txt".format(user.question_id))

                    with open(error, 'r') as e:
                        cerror = e.read()
                        cerror = cerror.split('/', 4)[4]

                if tcOut[0] == 2 or tcOut[1] == 2 or tcOut[2] == 2 or tcOut[3] == 2 or tcOut[4] == 2:
                    cerror = "Time limit exceeded"

                if tcOut[0] == 4 or tcOut[1] == 4 or tcOut[2] == 4 or tcOut[3] == 4 or tcOut[4] == 4:
                    cerror = "Abnormal Termination"

                if tcOut[0] == 5 or tcOut[1] == 5 or tcOut[2] == 5 or tcOut[3] == 5 or tcOut[4] == 5:
                    cerror = "Abnormal Termination"


                if int(id) == 1:
                    if user.quest1test <= user.score:
                        user.quest1test = user.score
                    user.total = (user.quest1test+user.quest2test+user.quest3test+user.quest4test+user.quest5test)//5

                elif int(id) == 2:
                    if user.quest2test <= user.score:
                        user.quest2test = user.score
                    user.total = (user.quest1test + user.quest2test + user.quest3test + user.quest4test + user.quest5test) // 5

                elif int(id) == 3:
                    if user.quest3test <= user.score:
                        user.quest3test = user.score
                    user.total = (user.quest1test + user.quest2test + user.quest3test + user.quest4test + user.quest5test) // 5

                elif int(id) == 4:
                    if user.quest4test <= user.score:
                        user.quest4test = user.score
                    user.total = (user.quest1test + user.quest2test + user.quest3test + user.quest4test + user.quest5test) // 5

                elif int(id) == 5:
                    if user.quest5test <= user.score:
                        user.quest5test = user.score
                    user.total = (user.quest1test + user.quest2test + user.quest3test + user.quest4test + user.quest5test) // 5

                user.save()
                now = datetime.datetime.now()
                minutes = now.minute * 60
                seconds = now.second
                count = minutes + seconds
                total_count = user.time - count

                a = Questions.objects.all()
                Q = a[user.question_id - 1]

                status = 'Not completed'

                for_count = 0

                for i in testlist:
                    if i == 'pass':
                        for_count += 1

                print(for_count)

                if for_count == 5:
                    status = 'Completed'
                    Q._submissions += 1
                    Q.save()

                elif for_count == 0:
                    status = 'fail'

                subb.testCaseScore = (for_count / 5) * 100
                print(subb.testCaseScore)
                subb.save()

                dictt = {'s':user.score,'e':cerror,'d':user.question_id,'t':total_count,'t1':testlist[0],'t2':testlist[1],'t3':testlist[2],'t4':testlist[3],'t5':testlist[4],'status':status}

            return render(request, 'basic_app/Test Casee.html',context=dictt)

        elif 'load' in request.POST:
            username = request.user.username
            user = UserProfileInfo.objects.get(user=request.user)

            try:
                option = user.option


                z = open('{}/{}/question{}/{}{}.{}'.format(path, username, user.question_id, username, user.attempts,
                                                           option), 'r')

                read = z.read()

                user.save()
                a = Questions.objects.all()
                Q = a[user.question_id - 1]
                q = Q.questions

                dict = {'q': q, 's': user.score, 'load': read}
                return render(request, 'basic_app/Codingg.html', context=dict)
            except FileNotFoundError:
                a = Questions.objects.all()
                Q = a[user.question_id - 1]
                q = Q.questions
                dict = {'q': q}

                return render(request, 'basic_app/Codingg.html', context=dict)

        elif 'browse' in request.POST:
            form = DocumentForm(request.POST, request.FILES)
            dict = {
                'load': form
            }
            if form.is_valid():
                file3 = request.FILES.get('doc1', )
                form.save()
                x = str(file3)

                path4 = 'data/upload/' + x

                uploadfile = open(path4, 'r')
                up = uploadfile.read()
                dict = {
                    'upload': up
                }
                return render(request, 'basic_app/Codingg.html', context=dict)


def question_panel(request):

    if request.user.is_authenticated:
        all_user = UserProfileInfo.objects.all()
        accuracy_count = [0, 0, 0, 0, 0, 0]
        percentage_accuracy = [0, 0, 0, 0, 0, 0]
        user_count = 0
        now = datetime.datetime.now()
        minutes = now.minute * 60
        seconds = now.second
        count = minutes + seconds
        user = UserProfileInfo.objects.get(user=request.user)
        total_count = user.time - count

        for user in all_user:
            user_count += 1
            if user.quest1test == 100:
                accuracy_count[0] += 1
            if user.quest2test == 100:
                accuracy_count[1] += 1
            if user.quest3test == 100:
                accuracy_count[2] += 1
            if user.quest4test == 100:
                accuracy_count[3] += 1
            if user.quest5test == 100:
                accuracy_count[4] += 1
            if user.quest6test == 100:
                accuracy_count[5] += 1

        for i in range(0, 6):
            percentage_accuracy[i] = int((accuracy_count[i] / user_count) * 100)

        all_question = Questions.objects.all()

        a1 = 0

        for i in all_question:
            i.accuracy = percentage_accuracy[a1]
            a1 += 1
            i.save()

        subs = []

        for i in range(0,6):
            subs.append(all_question[i]._submissions)

        dict={'t':total_count, 'a0': percentage_accuracy[0], 'a1': percentage_accuracy[1], 'a2': percentage_accuracy[2], 'a3': percentage_accuracy[3], 'a4': percentage_accuracy[4], 'a5': percentage_accuracy[5], 'subs0': subs[0], 'subs1': subs[1], 'subs2': subs[2], 'subs3': subs[3], 'subs4': subs[4], 'subs5': subs[5]}
        return render(request,'basic_app/Question Hub.html', context=dict)
    else:
        return HttpResponse("This is wrong boi")


def leader(request):
    if request.user.is_authenticated:
        now = datetime.datetime.now()
        minutes = now.minute * 60
        seconds = now.second
        count = minutes + seconds
        user = UserProfileInfo.objects.get(user=request.user)
        total_count = user.time - count
        a=UserProfileInfo.objects.order_by("total")
        b=a.reverse()
        dict={'list':b,'t':total_count}
        return render(request,'basic_app/Leaderboard.html',context=dict)

    else:
        return HttpResponse("This is wrong boi")


def instructions(request):
    if request.user.is_authenticated:
        if request.method=="POST":
            return HttpResponseRedirect(reverse('basic_app:questions'))
        return render(request,'basic_app/instruction.html')
    else:
        return HttpResponse("This is wrong boi")


def user_logout(request):
    user = UserProfileInfo.objects.get(user=request.user)
    a = UserProfileInfo.objects.order_by("total")
    b = a.reverse()
    counter = 0
    for i in b:
        counter += 1
        if str(i.user) == str(request.user.username):
            break

    dict = {'count': counter, 'name': request.user.username, 'score': user.score}

    logout(request)
    return render(request, 'basic_app/Result.htm', context=dict)


def register(request):
        try:
            if request.method == 'POST':
                username = request.POST.get('name')
                password= request.POST.get('password')
                name1 = request.POST.get('name1')
                name2 = request.POST.get('name2')
                phone1 = request.POST.get('phone1')
                phone2 = request.POST.get('phone1')
                email1 = request.POST.get('email1')
                email2 = request.POST.get('email2')

                print(name1)
                print(phone1)

                a= User.objects.create_user( username=username, password=password)

                a.save()
                login(request,a)
                b=UserProfileInfo()
                b.user=a
                b.name1= name1
                b.name2= name2
                b.phone1 = phone1
                b.phone2 = phone2
                b.email1 = email1
                b.email2 = email2
                b.save()

                return HttpResponseRedirect(reverse('basic_app:instructions'))

        except IntegrityError:
            return HttpResponse("you have already been registered.")
        return render(request,'basic_app/Loginn.html')


def sub(request):
    user = UserProfileInfo.objects.get(user=request.user)
    a = submissions.objects.filter(user=request.user,qid=user.question_id)

    TS = []

    for i in a:
        TS.append(i.testCaseScore)

    print("THIS IS TCS", TS)

    now = datetime.datetime.now()
    minutes = now.minute * 60
    seconds = now.second
    count = minutes + seconds
    user = UserProfileInfo.objects.get(user=request.user)
    total_count = user.time - count

    dict={'loop':TS,'timer':total_count}
    return render(request,'basic_app/Submissionn.html',context=dict)


def retry(request,id=1):
    if request.method=="GET":
        a = submissions.objects.filter(user=request.user)
        array=[]
        idd=[]

        for i in a:
            array.append(i.sub)
            idd.append(i.qid)
        var= Questions.objects.all()

        f=idd[int(id)-1]
        q=var[int(f)-1]
        question=q.questions
        now = datetime.datetime.now()
        minutes = now.minute * 60
        seconds = now.second
        count = minutes + seconds
        user = UserProfileInfo.objects.get(user=request.user)
        total_count = user.time - count
        dict = {'sub': array[int(id)-1], 'question':question,'s':user.score,'t':total_count}

        return render(request, 'basic_app/Codingg.html', context=dict)
    if request.method=="POST":
        return questions(request)


def checkuser(request):
    response_data = {}
    uname = request.POST.get("name")
    check1 = User.objects.filter(username=uname)
    if not check1:
        response_data["is_success"] = True
    else:
        response_data["is_success"] = False
    return JsonResponse(response_data)

