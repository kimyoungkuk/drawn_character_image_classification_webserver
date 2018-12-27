from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from PIL import Image
import re
import base64
from io import StringIO
import torch
import torch.nn as nn
import torchvision.transforms as transforms
from torch.autograd import Variable

#charactername = ["spongebob", "overbunny", "guardryan", "apeach", "jake", "hobbangman"]
#dic = { "스폰지밥" : "spongebob", "뚱이" : "ddongee", "징징이" : "jingjingee", "어피치" : "apeach", "라이언" : "ryan", "프로도" : "prodo", "네오" : "neo", "무지" : "moogie", "카카오 콘" : "kon", "카카오 제이지" : "jaygee", "라인 브라운" : "brown", "코니" : "cony", "라인 제임스" : "james", "라인 문" : "moon", "피카츄" : "pika", "파이리":"pyree", "꼬부기":"kkoboogie", "이상해씨":"iesanghaesee", "망나뇽" :"mangnanyong", "잠만보" : "jammanbo", "도라에몽" : "doraemong", "오버액션토끼" : "overbunny", "보노보노" : "bonobono", "짱구" :"jjangu", "흰둥이" : "whitedog", "뽀로로" :"bbororo", "수호랑":"guardryan", "아구몬" :"agumon", "무민":"moomin", "티모":"teemo", "미니언":"minion", "미키": "micky", "스누피":"snoopy", "심슨":"simpson", "바트":"bart", "마지":"marge", "푸":"poo", "제이크":"jake", "배찌":"batgee", "다오":"dao", "라바":"lava", "헬로키티":"hellokity", "호빵맨":"hobbangman", "케로로":"keroro", "햄토리":"hamtory", "집게사장":"jypgaesajang", "스폰지밥 플라크톤":"plankton", "핑크퐁":"pinkpong", "반다비":"bandabee", "앵그리버드":"angrybird", "뿌까":"ppukka", "졸라맨":"jolaman", "기영이" : "kiyoung", "마자용" : "majayong", "디그다" : "digda" }
dic = { "스폰지밥" : "spongebob", "뚱이" : "ddongee", "징징이" : "jingjingee", "어피치" : "apeach", "라이언" : "ryan", "프로도" : "prodo", "네오" : "neo", "무지" : "moogie", "카카오 콘" : "kon", "카카오 제이지" : "jaygee", "라인 브라운" : "brown", "코니" : "cony", "라인 제임스" : "james", "라인 문" : "moon", "피카츄" : "pika", "파이리":"pyree", "꼬부기":"kkoboogie", "이상해씨":"iesanghaesee", "망나뇽" :"mangnanyong", "잠만보" : "jammanbo", "도라에몽" : "doraemong", "오버액션토끼" : "overbunny", "보노보노" : "bonobono", "짱구" :"jjangu", "흰둥이" : "whitedog", "뽀로로" :"bbororo", "수호랑":"guardryan", "아구몬" :"agumon", "무민":"moomin", "티모":"teemo", "미니언":"minion", "미키": "micky", "스누피":"snoopy", "심슨":"simpson", "바트":"bart", "마지":"marge", "푸":"poo", "제이크":"jake", "배찌":"batgee", "다오":"dao", "라바":"lava", "헬로키티":"hellokity", "호빵맨":"hobbangman", "케로로":"keroro", "햄토리":"hamtory", "집게사장":"jypgaesajang", "스폰지밥 플라크톤":"plankton", "핑크퐁":"pinkpong", "반다비":"bandabee", "앵그리버드":"angrybird", "뿌까":"ppukka", "졸라맨":"jolaman", "디그다":"digda", "기영이":"kiyoung", "마자용":"majayong" }
dic_values = dic.values()
charactername = list(dic_values)
dic_keys = dic.keys()
characternamek = list(dic_keys)

resnet = torch.load('ti/static/ti/character_50.pth', map_location='cpu')
imsize = 224
loader = transforms.Compose([transforms.Scale(imsize), transforms.ToTensor()])
# Create your views here.
def index(request):
    #msg = Image.open('ti/pic2.png')
    msg = 'indexda'
    raw = request.POST.get('canvasData', '')
    x = raw[22:]
    x += "=" * ((4 - len(x) % 4) % 4)
    canvasData = base64.b64decode(x)
    output = open('ti/static/ti/drawpic.png', 'wb')
    output.write(canvasData)
    output.close()



    ###################
    #여기서 drawpic.png(유저가 그린 그림)를 읽어서 모델에 넣어야함
    #여기를 거쳐서 무언가를 내뱉고
    #아래의 return에 배출하거나
    #또다른 대표이미지으로 저장하거나 해야함
    ###################
    #resnet = torch.load('ti/static/ti/character_50.pth', map_location='cpu')
    #resnet = resnet.cpu().float()
    try:
        image = image_loader('ti/static/ti/drawpic.png')
    except:
        image = image_loader('ti/static/ti/pic.png')

    outputs = resnet(image)
    #print (outputs.size())   # (10, 100)
    #print (outputs)
    sm=nn.Softmax()

    k = 3
    _,labelarr=torch.topk(outputs,k)
    problarr,_=torch.topk(sm(outputs),k)

    candi=[]

    for i in range(k):
        x = problarr[0][i].__float__()
        candi.append([labelarr[0][i].__int__(),float("{0:.2f}".format(x)),characternamek[labelarr[0][i].__int__()]])


    #_, preds = torch.max(outputs.data, 1)
    #print(preds)
    #label=charactername[preds.__int__()]
    #return HttpResponse('Hello world!, do crawling, do matching')
    return render(request,'ti/index.html',{'label1': candi[0][1],'probl1': candi[0][2],'label2': candi[1][1],'probl2': candi[1][2],'label3': candi[2][1],'probl3': candi[2][2],})
    #return render(request,'ti/index.html',{'message': raw})


def image_loader(image_name):
    """load image, returns cuda tensor"""
    image = Image.open(image_name).convert('RGB')
    image = loader(image).float()
    image = Variable(image, requires_grad=True)
    image = image.unsqueeze(0)  #this is for VGG, may not be needed for ResNet
    return image  #assumes that you're using GPU


def test(request):
    msg = 'ti/pic2.png'
    #return HttpResponse('Hello world!, do crawling, do matching')
    return render(request,'ti/test.html',{'message': msg})

def process(request):
    # print 'dfsfds'
    #img = Image.somehowLoad(canvasData)

    canvasData = request.POST.get('img', '')
    output = open('output.txt', 'w')
    output.write(canvasData)
    output.close()

    canvasData ='r3h2iu'
    #img.save('ti/canvas.png')
    return render(request,'ti/index.html',{'message': canvasData})


# def test(request):
#     value = RequestContext(request, {'user':request.user})
#     template = get_template('ti/test.html')
#     output = template.render(value)
#     return HttpResponse(output)

def test2(request):
    name = request.GET['name']
    age = request.GET['age']
    value = RequestContext(request, {'name':name, 'age':age})
    template = get_template('ti/test2.html')
    output = template.render(value)
    return HttpResponse(output)
