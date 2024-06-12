from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from supabase import create_client

app = Flask(__name__)

app.secret_key = 'daddy1810'

supabase_url = 'https://rprpfogbzweynochfbwk.supabase.co/'
supabase_key = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJwcnBmb2diendleW5vY2hmYndrIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDUyMjE5MzMsImV4cCI6MjAyMDc5NzkzM30.guuLDU-xv6Heoe9cjwtnL1eBAZbDupB5nFcfn0vko8U'
pranav = create_client(supabase_url, supabase_key)

curr_user = ''

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about_us')
def about_us():
    return render_template('about_us.html')

@app.route('/login')
def show_login():
    return render_template('login.html')

@app.route('/logout')
def logout():
    return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    global curr_user
    email = request.form['email']
    password = request.form['password']

    response = pranav.auth.sign_in_with_password({'email':email, 'password':password})

    if 'error' not in response:
        curr_user = email
        return redirect(url_for('lists'))  
    else:
        flash('Wrong passwords')
        return redirect(url_for('show_login'))  
    
@app.route('/signup')
def show_signup():
    return render_template('signup.html')

@app.route('/confirm')
def confirm():
    return render_template('confirm.html')


@app.route('/signup', methods=['POST'])
def signup():
    email = request.form['email']
    password = request.form['password']

    response = pranav.auth.sign_up({'email':email, 'password':password})

    if 'error' not in response:
        flash('Confirm mail!')
        return redirect(url_for('confirm'))
    else:
        flash('Error')

@app.route('/home')
def lists():
    return render_template('home.html', curr_user=curr_user)

@app.route('/todo')
def todo():
    return render_template('todo.html')

@app.route('/guest_login')
def guest_login():
    return render_template('guest.html')

@app.route('/guest')
def guest():
    global curr_user
    curr_user = 'GUEST'
    return render_template('home.html')

@app.route('/random')
def random():
    return render_template('random.html')

@app.route('/venture')
def venture():
    return render_template('venture.html')

@app.route('/add_task', methods=['POST'])
def add_task():
    if request.method == 'POST':
        task = request.form['task']
        description = request.form['description']
        deadline = request.form['deadline']

        response = pranav.table('todo').insert([{'task': task, 'description': description, 'deadline': deadline, 'email':curr_user}]).execute()
        if 'error' not in response:
            flash('Task added successfully!')
            return redirect(url_for('todo')) 
        else:
            flash('Error adding task')
    
@app.route('/add_thought', methods=['POST', 'GET'])
def add_thought():
    if request.method == 'POST':
        task = request.form['why']
        description = request.form['what']
        deadline = request.form['when']

        response = pranav.table('random').insert([{'why': task, 'what': description, 'when': deadline, 'email' : curr_user}]).execute()
        if 'error' not in response:
            flash('Thought added successfully!')
            return redirect(url_for('random')) 
        else:
            flash('Error adding task')

@app.route('/add_idea', methods=['POST'])
def add_idea():
    if request.method == 'POST':
        domain = request.form['domain']
        title = request.form['title']
        ideas = request.form['ideas']
        requirements = request.form['requirements']
        description = request.form['description']
        how = request.form['how']

        response = pranav.table('venture').insert({'domain': domain, 'title': title, 'ideas': ideas, 'requirements':requirements, 'description':description, 'how':how, 'email' : curr_user}).execute()
        if 'error' not in response:
            flash('Task added successfully!')
            return redirect(url_for('venture')) 
        else:
            flash('Error adding task')

@app.route('/display_tasks', methods = ['GET'])
def display_tasks():
    tasks = []
    descs = []
    dls = []
    resp = pranav.table('todo').select('*').execute().data
    for x in resp:
        if x['email'] == curr_user:
            tasks.append(x['task'])
            descs.append(x['description'])
            dls.append(x['deadline'])
    data_arr = [tasks, descs, dls]
    return render_template('todoList.html', data_arr=data_arr)

@app.route('/display_thoughts', methods = ['GET'])
def display_thoughts():
    whats = []
    whys = []
    whens = []
    resp = pranav.table('random').select('*').execute().data
    for x in resp:
        if x['email'] == curr_user:
            whats.append(x['what'])
            whys.append(x['why'])
            whens.append(x['when'])
    data_arr = [whats, whys, whens]
    return render_template('randomList.html', data_arr=data_arr)

@app.route('/display_ideas', methods = ['GET'])
def display_ideas():
    domains = []
    titles = []
    ideases = []
    reqs = []
    descs = []
    hows = []
    resp = pranav.table('venture').select('*').execute().data
    for x in resp:
        if x['email'] == curr_user:
            domains.append(x['domain'])
            titles.append(x['title'])
            ideases.append(x['ideas'])
            reqs.append(x['requirements'])
            descs.append(x['description'])
            hows.append(x['how'])
    data_arr = [titles, domains, ideases, reqs, descs, hows]
    return render_template('ventureList.html', data_arr=data_arr)

@app.route('/selected_tasks', methods=['POST', 'GET', 'DELETE'])
def selected_tasks():
    tasks = request.form.getlist('selectedTasks')
    for task in tasks:
        resp = pranav.table('todo').delete().eq('task', task).execute()
    if 'error' not in resp:
        return redirect(url_for('display_tasks')) 
    
@app.route('/selected_thoughts', methods=['POST', 'GET', 'DELETE'])
def selected_thoughts():
    thoughts = request.form.getlist('selectedThoughts')
    for thought in thoughts:
        print(thought)
        resp = pranav.table('random').delete().eq('what', thought).execute()
    if 'error' not in resp:
        return redirect(url_for('display_thoughts')) 
    
@app.route('/selected_ideas', methods=['POST', 'GET', 'DELETE'])
def selected_ideas():
    ideas = request.form.getlist('selectedIdeas')
    for idea in ideas:
        resp = pranav.table('venture').delete().eq('title', idea).execute()
    if 'error' not in resp:
        #return 'sucess'
        return redirect(url_for('display_ideas'))

if __name__ == '__main__':
    app.run(debug=True)

