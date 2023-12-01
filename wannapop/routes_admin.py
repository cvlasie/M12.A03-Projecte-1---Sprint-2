from flask import Blueprint, render_template, redirect, url_for, flash, abort, request
from flask_login import current_user, login_required
from .models import User, BlockedUser
from .helper_role import Role, role_required
from . import db_manager as db
from .forms import ModerationForm
from datetime import datetime

# Blueprint
admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route('/admin')
@role_required(Role.admin, Role.moderator)
def admin_index():
    return render_template('admin/index.html')

@admin_bp.route('/admin/users')
@role_required(Role.admin)
def admin_users():
    users = db.session.query(User).all()
    return render_template('admin/users_list.html', users=users)

@admin_bp.route('/admin/users/<int:user_id>/block', methods=['GET', 'POST'])
@role_required(Role.admin)
def block_user(user_id):
    user_to_block = db.session.query(User).get(user_id)
    if user_to_block:
        if db.session.query(BlockedUser).filter_by(user_id=user_to_block.id).first():
            flash(f"Usuario {user_to_block.name} ya está bloqueado", "warning")
            return redirect(url_for('admin_bp.admin_users'))

        if request.method == 'POST':
            reason = request.form.get('reason')
            
            # Agrega la fecha de creación
            creation_date = datetime.now()

            # Bloquear al usuario y agregar a la tabla blocked_users
            blocked_user = BlockedUser(user_id=user_to_block.id, message=reason, created=creation_date)
            db.session.add(blocked_user)
            db.session.commit()

            flash(f"Usuario {user_to_block.name} bloqueado", "success")
            return redirect(url_for('admin_bp.admin_users', blocked_user_id=user_id))
        else:
            # Si es una solicitud GET, simplemente renderiza la plantilla
            return render_template('admin/block_users.html', blocked_user=user_to_block)
    else:
        flash("Usuario no encontrado", "error")
        return redirect(url_for('admin_bp.admin_users'))

@admin_bp.route('/admin/users/<int:user_id>/unblock', methods=['GET', 'POST'])
@role_required(Role.admin)
def unblock_user(user_id):
    user_to_unblock = db.session.query(User).get(user_id)
    form = ModerationForm()

    if user_to_unblock:
        blocked_user = db.session.query(BlockedUser).filter_by(user_id=user_to_unblock.id).first()

        if blocked_user:
            if request.method == 'POST':
                # Eliminar de la tabla blocked_users
                db.session.delete(blocked_user)
                db.session.commit()

                flash(f"Usuario {user_to_unblock.name} desbloqueado", "success")
                return redirect(url_for('admin_bp.admin_users'))
            
            return render_template('admin/unblock_users.html', blocked_user=user_to_unblock, form=form)
        
        flash("Usuario no está bloqueado", "warning")
    else:
        flash("Usuario no encontrado", "error")

    return redirect(url_for('admin_bp.admin_users'))