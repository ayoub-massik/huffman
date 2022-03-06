from tkinter import *
import tkinter.font as font
from tkinter import filedialog as fd
from tkinter import scrolledtext
import math
import compresser
import decompresser
class window():
	def __init__(self):
		self.wind=Tk()
		self.wind.title("AyoubMassik")
		self.wind.state("zoomed")
		self.wind.configure(background='white')
		Open=Button(self.wind,text="Open",border=0,command=self.open,fg="Black",bg="#ffc107",width=12,height=2,font=('Lucida Calligraphy',12,'bold')) 
		Open.place(x=10,y=10)
		Save=Button(self.wind,text="Save",border=0,command=self.save,fg="Black",bg="#ffc107",width=12,height=2,font=('Lucida Calligraphy',12,'bold')) 
		Save.place(x=190,y=10)
		self.txt1=scrolledtext.ScrolledText(self.wind,width=123,height=19)
		self.txt1.place(x=355,y=70)
		self.txt2=scrolledtext.ScrolledText(self.wind,width=123,height=17)
		self.txt2.place(x=355,y=402)
		self.txt3=scrolledtext.ScrolledText(self.wind,fg="green",bg="#f0f6fd",width=40,height=38)
		self.txt3.place(x=10,y=70)
		Label(self.wind,text="Original File",bg="#fff").place(x=355,y=48)
		Label(self.wind,text="Result",bg="#fff").place(x=355,y=380)
		self.ED=True
		self.text=""
		self.fileName=""
		self.wind.mainloop()
	def save(self):
		if self.ED:
			name=fd.asksaveasfile(mode='w',defaultextension=".bin")
		else:
			name=fd.asksaveasfile(mode='w',defaultextension=".txt")
		name.write(self.text)
		name.close
	def open(self):		
		self.fileName=fd.askopenfilename(title='Open a file',initialdir='/',filetypes=(('text files','*.txt'),('All files','*.*')))
		self.txt1.delete(1.0,END)
		self.txt2.delete(1.0,END)
		self.txt3.delete(1.0,END)
		if self.fileName[-3:]=="txt":
			self.ED=True
			self.encode(self.fileName)
		elif self.fileName[-3:]=="bin":
			self.ED=False
			self.decode(self.fileName)
	def decode(self,fileName):
		if fileName:
			with open(fileName) as f:
				text=f.read()
			ch,bt=[],[]
			x=""
			j=0
			for i in text:
				if i=="%":
					ch.append(x[0])
					bt.append(x[1::])
					x=""
				else:	
					x+=i
				j+=1
				if i=="&":
					break
			text=text[j::]
			res=""
			res=decompresser.decrypt(text,bt,ch)
			# print(text)
			# print(res)
			self.txt1.insert(INSERT,text)
			self.txt2.insert(INSERT,res)
			inf=""
			inf+="\n File Name :\n  "+fileName+"\n Storage :"
			inf+="\n  Original	"+str(len(text)/8)+" Octet(s)"
			inf+="\n  Result	"+str(len(res))+" Octet(s)"
			inf+="\n  Gain	"+str((len(res)-len(text)/8)*100/len(res))+" %\n"
			inf+="\n  *********** Informations ***********"
			for i in range(len(ch)):
				inf+="\n"+ch[i]+" > "+bt[i]
			self.txt3.insert(INSERT,inf)
	def encode(self,fileName):
		inf=""
		if fileName:
			with open(fileName) as f:
				text=f.read()
			self.txt1.insert(INSERT,text)	
			fre,P=compresser.compteur(fileName)
			binc=compresser.calcbin(fre)
		text01=""
		for i in text:
			if i in P:
				text01+=binc[i]
			else:
				text01+="\n"
			# text01+="|"
		self.text=""
		texte=text.replace("\n"," ")
		self.txt2.insert(INSERT,text01)
		inf+="\n File Name :\n  "+fileName+"\n Storage :"
		inf+="\n  Original	"+str(len(texte))+" Octet(s)"
		inf+="\n  Result	"+str(len(text01)/8)+" Octet(s)"
		inf+="\n  Gain	"+str((len(texte)-len(text01)/8)*100/len(texte))+" %\n"
		inf+="\n  *********** Informations ***********"
		entropy=Rmoy=0
		for i in P:
			self.text+=str(i)+binc[i]+"%"
			inf+="\n	"+str(i)+"="+str(P[i])+"	"+binc[i]
			entropy+=P[i]*math.log(P[i],2)*-1
			Rmoy+=P[i]*len(binc[i])
		self.text+="&"
		inf+="\n\n H(s) = "+str(entropy)+" sh/sym"
		inf+="\n Rmoy = "+str(Rmoy)+" bit/sym"
		self.txt3.insert(INSERT,inf)
		self.text+=text01
window().run()
