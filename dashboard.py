import tkinter as tk
from tkinter import filedialog, messagebox
import psutil
import platform
import os
from datetime import datetime

# IDENTIDADE VISUAL
BG = "#090909"
CARD = "#171717"
RED = "#ef3038"
WHITE = "#ffffff"
GRAY = "#a3a3a3"
GREEN = "#4ade80"

# JANELA PRINCIPAL
app = tk.Tk()
app.title("Wolf System Diagnostic PRO V3.0")
app.geometry("850x650")
app.configure(bg=BG)

# CABECALHO
header = tk.Frame(app, bg=BG)
header.pack(fill="x", padx=25, pady=15)

logo = tk.Canvas(
    header, width=65, height=65,
    bg=BG, highlightthickness=0
)
logo.pack(side="left", padx=(0, 15))

# LOGOTIPO GEOMETRICO DO LOBO
logo.create_polygon(
    5, 3, 23, 17, 42, 17, 60, 3,
    55, 37, 43, 51, 32, 62,
    21, 51, 10, 37,
    fill=RED, outline=RED
)

logo.create_polygon(
    14, 15, 27, 28, 38, 28, 51, 15,
    46, 39, 32, 54, 19, 39,
    fill=BG
)

logo.create_polygon(
    17, 29, 29, 34, 23, 38,
    fill=RED
)

logo.create_polygon(
    47, 29, 35, 34, 41, 38,
    fill=RED
)

title_frame = tk.Frame(header, bg=BG)
title_frame.pack(side="left")

tk.Label(
    title_frame,
    text="WOLF SYSTEM",
    font=("Segoe UI", 26, "bold"),
    bg=BG, fg=WHITE
).pack(anchor="w")

tk.Label(
    title_frame,
    text="DIAGNOSTIC PRO | VERSION 3.0",
    font=("Segoe UI", 11, "bold"),
    bg=BG, fg=RED
).pack(anchor="w")

tk.Frame(app, bg=RED, height=2).pack(
    fill="x", padx=25
)

# INDICADORES CIRCULARES
painel = tk.Frame(app, bg=BG)
painel.pack(fill="x", padx=20, pady=12)

def criar_indicador(nome):
    card = tk.Frame(painel, bg=CARD)
    card.pack(
        side="left", expand=True,
        fill="both", padx=5
    )

    tk.Label(
        card, text=nome,
        font=("Segoe UI", 11, "bold"),
        bg=CARD, fg=GRAY
    ).pack(pady=(10, 0))

    canvas = tk.Canvas(
        card, width=145, height=145,
        bg=CARD, highlightthickness=0
    )
    canvas.pack()

    canvas.create_oval(
        15, 15, 130, 130,
        outline="#333333", width=10
    )

    arco = canvas.create_arc(
        15, 15, 130, 130,
        start=90, extent=0,
        style="arc", outline=RED,
        width=10
    )

    texto = canvas.create_text(
        72, 72, text="0%",
        fill=WHITE,
        font=("Segoe UI", 20, "bold")
    )

    return canvas, arco, texto

cpu_card = criar_indicador("PROCESSADOR")
ram_card = criar_indicador("MEMORIA RAM")
disk_card = criar_indicador("ARMAZENAMENTO")

# INFORMACOES DO SISTEMA
info = tk.Frame(app, bg=CARD)
info.pack(fill="x", padx=25, pady=5)

tk.Label(
    info,
    text="INFORMACOES DO SISTEMA",
    font=("Segoe UI", 13, "bold"),
    bg=CARD, fg=RED
).pack(anchor="w", padx=15, pady=8)

dados = tk.Label(
    info,
    text="Coletando informacoes...",
    font=("Segoe UI", 10),
    justify="left",
    anchor="w",
    bg=CARD, fg=WHITE
)
dados.pack(fill="x", padx=15, pady=(0, 12))

# STATUS DO SISTEMA
status = tk.Label(
    app,
    text="MONITORAMENTO ATIVO",
    bg=BG, fg=GREEN,
    font=("Segoe UI", 11, "bold")
)
status.pack(pady=8)

unidade = os.environ.get("SystemDrive", "C:") + "\\"

ultimo_relatorio = ""

# ATUALIZAR INDICADORES
def atualizar_indicador(card, valor):
    canvas, arco, texto = card

    canvas.itemconfig(
        arco, extent=-(valor * 3.6)
    )

    canvas.itemconfig(
        texto, text=f"{valor:.1f}%"
    )

# COLETAR DADOS
def atualizar():
    global ultimo_relatorio

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory()
    disco = psutil.disk_usage(unidade)

    atualizar_indicador(cpu_card, cpu)
    atualizar_indicador(ram_card, ram.percent)
    atualizar_indicador(disk_card, disco.percent)

    sistema = (
        f"Sistema: {platform.system()} {platform.release()}\n"
        f"Arquitetura: {platform.machine()}\n"
        f"Nucleos fisicos: {psutil.cpu_count(logical=False)}"
        f" | Logicos: {psutil.cpu_count()}\n"
        f"RAM total: {ram.total / 1024**3:.2f} GiB"
        f" | Disponivel: {ram.available / 1024**3:.2f} GiB\n"
        f"Disco total: {disco.total / 1024**3:.2f} GiB"
        f" | Livre: {disco.free / 1024**3:.2f} GiB"
    )

    dados.config(text=sistema)

    alertas = []

    if cpu >= 90:
        alertas.append("CPU elevada")

    if ram.percent >= 85:
        alertas.append("RAM elevada")

    if disco.percent >= 90:
        alertas.append("Disco quase cheio")

    if alertas:
        mensagem = "ALERTA: " + " | ".join(alertas)
        status.config(text=mensagem, fg=RED)
    else:
        mensagem = "UTILIZACAO DENTRO DOS LIMITES"
        status.config(text=mensagem, fg=GREEN)

    ultimo_relatorio = (
        "WOLF SYSTEM DIAGNOSTIC PRO V3.0\n"
        "====================================\n"
        f"Data: {datetime.now():%d/%m/%Y %H:%M:%S}\n\n"
        + sistema +
        f"\n\nUso da CPU: {cpu:.1f}%"
        f"\nUso da RAM: {ram.percent:.1f}%"
        f"\nOcupacao do disco: {disco.percent:.1f}%"
        f"\n\nStatus: {mensagem}\n"
        "\nDesenvolvido por Silas de Paula Cesario"
    )

# MONITORAMENTO AUTOMATICO
def monitorar():
    atualizar()
    app.after(1000, monitorar)

# EXPORTAR RELATORIO TXT
def exportar():
    arquivo = filedialog.asksaveasfilename(
        defaultextension=".txt",
        initialfile="wolf-diagnostic.txt",
        filetypes=[("Relatorio TXT", "*.txt")]
    )

    if arquivo:
        try:
            with open(arquivo, "w", encoding="utf-8") as f:
                f.write(ultimo_relatorio)

            messagebox.showinfo(
                "Wolf Diagnostic",
                "Relatorio exportado com sucesso!"
            )

        except OSError as erro:
            messagebox.showerror(
                "Erro", str(erro)
            )

# BOTOES
botoes = tk.Frame(app, bg=BG)
botoes.pack(pady=10)

tk.Button(
    botoes,
    text="EXPORTAR RELATORIO",
    command=exportar,
    bg="#b91c1c", fg=WHITE,
    activebackground=RED,
    activeforeground=WHITE,
    font=("Segoe UI", 11, "bold"),
    relief="flat", cursor="hand2",
    padx=20, pady=10
).pack(side="left", padx=7)

tk.Button(
    botoes,
    text="ATUALIZAR",
    command=atualizar,
    bg="#262626", fg=WHITE,
    activebackground="#404040",
    activeforeground=WHITE,
    font=("Segoe UI", 11, "bold"),
    relief="flat", cursor="hand2",
    padx=20, pady=10
).pack(side="left", padx=7)

# RODAPE
tk.Label(
    app,
    text="Silas de Paula Cesario | SP.DEV",
    bg=BG, fg=GRAY,
    font=("Segoe UI", 9)
).pack(pady=(5, 0))

tk.Label(
    app,
    text="WOLF TECHNOLOGY",
    bg=BG, fg=RED,
    font=("Segoe UI", 9, "bold")
).pack()

psutil.cpu_percent()
monitorar()
app.mainloop()
