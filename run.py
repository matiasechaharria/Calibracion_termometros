import datetime
import os
import socket
from flask import Flask, request, flash, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from models import Equipo, Persona, Sonda, Medicion, Certificado,Certificado_INTI
from  app_things import app, db
from flask_wtf import  FlaskForm
from wtforms import SelectField
from calculos import error_tipico, interpolacion_patron, interpolacion_patron, temp_calibracion, cifra_correccion, incertidumbre, valores_para_certificado
import crear_pdf.crear_pdf as PDF
import numpy  as np


@app.route('/')
def Indice():
    return render_template('Indice.html')

@app.route('/Cartificado_pdf')
def Certificado_pdf(patron,ebp,medicion):

    obj = Certificado_INTI.query.order_by(Certificado_INTI.id.desc()).first()
    # print("obj")
    # print(obj.temp_0)
    certif_INTI=[[  obj.temp_n30,obj.correcion_n30,obj.incert_n30,	2],
                         [obj.temp_0,obj.correcion_0,obj.incert_0,	2],
                         [obj.temp_37,obj.correcion_37,obj.incert_37,	2],
                         [obj.temp_100,obj.correcion_100,obj.incert_100,	2],
                         [obj.temp_200,obj.correcion_200,obj.incert_200,	2]]



    print("average ebp =",np.average(ebp))
    print("average patron =",np.average(patron))
    temp,correccion,incert= valores_para_certificado(certif_INTI,patron,ebp)
    print("Temperatura = "+str(temp) +" Correccion = " +str(correccion) +" Incertidumbre = "+ str( incert))
    PDF.export_certificado(temp,correccion,incert)
    #PDF.export_certificado(equipos = Equipo.query.all())
    try:
        certificado=Certificado(medicion,temp,correccion,incert)
        db.session.add(certificado)
    except Exception as error:
        print("error al poner el certificado en la base")
        print(str(error))
        db.session.rollback()
        flash('error al poner el certificado en la base', 'error')
    else:
        db.session.commit()
        flash('El certificado fue cargado correctamente')
    #     return redirect(url_for('Listar_todos_los_certificados'))
    #
    # return render_template('Indice.html')

@app.route('/Listar_todos_los_certificados')
def Listar_todos_los_certificados():
    result = db.engine.execute("SELECT Certificado.id as certificado_id, \
        Equipo.nombre as nombre_equipo,\
        Sonda.nombre as Sonda_nombre, \
        Certificado.temp as certificado_temp, \
        Certificado.correcion as certificado_correcion, \
        Certificado.incert as certificado_incert \
        FROM Equipo \
        join Medicion on (Medicion.equipo_id = Equipo.id )\
        join Sonda on (Sonda.id = Medicion.sonda_id )\
        join Certificado on (Certificado.id = Medicion.id )\
        ORDER BY Equipo.id;")

    print("imprimo lo que sale de la mega consulta")
    certificados = []
    for lista in result:
        certificados.append(lista[:])
    print(certificados)


    return render_template('Listar_todos_los_certificados2.html', certificados=certificados  )
   #return render_template('Listar_todos_los_certificados.html', certificados = Certificado.query.all() )

@app.route('/Alta_certificado', methods = ['GET', 'POST'])
def Alta_certificado():
    """Carga los certificados del INTI en la base de datos"""
    if request.method == 'POST':
        if( not request.form['temp_n30'] \
            or not request.form['correcion_n30']\
            or not request.form['incert_n30']\
            or not request.form['temp_0']\
            or not request.form['correcion_0']\
            or not request.form['incert_0']\
            or not request.form['temp_37']\
            or not request.form['correcion_37']\
            or not request.form['incert_37']\
            or not request.form['temp_100']\
            or not request.form['correcion_100']\
            or not request.form['incert_100']\
            or not request.form['temp_200']\
            or not request.form['correcion_200']\
            or not request.form['incert_200']\
            or not request.form['fecha']):
            flash('Ingrese todos los campos', 'error')
        else:
            try:
                certificado_INTI = Certificado_INTI(float(request.form['temp_n30']), \
                 float(request.form['correcion_n30']),\
                 float(request.form['incert_n30']),\
                 float(request.form['temp_0']),\
                 float(request.form['correcion_0']),\
                 float(request.form['incert_0']),\
                 float(request.form['temp_37']),\
                 float(request.form['correcion_37']),\
                 float(request.form['incert_37']),\
                 float(request.form['temp_100']),\
                 float(request.form['correcion_100']),\
                 float(request.form['incert_100']),\
                 float(request.form['temp_200']),\
                 float(request.form['correcion_200']),\
                 float(request.form['incert_200']),\
                 request.form['fecha'])
                db.session.add(certificado_INTI)
            except Exception as error:
                print("error al poner el certificado del INTI en la base")
                print(str(error))
                db.session.rollback()
                flash('error al poner el certificado del INTI en la base', 'error')
            else:
                db.session.commit()
                flash('El certificado fue cargado correctamente')
                return redirect(url_for('Listar_todos_los_certificados'))
    return render_template('Alta_certificado.html')



@app.route('/Listar_todas_las_mediciones')
def Listar_todas_las_mediciones():
   return render_template('Listar_todas_las_mediciones.html', mediciones = Medicion.query.all() )

@app.route('/Alta_medicion', methods = ['GET', 'POST'])
def Alta_medicion():

   if request.method == 'POST':
      if( not request.form['temp_ambiente'] \
or not request.form['humedad'] \
or not request.form['persona_id'] \
or not request.form['ebp'] \
or not request.form['sonda'] \
or not request.form['temp_pat0']\
or not request.form['temp_pat1']\
or not request.form['temp_pat2']\
or not request.form['temp_pat3']\
or not request.form['temp_pat4']\
or not request.form['temp_pat5']\
or not request.form['temp_pat6']\
or not request.form['temp_pat7']\
or not request.form['temp_pat8']\
or not request.form['temp_pat9']\
or not request.form['temp_ebp0']\
or not request.form['temp_ebp1']\
or not request.form['temp_ebp2']\
or not request.form['temp_ebp3']\
or not request.form['temp_ebp4']\
or not request.form['temp_ebp5']\
or not request.form['temp_ebp6']\
or not request.form['temp_ebp7']\
or not request.form['temp_ebp8']\
or not request.form['temp_ebp9'] ):
         flash('Ingrese todos los campos', 'error')
      else:
        temp_ambiente=request.form['temp_ambiente']
        humedad= request.form['humedad']
        persona_id= request.form['persona_id']
        ebp= request.form['ebp']
        sonda= request.form['sonda']

        temp_pat=[request.form['temp_pat0'],\
        request.form['temp_pat1'],\
        request.form['temp_pat2'],\
        request.form['temp_pat3'],\
        request.form['temp_pat4'],\
        request.form['temp_pat5'],\
        request.form['temp_pat6'],\
        request.form['temp_pat7'],\
        request.form['temp_pat8'],\
        request.form['temp_pat9']]

        temp_ebp=[request.form['temp_ebp0'],\
        request.form['temp_ebp1'],\
        request.form['temp_ebp2'],\
        request.form['temp_ebp3'],\
        request.form['temp_ebp4'],\
        request.form['temp_ebp5'],\
        request.form['temp_ebp6'],\
        request.form['temp_ebp7'],\
        request.form['temp_ebp8'],\
        request.form['temp_ebp9']]

        existe = Persona.query.filter(Persona.nombre == persona_id).first()
        if not existe:
            flash('"La persona no existe !"')
        else:
            existe = Equipo.query.filter(Equipo.nombre == ebp).first()
            if not existe:
                flash('"El equipo no existe !"')
            else:
                existe = Sonda.query.filter(Sonda.nombre == sonda).first()
                if not existe:
                    flash('"La sonda no existe !"')
                else:
                    try:
                        print("cargando las mediciones")
                        medicion = Medicion(temp_ambiente, humedad, persona_id, ebp, sonda,\
                        request.form['temp_pat0'],\
                        request.form['temp_pat1'],\
                        request.form['temp_pat2'],\
                        request.form['temp_pat3'],\
                        request.form['temp_pat4'],\
                        request.form['temp_pat5'],\
                        request.form['temp_pat6'],\
                        request.form['temp_pat7'],\
                        request.form['temp_pat8'],\
                        request.form['temp_pat9'],\
                        request.form['temp_ebp0'],\
                        request.form['temp_ebp1'],\
                        request.form['temp_ebp2'],\
                        request.form['temp_ebp3'],\
                        request.form['temp_ebp4'],\
                        request.form['temp_ebp5'],\
                        request.form['temp_ebp6'],\
                        request.form['temp_ebp7'],\
                        request.form['temp_ebp8'],\
                        request.form['temp_ebp9'])
                        db.session.add(medicion)
                    except Exception as error:
                        print("error al cargar la medicion")
                        print(str(error))
                        db.session.rollback()
                        flash('error al cargar la medicion', 'error')
                    else:
                        db.session.commit()
                        temp_pat=[float(request.form['temp_pat0']),\
                        float(request.form['temp_pat1']),\
                        float(request.form['temp_pat2']),\
                        float(request.form['temp_pat3']),\
                        float(request.form['temp_pat4']),\
                        float(request.form['temp_pat5']),\
                        float(request.form['temp_pat6']),\
                        float(request.form['temp_pat7']),\
                        float(request.form['temp_pat8']),\
                        float(request.form['temp_pat9'])]

                        temp_ebp=[float(request.form['temp_ebp0']),\
                        float(request.form['temp_ebp1']),\
                        float(request.form['temp_ebp2']),\
                        float(request.form['temp_ebp3']),\
                        float(request.form['temp_ebp4']),\
                        float(request.form['temp_ebp5']),\
                        float(request.form['temp_ebp6']),\
                        float(request.form['temp_ebp7']),\
                        float(request.form['temp_ebp8']),\
                        float(request.form['temp_ebp9'])]
                        Certificado_pdf(temp_pat,temp_ebp,medicion)
                        flash('La medicion fue cargada correctamente')
                        return redirect(url_for('Listar_todas_las_mediciones'))
   return render_template('Alta_medicion.html')


@app.route('/Listar_todos_los_equipos')
def Listar_todos_los_equipos():
   return render_template('Listar_todos_los_equipos.html', equipos = Equipo.query.all() )

@app.route('/Alta_equipo', methods = ['GET', 'POST'])
def Alta_equipo():
    if request.method == 'POST':
        if not request.form['nombre'] or not request.form['marca']or not request.form['modelo']or not request.form['n_serie']or not request.form['fecha']:
            flash('Ingrese todos los campos', 'error')
        else:
            marca= request.form['marca']
            nombre_equipo      =request.form['nombre']
            modelo=request.form['modelo']
            n_serie= request.form['n_serie']
            fecha_alta= request.form['fecha']
            observaciones= request.form['observaciones']

            existe = Equipo.query.filter(Equipo.nombre == nombre_equipo).first()
            if existe:
                flash('"El equipo ya existe !"')
            else:
                try:
                    equipo = Equipo(nombre_equipo, marca, modelo, n_serie, fecha_alta, observaciones)
                    db.session.add(equipo)
                except Exception as error:
                    print("ERROR ! al cargar el equipo !")
                    print(str(error))
                    db.session.rollback()
                    flash('"ERROR ! al cargar el equipo !"')
                else:
                    db.session.commit()
                    flash('El equipo fue cargado correctamente')
                    return redirect(url_for('Listar_todos_los_equipos'))
    return render_template('Alta_equipo.html')

@app.route('/Alta_persona', methods = ['GET', 'POST'])
def Alta_persona():
   if request.method == 'POST':
      if not request.form['name'] or not request.form['city'] or not request.form['addr']:
         flash('Ingrese todos los campos', 'error')
      else:
        nombre      =request.form['name']
        email       =request.form['city']
        direccion   =request.form['addr']
        telefono    =request.form['pin']

        existe = Persona.query.filter(Persona.nombre == nombre).first()
        if existe:
            flash('"La persona ya existe !"')
        else:
            try:
                persona = Persona(nombre,email,direccion,telefono)
                db.session.add(persona)

            except Exception as error:
                print("ERROR ! al cargar la persona!")
                print(str(error))
                db.session.rollback()
                flash('"ERROR ! al cargar la persona !"')
            else:
                db.session.commit()
                flash('La persona fue agregada correctamente')
                return redirect(url_for('Listar_todas_las_personas'))
   return render_template('Alta_persona.html')

@app.route('/Listar_todas_las_personas')
def Listar_todas_las_personas():
    return render_template('Listar_todas_las_personas.html', personas = Persona.query.all() )

@app.route('/Alta_sonda', methods = ['GET', 'POST'])
def Alta_sonda():
   if request.method == 'POST':
      if not request.form['nombre'] or not request.form['fecha_alta']:
         flash('Ingrese todos los campos', 'error')
      else:
        nombre              =request.form['nombre']
        fecha               =request.form['fecha_alta']
        observaciones       =request.form['observaciones']

        existe = Sonda.query.filter(Sonda.nombre == nombre).first()
        if existe:
            flash('"La sonda ya existe !"')
        else:
            try:
                sonda = Sonda(nombre,fecha,observaciones)
                db.session.add(sonda)
            except Exception as error:
                print("ERROR ! al cargar la sonda!")
                print(str(error))
                db.session.rollback()
                flash('"ERROR ! al cargar la sonda !"')
            else:
                db.session.commit()
                flash('La sonda fue agregada correctamente')
                return redirect(url_for('Listar_todas_las_sondas'))
   return render_template('Alta_sonda.html')

@app.route('/Listar_todas_las_sondas')
def Listar_todas_las_sondas():
    return render_template('Listar_todas_las_sondas.html', sondas = Sonda.query.all() )

@app.route('/Historico_sondas')
def Historico_sondas():
    """"Genero el reporte de mediciones de equipos"""
    result = db.engine.execute("SELECT Equipo.nombre as nombre_equipo,\
        Sonda.nombre as Sonda_nombre, \
        Medicion.id as medcion_id, \
        Certificado.id as certificado_id, \
        Certificado.temp as certificado_temp, \
        Certificado.correcion as certificado_correcion, \
        Certificado.incert as certificado_incert \
        FROM Equipo \
        join Medicion on (Medicion.equipo_id = Equipo.id )\
        join Sonda on (Sonda.id = Medicion.sonda_id )\
        join Certificado on (Certificado.id = Medicion.id )\
        ORDER BY Equipo.id;")

    print("imprimo lo que sale de la mega consulta")
    reporte = []
    for lista in result:
        reporte.append(lista[:])
    print(reporte)
    print("-----------")

    PDF.Historico_pdf_2(reporte)

    return render_template('Indice.html')
    #return render_template('Historico_sondas.html',  )

if __name__ == '__main__':

    #creo el directorio para los certificados#
    now = datetime.datetime.now()
    nowAux = str(now)
    carpeta = nowAux[0:10]

    if not os.path.exists("certificados/"):
        os.makedirs("certificados/")
        print ("Carpeta creada:"+ "certificados/")

    if not os.path.exists("Historico_sondas/"):
        os.makedirs("Historico_sondas/")
        print ("Carpeta creada:"+ "Historico_sondas/")

    db.create_all()

    #app.run(debug = True)# para ambiente local
    #busco la ip local para poner en lan la app

    gw = os.popen("ip -4 route show default").read().split()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect((gw[2], 0))
    ipaddr = s.getsockname()[0]
    gateway = gw[2]
    host = socket.gethostname()
    print("---Datos de configuracion LAN---")
    print ("IP:", ipaddr, " GW:", gateway, " Host:", host)
    print("--------------------------------")

    #app.run(host='127.0.1.1')# poner la iplan ejemple
    app.run(host=ipaddr)
