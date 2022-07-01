from flask import Flask, sessions, render_template, request, redirect, url_for, flash, session, make_response, Response, jsonify #pip install flask
# import cv2 #pip install opencv-python-headless or pip install opencv-python
# import numpy as np  
# from pyzbar.pyzbar import decode #pip install pyzbar or pip install pyzbar[scripts]
from werkzeug.security import generate_password_hash, check_password_hash #pip install -U Werkzeug
from datetime import datetime, date #pip install datetime pip install pytz
import pytz 
import csv
from appaditional.connect import connectBD
import pymysql #pip install pymysql #pip install mysql-connector-python-rf
import os
  
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
      sql = "SELECT FirstName, User FROM users WHERE User=%s Limit 1"
      cur.execute(sql, (usuario,))
      # Read a single record
      data = cur.fetchone()
      cur.close()
      if data :
        username = data[0]
        user = data[1]
        return render_template('inicio.html',username=username,user=user)
      else:
        return render_template('index.html')
  else:
    return redirect('/')
 
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
 
 # home page 
@app.route('/mermas',methods=['POST','GET'])
def mermas():
  try:
    if 'FullName' in session:
      return render_template('mermas.html',Datos = session)
    else:
      flash("Inicia Sesion")
      return redirect('/')
  except Exception as error:
    flash(str(error))
    return redirect('/') 
   
# user validation
@app.route('/validar/<usuario>', methods=['POST'])
def validarcontrasena(usuario):
  try:
    if request.method == 'POST':
      clave = request.form['clave']
      link = connectBD()
      db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
      cur= db_connection.cursor()
      sql = "SELECT FirstName, LastName, Password, Access, Site FROM users WHERE User=%s Limit 1"
      cur.execute(sql, (usuario,))
      # Read a single record
      data = cur.fetchone()
      cur.close()
      if data :
        if check_password_hash(data[2],clave):
          session['UserName'] = data[0]
          session['FullName'] = data[0] +" "+ data[1]
          session['User'] = usuario
          session['SiteName'] = data[4]
          session['Rango'] = data[3]
          return redirect('/home')
        else:
          flash('Contraseña Incorrecta')
          return redirect('/')
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
      return redirect('/')
  except Exception as error:
    flash(str(error))
    return redirect('/') 

# # packing form 
# @app.route('/Packing',methods=['POST','GET'])
# def packing():
  # try:
  #   if 'FullName' in session:
  #     return render_template('form/packing.html',Datos = session)
  #   else:
  #     flash("Inicia Sesion")
  #     return redirect('/')
  # except Exception as error:
  #   flash(str(error))
  #   return redirect('/') 

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
@app.route('/Damage/<type>',methods=['POST','GET'])
def damage(type):
  try:
    if 'FullName' in session:
      if type == 'cpg':
        return render_template('form/damagerefrigecpg.html',Datos = session,type=type)
      elif type == 'fruver':
        return render_template('form/damagefruver.html',Datos = session,type=type)
      elif type == 'Refrigerados':
        return render_template('form/damagerefrigecpg.html',Datos = session,type=type)
      elif type == 'eggs':
        return render_template('form/damageeggs.html',Datos = session,type=type)
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
    return redirect('/home')
  except Exception as error:
    flash(str(error))
    return redirect('/')

# # packing register 
# @app.route('/RegistrarPacking',methods=['POST','GET'])
# def registroP():
#   try:
#       if request.method == 'POST':
#         deliveryday =  request.form['deliveryday']
#         clid =  request.form['route']
#         og =  request.form['OG']
#         Site =  session['SiteName']
#         status="Finished"
#         link = connectBD()
#         db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#         cur= db_connection.cursor()
#         # Read a single record
#         sql = "SELECT RouteName, FuOrder, Ean, ProductName, OriginalQuantity, CurrentQuantity, Status FROM `orders` WHERE CLid=%s AND DeliveryDay=%s AND NOT Status =%s AND OperationGroup=%s AND Site=%s "
#         cur.execute(sql, (clid,deliveryday,status,og,Site, ))
#         data = cur.fetchall()
#         cur.close()
#         link = connectBD()
#         db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#         cur= db_connection.cursor()
#         # Read a single record
#         sql = "SELECT RouteName, FuOrder, Ean, ProductName, OriginalQuantity, CurrentQuantity, Status FROM `orders` WHERE CLid=%s AND DeliveryDay=%s AND  Status =%s AND OperationGroup=%s AND Site=%s "
#         cur.execute(sql, (clid,deliveryday,status,og,Site, ))
#         data3 = cur.fetchall()
#         cur.close()
#         if data :
#           return render_template('actualizacion/Scan.html',Datos =session, data=data,dataf=data3,deliveryday=deliveryday,clid=clid,OG=og)
#         else:
#           flash("No hay Ordenes Pendientes es esta ruta")
#           return redirect('/Packing')
#       else:
#         redirect('/Packing')
#   except Exception as error: 
#     flash(str(error))
#     return redirect('/Packing')

# # packin mov register
# @app.route('/RegistroMovPacking/<clid>/<deliveryday>/<OG>',methods=['POST','GET'])
# def registroMovPacking(clid,deliveryday,OG):
#   try:
#       if request.method == 'POST':
#         ean =  request.form['ean'].strip()
#         status="Finished"
#         Site=session['SiteName']
#         if session['SiteName']=='CDMX01':
#           timeZ = pytz.timezone('America/Mexico_City')
#         elif session['SiteName']=='MEDELLIN01':
#           timeZ = pytz.timezone('America/Bogota')
#         link = connectBD()
#         db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#         cur= db_connection.cursor()
#         # Read a single record
#         sql = "SELECT * FROM product WHERE CB_Captura =%s  limit 1  "
#         cur.execute(sql, (ean))
#         product = cur.fetchone()
#         cur.close()
#         if product:
#             link = connectBD()
#             db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#             cur= db_connection.cursor()
#             # Read a single record
#             sql = "SELECT * FROM orders WHERE Ean=%s AND  CLid=%s AND DeliveryDay=%s AND NOT Status=%s AND OperationGroup=%s AND Site=%s  limit 1"
#             cur.execute(sql, (product[2],clid,deliveryday,status,OG,Site))
#             data = cur.fetchone()
#             cur.close()
#             if data :
#               Packer=session['UserName']
#               OriginalQuantity=data[12]
#               CurrentQuantity	=int(data[16])+int(product[4])
#               PendingQuantity=int(data[17])-int(product[4])
#               if OriginalQuantity==CurrentQuantity:
#                 estatus= 'Finished'
#               elif CurrentQuantity>0 and PendingQuantity> 0:
#                 estatus= 'In Process'
#               else:
#                 estatus= 'Pendding'
#               ID_Order =data[0]
#               link = connectBD()
#               db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#               cur= db_connection.cursor()
#               # Create a new record
#               sql = "UPDATE orders SET Packer = %s, CurrentQuantity = %s,PendingQuantity = %s, Status = %s WHERE ID_Order  = %s"
#               cur.execute(sql,(Packer,CurrentQuantity,PendingQuantity,estatus,ID_Order,))
#               # connection is not autocommit by default. So you must commit to save
#               # your changes.
#               db_connection.commit()
#               cur.close()
#               link = connectBD()
#               db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#               cur= db_connection.cursor()
#               # Create a new record
#               sql = "INSERT INTO movements (RouteName,FuOrder,CLid,Ean,Description,Quantity,Process,Responsible,Site,DateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#               cur.execute(sql,(data[1],data[6],clid,product[2],data[9],1,'Packing',session['UserName'],session['SiteName'],datetime.now(timeZ)))
#               # connection is not autocommit by default. So you must commit to save
#               # your changes.
#               db_connection.commit()
#               cur.close()
#               link = connectBD()
#               db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#               cur= db_connection.cursor()
#               # Read a single record
#               sql = "SELECT RouteName, FuOrder, Ean, ProductName, OriginalQuantity, CurrentQuantity, Status FROM orders WHERE  CLid=%s AND DeliveryDay=%s AND NOT Status =%s AND OperationGroup=%s AND Site=%s  "
#               cur.execute(sql, (clid,deliveryday,status, OG, Site))
#               data2 = cur.fetchall()
#               cur.close()
#               link = connectBD()
#               db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#               cur= db_connection.cursor()
#               # Read a single record
#               sql = "SELECT RouteName, FuOrder, Ean, ProductName, OriginalQuantity, CurrentQuantity, Status FROM orders WHERE  CLid=%s AND DeliveryDay=%s AND Status =%s AND OperationGroup=%s AND Site=%s  "
#               cur.execute(sql, (clid,deliveryday,status, OG, Site))
#               data3 = cur.fetchall()
#               cur.close()
#               if data2:
#                 return render_template('actualizacion/Scan.html',Datos =session, data=data2,clid=clid,deliveryday=deliveryday,OG=OG)
#               else:
#                 return render_template('actualizacion/Scan.html',Datos =session, dataf=data3,clid=clid,deliveryday=deliveryday,OG=OG)
#             else:
#               flash("Codigo Ean no Encontrado en esta Ruta")
              
#               link = connectBD()
#               db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#               cur= db_connection.cursor()
#               # Read a single record
#               sql = "SELECT RouteName, FuOrder, Ean, ProductName, OriginalQuantity, CurrentQuantity, Status FROM orders WHERE  CLid=%s AND DeliveryDay=%s AND NOT Status =%s AND OperationGroup=%s AND Site=%s "
#               cur.execute(sql, (clid,deliveryday,status, OG, Site))
#               data2 = cur.fetchall()
#               cur.close()
#               link = connectBD()
#               db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#               cur= db_connection.cursor()
#               # Read a single record
#               sql = "SELECT RouteName, FuOrder, Ean, ProductName, OriginalQuantity, CurrentQuantity, Status FROM orders WHERE  CLid=%s AND DeliveryDay=%s AND Status =%s AND OperationGroup=%s AND Site=%s "
#               cur.execute(sql, (clid,deliveryday,status, OG, Site))
#               data3 = cur.fetchall()
#               cur.close()
#               return render_template('actualizacion/Scan.html',Datos =session, data=data2, dataf=data3,clid=clid,deliveryday=deliveryday,OG=OG)
#         else:
#             link = connectBD()
#             db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#             cur= db_connection.cursor()
#             # Read a single record
#             sql = "SELECT * FROM orders WHERE Ean=%s AND  CLid=%s AND DeliveryDay=%s AND NOT Status=%s AND OperationGroup=%s AND Site=%s  limit 1"
#             cur.execute(sql, (ean,clid,deliveryday,status,OG,Site))
#             data = cur.fetchone()
#             cur.close
#             if data :
#               Packer=session['UserName']
#               OriginalQuantity=data[12]
#               CurrentQuantity	=data[16]+1
#               PendingQuantity=data[17]-1
#               if OriginalQuantity==CurrentQuantity:
#                 estatus= 'Finished'
#               elif CurrentQuantity>0 and PendingQuantity> 0:
#                 estatus= 'In Process'
#               else:
#                 estatus= 'Pendding'
#               ID_Order =data[0]
              
#               link = connectBD()
#               db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#               cur= db_connection.cursor()
#               # Create a new record
#               sql = "UPDATE orders SET Packer = %s, CurrentQuantity = %s,PendingQuantity = %s, Status = %s WHERE ID_Order  = %s"
#               cur.execute(sql,(Packer,CurrentQuantity,PendingQuantity,estatus,ID_Order,))
#               # connection is not autocommit by default. So you must commit to save
#               # your changes.
#               db_connection.commit()
#               cur.close()
              
#               link = connectBD()
#               db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#               cur= db_connection.cursor()
#               # Create a new record
#               sql = "INSERT INTO movements (RouteName,FuOrder,CLid,Ean,Description,Quantity,Process,Responsible,Site,DateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
#               cur.execute(sql,(data[1],data[6],clid,ean,data[9],1,'Packing',session['UserName'],session['SiteName'],datetime.now(timeZ)))
#               # connection is not autocommit by default. So you must commit to save
#               # your changes.
#               db_connection.commit()
#               cur.close()
              
#               link = connectBD()
#               db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#               cur= db_connection.cursor()
#               # Read a single record
#               sql = "SELECT RouteName, FuOrder, Ean, ProductName, OriginalQuantity, CurrentQuantity, Status FROM orders WHERE  CLid=%s AND DeliveryDay=%s AND NOT Status =%s AND OperationGroup=%s AND Site=%s  "
#               cur.execute(sql, (clid,deliveryday,status, OG, Site))
#               data2 = cur.fetchall()
#               cur.close()
              
#               link = connectBD()
#               db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#               cur= db_connection.cursor()
#               # Read a single record
#               sql = "SELECT RouteName, FuOrder, Ean, ProductName, OriginalQuantity, CurrentQuantity, Status FROM orders WHERE  CLid=%s AND DeliveryDay=%s AND Status =%s AND OperationGroup=%s AND Site=%s  "
#               cur.execute(sql, (clid,deliveryday,status, OG, Site))
#               data3 = cur.fetchall()
#               cur.close()
#               if data2:
#                 return render_template('actualizacion/Scan.html',Datos =session, data=data2, dataf=data3,clid=clid,deliveryday=deliveryday,OG=OG)
#               else:
#                 return render_template('actualizacion/Scan.html',Datos =session, dataf=data3,clid=clid,deliveryday=deliveryday,OG=OG)
#             else:
#               flash("Codigo Ean no Encontrado en esta Ruta")
              
#               link = connectBD()
#               db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#               cur= db_connection.cursor()
#               # Read a single record
#               sql = "SELECT RouteName, FuOrder, Ean, ProductName, OriginalQuantity, CurrentQuantity, Status FROM orders WHERE  CLid=%s AND DeliveryDay=%s AND NOT Status =%s AND OperationGroup=%s AND Site=%s "
#               cur.execute(sql, (clid,deliveryday,status, OG, Site))
#               data2 = cur.fetchall()
#               cur.close()
              
#               link = connectBD()
#               db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
#               cur= db_connection.cursor()
#               # Read a single record
#               sql = "SELECT RouteName, FuOrder, Ean, ProductName, OriginalQuantity, CurrentQuantity, Status FROM orders WHERE  CLid=%s AND DeliveryDay=%s AND Status =%s AND OperationGroup=%s AND Site=%s "
#               cur.execute(sql, (clid,deliveryday,status, OG, Site))
#               data3 = cur.fetchall()
#               cur.close()
#               return render_template('actualizacion/Scan.html',Datos =session, data=data2,dataf=data3,clid=clid,deliveryday=deliveryday,OG=OG)

#   except Exception as error:
#     flash(str(error))
#     return redirect('/Packing')

# receiving register 
@app.route('/RegistrarReceiving',methods=['POST','GET'])
def registrarReceiving():
  try:
      if request.method == 'POST':
        OrderNumber =  request.form['OrderNumber']
        ReceivingType="Recepción"
        return render_template('actualizacion/receivingscan.html',Datos =session, ReceivingType=ReceivingType,OrderNumber=OrderNumber)
  except Exception as error: 
    flash(str(error))
    return redirect('/Packing')

    
@app.route('/RegistrarReceivingP/<ReceivingType>',methods=['GET'])
def registrarReceivingp(ReceivingType):
  try:
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
        fc=data[4]
        cantidad2= int(cantidad)*int(fc)
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Create a new record
        sql = "INSERT INTO receiving (PurchaseOrder,Type,Ean,EanMuni,ConversionUnit	,Quantity,Description,Responsible,Status,Site,DateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(sql,(orderNumber,receivingType,ean,data[2],data[4],cantidad2,data[3],session['UserName'],'In Process',session['SiteName'],datetime.now(timeZ),))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        db_connection.commit()
        cur.close()
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")  
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM inventory WHERE CB_Captura =%s  limit 1  "
        cur.execute(sql, (ean))
        datainv = cur.fetchone()
        cur.close()
        if datainv:
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
        else:
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
        # Read a single record
        sql = "SELECT Cantidad FROM receivingtable WHERE Ean_Muni =%s AND PurchaseOrder =%s AND Type=%s  AND Site = %s AND Status =%s limit 1  "
        cur.execute(sql, (data[2],orderNumber,receivingType,session['SiteName'],'In Process'))
        Rdata = cur.fetchone()
        cur.close()
        if Rdata:
          cantidadr = int(Rdata[0])+int(cantidad2)
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
          cur.execute(sql,(orderNumber,receivingType,data[2],data[3],cantidad2,session['UserName'],session['SiteName'],'In Process',datetime.now(timeZ),))
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
        return render_template('actualizacion/receivingscan.html',Datos =session, data=data2,ReceivingType=receivingType,OrderNumber=orderNumber)
      else:
        return render_template('actualizacion/Searchproduct.html',Datos =session,ean=ean,cantidad=cantidad,ReceivingType=receivingType,OrderNumber=orderNumber)
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
    link = connectBD()
    db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
    cur= db_connection.cursor()
    # Create a new record
    sql = "UPDATE inventory SET 	Status=%s WHERE	Status=%s AND inventoryUser=%s AND Site=%s"
    cur.execute(sql,('finalized','In Process',session['UserName'], session['SiteName'],))
    # connection is not autocommit by default. So you must commit to save
    # your changes.
    db_connection.commit()
    cur.close()
    link = connectBD()
    db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")    
    cur= db_connection.cursor()
    # Create a new record
    sql = "UPDATE receivingtable SET Status = %s WHERE PurchaseOrder=%s AND Type=%s AND  Responsable =%s AND Status=%s AND Site =%s"
    cur.execute(sql,('received',orderNumber,receivingType,session['UserName'],'In Process',session['SiteName']))
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
            sql = "SELECT Type,Ean,EanMuni, Description, sum(Quantity) FROM receiving WHERE  PurchaseOrder=%s AND Type=%s AND  Responsible =%s AND Status=%s AND Site=%s GROUP BY PurchaseOrder,	Type,Ean, EanMuni, Description"
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
@app.route('/RegistrarProductorec/<ean>/<cantidad>/<ReceivingType>/<OrderNumber>',methods=['POST','GET'])
def registrarProductorec(ean,cantidad,ReceivingType,OrderNumber):
  try:
    if request.method == 'POST':
      EAN_MUNI =  request.form['EAN_MUNI']
      Producto =  request.form['Producto']
      if session['SiteName']=='CDMX01':
        timeZ = pytz.timezone('America/Mexico_City')
      elif session['SiteName']=='MEDELLIN01':
        timeZ = pytz.timezone('America/Bogota')
      Factor_de_Conversion =  request.form['Factor_de_Conversion']
      link = connectBD()
      db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
      cur= db_connection.cursor()
      # Create a new record
      sql = "INSERT INTO product (CB_Captura,EAN_MUNI,Producto,Factor_de_Conversion) VALUES (%s,%s,%s,%s)"
      cur.execute(sql,(ean,EAN_MUNI,Producto,Factor_de_Conversion,))
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
      if data:
        cantidad2= int(cantidad)*int(data[4])
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Create a new record
        sql = "INSERT INTO receiving (PurchaseOrder,Type,Ean,EanMuni,ConversionUnit	,Quantity,Description,Responsible,Status,Site,DateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        cur.execute(sql,(OrderNumber,ReceivingType,ean,data[2],data[4],cantidad2,data[3],session['UserName'],'In Process',session['SiteName'],datetime.now(timeZ),))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        db_connection.commit()
        cur.close()
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")  
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT * FROM inventory WHERE CB_Captura =%s  limit 1  "
        cur.execute(sql, (ean))
        datainv = cur.fetchone()
        cur.close()
        if datainv:
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
        else:
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
        # Read a single record
        sql = "SELECT Cantidad FROM receivingtable WHERE Ean_Muni =%s AND PurchaseOrder =%s AND Type=%s  AND Site = %s AND Status =%s limit 1  "
        cur.execute(sql, (data[2],OrderNumber,ReceivingType,session['SiteName'],'In Process'))
        Rdata = cur.fetchone()
        cur.close()
        if Rdata:
          cantidadr = int(Rdata[0])+int(cantidad2)
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Create a new record
          sql = "UPDATE receivingtable SET  Cantidad =%s, Fecha_de_Actualizacion=%s WHERE PurchaseOrder=%s AND Type=%s AND Ean_Muni=%s AND  Status=%s AND Site=%s "
          cur.execute(sql,(cantidadr,datetime.now(timeZ),OrderNumber,ReceivingType,data[2],'In Process',session['SiteName'],))
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
          cur.execute(sql,(OrderNumber,ReceivingType,data[2],data[3],cantidad2,session['UserName'],session['SiteName'],'In Process',datetime.now(timeZ),))
          # connection is not autocommit by default. So you must commit to save
          # your changes.
          db_connection.commit()
          cur.close()
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Read a single record
        sql = "SELECT PurchaseOrder,Type,Ean_Muni, Descripcion, Cantidad,Fecha_de_Actualizacion FROM receivingtable WHERE  PurchaseOrder=%s AND Type=%s AND  Responsable =%s AND Status=%s AND Site=%s ORDER BY Fecha_de_Actualizacion DESC"
        cur.execute(sql, (OrderNumber,ReceivingType,session['UserName'],'In Process',session['SiteName'],))
        data2 = cur.fetchall()
        cur.close()
        return render_template('actualizacion/receivingscan.html',Datos =session, data=data2,ReceivingType=ReceivingType,OrderNumber=OrderNumber) 
  except Exception as error:
    flash(str(error))
    return redirect('/Inventory')

# receiving mov register
@app.route('/RegistrarProductoselect/<ean>/<EAN_MUNI>/<Producto>/<Factor_de_Conversion>/<cantidad>/<ReceivingType>/<OrderNumber>',methods=['POST','GET'])
def registrarProductoSelect(ean,EAN_MUNI,Producto,Factor_de_Conversion,cantidad,ReceivingType,OrderNumber):
  try:
    if session['SiteName']=='CDMX01':
      timeZ = pytz.timezone('America/Mexico_City')
    elif session['SiteName']=='MEDELLIN01':
      timeZ = pytz.timezone('America/Bogota')
    link = connectBD()
    db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
    cur= db_connection.cursor()
    # Create a new record
    sql = "INSERT INTO product (CB_Captura,EAN_MUNI,Producto,Factor_de_Conversion) VALUES (%s,%s,%s,%s)"
    cur.execute(sql,(ean,EAN_MUNI,Producto,Factor_de_Conversion,))
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
    if data:
      cantidad2= int(cantidad)*int(data[4])
      link = connectBD()
      db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
      cur= db_connection.cursor()
      # Create a new record
      sql = "INSERT INTO receiving (PurchaseOrder,Type,Ean,EanMuni,ConversionUnit	,Quantity,Description,Responsible,Status,Site,DateTime) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      cur.execute(sql,(OrderNumber,ReceivingType,ean,data[2],data[4],cantidad2,data[3],session['UserName'],'In Process',session['SiteName'],datetime.now(timeZ),))
      # connection is not autocommit by default. So you must commit to save
      # your changes.
      db_connection.commit()
      cur.close()
      link = connectBD()
      db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")  
      cur= db_connection.cursor()
      # Read a single record
      sql = "SELECT * FROM inventory WHERE CB_Captura =%s  limit 1  "
      cur.execute(sql, (ean))
      datainv = cur.fetchone()
      cur.close()
      if datainv:
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
      else:
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
      # Read a single record
      sql = "SELECT Cantidad FROM receivingtable WHERE Ean_Muni =%s AND PurchaseOrder =%s AND Type=%s  AND Site = %s AND Status =%s limit 1  "
      cur.execute(sql, (data[2],OrderNumber,ReceivingType,session['SiteName'],'In Process'))
      Rdata = cur.fetchone()
      cur.close()
      if Rdata:
        cantidadr = int(Rdata[0])+int(cantidad2)
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        # Create a new record
        sql = "UPDATE receivingtable SET  Cantidad =%s, Fecha_de_Actualizacion=%s WHERE PurchaseOrder=%s AND Type=%s AND Ean_Muni=%s AND  Status=%s AND Site=%s "
        cur.execute(sql,(cantidadr,datetime.now(timeZ),OrderNumber,ReceivingType,data[2],'In Process',session['SiteName'],))
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
        cur.execute(sql,(OrderNumber,ReceivingType,data[2],data[3],cantidad2,session['UserName'],session['SiteName'],'In Process',datetime.now(timeZ),))
        # connection is not autocommit by default. So you must commit to save
        # your changes.
        db_connection.commit()
        cur.close()
      link = connectBD()
      db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
      cur= db_connection.cursor()
      # Read a single record
      sql = "SELECT PurchaseOrder,Type,Ean_Muni, Descripcion, Cantidad,Fecha_de_Actualizacion FROM receivingtable WHERE  PurchaseOrder=%s AND Type=%s AND  Responsable =%s AND Status=%s AND Site=%s ORDER BY Fecha_de_Actualizacion DESC"
      cur.execute(sql, (OrderNumber,ReceivingType,session['UserName'],'In Process',session['SiteName'],))
      data2 = cur.fetchall()
      cur.close()
      return render_template('actualizacion/receivingscan.html',Datos =session, data=data2,ReceivingType=ReceivingType,OrderNumber=OrderNumber) 
  except Exception as error:
    flash(str(error))
    return redirect('/Inventory')

# receiving mov register
@app.route('/RegistrarProductoinv/<ean>/<cantidad>',methods=['POST','GET'])
def registrarProductoInv(ean,cantidad):
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
      Factor_de_Conversion =  request.form['Factor_de_Conversion']
      link = connectBD()
      db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
      cur= db_connection.cursor()
      # Create a new record
      sql = "INSERT INTO product (CB_Captura,EAN_MUNI,Producto,Factor_de_Conversion) VALUES (%s,%s,%s,%s)"
      cur.execute(sql,(ean,EAN_MUNI,Producto,Factor_de_Conversion,))
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
@app.route('/RegistrarProductoselectinv/<ean>/<EAN_MUNI>/<Producto>/<Factor_de_Conversion>/<cantidad>',methods=['POST','GET'])
def registrarProductoSelectInv(ean,EAN_MUNI,Producto,Factor_de_Conversion,cantidad):
  try:
    receivingType="Inventory"
    orderNumber="No aplica"
    if session['SiteName']=='CDMX01':
      timeZ = pytz.timezone('America/Mexico_City')
    elif session['SiteName']=='MEDELLIN01':
      timeZ = pytz.timezone('America/Bogota')
    link = connectBD()
    db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
    cur= db_connection.cursor()
    # Create a new record
    sql = "INSERT INTO product (CB_Captura,EAN_MUNI,Producto,Factor_de_Conversion) VALUES (%s,%s,%s,%s)"
    cur.execute(sql,(ean,EAN_MUNI,Producto,Factor_de_Conversion,))
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
  try:
    if request.method == 'POST':
      EAN_MUNI =  request.form['EAN_MUNI'].strip()
      Producto =  request.form['Producto']
      Factor_de_Conversion =  request.form['Factor_de_Conversion']
      link = connectBD()
      db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
      cur= db_connection.cursor()
      # Create a new record
      sql = "INSERT INTO product (CB_Captura,EAN_MUNI,Producto,Factor_de_Conversion) VALUES (%s,%s,%s,%s)"
      cur.execute(sql,(ean,EAN_MUNI,Producto,Factor_de_Conversion,))
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
  except Exception as error:
    flash(str(error))
    return redirect('/Product')

# receiving mov register
@app.route('/RegistrarProductoselectproduct/<ean>/<EAN_MUNI>/<Producto>/<Factor_de_Conversion>',methods=['POST','GET'])
def registrarProductoSelectProduct(ean,EAN_MUNI,Producto,Factor_de_Conversion):
  try:
    link = connectBD()
    db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
    cur= db_connection.cursor()
    # Create a new record
    sql = "INSERT INTO product (CB_Captura,EAN_MUNI,Producto,Factor_de_Conversion) VALUES (%s,%s,%s,%s)"
    cur.execute(sql,(ean,EAN_MUNI,Producto,Factor_de_Conversion,))
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
  except Exception as error:
    flash(str(error))
    return redirect('/Product')

# Search Product
@app.route('/SearchProductrec/<ean>/<cantidad>/<ReceivingType>/<OrderNumber>',methods=['POST','GET'])
def searchProductrec(ean,cantidad,ReceivingType,OrderNumber):
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
        return render_template('actualizacion/product.html',Datos =session,data=data,ean=ean,cantidad=cantidad,ReceivingType=ReceivingType,OrderNumber=OrderNumber)
  except Exception as error:
    flash(str(error))
    return redirect('/Inventory')

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
@app.route('/RegistrarDamage/<type>/<um>',methods=['POST','GET'])
def registrarDamage(type,um):
  try:
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
          cur= db_connection.cursor()
          # Create a new record
          sql = "INSERT INTO mermas (type,	EAN_MUNI,Description,Quantity,Reason,Responsible,Status,Site,DateTime,unitOfMeasurement) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
          cur.execute(sql,(type,data[2],data[3],catidad2,Motivo,session['UserName'],'In Process',session['SiteName'],datetime.now(timeZ),um))
          # connection is not autocommit by default. So you must commit to save
          # your changes.
          db_connection.commit()
          cur.close()
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
          cur= db_connection.cursor()
          # Read a single record
          sql = "SELECT EAN_MUNI,	Description,Quantity, Reason FROM mermas WHERE  Responsible = %s And Status = %s AND Site = %s "
          cur.execute(sql, (session['UserName'],'In Process',session['SiteName'],))
          data2 = cur.fetchall()
          cur.close()
          return render_template('form/damage.html',Datos =session, data=data2)
        else:
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
            sql = "INSERT INTO mermas (type,	EAN_MUNI,Description,Quantity,Reason,Responsible,Status,Site,DateTime,unitOfMeasurement) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(type,Inv[1],Inv[2],cantidad,Motivo,session['UserName'],'In Process',session['SiteName'],datetime.now(timeZ),um))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Create a new record
            sql = "INSERT INTO mermas (type,	EAN_MUNI,Description,Quantity,Reason,Responsible,Status,Site,DateTime,unitOfMeasurement) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            cur.execute(sql,(type,ean,'No Registrado',cantidad,Motivo,session['UserName'],'In Process',session['SiteName'],datetime.now(timeZ),um))
            # connection is not autocommit by default. So you must commit to save
            # your changes.
            db_connection.commit()
            cur.close()
          cur= db_connection.cursor()
          # Read a single record
          sql = "SELECT EAN_MUNI,	Description,Quantity, Reason FROM mermas WHERE  Responsible = %s And Status = %s AND Site = %s"
          cur.execute(sql, (session['UserName'],'In Process',session['SiteName'],))
          data2 = cur.fetchall()
          cur.close()
          return render_template('form/damage.html',Datos =session, data=data2)
  except Exception as error: 
    flash(str(error))
    return redirect('/Damage')

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

# # cam scan 
# @app.route('/Scan',methods=['POST'])
# def registro_s_s():
#   try:
#       if request.method == 'POST':
#         DeliveryDate = request.form['DeliveryDate']
#         Route = request.form['Route']
#         return render_template('form/scan.html')
#   except Exception as error: 
#     flash(str(error))
#     return render_template('form/receiving.html',Datos = session)

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
@app.route('/ReporteProducts/<rowi>',methods=['POST','GET'])
def reporte_product(rowi):
  try:
      if request.method == 'POST':
        if request.method == 'GET':
          session['rowi_product']=rowi
          row1 = int(session['rowi_product'])
          row2 = 50
        else:
            row1 = int(session['rowi_product'])
            row2 =50
        if 'valor' in request.form:
          if len(request.form['valor'])>0:
            session['filtro_product']=request.form['filtro']
            session['valor_product']=request.form['valor']
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT * FROM product WHERE {} LIKE \'%{}%\'  ORDER BY ID_Product DESC  LIMIT {}, {}".format(session['filtro_product'],session['valor_product'],row1,row2)
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            return render_template('reportes/t_product.html',Datos = session,Infos =data)
          else:
            if 'valor_product' in session:
              session.pop('filtro_product')
              session.pop('valor_product')
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT * FROM product  ORDER BY ID_Product DESC  LIMIT {}, {}".format(row1,row2)
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            return render_template('reportes/t_product.html',Datos = session,Infos =data)
        else:
          if 'valor_product' in session:
            if len(session['valor_product'])>0:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM product WHERE {} LIKE \'%{}%\'  ORDER BY ID_Product DESC  LIMIT {}, {}".format(session['filtro_product'],session['valor_product'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_product.html',Datos = session,Infos =data) 
            else:
              session.pop('filtro_product')
              session.pop('valor_product')
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM product ORDER BY ID_Product DESC  LIMIT {}, {}".format(row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_product.html',Datos = session,Infos =data)
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT * FROM product  ORDER BY ID_Product DESC  LIMIT {}, {}".format(row1,row2)
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            return render_template('reportes/t_product.html',Datos = session,Infos =data) 
      else: 
        if request.method == 'GET':
          session['rowi_product']=rowi
          row1 = int(session['rowi_product'])
          row2 = 50
        else:
          row1 = int(session['rowi_product'])
          row2 =50
        if 'valor_product' in session:
          if len(session['valor_product'])>0:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT * FROM product WHERE {} LIKE \'%{}%\'  ORDER BY ID_Product DESC  LIMIT {}, {}".format(session['filtro_product'],session['valor_product'],row1,row2)
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            return render_template('reportes/t_product.html',Datos = session,Infos =data) 
          else:
            session.pop('filtro_product')
            session.pop('valor_product')
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT * FROM product  ORDER BY ID_Product DESC  LIMIT {}, {}".format(row1,row2)
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            return render_template('reportes/t_product.html',Datos = session,Infos =data)
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          # Read a single record
          sql = "SELECT * FROM product ORDER BY ID_Product DESC  LIMIT {}, {}".format(row1,row2)
          cur.execute(sql)
          data = cur.fetchall()
          cur.close()
          return render_template('reportes/t_product.html',Datos = session,Infos =data)         
  except Exception as error: 
    flash(str(error))
    return render_template('index.html')#

# movements report 
@app.route('/ReporteInventori/<rowi>',methods=['POST','GET'])
def reporte_inventori(rowi):
  try:
      if request.method == 'POST':
        if request.method == 'GET':
          session['rowi_inventori']=rowi
          row1 = int(session['rowi_inventori'])
          row2 = 50
        else:
            row1 = int(session['rowi_inventori'])
            row2 =50
        if 'valor' in request.form:
          if len(request.form['valor'])>0:
            session['filtro_inventori']=request.form['filtro']
            session['valor_inventori']=request.form['valor']
            if 'datefilter' in request.form:
              if len(request.form['datefilter'])>0:
                daterangef=request.form['datefilter']
                daterange=daterangef.replace("-", "' AND '")
                session['datefilter_inventori']=daterange
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM inventory WHERE {} LIKE \'%{}%\' AND DATE(Fecha_de_Actualizacion) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['filtro_inventori'],session['valor_inventori'],session['datefilter_inventori'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM inventory WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['filtro_inventori'],session['valor_inventori'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
            else:
              session.pop('datefilter')
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM inventory WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['filtro_inventori'],session['valor_inventori'],session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
          else:
            if 'datefilter' in request.form:
              if len(request.form['datefilter'])>0:
                if 'valor_inventori' in session:
                  if len(session['valor_inventori'])>0:
                    daterangef=request.form['datefilter']
                    daterange=daterangef.replace("-", "' AND '")
                    session['datefilter_inventori']=daterange
                    link = connectBD()
                    db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                    cur= db_connection.cursor()
                    # Read a single record
                    sql = "SELECT * FROM inventory WHERE {} LIKE \'%{}%\' AND  DATE(Fecha_de_Actualizacion) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['filtro_inventori'],session['valor_inventori'],session['datefilter_inventori'],session['SiteName'],row1,row2)
                    cur.execute(sql)
                    data = cur.fetchall()
                    cur.close()
                    return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
                  else:
                    session.pop('filtro_inventori')
                    session.pop('valor_inventori')
                    link = connectBD()
                    db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                    cur= db_connection.cursor()
                    # Read a single record
                    sql = "SELECT * FROM inventory WHERE  DATE(Fecha_de_Actualizacion) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['datefilter_inventori'],session['SiteName'],row1,row2)
                    cur.execute(sql)
                    data = cur.fetchall()
                    cur.close()
                    return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
                else:
                  daterangef=request.form['datefilter']
                  daterange=daterangef.replace("-", "' AND '")
                  session['datefilter_inventori']=daterange
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM inventory WHERE  DATE(Fecha_de_Actualizacion) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['datefilter_inventori'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
              else:
                if 'valor_inventori' in session:
                  session.pop('filtro_inventori')
                  session.pop('valor_inventori')
                if 'datefilter_inventori' in session:
                  session.pop('datefilter_inventori')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM inventory WHERE Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
            else:
              if 'valor_inventori' in session:
                session.pop('filtro_inventori')
                session.pop('valor_inventori')
              if 'datefilter_inventori' in session:
                  session.pop('datefilter_inventori')
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM inventory WHERE Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_inventori.html',Datos = session,Infos =data)

        else:
          if 'valor_inventori' in session:
            if len(session['valor_inventori'])>0:
              if 'datefilter_inventori' in session:
                if len(session['datefilter_inventori'])>0:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM inventory WHERE {} LIKE \'%{}%\' AND  DATE(Fecha_de_Actualizacion) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['filtro_inventori'],session['valor_inventori'],session['datefilter_inventori'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
                else:
                  session.pop('datefilter_inventori')
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM inventory WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['filtro_inventori'],session['valor_inventori'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM inventory WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['filtro_inventori'],session['valor_inventori'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_inventori.html',Datos = session,Infos =data) 
            else:
              session.pop('filtro_inventori')
              session.pop('valor_inventori')
              if 'datefilter_inventori' in session:
                if len(session['datefilter_inventori'])>0:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM inventory WHERE  DATE(Fecha_de_Actualizacion) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['datefilter_inventori'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
                else:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM inventory WHERE Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM inventory WHERE Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
          else:
            if 'datefilter_inventori' in session:
              if len(session['datefilter_inventori'])>0:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM inventory WHERE  DATE(Fecha_de_Actualizacion) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['datefilter_inventori'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter_inventori')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                cur.execute('SELECT * FROM inventory WHERE Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
            else:
              if 'datefilter' in request.form:
                if len(request.form['datefilter'])>0:
                  daterangef=request.form['datefilter']
                  daterange=daterangef.replace("-", "' AND '")
                  session['datefilter_inventori']=daterange
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM inventory WHERE   DATE(Fecha_de_Actualizacion) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['datefilter_inventori'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
                else:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM inventory WHERE Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_inventori.html',Datos = session,Infos =data) 
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM inventory WHERE Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_inventori.html',Datos = session,Infos =data) 
      else: 
        if request.method == 'GET':
          session['rowi_inventori']=rowi
          row1 = int(session['rowi_inventori'])
          row2 = 50
        else:
          row1 = int(session['rowi_inventori'])
          row2 =50
        if 'valor_inventori' in session:
          if len(session['valor_inventori'])>0:
            if 'datefilter_inventori' in session:
              if len(session['datefilter_inventori'])>0:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM inventory WHERE {} LIKE \'%{}%\' AND  DATE(Fecha_de_Actualizacion) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['filtro_inventori'],session['valor_inventori'],session['datefilter_inventori'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter_inventori')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM inventory WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['filtro_inventori'],session['valor_inventori'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
            else:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM inventory WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['filtro_inventori'],session['valor_inventori'],session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_inventori.html',Datos = session,Infos =data) 
          else:
            session.pop('filtro_inventori')
            session.pop('valor_inventori')
            if 'datefilter_inventori' in session:
              if len(session['datefilter_inventori'])>0:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM inventory WHERE  DATE(Fecha_de_Actualizacion) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['datefilter_inventori'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter_inventori')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM inventory WHERE Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
            else:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM inventory WHERE Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
        else:
          if 'datefilter_inventori' in session:
            if len(session['datefilter_inventori'])>0:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM inventory WHERE  DATE(Fecha_de_Actualizacion) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['datefilter_inventori'],session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
            else:
              session.pop('datefilter_inventori')
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM inventory WHERE Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_inventori.html',Datos = session,Infos =data)
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT * FROM inventory WHERE Site =\'{}\' ORDER BY Id_Inventori DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            return render_template('reportes/t_inventori.html',Datos = session,Infos =data)         
  except Exception as error: 
    flash(str(error))
    return render_template('index.html')

# movements report 
@app.route('/ReporteMermas/<rowi>',methods=['POST','GET'])
def reporte_mermas(rowi):
  try:
      if request.method == 'POST':
        if request.method == 'GET':
          session['rowi_mermas']=rowi
          row1 = int(session['rowi_mermas'])
          row2 = 50
        else:
            row1 = int(session['rowi_mermas'])
            row2 =50
        if 'valor' in request.form:
          if len(request.form['valor'])>0:
            session['filtro_mermas']=request.form['filtro']
            session['valor_mermas']=request.form['valor']
            if 'datefilter' in request.form:
              if len(request.form['datefilter'])>0:
                daterangef=request.form['datefilter']
                daterange=daterangef.replace("-", "' AND '")
                session['datefilter_mermas']=daterange
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM mermas WHERE {} LIKE \'%{}%\' AND DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['filtro_mermas'],session['valor_mermas'],session['datefilter_mermas'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM mermas WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['filtro_mermas'],session['valor_mermas'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
            else:
              session.pop('datefilter')
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM mermas WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['filtro_mermas'],session['valor_mermas'],session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
          else:
            if 'datefilter' in request.form:
              if len(request.form['datefilter'])>0:
                if 'valor_mermas' in session:
                  if len(session['valor_mermas'])>0:
                    daterangef=request.form['datefilter']
                    daterange=daterangef.replace("-", "' AND '")
                    session['datefilter_mermas']=daterange
                    link = connectBD()
                    db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                    cur= db_connection.cursor()
                    # Read a single record
                    sql = "SELECT * FROM mermas WHERE {} LIKE \'%{}%\' AND  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['filtro_mermas'],session['valor_mermas'],session['datefilter_mermas'],session['SiteName'],row1,row2)
                    cur.execute(sql)
                    data = cur.fetchall()
                    cur.close()
                    return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
                  else:
                    session.pop('filtro_mermas')
                    session.pop('valor_mermas')
                    link = connectBD()
                    db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                    cur= db_connection.cursor()
                    # Read a single record
                    sql = "SELECT * FROM mermas WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['datefilter_mermas'],session['SiteName'],row1,row2)
                    cur.execute(sql)
                    data = cur.fetchall()
                    cur.close()
                    return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
                else:
                  daterangef=request.form['datefilter']
                  daterange=daterangef.replace("-", "' AND '")
                  session['datefilter_mermas']=daterange
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM mermas WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['datefilter_mermas'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
              else:
                if 'valor_mermas' in session:
                  session.pop('filtro_mermas')
                  session.pop('valor_mermas')
                if 'datefilter_mermas' in session:
                  session.pop('datefilter_mermas')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM mermas WHERE Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
            else:
              if 'valor_mermas' in session:
                session.pop('filtro_mermas')
                session.pop('valor_mermas')
              if 'datefilter_mermas' in session:
                  session.pop('datefilter_mermas')
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM mermas WHERE Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_mermas.html',Datos = session,Infos =data)

        else:
          if 'valor_mermas' in session:
            if len(session['valor_mermas'])>0:
              if 'datefilter_mermas' in session:
                if len(session['datefilter_mermas'])>0:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM mermas WHERE {} LIKE \'%{}%\' AND  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['filtro_mermas'],session['valor_mermas'],session['datefilter_mermas'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
                else:
                  session.pop('datefilter_mermas')
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM mermas WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['filtro_mermas'],session['valor_mermas'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM mermas WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['filtro_mermas'],session['valor_mermas'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_mermas.html',Datos = session,Infos =data) 
            else:
              session.pop('filtro_mermas')
              session.pop('valor_mermas')
              if 'datefilter_mermas' in session:
                if len(session['datefilter_mermas'])>0:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM mermas WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['datefilter_mermas'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
                else:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM mermas WHERE Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM mermas WHERE Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
          else:
            if 'datefilter_mermas' in session:
              if len(session['datefilter_mermas'])>0:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM mermas WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['datefilter_mermas'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter_mermas')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                cur.execute('SELECT * FROM mermas WHERE Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
            else:
              if 'datefilter' in request.form:
                if len(request.form['datefilter'])>0:
                  daterangef=request.form['datefilter']
                  daterange=daterangef.replace("-", "' AND '")
                  session['datefilter_mermas']=daterange
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM mermas WHERE   DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['datefilter_mermas'],session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
                else:
                  link = connectBD()
                  db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                  cur= db_connection.cursor()
                  # Read a single record
                  sql = "SELECT * FROM mermas WHERE Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                  cur.execute(sql)
                  data = cur.fetchall()
                  cur.close()
                  return render_template('reportes/t_mermas.html',Datos = session,Infos =data) 
              else:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM mermas WHERE Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_mermas.html',Datos = session,Infos =data) 
      else: 
        if request.method == 'GET':
          session['rowi_mermas']=rowi
          row1 = int(session['rowi_mermas'])
          row2 = 50
        else:
          row1 = int(session['rowi_mermas'])
          row2 =50
        if 'valor_mermas' in session:
          if len(session['valor_mermas'])>0:
            if 'datefilter_mermas' in session:
              if len(session['datefilter_mermas'])>0:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM mermas WHERE {} LIKE \'%{}%\' AND  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['filtro_mermas'],session['valor_mermas'],session['datefilter_mermas'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter_mermas')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM mermas WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['filtro_mermas'],session['valor_mermas'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
            else:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM mermas WHERE {} LIKE \'%{}%\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['filtro_mermas'],session['valor_mermas'],session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_mermas.html',Datos = session,Infos =data) 
          else:
            session.pop('filtro_mermas')
            session.pop('valor_mermas')
            if 'datefilter_mermas' in session:
              if len(session['datefilter_mermas'])>0:
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM mermas WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['datefilter_mermas'],session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
              else:
                session.pop('datefilter_mermas')
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Read a single record
                sql = "SELECT * FROM mermas WHERE Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
                cur.execute(sql)
                data = cur.fetchall()
                cur.close()
                return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
            else:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM mermas WHERE Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
        else:
          if 'datefilter_mermas' in session:
            if len(session['datefilter_mermas'])>0:
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM mermas WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['datefilter_mermas'],session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
            else:
              session.pop('datefilter_mermas')
              link = connectBD()
              db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
              cur= db_connection.cursor()
              # Read a single record
              sql = "SELECT * FROM mermas WHERE Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
              cur.execute(sql)
              data = cur.fetchall()
              cur.close()
              return render_template('reportes/t_mermas.html',Datos = session,Infos =data)
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            # Read a single record
            sql = "SELECT * FROM mermas WHERE Site =\'{}\' ORDER BY ID_Merma DESC  LIMIT {}, {}".format(session['SiteName'],row1,row2)
            cur.execute(sql)
            data = cur.fetchall()
            cur.close()
            return render_template('reportes/t_mermas.html',Datos = session,Infos =data)         
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
    datos="ID Receiving"+","+"Orden de Compra"+","+"Tipo"+","+"Ean"+","+"Ean Muni"+","+"Unidad de Converción"+","+"Cantidad"+","+"Descripción"+","+"Responsable"+","+"Status"+","+"	Site"+","+"Fecha y Hora"+"\n"
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
    response = make_response(datos.encode('latin-1'))
    response.headers["Content-Disposition"] = "attachment; encoding=latin-1; filename="+"Movimientos-"+str(datetime.today())+".csv"; 
    return response
  except Exception as error: 
    flash(str(error))

# orders  dowload report
@app.route('/csvproduct',methods=['POST','GET'])
def crear_csvproduct():
  try:
    row1 = 0
    row2 =50000
    if 'valor_product' in session:
      if len(session['valor_product'])>0:
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        cur.execute('SELECT * FROM product WHERE {} LIKE \'%{}%\'  ORDER BY ID_Product DESC  LIMIT {}, {}'.format(session['filtro_product'],session['valor_product'],row1,row2))
        data = cur.fetchall()
        cur.close()
      else:
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        cur.execute('SELECT * FROM product ORDER BY ID_Product DESC  LIMIT {}, {}'.format(row1,row2))
        data = cur.fetchall()
        cur.close()
    else:
      link = connectBD()
      db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
      cur= db_connection.cursor()
      cur.execute('SELECT * FROM product  ORDER BY ID_Product DESC  LIMIT {}, {}'.format(row1,row2))
      data = cur.fetchall()
      cur.close()
    datos="ID Product"+","+"CB Captura"+","+"EAN MUNI"+","+"Producto"+","+"Factor de Conversion"+"\n"
    for res in data:
      datos+=str(res[0]).replace(","," ")
      datos+=","+str(res[1]).replace(","," ")
      datos+=","+str(res[2]).replace(","," ")
      datos+=","+str(res[3]).replace(","," ")
      datos+=","+str(res[4]).replace(","," ")
      datos+="\n"
    response = make_response(datos.encode('latin-1'))
    response.headers["Content-Disposition"] = "attachment; encoding=latin-1; filename="+"Productos-"+str(datetime.today())+".csv"; 
    return response
  except Exception as error: 
    flash(str(error))

# movements  dowload report
@app.route('/csvinventory',methods=['POST','GET'])
def crear_csvinventory():
  try:
    site=session['SiteName']
    row1 = 0
    row2 =5000
    if 'valor_inventori' in session:
      if len(session['valor_inventori'])>0:
        if 'datefilter_inventori' in session:
          if len(session['datefilter'])>0:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM inventory WHERE {} LIKE \'%{}%\' AND  DATE(Fecha_de_Actualizacion) BETWEEN \'{}\' AND Site =\'{}\'  ORDER BY Id_Inventori DESC  LIMIT {}, {}'.format(session['filtro_inventori'],session['valor_inventori'],session['datefilter_inventori'],session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM inventory WHERE {} LIKE \'%{}%\' AND Site =\'{}\'  ORDER BY Id_Inventori DESC  LIMIT {}, {}'.format(session['filtro_inventori'],session['valor_inventori'],session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM inventory WHERE {} LIKE \'%{}%\' AND Site =\'{}\'  ORDER BY Id_Inventori DESC  LIMIT {}, {}'.format(session['filtro_inventori'],session['valor_inventori'],session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
      else:
        if 'datefilter_inventori' in session:
          if len(session['datefilter_inventori'])>0:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM inventory WHERE  DATE(Fecha_de_Actualizacion) BETWEEN \'{}\' AND Site =\'{}\'  ORDER BY Id_Inventori DESC  LIMIT {}, {}'.format(session['datefilter_inventori'],session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM inventory WHERE Site =\'{}\'  ORDER BY Id_Inventori DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM inventory WHERE Site =\'{}\'  ORDER BY Id_Inventori DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
    else:
      if 'datefilter_inventori' in session:
        if len(session['datefilter_inventori'])>0:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM inventory WHERE  DATE(Fecha_de_Actualizacion) BETWEEN \'{}\' AND Site =\'{}\'  ORDER BY Id_Inventori DESC  LIMIT {}, {}'.format(session['datefilter_inventori'],session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM inventory WHERE Site =\'{}\'  ORDER BY Id_Inventori DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
      else:
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        cur.execute('SELECT * FROM inventory WHERE Site =\'{}\'  ORDER BY Id_Inventori DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
        data = cur.fetchall()
        cur.close()
    datos="Id Inventori"+","+"CB Captura"+","+"EAN MUNI"+","+"Producto"+","+"Cantidad Anterior"+","+"Cantidad Actual"+","+"Unidad de Medida"+","+"EStatus"+","+"inventory User"+","+"Fecha de Actualizacion"+","+"Site"+","+"\n"
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
    response = make_response(datos.encode('latin-1'))
    response.headers["Content-Disposition"] = "attachment; encoding=latin-1; filename="+"Inventario-"+str(datetime.today())+".csv"; 
    return response
  except Exception as error: 
    flash(str(error))

# movements  dowload report
@app.route('/csvmerma',methods=['POST','GET'])
def crear_csviMerma():
  try:
    site=session['SiteName']
    row1 = 0
    row2 =5000
    if 'valor_mermas' in session:
      if len(session['valor_mermas'])>0:
        if 'datefilter_mermas' in session:
          if len(session['datefilter'])>0:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM mermas WHERE {} LIKE \'%{}%\' AND  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\'  ORDER BY ID_Merma DESC  LIMIT {}, {}'.format(session['filtro_mermas'],session['valor_mermas'],session['datefilter_mermas'],session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM mermas WHERE {} LIKE \'%{}%\' AND Site =\'{}\'  ORDER BY ID_Merma DESC  LIMIT {}, {}'.format(session['filtro_mermas'],session['valor_mermas'],session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM mermas WHERE {} LIKE \'%{}%\' AND Site =\'{}\'  ORDER BY ID_Merma DESC  LIMIT {}, {}'.format(session['filtro_mermas'],session['valor_mermas'],session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
      else:
        if 'datefilter_mermas' in session:
          if len(session['datefilter_mermas'])>0:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM mermas WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\'  ORDER BY ID_Merma DESC  LIMIT {}, {}'.format(session['datefilter_mermas'],session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
          else:
            link = connectBD()
            db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
            cur= db_connection.cursor()
            cur.execute('SELECT * FROM mermas WHERE Site =\'{}\'  ORDER BY ID_Merma DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
            data = cur.fetchall()
            cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM mermas WHERE Site =\'{}\'  ORDER BY ID_Merma DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
    else:
      if 'datefilter_mermas' in session:
        if len(session['datefilter_mermas'])>0:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM mermas WHERE  DATE(DateTime) BETWEEN \'{}\' AND Site =\'{}\'  ORDER BY ID_Merma DESC  LIMIT {}, {}'.format(session['datefilter_mermas'],session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
        else:
          link = connectBD()
          db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
          cur= db_connection.cursor()
          cur.execute('SELECT * FROM mermas WHERE Site =\'{}\'  ORDER BY ID_Merma DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
          data = cur.fetchall()
          cur.close()
      else:
        link = connectBD()
        db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
        cur= db_connection.cursor()
        cur.execute('SELECT * FROM mermas WHERE Site =\'{}\'  ORDER BY ID_Merma DESC  LIMIT {}, {}'.format(session['SiteName'],row1,row2))
        data = cur.fetchall()
        cur.close()
    datos="ID Merma"+","+"Tipo"+","+"EAN MUNI"+","+"Descripción"+","+"Cantidad"+","+"Unidad de Medidia"+","+"Razón"+","+"Responsabilidad"+","+"Estatus"+","+"Site"+","+"Fecha y Hora"+","+"\n"
    for res in data:
      datos+=str(res[0]).replace(","," ")
      datos+=","+str(res[1]).replace(","," ")
      datos+=","+str(res[2]).replace(","," ")
      datos+=","+str(res[3]).replace(","," ")
      datos+=","+str(res[4]).replace(","," ")
      datos+=","+str(res[10]).replace(","," ")
      datos+=","+str(res[5]).replace(","," ")
      datos+=","+str(res[6]).replace(","," ")
      datos+=","+str(res[7]).replace(","," ")
      datos+=","+str(res[8]).replace(","," ")
      datos+=","+str(res[9]).replace(","," ")
      datos+="\n"
    response = make_response(datos.encode('latin-1'))
    response.headers["Content-Disposition"] = "attachment; encoding=latin-1; filename="+"Mermas-"+str(datetime.today())+".csv"; 
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
        with open(UPLOAD_FOLDER+'datos.csv',"r", encoding="latin-1", errors='ignore') as csv_file:
          data=csv.reader(csv_file, delimiter=',')
          i=0
          for row in data:
            if i >0:
              if row[2] != '#N/A':
                link = connectBD()
                db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
                cur= db_connection.cursor()
                # Create a new record
                sql = "INSERT INTO product (CB_Captura,  EAN_MUNI, Producto, Factor_de_Conversion) VALUES (%s,%s,%s,%s)"
                cur.execute(sql,(row[0], row[1], row[2], row[3],))
                # connection is not autocommit by default. So you must commit to save
                # your changes.
                db_connection.commit()
                cur.close()
            i+=1 
        flash(str(i)+' Registros Exitoso')
        return redirect('/files')
      # elif Base=='P&P':
      #   file.save(os.path.join(UPLOAD_FOLDER, "datos.csv"))
      #   with open(UPLOAD_FOLDER+'datos.csv',"r", encoding="utf8", errors='ignore') as csv_file:
      #     data=csv.reader(csv_file, delimiter=',')
      #     i=0
      #     for row in data:
      #       if i >0:
      #         routeName= row[1]
      #         FUName=row[4]
      #         Service_Zone=row[13]
      #         fk_order= row[15]
      #         packer=row[5]
      #         FuOrder=row[14]
      #         ean=row[7]
      #         operationGroup=row[12]
      #         productName=row[8]
      #         type=row[5]
      #         deliveryDate=row[0]
      #         originalQuantity=int(row[11])
      #         Vendor=row[9]
      #         CLid=row[3]
      #         Stop=row[2]
      #         currentQuantity=int(row[10])
      #         pendingQuantity=int(originalQuantity)-int(currentQuantity)
      #         if originalQuantity==currentQuantity:
      #           status= 'Finished'
      #         elif currentQuantity>0 and pendingQuantity> 0:
      #           status= 'In Process'
      #         else:
      #           status= 'Pendding'
      #         link = connectBD()
      #         db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
      #         cur= db_connection.cursor()
      #         # Read a single record
      #         sql = "SELECT * FROM orders WHERE RouteName=%s AND  Fk_order=%s AND FuOrder=%s AND Ean=%s  Limit 1 "
      #         cur.execute(sql, (routeName,fk_order,FuOrder,ean))
      #         data = cur.fetchone()
      #         cur.close()
      #         if data is None:
      #           link = connectBD()
      #           db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
      #           cur= db_connection.cursor()
      #           # Create a new record
      #           sql = "INSERT INTO orders (RouteName,FUName,Service_Zone,Fk_order,Packer,FuOrder,Ean,OperationGroup,ProductName,Type,DeliveryDay,OriginalQuantity,Vendedor,CLid,Stop,CurrentQuantity,PendingQuantity,Status,Site) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
      #           cur.execute(sql,(routeName,FUName,Service_Zone,fk_order,packer,FuOrder,ean,operationGroup,productName,type,deliveryDate,originalQuantity,Vendor,CLid,Stop,currentQuantity,pendingQuantity,status,session['SiteName'],))
      #           # connection is not autocommit by default. So you must commit to save
      #           # your changes.
      #           db_connection.commit()
      #           cur.close()
      #         else:
      #           link = connectBD()
      #           db_connection = pymysql.connect(host=link[0], user=link[1], passwd=link[2], db=link[3], charset="utf8", init_command="set names utf8")
      #           cur= db_connection.cursor()
      #           # Create a new record
      #           sql = "UPDATE orders SET CurrentQuantity = %s, PendingQuantity = %s, Status = %s, Packer = %s WHERE RouteName=%s AND  Fk_order=%s AND FuOrder=%s AND Ean=%s"
      #           cur.execute(sql,(currentQuantity,pendingQuantity,status,packer,routeName,fk_order,FuOrder,ean,))
      #           # connection is not autocommit by default. So you must commit to save
      #           # your changes.
      #           db_connection.commit()
      #           cur.close()
      #       i+=1 
      #   flash(str(i)+' Registros Exitoso')
      #   return redirect('/files')
  # except Exception as error:
 
  #   flash(str(error))
  #   return redirect('/files')


# if __name__=='__main__':
#     app.run(port = 3000, debug =True)