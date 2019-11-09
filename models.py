from sqlalchemy import Table, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import mapper
from app_things import db


##----Definiciones de class
##http://flask-sqlalchemy.pocoo.org/2.3/models/
class Sonda(db.Model):
    #__tablename__ = 'Sonda'
    id = db.Column( db.Integer, primary_key = True)
    nombre = db.Column(db.String(100))
    observaciones = db.Column(db.String(100))
    fecha_alta = db.Column(db.String(100))
    fecha_baja = db.Column(db.String(100))
    activa = db.Column(db.Boolean, default=True)
    mediciones=db.relationship('Medicion', back_populates='sonda')

    def __init__(self, nombre, fecha, observaciones):
        self.nombre = nombre
        self.fecha_alta = fecha
        self.observaciones = observaciones

class Equipo(db.Model):
    #__tablename__ = 'equipo'
    #id = db.Column('Equipo.id', db.Integer, primary_key = True)
    id = db.Column(db.Integer, primary_key = True)
    nombre =db.Column(db.String(50))
    marca = db.Column(db.String(500))
    modelo = db.Column(db.String(50))
    n_serie = db.Column(db.String(50))
    observaciones = db.Column(db.String(10))
    fecha_alta = db.Column(db.String(100))

    fecha_baja = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)
    mediciones=db.relationship('Medicion', back_populates='equipo')

    def __init__(self, name, marca, modelo,n_serie,fecha,observaciones):
        self.nombre=name
        self.marca = marca
        self.modelo = modelo
        self.n_serie = n_serie
        self.observaciones = observaciones
        self.fecha_alta=fecha

class Persona(db.Model):
    #__tablename__ = 'persona'
    id = db.Column( db.Integer, primary_key = True)
    nombre = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(50))
    direccion = db.Column(db.String(200))
    telefono = db.Column(db.String(10))
    mediciones=db.relationship('Medicion', back_populates='midio')
    fecha_alta = db.Column(db.String(100))
    fecha_baja = db.Column(db.String(100))
    activo = db.Column(db.Boolean, default=True)


    def __init__(self, name= None, city= None, addr= None, telefono = None):
        self.nombre = name
        self.email = city
        self.direccion = addr
        self.telefono= telefono


class Certificado_INTI(db.Model):
    #__tablename__ = 'Certificado'
    id = db.Column(db.Integer, primary_key = True)
    Fecha_de_calibracion = db.Column(db.String(100))

    temp_n30=db.Column(db.Float)
    correcion_n30=db.Column(db.Float)
    incert_n30=db.Column(db.Float)

    temp_0=db.Column(db.Float)
    correcion_0=db.Column(db.Float)
    incert_0=db.Column(db.Float)

    temp_37=db.Column(db.Float)
    correcion_37=db.Column(db.Float)
    incert_37=db.Column(db.Float)

    temp_100=db.Column(db.Float)
    correcion_100=db.Column(db.Float)
    incert_100=db.Column(db.Float)

    temp_200=db.Column(db.Float)
    correcion_200=db.Column(db.Float)
    incert_200=db.Column(db.Float)


    certificados_internos=db.relationship('Certificado', back_populates='certificado_INTI')

    def __init__(self, \
        temp_n30,\
        correcion_n30,\
        incert_n30,\
        temp_0,\
        correcion_0,\
        incert_0,\
        temp_37,\
        correcion_37,\
        incert_37,\
        temp_100,\
        correcion_100,\
        incert_100,\
        temp_200,\
        correcion_200,\
        incert_200 ,    Fecha_de_calibracion   ):
        self.Fecha_de_calibracion=Fecha_de_calibracion
        self.temp_n30=temp_n30
        self.correcion_n30=correcion_n30
        self.incert_n30=incert_n30

        self.temp_0=temp_0
        self.correcion_0=correcion_0
        self.incert_0=incert_0

        self.temp_37=temp_37
        self.correcion_37=correcion_37
        self.incert_37=incert_37

        self.temp_100=temp_100
        self.correcion_100=correcion_100
        self.incert_100=incert_100

        self.temp_200=temp_200
        self.correcion_200=correcion_200
        self.incert_200=incert_200




class Certificado(db.Model):
    #__tablename__ = 'Certificado'
    id = db.Column(db.Integer, primary_key = True)
    Fecha_de_calibracion = db.Column(db.String(100))
    temp=db.Column(db.Float)
    correcion=db.Column(db.Float)
    incert=db.Column(db.Float)

    medicion_id = db.Column(db.Integer, db.ForeignKey('medicion.id'))
    medicion = db.relationship("Medicion", back_populates='certificado')


    certificado_INTI_id = db.Column(db.Integer, db.ForeignKey('certificado_INTI.id'))
    certificado_INTI = db.relationship("Certificado_INTI", back_populates='certificados_internos')



    def __init__(self, medicion=None,temp=None,correcion=None,incertidumbre=None):
        #self.Fecha_de_calibracion=Fecha_de_calibracion
        self.temp=temp
        self.correcion=correcion
        self.incert=incertidumbre
        self.medicion=Medicion.query.filter(Medicion.id == medicion.id).one()
        self.certificado_INTI=Certificado_INTI.query.order_by(Certificado_INTI.id.desc()).first()

class Medicion(db.Model):
    #__tablename__ = 'medicion'
    id = db.Column(db.Integer, primary_key = True)
    temp_ambiente = db.Column(db.Integer)
    humedad = db.Column(db.Integer)

    midio_id = db.Column(db.Integer, db.ForeignKey('persona.id'))
    midio = db.relationship("Persona", back_populates='mediciones')

    equipo_id = db.Column(db.Integer, db.ForeignKey('equipo.id'))
    equipo = db.relationship("Equipo", back_populates='mediciones')

    sonda_id = db.Column(db.Integer, db.ForeignKey('sonda.id'))
    sonda = db.relationship("Sonda", back_populates='mediciones')

    certificado=db.relationship('Certificado',uselist=False, back_populates='medicion')



    temp_pat0=db.Column(db.Float)
    temp_pat1=db.Column(db.Float)
    temp_pat2=db.Column(db.Float)
    temp_pat3=db.Column(db.Float)
    temp_pat4=db.Column(db.Float)
    temp_pat5=db.Column(db.Float)
    temp_pat6=db.Column(db.Float)
    temp_pat7=db.Column(db.Float)
    temp_pat8=db.Column(db.Float)
    temp_pat9=db.Column(db.Float)
    temp_ebp0=db.Column(db.Float)
    temp_ebp1=db.Column(db.Float)
    temp_ebp2=db.Column(db.Float)
    temp_ebp3=db.Column(db.Float)
    temp_ebp4=db.Column(db.Float)
    temp_ebp5=db.Column(db.Float)
    temp_ebp6=db.Column(db.Float)
    temp_ebp7=db.Column(db.Float)
    temp_ebp8=db.Column(db.Float)
    temp_ebp9=db.Column(db.Float)



    def __init__(self, temp_ambiente= None, humedad= None, persona=None, edp=None, sonda= None,\
    temp_pat0=None,\
    temp_pat1=None,\
    temp_pat2=None,\
    temp_pat3=None,\
    temp_pat4=None,\
    temp_pat5=None,\
    temp_pat6=None,\
    temp_pat7=None,\
    temp_pat8=None,\
    temp_pat9=None,\
    temp_ebp0=None,\
    temp_ebp1=None,\
    temp_ebp2=None,\
    temp_ebp3=None,\
    temp_ebp4=None,\
    temp_ebp5=None,\
    temp_ebp6=None,\
    temp_ebp7=None,\
    temp_ebp8=None,\
    temp_ebp9=None):
         self.temp_ambiente =temp_ambiente
         self.humedad=humedad
         self.midio = Persona.query.filter(Persona.nombre == persona).one()
         self.equipo= Equipo.query.filter(Equipo.nombre == edp).one()
         self.sonda= Sonda.query.filter(Sonda.nombre == sonda).one()
         self.temp_pat0=temp_pat0
         self.temp_pat1=temp_pat1
         self.temp_pat2=temp_pat2
         self.temp_pat3=temp_pat3
         self.temp_pat4=temp_pat4
         self.temp_pat5=temp_pat5
         self.temp_pat6=temp_pat6
         self.temp_pat7=temp_pat7
         self.temp_pat8=temp_pat8
         self.temp_pat9=temp_pat9
         self.temp_ebp0=temp_ebp0
         self.temp_ebp1=temp_ebp1
         self.temp_ebp2=temp_ebp2
         self.temp_ebp3=temp_ebp3
         self.temp_ebp4=temp_ebp4
         self.temp_ebp5=temp_ebp5
         self.temp_ebp6=temp_ebp6
         self.temp_ebp7=temp_ebp7
         self.temp_ebp8=temp_ebp8
         self.temp_ebp9=temp_ebp9
