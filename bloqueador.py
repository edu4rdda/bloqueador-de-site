import tkinter as tk
import os
import sys
import ctypes

arq_host = r"C:\Windows\System32\drivers\etc\hosts"
redi = "127.0.0.1"

lista = []

def limpar_cache_dns():
    os.system("ipconfig /flushdns")
    print("Cache DNS limpo.")

def carregar_sites_bloqueados():
    try:
        with open(arq_host, 'r') as arquivo:
            conteudo = arquivo.readlines()
            sites = [linha.split()[1] for linha in conteudo if linha.startswith(redi)]
            return sites
    except Exception as e:
        print(f"Erro ao carregar sites bloqueados: {e}")
        return []

def verificar_permissoes():
    try:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
        if not is_admin:
            print("Execute o programa como administrador.")
            sys.exit(1)
    except Exception as e:
        print(f"Erro ao verificar permissões de administrador: {e}")
        sys.exit(1)

def bloquear_site(site):
    if site.startswith("http://") or site.startswith("https://"):
        site = site.split("//")[1]
    try:
        with open(arq_host, 'r+') as arquivo:
            conteudo = arquivo.readlines()
            dominios = [site, f"www.{site}" if not site.startswith("www.") else site.replace("www.", "")]
            
            # Verifica se o domínio já está redirecionado
            for dominio in dominios:
                if any(dominio in linha for linha in conteudo):
                    return f"O site {site} já está redirecionado para {redi}."
            
            # Adiciona o domínio ao arquivo hosts
            for dominio in dominios:
                arquivo.write(f"{redi} {dominio}\n")
            
            limpar_cache_dns()
            return f"O site {site} foi bloqueado com sucesso e redirecionado para {redi}."
    except PermissionError:
        return "Erro: Você precisa executar o programa como administrador."
    except Exception as e:
        return f"Erro ao bloquear o site: {e}"

def desbloquear_site(site):
    """Desbloqueia o site removendo o redirecionamento no arquivo hosts"""
    try:
        with open(arq_host, 'r') as arquivo:
            conteudo = arquivo.readlines()
        with open(arq_host, 'w') as arquivo:
            for linha in conteudo:
                if site not in linha:
                    arquivo.write(linha)
        limpar_cache_dns() 
        return f"O site {site} foi desbloqueado com sucesso."
    except PermissionError:
        return "Erro: Você precisa executar o programa como administrador."
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

verificar_permissoes()

root = tk.Tk()
root.title("Bloqueador de Sites")
root.geometry("400x550")
root.configure(bg="#f0f4f8")

widget1 = tk.Frame(root, bg="#f0f4f8")
widget1.pack(pady=20)

titulo = tk.Label(widget1, text="Bloqueador de Sites", foreground="#333333", bg="#f0f4f8", font=("Helvetica", 18, "bold"))
titulo.pack(pady=(0, 20))

entrada_site = tk.Entry(widget1, width=35, font=("Helvetica", 12))
entrada_site.pack(pady=(0, 10))

b_bloquear = tk.Button(widget1, text="Bloquear", command=adicionar, fg="white", bg="#007BFF", font=("Helvetica", 12, "bold"))
b_bloquear.pack(pady=(0, 20))

nome_lista = tk.Label(widget1, text="Sites Bloqueados", foreground="#333333", bg="#f0f4f8", font=("Helvetica", 10, "bold"))
nome_lista.pack()

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
