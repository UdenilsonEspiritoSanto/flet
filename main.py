from flet import *
# IMPORT YOU CREATE TABLE 
from myaction import create_table
from datatable import mytable,tb,calldb,buscar
import sqlite3
conn = sqlite3.connect("db/dbone.db",check_same_thread=False)

def main(page:Page):
    
	# AND RUN SCRIPT FOR CREATE TABLE WHEN FLET FIRST RUN
	create_table()
    

	page.scroll = "auto"

	def showInput(e):
		inputcon.offset = transform.Offset(0,0)
		page.update()

	def hidecon(e):
		inputcon.offset = transform.Offset(2,0)
		page.update()

	def savedata(e):
		try:
			# INPUT TO DATABASE
			c = conn.cursor()
			c.execute("INSERT INTO users (nome,idade,contato,email,endereco,genero) VALUES(?,?,?,?,?,?)",(nome.value,idade.value,contato.value,email.value,endereco.value,genero.value))
			conn.commit()
			print("success")

			# AND SLIDE RIGHT AGAIN IF FINAL INPUT SUUCESS
			inputcon.offset = transform.Offset(2,0)

			# ADD SNACKBAR IF SUCCESS INPUT TO DATABASE

			page.snack_bar = SnackBar(
				Text("Dado Registrado"),
				bgcolor="green"
				)

			page.snack_bar.open = True

			# REFRESH TABLE
			tb.rows.clear()
   
			calldb()
           
			tb.update()
			page.update()


		except Exception as e:
			print(e)

	# CREATE FIELD FOR INPUT
    
	nome = TextField(label="nome")
	idade = TextField(label="idade")
	contato = TextField(label="contato")
	email = TextField(label="email")
	endereco = TextField(label="endereco")
	genero = RadioGroup(content=Column([
		Radio(value="homem",label="Homem"),
		Radio(value="Mulher",label="Mulher")

		]))
    
	# CREATE MODAL INPUT FOR ADD NEW DATA 
     
  
	inputcon = Card(
       
		# ADD SLIDE LEFT EFFECT
		offset = transform.Offset(2,0),
		animate_offset = animation.Animation(600,curve="easeIn"),
		elevation=10,
        
		content=Container(
			content=Column([
				Row([
				Text("Cadastro",size=30,weight="bold"),
				IconButton(icon="close",icon_size=30,
				on_click=hidecon
					),
					],alignment="spaceBetween"),
				nome,
				idade,
				contato,
				email,
				genero,
				endereco,
				FilledButton("Guardar",
				on_click=savedata
					)

			])

		)

		)
                      
   
	page.add(
	Column([
		Text("ESCOLAR APP",size=30,weight="bold"),
		
		
        Row(
            
            [
            
        ElevatedButton("Cadastrar",bgcolor="green400",
		on_click=showInput   
		),
        
        TextField(label="procurar",on_change= buscar)
             ]),
		mytable,
		# AND DIALOG FOR ADD DATA
		inputcon 


		# NOTICE IF YOU ERROR
		# DISABLE import Datatable like this
		]
        
        )

		)

app(target=main)