#!/usr/bin/env python3
"""
Servidor simple para servir el frontend
"""
import http.server
import socketserver
import os
import sys
import webbrowser
from pathlib import Path

PORT = 3000

class CORSRequestHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', '*')
        super().end_headers()

def serve_frontend():
    # Cambiar al directorio Front
    frontend_dir = Path(__file__).parent
    os.chdir(frontend_dir)
    
    print(f"🌐 Iniciando servidor frontend en http://localhost:{PORT}")
    print(f"📁 Sirviendo archivos desde: {frontend_dir}")
    print("🚀 Presiona Ctrl+C para detener el servidor")
    print()
    print("📋 Instrucciones:")
    print("1. Asegúrate de que tu API esté ejecutándose en http://localhost:8000")
    print("2. Abre http://localhost:3000/login.html en tu navegador")
    print("3. Inicia sesión con las credenciales de prueba:")
    print("   - Admin: admin123 / admin123")
    print("   - User: user123 / user123")
    print()
    
    try:
        with socketserver.TCPServer(("", PORT), CORSRequestHandler) as httpd:
            print(f"✅ Servidor iniciado exitosamente en puerto {PORT}")
            
            # Intentar abrir el navegador automáticamente
            try:
                webbrowser.open(f'http://localhost:{PORT}/login.html')
                print("🌐 Abriendo navegador automáticamente...")
            except:
                print("❌ No se pudo abrir el navegador automáticamente")
                print(f"   Abre manualmente: http://localhost:{PORT}")
            
            print()
            httpd.serve_forever()
            
    except KeyboardInterrupt:
        print("\n⏹️  Servidor detenido por el usuario")
    except OSError as e:
        if e.errno == 48:  # Address already in use
            print(f"❌ Error: El puerto {PORT} ya está en uso")
            print("   Detén el otro proceso o usa un puerto diferente")
        else:
            print(f"❌ Error al iniciar servidor: {e}")
    except Exception as e:
        print(f"❌ Error inesperado: {e}")

if __name__ == "__main__":
    serve_frontend()