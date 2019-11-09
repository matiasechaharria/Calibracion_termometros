
# Imports necesarios
import numpy  as np # importando numpy
import matplotlib.pyplot as plt
import pandas as pd # importando pandas
import crear_pdf.crear_pdf as PDF
#recta de regresion lineal


def error_tipico(Certificado):
    """Esta funcion devuelve el valor del error tipico del equipo"""
    N=5
    T=0.04

    Sx=np.sum(Certificado, axis=0)[:1]
    Sy=np.sum(Certificado, axis=0)[1:2]
    Sxx_aux=np.power(Certificado[:],2)
    Sxx=np.sum(Sxx_aux, axis=0)[:1]
    #Sxy
    Sxy=    Certificado[0][0]*Certificado[0][1]+Certificado[1][0]*Certificado[1][1]+ Certificado[2][0]*Certificado[2][1]+ Certificado[3][0]*Certificado[3][1]+Certificado[4][0]*Certificado[4][1]
    #Syy
    Syy_aux=np.power(Certificado,2)
    Syy=np.sum(Syy_aux, axis=0)[1:2]

    a_n_aux=N*Sxy-Sx*Sy
    b_n_aux=N*Sxx-Sx*Sx
    m=a_n_aux/b_n_aux

    a_m_aux=Sxx*Sy-Sx*Sxy
    n=a_m_aux/b_n_aux
    Cc=m*T+n

    #(n+m xi - yi)2
    error_tipico= (n+m* Certificado[0][0]-Certificado[0][1])*(n+m* Certificado[0][0]-Certificado[0][1])+(n+m*Certificado[1][0]-Certificado[1][1])*(n+m*Certificado[1][0]-Certificado[1][1])+(n+m*Certificado[2][0]-Certificado[2][1])*(n+m*Certificado[2][0]-Certificado[2][1])+(n+m*Certificado[3][0]-Certificado[3][1])*(n+m*Certificado[3][0]-Certificado[3][1])+(n+m*Certificado[4][0]-Certificado[4][1])*(n+m*Certificado[4][0]-Certificado[4][1])
    return(error_tipico)



def interpolacion_patron(Certificado):
    """ busca el factor de correccion interpolado del certificado de calibracion"""
    #http://cs231n.github.io/python-numpy-tutorial/#numpy-arrays
    N=5
    T=0.04


    Sx=np.sum(Certificado, axis=0)[:1]
    Sy=np.sum(Certificado, axis=0)[1:2]
    Sxx_aux=np.power(Certificado[:],2)
    Sxx=np.sum(Sxx_aux, axis=0)[:1]
    #Sxy
    Sxy=    Certificado[0][0]*Certificado[0][1]+Certificado[1][0]*Certificado[1][1]+ Certificado[2][0]*Certificado[2][1]+ Certificado[3][0]*Certificado[3][1]+Certificado[4][0]*Certificado[4][1]
    #Syy
    Syy_aux=np.power(Certificado,2)
    Syy=np.sum(Syy_aux, axis=0)[1:2]
    a_n_aux=N*Sxy-Sx*Sy
    b_n_aux=N*Sxx-Sx*Sx
    m=a_n_aux/b_n_aux
    a_m_aux=Sxx*Sy-Sx*Sxy
    n=a_m_aux/b_n_aux

    Cc=m*T+n
    #print("Cc= ", Cc)
    #print("recta de m*x+n =  ", m,"T",n )
    return(m,n)

def temp_calibracion(Certificado,patron):
    """regresa el valor de Temperatura real de calibracion"""
    m,n=interpolacion_patron(Certificado)
    tcp=m*np.average(patron)+n
    return(tcp+np.average(patron))

def cifra_correccion(ebp,temp):
    """calcula la cifra de correccion"""
    return(temp-np.average(ebp))


def incertidumbre(Certificado,tcp):
    """busco valor de la incertidumbre tipo b"""
    if tcp<= Certificado[0][0] :
        return(Certificado[0][2]/2)

    elif  Certificado[0][0] <= tcp  and tcp<= Certificado[1][0]:
        return(Certificado[1][2]/2)

    elif  Certificado[1][0] <= tcp  and tcp<= Certificado[2][0]:
        return(Certificado[2][2]/2)

    elif  Certificado[2][0] <= tcp  and tcp<= Certificado[3][0]:
        return(Certificado[3][2]/2)

    elif  Certificado[3][0] <= tcp  and tcp<= Certificado[4][0]:
        return(Certificado[3][2]/2)

    elif  Certificado[4][0] <= tcp:
        return(Certificado[4][2]/2)

def valores_para_certificado(Certificado,patron,ebp,):
    """Retorna el valor de Temperatura, correccion e incertidumbre para el certificado de calibracion"""

    tcp=temp_calibracion(Certificado,patron)
    coorrecion=cifra_correccion(ebp,tcp)
    print("temp_calibracion",tcp)
    tipob=(incertidumbre(Certificado,tcp))
    errort=error_tipico(Certificado)

    estabilidad=0.1/((12)**1/2)
    uniformidad=0.1/((12)**1/2)
    resolusion_patron=0.01/((12)**0.5)

    tipob_combinada=((tipob**2+estabilidad**2+uniformidad**2+resolusion_patron**2+errort**2)**0.5)
    resolusion_ebp=0.01/((12)**0.5)


    tipo_AB_combinada=(np.std(ebp)**2+resolusion_ebp**2+tipob_combinada**2 )**0.5
    tipo_AB_combinada=tipo_AB_combinada*2

    return(np.average(ebp),coorrecion ,tipo_AB_combinada)

if __name__ == '__main__':

    patron=[-19.34,	-19.34	,-19.34	,-19.34,	-19.34	,-19.34	,-19.34,	-19.34	,-19.34	,-19.34]
    ebp=[-18.42	,-18.42,	-18.42	,-18.43,	-18.43	,-18.43,	-18.43,	-18.43,	-18.43,	-18.43]

    Certificado_INTI=[[  -31.14  ,  0.27	,0.04,	2],
                        [-0.09,	0.09	,0.05,	2],
                        [37.14,	-0.13	,0.1,	2],
                        [100.49	,-0.35	,0.04,	2],
                        [200.74,	-0.55	,0.07,	2]]



    print("average ebp =",np.average(ebp))
    print("average patron =",np.average(patron))
    temp,correccion,incert= valores_para_certificado(Certificado_INTI,patron,ebp)
    print("Temperatura = "+str(temp) +" Correccion = " +str(correccion) +" Incertidumbre = "+ str( incert))
    PDF.export_certificado(temp,correccion,incert)
    #PDF.simple_table()
