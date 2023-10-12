from .models import Image
from .serializers import ImageSerializer

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .module.colorchart import getChart
from .module.http import ok

import os
import subprocess

# Create your views here.
@api_view(['POST'])
def post(request):
    if request.method == 'POST':
        serializer = ImageSerializer (data=request.data)
        if serializer.is_valid(raise_exception = True):
            serializer.save()
            # 현재 디렉토리 저장
            original_dir = os.getcwd()
            # 새로운 디렉토리로 이동
            os.chdir("color/src")
            try:
                # 스크립트 실행
                res = subprocess.check_output("python main.py --image ../.." + serializer.data['image'], shell=True)
            except subprocess.CalledProcessError as e:
                return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            finally:
                # 원래의 디렉토리로 돌아가기
                os.chdir(original_dir)
            return Response(ok("퍼스널컬러 차트 로드 성공", rtnColorChart(res.decode("utf-8"))), status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def rtnColorChart(result):
    personal_color_info = result.split('퍼스널 컬러는 ')[1]
    tone = personal_color_info.split('(')[0]

    colorChart = getChart(tone)

    result = {"personal_color": colorChart}
    return result
