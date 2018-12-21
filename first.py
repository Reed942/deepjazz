from __future__ import print_function
from generator import generate
from django.http import JsonResponse
from django.conf import settings
import os
import time


def aicompositionrequest(request):
    #用户认证
    authorization = request.POST.get('authorization')
    #文件格式 midi、mp3、wav
    preset = request.POST.get('preset')
    #文件名称 默认用时间+序号
    filename = request.POST.get('filename', time.strftime("%Y%m%d%H%M%S", time.localtime()))
    #每分钟节拍数
    bpm = request.POST.get('bpm', '80')
    #风格 jazz、piano
    essential = request.POST.get('essential')
    #乐器 piano
    instrument = request.POST.get('instrument')

    if (bpm.isdigit()):
        print('bpm:' + bpm)
    else:
        result = {"status": "FAIL", "message": "参数错误：bpm格式错误"}
        return JsonResponse(result, content_type="application/json,charset=utf-8")

    N_epochs = 64  # default


    print('filename:'+filename)
    bpm = int(bpm)

    # i/o settings
    data_fn = '/home/reed/dev/git@github/deepjazz/midi/' + 'original_metheny.mid'  # 'And Then I Knew' by Pat Metheny
    out_path = settings.AUDIO_ROOT
    out_directory = time.strftime("%Y%m%d", time.localtime())
    if not os.path.exists(out_path + out_directory):
        os.mkdir(out_path + out_directory)
    filename = filename + str(N_epochs)
    if (N_epochs == 1):
        filename += '_epoch.midi'
    else:
        filename += '_epochs.midi'
    out_fn = out_path + out_directory + '/' + filename

    start = time.time()
    aicomposition(data_fn, out_fn, N_epochs, bpm)
    end = time.time()
    print (end - start)

    access_url = settings.BASE_URL_PHDDNS + settings.AUDIO_URL + out_directory + '/' + filename
    result = {"status": "SUCCESS", "message": "响应成功", "data": {"audioPath": access_url}}
    return JsonResponse(result, content_type="application/json,charset=utf-8")

def aicomposition(data_fn, out_fn, N_epochs, bpm):
    generate(data_fn, out_fn, N_epochs, bpm)

