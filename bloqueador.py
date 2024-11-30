import tkinter as tk

arq_host = r"C:\Windows\System32\drivers\etc\hosts"
redi = "127.0.0.1"

lista = []

def carregar_sites_bloqueados():
    try:
        with open(arq_host, 'r') as arquivo:
            conteudo = arquivo.readlines()
            sites = [linha.split()[1] for linha in conteudo if linha.startswith(redi)]
            return sites
    except Exception as e:
        print(f"Erro ao carregar sites bloqueados: {e}")
        return []

def bloquear_site(site):
    if site.startswith("http://") or site.startswith("https://"):
        site = site.split("//")[1]
    try:
        with open(arq_host, 'r+') as arquivo:
            conteudo = arquivo.readlines()
            if any(site in linha for linha in conteudo):
                return f"O site {site} já está bloqueado."
            arquivo.write(f"{redi} {site}\n")
            return f"O site {site} foi bloqueado com sucesso."
    except PermissionError:
        return "Execute o programa como administrador."
    except Exception as e:
        return f"Erro ao bloquear o site: {e}"

def desbloquear_site(site):
    try:
        with open(arq_host, 'r') as arquivo:
            conteudo = arquivo.readlines()
        with open(arq_host, 'w') as arquivo:
            for linha in conteudo:
                if site not in linha:
                    arquivo.write(linha)
        return f"O site {site} foi desbloqueado com sucesso."
    except PermissionError:
        return "Execute o programa como administrador."
    except Exception as e:
        return f"Erro ao desbloquear o site: {e}"

def adicionar():
    site = entrada_site.get().strip()
    if site:
        resultado = bloquear_site(site)
        if "foi bloqueado com sucesso" in resultado:
            lista.append(site)
            atualizar_lista()
        print(resultado)
        entrada_site.delete(0, tk.END)

def desbloquear():
    selecionado = lista_box.curselection()
    if selecionado:
        site = lista[selecionado[0]]
        resultado = desbloquear_site(site)
        if "foi desbloqueado com sucesso" in resultado:
            lista.pop(selecionado[0])
            atualizar_lista()
        print(resultado)

def atualizar_lista():
    lista_box.delete(0, tk.END)
    for site in lista:
        lista_box.insert(tk.END, site)

root = tk.Tk()
root.title("Bloqueador de Sites")
root.geometry("400x550")
root.configure(bg="#f0f4f8")

widget1 = tk.Frame(root, bg="#f0f4f8")
widget1.pack(pady=20)

msg = tk.Label(widget1, text="Bloqueador de Sites", foreground="#333333", bg="#f0f4f8", font=("Helvetica", 18, "bold"))
msg.pack(pady=(0, 20))

entrada_site = tk.Entry(widget1, width=35, font=("Helvetica", 12))
entrada_site.pack(pady=(0, 10))

button1 = tk.Button(widget1, text="Bloquear", command=adicionar, fg="white", bg="#007BFF", font=("Helvetica", 12, "bold"))
button1.pack(pady=(0, 20))

text1 = tk.Label(widget1, text="Sites Bloqueados", foreground="#333333", bg="#f0f4f8", font=("Helvetica", 10, "bold"))
text1.pack()

frame_lista = tk.Frame(widget1, bg="#f0f4f8")
frame_lista.pack(pady=(0, 20))

lista_box = tk.Listbox(frame_lista, width=40, height=10, font=("Helvetica", 12))
lista_box.grid(row=0, column=0, padx=10, pady=(0, 10))

botao_frame = tk.Frame(widget1, bg="#f0f4f8")
botao_frame.pack(pady=(5, 5))

b_desbloquear = tk.Button(botao_frame, text="Desbloquear", command=desbloquear, fg="white", bg="#28A745", font=("Helvetica", 12, "bold"))
b_desbloquear.grid(row=0, column=1, padx=(10, 0))

lista = carregar_sites_bloqueados()
atualizar_lista()

root.mainloop()
