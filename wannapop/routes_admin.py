from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Product, BannedProduct
from .helper_role import Role, role_required
from . import db_manager as db
from flask_login import login_required
from .forms import UnbanForm

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

@admin_bp.route('/admin/products/<int:product_id>/ban', methods=['GET', 'POST'])
@login_required
@role_required(Role.moderator)
def ban_product(product_id):
    product = Product.query.get_or_404(product_id)
    banned_product = BannedProduct.query.filter_by(product_id=product_id).first()

    if banned_product:
        flash('Aquest producte ja està prohibit.', 'error')
        return redirect(url_for('admin_bp.admin_index'))
        
    if request.method == 'POST':
        reason = request.form.get('reason')
        if not reason:
            flash('Has d\'introduir una raó per a la prohibició.', 'error')
            return redirect(url_for('admin_bp.admin_index'))


        new_banned_product = BannedProduct(product_id=product_id, reason=reason)
        db.session.add(new_banned_product)
        db.session.commit()

        flash('Producte prohibit amb èxit.', 'success')
        return redirect(url_for('admin_bp.admin_index'))

    return render_template('admin/ban_product.html', product=product)

@admin_bp.route('/admin/products/<int:product_id>/unban', methods=['GET', 'POST'])
@login_required
@role_required(Role.moderator)
def unban_product(product_id):
    form = UnbanForm()
    banned_product = BannedProduct.query.filter_by(product_id=product_id).first()
    if not banned_product:
        flash('Aquest producte no està prohibit.', 'error')
        return redirect(url_for('admin_bp.admin_index'))
    if request.method == 'POST' and form.validate_on_submit():
        

        db.session.delete(banned_product)
        db.session.commit()
        flash('La prohibició del producte ha estat eliminada.', 'success')
        return redirect(url_for('admin_bp.admin_index'))

    return render_template('admin/unban_product.html', product_id=product_id, form=form)