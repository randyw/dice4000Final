from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm
from flask_login import current_user, login_user
from flask_login import logout_user
from flask_login import login_required
from app.models import User, Org
from flask import request
from werkzeug.urls import url_parse
from app import db
from app.forms import RegistrationForm, CreateOrgForm, EditOrgForm, CreateUserForm, EditUserForm, DeleteOrgForm, DeleteUserForm


@app.route('/')
@app.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        # NOTE: Set permission_level 2 = admins, 1 = faculty, 0 = students
        user = User(email=form.email.data, permission_level=form.permission_level.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/search/users', methods=['GET'])
@login_required
def search_users():
    if current_user.permission_level is not 2:
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    results_count = User.query.count()
    users = User.query.order_by(User.email).paginate(
        page, app.config['RESULTS_PER_PAGE'], False)
    next_url = url_for('search_users', page=users.next_num) \
        if users.has_next else None
    prev_url = url_for('search_users', page=users.prev_num) \
        if users.has_prev else None
    return render_template('search_users.html', title='Search Users',
        users=users.items, next_url=next_url, prev_url=prev_url,
        results_count=results_count)


@app.route('/create/user', methods=['GET', 'POST'])
@login_required
def create_user():
    if current_user.permission_level is not 2:
        return redirect(url_for('index'))
    form = CreateUserForm()
    if form.validate_on_submit():
        # NOTE: Set permission_level 2 = admins, 1 = faculty, 0 = students
        user = User(email=form.email.data, permission_level=form.permission_level.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you created a user!')
        return redirect(url_for('index'))
    return render_template('create_user.html', title='Create User', form=form)


@app.route('/search/orgs', methods=['GET'])
@login_required
def search_orgs():
    page = request.args.get('page', 1, type=int)
    results_count = Org.query.count()
    orgs = Org.query.order_by(Org.name).paginate(
        page, app.config['RESULTS_PER_PAGE'], False)
    next_url = url_for('search_orgs', page=orgs.next_num) \
        if orgs.has_next else None
    prev_url = url_for('search_orgs', page=orgs.prev_num) \
        if orgs.has_prev else None
    return render_template('search_orgs.html', title='Search Organizations',
        orgs=orgs.items, next_url=next_url, prev_url=prev_url,
        results_count=results_count)


@app.route('/create/org', methods=['GET', 'POST'])
@login_required
def create_org():
    if current_user.permission_level is 0:
        return redirect(url_for('index'))
    form = CreateOrgForm()
    if form.validate_on_submit():
        org = Org(
            name=form.name.data,             
            bg_check_required=form.bg_check_required.data,             
            description=form.description.data,             
            keywords=form.keywords.data,             
            num_volunteers=form.num_volunteers.data,             
            mission_statement=form.mission_statement.data,             
            website=form.website.data, 
            primary_contact_name=form.primary_contact_name.data,             
            primary_contact_title=form.primary_contact_title.data,             
            primary_contact_email=form.primary_contact_email.data,             
            primary_contact_phone=form.primary_contact_phone.data,             
            street_address=form.street_address.data,             
            zip_code=form.zip_code.data,             
            alt_contact_name=form.alt_contact_name.data,             
            alt_contact_email=form.alt_contact_email.data,             
            application_url=form.application_url.data            
            )        
        db.session.add(org)
        db.session.commit()
        flash('Congratulations, you created an org!')
        return redirect(url_for('index'))
    return render_template('create_org.html', title='Create Organization', form=form)

@app.route('/edit/user/<userid>', methods=['GET', 'POST'])
@login_required
def edit_user(userid):
    if current_user.permission_level is not 2:
        return redirect(url_for('index'))
    user = User.query.filter_by(id=userid).first_or_404()
    form = EditUserForm()
    
    if form.validate_on_submit():
        user.permission_level = form.permission_level.data
        db.session.commit()
        flash('User Updated')
        return redirect(url_for('view_user', userid=user.id))

    return render_template('edit_user.html', title='Edit User', user=user, form=form)

@app.route('/view/user/<userid>', methods=['GET'])    
@login_required
def view_user(userid):
    if current_user.permission_level is not 2:
        return redirect(url_for('index'))
    user = User.query.filter_by(id=userid).first_or_404()
    return render_template('view_user.html', title='View User', user=user)

@app.route('/view/org/<orgid>', methods=['GET'])
@login_required
def view_org(orgid):
    org = Org.query.filter_by(id=orgid).first_or_404()
    return render_template('view_org.html', title='View Organization', org=org)

#start of Aaron Adds:
@app.route('/edit/org/<orgid>', methods=['GET', 'POST'])
@login_required
def edit_org(orgid):
    form = EditOrgForm()
    if current_user.permission_level is 0:
        return redirect(url_for('index'))
    org = Org.query.filter_by(id=orgid).first_or_404()

    if form.validate_on_submit():
        org.name = form.name.data
        org.bg_check_required = form.bg_check_required.data
        org.description = form.description.data
        org.keywords = form.keywords.data
        org.num_volunteers = form.num_volunteers.data
        org.mission_statement = form.mission_statement.data
        org.website = form.website.data
        org.primary_contact_name = form.primary_contact_name.data
        org.primary_contact_title = form.primary_contact_title.data 
        org.primary_contact_email = form.primary_contact_email.data 
        org.primary_contact_phone = form.primary_contact_phone.data 
        org.street_address = form.street_address.data
        org.zip_code = form.zip_code.data
        org.alt_contact_name = form.alt_contact_name.data
        org.alt_contact_email = form.alt_contact_email.data
        org.application_url = form.application_url.data

        db.session.commit()
        flash('Organization Updated! ')
        return redirect(url_for('view_org', orgid=org.id))
    elif request.method == 'GET':
        form.name.data = org.name
        form.bg_check_required.data = org.bg_check_required
        form.description.data = org.description
        form.keywords.data = org.keywords
        form.num_volunteers.data = org.num_volunteers
        form.mission_statement.data = org.mission_statement
        form.website.data = org.website
        form.primary_contact_name.data = org.primary_contact_name
        form.primary_contact_title.data = org.primary_contact_title
        form.primary_contact_email.data = org.primary_contact_email
        form.primary_contact_phone.data = org.primary_contact_phone
        form.street_address.data = org.street_address
        form.zip_code.data = org.zip_code
        form.alt_contact_name.data = org.alt_contact_name
        form.alt_contact_email.data = org.alt_contact_email
        form.application_url.data = org.application_url
        
    return render_template('edit_org.html', title='Edit Organization', org=org, form=form )
#end of aaron adds

@app.route('/delete/org/<orgid>', methods=['GET', 'POST'])
@login_required
def delete_org(orgid):
    if current_user.permission_level is 0:
        return redirect(url_for('index'))
    
    org = Org.query.filter_by(id=orgid).first_or_404()
    form = DeleteOrgForm()
    
    if form.validate_on_submit():
        db.session.delete(org)
        db.session.commit()
        flash('Organization Deleted')
        return redirect(url_for('index'))
    
    return render_template('delete_org.html', title='Delete Organization', org=org, form=form )


@app.route('/delete/user/<userid>', methods=['GET', 'POST'])
@login_required
def delete_user(userid):
    if current_user.permission_level is not 2:
        return redirect(url_for('index'))
    user = User.query.filter_by(id=userid).first_or_404()
    
    form = DeleteUserForm()
    if form.validate_on_submit():
        db.session.delete(user)
        db.session.commit()
        flash('User Deleted')
        return redirect(url_for('index'))
    
    return render_template('delete_user.html', title='Delete User', user=user, form=form )