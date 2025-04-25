from flask import request, jsonify, redirect, url_for, render_template
from auth import generate_token, validate_token
from decorators import token_required
from utils import validate_input, load_secret_key
from database import DATABASE
import sqlite3
import os

def register_routes(app):
    """Register all application routes.
    Args:
        app: Flask application instance
    """
    @app.route('/')
    def index():
        """Render index page"""
        return render_template('index.html')

    @app.route('/login', methods=['POST'])
    def login():
        """Handle user login.
        Returns:
            JSON response with login status and sets JWT cookie if successful
        """
        data = request.get_json()

        if not data or 'username' not in data or 'password' not in data:
            return jsonify({'status': 'error'}), 401

        username = data['username']
        password = data['password']

        try:
            with sqlite3.connect(DATABASE) as conn:
                c = conn.cursor()
                c.execute("SELECT * FROM users WHERE username=? AND password=? LIMIT 1", 
                        (username, password))
                user = c.fetchone()

                if user:
                    SECRET_KEY = load_secret_key()
                    token = generate_token({
                        'id': user[0],
                        'username': user[1],
                        'access_level': user[4],
                        'email': user[3]
                    }, SECRET_KEY)

                    response = jsonify({'status': 'success'})
                    response.set_cookie('token', token, httponly=True, secure=True, samesite='Lax')
                    return response

            return jsonify({'status': 'error'}), 401
        except Exception as e:
            print("Login error:", str(e))
            return jsonify({'status': 'error'}), 500


    @app.route('/register', methods=['POST'])
    def register():
        """Handle user registration.
        Returns:
            JSON response with registration status
        """
        try:
            data = request.get_json()
            if not data or not all(k in data for k in ['username', 'password', 'email']):
                return jsonify({'status': 'error', 'message': 'Datos incompletos'}), 400
            
            if not all(validate_input(data[k]) for k in ['username', 'password', 'email']):
                return jsonify({'status': 'error', 'message': 'Caracteres no permitidos'}), 400

            with sqlite3.connect(DATABASE) as conn:
                c = conn.cursor()
                c.execute("SELECT 1 FROM users WHERE username=? LIMIT 1", (data['username'],))
                if c.fetchone():
                    return jsonify({'status': 'error', 'message': 'Usuario ya existe'}), 400
                
                c.execute(
                    "INSERT INTO users (username, password, email, access_level) VALUES (?, ?, ?, 1)",
                    (data['username'], data['password'], data['email'])
                )
                conn.commit()
                user_id = c.lastrowid
            
            response = jsonify({'status': 'success'})
            return response
            
        except sqlite3.Error:
            return jsonify({'status': 'error', 'message': 'Error en la base de datos'}), 500
        except Exception as e:
            print(f"Error inesperado: {e}")
            return jsonify({'status': 'error', 'message': 'Error en el servidor'}), 500

    @app.route('/doctor/<int:doctor_id>/research', methods = ['GET'])
    @token_required
    def get_doctor_research(doctor_id):
        """Get doctor research data if user has sufficient access level.
        Args:
            doctor_id: ID of the doctor to get research for
        Returns:
            JSON response with research data or error message
        """

        try:
            current_user = request.current_user

            with sqlite3.connect(DATABASE) as conn:
                c = conn.cursor()
                c.execute("SELECT id, name, record, access_level FROM doctors WHERE id = ? LIMIT 1", (doctor_id,))
                doctor = c.fetchone()

                if not doctor:
                    return jsonify({'error': 'Doctor no encontrado'}), 404

                doctor_id, name, record, access_level = doctor

                if current_user['access_level'] < access_level:
                    return jsonify({
                        'error': f'Se requiere nivel de acceso {access_level} para ver esta investigación',
                        'required_level': access_level
                    }), 403

                # Construir datos de investigación basados en nivel de acceso
                is_high_level = access_level == 3
                research_data = {
                    'doctor_id': doctor_id,
                    'doctor_name': name,
                    'last_updated': '2025-04-24',
                    'research_data': {
                        'project': 'Neurotecnología Experimental' if is_high_level else 'Estudio Neurológico',
                        'code': f"NEURO-2025-{doctor_id:03d}",
                        'findings': record or 'No hay hallazgos registrados',
                        'methods': ['EEG', 'fMRI'],
                        'results': (
                            "Resultados preliminares muestran actividad cerebral inusual."
                            if is_high_level else
                            "Resultados dentro de parámetros normales."
                        ),
                        'notes': (
                            "Paciente bajo observación especial."
                            if is_high_level else
                            "Seguimiento rutinario."
                        )
                    }
                }

                return jsonify(research_data)

        except Exception as e:
            print(f"Error: {str(e)}")
            return jsonify({'error': 'Error en el servidor'}), 500

    @app.route('/dashboard')
    @token_required
    def dashboard():
        """Render dashboard page for authenticated users.
        Returns:
            Rendered dashboard template with user data
        """
        return render_template('dashboard.html', user=request.current_user)
