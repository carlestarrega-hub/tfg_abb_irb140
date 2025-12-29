from flask import Flask, render_template

# Le decimos a Flask que busque el HTML en la carpeta donde estamos ('.')
app = Flask(__name__, template_folder='.')

@app.route('/')
def index():
    # Aquí es donde le dice al navegador: "Toma el archivo index.html que hizo Carles"
    return render_template('index.html')

if __name__ == '__main__':
    # Arranca el servidor para que puedas entrar
    app.run(host='0.0.0.0', port=5000, debug=True)
