from flask import Flask, request, jsonify, render_template, redirect, url_for
from models import db, User

app = Flask(__name__)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:sanjai@localhost:5432/User'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)


with app.app_context():
    db.create_all()


# API routes
@app.route('/api/users', methods=['POST'])

def create_user_api():
    data = request.json
    new_user = User(
        username=data['username'], 
        email=data['email'], 
        password_hash=data['password_hash']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'id': new_user.id, 'status': 'User created successfully'}), 201


@app.route('/api/users', methods=['GET'])

def get_users_api():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200


@app.route('/api/users/<int:user_id>', methods=['GET'])

def get_user_api(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200


@app.route('/api/users/<int:user_id>', methods=['PUT'])

def update_user_api(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json
    user.username = data['username']

    db.session.commit()
    return jsonify({'status': 'User updated successfully'})


@app.route('/api/users/<int:user_id>', methods=['DELETE'])

def delete_user_api(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'status': 'User deleted successfully'})


# UI routes
@app.route('/')
def index():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/add-user', methods=['POST'])

def add_user():
    username = request.form['username']
    email = request.form['email']
    password_hash = request.form['password_hash']

    new_user = User(username=username, email=email, password_hash=password_hash)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))


@app.route('/edit-user/<int:user_id>', methods=['GET', 'POST'])

def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        user.username = request.form['username']
        user.email = request.form['email']

        db.session.commit()
        return redirect(url_for('index'))
    return render_template('edit-user.html', user=user)


@app.route('/delete-user/<int:user_id>')
def delete_user_ui(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('index'))


if __name__ == "__main__":
    app.run(debug=True)
