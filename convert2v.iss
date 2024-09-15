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

