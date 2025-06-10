from flask import Blueprint, render_template, request, flash

createfile = Blueprint('createfile', __name__, static_folder='static', template_folder='templates')

@createfile.route('/create', methods=['POST','GET'])
@createfile.route('/', methods=['POST','GET'])
def create():
    if request.method == 'POST':
        create_file(request.form['filename'])
        flash('File has been created', 'info')
    return render_template('create.html')

def create_file(filename):
    with open(f'{filename}.txt', 'w') as file:
        file.write('hello')