from flask import Flask, request, render_template, jsonify, redirect, session, url_for
import os, uuid, datetime, random

from db import AccountsDatabase, ProjectsDatabase

app = Flask(__name__)

UPLOAD_FOLDER = 'static/pic/user/icon'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = str(uuid.uuid4())
app.permanent_session_lifetime = datetime.timedelta(days=31)

@app.route('/')
@app.route('/main')
def main():
    if 'Login' not in session or not session['Login']:
        return redirect(url_for("authorization"))
    return render_template('main.html')

@app.route('/profile')
def prof():    
    if 'Login' not in session or not session['Login']:
        return redirect(url_for("authorization"))
    return render_template('profile.html')

@app.route('/fil')
def fil():    
    if 'Login' not in session or not session['Login']:
        return redirect(url_for("authorization"))
    return render_template('filter.html')

@app.route('/startup')
def startup():    
    if 'Login' not in session or not session['Login']:
        return redirect(url_for("authorization"))
    return render_template('startup.html')

@app.route('/register')
def autoriz():
    return render_template('index.html')

@app.route('/reg', methods=['POST'])
def reg():
    data = AccountsDatabase()
    return data.register_user({'login': request.json['login'], 'password': request.json['password-1']})
    
@app.route('/authorization')
def authorization():
    session.permanent = True
    if 'Login' not in session:
        session['Login'] = ''
        session['Startups'] = []
        session['Icon'] = ''
        session['Description_prof'] = ''
        session['Contacts'] = ''
        session['Id_proj'] = ''
        session.modified = True
    return render_template('autorization.html')

@app.route('/log', methods=['POST'])
def log():
    if 'Login' not in session:
        return 'Не не не'
    if request.method == 'POST':
        login = request.json['login']
        password = request.json['password']

        data = AccountsDatabase()
        resp = data.authenticate_user({'login': login, 'password': password})
        
        if resp['status'] == 200:
            session.permanent = True
            session['Login'] = login
            session['Icon'] = resp['icon']
            session['Description_prof'] = resp['description_profile']
            session['Contacts'] = resp['contacts']
            session.modified = True
            return jsonify({'status': 200, 'message': 'Успешная авторизация'})
        return jsonify({'status': 403, 'message': 'Ошибка при авторизации'})

@app.route('/main_ps', methods=['POST'])
def main_ps():
    if request.json['index_action'] == 1:
        try:
            if 'Login' not in session or session['Login'] == '':
                login = ''
            else:
                login = session['Login']
        except:
            login = ''
        
        data = {
            'index_action': 0,
            'status': 0,
            'project_ids': {},
            'message': '',
            'login': login,
            'icon': '',
            'name_project': '',
            'startups': {
            }
        }

        datab = ProjectsDatabase()
        print(datab.get_next_five_projects(data))
        return datab.get_next_five_projects(data)

@app.route('/like_ps', methods=['POST'])
def like_ps():
    if 'Login' not in session or session['Login'] == '':
        return {
            'status': 0,
            'message': 'Вы не авторизованы'
        }
    print(1, request.json)
    if request.json['index_action'] == 1:
        name_project = request.json['content']['name']
        
        data = {
            'login': session['Login'], 
            'project_name': name_project
        }        
        
        datab = ProjectsDatabase()
        
        return datab.like_project(data)
    
@app.route('/fil_ps', methods=['POST'])
def fil_ps():
    if request.json['index_action'] == 1:
        # print(1, request.json)
        index_action = request.json['filter']['selected']
        name_project = request.json['filter']['input']
        count = request.json['posts']
        login = session['Login']
        data = {
            'index_action': int(index_action),
            'name_project': name_project,
            'project_ids': count,
            'status': 0,
            'message': '',
            'login': login,
            'icon': session['Icon'],
            'startups': {
            }
        }
        
        datab = ProjectsDatabase()

        return datab.get_next_five_projects(data)

@app.route('/card=<int:id_pr>')
def card(id_pr):
    if 'Login' not in session or session['Login'] == '':
        return {
        'status': 0,
        'message': 'Вы не авторизованы'
    }
    
    session.permanent = True
    session['Id_proj'] = id_pr
    session.modified = True
    
    return render_template('card.html')

@app.route('/card_ps', methods=['POST'])
def card_ps():
    # print(request.json)
    if request.json['index_action'] == 1:
        id_pr = session['Id_proj']
        
        data = {
            'status': 0,
            'message': '',
            'name_project': '',
            'description': '',
            'contacts': '',
            'login': session['Login'],
            'icon': session['Icon']
        }
        
        datab = ProjectsDatabase()
        return datab.getprojectdata(data, id_pr)

@app.route('/profile_ps', methods=['POST'])
def profile_ps():
    if 'Login' not in session or session['Login'] == '':
        return {
        'status': 0,
        'message': 'Вы не авторизованы'
    }
    
    qury = request.json
    print(qury)
    if qury['index_action'] == 1:
        data = {
            'status': 200,
            'message': 'Всё гуд',
            'icon': session['Icon'],
            'description_profile': session['Description_prof'],
            'contacts': session['Contacts'],
            'login': session['Login'],
            'startups': {
            }
        }
        
        datab = AccountsDatabase()
        
        return datab.get_account_projects(data)
        
    
    elif qury['index_action'] == 2:
        descr = qury['description_profile']
        cont = qury['contacts']
        
        data = {
            'status': 0,
            'message': '',
            'login': session['Login'],
            'description_profile': descr,
            'contacts': cont
        }
        
        datab = AccountsDatabase()
        
        datab.edit_user_description_contacts(data)
        
        session.permanent = True
        session['Description_prof'] = descr
        session['Contacts'] = cont
        session.modified = True
        
        return {
            'status': 200,
            'message': 'Всё гуд'
        }
        
    elif qury['index_action'] == 3:
        id_proj = int(qury['id_proj'])
        
        datab = AccountsDatabase()

        datab.delete_project(id_proj, session['Login'])
        
        return {
            'status': 200,
            'message': 'Всё гуд',
            'id': id_proj
        }
    
    else:
        return 'Не не не'
    
@app.route('/icon_ps', methods=['POST'])
def icon_ps():
    if 'file' not in request.files:
            return jsonify({
            'status': 0,
            'message': 'Ошибка запроса'
        })
    
    file = request.files['file']
    
    file.save(os.path.join(UPLOAD_FOLDER, file.filename))
    session.permanent = True
    session['Icon'] = f'static/pic/user/icon/{file.filename}'
    session.modified = True
    
    datab = AccountsDatabase()
    
    datab.upload_user_avatar(session['Login'], file.filename)
    
    return {
        'status': 200,
        'message': 'Всё гуд',
        'icon': session['Icon']
    }

@app.route('/startup_ps', methods=['POST'])
def startup_ps():
    if 'Login' not in session or session['Login'] == '':
            return {
        'status': 0,
        'message': 'Вы не авторизованы'
    }
        
    qury = request.json
    print(qury)
    
    data = {
        'status': 0,
        'message': '',
        'name_project': qury[0]['value'],
        'description': qury[2]['value'],
        'login': session['Login']
    }
    
    datab = ProjectsDatabase()
    
    return datab.upload_project(data)

if __name__ == '__main__':
    app.run(debug=True)
    