import tkinter as tk
from tkinter import ttk, messagebox
import yfinance as yf
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


def calcular_mayer(ticker):
    """Baixa os dados e calcula a média móvel de 200 dias + múltiplo."""
    try:
        dados = yf.download(ticker, period="1y")
        dados = dados.sort_index()

        # Calcula MM200
        dados["MM200"] = dados["Close"].rolling(window=200).mean()

        preco_atual = float(dados["Close"].iloc[-1])
        mm200 = float(dados["MM200"].iloc[-1])

        if mm200 == 0 or mm200 != mm200:
            return None, None, None, dados

        mayer = preco_atual / mm200
        return preco_atual, mm200, mayer, dados

    except Exception as e:
        messagebox.showerror("Erro", f"Falha ao obter dados: {e}")
        return None, None, None, None


def exibir_grafico(dados, ticker):
    plt.style.use("dark_background")
    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(dados.index, dados["Close"], label="Preço", linewidth=1.5)
    ax.plot(dados.index, dados["MM200"], label="Média Móvel 200d", linestyle="--", linewidth=1.5)
    ax.set_title(f"Preço e MM200 - {ticker}", fontsize=12, fontweight="bold")
    ax.legend()
    ax.grid(True, linestyle="--", alpha=0.5)

    canvas = FigureCanvasTkAgg(fig, master=frame_grafico)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=5, pady=5)



def calcular():
    ativo = combo_ativo.get()
    if ativo == "Bitcoin (BTC-USD)":
        ticker = "BTC-USD"
    elif ativo == "IVVB11 (ETF)":
        ticker = "IVVB11.SA"
    else:
        messagebox.showwarning("Atenção", "Selecione um ativo válido.")
        return

    for widget in frame_grafico.winfo_children():
        widget.destroy() #Limpar o gráfico anterior

    preco, mm200, mayer, dados = calcular_mayer(ticker)
    if preco is None or dados is None:
        return

    texto_resultado.set(
        f"{ativo}\n"
        f"Preço atual: R$ {preco:,.2f}\n"
        f"Média móvel (200 dias): R$ {mm200:,.2f}\n"
        f"Múltiplo de Mayer: {mayer:.2f}\n\n"
    )

    exibir_grafico(dados, ticker)


# Interface principal 
janela = tk.Tk()
janela.title("📈 Múltiplo de Mayer - Bitcoin & IVVB11")
janela.geometry("800x600")
janela.resizable(True, True)

# Título
titulo = tk.Label(janela, text="Múltiplo de Mayer", font=("Lato", 16, "bold"))
titulo.pack(pady=10)

# Seleção de ativo
frame_top = tk.Frame(janela)
frame_top.pack(pady=10)

tk.Label(frame_top, text="Selecione o ativo:", font=("Open Sans", 12)).grid(row=0, column=0, padx=10)

combo_ativo = ttk.Combobox(frame_top, values=["Bitcoin (BTC-USD)", "IVVB11 (ETF)"], state="readonly", width=25)
combo_ativo.grid(row=0, column=1)
combo_ativo.set("Selecione...")

btn_calcular = ttk.Button(frame_top, text="Calcular", command=calcular)
btn_calcular.grid(row=0, column=2, padx=10)

# Resultado do cálculo
texto_resultado = tk.StringVar()
label_resultado = tk.Label(janela, textvariable=texto_resultado, font=("Open Sans", 12), justify="left")
label_resultado.pack(pady=15)

# Frame do gráfico
frame_grafico = tk.Frame(janela, bg="white", relief="sunken", borderwidth=1)
frame_grafico.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)

# Rodapé
tk.Label(janela, text="⚙️ Desenvolvido por Nicolas Tavares", font=("Open Sans", 9)).pack(side="bottom", pady=5)

janela.mainloop()

def on_resize(event):
    for widget in frame_grafico.winfo_children():
        if isinstance(widget, FigureCanvasTkAgg):
            widget.draw()

janela.bind("<Configure>", on_resize)

