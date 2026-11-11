import sqlite3
from flask import Flask, render_template, request, redirect, url_for

#===========================Conectar ao banco===========================
app = Flask(__name__)
def conectar_banco():
    conexao = sqlite3.connect("banco_itens/banco_de_dados.db")
    conexao.row_factory = sqlite3.Row
    return conexao

#===========================Tela inicial===========================
@app.route("/")
def index():
    conexao = conectar_banco()

    itens = conexao.execute(
        "SELECT * FROM Itens ORDER BY ID ASC"
    ).fetchall()

    conexao.close()

    return render_template("index.html", itens=itens)

#===========================Filtro===========================
@app.route("/", methods=['POST'])
def btw_filtrar():
    if request.method == "POST":
        id_item = request.form.get("id_item", "").strip()
        nome = request.form.get("nome", "").strip()
        descricao = request.form.get("descricao", "").strip()
        data = request.form.get("data", "").strip()
        local = request.form.get("local", "").strip()
        situacao = request.form.get("situacao", "")

        conexao = conectar_banco()

        filtro = "SELECT * FROM Itens WHERE 1=1"

        parametros = []

        if id_item != "":
            filtro += " AND ID = ?"
            parametros.append(id_item)

        if nome != "":
            filtro += " AND Nome LIKE ?"
            parametros.append(f"%{nome}%")

        if descricao != "":
            filtro += ' AND "Descrição" LIKE ?'
            parametros.append(f"%{descricao}%")

        if data != "":
            filtro += " AND Data LIKE ?"
            parametros.append(f"%{data}%")

        if local != "":
            filtro += " AND Local LIKE ?"
            parametros.append(f"%{local}%")

        if situacao:
            filtro += ' AND "Situação" = ?'
            parametros.append(situacao)

        filtro += " ORDER BY ID ASC"

        conexao = conectar_banco()

        itens = conexao.execute(
            filtro, parametros
        ).fetchall()

        conexao.close()

        return render_template("index.html", itens=itens)

    return redirect(url_for("index"))

#===========================Menu===========================
@app.route("/senac/<pagina>")
def menu(pagina):
    if pagina == 'cadastro':
        return render_template("cadastro.html")
    elif pagina == 'achados_e_perdidos':
        return redirect(url_for("index"))
    elif pagina == "editar":
        return render_template("editar.html")

#===========================Cadastrar Item===========================
@app.route("/cadastrar", methods=['GET', 'POST'])
def btw_cadastrar():
    if request.method == "POST":
        # Recebe os dados do formulário
        nome = request.form["nome"].strip()
        descricao = request.form["descricao"].strip()
        data = request.form.get("data").strip() or None
        local = request.form["local"].strip()
        situacao = request.form["situacao"]

        conexao = conectar_banco()

        conexao.execute("""
            INSERT INTO Itens
                (Nome, Descrição, Data, Local, Situação)
            VALUES (?, ?, COALESCE(?, CURRENT_DATE), ?, ?)
        """, (nome, descricao, data, local, situacao))

        conexao.commit()
        conexao.close()

        return redirect(url_for("index"))

    return render_template("cadastro.html")

#===========================Editar Item===========================
@app.route("/atualizar//<int:id_item>", methods=['POST'])
def btw_atualizar(id_item):
    if request.method == "POST":
        #id_item = request.form.get("id_item", "").strip()
        nome = request.form.get("nome", "").strip()
        descricao = request.form.get("descricao", "").strip()
        data = request.form.get("data", "").strip()
        local = request.form.get("local", "").strip()
        situacao = request.form.get("situacao", "")

        conexao = conectar_banco()

        editar = "UPDATE Itens SET "

        dados = []
        parametros = []

        #if id_item != "":
        #    dados.append(" ID = ?")
        #    parametros.append(id_item)

        if nome != "":
            dados.append(" Nome = ?")
            parametros.append(nome)

        if descricao != "":
            dados.append(' "Descrição" = ?')
            parametros.append(descricao)

        if data != "":
            dados.append(" Data = ?")
            parametros.append(data)

        if local != "":
            dados.append(" Local = ?")
            parametros.append(local)

        if situacao:
            dados.append(' "Situação" = ?')
            parametros.append(situacao)

        parametros.append(id_item)
        editar = "UPDATE Itens SET " + ", ".join(dados)
        editar += " WHERE ID = ?"

        conexao = conectar_banco()
        conexao.execute(editar, parametros)
        conexao.commit()
        conexao.close()

        return redirect(url_for("index"))

#===========================Deletar Item===========================
@app.route("/excluir/<int:id_item>", methods=["POST"])
def btw_excluir(id_item):

    conexao = conectar_banco()

    conexao.execute(
        "DELETE FROM Itens WHERE ID = ?",
        (id_item,)
    )

    conexao.commit()
    conexao.close()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)