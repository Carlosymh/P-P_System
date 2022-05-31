import requests # pip install requests
import json
from datetime import datetime, date #pip install datetime
from connect import connectBD
import pymysql #pip install pymysql #pip install mysql-connector-python-rf


url="https://metabase.munitienda.com/public/question/e8e1234f-6818-430f-a6c8-86585cd4ef09.json"
response = requests.get(url)
if  response.status_code == 200:
  content = response.json()
  for row in content:
    if row['EAN']:
        routeName= row['ROUTENAME']
        FUName=row['FUNAME']
        Service_Zone=row['SERVICE_ZONE']
        fk_order= row['FK_ORDER']
        packer=row['PACKER']
        FuOrder=row['FUORDER']
        ean=row['EAN']
        operationGroup=row['OPERATIONGROUP']
        productName=row['PRODUCTNAME']
        type=row['TYPE']
        deliveryDate=row['DELIVERYDATE']
        originalQuantity=int(row['ORIGINALQUANTITY'])
        Vendor=row['VENDOR']
        CLid=row['CLID']
        Stop=row['STOP']
        currentQuantity=int(row['CURRENTQUANTITY'])
        pendingQuantity=int(originalQuantity)-int(currentQuantity)
        if originalQuantity==currentQuantity:
          status= 'Finished'
        elif currentQuantity>0 and pendingQuantity> 0:
          status= 'In Process'
        else:
          status= 'Pending'
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM orders WHERE RouteName=%s AND  Fk_order=%s AND FuOrder=%s AND Ean=%s  Limit 1 "
        cur.execute(sql, (routeName,fk_order,FuOrder,ean))
        data = cur.fetchone()
        cur.close()
        if data is None:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Create a new record
          sql = "INSERT INTO orders (RouteName,FUName,Service_Zone,Fk_order,Packer,FuOrder,Ean,OperationGroup,ProductName,Type,DeliveryDay,OriginalQuantity,Vendedor,CLid,Stop,CurrentQuantity,PendingQuantity,Status,Site) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
          cur.execute(sql,(routeName,FUName,Service_Zone,fk_order,packer,FuOrder,ean,operationGroup,productName,type,deliveryDate,originalQuantity,Vendor,CLid,Stop,currentQuantity,pendingQuantity,status,'CDMX01',))
          # connection is not autocommit by default. So you must commit to save
          # your changes.
          db_connection.commit()
          cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Create a new record
          sql = "UPDATE orders SET CurrentQuantity = %s, PendingQuantity = %s, Status = %s, Packer = %s WHERE RouteName=%s AND  Fk_order=%s AND FuOrder=%s AND Ean=%s"
          cur.execute(sql,(currentQuantity,pendingQuantity,status,packer,routeName,fk_order,FuOrder,ean,))
          # connection is not autocommit by default. So you must commit to save
          # your changes.
          db_connection.commit()
          cur.close()
print('Mex')

url="https://metabase.munitienda.com/public/question/2bf5ae32-804a-4259-8f33-b7b7b6b9f9ec.json"
response = requests.get(url)
if  response.status_code == 200:
  content = response.json()
  for row in content:
    if row['EAN']:
        routeName= row['ROUTENAME']
        FUName=row['FUNAME']
        Service_Zone=row['SERVICE_ZONE']
        fk_order= 0
        packer=row['PACKER']
        FuOrder='No aplica'
        ean=row['EAN']
        operationGroup=row['OPERATIOGROUP']
        productName=row['PRODUCT']
        type=row['TYPE']
        deliveryDate=row['DELIVERY_DATE']
        originalQuantity=int(row['ORIGINALQUANTITY'])
        Vendor=row['VENDOR_NAME']
        CLid=row['CLID']
        Stop=row['STOP']
        currentQuantity=int(row['CURRENTQUANTITY'])
        pendingQuantity=int(originalQuantity)-int(currentQuantity)
        if originalQuantity==currentQuantity:
          status= 'Finished'
        elif currentQuantity>0 and pendingQuantity> 0:
          status= 'In Process'
        else:
          status= 'Pending'
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM orders WHERE RouteName=%s AND  Fk_order=%s AND FuOrder=%s AND Ean=%s  Limit 1 "
        cur.execute(sql, (routeName,fk_order,FuOrder,ean))
        data = cur.fetchone()
        cur.close()
        if data is None:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Create a new record
          sql = "INSERT INTO orders (RouteName,FUName,Service_Zone,Fk_order,Packer,FuOrder,Ean,OperationGroup,ProductName,Type,DeliveryDay,OriginalQuantity,Vendedor,CLid,Stop,CurrentQuantity,PendingQuantity,Status,Site) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
          cur.execute(sql,(routeName,FUName,Service_Zone,fk_order,packer,FuOrder,ean,operationGroup,productName,type,deliveryDate,originalQuantity,Vendor,CLid,Stop,currentQuantity,pendingQuantity,status,'MEDELLIN01',))
          # connection is not autocommit by default. So you must commit to save
          # your changes.
          db_connection.commit()
          cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Create a new record
          sql = "UPDATE orders SET CurrentQuantity = %s, PendingQuantity = %s, Status = %s, Packer = %s WHERE RouteName=%s AND  Fk_order=%s AND FuOrder=%s AND Ean=%s"
          cur.execute(sql,(currentQuantity,pendingQuantity,status,packer,routeName,fk_order,FuOrder,ean,))
          # connection is not autocommit by default. So you must commit to save
          # your changes.
          db_connection.commit()
          cur.close()
print('col')
