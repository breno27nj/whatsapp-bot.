"""
Bot de respostas automáticas para WhatsApp (via Twilio Sandbox).
Autor: você :)

Como funciona:
1. O WhatsApp manda a mensagem do usuário para o Twilio.
2. O Twilio manda essa mensagem para ESTE servidor (rota /webhook).
3. Este servidor decide a resposta e devolve para o Twilio.
4. O Twilio entrega a resposta no WhatsApp do usuário.
"""

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# ---------------------------------------------------------------
# AQUI é onde você programa a "inteligência" do bot.
# Por enquanto é um bot simples baseado em palavras-chave.
# Depois você pode trocar essa função por uma chamada a uma IA,
# um banco de dados, uma consulta ao Bitrix24, etc.
# ---------------------------------------------------------------
def gerar_resposta(mensagem_usuario: str) -> str:
    texto = mensagem_usuario.strip().lower()

    if texto in ("oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"):
        return (
            "Olá! 👋 Eu sou o bot de atendimento automático.\n"
            "Digite:\n"
            "1 - Falar sobre produtos\n"
            "2 - Falar com um atendente\n"
            "3 - Horário de funcionamento"
        )

    if texto == "1":
        return "Temos os produtos A, B e C. Qual te interessa?"

    if texto == "2":
        return "Certo! Em instantes um atendente humano vai te responder por aqui."

    if texto == "3":
        return "Funcionamos de segunda a sexta, das 9h às 18h."

    # resposta padrão quando não entende a mensagem
    return (
        "Desculpe, não entendi .\n"
        "Digite *oi* para ver as opções disponíveis."
    )


@app.route("/webhook", methods=["POST"])
def webhook():
    # O Twilio envia a mensagem recebida no campo "Body"
    mensagem_recebida = request.values.get("Body", "")
    numero_remetente = request.values.get("From", "")

    print(f"Mensagem recebida de {numero_remetente}: {mensagem_recebida}")

    resposta_texto = gerar_resposta(mensagem_recebida)

    # Monta a resposta no formato que o Twilio/WhatsApp entende (TwiML)
    resposta = MessagingResponse()
    resposta.message(resposta_texto)

    return str(resposta)


@app.route("/", methods=["GET"])
def home():
    return "Bot rodando! Configure o webhook do Twilio para /webhook"


if __name__ == "__main__":
    # debug=True só em ambiente de desenvolvimento/teste
    app.run(port=5000, debug=True)
