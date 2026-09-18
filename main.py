import http.server
import socketserver
import json
import os
import base64
import io
import threading
import time
import numpy as np
from PIL import Image, ImageFilter

# --- TU MOTOR DE IA (NBO-a / PERCEPTRÓN 211) ---
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
            self.send_error(404)

PORT = 8080

# 🚀 FORZAR RUTA: Asegura que el servidor corra exactamente donde están index.html y main.py
ruta_raiz = os.path.dirname(os.path.abspath(__file__))
os.chdir(ruta_raiz)

def iniciar_servidor():
    print(f"--- Servidor en Puerto {PORT} http://localhost:8080/index.html ---")
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.TCPServer(("", PORT), HandlerProcesador) as httpd:
        httpd.serve_forever()

# Servidor en segundo plano para evitar congelamientos
server_thread = threading.Thread(target=iniciar_servidor)
server_thread.daemon = True
server_thread.start()

# --- INTERFAZ KIVY CON WEBVIEW NATIVO PARA ANDROID ---
try:
    from kivy.app import App
    from kivy.uix.modalview import ModalView
    # Importación nativa de Android para incrustar tu HTML en la pantalla del celular
    from jnius import autoclass
    
    class SalonStudioApp(App):
        def build(self):
            # Usamos la actividad nativa de Android para renderizar el navegador dentro del APK
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            
            WebView = autoclass('android.webkit.WebView')
            WebViewClient = autoclass('android.webkit.WebViewClient')
            
            # Crear el componente web en el hilo de la interfaz de Android
            browser = WebView(activity)
            browser.getSettings().setJavaScriptEnabled(True)
            browser.getSettings().setDomStorageEnabled(True) # Requerido para cámaras web
            browser.setWebViewClient(WebViewClient())
            
            # Cargar tu index.html local
            browser.loadUrl(f"http://localhost:{PORT}/index.html")
            
            activity.setContentView(browser)
            return browser
            
    if __name__ == '__main__':
        SalonStudioApp().run()
except Exception as e:
    print("Entorno de desarrollo PC o Kivy nativo ausente. Manteniendo servidor activo de prueba...")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        pass
