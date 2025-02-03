from flask import render_template , url_for ,  redirect , Blueprint , flash
from flask_login import login_required , current_user

from auths.forms import CreateTaskForm , UpdateTaskForm , DeleteTaskForm 
from models.models import Task ,  db


other_bp = Blueprint('other' , __name__)

@other_bp.route('/')
def WelcomePage():
    return render_template("WelcomePage.html")



@other_bp.route('/home' , methods = ['GET' , 'POST'])
@login_required
def userpage():
    create_form = CreateTaskForm()
    update_form = UpdateTaskForm()
    delete_form = DeleteTaskForm()
    
    # Handle task creation
    if create_form.validate_on_submit():
        new_task = Task(
            title=create_form.title.data,
            description=create_form.description.data,
            user_id=current_user.id
        )
        db.session.add(new_task)
        db.session.commit()
        flash('Task created successfully!', 'success')
        return redirect(url_for('other.userpage'))

    # Handle task updates
    elif update_form.validate_on_submit():
        task = Task.query.get(update_form.id.data)
        if task and task.user_id == current_user.id:
            task.title = update_form.title.data
            task.description = update_form.description.data
            db.session.commit()
            flash('Task updated successfully!', 'success')
        else:
            flash('Task not found or unauthorized', 'error')
        return redirect(url_for('other.userpage'))

    # Handle task deletion
    elif delete_form.validate_on_submit():
        task = Task.query.get(delete_form.id.data)
        if task is None:
            flash('task not found', 'error')
        elif task and task.user_id == current_user.id :
            db.session.delete(task)
            db.session.commit()
            flash('Task deleted successfully!', 'success')
        elif task and task.user_id != current_user.id:
            flash('Task not found or unauthorized', 'error')
        return redirect(url_for('other.userpage'))

    # Get current user's tasks
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template(
        'home.html',
        create_form=create_form,
        update_form=update_form,
        delete_form=delete_form,
        tasks=tasks
    )



@other_bp.route('/terms')
def terms_of_service():
    return 'just accept it you have nothing to lose !'



@other_bp.errorhandler(404)
def page_not_found():
    return render_template('404.html')
