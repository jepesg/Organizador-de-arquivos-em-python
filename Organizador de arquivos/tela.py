import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pathlib import Path
from main import organize_files

# Classe para criar a interface grafica
class OrganizadorApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        root.title("Organizador de Arquivos")
        root.geometry("620x360")
        root.resizable(False, False)

        self.pasta_selecionada = tk.StringVar(value=str(Path.cwd()))
        self.status_texto = tk.StringVar(value="Selecione uma pasta para organizar.")

        container = ttk.Frame(root, padding=16)
        container.pack(fill="both", expand=True)

        ttk.Label(container, text="Pasta para organizar:").grid(
            row=0, column=0, sticky="w", pady=(0, 6)
        )

        entrada = ttk.Entry(container, textvariable=self.pasta_selecionada, width=60)
        entrada.grid(row=1, column=0, sticky="ew", padx=(0, 8))

        ttk.Button(container, text="Procurar", command=self.selecionar_pasta).grid(
            row=1, column=1, sticky="e"
        )

        ttk.Label(container, textvariable=self.status_texto, wraplength=560, justify="left").grid(
            row=2, column=0, columnspan=2, sticky="w", pady=(12, 0)
        )

        ttk.Button(container, text="Organizar arquivos", command=self.organizar).grid(
            row=3, column=0, columnspan=2, pady=(16, 0)
        )

        self.lista_arquivos = tk.Text(container, height=10, width=72, wrap="word")
        self.lista_arquivos.grid(row=4, column=0, columnspan=2, pady=(10, 0), sticky="nsew")
        self.lista_arquivos.configure(state="disabled")

        ttk.Label(
            container,
            text="Criado por Guilherme Jepes",
            foreground="#666666",
            font=("Segoe UI", 9),
        ).grid(row=5, column=0, columnspan=2, pady=(10, 0))

        container.columnconfigure(0, weight=1)
        container.rowconfigure(4, weight=1)

#   Função para selecionar a pasta que vamos organizar
    def selecionar_pasta(self) -> None:
        pasta = filedialog.askdirectory(title="Selecione a pasta")
        if pasta:
            self.pasta_selecionada.set(pasta)

# Função para mostrar a lista de arquivos na interface
    def mostrar_lista(self, arquivos: list[tuple[str, str]]) -> None:
        self.lista_arquivos.configure(state="normal")
        self.lista_arquivos.delete("1.0", "end")
        if not arquivos:
            self.lista_arquivos.insert("1.0", "Nenhum arquivo foi organizado.")
        else:
            linhas = [f"{nome} -> {pasta}" for nome, pasta in arquivos]
            self.lista_arquivos.insert("1.0", "Arquivos organizados:\n" + "\n".join(linhas))
        self.lista_arquivos.configure(state="disabled")

# Função para exportar a lista de arquivos para um .txt
    def exportar_txt(self, arquivos:list[tuple[str, str]]) -> None:
        if not arquivos:
            messagebox.showinfo("Exportar", "Nenhum arquivo para exportar.")
            return

        pasta_destino = filedialog.askdirectory(title="Selecione a pasta de destino")
        if not pasta_destino:
            return

        log_file = Path(pasta_destino) / "organizador_log.txt"
        try:
            with log_file.open("w", encoding="utf-8") as f:
                for nome, pasta in arquivos:
                    f.write(f"{nome} -> {pasta}\n")
            messagebox.showinfo("Exportar", f"Log exportado com sucesso para:\n{log_file}")
        except Exception as erro:
            messagebox.showerror("Erro", f"Não foi possível exportar o log.\n{erro}")

#   Função para organizar os arquivos
    def organizar(self) -> None:
        pasta = self.pasta_selecionada.get().strip()
        if not pasta:
            messagebox.showwarning("Aviso", "Selecione uma pasta antes de organizar.")
            return

        try:
            quantidade, arquivos = organize_files(
                pasta,
                skip_files={"main.py", "tela.py"},
                return_details=True,
            )
            self.status_texto.set(f"{quantidade} arquivo(s) organizado(s) com sucesso.")
            self.mostrar_lista(arquivos)
            self.exportar_txt(arquivos)
        except Exception as erro:
            self.status_texto.set(f"Erro: {erro}")
            self.mostrar_lista([])
            messagebox.showerror("Erro", f"Não foi possível organizar os arquivos.\n{erro}")

# Função para mostrar o log def generate_log do main.py na interface
# Self none para mostrar o log na interface
    def log_viwer(self) -> None:
        log_file = Path.home() / "Documentos" / "organizador_log.txt"
        if not log_file.exists():
            messagebox.showinfo("Log", "Nenhum log encontrado.")
            return

        with log_file.open("r", encoding="utf-8") as f:
            conteudo = f.read()

        log_window = tk.Toplevel(self.root)
        log_window.title("Log de Organização")
        log_window.geometry("600x400")

        text_area = tk.Text(log_window, wrap="word")
        text_area.pack(fill="both", expand=True)
        text_area.insert("1.0", conteudo)
        text_area.configure(state="disabled")
        
if __name__ == "__main__":
    raiz = tk.Tk()
    app = OrganizadorApp(raiz)
    raiz.mainloop()
    log_viewer_button = ttk.Button(app.root, text="Ver Log", command=app.log_viwer)
    log_viewer_button.pack(pady=10)
