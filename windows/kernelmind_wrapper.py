"""
KernelMind Wrapper para Windows
Converte comandos do KernelMind (WSL) em aplicação Windows GUI
"""

import subprocess
import json
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import os
from datetime import datetime

class KernelMindApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KernelMind - IA Ética para Monitoramento do Sistema")
        self.root.geometry("1200x700")
        self.root.configure(bg='#1e1e1e')
        
        # Status do WSL
        self.wsl_ready = self.check_wsl()
        
        # Criar interface
        self.create_widgets()
        
        # Iniciar monitoramento automático
        if self.wsl_ready:
            self.start_monitoring()
        else:
            messagebox.showerror("Erro", "WSL não encontrado. Instale o WSL primeiro!")
    
    def check_wsl(self):
        """Verifica se WSL está instalado"""
        try:
            result = subprocess.run(['wsl', '--status'], 
                                  capture_output=True, text=True)
            return result.returncode == 0
        except:
            return False
    
    def create_widgets(self):
        """Cria interface gráfica"""
        
        # Estilos
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TLabel', background='#1e1e1e', foreground='#ffffff')
        style.configure('TButton', background='#0e639c', foreground='#ffffff')
        
        # Frame principal
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Título
        title = tk.Label(main_frame, text="🧠 KernelMind", 
                        font=('Arial', 24, 'bold'), 
                        bg='#1e1e1e', fg='#00ff00')
        title.pack(pady=10)
        
        # Subtítulo
        subtitle = tk.Label(main_frame, 
                          text="Monitoramento Ético do Sistema | EthicsLock Ativo",
                          font=('Arial', 10), bg='#1e1e1e', fg='#888888')
        subtitle.pack(pady=(0,20))
        
        # Frame de métricas (3 colunas)
        metrics_frame = ttk.Frame(main_frame)
        metrics_frame.pack(fill=tk.X, pady=10)
        
        # CPU
        cpu_frame = ttk.LabelFrame(metrics_frame, text=" CPU ", padding=10)
        cpu_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.cpu_label = tk.Label(cpu_frame, text="0%", 
                                 font=('Arial', 36, 'bold'),
                                 bg='#2d2d2d', fg='#00ff00')
        self.cpu_label.pack()
        
        self.cpu_detail = tk.Label(cpu_frame, text="Carregando...", 
                                  bg='#2d2d2d', fg='#cccccc')
        self.cpu_detail.pack()
        
        # RAM
        ram_frame = ttk.LabelFrame(metrics_frame, text=" Memória RAM ", padding=10)
        ram_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.ram_label = tk.Label(ram_frame, text="0%", 
                                 font=('Arial', 36, 'bold'),
                                 bg='#2d2d2d', fg='#ffaa00')
        self.ram_label.pack()
        
        self.ram_detail = tk.Label(ram_frame, text="Carregando...", 
                                  bg='#2d2d2d', fg='#cccccc')
        self.ram_detail.pack()
        
        # Disco
        disk_frame = ttk.LabelFrame(metrics_frame, text=" Disco ", padding=10)
        disk_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        self.disk_label = tk.Label(disk_frame, text="0%", 
                                  font=('Arial', 36, 'bold'),
                                  bg='#2d2d2d', fg='#00aaff')
        self.disk_label.pack()
        
        self.disk_detail = tk.Label(disk_frame, text="Carregando...", 
                                   bg='#2d2d2d', fg='#cccccc')
        self.disk_detail.pack()
        
        # Frame de sugestões
        suggestions_frame = ttk.LabelFrame(main_frame, text=" 💡 Sugestões da IA ", padding=10)
        suggestions_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.suggestions_text = scrolledtext.ScrolledText(suggestions_frame, 
                                                          height=8,
                                                          bg='#252526',
                                                          fg='#cccccc',
                                                          font=('Consolas', 10))
        self.suggestions_text.pack(fill=tk.BOTH, expand=True)
        
        # Frame de ações
        actions_frame = ttk.Frame(main_frame)
        actions_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(actions_frame, text="🔄 Atualizar Agora", 
                  command=self.manual_refresh).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(actions_frame, text="💾 Otimizar RAM", 
                  command=self.optimize_ram).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(actions_frame, text="📊 Ver Log Ético", 
                  command=self.show_ethics_log).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(actions_frame, text="🚀 Iniciar API", 
                  command=self.start_api).pack(side=tk.LEFT, padx=5)
        
        # Status bar
        self.status_bar = tk.Label(self.root, text="✅ Pronto | EthicsLock: ATIVO", 
                                  bd=1, relief=tk.SUNKEN, anchor=tk.W,
                                  bg='#007acc', fg='#ffffff')
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
    
    def run_wsl_command(self, command):
        """Executa comando no WSL e retorna resultado"""
        try:
            result = subprocess.run(['wsl', 'bash', '-c', command],
                                  capture_output=True, text=True, timeout=10)
            return result.stdout, result.stderr
        except Exception as e:
            return "", str(e)
    
    def get_system_stats(self):
        """Obtém estatísticas do sistema via KernelMind"""
        cmd = "cd ~/kernelmind && km snapshot --json"
        output, error = self.run_wsl_command(cmd)
        
        if output:
            try:
                data = json.loads(output)
                return data
            except:
                pass
        return None
    
    def get_ram_suggestions(self):
        """Obtém sugestões de otimização"""
        cmd = "cd ~/kernelmind && km memory"
        output, error = self.run_wsl_command(cmd)
        return output if output else "Sem sugestões no momento"
    
    def update_metrics(self):
        """Atualiza as métricas na interface"""
        stats = self.get_system_stats()
        
        if stats:
            # Atualizar CPU
            cpu_percent = stats.get('cpu', {}).get('percent', 0)
            self.cpu_label.config(text=f"{cpu_percent:.1f}%")
            self.cpu_detail.config(text=f"CPUs: {stats.get('cpu', {}).get('count', 0)} núcleos")
            
            # Atualizar RAM
            memory = stats.get('memory', {})
            ram_percent = memory.get('percent', 0)
            self.ram_label.config(text=f"{ram_percent:.1f}%")
            ram_used = memory.get('used_gb', 0)
            ram_total = memory.get('total_gb', 0)
            self.ram_detail.config(text=f"Usado: {ram_used:.1f}GB / {ram_total:.1f}GB")
            
            # Atualizar Disco
            disk = stats.get('disk', {})
            disk_percent = disk.get('percent', 0)
            self.disk_label.config(text=f"{disk_percent:.1f}%")
            self.disk_detail.config(text=f"Livre: {disk.get('free_gb', 0):.1f}GB")
            
            # Atualizar sugestões
            if ram_percent > 80:
                suggestions = self.get_ram_suggestions()
                self.update_suggestions(suggestions)
            
            self.status_bar.config(text=f"✅ Última atualização: {datetime.now().strftime('%H:%M:%S')} | EthicsLock: ATIVO")
        
        # Agendar próxima atualização
        self.root.after(5000, self.update_metrics)
    
    def update_suggestions(self, suggestions):
        """Atualiza área de sugestões"""
        self.suggestions_text.delete(1.0, tk.END)
        self.suggestions_text.insert(1.0, suggestions)
    
    def manual_refresh(self):
        """Atualização manual"""
        self.status_bar.config(text="🔄 Atualizando...")
        self.update_metrics()
    
    def optimize_ram(self):
        """Solicita otimização de RAM (com confirmação ética)"""
        if messagebox.askyesno("EthicsLock", 
                               "KernelMind sugere otimizar a memória RAM.\n\n"
                               "Isso pode melhorar o desempenho do sistema.\n\n"
                               "Deseja permitir esta ação?"):
            self.status_bar.config(text="⚙️ Executando otimização de RAM...")
            cmd = "cd ~/kernelmind && km memory --optimize"
            output, error = self.run_wsl_command(cmd)
            messagebox.showinfo("Otimização", "Otimização concluída!\n\n" + output[:500])
            self.status_bar.config(text="✅ Otimização concluída")
    
    def show_ethics_log(self):
        """Mostra log ético do KernelMind"""
        cmd = "cd ~/kernelmind && km ethics --log"
        output, error = self.run_wsl_command(cmd)
        
        log_window = tk.Toplevel(self.root)
        log_window.title("Log Ético do KernelMind")
        log_window.geometry("800x500")
        
        text_area = scrolledtext.ScrolledText(log_window, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True)
        text_area.insert(1.0, output if output else "Nenhum log encontrado")
    
    def start_api(self):
        """Inicia o servidor API em thread separada"""
        def run_api():
            cmd = "cd ~/kernelmind && python3 api/server.py"
            self.run_wsl_command(cmd)
        
        thread = threading.Thread(target=run_api, daemon=True)
        thread.start()
        messagebox.showinfo("API", "API KernelMind iniciada em http://localhost:7771\n\n"
                                  "Acesse /docs para documentação")
    
    def start_monitoring(self):
        """Inicia monitoramento contínuo"""
        check_cmd = "test -d ~/kernelmind && echo 'installed'"
        output, _ = self.run_wsl_command(check_cmd)
        
        if 'installed' not in output:
            messagebox.showwarning("Aviso", 
                                  "KernelMind não encontrado no WSL.\n\n"
                                  "Clique em OK para instalar automaticamente.")
            self.install_kernelmind()
        else:
            self.update_metrics()
    
    def install_kernelmind(self):
        """Instala KernelMind automaticamente"""
        install_script = """
        cd ~
        git clone https://github.com/armazen-nft/KERNEL-MIND.git kernelmind
        cd kernelmind
        pip3 install psutil fastapi uvicorn
        python3 install.py
        """
        
        self.status_bar.config(text="📦 Instalando KernelMind...")
        output, error = self.run_wsl_command(install_script)
        
        if error:
            messagebox.showerror("Erro", "Falha na instalação:\n" + error)
        else:
            messagebox.showinfo("Sucesso", "KernelMind instalado com sucesso!")
            self.start_monitoring()

if __name__ == "__main__":
    root = tk.Tk()
    app = KernelMindApp(root)
    root.mainloop()
