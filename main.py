from converter import Converter
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from forms import AddRace, UserForm, LoginForm
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user
from sqlalchemy.orm import relationship
from sqlalchemy import ForeignKey
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL", "sqlite:///races-database.db")
app.config['SQLALCHEMY_TRACK_MODIFICATION'] = False
app.secret_key = os.environ.get("SECRET_KEY", "Eden My Love")
Bootstrap(app)


login_manager = LoginManager()
login_manager.init_app(app)


db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False, unique=True)
    password = db.Column(db.String(250), nullable=False)
    races = relationship("Race", back_populates="runner")


class Race(db.Model):
    __tablename__ = "races"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String, nullable=False)
    runner_id = db.Column(db.Integer, ForeignKey('users.id'))
    runner = relationship("User", back_populates="races")


# db.create_all()


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/', methods=["POST", "GET"])
def home():
    render_template('index.html')
    data = request.form
    if request.method == "GET":
        units = ""
        return render_template('index.html', units=units, user=current_user, logged_in=current_user.is_authenticated)
    if data['unit'] == "km":
        units = "km/h:"
    else:
        units = "miles/h:"
    if data['calculation'] == "speed":
        try:
            converter = Converter(distance=float(data['distance']), time=float(data['time']))
            result = converter.convert_to_speed()
            return render_template('index.html', result=result, units=units, user=current_user,
                                   logged_in=current_user.is_authenticated)
        except ValueError:
            return render_template('index.html', units="Please enter a valid number", user=current_user,
                                   logged_in=current_user.is_authenticated)
    else:
        if data['unit'] == "km":
            units = "mins per km:"
        else:
            units = "mins per mile:"
        try:
            converter = Converter(distance=float(data['distance']), time=float(data['time']))
            result = converter.convert_to_pace()
            return render_template('index.html', result=result, units=units, user=current_user,
                                   logged_in=current_user.is_authenticated)
        except ValueError:
            return render_template('index.html', units="Please enter a valid number", user=current_user,
                                   logged_in=current_user.is_authenticated)


@app.route("/races", methods=["GET", "POST"])
def races():
    all_races = Race.query.order_by(Race.id).all()
    add_form = AddRace()
    if add_form.validate_on_submit():
        race_name = add_form.race_name.data
        race_date = add_form.race_date.data
        for race in current_user.races:
            if race.title == race_name:
                flash(f"You are already running {race_name}")
                return redirect(url_for("races"))
        new_race = Race(title=race_name,
                        date=race_date,
                        runner_id=current_user.id,
                        runner=current_user
                        )
        db.session.add(new_race)
        db.session.commit()
        return redirect(url_for('races'))
    return render_template("races.html", form=add_form, races=all_races, user=current_user,
                           logged_in=current_user.is_authenticated)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        password = generate_password_hash(form.password.data,
                                          method='pbkdf2:sha256',
                                          salt_length=8)

        new_user = User(name=name,
                        email=email,
                        password=password)
        if User.query.filter_by(email=form.email.data).first():
            flash("You already registered with this email!")
            return redirect(url_for("register"))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template("register.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return redirect(url_for("home"))
        else:
            flash("incorrect email/password")
            return redirect(url_for("login"))
    return render_template("login.html", form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/delete/<int:race_id>')
def delete_race(race_id):
    race_to_delete = Race.query.get(race_id)
    db.session.delete(race_to_delete)
    db.session.commit()
    return redirect(url_for('races'))


if __name__ == "__main__":
    app.run(debug=True)
