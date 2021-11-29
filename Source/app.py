import sqlite3
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

# Создаем соединение с нашей базой данных    SQLITE tyt podkluchaem
conn = sqlite3.connect('tablo.db', check_same_thread=False)
# Создаем курсор - это специальный объект который делает запросы и получает их результаты
cursor = conn.cursor()

# sozdanie obekta, name = app.py
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tablo.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
tablo = create_engine('sqlite:///tablo.db', echo=True)

# Создание таблици если еще нету
cursor.execute("""CREATE TABLE IF NOT EXISTS Result (
    id INTEGER,
    nomer INTEGER,
    name TEXT,
    team TEXT,
    cold INTEGER,
    hot INTEGER,
    sum INTEGER,
    wincold INTEGER,
    winsum INTEGER
)""")

conn.commit()


# class Total() структура бази даних
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nomer = db.Column(db.Integer, nullable=True)
    name = db.Column(db.String(200), nullable=False)
    team = db.Column(db.String(200), nullable=False)
    cold = db.Column(db.Integer)
    hot = db.Column(db.Integer)
    sum = db.Column(db.Integer)
    wincold = db.Column(db.Integer)
    winsum = db.Column(db.Integer)

    def __repr__(self):
        return '<Result %r>' % self.id


# nayti agentov s naybolshim totalom
winsumz = 0


def topsum():
    # stavim vse wincold na 0:
    cursor.execute("UPDATE Result SET winsum = 0 WHERE winsum = 1")

    # stavim znacheznnya winsum = 1 de top :
    cursor.execute("UPDATE Result SET winsum = 1 WHERE sum = (SELECT MAX(sum) FROM result)")
    cursor.execute("SELECT winsum FROM Result WHERE sum = (SELECT MAX(sum) FROM result)")
    (winsumz,) = cursor.fetchone()
    conn.commit()
    return winsumz


# nayti agentov s naybolshim totalom cold
wincoldz = 0


def topcold():
    cursor.execute("SELECT SUM(cold) FROM Result ")
    sumacoldov = cursor.fetchone()
    if sumacoldov == (0,):
        print("netu koldov, ne zapolnyat wincold", sumacoldov)
        return viborkaGA
    else:
        # stavim vse wincold na 0:
        cursor.execute("UPDATE Result SET wincold = 0 WHERE wincold = 1")

        # stavim znacheznnya wincold = 1 de top wincold:
        cursor.execute("UPDATE Result SET wincold = 1 WHERE cold = (SELECT MAX(cold) FROM result)")
        cursor.execute("SELECT wincold FROM Result WHERE cold = (SELECT MAX(cold) FROM result)")
        (wincoldz,) = cursor.fetchone()
        conn.commit()
        return wincoldz


# popitka vivesti sumu (hot, cold) po timam
# obyavlyaem peremennie spiski
viborkaEA = []
viborkaPA = []
viborkaGA = []
viborkaAll = []


# esli est dannie vibiraem otdelno cold, hot i sum
def Eteam(viborkaEA):
    cursor.execute("SELECT SUM(sum) FROM Result WHERE team = 'ENG'")
    viborkaEA = cursor.fetchone()
    if viborkaEA == (None,):
        print("Spisok ENG: netu danih", viborkaEA)
        return viborkaEA
    else:
        viborkaEA = []
        cursor.execute("SELECT SUM(cold) FROM Result WHERE team = 'ENG'")
        engcold = cursor.fetchone()[0]
        viborkaEA.insert(0, engcold)
        cursor.execute("SELECT SUM(hot) FROM Result WHERE team = 'ENG'")
        enghot = cursor.fetchone()[0]
        viborkaEA.insert(1, enghot)
        viborkaEA.insert(2, (engcold + enghot))
        print("Spisok ENG: ", viborkaEA)
        return viborkaEA


# esli est dannie vibiraem otdelno cold, hot i sum
def Gteam(viborkaGA):
    cursor.execute("SELECT SUM(sum) FROM Result WHERE team = 'GER'")
    viborkaGA = cursor.fetchone()
    if viborkaGA == (None,):
        print("Spisok GER: netu danih", viborkaGA)
        return viborkaGA
    else:
        viborkaGA = []
        cursor.execute("SELECT SUM(cold) FROM Result WHERE team = 'GER'")
        gercold = cursor.fetchone()[0]
        viborkaGA.insert(0, gercold)
        cursor.execute("SELECT SUM(hot) FROM Result WHERE team = 'GER'")
        gerhot = cursor.fetchone()[0]
        viborkaGA.insert(1, gerhot)
        viborkaGA.insert(2, (gercold + gerhot))
        print("Spisok GER: ", viborkaGA)
        return viborkaGA


# esli est dannie vibiraem otdelno cold, hot i sum
def Pteam(viborkaPA):
    cursor.execute("SELECT SUM(sum) FROM Result WHERE team = 'POL'")
    viborkaPA = cursor.fetchone()
    if viborkaPA == (None,):
        print("Spisok POL: netu danih")
        return viborkaPA
    else:
        viborkaPA = []
        cursor.execute("SELECT SUM(cold) FROM Result WHERE team = 'POL'")
        polcold = cursor.fetchone()[0]
        viborkaPA.insert(0, polcold)
        cursor.execute("SELECT SUM(hot) FROM Result WHERE team = 'POL'")
        polhot = cursor.fetchone()[0]
        viborkaPA.insert(1, polhot)
        viborkaPA.insert(2, (polcold + polhot))
        print("Spisok POL: ", viborkaPA)
        return viborkaPA


# esli est dannie vibiraem otdelno cold, hot i sum dlya vseh team
def SumaTeam(viborkaAll):
    cursor.execute("SELECT SUM(sum) FROM Result")
    viborkaAll = cursor.fetchone()
    if viborkaAll == (None,):
        print("Spisok po timam: netu danih", viborkaAll)
        return viborkaPA
    else:
        viborkaAll = []
        cursor.execute("SELECT SUM(cold) FROM Result")
        allcold = cursor.fetchone()[0]
        viborkaAll.insert(0, allcold)
        cursor.execute("SELECT SUM(hot) FROM Result")
        allhot = cursor.fetchone()[0]
        viborkaAll.insert(1, allhot)
        viborkaAll.insert(2, (allcold + allhot))
        print("Spisok po timam: ", viborkaAll)
        return viborkaAll


# основной путь / и соответствующий ему обработчик запросов:
@app.route("/")
@app.route('/index')
@app.route("/home")
def main():
    return render_template('index.html')


@app.route("/about")
def about():
    cursor.execute("SELECT SUM(sum) FROM Result")
    viborka = cursor.fetchone()
    if viborka == (None,):
        pass
    else:
        topsum()
        topcold()

    result = Result.query.order_by(Result.sum.desc(), Result.cold.desc()).all()
    print("Vot: ", result)
    return render_template('about.html', result=result, viborkaAll=SumaTeam(viborkaAll), viborkaEA=Eteam(viborkaEA),
                           viborkaGA=Gteam(viborkaGA), viborkaPA=Pteam(viborkaPA))


@app.route("/add", methods=['POST', 'GET'])  # dobavlenie agentov
def add():
    if request.method == 'POST':
        id = request.form['nomer']
        nomer = id
        name = request.form['name']
        cold = request.form['cold']
        hot = request.form['hot']
        team = request.form['team']
        sum = int(hot) + int(cold)
        wincold = 0
        winsum = 0

        cursor.execute(f"SELECT nomer FROM Result WHERE nomer ='{nomer}'")
        if cursor.fetchone() is None:
            print("Takoy agent esche nety")
            print("Peredano v bazy: ", id, nomer, name, hot, cold, team, sum)
            try:
                cursor.execute(f"INSERT INTO Result VALUES (?,?,?,?,?,?,?,?,?)",
                               (id, nomer, name, team, cold, hot, sum, wincold, winsum))
                conn.commit()
                return redirect('/about')
            except:
                return "ERROR oshibka sozdaniya!!!"
        else:
            print("Takoy agent uzhe est!")
            return redirect('/edit')
    else:
        print("Otkril add")
        result = Result.query.order_by(Result.sum.desc()).all()
        pass
        return render_template('add.html', result=result, viborkaAll=SumaTeam(viborkaAll))


@app.route("/del", methods=['POST', 'GET'])  # udalenie agentov
def udalit():
    result = Result.query.order_by(Result.nomer.asc()).all()
    if request.method == 'POST':  # ne RABOTAET suka normalno
        id = request.form['nomer']
        print("Poluchil nomer :", id)
        result = Result.query.get(id)
        try:
            with conn:
                cursor.execute("SELECT * FROM Result WHERE id = 'result'")
                db.session.delete(result)
                db.session.commit()
                print("Udalil nomer :", id)
                return redirect('/about')
        except:
            pass
            return "ERROR pri udalenii!!!"
    else:
        print("Otkril del")
        pass
        return render_template('del.html', result=result, viborkaAll=SumaTeam(viborkaAll))


@app.route("/del/vse")
def delvle():
    cursor.execute("DELETE FROM Result")
    conn.commit()
    return render_template('about.html')


@app.route("/edit", methods=['POST', 'GET'])  # redaktirovanie obektov
def edit():
    if request.method == 'POST':  # ne RABOTAET suka normalno
        if int(request.form.get('hot')) < 0:
            print("Oshibka vvoda hot!")
            return redirect('/edit')
        elif int(request.form.get('cold')) < 0:
            print("Oshibka vvoda cold!")
            return redirect('/edit')
        else:
            id = request.form['no_user']
            print(id)
            result = Result.query.get(id)
            print("Vzyato s bazi: ", id, result.nomer, result.name, result.hot, result.cold, result.team, result.sum)

            result = Result.query.get(id)
            result.hot = int(request.form.get('hot'))
            result.cold = int(request.form.get('cold'))
            result.sum = int(result.hot) + int(result.cold)
            db.session.commit()
            print("Peredano v bazy: ", id, result.hot, result.cold, result.sum)
            try:
                return redirect('/about')
            except:
                return "ERROR, ne vernie dannie!!!"
    else:
        result = Result.query.order_by(Result.nomer.asc()).all()
        print("Otkril edit")
        pass
        return render_template('edit.html', result=result, viborkaAll=SumaTeam(viborkaAll))


# является ли etot файл главной программой и запустите приложение:
if __name__ == "__main__":
    app.run(debug=True)  # zapuskaet lokalniy server i debazhet

# закрыть соединение с базой данных
conn.close()

# шоб прога не закрилася в консолі
input("Press Enter")
