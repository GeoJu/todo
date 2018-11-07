from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from models import *
import os

app = Flask(__name__)

# db 설정
#app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql:///todo'  # plsql로 생성한 데이터 베이스 이름을 적는 다
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL')
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False
db.init_app(app)
migrate = Migrate(app,db)


@app.route('/')
def index():
    todos = Todo.query.order_by(Todo.deadline.asc()).all()
    return render_template('index.html', todos = todos)

@app.route('/posts/new')
def new():
    return render_template('new.html')


# @app.route('/posts/create', methods = ['post'])
# def creat():
#     # 사용자가 입력한 데이터 가져오기
#     #request.form['todo']       # todo라는 name 속성을 html파일에 생성해 줘야한다.
#     do = request.form.get('todo')
#     line = request.form.get('deadline')

#     # 가져온 데이터로 ToDo만들기
#     todo = Todo(todo=do, deadline=line)
    
#     # Todo Db에 저장하기
#     db.session.add(todo)
#     db.session.commit()
    
#     return redirect('/')
    
    
@app.route('/todos/create', methods = ['POST', 'GET'])
def todo():
    if request.method == 'POST':
        todo = Todo(request.form.get('todo'), request.form.get('deadline'))
        #데이터 저장 로직
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    return render_template('new.html')

# @app.route('/todos/<int:id>/update', methods = ['POST', 'GET'])
# def update(id):
#     todo = Todo.query.get('id')
#     request.args.get('id')



#삭제하는 경로를 라우트에 추가한다.
@app.route('/todos/<int:id>/delete')
def delete(id):
    #몇번글을 삭제할지 알아낸다.
    todo = Todo.query.get(id)
    #글을 삭제 한다.
    db.session.delete(todo)
    #상태를 저장한다.
    db.session.commit()
    #어디로 보낼지(url)설정한다.
    return redirect('/')



#EDIT 처리로직
# 기존의 데이터를 가져와서 수정할수 있는 폼 보여주기
@app.route('/todos/<int:id>/edit')
def edit(id):
    todo = Todo.query.get(id)
    
#    do = todo.todo
#    deadline = todo.deadline
    
    return render_template('edit.html', todo = todo)
    
    
    
#UPDATE 처리 로직
# 변경한 데이터를 가져와서 db에 반영
@app.route('/todos/<int:id>/update', methods=['POST'])
def update(id):
    todo = Todo.query.get(id)
    #do = request.form.get('todo')
    #line = request.form.get('deadline')
    
    todo.todo = request.form.get('todo')
    todo.deadline = request.form.get('deadline')
    
    #db.session.update(todo)
    db.session.commit()
    return redirect('/')
    
@app.route('/todos/<int:id>/upgrade', methods=['POST', 'GET'])
def upgrade(id):
    todo = Todo.query.get(id)
    
    if request.method == 'POST':
        
        todo.todo = request.form.get('todo')
        todo.deadline = request.form.get('deadline')
        db.session.commit()
        return redirect('/')
    #수정 할 수 있는 홈을 설정
    return render_template('edit.html', todo = todo)