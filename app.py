from classes import mg
from flask import Flask,render_template,request, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_alembic import Alembic

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///baza.db'
db = SQLAlchemy(app)


class Action(db.Model):
    pk = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(15),nullable=False,unique=False)
    kwota = db.Column(db.Integer, nullable=True, unique=False)
    comment = db.Column(db.String(30), nullable=True, unique=False)
    product = db.Column(db.String(30), nullable=True, unique=False)
    price = db.Column(db.Integer, nullable=True, unique=False)
    qty = db.Column(db.Integer, nullable=True, unique=False)
    saldo = db.Column(db.Integer, nullable=False, unique=False)

db.create_all()

def update_manager():
    actions=db.session.query(Action).all()
    for action in actions:
        if action.action =="saldo":
            params=[action.kwota,action.comment]
        else:
            params=[action.product,action.price,action.qty]
        mg.commands.append((action.action,params))

update_manager()
mg.execute()

@app.route("/", methods=["get","post"])
def index():
    saldo = mg.saldo
    products = mg.magazyn

    product_list =[]
    for product in products:
        product_list.append((product,products[product]))
    return render_template("index.html", saldo=saldo ,products=product_list)

@app.route("/resp/", methods=["post","get"])
def resp():
    resp_dict=dict(request.form)
    wplata= resp_dict["wplata"]
    komentarz = resp_dict["komentarz"]
    params=[wplata,komentarz]
    mg.callbacks[resp_dict["action"]](params)
    saldo = mg.saldo
    products = mg.magazyn
    product_list = []
    for product in products:
        product_list.append((product, products[product]))
    command_resp = []
    for i in resp_dict.values():
        command_resp.append(i)
    mg.commands.append((command_resp[0], command_resp[1:]))
    saldo_inpout = Action(action="saldo", kwota=wplata, comment=komentarz,saldo=mg.saldo)
    db.session.add(saldo_inpout)
    db.session.commit()
    return render_template("index.html", saldo=saldo, products=product_list)


@app.route("/resp1/", methods=["post","get"])
def resp1():
    resp_dict=dict(request.form)
    nazwa = resp_dict["nazwa_produktu"]
    cena = resp_dict["cena"]
    ilosc = resp_dict["ilosc"]
    params=[nazwa,cena,ilosc]
    mg.callbacks[resp_dict["action1"]](params)
    saldo = mg.saldo
    products = mg.magazyn
    product_list = []
    for product in products:
        product_list.append((product, products[product]))
    command_resp = []
    for i in resp_dict.values():
        command_resp.append(i)
    mg.commands.append((command_resp[0], command_resp[1:]))
    kupno_input = Action(action="kupno",product=nazwa,price=cena,qty=ilosc,saldo=mg.saldo)
    db.session.add(kupno_input)
    db.session.commit()
    return render_template("index.html", saldo=saldo,products=product_list)

@app.route("/resp2/", methods=["post","get"])
def resp2():
    resp_dict=dict(request.form)
    nazwa = resp_dict["nazwa_produktu"]
    cena = resp_dict["cena"]
    ilosc = resp_dict["ilosc"]
    params=[nazwa,cena,ilosc]
    mg.callbacks[resp_dict["action2"]](params)
    saldo = mg.saldo
    products = mg.magazyn
    product_list = []
    for product in products:
        product_list.append((product, products[product]))
    command_resp=[]
    for i in resp_dict.values():
        command_resp.append(i)
    mg.commands.append((command_resp[0],command_resp[1:]))
    kupno_input = Action(action="sprzedaz", product=nazwa, price=cena, qty=ilosc, saldo=mg.saldo)
    db.session.add(kupno_input)
    db.session.commit()

    return render_template("index.html", saldo=saldo, products=product_list)

@app.route("/resp3/",methods=["get","post"])
def resp3():
    resp_dict = dict(request.form)
    od = int(resp_dict["od"])
    do = int(resp_dict["do"])
    historia = mg.commands
    historia_list = []
    for transakcja in historia:
        historia_list.append(transakcja)
    if od and do == " ":
        historia_list=historia_list
    else:
        historia_list=historia_list[od:do]
    return render_template("historia.html" ,historia=historia_list,od=od,do=do)

alembic = Alembic()
alembic.init_app(app)
