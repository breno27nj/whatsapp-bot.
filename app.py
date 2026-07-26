from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

def gerar_resposta(mensagem_usuario: str) -> str:
    texto = mensagem_usuario.strip().lower()

    if texto in ("oi", "olá", "ola", "bom dia", "boa tarde", "boa noite"):
        return (
            "Olá! Sou um bot de atendimento automatico, Irei iniciar o seu atendimento. .\n"
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
   
    return (
        "Desculpe, não entendi .\n"
        "Digite *oi* para ver as opções disponíveis."
    )

@app.route("/webhook", methods=["POST"])
def webhook():
   mensagem_recebida = request.values.get("Body", "")
    numero_remetente = request.values.get("From", "")

    print(f"Mensagem recebida de {numero_remetente}: {mensagem_recebida}")

    resposta_texto = gerar_resposta(mensagem_recebida)
    resposta = MessagingResponse()
    resposta.message(resposta_texto)

    return str(resposta)

@app.route("/", methods=["GET"])
def home():
    return "Bot rodando! Configure o webhook do Twilio para /webhook"

if __name__ == "__main__":
    app.run(port=5000, debug=True)
