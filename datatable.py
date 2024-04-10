from flet import *
import sqlite3
conn = sqlite3.connect('db/dbone.db',check_same_thread=False)

tb = DataTable(
	columns=[
		DataColumn(Text("Ação",size=20)),
		DataColumn(Text("Nome",size=20)),
		DataColumn(Text("Idade",size=20)),
		DataColumn(Text("Contato",size=20)),
		DataColumn(Text("email",size=20)),
		DataColumn(Text("Endereço",size=20)),
		DataColumn(Text("Gênero",size=20)),
	],
	rows=[]

	)


def showdelete(e):
	try:
		myid = int(e.control.data)
		c = conn.cursor()
		c.execute("DELETE FROM users WHERE id=?", (myid,))
		conn.commit()
		print("dados apagados")
		tb.rows.clear()	
		calldb()
		tb.update()

	except Exception as e:
		print(e)


id_edit = Text()
name_edit = TextField(label="nome")
age_edit = TextField(label="idade")
contact_edit = TextField(label="contato")
gender_edit = RadioGroup(content=Column([
		Radio(value="homem",label="homem"),
        Radio(value="mulher",label="mulher"),

	]))
email_edit = TextField(label="email")
address_edit = TextField(label="endereco")


def hidedlg(e):
	dlg.visible = False
	dlg.update()


def updateandsave(e):
	try:
		myid = id_edit.value
		c = conn.cursor()
		c.execute("UPDATE users SET nome=?, contato=?, idade=?, genero=?, email=?, endereco=? WHERE id=?", (name_edit.value, contact_edit.value, age_edit.value, gender_edit.value, email_edit.value, address_edit.value, myid))
		conn.commit()
		print("dados editados ")
		tb.rows.clear()	
		calldb()
		dlg.visible = False
		dlg.update()
		tb.update()
	except Exception as e:
		print(e)

dlg = Container(
	bgcolor="orange200",
	padding=10,
			content=Column([
				Row([
				Text("Editar Dados",size=30,weight="bold", color=colors.RED),
				IconButton(icon="close",on_click=hidedlg),
					],alignment="spaceBetween"),
				name_edit,
				age_edit,
				contact_edit,
				Text("Select Gender",size=20,weight="bold"),
				gender_edit,
				email_edit,
				address_edit,
				ElevatedButton("Atualizar",on_click=updateandsave,tooltip="Atualizar")

				])
)




def showedit(e):
	data_edit = e.control.data
	id_edit.value = data_edit['id']
	name_edit.value = data_edit['nome']
	age_edit.value = data_edit['idade']
	contact_edit.value = data_edit['contato']
	gender_edit.value = data_edit['genero']
	email_edit.value = data_edit['email']
	address_edit.value = data_edit['endereco']

	dlg.visible = True
	dlg.update()


def calldb():
	c = conn.cursor()
	c.execute("SELECT * FROM users")
	users = c.fetchall()
	print(users)
	if not users == "":
		keys = ['id', 'nome', 'contato', 'idade', 'genero', 'email', 'endereco']
		result = [dict(zip(keys, values)) for values in users]
		for x in result:
			tb.rows.append(
				DataRow(
                    cells=[
                        DataCell(Row([
                        	IconButton(icon="create",icon_color="blue",
                        		data=x,
                        		on_click=showedit,
                                tooltip="Editar"

                        		),
                        	IconButton(icon="delete", icon_color="red",
                        		data=x['id'],
                        	on_click=showdelete,
                            tooltip="Apagar"

                        		),
                        	])),
                        DataCell(Text(x['nome'])),
                        DataCell(Text(x['idade'])),
                        DataCell(Text(x['contato'])),
                        DataCell(Text(x['email'])),
                        DataCell(Text(x['endereco'])),
                        DataCell(Text(x['genero'])),
                    ],
                ),

		)


calldb()

def buscar(e):
    nome = e.control.data
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE nome=? ORDER BY asc",nome)
    users = c.fetchall()
    print(users)
    if not users == "":
       keys = ['id', 'nome', 'contato', 'idade', 'genero', 'email', 'endereco']
       result = [dict(zip(keys, values)) for values in users]
       for x in result:
        tb.rows.append(
				DataRow(
                    cells=[
                        DataCell(Row([
                        	IconButton(icon="create",icon_color="blue",
                        		data=x,
                        		on_click=showedit,
                                tooltip="Editar"

                        		),
                        	IconButton(icon="delete", icon_color="red",
                        		data=x['id'],
                        	on_click=showdelete,
                            tooltip="Apagar"

                        		),
                        	])),
                        DataCell(Text(x['nome'])),
                        DataCell(Text(x['idade'])),
                        DataCell(Text(x['contato'])),
                        DataCell(Text(x['email'])),
                        DataCell(Text(x['endereco'])),
                        DataCell(Text(x['genero'])),
                    ],
                ),

		)

buscar()

dlg.visible = False
mytable = Column([
	dlg,
	Row([tb],scroll="always")
	])