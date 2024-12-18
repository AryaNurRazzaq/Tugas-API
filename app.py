from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from datetime import datetime
from flask_bcrypt import Bcrypt


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db_tugas.db'  # Database lokal
app.config['JWT_SECRET_KEY'] = 'kunci-rahasia-saya'  # Ganti kunci untuk produksi

db = SQLAlchemy(app)
jwt = JWTManager(app)
bcrypt = Bcrypt(app)

# Database Tugas
class Tugas(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    judul = db.Column(db.String(100), nullable=False)
    deskripsi = db.Column(db.String(250))
    selesai = db.Column(db.Boolean, default=False)
    tanggal = db.Column(db.DateTime, default=datetime.utcnow)  # Ubah 'dibuat_pada' menjadi 'tanggal'

# Database Pengguna
class Pengguna(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

# Login
@app.route('/masuk', methods=['POST'])
def masuk():
    data = request.get_json()
    pengguna = Pengguna.query.filter_by(username=data.get("username")).first()

    if pengguna and bcrypt.check_password_hash(pengguna.password, data.get("password")):
        token = create_access_token(identity=pengguna.username)
        return jsonify({"token": token}), 200

    return jsonify({"pesan": "Username atau password salah"}), 401

# Register
@app.route('/daftar', methods=['POST'])
def daftar():
    data = request.get_json()
    
    # Cek username dalam database
    pengguna = Pengguna.query.filter_by(username=data['username']).first()
    if pengguna:
        return jsonify({'pesan': 'Username sudah terdaftar.'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    
    
    pengguna_baru = Pengguna(username=data['username'], password=hashed_password)
    db.session.add(pengguna_baru)
    db.session.commit()
    
    return jsonify({'pesan': 'Pengguna berhasil ditambahkan'}), 201


@app.route('/tugas', methods=['GET'])
@jwt_required()
def ambil_tugas():
    halaman = request.args.get('halaman', 1, type=int)
    jumlah_per_halaman = request.args.get('jumlah', 5, type=int)
    urutan = request.args.get('urutan', 'id') 
    filter_selesai = request.args.get('selesai')

    query = Tugas.query
    if filter_selesai:
        if filter_selesai.lower() == 'true':
            query = query.filter_by(selesai=True)
        elif filter_selesai.lower() == 'false':
            query = query.filter_by(selesai=False)

    if urutan == 'id':
        query = query.order_by(Tugas.id)
    elif urutan == 'judul':
        query = query.order_by(Tugas.judul)
    else:
        query = query.order_by(Tugas.tanggal)

    data_tugas = query.offset((halaman - 1) * jumlah_per_halaman).limit(jumlah_per_halaman).all()

    hasil = []
    for tugas in data_tugas:
        hasil.append({
            "id": tugas.id,
            "judul": tugas.judul,
            "deskripsi": tugas.deskripsi,
            "selesai": tugas.selesai,
            "tanggal": tugas.tanggal.strftime("%Y-%m-%d %H:%M:%S")  # Gunakan 'tanggal' di sini
        })

    return jsonify(hasil), 200

# Menambah tugas
@app.route('/tugas', methods=['POST'])
@jwt_required()
def tambah_tugas():

    data = request.get_json()
    if not data.get('judul'):
        return jsonify({"pesan": "Judul harus diisi"}), 400

    tugas_baru = Tugas(
        judul=data['judul'],
        deskripsi=data.get('deskripsi', '')
    )
    db.session.add(tugas_baru)
    db.session.commit()
    return jsonify({"pesan": "Tugas berhasil ditambahkan", "id": tugas_baru.id}), 201

# Edit tugas
@app.route('/tugas/<int:tugas_id>', methods=['PUT'])
@jwt_required()
def perbarui_tugas(tugas_id):
    tugas = Tugas.query.get(tugas_id)
    if not tugas:
        return jsonify({"pesan": "Tugas tidak ditemukan"}), 404

    data = request.get_json()
    tugas.judul = data.get('judul', tugas.judul)
    tugas.deskripsi = data.get('deskripsi', tugas.deskripsi)
    tugas.selesai = data.get('selesai', tugas.selesai)

    db.session.commit()
    return jsonify({"pesan": "Tugas berhasil diperbarui"}), 200

# Hapus tugas
@app.route('/tugas/<int:tugas_id>', methods=['DELETE'])
@jwt_required()
def hapus_tugas(tugas_id):
    tugas = Tugas.query.get(tugas_id)
    if not tugas:
        return jsonify({"pesan": "Tugas tidak ditemukan"}), 404

    db.session.delete(tugas)
    db.session.commit()
    return jsonify({"pesan": "Tugas berhasil dihapus"}), 200

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
