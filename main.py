import http.server
import socketserver
import json
import os
import base64
import io
import numpy as np
from PIL import Image, ImageFilter

# --- MOTOR NBO-A / PERCEPTRÓN 211 ---
def relu_mod_211(S):
    if S <= 0:
        return 0.0
    y1 = S * 0.5
    return y1 * (211.0 / (211.0 + y1))

def procesar_matriz_rostro(img_pil, tono_r, tono_g, tono_b, brillo, contraste, suavizado):
    arr = np.array(img_pil, dtype=np.float32)

    factor_brillo = relu_mod_211(brillo) / 50.0
    factor_contraste = relu_mod_211(contraste) / 50.0

    arr = (arr - 128.0) * factor_contraste + 128.0 + (factor_brillo * 25.5)

    if tono_r != 100 or tono_g != 100 or tono_b != 100:
        arr[:, :, 0] *= (tono_r / 100.0)
        arr[:, :, 1] *= (tono_g / 100.0)
        arr[:, :, 2] *= (tono_b / 100.0)

    arr = np.clip(arr, 0, 255).astype(np.uint8)
    img_resultado = Image.fromarray(arr)

    if suavizado > 0:
        radio_blur = (suavizado / 100.0) * 3.0
        img_resultado = img_resultado.filter(ImageFilter.GaussianBlur(radius=radio_blur))

    return img_resultado

class HandlerProcesador(http.server.SimpleHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_OPTIONS(self):
        self._set_headers()

    def do_POST(self):
        if self.path == '/api/procesar_rostro':
            try:
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                datos = json.loads(post_data.decode('utf-8'))

                img_b64 = datos.get('imagen').split(',')[1]
                img_bytes = base64.b64decode(img_b64)
                img = Image.open(io.BytesIO(img_bytes)).convert('RGB')

                t_r = float(datos.get('tono_r', 100))
                t_g = float(datos.get('tono_g', 100))
                t_b = float(datos.get('tono_b', 100))
                brillo = float(datos.get('brillo', 50))
                contraste = float(datos.get('contraste', 50))
                suavizado = float(datos.get('suavizado', 0))

                img_editada = procesar_matriz_rostro(img, t_r, t_g, t_b, brillo, contraste, suavizado)

                buffered = io.BytesIO()
                img_editada.save(buffered, format="JPEG", quality=85)
                img_resultado_b64 = "data:image/jpeg;base64," + base64.b64encode(buffered.getvalue()).decode('utf-8')

                self._set_headers()
                self.wfile.write(json.dumps({"estatus": "ok", "imagen_procesada": img_resultado_b64}).encode('utf-8'))
            except Exception as e:
                self.send_response(500)
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode('utf-8'))
        else:
            # Permite servir los archivos estáticos de la carpeta assets (como index.html)
            super().do_GET()

PORT = 8080
os.chdir(os.path.dirname(os.path.abspath(__file__)))

print(f"--- Servidor NBO-A Génesis B en Puerto {PORT} http://localhost:8080/assets/index.html ---")
with socketserver.TCPServer(("", PORT), HandlerProcesador) as httpd:
    httpd.serve_forever()
