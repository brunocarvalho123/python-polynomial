#!/usr/bin/python
from tkinter import *
import tkinter.messagebox
import re

'''
@author: Bruno Carvalho 201508043

'''

def normalizar(poli):
    for j in range(len(poli)):
        tipo = type(poli[j])
        if tipo is int:
            var = 'int'
            if poli[j] == 0:
                poli.pop(j)
                return normalizar(poli)
        else:
            var = poli[j][1]
            exp = poli[j][2]
        for i in range(j+1,len(poli)):
            if (type(poli[i]) == tipo) and tipo is not int:
                if poli[i][1] == var and poli[i][2] == exp:
                    if(poli[i][0]+poli[j][0] != 0):
                        poli.append((poli[i][0]+poli[j][0],var,exp))
                    poli.pop(i)
                    poli.pop(j)
                    return normalizar(poli)
            if (type(poli[i]) == tipo) and tipo is int:
                poli.append(poli[i] + poli[j])
                poli.pop(i)
                poli.pop(j)
                return normalizar(poli)
    return poli

def somar(poli1, poli2):
    poli1.extend(poli2)
    return normalizar(poli1)

def derivar(poli):
    for i in range(len(poli)):
        if(type(poli[i]) is int):
            poli[i] = 0;
        elif (poli[i][2]==1):
            poli[i]=poli[i][0]
        else:
            poli[i] = (poli[i][0]*poli[i][2],poli[i][1],poli[i][2]-1)
    return normalizar(poli)

def primitivar(poli, var):
    poli = normalizar(poli)
    for i in range(len(poli)):
        if(type(poli[i]) is int):
            poli[i] = (poli[i],var,1)
        elif((poli[i][2]==1) and (poli[i][1]==var)):
            if(poli[i][0] % 2 == 0):
                poli[i]=(int(poli[i][0]/2),poli[i][1],poli[i][2]+1)
            else:
                poli[i]=(str(poli[i][0])+'/2',poli[i][1],poli[i][2]+1)
        elif(poli[i][1]==var):
            if(poli[i][0] % (poli[i][2]+1) == 0):
                poli[i]=(int(poli[i][0]/(poli[i][2]+1)),poli[i][1],poli[i][2]+1)
            else:
                poli[i]=(str(poli[i][0])+'/'+str((poli[i][2])+1),poli[i][1],poli[i][2]+1)
        else:
            poli[i]=(poli[i][0],(poli[i][1]+var),poli[i][2])
    return poli

#transforma uma string numa lista de tuplos e inteiros
def polToList(s):
    #separar
    poli = s.split('+')
    for i in range(len(poli)):
        if(not poli[i].isdigit()):
            poli[i] = re.findall('(\d+|\D?)',poli[i])
            poli[i] = poli[i][:-1]

    #transformar de str para int
    for i in range(len(poli)):
        if(type(poli[i]) is list):
            for j in range(len(poli[i])):
                if(poli[i][j].isdigit()):
                    poli[i][j]=int(poli[i][j])
        else:
            poli[i]=int(poli[i])

    #apagar o simbolo de potencia '^' e criar negativos
    for i in range(len(poli)):
        if(type(poli[i]) is not int):
            for j in range(len(poli[i])):
                if(j==0):
                    if(poli[i][j]=='-'):
                        poli[i][j+1] = poli[i][j+1]*-1
                        del poli[i][j]
                        break
            for j in range(len(poli[i])):
                if(poli[i][j]=='^'):
                    del poli[i][j]
                    break

    #apagar listas com um unico elemento
    for i in range(len(poli)):
        if(type(poli[i]) is not int and len(poli[i])==1):
            poli[i]=poli[i][0]

    #transformar em tuplo
    for i in range(len(poli)):
        if(type(poli[i]) is not int):
            if(len(poli[i])==2):
                poli[i].append(1)
            poli[i]=tuple(poli[i])
    return poli

#transforma uma lista de tuplos e inteiros numa string
def printPoli(poli):
    s = ''
    for i in range(len(poli)):
        if(type(poli[i]) is tuple):
            for j in range(len(poli[i])):
                if(type(poli[i][j]) is int):
                    if(j==2):
                        if(poli[i][j]!=1):
                            s = s + '^' + str(poli[i][j])
                    else:
                        s = s + str(poli[i][j])
                else:
                    s = s + poli[i][j]
        else:
            s = s+str(poli[i])
        s=s+'+'
    return s[:-1]




root = Tk()
root.resizable(width=False, height=False)
root.minsize(width=550, height=200)

top = Frame(root)
top.pack()
mid = Frame(root)
mid.pack()
bot = Frame(root)
bot.pack(ipady=10)

label1 = Label(top, text='Manipulador Algébrico', font=('Verdana',20))
label1.pack(ipady=0)

v= IntVar()

def disable():
    text2.config(state='disabled')
    label3.config(text='Aux:',font=('Helvetica',14))
def soma():
    text2.config(state='normal')
    label3.config(text='Poli 2:',font=('Helvetica',14))
def prim():
    text2.config(state='normal')
    label3.config(text='Em função a:',font=('Helvetica',10))

rbutton1 = Radiobutton(top, text = 'Normalizar', variable=v, value=1, \
                        font=('Helvetica',14),command=disable)
rbutton2 = Radiobutton(top, text = 'Somar', variable=v, value=2, \
                        font=('Helvetica',14),command=soma)
rbutton3 = Radiobutton(top, text= 'Derivar', variable=v, value=3, \
                        font=('Helvetica',14),command=disable)
rbutton4 = Radiobutton(top, text = 'Primitivar', variable=v, value=4, \
                        font=('Helvetica',14),command=prim)

rbutton1.pack(side=LEFT,ipady=25)
rbutton2.pack(side=LEFT)
rbutton3.pack(side=LEFT)
rbutton4.pack(side=LEFT)

label2 = Label(mid, text='Polinómio: ', font=('Helvetica',14))
label2.grid(row=0, column=0)
text = Entry(mid,font=('Helvetica',14))
text.grid(row=0, column=1, ipadx=38)

label3 = Label(mid, text='Aux: ', font=('Helvetica',14))
label3.grid(row=1, column=0,ipady=15, sticky=W)
text2 = Entry(mid,font=('Helvetica',14))
text2.grid(row=1, column=1, ipadx=38)
text2.config(state='disabled')

#verificar se o que se encontra no text2 é uma variavel
def check(a):
    if(len(a)>1):
        return 0
    if(a.isdigit()):
        return 0
    else:
        return 1

def calc():
    if(v.get() == 1):
        tkinter.messagebox.showinfo('resultado',(printPoli(\
                normalizar(polToList(text.get())))))
    if(v.get() == 2):
        tkinter.messagebox.showinfo('resultado',(printPoli(\
                somar(polToList(text.get()),polToList(text2.get())))))
    if(v.get() == 3):
        tkinter.messagebox.showinfo('resultado',(printPoli(\
                derivar(polToList(text.get())))))
    if(v.get() == 4):
        if(check(text2.get())==1):
            tkinter.messagebox.showinfo('resultado',(printPoli(\
                    primitivar(polToList(text.get()),text2.get()))))
        else:
            tkinter.messagebox.showinfo('resultado','ERRO')

button1 = Button(bot, text='Calcular', command=calc, font=('Helvetica',14))
button1.pack()

top.mainloop()
