"""
Práctica 3: Sistema musculoesquelético

Departamento de Ingeniería Eléctrica y Electrónica, Ingeniería Biomédica
Tecnológico Nacional de México [TecNM - Tijuana]
Blvd. Alberto Limón Padilla s/n, C.P. 22454, Tijuana, B.C., México

Nombre del alumno: Josue Raul Guerrero Peñaloza
Número de control: 24210583
Correo institucional: l24210583@tectijuana.edu.mx

Asignatura: Modelado de Sistemas Fisiológicos
Docente: Dr. Paul Antonio Valle Trujillo; paul.valle@tectijuana.edu.mx
"""
# Instalar librerias en consola
# pip install numpy control matplotlib

# librerias
import numpy as np
import math as m
import control as ctrl
import matplotlib.pyplot as plt

# datos generales de la simulacion
x0,t0,tend,dt,w,h, = 0,0,10,1E-3,7,3.5
N = round(tend/dt)+1
t = np.linspace(t0,tend,N)
F = np.zeros(N); F[round(1/dt):round(2/dt)] = 1


#FT control
a,R,Cs,Cp = 0.25,100,10E-6,100E-6
num = [R*Cs,1-a]
den = [R*(Cp + Cs),1]
Control = ctrl.tf(num,den)
print(f"Funcion de transferencia Control: {Control}\n")

#FT caso
a,R,Cs,Cp = 0.25,10E3,10E-6,100E-6
num = [R*Cs,1-a]
den = [R*(Cp + Cs),1]
Caso = ctrl.tf(num,den)
print(f"Funcion de transferencia Caso: {Caso}\n")


#componenetes del controlador
kP,kI = 0.4052,1961.2460

numPID = [kP, kI]
denPID = [1, 0]
PID = ctrl.tf(numPID, denPID)

#Sistema de control tratamiento
Tratamiento = ctrl.feedback(ctrl.series(PID,Caso),1,sign = -1)
print(f"Funcion de transferencia en Controlador: {Tratamiento}\n")

Fsx = ctrl.forced_response(Control, t, F).outputs
Fsy = ctrl.forced_response(Caso, t, F).outputs
Tratamiento = ctrl.forced_response(Tratamiento, t, Fsx).outputs



#colores
clr1 = np.array([149, 100, 221])/256
clr2 = np.array([228, 218, 114])/256
clr3 = np.array([62, 15, 141])/256



#Grafica
fg = plt.figure(1)
fg.set_size_inches(w, h)

plt.rcParams["font.size"] = 11
plt.rcParams["font.family"] = "serif"
plt.rcParams["font.serif"] = ["Times New Roman"]

plt.plot(t, F, "-", color=clr2, label="F(t)")
plt.plot(t, Tratamiento, "--", color=clr3, label="PID(t): Tratamiento")
plt.plot(t, Fsy, ":", color=clr2, label="Fsy(t): Caso")
plt.plot(t, Fsx, ":", color=clr1, label="Fsx(t): Control")

plt.xlim(-0.25, 10)
plt.xticks(np.arange(0, 11, 1))
plt.ylim(-0.1, 1.1)
plt.yticks(np.arange(0, 1.1, 0.2))
plt.xlabel("t [s]")
plt.ylabel("F(t) [V]")
plt.legend(loc="best", ncol=2, frameon=False)
plt.grid()
plt.show()
fg.savefig("CasoTratamiento_python.pdf", bbox_inches="tight")
