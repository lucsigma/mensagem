
import streamlit as st
import sqlite3
from datetime import datetime

# Banco de dados SQLite
conn = sqlite3.connect("chat.db", check_same_thread=False)
cursor = conn.cursor()

# Criação da tabela se não existir
cursor.execute('''
CREATE TABLE IF NOT EXISTS mensagens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    texto TEXT NOT NULL,
    timestamp TEXT NOT NULL
)
''')
conn.commit()

st.title("💬 Bate-papo")

# 👉 Estilo para deixar o texto preto dentro das caixas de entrada
st.markdown("""
    <style>
    textarea, input[type="text"] {
        color: black !important;
        background-color: white !important;
    }
    </style>
""", unsafe_allow_html=True)

# Campo de entrada
nome = st.text_input("Seu nome:")
mensagem = st.text_area("Digite sua mensagem (pode usar emojis como 😄, ❤, 🔥):")

# Botão de envio
if st.button("📨 Enviar"):
    if nome.strip() and mensagem.strip():
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        cursor.execute("INSERT INTO mensagens (nome, texto, timestamp) VALUES (?, ?, ?)",
                       (nome.strip(), mensagem.strip(), agora))
        conn.commit()
        st.success("Mensagem enviada!")
    else:
        st.warning("Preencha nome e mensagem.")

# Exibir mensagens
st.subheader("🗂 Histórico de Mensagens")
cursor.execute("SELECT nome, texto, timestamp FROM mensagens ORDER BY id DESC")
mensagens = cursor.fetchall()

for nome, texto, timestamp in mensagens:
    st.markdown(f"""
    <div style="background-color:#f1f1f1; padding:10px; margin-bottom:10px; border-radius:10px; color:black;">
        <b>{nome}</b> <span style="color:gray; font-size:12px;">[{timestamp}]</span><br>
        <span style="color:black;">{texto}</span>
    </div>
    """, unsafe_allow_html=True)

# 🔒 Exclusão com senha
st.subheader("⚠ Limpar todas as mensagens")
senha = st.text_input("Digite a senha para apagar:", type="password")

if st.button("🧹 Apagar tudo"):
    if senha == "luc123":
        cursor.execute("DELETE FROM mensagens")
        conn.commit()
        st.success("Mensagens apagadas com sucesso!")
    else:
        st.error("Senha incorreta. Ação não permitida.")