import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import qrcode
import os
from pathlib import Path

class GeneradorQR:
    def __init__(self, root):
        self.root = root
        self.root.title("Generador de Códigos QR")
        self.root.geometry("500x400")
        self.root.resizable(True, True)
        
        # Variable para guardar la ruta seleccionada
        self.ruta_guardado = str(Path.home() / "Downloads")  # Ruta por defecto: Downloads
        
        self.crear_interfaz()
    
    def crear_interfaz(self):
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configurar el grid para que se expanda
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Título
        titulo = ttk.Label(main_frame, text="Generador de Códigos QR", 
                          font=("Arial", 16, "bold"))
        titulo.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Campo para el enlace
        ttk.Label(main_frame, text="Enlace:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.entry_link = ttk.Entry(main_frame, width=40)
        self.entry_link.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Campo para el nombre del archivo
        ttk.Label(main_frame, text="Nombre del archivo:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.entry_nombre = ttk.Entry(main_frame, width=40)
        self.entry_nombre.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Nota sobre la extensión
        nota = ttk.Label(main_frame, text="(No incluyas la extensión .png, se añade automáticamente)", 
                        font=("Arial", 8), foreground="gray")
        nota.grid(row=3, column=1, columnspan=2, sticky=tk.W, pady=(0, 10))
        
        # Ruta de guardado
        ttk.Label(main_frame, text="Guardar en:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.label_ruta = ttk.Label(main_frame, text=self.ruta_guardado, 
                                   background="white", relief="sunken", width=35)
        self.label_ruta.grid(row=4, column=1, sticky=(tk.W, tk.E), pady=5, padx=(0, 5))
        
        # Botón para cambiar ruta
        btn_cambiar_ruta = ttk.Button(main_frame, text="Cambiar", 
                                     command=self.cambiar_ruta)
        btn_cambiar_ruta.grid(row=4, column=2, pady=5)
        
        # Frame para botones
        frame_botones = ttk.Frame(main_frame)
        frame_botones.grid(row=5, column=0, columnspan=3, pady=20)
        
        # Botones
        btn_generar = ttk.Button(frame_botones, text="Generar QR", 
                               command=self.generar_qr, style="Accent.TButton")
        btn_generar.pack(side=tk.LEFT, padx=5)
        
        btn_limpiar = ttk.Button(frame_botones, text="Limpiar", 
                               command=self.limpiar_campos)
        btn_limpiar.pack(side=tk.LEFT, padx=5)
        
        # Área de estado/resultados
        self.text_resultado = tk.Text(main_frame, height=8, width=50, 
                                    wrap=tk.WORD, state=tk.DISABLED)
        self.text_resultado.grid(row=6, column=0, columnspan=3, pady=10, 
                               sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Scrollbar para el texto
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, 
                                command=self.text_resultado.yview)
        scrollbar.grid(row=6, column=3, sticky=(tk.N, tk.S), pady=10)
        self.text_resultado.configure(yscrollcommand=scrollbar.set)
        
        # Configurar expansión del grid
        main_frame.rowconfigure(6, weight=1)
    
    def cambiar_ruta(self):
        """Permite al usuario seleccionar una carpeta donde guardar el QR"""
        nueva_ruta = filedialog.askdirectory(
            title="Selecciona la carpeta donde guardar el QR",
            initialdir=self.ruta_guardado
        )
        
        if nueva_ruta:  # Si el usuario no canceló
            self.ruta_guardado = nueva_ruta
            self.label_ruta.config(text=self.ruta_guardado)
            self.agregar_mensaje(f"Ruta cambiada a: {self.ruta_guardado}")
    
    def generar_qr(self):
        """Genera el código QR con los datos proporcionados"""
        # Obtener datos de los campos
        link = self.entry_link.get().strip()
        nombre = self.entry_nombre.get().strip()
        
        # Validaciones
        if not link:
            messagebox.showerror("Error", "Por favor ingresa un enlace")
            return
        
        if not nombre:
            messagebox.showerror("Error", "Por favor ingresa un nombre para el archivo")
            return
        
        # Validar caracteres válidos para nombres de archivo
        caracteres_invalidos = '<>:"/\\|?*'
        if any(char in nombre for char in caracteres_invalidos):
            messagebox.showerror("Error", 
                               f"El nombre no puede contener estos caracteres: {caracteres_invalidos}")
            return
        
        try:
            # Crear el QR
            qr = qrcode.QRCode(
                version=1,  # Controla el tamaño del QR
                error_correction=qrcode.constants.ERROR_CORRECT_L,  # Nivel de corrección de errores
                box_size=10,  # Tamaño de cada cuadrito
                border=4,  # Grosor del borde
            )
            
            qr.add_data(link)
            qr.make(fit=True)
            
            # Crear la imagen
            imagen_qr = qr.make_image(fill_color="black", back_color="white")
            
            # Crear la ruta completa del archivo
            nombre_completo = f"{nombre}.png"
            ruta_completa = os.path.join(self.ruta_guardado, nombre_completo)
            
            # Verificar si el archivo ya existe
            if os.path.exists(ruta_completa):
                respuesta = messagebox.askyesno(
                    "Archivo existente", 
                    f"El archivo '{nombre_completo}' ya existe. ¿Deseas reemplazarlo?"
                )
                if not respuesta:
                    return
            
            # Guardar la imagen
            imagen_qr.save(ruta_completa)
            
            # Mensaje de éxito
            mensaje_exito = f"✅ QR generado exitosamente!\n"
            mensaje_exito += f"📄 Archivo: {nombre_completo}\n"
            mensaje_exito += f"📁 Guardado en: {self.ruta_guardado}\n"
            mensaje_exito += f"🔗 Contenido: {link}"
            
            self.agregar_mensaje(mensaje_exito)
            
            # Preguntar si quiere abrir la carpeta
            if messagebox.askyesno("¿Abrir carpeta?", 
                                 "¿Deseas abrir la carpeta donde se guardó el archivo?"):
                self.abrir_carpeta()
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar el QR: {str(e)}")
            self.agregar_mensaje(f"❌ Error: {str(e)}")
    
    def abrir_carpeta(self):
        """Abre la carpeta donde se guardó el archivo"""
        try:
            if os.name == 'nt':  # Windows
                os.startfile(self.ruta_guardado)
            elif os.name == 'posix':  # macOS y Linux
                os.system(f'open "{self.ruta_guardado}"')  # macOS
                # Para Linux: os.system(f'xdg-open "{self.ruta_guardado}"')
        except Exception as e:
            self.agregar_mensaje(f"No se pudo abrir la carpeta: {str(e)}")
    
    def limpiar_campos(self):
        """Limpia todos los campos de entrada"""
        self.entry_link.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.text_resultado.config(state=tk.NORMAL)
        self.text_resultado.delete(1.0, tk.END)
        self.text_resultado.config(state=tk.DISABLED)
        
        # Restaurar ruta por defecto
        self.ruta_guardado = str(Path.home() / "Downloads")
        self.label_ruta.config(text=self.ruta_guardado)
    
    def agregar_mensaje(self, mensaje):
        """Agrega un mensaje al área de resultados"""
        self.text_resultado.config(state=tk.NORMAL)
        self.text_resultado.insert(tk.END, mensaje + "\n\n")
        self.text_resultado.config(state=tk.DISABLED)
        # Hacer scroll hacia abajo
        self.text_resultado.see(tk.END)

def main():
    # Crear la ventana principal
    root = tk.Tk()
    
    # Configurar ícono de la ventana - VERSIÓN CORREGIDA
    try:
        import sys
        
        # Determinar la ruta correcta del ícono
        if hasattr(sys, '_MEIPASS'):
            # Si está ejecutándose como .exe (PyInstaller)
            icon_path = os.path.join(sys._MEIPASS, 'icon.ico')
        else:
            # Si está ejecutándose como .py normal
            icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'icon.ico')
        
        # Verificar que el archivo existe antes de usarlo
        if os.path.exists(icon_path):
            root.iconbitmap(icon_path)
        else:
            # Fallback: intentar desde el directorio actual
            if os.path.exists('icon.ico'):
                root.iconbitmap('icon.ico')
    except Exception as e:
        # Si hay cualquier error, continuar sin ícono
        print(f"No se pudo cargar el ícono: {e}")
        pass
    
    # Configurar el estilo
    style = ttk.Style()
    style.theme_use('clam')  # Puedes cambiar por 'alt', 'default', 'classic'
    
    # Crear la aplicación
    app = GeneradorQR(root)
    
    # Mensaje de bienvenida
    app.agregar_mensaje("🚀 ¡Bienvenido al Generador de QR!")
    app.agregar_mensaje("📝 Instrucciones:\n" +
                       "1. Ingresa el enlace o texto que quieres convertir a QR\n" +
                       "2. Elige un nombre para tu archivo\n" +
                       "3. Selecciona dónde guardarlo (opcional)\n" +
                       "4. ¡Haz clic en 'Generar QR'!")
    
    # Iniciar la aplicación
    root.mainloop()

if __name__ == "__main__":
    main()