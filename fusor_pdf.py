import os
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
from PyPDF2 import PdfMerger

# Função para iniciar o processo de listagem e mesclagem
def iniciar():
    global pdfs, pasta
    pasta = pasta_entry.get()

    if not os.path.isdir(pasta):
        messagebox.showerror("Erro", "Pasta inválida!")
        return

    arquivos = os.listdir(pasta)
    pdfs = sorted([arquivo for arquivo in arquivos if arquivo.endswith('.pdf')])

    if not pdfs:
        messagebox.showinfo("Nenhum PDF", "Nenhum arquivo PDF foi encontrado.")
        return

    imprimir_lista(pdfs)
    pergunta_ordem()

# Função para imprimir a lista de PDFs na interface
def imprimir_lista(pdfs):
    lista_pdf.delete(0, tk.END)
    for i, pdf in enumerate(pdfs, start=1):
        lista_pdf.insert(tk.END, f"{i}. {pdf}")

# Função para perguntar ao usuário se a ordem está correta
def pergunta_ordem():
    pergunta_label.config(text="Essa é a ordem correta para mesclar os PDFs?")
    sim_button.config(state=tk.NORMAL)
    nao_button.config(state=tk.NORMAL)

# Função chamada ao clicar "Sim"
def confirmar_sim():
    sim_button.config(state=tk.DISABLED)
    nao_button.config(state=tk.DISABLED)
    mesclar_pdfs()

# Função chamada ao clicar "Não"
def confirmar_nao():
    troca = simpledialog.askstring("Trocar Arquivos", "Digite os números dos arquivos que deseja trocar de lugar, separados por vírgula (ex: 1,2):")
    if troca:
        try:
            indices = [int(x) - 1 for x in troca.split(',')]
            if len(indices) == 2:
                pdfs[indices[0]], pdfs[indices[1]] = pdfs[indices[1]], pdfs[indices[0]]
                imprimir_lista(pdfs)
            else:
                messagebox.showerror("Erro", "Forneça exatamente dois números.")
        except ValueError:
            messagebox.showerror("Erro", "Entrada inválida.")
    pergunta_ordem()

# Função para mesclar os PDFs
def mesclar_pdfs():
    merger = PdfMerger()
    for pdf in pdfs:
        caminho_completo = os.path.join(pasta, pdf)
        merger.append(caminho_completo)

    nome_pasta = os.path.basename(os.path.normpath(pasta))
    nome_arquivo_saida = f"{nome_pasta}.pdf"

    with open(nome_arquivo_saida, 'wb') as output_pdf:
        merger.write(output_pdf)

    messagebox.showinfo("Sucesso", f"PDFs mesclados com sucesso! Arquivo salvo como '{nome_arquivo_saida}'")

# Configuração da janela principal
root = tk.Tk()
root.title("Mesclador de PDFs")

# Campo de texto para a pasta
tk.Label(root, text="Endereço da pasta:").pack(pady=5)
pasta_entry = tk.Entry(root, width=50)
pasta_entry.pack(pady=5)

# Botão para iniciar o processo
iniciar_button = tk.Button(root, text="Iniciar", command=iniciar)
iniciar_button.pack(pady=10)

# Lista para exibir a ordem dos PDFs
tk.Label(root, text="Lista de arquivos PDF:").pack(pady=5)
lista_pdf = tk.Listbox(root, height=10, width=50)
lista_pdf.pack(pady=5)

# Pergunta se a ordem está correta
pergunta_label = tk.Label(root, text="")
pergunta_label.pack(pady=5)

# Botões de "Sim" e "Não"
sim_button = tk.Button(root, text="Sim", state=tk.DISABLED, command=confirmar_sim)
sim_button.pack(side=tk.LEFT, padx=20, pady=10)

nao_button = tk.Button(root, text="Não", state=tk.DISABLED, command=confirmar_nao)
nao_button.pack(side=tk.RIGHT, padx=20, pady=10)

# Inicia a interface gráfica
root.mainloop()
