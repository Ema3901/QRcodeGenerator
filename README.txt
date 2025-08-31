Una aplicación de escritorio simple y elegante para generar códigos QR personalizados usando Python y Tkinter.

Instalación y uso
Opción 1: Ejecutar desde código fuente

Clona el repositorio:
bashgit clone https://github.com/tu-usuario/generador-qr.git
cd generador-qr

Instala las dependencias:
bashpip install qrcode[pil]

Ejecuta la aplicación:
bashpython generador_qr.py


Opción 2: Crear ejecutable (.exe)

Instala PyInstaller:
bashpip install pyinstaller

Instala las dependencias necesarias:
bashpip install qrcode[pil]

Genera el ejecutable:
bashpyinstaller --onefile --windowed --icon=icon.ico --add-data "icon.ico;." --name="Generador QR" generador_qr.py

Encuentra tu ejecutable:

El archivo .exe estará en la carpeta dist/
¡Ya puedes compartirlo sin necesidad de instalar Python!


Créditos
Ícono: Creado por Chehuna en Flaticon
Librería QR: Generación de códigos QR usando la librería qrcode
