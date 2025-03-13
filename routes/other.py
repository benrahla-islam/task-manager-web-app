from flask import render_template, url_for, redirect, Blueprint, flash, request, jsonify, get_flashed_messages, current_app
from flask_login import login_required, current_user
from functools import partial
from sqlalchemy.exc import IntegrityError
import logging

from auths.forms import CreateTaskForm, UpdateTaskForm, DeleteTaskForm, CreateGroupForm, DeleteGroupForm, UpdateGroupForm
from models.models import Task, db, Group


other_bp = Blueprint('other', __name__)


class FlashMessageManager:
    """Centralized flash message management system"""
    
    # Message categories
    SUCCESS = 'success'
    ERROR = 'error'
    INFO = 'info'
    WARNING = 'warning'
    
    @staticmethod
    def flash(message, category=INFO, log_level=None):
        """
        Flash a message to the user and optionally log it
        
        Args:
            message: The message text to display
            category: Message category (success, error, info, warning)
            log_level: Optional logging level (debug, info, warning, error, critical)
        """
        if message:
            flash(message, category)
            
            # Log the message if requested
            if log_level:
                logger = logging.getLogger(current_app.name)
                log_method = getattr(logger, log_level, logger.info)
                log_method(f"[{category.upper()}] {message}")
    
    @classmethod
    def success(cls, message, log_level='info'):
        """Flash a success message"""
        cls.flash(message, cls.SUCCESS, log_level)
    
    @classmethod
    def error(cls, message, log_level='error'):
        """Flash an error message"""
        cls.flash(message, cls.ERROR, log_level)
    
    @classmethod
    def form_errors(cls, form):
        """Handle form validation errors"""
        if form.errors:
            cls.error("Please check the form for errors", 'warning')


def process_form(form, action, success_message, error_message, **kwargs):
    if form.validate_on_submit():
        try:
            action(form, **kwargs)
            db.session.commit()
            FlashMessageManager.success(success_message)
            return True
        except IntegrityError as e:
            db.session.rollback()
            logging.error(f"Database integrity error: {str(e)}")
        except Exception as e:
            db.session.rollback()
            logging.error(f"Error processing form: {str(e)}")
            FlashMessageManager.error(error_message)
    else:
        FlashMessageManager.form_errors(form)
    return False


def create_task(form, current_user):
    new_task = Task(
        title=form.title.data,
        description=form.description.data,
        user_id=current_user.id , 
        group_id=form.group.data if form.group.data else None
    )
    db.session.add(new_task)


def update_task(form):
    task = Task.query.get(form.id.data)
    if task:
        task.title = form.title.data
        task.description = form.description.data


def delete_task(form):
    task = Task.query.get(form.id.data)
    if task:
        db.session.delete(task)


def create_group(form, current_user):
    new_group = Group(
        name=form.name.data,
        user_id=current_user.id,
        color=form.color.data if form.color.data else 'blue'
    )
    db.session.add(new_group)

def delete_group(form):
    group = Group.query.get(form.id.data)
    if group:
        db.session.delete(group)


def update_group(form):
    group = Group.query.get(form.id.data)
    if group:
        group.name = form.name.data
        



@other_bp.route('/')
def WelcomePage():
    return render_template("WelcomePage.html")



@other_bp.route('/home', methods=['GET', 'POST'])
@login_required
def userpage():
    create_task_form = CreateTaskForm(prefix='create_task_form')
    update_task_form = UpdateTaskForm(prefix='update_task_form')
    delete_task_form = DeleteTaskForm(prefix='delete_task_form')
    create_group_form = CreateGroupForm(prefix='create_group_form')
    update_group_form = UpdateGroupForm(prefix='update_group_form')
    delete_group_form = DeleteGroupForm(prefix='delete_group_form')

    create_task_form.group.choices = [(group.id, group.name) for group in Group.query.filter_by(user_id=current_user.id).all()]

    tasks = Task.query.filter_by(user_id=current_user.id).all()
    groups = Group.query.filter_by(user_id=current_user.id).all()

    #creating updated version of the creation function by adding the current user as a parameter, because it cannot be added later in the form precessing function
    process_create_task = partial(create_task, current_user=current_user)

    process_update_task = update_task
    process_delete_task = delete_task
    process_create_group = partial(create_group, current_user=current_user)
    process_update_group = update_group
    process_delete_group = delete_group

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        # Handle AJAX request
        form_name = request.form.get('form_name')

        if form_name == 'create_task_form' and create_task_form.validate_on_submit():
            process_form(create_task_form, process_create_task, 'Task created successfully!', 'An error occurred while creating the task.', current_user=current_user)
        elif form_name == 'update_task_form' and update_task_form.validate_on_submit():
            process_form(update_task_form, process_update_task, 'Task updated successfully!', 'An error occurred while updating the task.')
        elif form_name == 'delete_task_form' and delete_task_form.validate_on_submit():
            process_form(delete_task_form, process_delete_task, 'Task deleted successfully!', 'An error occurred while deleting the task.')
        elif form_name == 'create_group_form' and create_group_form.validate_on_submit():
            process_form(create_group_form, process_create_group, 'Group created successfully!', 'An error occurred while creating the group.', current_user=current_user)
        elif form_name == 'update_group_form' and update_group_form.validate_on_submit():
            process_form(update_group_form, process_update_group, 'Group updated successfully!', 'An error occurred while updating the group.')
        elif form_name == 'delete_group_form' and delete_group_form.validate_on_submit():
            process_form(delete_group_form, process_delete_group, 'Group deleted successfully!', 'An error occurred while deleting the group.')
        else:
            return jsonify({'status': 'error', 'message': 'Invalid form submission'})


        tasks = Task.query.filter_by(user_id=current_user.id).all()
        groups = Group.query.filter_by(user_id=current_user.id).all()
        return jsonify({'status': 'success', 'tasks': render_template('task_list.html', tasks=tasks), 'groups': render_template('group_list.html', groups=groups)})

    else:
        # Handle regular form submission
        if process_form(create_task_form, process_create_task, 'Task created successfully!', 'An error occurred while creating the task.') or \
                process_form(update_task_form, update_task, 'Task updated successfully!', 'An error occurred while updating the task.') or \
                process_form(delete_task_form, delete_task, 'Task deleted successfully!', 'An error occurred while deleting the task.') or \
                process_form(create_group_form, process_create_group, 'Group created successfully!', 'An error occurred while creating the group.') or \
                process_form(delete_group_form, delete_group, 'Group deleted successfully!', 'An error occurred while deleting the group.') or \
                process_form(update_group_form, update_group, 'Group updated successfully!', 'An error occurred while updating the group.'):
            return redirect(url_for('other.userpage'))


    return render_template(
        'home.html',
        create_task_form=create_task_form,
        update_task_form=update_task_form,
        delete_task_form=delete_task_form,
        create_group_form=create_group_form,
        delete_group_form=delete_group_form,
        tasks=tasks,
        groups=groups
    )


@other_bp.route('/terms')
def terms_of_service():
    return 'just accept it you have nothing to lose !'



@other_bp.errorhandler(404)
def page_not_found():
    return render_template('404.html')

