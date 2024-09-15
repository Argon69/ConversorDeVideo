import os
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar, QMessageBox, QFileDialog, QLabel, QComboBox, QHBoxLayout, QMenuBar, QAction, QDialog, QDialogButtonBox
)
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QFont, QIcon


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Acerca de")
        self.setGeometry(300, 300, 300, 150)
        self.setWindowIcon(QIcon("icon.png"))

        layout = QVBoxLayout()
        info_label = QLabel("<h3>Conversor de Video</h3>"
                            "<p>Versión: 1.0</p>"
                            "<p>Desarrollado por Xenon Technologies</p>"
                            "<p>Contacto: xenonbusinessti@gmail.com</p>")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)

        button_box = QDialogButtonBox(QDialogButtonBox.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)

        self.setLayout(layout)


class ConvertThread(QThread):
    progress = pyqtSignal(int)
    status = pyqtSignal(str)

    def __init__(self, input_files, output_dir, conversion_type, parent=None):
        super().__init__(parent)
        self.input_files = input_files
        self.output_dir = output_dir
        self.conversion_type = conversion_type
        self.is_paused = False
        self.is_stopped = False

    def run(self):
        total_files = len(self.input_files)
        for idx, input_file_path in enumerate(self.input_files):
            if self.is_stopped:
                self.status.emit("Proceso detenido.")
                break

            while self.is_paused:
                self.msleep(100)

            file_name, _ = os.path.splitext(os.path.basename(input_file_path))
            output_file_path = self.generate_output_path(file_name)

            try:
                self.perform_conversion(input_file_path, output_file_path)
                self.progress.emit(int((idx + 1) / total_files * 100))
            except subprocess.CalledProcessError as e:
                self.status.emit(f"Error al convertir {input_file_path}: {e.stderr}")
                break
            except Exception as e:
                self.status.emit(f"Error inesperado: {str(e)}")
                break

        self.status.emit("Conversión completada.")

    def generate_output_path(self, file_name):
        extension = 'mp4' if self.conversion_type == 'webm_to_mp4' else 'webm'
        output_file_path = os.path.join(self.output_dir, f"{file_name}.{extension}")

        counter = 1
        while os.path.exists(output_file_path):
            output_file_path = os.path.join(self.output_dir, f"{file_name}_copy{counter}.{extension}")
            counter += 1

        return output_file_path

    def perform_conversion(self, input_file, output_file):
        cmd = ['ffmpeg', '-i', input_file]
        if self.conversion_type == 'webm_to_mp4':
            cmd.append(output_file)
        else:
            cmd.extend(['-c:v', 'libvpx', '-b:v', '1M', '-c:a', 'libvorbis', output_file])

        # Omitir la ventana CMD con `creationflags=subprocess.CREATE_NO_WINDOW`
        result = subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, creationflags=subprocess.CREATE_NO_WINDOW)
        if result.returncode != 0:
            raise subprocess.CalledProcessError(result.returncode, cmd, output=result.stderr)

    def pause(self):
        self.is_paused = True

    def resume(self):
        self.is_paused = False

    def stop(self):
        self.is_stopped = True


class ConverterApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.thread = None

    def initUI(self):
        self.setWindowTitle('Conversor de Video WebM y MP4')
        self.setGeometry(400, 150, 600, 350)
        self.setFixedSize(600, 350)
        self.setWindowIcon(QIcon("icon.png"))

        layout = QVBoxLayout()

        title = QLabel("Conversor de Video")
        title.setFont(QFont('Arial', 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        instructions = QLabel("Selecciona el tipo de conversión y los archivos a convertir")
        instructions.setAlignment(Qt.AlignCenter)
        layout.addWidget(instructions)

        # Configuración del tipo de conversión
        conversion_layout = QHBoxLayout()
        conversion_label = QLabel("Tipo de Conversión:")
        conversion_label.setFont(QFont('Arial', 10))
        conversion_layout.addWidget(conversion_label)

        self.conversion_type = QComboBox(self)
        self.conversion_type.addItems(["WebM a MP4", "MP4 a WebM"])
        conversion_layout.addWidget(self.conversion_type)
        layout.addLayout(conversion_layout)

        # Barra de progreso
        self.progressBar = QProgressBar(self)
        self.progressBar.setValue(0)
        layout.addWidget(self.progressBar)

        # Estado
        self.status_label = QLabel("Estado: En espera")
        self.status_label.setFont(QFont('Arial', 10))
        layout.addWidget(self.status_label)

        # Botones de selección y control
        button_layout = QHBoxLayout()
        self.selectButton = QPushButton('Seleccionar archivos o carpeta')
        self.selectButton.clicked.connect(self.select_files_or_folder)
        button_layout.addWidget(self.selectButton)

        self.startButton = QPushButton('Iniciar Conversión')
        self.startButton.clicked.connect(self.start_conversion)
        button_layout.addWidget(self.startButton)
        layout.addLayout(button_layout)

        control_layout = QHBoxLayout()
        self.pauseButton = QPushButton('Pausar')
        self.pauseButton.clicked.connect(self.pause_conversion)
        self.pauseButton.setEnabled(False)
        control_layout.addWidget(self.pauseButton)

        self.resumeButton = QPushButton('Reanudar')
        self.resumeButton.clicked.connect(self.resume_conversion)
        self.resumeButton.setEnabled(False)
        control_layout.addWidget(self.resumeButton)

        self.stopButton = QPushButton('Detener')
        self.stopButton.clicked.connect(self.stop_conversion)
        self.stopButton.setEnabled(False)
        control_layout.addWidget(self.stopButton)

        layout.addLayout(control_layout)
        self.setLayout(layout)

        # Menú de Acerca de
        self.menuBar = QMenuBar(self)
        about_action = QAction('Acerca de', self)
        about_action.triggered.connect(self.show_about_dialog)
        self.menuBar.addAction(about_action)
        layout.setMenuBar(self.menuBar)

    def select_files_or_folder(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Seleccionar archivos", "", "Archivos de video (*.webm *.mp4);;Todos los archivos (*)")

        if not files:
            folder = QFileDialog.getExistingDirectory(self, "Seleccionar directorio de entrada")
            if folder:
                files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith(('.webm', '.mp4'))]

        if files:
            output_dir = QFileDialog.getExistingDirectory(self, "Seleccionar directorio de salida")
            if output_dir:
                self.input_files = files
                self.output_dir = output_dir
            else:
                QMessageBox.warning(self, "Error", "No se seleccionó un directorio de salida.")
        else:
            QMessageBox.warning(self, "Error", "No se seleccionaron archivos.")

    def start_conversion(self):
        if not hasattr(self, 'input_files') or not hasattr(self, 'output_dir'):
            QMessageBox.warning(self, "Error", "Por favor, seleccione archivos y directorio de salida.")
            return

        conversion_type = 'webm_to_mp4' if self.conversion_type.currentText() == "WebM a MP4" else 'mp4_to_webm'
        self.thread = ConvertThread(self.input_files, self.output_dir, conversion_type)
        self.thread.progress.connect(self.update_progress)
        self.thread.status.connect(self.update_status)
        self.thread.start()

        self.pauseButton.setEnabled(True)
        self.resumeButton.setEnabled(True)
        self.stopButton.setEnabled(True)

    def update_progress(self, value):
        self.progressBar.setValue(value)

    def update_status(self, status):
        self.status_label.setText(f"Estado: {status}")
        if status == "Conversión completada.":
            self.pauseButton.setEnabled(False)
            self.resumeButton.setEnabled(False)
            self.stopButton.setEnabled(False)

    def pause_conversion(self):
        if self.thread:
            self.thread.pause()

    def resume_conversion(self):
        if self.thread:
            self.thread.resume()

    def stop_conversion(self):
        if self.thread:
            self.thread.stop()

    def show_about_dialog(self):
        about_dialog = AboutDialog(self)
        about_dialog.exec_()


if __name__ == "__main__":
    app = QApplication([])
    window = ConverterApp()
    window.show()
    app.exec_()
