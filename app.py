from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Database connection
DB_USER = "postgres"
DB_PASSWORD = "321194142"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "loginappdb"

app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    def set_password(self, raw):
        self.password_hash = generate_password_hash(raw)

    def check_password(self, raw):
        return check_password_hash(self.password_hash, raw)

# Routes
@app.route('/')
def home():
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        return f"Registered Successfully: {name}"

    # If GET → show the register page
    return render_template("register.html")



# 3️⃣ LOGIN PAGE (GET)
@app.route('/login', methods=['GET'])
def login_page():
    return render_template("login.html")

# 4️⃣ LOGIN CHECK (POST)
@app.route('/login', methods=['POST'])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    user = User.query.filter_by(username=username).first()

    if user and user.check_password(password):
        return "Login Successful!"

    return "Invalid username or password"


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
