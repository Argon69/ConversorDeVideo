```markdown
# Conversor de Video

**Conversor de Video** es una aplicación de escritorio para convertir archivos de video entre formatos WebM y MP4. Desarrollada en Python con PyQt5, esta aplicación proporciona una interfaz gráfica amigable para seleccionar archivos, configurar conversiones y gestionar el proceso de conversión.

## Requisitos

- **Python 3.x**: Asegúrate de tener Python instalado en tu sistema.
- **PyQt5**: Biblioteca para crear interfaces gráficas en Python.
- **FFmpeg**: Herramienta de línea de comandos para la conversión de video.

## Instalación

### 1. Clonar el Repositorio

Primero, clona el repositorio donde se encuentra el código fuente del proyecto:

```bash
git clone <URL_DEL_REPOSITORIO>
cd <NOMBRE_DEL_REPOSITORIO>
```

### 2. Configurar el Entorno

Instala las dependencias necesarias usando `pip`:

```bash
pip install pyqt5
```

Asegúrate también de tener [FFmpeg](https://ffmpeg.org/download.html) instalado y accesible desde la línea de comandos.

### 3. Crear el Ejecutable

Utiliza PyInstaller para convertir el script Python en un ejecutable. Asegúrate de tener PyInstaller instalado:

```bash
pip install pyinstaller
```

Luego, crea el ejecutable:

```bash
pyinstaller --onefile --icon=<RUTA_DEL_ICONO> <NOMBRE_DEL_ARCHIVO>.py
```

Esto generará un archivo ejecutable en la carpeta `dist`.

### 4. Crear el Instalador para Windows con Inno Setup

1. **Instala Inno Setup**: Descarga e instala [Inno Setup](https://jrsoftware.org/isinfo.php).

2. **Configura el Script de Instalación**: Usa el siguiente script de Inno Setup para crear el instalador:

   ```ini
   [Setup]
   AppName=Conversor de Video
   AppVersion=1.0
   AppPublisher=Xenon Technologies
   AppPublisherURL=https://xenontechec.netlify.app/
   DefaultDirName={pf}\ConversorDeVideo
   DefaultGroupName=ConversorDeVideo
   OutputBaseFilename=InstaladorConversorDeVideo
   Compression=lzma
   SolidCompression=yes
   PrivilegesRequired=admin
   DisableProgramGroupPage=yes
   UninstallDisplayIcon={app}\favicon.ico
   SetupIconFile=C:\Users\nixon\Documents\validador\nuevo\favicon.ico
   WizardStyle=modern

   [Files]
   ; Incluir el ejecutable generado por PyInstaller
   Source: "C:\Users\nixon\Documents\validador\nuevo\dist\ConversorDeVideo.exe"; DestDir: "{app}"; Flags: ignoreversion

   ; Incluir solo el archivo esencial de FFmpeg
   Source: "C:\Users\nixon\Documents\validador\nuevo\ffmpeg-master-latest-win64-gpl\bin\ffmpeg.exe"; DestDir: "{app}\ffmpeg\bin"; Flags: ignoreversion

   ; Incluir el archivo del icono
   Source: "C:\Users\nixon\Documents\validador\nuevo\favicon.ico"; DestDir: "{app}"; Flags: ignoreversion

   [Run]
   ; Ejecutar tu aplicación después de la instalación sin abrir CMD
   Filename: "{app}\ConversorDeVideo.exe"; Description: "Iniciar Conversor de Video"; Flags: nowait postinstall skipifsilent

   [Icons]
   ; Crear accesos directos en el menú de inicio y en el escritorio con el icono personalizado
   Name: "{autoprograms}\Conversor de Video"; Filename: "{app}\ConversorDeVideo.exe"; IconFilename: "{app}\favicon.ico"
   Name: "{userdesktop}\Conversor de Video"; Filename: "{app}\ConversorDeVideo.exe"; IconFilename: "{app}\favicon.ico"; Tasks: desktopicon

   [Registry]
   ; Agregar FFmpeg al PATH del sistema para que se pueda usar globalmente
   Root: HKLM; Subkey: "SYSTEM\CurrentControlSet\Control\Session Manager\Environment"; ValueType: expandsz; ValueName: "Path"; ValueData: "{app}\ffmpeg\bin"; Flags: preservestringtype

   [Tasks]
   ; Opción para crear icono en el escritorio
   Name: "desktopicon"; Description: "Crear un icono en el escritorio"; GroupDescription: "Tareas adicionales:"; Flags: unchecked

   [Messages]
   SetupWindowTitle=Instalación del Conversor de Video
   SetupAppTitle=Conversor de Video
   ```

   Guarda este script con una extensión `.iss` (por ejemplo, `setup.iss`).

3. **Compila el Instalador**: Abre el script `.iss` en Inno Setup y compílalo para generar el archivo de instalación.

## Uso

1. **Ejecuta el Instalador**: Doble clic en el archivo `.exe` generado para iniciar el proceso de instalación.

2. **Inicia la Aplicación**: Después de la instalación, puedes iniciar la aplicación desde el menú de inicio o desde el escritorio si seleccionaste la opción correspondiente durante la instalación.

3. **Configura y Usa la Aplicación**: Sigue las instrucciones en la interfaz gráfica para seleccionar archivos, configurar el tipo de conversión, y gestionar el proceso.

## Contribuciones

Las contribuciones al proyecto son bienvenidas. Para contribuir:

1. Realiza un fork del repositorio.
2. Realiza tus cambios y prueba la aplicación.
3. Envía un pull request con una descripción de tus cambios.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

## Contacto

Para consultas o soporte, puedes contactar a los desarrolladores en xenonbusinessti@gmail.com.

## Captura de Pantalla

![Captura de Pantalla](captura.png)
```

Asegúrate de reemplazar las rutas en el script de Inno Setup con las correctas en tu sistema, y ajustar cualquier otro detalle según tus necesidades específicas.
