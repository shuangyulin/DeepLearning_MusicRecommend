import configparser
import re
import json
import os
import mysql.connector
from django.http import JsonResponse
from hdfs import InsecureClient
from pyhive import hive
import csv
from util.configread import config_read
from util.CustomJSONEncoder import CustomJsonEncoder
from util.codes import normal_code, system_error_code
# 获取当前文件路径的根目录
parent_directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
m_username = "Administrator"
hadoop_client = InsecureClient('http://localhost:9870')
dbtype, host, port, user, passwd, dbName, charset,hasHadoop = config_read(os.path.join(parent_directory,"config.ini"))

#将mysql里的相关表转成hive库里的表
def migrate_to_hive():

    mysql_conn = mysql.connector.connect(
        host=host,
        port=port,
        user=user,
        password=passwd,
        database=dbName
    )
    cursor = mysql_conn.cursor()

    hive_conn = hive.Connection(
        host='localhost',
        port=10000,
        username=m_username,
    )
    hive_cursor = hive_conn.cursor()
    #创建Hive数据库（如果不存在）
    hive_cursor.execute(f"CREATE DATABASE IF NOT EXISTS {dbName}")
    hive_cursor.execute(f"USE {dbName}")

    gequxinxi_table_path=f'/user/hive/warehouse/{dbName}.db/gequxinxi'
    #删除已有的hive表
    if hadoop_client.status(gequxinxi_table_path,strict=False):
        hadoop_client.delete(gequxinxi_table_path, recursive=True)
    # 在Hive中删除表
    gequxinxi_drop_table_query = f"""DROP TABLE gequxinxi"""
    hive_cursor.execute(gequxinxi_drop_table_query)
    cursor.execute("SELECT * FROM gequxinxi")
    gequxinxi_column_info = cursor.fetchall()
    #将数据写入 CSV 文件
    with open(os.path.join(parent_directory, "gequxinxi.csv"), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # 写入数据行
        for row in gequxinxi_column_info:
            writer.writerow(row)
    cursor.execute("DESCRIBE gequxinxi")
    gequxinxi_column_info = cursor.fetchall()
    create_table_query = "CREATE TABLE IF NOT EXISTS gequxinxi ("
    for column, data_type, _, _, _, _ in gequxinxi_column_info:
        match = re.match(r'(\w+)(\(\d+\))?', data_type)
        mysql_type = match.group(1)
        hive_data_type = get_hive_type(mysql_type)
        create_table_query += f"{column} {hive_data_type}, "
    gequxinxi_create_table_query = create_table_query[:-2] + ") row format delimited fields terminated by ','"
    hive_cursor.execute(gequxinxi_create_table_query)
    # 上传映射文件
    gequxinxi_hdfs_csv_path = f'/user/hive/warehouse/{dbName}.db/gequxinxi'
    hadoop_client.upload(gequxinxi_hdfs_csv_path, os.path.join(parent_directory, "gequxinxi.csv"))
    fensixinxi_table_path=f'/user/hive/warehouse/{dbName}.db/fensixinxi'
    #删除已有的hive表
    if hadoop_client.status(fensixinxi_table_path,strict=False):
        hadoop_client.delete(fensixinxi_table_path, recursive=True)
    # 在Hive中删除表
    fensixinxi_drop_table_query = f"""DROP TABLE fensixinxi"""
    hive_cursor.execute(fensixinxi_drop_table_query)
    cursor.execute("SELECT * FROM fensixinxi")
    fensixinxi_column_info = cursor.fetchall()
    #将数据写入 CSV 文件
    with open(os.path.join(parent_directory, "fensixinxi.csv"), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # 写入数据行
        for row in fensixinxi_column_info:
            writer.writerow(row)
    cursor.execute("DESCRIBE fensixinxi")
    fensixinxi_column_info = cursor.fetchall()
    create_table_query = "CREATE TABLE IF NOT EXISTS fensixinxi ("
    for column, data_type, _, _, _, _ in fensixinxi_column_info:
        match = re.match(r'(\w+)(\(\d+\))?', data_type)
        mysql_type = match.group(1)
        hive_data_type = get_hive_type(mysql_type)
        create_table_query += f"{column} {hive_data_type}, "
    fensixinxi_create_table_query = create_table_query[:-2] + ") row format delimited fields terminated by ','"
    hive_cursor.execute(fensixinxi_create_table_query)
    # 上传映射文件
    fensixinxi_hdfs_csv_path = f'/user/hive/warehouse/{dbName}.db/fensixinxi'
    hadoop_client.upload(fensixinxi_hdfs_csv_path, os.path.join(parent_directory, "fensixinxi.csv"))
    songinfo_table_path=f'/user/hive/warehouse/{dbName}.db/songinfo'
    #删除已有的hive表
    if hadoop_client.status(songinfo_table_path,strict=False):
        hadoop_client.delete(songinfo_table_path, recursive=True)
    # 在Hive中删除表
    songinfo_drop_table_query = f"""DROP TABLE songinfo"""
    hive_cursor.execute(songinfo_drop_table_query)
    cursor.execute("SELECT * FROM songinfo")
    songinfo_column_info = cursor.fetchall()
    #将数据写入 CSV 文件
    with open(os.path.join(parent_directory, "songinfo.csv"), 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        # 写入数据行
        for row in songinfo_column_info:
            writer.writerow(row)
    cursor.execute("DESCRIBE songinfo")
    songinfo_column_info = cursor.fetchall()
    create_table_query = "CREATE TABLE IF NOT EXISTS songinfo ("
    for column, data_type, _, _, _, _ in songinfo_column_info:
        match = re.match(r'(\w+)(\(\d+\))?', data_type)
        mysql_type = match.group(1)
        hive_data_type = get_hive_type(mysql_type)
        create_table_query += f"{column} {hive_data_type}, "
    songinfo_create_table_query = create_table_query[:-2] + ") row format delimited fields terminated by ','"
    hive_cursor.execute(songinfo_create_table_query)
    # 上传映射文件
    songinfo_hdfs_csv_path = f'/user/hive/warehouse/{dbName}.db/songinfo'
    hadoop_client.upload(songinfo_hdfs_csv_path, os.path.join(parent_directory, "songinfo.csv"))
    cursor.close()
    mysql_conn.close()
    hive_cursor.close()
    hive_conn.close()

#转换成hive的类型
def get_hive_type(mysql_type):
    type_mapping = {
        'INT': 'INT',
        'BIGINT': 'BIGINT',
        'FLOAT': 'FLOAT',
        'DOUBLE': 'DOUBLE',
        'DECIMAL': 'DECIMAL',
        'VARCHAR': 'STRING',
        'TEXT': 'STRING',
    }
    if isinstance(mysql_type, str):
        mysql_type = mysql_type.upper()
    return type_mapping.get(str(mysql_type), 'STRING')

#执行hive查询
def hive_query():
    # 连接到Hive服务器
    conn = hive.Connection(host='localhost', port=10000, username=m_username,database=dbName)
    # 创建一个游标对象
    cursor = conn.cursor()
    try:

        #定义Hive查询语句
        szdq_query = "SELECT COUNT(*) AS total, szdq FROM fensixinxi GROUP BY szdq"
        # 执行Hive查询语句
        cursor.execute(szdq_query)
        # 获取查询结果
        szdq_results = cursor.fetchall()
        szdq_json_list=[]
        for row in szdq_results:
            szdq_json_list.append({"szdq":row[1],"total":row[0]})
        #将JSON数据写入文件
        with open(os.path.join(parent_directory, "fensixinxi_groupszdq.json"), 'w', encoding='utf-8') as f:
            json.dump(szdq_json_list, f, ensure_ascii=False, indent=4)


        #定义Hive查询语句
        singer_query = "SELECT COUNT(*) AS total, singer FROM songinfo GROUP BY singer"
        # 执行Hive查询语句
        cursor.execute(singer_query)
        # 获取查询结果
        singer_results = cursor.fetchall()
        singer_json_list=[]
        for row in singer_results:
            singer_json_list.append({"singer":row[1],"total":row[0]})
        #将JSON数据写入文件
        with open(os.path.join(parent_directory, "songinfo_groupsinger.json"), 'w', encoding='utf-8') as f:
            json.dump(singer_json_list, f, ensure_ascii=False, indent=4)

        pass
    except Exception as e:
         print(f"An error occurred: {e}")
    finally:
        # 关闭游标和连接
        cursor.close()
        conn.close()

    # hive分析
def hive_analyze(request):
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "data": {}}
        try:
            migrate_to_hive()
            hive_query()
            return JsonResponse(msg, encoder=CustomJsonEncoder)
        except Exception as e:
            msg['code'] = system_error_code
            msg['msg'] = f"发生错误：{e}"
            return JsonResponse(msg, encoder=CustomJsonEncoder)



