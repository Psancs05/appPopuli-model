from decimal import Decimal, ROUND_HALF_UP
from flask import Flask, request, jsonify
from flask_cors import CORS
from gevent.pywsgi import WSGIServer
import Predictions.main_predictions
import os
from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)
SCRIPT = '/Predictions/main_predictions.py'

@app.errorhandler(405)
def handle_method_not_allowed(e):
    return jsonify({'estado': 'ko', 'resultado': 'Solo se admite el uso del método -POST- '}), 405

@app.errorhandler(404)
def handle_method_not_allowed(e):
    return jsonify({'estado': 'ko', 'resultado': 'Solo se admite el uso del método -POST- '}), 404

@app.errorhandler(500)
def handle_method_not_allowed(e):
    return jsonify({'estado': 'ko', 'resultado': 'El argumento ruta_img o ruta_model estan mal '}), 500

# @app.route('/api', methods=['POST'])
# def api():
#     try:
#         ruta_img = request.get_json().get('ruta_img')
#         ruta_model = request.get_json().get('ruta_model')

#         # print ruta_img and ruta_model
#         print("ruta_img: ",ruta_img)
#         print("ruta_model: ",ruta_model)

#         # Comprueba el parámetro
#         if ruta_img is None:
#             return jsonify({'estado': 'ko', 'resultado': 'El argumento ruta_img o ruta_model estan mal '}), 500

#         if ruta_model is None:
#             output = Predictions.main_predictions.main(ruta_img)
#         else:
#             output = Predictions.main_predictions.main(ruta_img,ruta_model)
        
#         return jsonify({'estado': 'ok', 'resultado': output})
#     except Exception as e:
#         return jsonify({'estado': 'ko', 'resultado': 'Error en el engine' , 'excepcion': str(e)})

@app.route('/api', methods=['POST'])
def api():
    try:
        # Acceder al archivo de imagen cargado
        image_file = request.files.get('image')

        image_file.seek(0, 2)  # Mover al final del archivo
        file_size = image_file.tell()  # Obtener la posición, que es igual al tamaño del archivo en bytes
        image_file.seek(0)  # Mover de nuevo al inicio del archivo para futuras operaciones
        print(f"File size: {file_size} bytes")


        # Si no se proporcionó ningún archivo, devolver un error
        if image_file is None:
            return jsonify({'estado': 'ko', 'resultado': 'No se proporcionó una imagen'}), 400

        # Cargar la imagen en PIL para su posterior procesamiento
        image = Image.open(BytesIO(image_file.read()))

        ruta_model = request.form.get('ruta_model')  # Si necesitas ruta_model, puedes enviarlo como parte del FormData

        # Tu código para hacer la predicción, asumiendo que tu función main() puede manejar un objeto PIL
        if ruta_model is None:
            output = Predictions.main_predictions.main(image)
        else:
            output = Predictions.main_predictions.main(image, ruta_model)

        return jsonify({'estado': 'ok', 'resultado': output})

    except Exception as e:
        return jsonify({'estado': 'ko', 'resultado': 'Error en el engine', 'excepcion': str(e)})
    
@app.route('/api', methods=['GET'])
def ping():
    return jsonify({'estado': 'ok', 'resultado': 'pong'})
    


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8080))
    http_server = WSGIServer(("0.0.0.0", port), app)
    http_server.serve_forever()
