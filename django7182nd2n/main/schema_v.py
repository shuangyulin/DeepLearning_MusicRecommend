# coding:utf-8

import logging, os, time
import json
from django.http import JsonResponse
from django.apps import apps
from wsgiref.util import FileWrapper
from django.http import HttpResponse,HttpResponseRedirect
from django.shortcuts import redirect
import requests
from .config_model import config
from util.codes import *
from util import message as mes
from util.baidubce_api import BaiDuBce
from util.locate import geocoding
from dj2.settings import dbName as schemaName
from dj2.settings import hasHadoop
from django.db import connection
from hdfs.client import Client

def schemaName_cal(request, tableName, columnName):
    '''
    计算规则接口
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, 'data': []}
        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__ == tableName:

                data = m.getcomputedbycolumn(
                    m,
                    m,
                    columnName
                )
                print(data)
                if data:
                    try:
                        sum='%.05f' % float(data.get("sum"))
                    except:
                        sum=0.00
                    try:
                        max='%.05f' % float(data.get("max"))
                    except:
                        max=0.00
                    try:
                        min='%.05f' % float(data.get("min"))
                    except:
                        min=0.00
                    try:
                        avg='%.05f' % float(data.get("avg"))
                    except:
                        avg=0.00
                    msg['data'] = {
                        "sum": sum,
                        "max": max,
                        "min": min,
                        "avg": avg,
                    }
                break

        return JsonResponse(msg)


def schemaName_file_upload(request):
    '''
    上传
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}

        req_dict = request.session.get("req_dict")
        type = req_dict.get("type")

        file = request.FILES.get("file")

        if file:
            filename = file.name
            filesuffix = filename.split(".")[-1]
            file_name = "{}.{}".format(int(float(time.time()) * 1000), filesuffix)
            if type != None and '_template' in type:
                file_name="{}.{}".format(type,filesuffix)
            filePath = os.path.join(os.getcwd(), "templates/front", file_name)
            print("filePath===========>", filePath)

            with open(filePath, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            msg["file"] = file_name
            # 判断是否需要保存为人脸识别基础照片
            req_dict = request.session.get("req_dict")
            type1 = req_dict.get("type", 0)
            print("type1=======>",type1)
            type1 = str(type1)
            if type1 == '1':
                params = {"name":"faceFile","value": file_name}
                config.createbyreq(config, config, params)
            if '是' in hasHadoop or 'spark' in hasHadoop:
                try:
                    client = Client("http://127.0.0.1:50070/")
                    client.upload(hdfs_path=f'/{file_name}', local_path=filePath, chunk_size=2 << 19, overwrite=True)
                except Exception as e:
                    print(f"hdfs upload error : {e}")

        return JsonResponse(msg)


def schemaName_file_download(request):
    '''
    下载
    '''
    if request.method in ["POST", "GET"]:
        req_dict = request.session.get("req_dict")
        filename = req_dict.get("fileName")

        filePath = os.path.join(os.getcwd(), "templates/front", filename)
        print("filePath===========>", filePath)
        if '是' in hasHadoop or 'spark' in hasHadoop:
            try:
                client = Client("http://127.0.0.1:50070/")
                client.download(hdfs_path=f'/{filename}', local_path=filename, overwrite=True)
            except Exception as e:
                print(f"hdfs download error : {e}")
        file = open(filePath, 'rb')
        response = HttpResponse(file)

        response['Content-Type'] = 'text/plain'
        response['Content-Disposition'] = 'attachment; filename=%s' % os.path.basename(filePath)
        response['Content-Length'] = os.path.getsize(filePath)
        return response


def schemaName_follow_level(request, tableName, columnName, level, parent):
    '''

    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, 'data': []}
        # 组合查询参数
        params = {
            "level": level,
            "parent": parent
        }

        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__ == tableName:
                data = m.getbyparams(
                    m,
                    m,
                    params
                )
                # 只需要此列的数据
                for i in data:
                    msg['data'].append(i.get(columnName))
                break
        return JsonResponse(msg)


def schemaName_follow(request, tableName, columnName):
    '''
    根据option字段值获取某表的单行记录接口
    组合columnName和columnValue成dict，传入查询方法
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, 'data': []}
        # 组合查询参数
        params = request.session.get('req_dict')
        columnValue = params.get("columnValue")
        params = {columnName: columnValue}

        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__ == tableName:
                data = m.getbyparams(
                    m,
                    m,
                    params
                )
                if len(data)>0:
                    msg['data'] = data[0]
                break

        return JsonResponse(msg)


def schemaName_location(request):
    '''
    定位
    :return:
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": mes.normal_code, "address": ''}
        req_dict = request.session.get('req_dict')

        datas = config.getbyparams(config, config, {"name": "baidu_ditu_ak"})
        if len(datas) > 0:
            baidu_ditu_ak = datas[0].get("baidu_ditu_ak")
        else:
            baidu_ditu_ak = 'QvMZVORsL7sGzPyTf5ZhawntyjiWYCif'
        lat = req_dict.get("lat", 24.2943350100)
        lon = req_dict.get("lng", 116.1287866600)
        msg['address'] = geocoding(baidu_ditu_ak, lat, lon)

        return JsonResponse(msg)


def schemaName_matchface(request):
    '''
    baidubce百度人脸识别
    '''
    if request.method in ["POST", "GET"]:
        try:
            msg = {"code": normal_code}
            req_dict = request.session.get("req_dict")

            face1 = req_dict.get("face1")
            file_path1 = os.path.join(os.getcwd(),"templates/front",face1)

            face2 = req_dict.get("face2")
            file_path2 = os.path.join(os.getcwd(), "templates/front", face2)

            data = config.getbyparams(config, config, {"name": "APIKey"})
            client_id = data[0].get("value")
            data = config.getbyparams(config, config, {"name": "SecretKey"})
            client_secret = data[0].get("value")

            bdb = BaiDuBce()
            score = bdb.bd_check2pic(file_path1, file_path2)
            msg['score'] = score

            return JsonResponse(msg)
        except:
            return JsonResponse({"code": 500, "msg": "匹配失败", "score": 0})


def schemaName_option(request, tableName, columnName):
    '''
    获取某表的某个字段列表接口
    :param request:
    :param tableName:
    :param columnName:
    :return:
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, 'data': []}

        new_params = {}
        params = request.session.get("req_dict")
        if params.get('conditionColumn') != None and params.get('conditionValue') != None:
            new_params[params['conditionColumn']] = params['conditionValue']

        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__ == tableName:
                data = m.getbyColumn(
                    m,
                    m,
                    columnName,
                    new_params
                )

                msg['data'] = data
                break
        return JsonResponse(msg)

def schemaName_sh(request, tableName):
    '''
    根据主键id修改table表的sfsh状态接口
    '''
    if request.method in ["POST", "GET"]:
        print('tableName=========>', tableName)
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        req_dict = request.session.get("req_dict")
        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__ == tableName:

                # 查询结果
                data1 = m.getbyid(
                    m,
                    m,
                    req_dict.get('id')
                )
                if data1[0].get("sfsh") == '是':
                    req_dict['sfsh'] = '否'
                else:
                    req_dict['sfsh'] = '否'

                # 更新
                res = m.updatebyparams(
                    m,
                    m,
                    req_dict
                )
                # logging.warning("schemaName_sh.res=====>{}".format(res))
                if res!=None:
                    msg["code"]=crud_error_code
                    msg["code"]=mes.crud_error_code
                break
        return JsonResponse(msg)


def schemaName_upload(request, fileName):
    '''
    '''
    if request.method in ["POST", "GET"]:
        return HttpResponseRedirect ("/{}/front/{}".format(schemaName,fileName))

def schemaName_upload_forecast(request,tableName,fileName):
    '''
    '''
    if request.method in ["POST", "GET"]:
        return HttpResponseRedirect ("/{}/front/{}/{}".format(schemaName,tableName,fileName))


def schemaName_group_quyu(request, tableName, columnName):
    '''
    {
    "code": 0,
    "data": [
        {
            "total": 2,
            "shangpinleibie": "水果"
        },
        {
            "total": 1,
            "shangpinleibie": "蔬菜"
        }
    ]
    }
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        allModels = apps.get_app_config('main').get_models()
        where = {}
        for m in allModels:
            if m.__tablename__ == tableName:
                for item in m.__authTables__.items():
                    if request.session.get("tablename") == item[1]:
                        where[item[0]] = request.session.get("params").get(item[0])
                msg['data'] = m.groupbycolumnname(
                    m,
                    m,
                    columnName,
                    where
                )
                break

        return JsonResponse(msg)


def schemaName_value_quyu(request, tableName, xColumnName, yColumnName):
    '''
    按值统计接口,
    {
    "code": 0,
    "data": [
        {
            "total": 10.0,
            "shangpinleibie": "aa"
        },
        {
            "total": 20.0,
            "shangpinleibie": "bb"
        },
        {
            "total": 15.0,
            "shangpinleibie": "cc"
        }
    ]
}
    '''
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        allModels = apps.get_app_config('main').get_models()
        where = {}
        for m in allModels:
            if m.__tablename__ == tableName:
                for item in m.__authTables__.items():
                    if request.session.get("tablename") == item[1]:
                        where[item[0]] = request.session.get("params").get(item[0])
                msg['data'] = m.getvaluebyxycolumnname(
                    m,
                    m,
                    xColumnName,
                    yColumnName,
                    where
                )
                break

        return JsonResponse(msg)

def schemaName_value_riqitj(request, tableName, xColumnName, yColumnName, timeStatType):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        where = ' where 1 = 1 '
        allModels = apps.get_app_config('main').get_models()
        for m in allModels:
            if m.__tablename__ == tableName:
                for item in m.__authTables__.items():
                    if request.session.get("tablename") == item[1]:
                        where = where + " and " + item[0] + " = '" +  request.session.get("params").get(item[0]) + "' "
        sql = ''
        if timeStatType == '日':
            sql = "SELECT DATE_FORMAT({0}, '%Y-%m-%d') {0}, sum({1}) total FROM {3} {2} GROUP BY DATE_FORMAT({0}, '%Y-%m-%d')".format(xColumnName, yColumnName, where, tableName, '%Y-%m-%d')

        if timeStatType == '月':
            sql = "SELECT DATE_FORMAT({0}, '%Y-%m') {0}, sum({1}) total FROM {3} {2} GROUP BY DATE_FORMAT({0}, '%Y-%m')".format(xColumnName, yColumnName, where, tableName, '%Y-%m')

        if timeStatType == '年':
            sql = "SELECT DATE_FORMAT({0}, '%Y') {0}, sum({1}) total FROM {3} {2} GROUP BY DATE_FORMAT({0}, '%Y')".format(xColumnName, yColumnName, where, tableName, '%Y')

        L = []
        cursor = connection.cursor()
        cursor.execute(sql)
        desc = cursor.description
        data_dict = [dict(zip([col[0] for col in desc], row)) for row in cursor.fetchall()] 
        for online_dict in data_dict:
            for key in online_dict:
                if 'datetime.datetime' in str(type(online_dict[key])):
                    online_dict[key] = online_dict[key].strftime(
                        "%Y-%m-%d %H:%M:%S")
                else:
                    pass
            L.append(online_dict)
        msg['data'] = L

        return JsonResponse(msg)

def schemaName_spider(request, tableName):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": []}

        # Linux
        cmd = "cd /yykj/python/9999/spider7ph56346 && scrapy crawl "+tableName+"Spider -a databaseName=django7182nd2n"
        # Windows
        # cmd = "cd C:\\test1\\spider && scrapy crawl " + tableName + "Spider -a databaseName=django7182nd2n"
        os.system(cmd)

        return JsonResponse(msg)







