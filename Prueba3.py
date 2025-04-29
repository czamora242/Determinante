from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import (
    QMainWindow, QTableWidgetItem, QTextEdit, QVBoxLayout, QLabel, QPushButton,
    QTableWidget, QComboBox, QLineEdit, QWidget
)
import sys


class CalculadoraDeterminantes(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Calculadora de Determinantes")
        self.setGeometry(100, 100, 1000, 800)
        self.initUI()

    def initUI(self):
        # Estilo general
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f0f8ff;
            }
            QLabel {
                font-size: 16px;
                color: #333;
            }
            QLineEdit {
                font-size: 16px;
                padding: 5px;
                border: 2px solid #4682b4;
                border-radius: 5px;
            }
            QPushButton {
                font-size: 16px;
                background-color: #4682b4;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #5a9bd3;
            }
            QTableWidget {
                font-size: 14px;
                gridline-color: #4682b4;
                selection-background-color: #add8e6;
            }
            QComboBox {
                font-size: 16px;
                padding: 5px;
            }
            QTextEdit {
                font-size: 14px;
                background-color: #ffffff;
                border: 2px solid #4682b4;
                border-radius: 5px;
                padding: 10px;
            }
        """)

        # Layout principal
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Título de la aplicación
        titulo = QLabel("Calculadora de Determinantes")
        titulo.setAlignment(QtCore.Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #4682b4;")
        main_layout.addWidget(titulo)

        # Entrada para el orden de la matriz
        self.orden_label = QLabel("Introduce el orden de la matriz:")
        main_layout.addWidget(self.orden_label)

        self.entry_orden = QLineEdit()
        self.entry_orden.setPlaceholderText("Ejemplo: 3")
        main_layout.addWidget(self.entry_orden)

        # Botón para generar la matriz
        self.generar_btn = QPushButton("Generar matriz")
        self.generar_btn.clicked.connect(self.generar_matriz)
        main_layout.addWidget(self.generar_btn)

        # Tabla para la matriz
        self.matriz_table = QTableWidget()
        main_layout.addWidget(self.matriz_table)

        # Selección de método
        self.metodo_combo = QComboBox()
        self.metodo_combo.addItems(["Cofactor", "Gauss"])
        main_layout.addWidget(QLabel("Selecciona el método:"))
        main_layout.addWidget(self.metodo_combo)

        # Botón para calcular el determinante
        self.calcular_btn = QPushButton("Calcular Determinante")
        self.calcular_btn.clicked.connect(self.calcular_determinante)
        main_layout.addWidget(self.calcular_btn)

        # Área de texto para mostrar pasos
        self.pasos_text = QTextEdit()
        self.pasos_text.setReadOnly(True)
        main_layout.addWidget(QLabel("Pasos:"))
        main_layout.addWidget(self.pasos_text)

    def generar_matriz(self):
        try:
            n = int(self.entry_orden.text())
            if n <= 0:
                raise ValueError("El orden de la matriz debe ser mayor a 0.")
            self.matriz_table.setRowCount(n)
            self.matriz_table.setColumnCount(n)
            for i in range(n):
                for j in range(n):
                    self.matriz_table.setItem(i, j, QTableWidgetItem(""))
            self.pasos_text.append(f"Matriz de orden {n} generada correctamente.")
        except ValueError:
            self.pasos_text.append("Error: Introduce un valor entero positivo para el orden de la matriz.")

    def leer_matriz(self):
        try:
            n = self.matriz_table.rowCount()
            matriz = []
            for i in range(n):
                fila = []
                for j in range(n):
                    valor = self.matriz_table.item(i, j)
                    if valor and valor.text().strip():
                        fila.append(float(valor.text()))
                    else:
                        fila.append(0.0)
                matriz.append(fila)
            return matriz
        except Exception as e:
            self.pasos_text.append(f"Error al leer la matriz: {e}")
            return []

    def calcular_determinante(self):
        matriz = self.leer_matriz()
        if not matriz:
            self.pasos_text.append("Error: No se pudo leer la matriz.")
            return

        metodo = self.metodo_combo.currentText()
        self.pasos_text.clear()

        try:
            if metodo == "Cofactor":
                self.pasos_text.append("Método: Cofactor\n")
                resultado = self.determinante_cofactor(matriz)
            elif metodo == "Gauss":
                self.pasos_text.append("Método: Gauss\n")
                resultado = self.determinante_gauss(matriz)
            else:
                self.pasos_text.append("Error: Método no válido.")
                return

            self.pasos_text.append(f"\nResultado final: {resultado}")
        except Exception as e:
            self.pasos_text.append(f"Error durante el cálculo: {e}")

    def determinante_cofactor(self, matriz):
        n = len(matriz)
        if n == 1:
            self.pasos_text.append(f"Determinante de matriz 1x1: {matriz[0][0]}")
            return matriz[0][0]

        determinante = 0
        self.pasos_text.append("Matriz inicial:")
        for fila in matriz:
            self.pasos_text.append(str(fila))

        for j in range(n):
            submatriz = [fila[:j] + fila[j+1:] for fila in matriz[1:]]
            self.pasos_text.append(f"\nEliminamos fila 0 y columna {j} para formar la submatriz:")
            for fila in submatriz:
                self.pasos_text.append(str(fila))

            sub_det = self.determinante_cofactor(submatriz)
            signo = (-1)**j
            cofactor = signo * matriz[0][j] * sub_det
            self.pasos_text.append(f"(-1)^{j} × {matriz[0][j]} × {sub_det} = {cofactor}")
            determinante += cofactor

        return determinante

    def determinante_gauss(self, matriz):
        n = len(matriz)
        det = 1
        self.pasos_text.append("Matriz inicial:")
        for fila in matriz:
            self.pasos_text.append(str(fila))

        while n > 2:
            pivote_fila = next((i for i in range(n) if matriz[i][0] in [1, -1]), -1)
            if pivote_fila == -1:
                pivote_fila = max(range(n), key=lambda x: abs(matriz[x][0]))

            matriz[0], matriz[pivote_fila] = matriz[pivote_fila], matriz[0]
            self.pasos_text.append(f"\nIntercambio de filas 0 y {pivote_fila}:")
            for fila in matriz:
                self.pasos_text.append(str(fila))

            pivote = matriz[0][0]
            det *= pivote
            self.pasos_text.append(f"\nNormalizamos fila 0 dividiendo por el pivote {pivote}:")
            for j in range(n):
                matriz[0][j] /= pivote
            for fila in matriz:
                self.pasos_text.append(str(fila))

            for i in range(1, n):
                factor = matriz[i][0]
                self.pasos_text.append(f"\nEliminando valor en columna 0 de fila {i} usando factor {factor}:")
                for j in range(n):
                    matriz[i][j] -= factor * matriz[0][j]
                for fila in matriz:
                    self.pasos_text.append(str(fila))

            matriz = [fila[1:] for fila in matriz[1:]]
            n -= 1

        self.pasos_text.append("\nMatriz reducida a 2x2:")
        for fila in matriz:
            self.pasos_text.append(str(fila))

            a, b = matriz[0][0], matriz[0][1]
            c, d = matriz[1][0], matriz[1][1]
            det_final = a * d - b * c
            det *= det_final
            self.pasos_text.append(f"\nDeterminante de matriz 2x2: ({a} * {d}) - ({b} * {c}) = {det_final}")
            self.pasos_text.append(f"\nResultado acumulado: {det}")
        return det

        # Ejecución de la aplicación
def main():
    app = QtWidgets.QApplication(sys.argv)
    ventana = CalculadoraDeterminantes()
    ventana.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
