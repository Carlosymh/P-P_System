from flask import Flask, render_template, request, redirect, url_for, flash, session, make_response, Response, jsonify #pip install flask
import requests # pip install requests
import io # pip install requires.io
import json
import cv2 #pip install opencv-python-headless or pip install opencv-python
import numpy as np  
from pyzbar.pyzbar import decode #pip install pyzbar or pip install pyzbar[scripts]
from werkzeug.security import generate_password_hash, check_password_hash #pip install -U Werkzeug
from datetime import datetime, date #pip install datetime pip install pytz
import pytz 
import hashlib #pip install hashlib
import qrcode #pip install qrcode #pip install Pillow
import csv
from connect import connectBD
import pymysql #pip install pymysql #pip install mysql-connector-python-rf
import os
import unicodedata
  
UTC = pytz.utc 


# settings
app = Flask(__name__)
app.secret_key = 'mysecretkey'
UPLOAD_FOLDER = 'static/file/'

# Function for passwords 
def _create_password(password):
   return generate_password_hash(password,'pbkdf2:sha256:30',30)

# index page (user form)
@app.route('/')
def Index():
  try:
    if 'FullName' in session:
      return redirect('/home')
    else:
      return render_template('index.html')
  except Exception as error:
    flash(str(error))
    return render_template('index.html')

# password form 
@app.route('/inicio', methods=['POST'])
def validarusuaro():
  if request.method == 'POST':
      usuario =  request.form['user'] 
      link = connectBD()
      db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
      cur= db_connection.cursor()
      sql = "SELECT * FROM `users` WHERE `User`=%s Limit 1"
      cur.execute(sql, (usuario,))
      # Read a single record
      data = cur.fetchone()
      cur.close()
      if data :
        username = data[1]
        user = data[3]
        return render_template('inicio.html',username=username,user=user)
      else:
        return render_template('index.html')
 
# form to change site
@app.route('/cambiar', methods=['POST'])
def cambiarfacility():
  try:
    if request.method == 'POST':
      facility = request.form['facility']
      session['SiteName']=facility
      return redirect('/home')
  except:
    return redirect('/home')
    
# user validation
@app.route('/validar/<usuario>', methods=['POST'])
def validarcontrasena(usuario):
  try:
    if request.method == 'POST':
      usuario =  usuario
      password = request.form['clave']
      link = connectBD()
      db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
      cur= db_connection.cursor()
      sql = "SELECT * FROM `users` WHERE `User`=%s Limit 1"
      cur.execute(sql, (usuario,))
      # Read a single 
      data = cur.fetchone()
      cur.close()
      if data :
        if check_password_hash(data[4],password):
          session['UserName'] = data[1]
          session['FullName'] = data[1] +" "+ data[2]
          session['User'] = data[3]
          session['SiteName'] = data[6]
          session['Rango'] = data[5]
          return redirect('/home')
        else:
          flash('Contraseña Incorrecta')
          return redirect('/')
    else:
      return redirect('/')
  except Exception as error:
    flash(str(error))
    return redirect('/')

# home page 
@app.route('/home',methods=['POST','GET'])
def home():
  try:
    if 'FullName' in session:
      return render_template('home.html',Datos = session)
    else:
      flash("Inicia Sesion")
      return render_template('index.html')

  except Exception as error:
    flash(str(error))
    return redirect('/') 

# packing form 
@app.route('/Packing',methods=['POST','GET'])
def packing():
  try:
    if 'FullName' in session:
      return render_template('form/packing.html',Datos = session)
    else:
      flash("Inicia Sesion")
      return render_template('index.html')
  except Exception as error:
    flash(str(error))
    return redirect('/') 

# receiving form 
@app.route('/Receiving',methods=['POST','GET'])
def recdeiving():
  try:
    if 'FullName' in session:
      return render_template('form/receiving.html',Datos = session)
    else:
      flash("Inicia Sesion")
      return redirect('/')
  except Exception as error:
    flash(str(error))
    return redirect('/') 

# inventori form
@app.route('/Inventory',methods=['POST','GET'])
def inventory():
  try:
    if 'FullName' in session:
      return render_template('form/inventory.html',Datos = session)
    else:
      flash("Inicia Sesion")
      return redirect('/')
  except Exception as error:
    flash(str(error))
    return redirect('/') 

# inventori form
@app.route('/Damage',methods=['POST','GET'])
def damage():
  try:
    if 'FullName' in session:
      return render_template('form/damage.html',Datos = session)
    else:
      flash("Inicia Sesion")
      return redirect('/')
  except Exception as error:
    flash(str(error))
    return redirect('/') 

# inventori form
@app.route('/Product',methods=['POST','GET'])
def product():
  try:
    if 'FullName' in session:
      return render_template('form/product.html',Datos = session)
    else:
      flash("Inicia Sesion")
      return redirect('/')
  except Exception as error:
    flash(str(error))
    return redirect('/') 

# user register form 
@app.route('/registro',methods=['POST','GET'])
def registro():
  try:
    if session['Rango'] == 'Administrador' or session['Rango'] == 'Training' :
      return render_template('registro.html', Datos = session)
    else:
      flash("Acseso Denegado")
    return render_template('index.html')
  except Exception as error:
    flash(str(error))
    return redirect('/')

# packing register 
@app.route('/RegistrarPacking',methods=['POST','GET'])
def registroP():
  try:
      if request.method == 'POST':
        deliveryday =  request.form['deliveryday']
        route =  request.form['route']
        OG =  request.form['OG']
        Site =  session['SiteName']
        status="Finished"
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM `orders` WHERE CLid=%s AND DeliveryDay=%s AND NOT Status =%s AND OperationGroup=%s AND Site=%s "
        cur.execute(sql, (route,deliveryday,status,OG,Site, ))
        data = cur.fetchall()
        cur.close()
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM `orders` WHERE CLid=%s AND DeliveryDay=%s AND  Status =%s AND OperationGroup=%s AND Site=%s "
        cur.execute(sql, (route,deliveryday,status,OG,Site, ))
        data3 = cur.fetchall()
        cur.close()
        if data :
          return render_template('actualizacion/Scan.html',Datos =session, data=data,dataf=data3)
        else:
          flash("No hay Ordenes Pendientes es esta ruta")
          return redirect('/Packing')
  except Exception as error: 
    flash(str(error))
    return redirect('/Packing')

# packin mov register
@app.route('/RegistroMovPacking/<route>/<deliveryday>/<OG>',methods=['POST','GET'])
def registroMovPacking(route,deliveryday,OG):
  try:
      if request.method == 'POST':
        ean =  request.form['ean'].strip()
        status="Finished"
        Site=session['SiteName']
        
        if session['SiteName']=='CDMX01':
          timeZ = pytz.timezone('America/Mexico_City')
        elif session['SiteName']=='MEDELLIN01':
          timeZ = pytz.timezone('America/Bogota')
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM product WHERE CB_Captura =%s  limit 1  "
        cur.execute(sql, (ean))
        product = cur.fetchone()
        cur.close()
        if product:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT * FROM orders WHERE Ean=%s AND  CLid=%s AND DeliveryDay=%s AND NOT Status=%s AND OperationGroup=%s AND Site=%s  limit 1"
            cur.execute(sql, (product[2],route,deliveryday,status,OG,Site))
            data = cur.fetchone()
            cur.close()
            if data :
              Packer=session['UserName']
              OriginalQuantity=data[12]
              CurrentQuantity	=int(data[16])+int(product[4])
              PendingQuantity=int(data[17])-int(product[4])
              if OriginalQuantity==CurrentQuantity:
                estatus= 'Finished'
              elif CurrentQuantity>0 and PendingQuantity> 0:
                estatus= 'In Process'
              else:
                estatus= 'Pendding'
              ID_Order =data[0]
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Create a new record
              sql = "UPDATE orders SET Packer = %s, CurrentQuantity = %s,PendingQuantity = %s, Status = %s WHERE ID_Order  = %s"
              cur.execute(sql,(Packer,CurrentQuantity,PendingQuantity,estatus,ID_Order,))
              # connection is not autocommit by default. So you must commit to save
              # your changes.
              db_connection.commit()
              cur.close()
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Create a new record
              sql = "INSERT INTO movements (RouteName,FuOrder,CLid,Ean,Description,Quantity,Process,Responsible,Site,DateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
              cur.execute(sql,(data[1],data[6],route,product[2],data[9],1,'Packing',session['UserName'],session['SiteName'],datetime.now(timeZ)))
              # connection is not autocommit by default. So you must commit to save
              # your changes.
              db_connection.commit()
              cur.close()
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM orders WHERE  CLid=%s AND DeliveryDay=%s AND NOT Status =%s AND OperationGroup=%s AND Site=%s  "
              cur.execute(sql, (route,deliveryday,status, OG, Site))
              data2 = cur.fetchall()
              cur.close()
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM orders WHERE  CLid=%s AND DeliveryDay=%s AND Status =%s AND OperationGroup=%s AND Site=%s  "
              cur.execute(sql, (route,deliveryday,status, OG, Site))
              data3 = cur.fetchall()
              cur.close()
              if data2:
                return render_template('actualizacion/Scan.html',Datos =session, data=data2, dataf=data3)
              else:
                return render_template('actualizacion/Scan.html',Datos =session, dataf=data3)
            else:
              flash("Codigo Ean no Encontrado en esta Ruta")
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM orders WHERE  CLid=%s AND DeliveryDay=%s AND NOT Status =%s AND OperationGroup=%s AND Site=%s "
              cur.execute(sql, (route,deliveryday,status, OG, Site))
              data2 = cur.fetchall()
              cur.close()
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM orders WHERE  CLid=%s AND DeliveryDay=%s AND Status =%s AND OperationGroup=%s AND Site=%s "
              cur.execute(sql, (route,deliveryday,status, OG, Site))
              data3 = cur.fetchall()
              cur.close()
              return render_template('actualizacion/Scan.html',Datos =session, data=data2, dataf=data3)

        else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT * FROM orders WHERE Ean=%s AND  CLid=%s AND DeliveryDay=%s AND NOT Status=%s AND OperationGroup=%s AND Site=%s  limit 1"
            cur.execute(sql, (ean,route,deliveryday,status,OG,Site))
            data = cur.fetchone()
            cur.close
            if data :
              Packer=session['UserName']
              OriginalQuantity=data[12]
              CurrentQuantity	=data[16]+1
              PendingQuantity=data[17]-1
              if OriginalQuantity==CurrentQuantity:
                estatus= 'Finished'
              elif CurrentQuantity>0 and PendingQuantity> 0:
                estatus= 'In Process'
              else:
                estatus= 'Pendding'
              ID_Order =data[0]
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Create a new record
              sql = "UPDATE orders SET Packer = %s, CurrentQuantity = %s,PendingQuantity = %s, Status = %s WHERE ID_Order  = %s"
              cur.execute(sql,(Packer,CurrentQuantity,PendingQuantity,estatus,ID_Order,))
              # connection is not autocommit by default. So you must commit to save
              # your changes.
              db_connection.commit()
              cur.close()
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Create a new record
              sql = "INSERT INTO movements (RouteName,FuOrder,CLid,Ean,Description,Quantity,Process,Responsible,Site,DateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
              cur.execute(sql,(data[1],data[6],route,ean,data[9],1,'Packing',session['UserName'],session['SiteName'],datetime.now(timeZ)))
              # connection is not autocommit by default. So you must commit to save
              # your changes.
              db_connection.commit()
              cur.close()
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM orders WHERE  CLid=%s AND DeliveryDay=%s AND NOT Status =%s AND OperationGroup=%s AND Site=%s  "
              cur.execute(sql, (route,deliveryday,status, OG, Site))
              data2 = cur.fetchall()
              cur.close()
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM orders WHERE  CLid=%s AND DeliveryDay=%s AND Status =%s AND OperationGroup=%s AND Site=%s  "
              cur.execute(sql, (route,deliveryday,status, OG, Site))
              data3 = cur.fetchall()
              cur.close()
              if data2:
                return render_template('actualizacion/Scan.html',Datos =session, data=data2, dataf=data3)
              else:
                return render_template('actualizacion/Scan.html',Datos =session, dataf=data3)
            else:
              flash("Codigo Ean no Encontrado en esta Ruta")
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM orders WHERE  CLid=%s AND DeliveryDay=%s AND NOT Status =%s AND OperationGroup=%s AND Site=%s "
              cur.execute(sql, (route,deliveryday,status, OG, Site))
              data2 = cur.fetchall()
              cur.close()
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM orders WHERE  CLid=%s AND DeliveryDay=%s AND Status =%s AND OperationGroup=%s AND Site=%s "
              cur.execute(sql, (route,deliveryday,status, OG, Site))
              data3 = cur.fetchall()
              cur.close()
              return render_template('actualizacion/Scan.html',Datos =session, data=data2, dataf=data3)

  except Exception as error:
    flash(str(error))
    return redirect('/Packing')

# receiving register 
@app.route('/RegistrarReceiving',methods=['POST','GET'])
def registrarReceiving():
  try:
      if request.method == 'POST':
        ReceivingType =  request.form['ReceivingType']
        if request.form['OrderNumber']:
          OrderNumber =  request.form['OrderNumber']
        else:
          OrderNumber =  "No aplica"

        return render_template('actualizacion/receivingscan.html',Datos =session, ReceivingType=ReceivingType,OrderNumber=OrderNumber)
  except Exception as error: 
    flash(str(error))
    return redirect('/Packing')

# receiving mov register 
@app.route('/RegistroMovReceiving/<receivingType>/<orderNumber>',methods=['POST','GET'])
def registroMovReceiving(receivingType,orderNumber):
  try:
      if request.method == 'POST':
        ean =  request.form['ean'].strip()
        cantidad =  request.form['cantidad']
        if session['SiteName']=='CDMX01':
          timeZ = pytz.timezone('America/Mexico_City')
        elif session['SiteName']=='MEDELLIN01':
          timeZ = pytz.timezone('America/Bogota')
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM product WHERE CB_Captura =%s  limit 1  "
        cur.execute(sql, (ean))
        data = cur.fetchone()
        cur.close()
        if data:
          catidad2= int(cantidad)*int(data[4])
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Create a new record
          sql = "INSERT INTO receiving (PurchaseOrder,Type,Ean,EanMuni,ConversionUnit	,Quantity,Description,Responsible,Status,Site,DateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
          cur.execute(sql,(orderNumber,receivingType,ean,data[2],data[4],catidad2,data[3],session['UserName'],'In Process',session['SiteName'],datetime.now(timeZ),))
          # connection is not autocommit by default. So you must commit to save
          # your changes.
          db_connection.commit()
          cur.close()
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Read a single record
          sql = "SELECT * FROM receivingtable WHERE Ean_Muni =%s  limit 1  "
          cur.execute(sql, (data[2]))
          Rdata = cur.fetchone()
          cur.close()
          if Rdata:
            cantidadr = int(Rdata[5])+int(catidad2)
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Create a new record
            sql = "UPDATE receivingtable SET  Cantidad =%s, Fecha_de_Actualizacion=%s WHERE PurchaseOrder=%s AND Type=%s AND Ean_Muni=%s AND  Status=%s AND Site=%s "
            cur.execute(sql,(cantidadr,datetime.now(timeZ),orderNumber,receivingType,data[2],'In Process',session['SiteName'],))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Create a new record
            sql = "INSERT INTO receivingtable (	PurchaseOrder,Type,Ean_Muni,Descripcion,Cantidad,Responsable,	Site,	Status,Fecha_de_Actualizacion) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(orderNumber,receivingType,data[2],data[3],catidad2,session['UserName'],session['SiteName'],'In Process',datetime.now(timeZ),))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Read a single record
          sql = "SELECT PurchaseOrder,	Type,Ean_Muni, Descripcion, Cantidad,Fecha_de_Actualizacion FROM receivingtable WHERE  PurchaseOrder=%s AND Type=%s AND  Responsable =%s AND Status=%s AND Site=%s ORDER BY Fecha_de_Actualizacion DESC"
          cur.execute(sql, (orderNumber,receivingType,session['UserName'],'In Process',session['SiteName'],))
          data2 = cur.fetchall()
          cur.close()
          return render_template('actualizacion/receivingscan.html',Datos =session, data=data2, ReceivingType=receivingType,OrderNumber=orderNumber)
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Create a new record
          sql = "INSERT INTO receiving (PurchaseOrder,Type,Ean,Quantity,Responsible,Status,Site,DateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
          cur.execute(sql,(orderNumber,receivingType,ean,cantidad,session['UserName'],'In Process',session['SiteName'],datetime.now(timeZ),))
          # connection is not autocommit by default. So you must commit to save
          # your changes.
          db_connection.commit()
          cur.close()
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Read a single record
          sql = "SELECT * FROM receivingtable WHERE Ean_Muni =%s  limit 1  "
          cur.execute(sql, (ean))
          Rdata = cur.fetchone()
          cur.close()
          if Rdata:
            cantidadr = int(Rdata[5])+int(cantidad)
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Create a new record
            sql = "UPDATE receivingtable SET  Cantidad =%s, Fecha_de_Actualizacion=%s WHERE PurchaseOrder=%s AND Type=%s AND Ean_Muni=%s AND  Status=%s AND Site=%s "
            cur.execute(sql,(cantidadr,datetime.now(timeZ),orderNumber,receivingType,ean,'In Process',session['SiteName'],))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Create a new record
            sql = "INSERT INTO receivingtable (	PurchaseOrder,Type,Ean_Muni,Descripcion,Cantidad,Responsable,	Site,	Status,Fecha_de_Actualizacion) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(orderNumber,receivingType,ean,'No reistrado',cantidad,session['UserName'],session['SiteName'],'In Process',datetime.now(timeZ),))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Read a single record
          sql = "SELECT PurchaseOrder,	Type,Ean_Muni, Descripcion, Cantidad,Fecha_de_Actualizacion FROM receivingtable WHERE  PurchaseOrder=%s AND Type=%s AND  Responsable =%s AND Status=%s AND Site=%s ORDER BY Fecha_de_Actualizacion DESC"
          cur.execute(sql, (orderNumber,receivingType,session['UserName'],'In Process',session['SiteName'],))
          data2 = cur.fetchall()
          cur.close()
          return render_template('actualizacion/receivingscan.html',Datos =session, data=data2, ReceivingType=receivingType,OrderNumber=orderNumber)
  except Exception as error: 
    flash(str(error))
    return redirect('/Receiving')

# close receipt
@app.route('/CerrarReceiving/<receivingType>/<orderNumber>',methods=['POST','GET'])
def cerrarReceiving(receivingType,orderNumber):
  try:
      link = connectBD()
      db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
      cur= db_connection.cursor()
      # Create a new record
      sql = "UPDATE receiving SET Status = %s WHERE PurchaseOrder=%s AND Type=%s AND  Responsible =%s AND Status=%s"
      cur.execute(sql,('received',orderNumber,receivingType,session['UserName'],'In Process',))
      # connection is not autocommit by default. So you must commit to save
      # your changes.
      db_connection.commit()
      cur.close()
      return redirect('/Receiving')
  except Exception as error:
    flash(str(error))
    return redirect('/Receiving')

# receiving register 
@app.route('/RegistrarInventory',methods=['POST','GET'])
def registrarInventory():
  # try:
      if request.method == 'POST':
        receivingType="Inventory"
        orderNumber="No aplica"
        ean =  request.form['ean']
        cantidad =  request.form['cantidad']
        if session['SiteName']=='CDMX01':
          timeZ = pytz.timezone('America/Mexico_City')
        elif session['SiteName']=='MEDELLIN01':
          timeZ = pytz.timezone('America/Bogota')
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM product WHERE CB_Captura =%s  limit 1  "
        cur.execute(sql, (ean))
        data = cur.fetchone()
        cur.close()
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM inventory WHERE CB_Captura =%s  limit 1  "
        cur.execute(sql, (ean))
        datainv = cur.fetchone()
        cur.close()
        if data:
          cantidad2= int(cantidad)*int(data[4])
          if datainv:
            if datainv[7]== 'finalized':
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Create a new record
              sql = "UPDATE inventory SET Status = %s, Cantidad_Anterior=%s, Cantidad_Actual=%s, inventoryUser=%s,	Fecha_de_Actualizacion=%s WHERE CB_Captura=%s AND Site=%s "
              cur.execute(sql,('In Process',datainv[5],cantidad2,session['UserName'],datetime.now(timeZ),ean,session['SiteName'],))
              # connection is not autocommit by default. So you must commit to save
              # your changes.
              db_connection.commit()
              cur.close()
            else:
              cantidad3=int(datainv[5])+cantidad2
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Create a new record
              sql = "UPDATE inventory SET Cantidad_Actual=%s, inventoryUser=%s WHERE CB_Captura=%s AND Site=%s"
              cur.execute(sql,(cantidad3,session['UserName'],ean, session['SiteName'],))
              # connection is not autocommit by default. So you must commit to save
              # your changes.
              db_connection.commit()
              cur.close()
            catidad2= int(cantidad)*int(data[4])
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Create a new record
            sql = "INSERT INTO receiving (PurchaseOrder,Type,Ean,EanMuni,ConversionUnit	,Quantity,Description,Responsible,Status,Site,DateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(orderNumber,receivingType,ean,data[2],data[4],catidad2,data[3],session['UserName'],'In Process',session['SiteName'],datetime.now(timeZ),))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT PurchaseOrder,	Type,EanMuni, Description, sum(Quantity) FROM receiving WHERE  PurchaseOrder=%s AND Type=%s AND  Responsible =%s AND Status=%s AND Site=%s GROUP BY PurchaseOrder,	Type, EanMuni, Description"
            cur.execute(sql, (orderNumber,receivingType,session['UserName'],'In Process',session['SiteName'],))
            data2 = cur.fetchall()
            cur.close()
            return render_template('form/inventory.html',Datos =session, data=data2)
          else:
            catidad2= int(cantidad)*int(data[4])
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Create a new record
            sql = "INSERT INTO inventory (CB_Captura,EAN_MUNI,Producto,Cantidad_Anterior,Cantidad_Actual,Unidad_de_Medida,Status,inventoryUser,Fecha_de_Actualizacion,Site) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(ean,data[2],data[3],0,cantidad2,data[4],'In Process',session['UserName'],datetime.now(timeZ),session['SiteName'],))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Create a new record
            sql = "INSERT INTO receiving (PurchaseOrder,Type,Ean,EanMuni,ConversionUnit	,Quantity,Description,Responsible,Status,Site,DateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(orderNumber,receivingType,ean,data[2],data[4],catidad2,data[3],session['UserName'],'In Process',session['SiteName'],datetime.now(timeZ),))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT PurchaseOrder,	Type,Ean,EanMuni, Description, sum(Quantity) FROM receiving WHERE  PurchaseOrder=%s AND Type=%s AND  Responsible =%s AND Status=%s AND Site=%s GROUP BY PurchaseOrder,	Type,Ean, EanMuni, Description"
            cur.execute(sql, (orderNumber,receivingType,session['UserName'],'In Process',session['SiteName'],))
            data2 = cur.fetchall()
            cur.close()
            return render_template('form/inventory.html',Datos =session, data=data2)
        else:
          return render_template('actualizacion/Searchproduct.html',Datos =session,ean=ean,cantidad=cantidad)
  # except Exception as error: 
  #   flash(str(error))
  #   return redirect('/Inventory')

# Search Product
@app.route('/FormSearch',methods=['POST','GET'])
def formsearch():  
  try:
      if request.method == 'POST':
        ean =  request.form['ean'].strip()
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM product WHERE CB_Captura  =  %s"
        cur.execute(sql,(ean))
        data = cur.fetchall()
        cur.close()
        if data:
          flash('Producto ya Registrado')
          return redirect('/Product')
        else:
          return render_template('actualizacion/Searchproduct.html',Datos =session,ean=ean)
  except:
    return redirect('/')


# receiving mov register
@app.route('/RegistrarProductoinv/<ean>/<cantidad>',methods=['POST','GET'])
def registrarProductoinv(ean,cantidad):
  try:
      if request.method == 'POST':
        receivingType="Inventory"
        orderNumber="No aplica"
        EAN_MUNI =  request.form['EAN_MUNI']
        Producto =  request.form['Producto']
        if session['SiteName']=='CDMX01':
          timeZ = pytz.timezone('America/Mexico_City')
        elif session['SiteName']=='MEDELLIN01':
          timeZ = pytz.timezone('America/Bogota')
        Factor_de_Conversión =  request.form['Factor_de_Conversión']
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Create a new record
        sql = "INSERT INTO product (CB_Captura,EAN_MUNI,Producto,Factor_de_Conversión) VALUES (%s,%s,%s,%s)"
        cur.execute(sql,(ean,EAN_MUNI,Producto,Factor_de_Conversión,))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        db_connection.commit()
        cur.close()
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM product WHERE CB_Captura =%s  limit 1  "
        cur.execute(sql, (ean))
        data = cur.fetchone()
        cur.close()
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM inventory WHERE CB_Captura =%s  limit 1  "
        cur.execute(sql, (ean))
        datainv = cur.fetchone()
        cur.close()
        if data:
          cantidad2= int(cantidad)*int(data[4])
          if datainv:
            if datainv[7]== 'finalized':
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Create a new record
              sql = "UPDATE inventory SET Status = %s, Cantidad_Anterior=%s, Cantidad_Actual=%s, inventoryUser=5s,	Fecha_de_Actualizacion=%s WHERE CB_Captura=%s AND Site=%s "
              cur.execute(sql,('In Process',datainv[5],cantidad2,session['UserName'],datetime.now(timeZ),ean,session['SiteName'],))
              # connection is not autocommit by default. So you must commit to save
              # your changes.
              db_connection.commit()
              cur.close()
            else:
              cantidad3=int(datainv[5])+cantidad2
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Create a new record
              sql = "UPDATE inventory SET Cantidad_Actual=%s, inventoryUser=%s WHERE CB_Captura=%s AND Site=%s"
              cur.execute(sql,(cantidad3,session['UserName'],ean, session['SiteName'],))
              # connection is not autocommit by default. So you must commit to save
              # your changes.
              db_connection.commit()
              cur.close()
            catidad2= int(cantidad)*int(data[4])
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Create a new record
            sql = "INSERT INTO receiving (PurchaseOrder,Type,Ean,EanMuni,ConversionUnit	,Quantity,Description,Responsible,Status,Site,DateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(orderNumber,receivingType,ean,data[2],data[4],catidad2,data[3],session['UserName'],'In Process',session['SiteName'],datetime.now(timeZ),))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT PurchaseOrder,	Type,EanMuni, Description, sum(Quantity) FROM receiving WHERE  PurchaseOrder=%s AND Type=%s AND  Responsible =%s AND Status=%s AND Site=%s GROUP BY PurchaseOrder,	Type, EanMuni, Description"
            cur.execute(sql, (orderNumber,receivingType,session['UserName'],'In Process',session['SiteName'],))
            data2 = cur.fetchall()
            cur.close()
            return render_template('form/inventory.html',Datos =session, data=data2)
          else:
            catidad2= int(cantidad)*int(data[4])
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Create a new record
            sql = "INSERT INTO inventory (CB_Captura,EAN_MUNI,Producto,Cantidad_Anterior,Cantidad_Actual,Unidad_de_Medida,Status,inventoryUser,Fecha_de_Actualizacion,Site) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(ean,data[2],data[3],0,cantidad2,data[4],'In Process',session['UserName'],datetime.now(timeZ),session['SiteName'],))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Create a new record
            sql = "INSERT INTO receiving (PurchaseOrder,Type,Ean,EanMuni,ConversionUnit	,Quantity,Description,Responsible,Status,Site,DateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(orderNumber,receivingType,ean,data[2],data[4],catidad2,data[3],session['UserName'],'In Process',session['SiteName'],datetime.now(timeZ),))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT PurchaseOrder,	Type,EanMuni, Description, sum(Quantity) FROM receiving WHERE  PurchaseOrder=%s AND Type=%s AND  Responsible =%s AND Status=%s AND Site=%s GROUP BY PurchaseOrder,	Type, EanMuni, Description"
            cur.execute(sql, (orderNumber,receivingType,session['UserName'],'In Process',session['SiteName'],))
            data2 = cur.fetchall()
            cur.close()
            return render_template('form/inventory.html',Datos =session, data=data2)
        else:
          return render_template('actualizacion/Searchproduct.html',Datos =session,ean=ean,cantidad=cantidad )
  except Exception as error:
    flash(str(error))
    return redirect('/Inventory')

# receiving mov register
@app.route('/RegistrarProducto/<ean>',methods=['POST','GET'])
def registrarProducto(ean):
  # try:
      if request.method == 'POST':
        EAN_MUNI =  request.form['EAN_MUNI'].strip()
        Producto =  request.form['Producto']
        Factor_de_Conversión =  request.form['Factor_de_Conversión']
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Create a new record
        sql = "INSERT INTO product (CB_Captura,EAN_MUNI,Producto,Factor_de_Conversión) VALUES (%s,%s,%s,%s)"
        cur.execute(sql,(ean,EAN_MUNI,Producto,Factor_de_Conversión,))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        db_connection.commit()
        cur.close()
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM product WHERE CB_Captura =%s  limit 1  "
        cur.execute(sql, (ean))
        data = cur.fetchone()
        cur.close()
        return render_template('form/product.html',Datos =session, data=data)
  # except Exception as error:
  #   flash(str(error))
  #   return redirect('/Product')

# Search Product
@app.route('/SearchProductinv/<ean>/<cantidad>',methods=['POST','GET'])
def searchProductinv(ean,cantidad):
  try:
      if request.method == 'POST':
        desc =  request.form['desc']
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM product WHERE Producto LIKE '%{}%'"
        cur.execute(sql.format(desc))
        data = cur.fetchall()
        cur.close()
        return render_template('actualizacion/product.html',Datos =session,data=data,ean=ean,cantidad=cantidad )
  except Exception as error:
    flash(str(error))
    return redirect('/Inventory')

# Search Product
@app.route('/SearchProduct/<ean>',methods=['POST','GET'])
def searchProduct(ean):  
  try:
      if request.method == 'POST':
        desc =  request.form['desc']
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM product WHERE Producto LIKE '%{}%'"
        cur.execute(sql.format(desc))
        data = cur.fetchall()
        cur.close()
        return render_template('actualizacion/product.html',Datos =session,data=data,ean=ean)
  except Exception as error: 
    flash(str(error))
    return redirect('/Inventory')

# receiving register 
@app.route('/RegistrarDamage',methods=['POST','GET'])
def registrarDamage():
  # try:
      if request.method == 'POST':
        cantidad =  request.form['cantidad']
        Motivo =  request.form['Motivo']
        ean =  request.form['ean']
        if session['SiteName']=='CDMX01':
          timeZ = pytz.timezone('America/Mexico_City')
        elif session['SiteName']=='MEDELLIN01':
          timeZ = pytz.timezone('America/Bogota')
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM product WHERE CB_Captura =%s  limit 1  "
        cur.execute(sql, (ean))
        data = cur.fetchone()
        cur.close()
        if data:
          catidad2= int(cantidad)*int(data[4])
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Create a new record
          sql = "INSERT INTO mermas (Ean,	EAN_MUNI,Description,Quantity,Reason,Responsible,Status,Site,DateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
          cur.execute(sql,(ean,data[2],data[3],catidad2,Motivo,session['UserName'],'In Process',session['SiteName'],datetime.now(timeZ),))
          # connection is not autocommit by default. So you must commit to save
          # your changes.
          db_connection.commit()
          cur.close()
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Read a single record
          sql = "SELECT	CB_Captura, EAN_MUNI, Producto,Site,  sum(Cantidad_Actual) FROM inventory WHERE 	EAN_MUNI =%s  GROUP BY CB_Captura, EAN_MUNI, Producto,Site limit 1  "
          cur.execute(sql, (data[2]))
          Inv = cur.fetchone()
          cur.close()
          if Inv:
            cantidadinv=int(Inv[4])-int(catidad2)
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Create a new record
            sql = "UPDATE inventory SET Cantidad_Actual = %s, Fecha_de_Actualizacion = %s WHERE EAN_MUNI=%s AND  Site=%s "
            cur.execute(sql,(cantidadinv,datetime.now(timeZ),data[2],session['SiteName']))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Read a single record
          sql = "SELECT EAN_MUNI,	Description,Quantity, Reason FROM mermas WHERE  Responsible = %s And Status = %s AND Site = %s "
          cur.execute(sql, (session['UserName'],'In Process',session['SiteName'],))
          data2 = cur.fetchall()
          cur.close()
          return render_template('form/damage.html',Datos =session, data=data2)
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Read a single record
          sql = "SELECT	CB_Captura, EAN_MUNI, Producto,Site,  sum(Cantidad_Actual) FROM inventory WHERE 	EAN_MUNI =%s  GROUP BY CB_Captura, EAN_MUNI, Producto,Site limit 1  "
          cur.execute(sql, (ean))
          Inv = cur.fetchone()
          cur.close()
          if Inv:
            cantidadinv=int(Inv[4])-int(catidad2)
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Create a new record
            sql = "UPDATE inventory SET Cantidad_Actual = %s, Fecha_de_Actualizacion = %s WHERE EAN_MUNI=%s AND  Site=%s "
            cur.execute(sql,(cantidadinv,datetime.now(timeZ),Inv[1],session['SiteName']))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Create a new record
            sql = "INSERT INTO mermas (Ean,	EAN_MUNI,Description,Quantity,Reason,Responsible,Status,Site,DateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(ean,Inv[1],Inv[2],cantidad,Motivo,session['UserName'],'In Process',session['SiteName'],datetime.now(timeZ),))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Create a new record
            sql = "INSERT INTO mermas (Ean,	EAN_MUNI,Description,Quantity,Reason,Responsible,Status,Site,DateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(ean,ean,'No Registrado',cantidad,Motivo,session['UserName'],'In Process',session['SiteName'],datetime.now(timeZ),))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Read a single record
          sql = "SELECT EAN_MUNI,	Description,Quantity, Reason FROM mermas WHERE  Responsible = %s And Status = %s AND Site = %s"
          cur.execute(sql, (session['UserName'],'In Process',session['SiteName'],))
          data2 = cur.fetchall()
          cur.close()
          return render_template('form/damage.html',Datos =session, data=data2)
  # except Exception as error: 
  #   flash(str(error))
  #   return redirect('/Damage')

# close receipt
@app.route('/CerrarDamage',methods=['POST','GET'])
def cerrarDamage():
  try:
      link = connectBD()
      db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
      cur= db_connection.cursor()
      # Create a new record
      sql = "UPDATE mermas SET 	Status=%s WHERE 	Status=%s AND Responsible=%s AND Site=%s"
      cur.execute(sql,('finalized','In Process',session['UserName'], session['SiteName'],))
      # connection is not autocommit by default. So you must commit to save
      # your changes.
      db_connection.commit()
      cur.close()
      return redirect('/home')
  except Exception as error:
    flash(str(error))
    return redirect('/home')

# close receipt
@app.route('/CerrarInventory',methods=['POST','GET'])
def cerrarInventory():
  try:
      receivingType="Inventory"
      orderNumber="No aplica"
      link = connectBD()
      db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
      cur= db_connection.cursor()
      # Create a new record
      sql = "UPDATE inventory SET 	Status=%s WHERE 	Status=%s AND inventoryUser=%s AND Site=%s"
      cur.execute(sql,('finalized','In Process',session['UserName'], session['SiteName'],))
      # connection is not autocommit by default. So you must commit to save
      # your changes.
      db_connection.commit()
      cur.close()
      link = connectBD()
      db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
      cur= db_connection.cursor()
      # Create a new record
      sql = "UPDATE receiving SET Status = %s WHERE PurchaseOrder=%s AND Type=%s AND  Responsible =%s AND Status=%s"
      cur.execute(sql,('received',orderNumber,receivingType,session['UserName'],'In Process',))
      # connection is not autocommit by default. So you must commit to save
      # your changes.
      db_connection.commit()
      cur.close()
      return redirect('/home')
  except Exception as error:
    flash(str(error))
    return redirect('/home')

# user register
@app.route('/registrar',methods=['POST'])
def registrar():
  try:
      if request.method == 'POST':
        FirstName =  request.form['FirstName']
        LastName =  request.form['LastName']
        User = request.form['User']
        Access =  request.form['Access']
        Site = request.form['Site']

        password = _create_password(request.form['Password'])

        if check_password_hash(password,request.form['Password']) and check_password_hash(password,request.form['ValidatePassword']):
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          sql = "SELECT * FROM users WHERE User=%s Limit 1"
          cur.execute(sql, (User,))
          # Read a single record
          data = cur.fetchone()
          cur.close()
          if data:
            flash("El Usuario Ya Existe")
            return render_template('registro.html',Datos =session)
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Create a new record
            sql = "INSERT INTO users (FirstName,LastName,User,Password,Access,Site) VALUES (%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(FirstName,LastName,User,password,Access,Site,))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
            flash("Registro Correcto")
            return redirect('/registro')
        else:
          flash("Las Contraceñas no Cionciden")
          return redirect('/registro')
  except:
    flash("Registro Fallido")
    return render_template('registro.html',Datos =session)

# cam scan 
@app.route('/Scan',methods=['POST'])
def registro_s_s():
  try:
      if request.method == 'POST':
        DeliveryDate = request.form['DeliveryDate']
        Route = request.form['Route']
        return render_template('form/scan.html')
  except Exception as error: 
    flash(str(error))
    return render_template('form/receiving.html',Datos = session)

# close session
@app.route('/logout')
def Cerrar_session():
  try:
    session.clear()
    return redirect('/')
  except Exception as error: 
    flash(str(error))
    return redirect('/')

# receiving report 
@app.route('/Reporte_receiving/<rowi>',methods=['POST','GET'])
def reporte_receiving(rowi):
  try:
      if request.method == 'POST':
        if request.method == 'GET':
          session['rowi_receiving']=rowi
          row1 = int(session['rowi_receiving'])
          row2 = 50
        else:
            row1 = int(session['rowi_receiving'])
            row2 =50
        if 'valor' in request.form:
          if len(request.form['valor'])>0:
            session['filtro_receiving']=request.form['filtro']
            session['valor_receiving']=request.form['valor']
            if 'datefilter' in request.form:
              if len(request.form['datefilter'])>0:
                daterangef=request.form['datefilter']
                daterange=daterangef.replace("-", "' AND '")
                session['datefilter_receiving']=daterange
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM receiving WHERE {} LIKE \'%{}%\' AND DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['filtro_receiving'],session['valor_receiving'],session['datefilter_receiving'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM receiving WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['filtro_receiving'],session['valor_receiving'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
            else:
              session.pop('datefilter_receiving')
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM receiving WHERE {} LIKE \'%{}%\' WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['filtro_receiving'],session['valor_receiving'],session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
          else:
            if 'datefilter' in request.form:
              if len(request.form['datefilter'])>0:
                if 'valor_receiving' in session:
                  if len(session['valor_receiving'])>0:
                    daterangef=request.form['datefilter']
                    daterange=daterangef.replace("-", "' AND '")
                    session['datefilter_receiving']=daterange
                    link = connectBD()
                    db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                    cur= db_connection.cursor()
                    # Read a single record
                    sql = "SELECT * FROM receiving WHERE {} LIKE \'%{}%\' AND DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['filtro_receiving'],session['valor_receiving'],session['datefilter_receiving'],session['SiteName'],row1,row2)
                    cur.execute(sql)
                    data = cur.fetchall()
                    cur.close()
                    return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
                  else:
                    session.pop('filtro_receiving')
                    session.pop('valor_receiving')
                    link = connectBD()
                    db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                    cur= db_connection.cursor()
                    # Read a single record
                    sql = "SELECT * FROM receiving WHERE DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['datefilter_receiving'],session['SiteName'],row1,row2)
                    cur.execute(sql)
                    data = cur.fetchall()
                    cur.close()
                    return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
                else:
                  daterangef=request.form['datefilter']
                  daterange=daterangef.replace("-", "' AND '")
                  session['datefilter_receiving']=daterange
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM receiving WHERE DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['datefilter_receiving'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
              else:
                if 'valor_receiving' in session:
                  session.pop('filtro_receiving')
                  session.pop('valor_receiving')
                  if 'datefilter_receiving' in session:
                    session.pop('datefilter_receiving')
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
                else:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
            else:
              if 'valor_receiving' in session:
                session.pop('filtro_receiving')
                session.pop('valor_receiving')
              if 'datefilter_receiving' in session:
                session.pop('datefilter_receiving')
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
        elif 'datefilter' in request.form:
          if len(request.form['datefilter'])>0:
            if 'valor_receiving' in session:
              if len(session['valor_receiving'])>0:
                daterangef=request.form['datefilter']
                daterange=daterangef.replace("-", "' AND '")
                session['datefilter_receiving']=daterange
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM receiving WHERE {} LIKE \'%{}%\' AND DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['filtro_receiving'],session['valor_receiving'],session['datefilter_receiving'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
              else:
                session.pop('filtro_receiving')
                session.pop('valor_receiving')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM receiving WHERE DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['datefilter_receiving'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
            else:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM receiving WHERE DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['datefilter_receiving'],session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
          else:
            if 'valor_receiving' in session:
              session.pop('filtro_receiving')
              session.pop('valor_receiving')
            if 'datefilter_receiving' in session:
                session.pop('datefilter_receiving')
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
        else:
          if 'valor_receiving' in session:
            if len(session['valor_receiving'])>0:
              if 'datefilter_receiving' in session:
                if len(session['datefilter_receiving'])>0:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM receiving WHERE {} LIKE \'%{}%\' AND DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['filtro_receiving'],session['valor_receiving'],session['datefilter_receiving'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
                else:
                  session.pop('datefilter_receiving')
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM receiving WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['filtro_receiving'],session['valor_receiving'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM receiving WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['filtro_receiving'],session['valor_receiving'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_receiving.html',Datos = session,Infos =data) 
            else:
              session.pop('filtro_receiving')
              session.pop('valor_receiving')
              if 'datefilter_receiving' in session:
                if len(session['datefilter_receiving'])>0:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM receiving WHERE fecha BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['datefilter_receiving'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
                else:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
          else:
            if 'datefilter_receiving' in session:
              if len(session['datefilter_receiving'])>0:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM receiving WHERE DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['datefilter_receiving'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter_receiving')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
            else:
              if 'datefilter' in request.form:
                if len(request.form['datefilter'])>0:
                  daterangef=request.form['datefilter']
                  daterange=daterangef.replace("-", "' AND '")
                  session['datefilter_receiving']=daterange
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM receiving WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['datefilter_receiving'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
                else:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_receiving.html',Datos = session,Infos =data) 
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_receiving.html',Datos = session,Infos =data) 
        
      else: 
        if request.method == 'GET':
          session['rowi_receiving']=rowi
          row1 = int(session['rowi_receiving'])
          row2 = 50
        else:
          row1 = int(session['rowi_receiving'])
          row2 =50
        if 'valor_receiving' in session:
          if len(session['valor_receiving'])>0:
            if 'datefilter_receiving' in session:
              if len(session['datefilter_receiving'])>0:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM receiving WHERE {} LIKE \'%{}%\' AND DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['filtro_receiving'],session['valor_receiving'],session['datefilter_receiving'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter_receiving')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM receiving WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['filtro_receiving'],session['valor_receiving'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
            else:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM receiving WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['filtro_receiving'],session['valor_receiving'],session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_receiving.html',Datos = session,Infos =data) 
          else:
            session.pop('filtro_receiving')
            session.pop('valor_receiving')
            if 'datefilter_receiving' in session:
              if len(session['datefilter_receiving'])>0:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM receiving WHERE DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['datefilter_receiving'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter_receiving')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
            else:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
        else:
          if 'datefilter_receiving' in session:
            if len(session['datefilter_receiving'])>0:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM receiving WHERE DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['datefilter_receiving'],session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
            else:
              session.pop('datefilter_receiving')
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_receiving.html',Datos = session,Infos =data)
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            return render_template('reportes/t_receiving.html',Datos = session,Infos =data)         
  except Exception as error: 
    flash(str(error))
    return render_template('index.html')

# orders report 
@app.route('/Reporte_orders/<rowi>',methods=['POST','GET'])
def reporte_orders(rowi):
  try:
      if request.method == 'POST':
        if request.method == 'GET':
          session['rowi_orders']=rowi
          row1 = int(session['rowi_orders'])
          row2 = 50
        else:
            row1 = int(session['rowi_orders'])
            row2 =50
        if 'valor' in request.form:
          if len(request.form['valor'])>0:
            session['filtro_orders']=request.form['filtro']
            session['valor_orders']=request.form['valor']
            if 'datefilter' in request.form:
              if len(request.form['datefilter'])>0:
                daterangef=request.form['datefilter']
                daterange=daterangef.replace("-", "' AND '")
                session['datefilter_orders']=daterange
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM orders WHERE {} LIKE \'%{}%\' AND DeliveryDay BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['filtro_orders'],session['valor_orders'],session['datefilter_orders'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_orders.html',Datos = session,Infos =data)
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM orders WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['filtro_orders'],session['valor_orders'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_orders.html',Datos = session,Infos =data)
            else:
              session.pop('datefilter')
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM orders WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['filtro_orders'],session['valor_orders'],session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_orders.html',Datos = session,Infos =data)
          else:
            if 'datefilter' in request.form:
              if len(request.form['datefilter'])>0:
                if 'valor_orders' in session:
                  if len(session['valor_orders'])>0:
                    daterangef=request.form['datefilter']
                    daterange=daterangef.replace("-", "' AND '")
                    session['datefilter_orders']=daterange
                    link = connectBD()
                    db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                    cur= db_connection.cursor()
                    # Read a single record
                    sql = "SELECT * FROM orders WHERE {} LIKE \'%{}%\' AND DeliveryDay BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['filtro_orders'],session['valor_orders'],session['datefilter_orders'],session['SiteName'],row1,row2)
                    cur.execute(sql)
                    data = cur.fetchall()
                    cur.close()
                    return render_template('reportes/t_orders.html',Datos = session,Infos =data)
                  else:
                    session.pop('filtro_orders')
                    session.pop('valor_orders')
                    link = connectBD()
                    db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                    cur= db_connection.cursor()
                    # Read a single record
                    sql = "SELECT * FROM orders WHERE DeliveryDay BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['datefilter_orders'],session['SiteName'],row1,row2)
                    cur.execute(sql)
                    data = cur.fetchall()
                    cur.close()
                    return render_template('reportes/t_orders.html',Datos = session,Infos =data)
                else:
                  daterangef=request.form['datefilter']
                  daterange=daterangef.replace("-", "' AND '")
                  session['datefilter_orders']=daterange
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM orders WHERE DeliveryDay BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['datefilter_orders'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_orders.html',Datos = session,Infos =data)
              else:
                if 'valor_orders' in session:
                  session.pop('filtro_orders')
                  session.pop('valor_orders')
                if 'datefilter_orders' in session:
                  session.pop('datefilter_orders')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM orders WHERE Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
            else:
              if 'valor_orders' in session:
                session.pop('filtro_orders')
                session.pop('valor_orders')
              if 'datefilter_orders' in session:
                  session.pop('datefilter_orders')
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM orders WHERE Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_orders.html',Datos = session,Infos =data)

        else:
          if 'valor_orders' in session:
            if len(session['valor_orders'])>0:
              if 'datefilter_orders' in session:
                if len(session['datefilter_orders'])>0:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM orders WHERE {} LIKE \'%{}%\' AND DeliveryDay BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['filtro_orders'],session['valor_orders'],session['datefilter_orders'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_orders.html',Datos = session,Infos =data)
                else:
                  session.pop('datefilter_orders')
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM orders WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['filtro_orders'],session['valor_orders'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_orders.html',Datos = session,Infos =data)
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM orders WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['filtro_orders'],session['valor_orders'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_orders.html',Datos = session,Infos =data) 
            else:
              session.pop('filtro_orders')
              session.pop('valor_orders')
              if 'datefilter_orders' in session:
                if len(session['datefilter_orders'])>0:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM orders WHERE DeliveryDay BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['datefilter_orders'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_orders.html',Datos = session,Infos =data)
                else:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM orders WHERE Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_orders.html',Datos = session,Infos =data)
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM orders WHERE Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_orders.html',Datos = session,Infos =data)
          else:
            if 'datefilter_orders' in session:
              if len(session['datefilter_orders'])>0:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM orders WHERE DeliveryDay BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['datefilter_orders'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_orders.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter_orders')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                cur.execute('SELECT * FROM orders WHERE Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_orders.html',Datos = session,Infos =data)
            else:
              if 'datefilter' in request.form:
                if len(request.form['datefilter'])>0:
                  daterangef=request.form['datefilter']
                  daterange=daterangef.replace("-", "' AND '")
                  session['datefilter_orders']=daterange
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM orders WHERE  DeliveryDay BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['datefilter_orders'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_orders.html',Datos = session,Infos =data)
                else:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM orders WHERE Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_orders.html',Datos = session,Infos =data) 
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM orders WHERE Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_orders.html',Datos = session,Infos =data) 
      else: 
        if request.method == 'GET':
          session['rowi_orders']=rowi
          row1 = int(session['rowi_orders'])
          row2 = 50
        else:
          row1 = int(session['rowi_orders'])
          row2 =50
        if 'valor_orders' in session:
          if len(session['valor_orders'])>0:
            if 'datefilter_orders' in session:
              if len(session['datefilter_orders'])>0:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM orders WHERE {} LIKE \'%{}%\' AND DeliveryDay BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['filtro_orders'],session['valor_orders'],session['datefilter_orders'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_orders.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter_orders')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM orders WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['filtro_orders'],session['valor_orders'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_orders.html',Datos = session,Infos =data)
            else:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM orders WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['filtro_orders'],session['valor_orders'],session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_orders.html',Datos = session,Infos =data) 
          else:
            session.pop('filtro_orders')
            session.pop('valor_orders')
            if 'datefilter_orders' in session:
              if len(session['datefilter_orders'])>0:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM orders WHERE DeliveryDay BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['datefilter_orders'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_orders.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter_orders')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM orders WHERE Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_orders.html',Datos = session,Infos =data)
            else:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM orders WHERE Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_orders.html',Datos = session,Infos =data)
        else:
          if 'datefilter_orders' in session:
            if len(session['datefilter_orders'])>0:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM orders WHERE DeliveryDay BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['datefilter_orders'],session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_orders.html',Datos = session,Infos =data)
            else:
              session.pop('datefilter_orders')
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM orders WHERE Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_orders.html',Datos = session,Infos =data)
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT * FROM orders WHERE Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            return render_template('reportes/t_orders.html',Datos = session,Infos =data)         
  except Exception as error: 
    flash(str(error))
    return render_template('index.html')#

# movements report 
@app.route('/Reporte_movements/<rowi>',methods=['POST','GET'])
def reporte_movements(rowi):
  try:
      if request.method == 'POST':
        if request.method == 'GET':
          session['rowi_movements']=rowi
          row1 = int(session['rowi_movements'])
          row2 = 50
        else:
            row1 = int(session['rowi_movements'])
            row2 =50
        if 'valor' in request.form:
          if len(request.form['valor'])>0:
            session['filtro_movements']=request.form['filtro']
            session['valor_movements']=request.form['valor']
            if 'datefilter' in request.form:
              if len(request.form['datefilter'])>0:
                daterangef=request.form['datefilter']
                daterange=daterangef.replace("-", "' AND '")
                session['datefilter_movements']=daterange
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM movements WHERE {} LIKE \'%{}%\' AND DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['filtro_movements'],session['valor_movements'],session['datefilter_movements'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_movements.html',Datos = session,Infos =data)
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM movements WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['filtro_movements'],session['valor_movements'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_movements.html',Datos = session,Infos =data)
            else:
              session.pop('datefilter')
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM movements WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['filtro_movements'],session['valor_movements'],session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_movements.html',Datos = session,Infos =data)
          else:
            if 'datefilter' in request.form:
              if len(request.form['datefilter'])>0:
                if 'valor_movements' in session:
                  if len(session['valor_movements'])>0:
                    daterangef=request.form['datefilter']
                    daterange=daterangef.replace("-", "' AND '")
                    session['datefilter_movements']=daterange
                    link = connectBD()
                    db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                    cur= db_connection.cursor()
                    # Read a single record
                    sql = "SELECT * FROM movements WHERE {} LIKE \'%{}%\' AND  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['filtro_movements'],session['valor_movements'],session['datefilter_movements'],session['SiteName'],row1,row2)
                    cur.execute(sql)
                    data = cur.fetchall()
                    cur.close()
                    return render_template('reportes/t_movements.html',Datos = session,Infos =data)
                  else:
                    session.pop('filtro_movements')
                    session.pop('valor_movements')
                    link = connectBD()
                    db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                    cur= db_connection.cursor()
                    # Read a single record
                    sql = "SELECT * FROM movements WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['datefilter_movements'],session['SiteName'],row1,row2)
                    cur.execute(sql)
                    data = cur.fetchall()
                    cur.close()
                    return render_template('reportes/t_movements.html',Datos = session,Infos =data)
                else:
                  daterangef=request.form['datefilter']
                  daterange=daterangef.replace("-", "' AND '")
                  session['datefilter_movements']=daterange
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM movements WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['datefilter_movements'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_movements.html',Datos = session,Infos =data)
              else:
                if 'valor_movements' in session:
                  session.pop('filtro_movements')
                  session.pop('valor_movements')
                if 'datefilter_movements' in session:
                  session.pop('datefilter_movements')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM movements WHERE Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
            else:
              if 'valor_movements' in session:
                session.pop('filtro_movements')
                session.pop('valor_movements')
              if 'datefilter_movements' in session:
                  session.pop('datefilter_movements')
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM movements WHERE Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_movements.html',Datos = session,Infos =data)

        else:
          if 'valor_movements' in session:
            if len(session['valor_movements'])>0:
              if 'datefilter_movements' in session:
                if len(session['datefilter_movements'])>0:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM movements WHERE {} LIKE \'%{}%\' AND  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['filtro_movements'],session['valor_movements'],session['datefilter_movements'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_movements.html',Datos = session,Infos =data)
                else:
                  session.pop('datefilter_movements')
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM movements WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['filtro_movements'],session['valor_movements'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_movements.html',Datos = session,Infos =data)
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM movements WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['filtro_movements'],session['valor_movements'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_movements.html',Datos = session,Infos =data) 
            else:
              session.pop('filtro_movements')
              session.pop('valor_movements')
              if 'datefilter_movements' in session:
                if len(session['datefilter_movements'])>0:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM movements WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['datefilter_movements'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_movements.html',Datos = session,Infos =data)
                else:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM movements WHERE Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_movements.html',Datos = session,Infos =data)
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM movements WHERE Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_movements.html',Datos = session,Infos =data)
          else:
            if 'datefilter_movements' in session:
              if len(session['datefilter_movements'])>0:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM movements WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['datefilter_movements'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_movements.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter_movements')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                cur.execute('SELECT * FROM movements WHERE Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_movements.html',Datos = session,Infos =data)
            else:
              if 'datefilter' in request.form:
                if len(request.form['datefilter'])>0:
                  daterangef=request.form['datefilter']
                  daterange=daterangef.replace("-", "' AND '")
                  session['datefilter_movements']=daterange
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM movements WHERE   DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['datefilter_movements'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_movements.html',Datos = session,Infos =data)
                else:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM movements WHERE Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_movements.html',Datos = session,Infos =data) 
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM movements WHERE Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_movements.html',Datos = session,Infos =data) 
      else: 
        if request.method == 'GET':
          session['rowi_movements']=rowi
          row1 = int(session['rowi_movements'])
          row2 = 50
        else:
          row1 = int(session['rowi_movements'])
          row2 =50
        if 'valor_movements' in session:
          if len(session['valor_movements'])>0:
            if 'datefilter_movements' in session:
              if len(session['datefilter_movements'])>0:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM movements WHERE {} LIKE \'%{}%\' AND  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['filtro_movements'],session['valor_movements'],session['datefilter_movements'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_movements.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter_movements')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM movements WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['filtro_movements'],session['valor_movements'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_movements.html',Datos = session,Infos =data)
            else:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM movements WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['filtro_movements'],session['valor_movements'],session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_movements.html',Datos = session,Infos =data) 
          else:
            session.pop('filtro_movements')
            session.pop('valor_movements')
            if 'datefilter_movements' in session:
              if len(session['datefilter_movements'])>0:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM movements WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['datefilter_movements'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_movements.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter_movements')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM movements WHERE Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_movements.html',Datos = session,Infos =data)
            else:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM movements WHERE Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_movements.html',Datos = session,Infos =data)
        else:
          if 'datefilter_movements' in session:
            if len(session['datefilter_movements'])>0:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM movements WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['datefilter_movements'],session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_movements.html',Datos = session,Infos =data)
            else:
              session.pop('datefilter_movements')
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM movements WHERE Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_movements.html',Datos = session,Infos =data)
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT * FROM movements WHERE Site =\'{}\' ORDER BY ID_Mov DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            return render_template('reportes/t_movements.html',Datos = session,Infos =data)         
  except Exception as error: 
    flash(str(error))
    return render_template('index.html')

# receiving  dowload report
@app.route('/csvreceiving',methods=['POST','GET'])
def crear_csvreceiving():
  try:
    site=session['SiteName']
    row1 = 0
    row2 =50000
    if 'valor_receiving' in session:
      if len(session['valor_receiving'])>0:
        if 'datefilter_receiving' in session:
          if len(session['datefilter_receiving'])>0:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM receiving WHERE {} LIKE \'%{}%\' AND DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}'.format(session['filtro_receiving'],session['valor_receiving'],session['datefilter_receiving'],session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM receiving WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}'.format(session['filtro_receiving'],session['valor_receiving'],session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM receiving WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}'.format(session['filtro_receiving'],session['valor_receiving'],session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
      else:
        if 'datefilter_receiving' in session:
          if len(session['datefilter_receiving'])>0:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM receiving WHERE DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}'.format(session['datefilter_receiving'],session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
    else:
      if 'datefilter_receiving' in session:
        if len(session['datefilter_receiving'])>0:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM receiving WHERE DATE(DateTime) BETWEEN \'{}\' AND ORDER BY ID_Receiving DESC  Site =\'{}\' LIMIT {}, {}'.format(session['datefilter_receiving'],session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
      else:
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        cur.execute('SELECT * FROM receiving WHERE Site =\'{}\' ORDER BY ID_Receiving DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
        data = cur.fetchall()
        cur.close()
    datos="ID Receiving"+","+"Purchase Order"+","+"Type"+","+"Ean"+","+"Ean Muni"+","+"Conversion Unit"+","+"Quantity"+","+"Description"+"Responsible"+","+"Status"+","+"	Site"+","+"	Date Time"+"\n"
    for res in data:
      datos+=str(res[0])
      datos+=","+str(res[1]).replace(","," ")
      datos+=","+str(res[2]).replace(","," ")
      datos+=","+str(res[3]).replace(","," ")
      datos+=","+str(res[4]).replace(","," ")
      datos+=","+str(res[5]).replace(","," ")
      datos+=","+str(res[6]).replace(","," ")
      datos+=","+str(res[7]).replace(","," ")
      datos+=","+str(res[8]).replace(","," ")
      datos+=","+str(res[9]).replace(","," ")
      datos+=","+str(res[10]).replace(","," ")
      datos+=","+str(res[11]).replace(","," ")
      datos+="\n"

    response = make_response(datos)
    response.headers["Content-Disposition"] = "attachment; filename="+"Reportre_receiving-"+str(datetime.today())+".csv"; 
    return response
  except Exception as error: 
    flash(str(error))

# orders  dowload report
@app.route('/csvorders',methods=['POST','GET'])
def crear_csvorders():
  try:
    site=session['SiteName']
    row1 = 0
    row2 =50000
    if 'valor_orders' in session:
      if len(session['valor_orders'])>0:
        if 'datefilter_orders' in session:
          if len(session['datefilter_orders'])>0:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM orders WHERE {} LIKE \'%{}%\' AND 	DeliveryDay BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}'.format(session['filtro_orders'],session['valor_orders'],session['datefilter_orders'],session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM orders WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}'.format(session['filtro_orders'],session['valor_orders'],session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM orders WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}'.format(session['filtro_orders'],session['valor_orders'],session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
      else:
        if 'datefilter_orders' in session:
          if len(session['datefilter_orders'])>0:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM orders WHERE 	DeliveryDay BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}'.format(session['datefilter_orders'],session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM orders WHERE Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM orders WHERE Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
    else:
      if 'datefilter_orders' in session:
        if len(session['datefilter_orders'])>0:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM orders WHERE 	DeliveryDay BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}'.format(session['datefilter_orders'],session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM orders WHERE Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
      else:
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        cur.execute('SELECT * FROM orders WHERE Site =\'{}\' ORDER BY ID_Order DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
        data = cur.fetchall()
        cur.close()
    datos="ID Order"+","+"Route Name"+","+"FU Name"+","+"Service Zone"+","+"FK Order"+","+"Packer"+","+"Fu Order"+","+"Ean"+","+"Operation Group"+","+"Product Name"+","+"Type"+","+"Delivery Day"+","+"Original Quantity"+","+"Vendedor"+","+"CL id"+","+"Stop"+","+"Current Quantity"+","+"Pending Quantity"+","+"Status"+","+"Site"+","+"\n"
    for res in data:
      datos+=str(res[0]).replace(","," ")
      datos+=","+str(res[1]).replace(","," ")
      datos+=","+str(res[2]).replace(","," ")
      datos+=","+str(res[3]).replace(","," ")
      datos+=","+str(res[4]).replace(","," ")
      datos+=","+str(res[5]).replace(","," ")
      datos+=","+str(res[6]).replace(","," ")
      datos+=","+str(res[7]).replace(","," ")
      datos+=","+str(res[8]).replace(","," ")
      datos+=","+str(res[9]).replace(","," ")
      datos+=","+str(res[10]).replace(","," ")
      datos+=","+str(res[11]).replace(","," ")
      datos+=","+str(res[12]).replace(","," ")
      datos+=","+str(res[13]).replace(","," ")
      datos+=","+str(res[14]).replace(","," ")
      datos+=","+str(res[15]).replace(","," ")
      datos+=","+str(res[16]).replace(","," ")
      datos+=","+str(res[17]).replace(","," ")
      datos+=","+str(res[18]).replace(","," ")
      datos+=","+str(res[19]).replace(","," ")
      datos+="\n"

    response = make_response(datos)
    response.headers["Content-Disposition"] = "attachment; filename="+"orders-"+str(datetime.today())+".csv"; 
    return response
  except Exception as error: 
    flash(str(error))

# movements  dowload report
@app.route('/csvmovements',methods=['POST','GET'])
def crear_ccsvmovements():
  try:
    site=session['SiteName']
    row1 = 0
    row2 =5000
    if 'valor_movements' in session:
      if len(session['valor_movements'])>0:
        if 'datefilter_movements' in session:
          if len(session['datefilter'])>0:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM movements WHERE {} LIKE \'%{}%\' AND  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\'  ORDER BY ID_Mov DESC  LIMIT {}, {}'.format(session['filtro_movements'],session['valor_movements'],session['datefilter_movements'],session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM movements WHERE {} LIKE \'%{}%\' AND Site =\'{}\'  ORDER BY ID_Mov DESC  LIMIT {}, {}'.format(session['filtro_movements'],session['valor_movements'],session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM movements WHERE {} LIKE \'%{}%\' AND Site =\'{}\'  ORDER BY ID_Mov DESC  LIMIT {}, {}'.format(session['filtro_movements'],session['valor_movements'],session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
      else:
        if 'datefilter_movements' in session:
          if len(session['datefilter_movements'])>0:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM movements WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\'  ORDER BY ID_Mov DESC  LIMIT {}, {}'.format(session['datefilter_movements'],session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM movements WHERE Site =\'{}\'  ORDER BY ID_Mov DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM movements WHERE Site =\'{}\'  ORDER BY ID_Mov DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
    else:
      if 'datefilter_movements' in session:
        if len(session['datefilter_movements'])>0:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM movements WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\'  ORDER BY ID_Mov DESC  LIMIT {}, {}'.format(session['datefilter_movements'],session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM movements WHERE Site =\'{}\'  ORDER BY ID_Mov DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
      else:
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        cur.execute('SELECT * FROM movements WHERE Site =\'{}\'  ORDER BY ID_Mov DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
        data = cur.fetchall()
        cur.close()
    datos="ID Mov"+","+"Route Name"+","+"Fu Order"+","+"CL id"+","+"Ean"+","+"Description"+","+"Quantity"+","+"Process"+","+"Responsible"+","+"Site"+","+"Date Time"+","+"\n"
    for res in data:
      datos+=str(res[0]).replace(","," ")
      datos+=","+str(res[1]).replace(","," ")
      datos+=","+str(res[2]).replace(","," ")
      datos+=","+str(res[3]).replace(","," ")
      datos+=","+str(res[4]).replace(","," ")
      datos+=","+str(res[5]).replace(","," ")
      datos+=","+str(res[6]).replace(","," ")
      datos+=","+str(res[7]).replace(","," ")
      datos+=","+str(res[8]).replace(","," ")
      datos+=","+str(res[9]).replace(","," ")
      datos+=","+str(res[10]).replace(","," ")
      datos+="\n"

    response = make_response(datos)
    response.headers["Content-Disposition"] = "attachment; filename="+"Rezagos-"+str(datetime.today())+".csv"; 
    return response
  except Exception as error: 
    flash(str(error))

# files form 
@app.route('/files',methods=['POST','GET'])
def Files_():
  try:
    if 'FullName' in session:
      return render_template('form/files.html',Datos=session)
    else:
      return redirect('/')
  except Exception as error: 
    flash(str(error))

# data file register 
@app.route('/CargarDatos',methods=['POST','GET'])
def uploadFiles():
  # try:
    if 'FullName' in session:
      # get the uploaded file
      file =request.files['datos']
      Base =request.form['base']
      if Base=='Product':
        file.save(os.path.join(UPLOAD_FOLDER, "datos.csv"))
        with open(UPLOAD_FOLDER+'datos.csv',"r", encoding="utf8", errors='ignore') as csv_file:
          data=csv.reader(csv_file, delimiter=',')
          i=0
          for row in data:
            if i >0:
              if row[2] != '#N/A':
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8mb4", init_command="set names utf8mb4")
                cur= db_connection.cursor()
                # Create a new record
                sql = "INSERT INTO product (CB_Captura,  EAN_MUNI, Producto, Factor_de_Conversión) VALUES (%s,%s,%s,%s)"
                cur.execute(sql,(row[0], row[1], row[2], row[3],))
                # connection is not autocommit by default. So you must commit to save
                # your changes.
                db_connection.commit()
                cur.close()
            i+=1 
        flash(str(i)+' Registros Exitoso')
        return redirect('/files')
        
      elif Base=='P&P':
        file.save(os.path.join(UPLOAD_FOLDER, "datos.csv"))
        with open(UPLOAD_FOLDER+'datos.csv',"r", encoding="utf8", errors='ignore') as csv_file:
          data=csv.reader(csv_file, delimiter=',')
          i=0
          for row in data:
            if i >0:
              routeName= row[1]
              FUName=row[4]
              Service_Zone=row[13]
              fk_order= row[15]
              packer=row[5]
              FuOrder=row[14]
              ean=row[7]
              operationGroup=row[12]
              productName=row[8]
              type=row[5]
              deliveryDate=row[0]
              originalQuantity=int(row[11])
              Vendor=row[9]
              CLid=row[3]
              Stop=row[2]
              currentQuantity=int(row[10])
              pendingQuantity=int(originalQuantity)-int(currentQuantity)
              if originalQuantity==currentQuantity:
                status= 'Finished'
              elif currentQuantity>0 and pendingQuantity> 0:
                status= 'In Process'
              else:
                status= 'Pendding'
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
                cur.execute(sql,(routeName,FUName,Service_Zone,fk_order,packer,FuOrder,ean,operationGroup,productName,type,deliveryDate,originalQuantity,Vendor,CLid,Stop,currentQuantity,pendingQuantity,status,session['SiteName'],))
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
            i+=1 
        flash(str(i)+' Registros Exitoso')
        return redirect('/files')
  # except Exception as error:
  #   flash(str(error))
  #   return redirect('/files')

# cam scan fuction
@app.route('/scanercam',methods=['POST','GET'])
def scancam():
  cap = cv2.VideoCapture(0)
  cap.set(3,640)
  cap.set(4,480)
  i=0
  while i<1:
      success,img= cap.read()
      for barcode in decode(img):
          myData= barcode.data.decode('utf-8')
          print(myData)
          pts= np.array([barcode.polygon],np.int32)
          pts= pts.reshape((-1,1,2))
          cv2.polylines(img,[pts],True,(255,0,255),5)
          i+=1
      cv2.imshow('Result',img)
      cv2.waitKey(1)

# fuction main   
if __name__=='__main__':
    app.run(port = 3000, debug =True)