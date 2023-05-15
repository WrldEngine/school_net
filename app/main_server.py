from flask import Flask
from flask import redirect, render_template, url_for
from flask import request, session, make_response
from flask import flash, Blueprint

from .models import db, Students, Teachers, Tasks, SendAns

disp = Blueprint('main_server', __name__, template_folder='templates')

@disp.route('/')
def main_pg():
    if 'name' in session:
        get_data = Students.query.all()
        get_teacher = Teachers.query.all()
        user_name = session['name']

        return render_template('index.html', get_data=get_data, teachers=get_teacher, user=user_name)
        
    return redirect('/reg_student')

@disp.route('/teacher/<username>')
def select_teacher(username):
    isTeacher = session['name'] == username

    get_teacher = Teachers.query.filter_by(username=username).first()
    get_tasks = Tasks.query.filter(Tasks.teacher == username).all()

    return render_template('teach_cab.html', get_tasks=get_tasks, get_teacher=get_teacher, isTeacher=isTeacher)

@disp.route('/student/<username>')
def select_student(username):
    isAuthorAccount = session['name'] == username

    get_student = Students.query.filter_by(username=username).first()
    get_stud_ans = SendAns.query.filter(SendAns.from_author == username).all()

    return render_template('student.html', student=get_student, is_author=isAuthorAccount, stud_ans=get_stud_ans)

@disp.route('/reg_student', methods=['POST', 'GET'])
def reg_stud():
    if request.method == 'POST':
        full_name = request.form['name']
        user_name = request.form['username']
        password = request.form['password']
        grade = request.form['grade']

        grade_sym_low = request.form['grade_sym']
        grade_symbol = grade_sym_low.upper()

        std_usname_ex = Students.query.filter(Students.username == user_name).all()
        tch_usname_ex = Teachers.query.filter(Teachers.username == user_name).all()

        if not std_usname_ex and not tch_usname_ex:
            save_stud = Students(
                            name=full_name,
                            username=user_name,
                            grade=grade,
                            grade_symbol=grade_symbol,
                            password=password
                        )
            try:
                db.session.add(save_stud)
                db.session.commit()

                session['name'] = user_name
                return redirect('/')
            except:
                return '404'
        else:
            us_ex_err = 'Это имя пользователся уже существует'
            return render_template('reg_stud.html', err=us_ex_err)

    return render_template('reg_stud.html')

@disp.route('/reg_teacher', methods=['POST', 'GET'])
def reg_teach():
    if request.method == 'POST':
        full_name = request.form['name']
        user_name = request.form['username']
        password = request.form['password']

        subject = request.form.getlist('options')[0]

        std_usname_ex = Students.query.filter(Students.username == user_name).all()
        tch_usname_ex = Teachers.query.filter(Teachers.username == user_name).all()

        if not std_usname_ex and not tch_usname_ex:
            save_teacher = Teachers(
                            name=full_name,
                            username=user_name,
                            password=password,
                            subject=subject
                        )
            try:
                db.session.add(save_teacher)
                db.session.commit()

                session['name'] = user_name
                return redirect('/')
            except:
                return '404'
        else:
            us_ex_err = 'Это имя пользователся уже существует'
            return render_template('reg_teach.html', err=us_ex_err)

    return render_template('reg_teach.html')

@disp.route('/auth', methods=['POST', 'GET'])
def auth_stud():
    if request.method == "POST":
        user_name = request.form['username']
        password = request.form['password']

        Stud_exist = Students.query.filter(Students.username == user_name).all()
        Teach_exist = Teachers.query.filter(Teachers.username == user_name).all()

        Stud_exist_passw = Students.query.filter(Students.password == password).all()
        Teach_exist_passw = Teachers.query.filter(Teachers.password == password).all()

        if Stud_exist and Stud_exist_passw or Stud_exist_passw and Teach_exist_passw:
            session['name'] = user_name
            return redirect('/')
        else:
            flash('Этот аккаунт не существует')
            return render_template('auth.html')

    return render_template('auth.html')

@disp.route('/commit_task', methods=['POST', 'GET'])
def commit_task():
    isTeacher = Teachers.query.filter(Teachers.username == session['name']).all()
    
    if isTeacher:
        if request.method == 'POST':
            task_name = request.form['task_name']
            task_desc = request.form['task_desc']
            task_photo = request.files['task_photo']
            img_content = task_photo.read()

            set_task = Tasks(teacher=session['name'], task_name=task_name, task_desc=task_desc, task_photo=img_content)
            db.session.add(set_task)
            db.session.commit()

            return redirect('/')
        else:
            return render_template('create_task.html')
    else:
        return '404'

@disp.route('/task/<teacher>/<id>', methods=['POST', 'GET'])
def tasks(teacher, id):
    student = session['name']
    get_task = Tasks.query.filter_by(teacher=teacher, id=id).first()
    ansExist = SendAns.query.filter(SendAns.from_author == student, SendAns.task_id == id).all()

    if request.method == 'POST':
        if student and student != teacher:
            author = session['name']

            ans_desc = request.form['ans_desc']
            ans_photo = request.files['ans_photo']
            ans_img = ans_photo.read()

            commit_answer = SendAns(task_id=id, answer_photo=ans_img, answer_desc=ans_desc, from_author=author, to_teacher=teacher)
            try:
                db.session.add(commit_answer)
                db.session.commit()
                return redirect(f'/task/{teacher}/{id}')
            except:
                return '404'
        else:
            return "Вы не можете отправить самому себе или вы не авторизованы"

    return render_template('teacher_task.html', task=get_task, ansExist=ansExist)

@disp.route('/teacher/<teacher>/answers')
def answers(teacher):
    isTeacher = session['name'] == teacher

    if isTeacher:
        task_id = request.args.get('task_id')

        answer_list = SendAns.query.filter(SendAns.task_id == task_id).all()
        return render_template('teacher_answers.html', answer_list=answer_list)
    else:
        return "Вы не учитель"

@disp.route('/teacher/<teacher>/answers', methods=['GET', 'POST'])
def confirm(teacher):
    isTeacher = session['name'] == teacher

    if isTeacher:
        if request.method == 'POST':
            task_id = request.args.get('task_id')
            author_name = request.args.get('author')
            status = request.args.get('status')

            set_status = SendAns.query.filter_by(task_id=task_id, from_author=author_name).first()

            if status == 'True': set_status.status = True
            if status == 'False': set_status.status = False

            db.session.commit()
            return redirect(f'/teacher/{teacher}')
        else:
            return '404'
    return 'Вы не учитель'

@disp.route('/storage_t/<teacher>/<id>/')
def storage_f(teacher, id):
    conn_to_table = Tasks.query.filter_by(teacher=teacher, id=id).first()
    image_cont = conn_to_table.task_photo

    m_req = make_response(image_cont)
    m_req.headers['Content-Type'] = 'image/png'
    return m_req

@disp.route('/storage_s/<student>/<teacher>/<id>/')
def storage_s(student, teacher, id):
    if session['name'] == student or session['name'] == teacher:
        conn_to_table = SendAns.query.filter_by(from_author=student, to_teacher=teacher, task_id=id).first()
        image_cont = conn_to_table.answer_photo

        m_req = make_response(image_cont)
        m_req.headers['Content-Type'] = 'image/png'
        return m_req
    else:
        return '404'

@disp.route("/logout")
def logout_page():
    if 'name' in session:
        del session['name']
        return redirect("/")
    else:
        return "you dont have account"

@disp.errorhandler(404)
def page_not_found(error):
    return '404'

@disp.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return '500'