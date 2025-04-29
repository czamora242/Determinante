import tkinter as tk
from tkinter import messagebox

def calcular_determinante():
    try:
        n = int(entry_orden.get())
        matriz = []
        for i in range(n):
            fila = []
            for j in range(n):
                valor = matriz_entries[i][j].get()
                fila.append(float(valor))
            matriz.append(fila)

        metodo = metodo_var.get()
        pasos_text.delete("1.0", tk.END)  # Limpiar el cuadro de texto
        if metodo == "Cofactor":
            pasos_text.insert(tk.END, "Método: Cofactor\n", "step")
            resultado = determinante_cofactor(matriz)
        elif metodo == "Gauss":
            pasos_text.insert(tk.END, "Método: Gauss\n", "step")
            resultado = determinante_gauss([fila[:] for fila in matriz])  # Copia de la matriz
        else:
            raise ValueError("Método no seleccionado.")

        pasos_text.insert(tk.END, f"\nResultado final: {resultado}\n", "result")
    except Exception as e:
        messagebox.showerror("Error", f"Error al calcular: {e}")

def generar_matriz():
    try:
        n = int(entry_orden.get())
        for widget in matriz_frame.winfo_children():
            widget.destroy()

        matriz_entries.clear()
        for i in range(n):
            fila_entries = []
            for j in range(n):
                entry = tk.Entry(matriz_frame, width=5, font=("Arial", 12))
                entry.grid(row=i, column=j, padx=5, pady=5)
                fila_entries.append(entry)
            matriz_entries.append(fila_entries)

        tk.Label(ventana, text="Selecciona el método:", font=("Arial", 12, "bold"), fg="blue").pack(pady=5)
        metodo_var.set("Cofactor")
        metodo_menu = tk.OptionMenu(ventana, metodo_var, "Cofactor", "Gauss")
        metodo_menu.config(font=("Arial", 12), bg="lightgrey", activebackground="lightblue")
        metodo_menu.pack(pady=5)

        calcular_btn = tk.Button(ventana, text="Calcular Determinante", command=calcular_determinante, bg="#4caf50", fg="white", font=("Arial", 12, "bold"))
        calcular_btn.pack(pady=10)
    except Exception as e:
        messagebox.showerror("Error", f"Error al generar la matriz: {e}")


def determinante_cofactor(matriz):
    n = len(matriz)
    if n == 1:
        pasos_text.insert(tk.END, f"Determinante de matriz 1x1: {matriz[0][0]}\n", "result")
        return matriz[0][0]

    determinante = 0
    pasos_text.insert(tk.END, "Matriz inicial:\n", "step")
    for fila in matriz:
        pasos_text.insert(tk.END, f"{fila}\n", "step")

    pasos_text.insert(tk.END, f"Calculando determinante por el método de cofactor:\n", "step")

    for j in range(n):
        # Mostrar el elemento seleccionado como pivote
        pasos_text.insert(tk.END, f"\nSeleccionamos el elemento en posición (0,{j}): {matriz[0][j]}\n", "step")

        # Crear la submatriz al eliminar la fila 0 y columna j
        submatriz = [fila[:j] + fila[j + 1:] for fila in matriz[1:]]
        pasos_text.insert(tk.END, "Submatriz generada eliminando fila 0 y columna {j}:\n", "step")
        for fila in submatriz:
            pasos_text.insert(tk.END, f"{fila}\n", "step")

        # Calcular el determinante de la submatriz
        sub_det = determinante_cofactor(submatriz)

        # Mostrar cálculo intermedio de la submatriz
        pasos_text.insert(tk.END, f"Determinante de la submatriz: {sub_det}\n", "step")

        # Calcular el cofactor y agregarlo al acumulado
        signo = (-1) ** j
        cofactor = signo * matriz[0][j] * sub_det
        pasos_text.insert(tk.END, f"(-1)^{j} × {matriz[0][j]} × {sub_det} = {cofactor}\n", "step")
        determinante += cofactor
        pasos_text.insert(tk.END, f"Determinante acumulado: {determinante}\n", "step")

    pasos_text.insert(tk.END, f"\nDeterminante final: {determinante}\n", "result")
    return determinante
def determinante_gauss(matriz):
    n = len(matriz)
    det = 1  # Inicializamos el determinante

    pasos_text.insert(tk.END, "Matriz inicial:\n", "step")
    for fila in matriz:
        pasos_text.insert(tk.END, f"{fila}\n", "step")

    while n > 2:  # Seguimos reduciendo hasta que la matriz sea 2x2
        # Buscar el mejor pivote (idealmente 1 o -1) en la columna actual
        pivote_fila = -1
        for i in range(n):
            if matriz[i][0] == 1 or matriz[i][0] == -1:
                pivote_fila = i
                break
        if pivote_fila == -1:  # Si no encontramos 1 o -1, seleccionamos el mayor valor absoluto
            pivote_fila = max(range(n), key=lambda x: abs(matriz[x][0]))

        # Intercambiar filas si el pivote no está en la primera fila
        if pivote_fila != 0:
            matriz[0], matriz[pivote_fila] = matriz[pivote_fila], matriz[0]
            det *= -1  # Cambiar el signo del determinante por el intercambio
            pasos_text.insert(tk.END, f"\n(-1) × Determinante actual después del intercambio:\n")
            for fila in matriz:
                pasos_text.insert(tk.END, f"{fila}\n")

        # Normalizamos la fila del pivote para que el valor del pivote sea 1
        pivote = matriz[0][0]
        det *= pivote
        pasos_text.insert(tk.END, f"\n({pivote}) × Determinante después de normalizar fila 0:\n")
        for j in range(n):
            matriz[0][j] /= pivote
        pasos_text.insert(tk.END, "Matriz después de normalizar:\n")
        for fila in matriz:
            pasos_text.insert(tk.END, f"{fila}\n")

        # Realizar operaciones elementales para anular los elementos en la columna debajo del pivote
        for i in range(1, n):
            factor = matriz[i][0]
            pasos_text.insert(tk.END, f"\nMultiplicando por el factor {factor} para eliminar fila {i}:\n")
            for j in range(n):
                matriz[i][j] -= factor * matriz[0][j]
            pasos_text.insert(tk.END, "Matriz después de la eliminación:\n")
            for fila in matriz:
                pasos_text.insert(tk.END, f"{fila}\n")

        # Eliminar la primera fila y columna después de trabajar con el pivote
        matriz = [fila[1:] for fila in matriz[1:]]
        n -= 1
        pasos_text.insert(tk.END, f"\nMatriz después de eliminar primera fila y columna:\n")
        for fila in matriz:
            pasos_text.insert(tk.END, f"{fila}\n")

    # Calcular el determinante de la matriz 2x2 resultante
    pasos_text.insert(tk.END, "\nMatriz reducida a 2x2:\n")
    for fila in matriz:
        pasos_text.insert(tk.END, f"{fila}\n")

    a, b = matriz[0][0], matriz[0][1]
    c, d = matriz[1][0], matriz[1][1]
    det_final = a * d - b * c
    pasos_text.insert(tk.END, f"\nDeterminante de la matriz 2x2: ({a} * {d}) - ({b} * {c}) = {det_final}\n")
    det *= det_final

    # *** SOLUCIÓN ***
    # Retornamos el valor calculado
    return det

# Interfaz gráfica mejorada
ventana = tk.Tk()
ventana.title("Calculadora de Determinantes")
ventana.geometry("800x800")
ventana.config(bg="#f0f8ff")

header = tk.Label(ventana, text="Calculadora de Determinantes", font=("Arial", 18, "bold"), fg="white", bg="#4682b4", pady=10)
header.pack(fill=tk.X)

tk.Label(ventana, text="Introduce el orden de la matriz:", font=("Arial", 12), fg="black").pack(pady=5)
entry_orden = tk.Entry(ventana, font=("Arial", 12), width=10)
entry_orden.pack(pady=5)

generar_btn = tk.Button(ventana, text="Generar matriz vacía", command=generar_matriz, bg="#007bff", fg="white", font=("Arial", 12, "bold"))
generar_btn.pack(pady=10)

matriz_frame = tk.Frame(ventana, bg="#f0f8ff")
matriz_frame.pack(pady=10)
matriz_entries = []

metodo_var = tk.StringVar()

pasos_text = tk.Text(ventana, height=15, width=70, font=("Arial", 12), bg="#e6f7ff", fg="black", wrap=tk.WORD)
pasos_text.tag_config("step", foreground="blue")
pasos_text.tag_config("result", foreground="green", font=("Arial", 12, "bold"))
pasos_text.pack(pady=10)

ventana.mainloop()