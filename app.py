from flask import *
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/add")
def add():
    return render_template("add.html")


@app.route("/savedetails", methods=["POST", "GET"])
def saveDetails():
    msg = "msg"
    if request.method == "POST":
        try:
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            empresa= request.form["empresa"]
            with sqlite3.connect("employee.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into Employees (name, email,empresa, address) values (?,?,?,?)", (name, email, empresa, address))
                con.commit()
                msg = "Mensagem adicionada com Sucesso!"
        except:
            con.rollback()
            msg = "Mensagem não adicionada!"
        finally:
            return render_template("success.html", msg=msg)
            con.close()


@app.route("/view")
def view():
    con = sqlite3.connect("employee.db")
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute("select * from Employees")
    rows = cur.fetchall()
    return render_template("view.html", rows=rows)


@app.route("/delete")
def delete():
    return render_template("delete.html")


@app.route("/deleterecord", methods=["POST"])
def deleterecord():
    id = request.form["id"]
    with sqlite3.connect("employee.db") as con:
        try:
            cur = con.cursor()
            cur.execute("delete from Employees where id = ?", id)
            msg = "Comentário removido com Sucesso!"
        except:
            msg = "Não foi removido"
        finally:
            return render_template("delete_record.html", msg=msg)

@app.route("/update")
def update():
    return render_template("update.html")

@app.route("/updatedetails", methods=["POST"])
def updaterecord():
    msg = "msg"
    if request.method == "POST":
        try:
            id = request.form["id"]
            name = request.form["name"]
            email = request.form["email"]
            address = request.form["address"]
            with sqlite3.connect("employee.db") as con:
                cur = con.cursor()
                cur.execute("UPDATE Employees SET name=?, email=?, address=? WHERE id=?", (name, email, address, id))
                con.commit()
                msg = "comentário Atualizado"
        except:
            con.rollback()
            msg = "Não foi atualizado!"
        finally:
            return render_template("success.html", msg=msg)
            con.close()

if __name__ == "__main__":
    app.run(debug=True)