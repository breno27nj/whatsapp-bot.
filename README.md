# Bot de Respostas Automáticas para WhatsApp — Passo a Passo

Guia completo para iniciantes, usando Python + Flask + Twilio.

---

## PARTE 1 — Preparar o ambiente no seu PC

### 1.1. Confirmar o Python instalado
No VS Code, abra o terminal (menu **Terminal > New Terminal**) e digite:
```
python --version
```
Se aparecer algo como `Python 3.x.x`, está tudo certo. Se der erro, instale o Python em https://python.org (marque a opção "Add Python to PATH" na instalação).

### 1.2. Criar uma pasta para o projeto
```
mkdir whatsapp-bot
cd whatsapp-bot
```
Abra essa pasta no VS Code (**File > Open Folder**).

### 1.3. Criar um ambiente virtual (isola as bibliotecas deste projeto)
```
python -m venv venv
```
Ativar o ambiente virtual:
- **Windows:** `venv\Scripts\activate`
- **Mac/Linux:** `source venv/bin/activate`

Você vai ver `(venv)` aparecendo no início da linha do terminal — isso confirma que está ativo.

### 1.4. Instalar as bibliotecas
Copie os arquivos `app.py` e `requirements.txt` (fornecidos) para dentro da pasta `whatsapp-bot`. Depois rode:
```
pip install -r requirements.txt
```

---

## PARTE 2 — Criar a conta no Twilio (é grátis para testes)

### 2.1. Cadastro
Acesse https://www.twilio.com/try-twilio e crie uma conta gratuita.

### 2.2. Ativar o WhatsApp Sandbox
1. No painel do Twilio, vá em **Messaging > Try it out > Send a WhatsApp message**.
2. Você verá um número do Twilio e um código tipo `join palavra-chave`.
3. No **seu** WhatsApp, mande uma mensagem para esse número do Twilio com o código exibido (ex: `join azul-gato`).
4. Isso conecta o SEU WhatsApp ao Sandbox de testes por 24h (depois é só reenviar o `join` de novo).

> Isso é só para testes. Para um número de produção definitivo, depois você configura um número WhatsApp Business real dentro do próprio Twilio (processo pago e mais burocrático).

---

## PARTE 3 — Rodar o bot localmente

### 3.1. Testar se o Flask sobe
Dentro da pasta do projeto, com o ambiente virtual ativado:
```
python app.py
```
Se aparecer `Running on http://127.0.0.1:5000`, está funcionando. Deixe esse terminal aberto.

### 3.2. Expor seu computador para a internet (com ngrok)
O Twilio precisa alcançar seu servidor, que hoje só existe no seu PC (`localhost`). Para isso, usamos o **ngrok**, que cria um link público temporário apontando pro seu localhost.

1. Baixe em https://ngrok.com/download e instale.
2. Crie uma conta gratuita no site do ngrok e pegue seu "authtoken".
3. No terminal, configure o token (uma vez só):
   ```
   ngrok config add-authtoken SEU_TOKEN_AQUI
   ```
4. Em um **novo** terminal (deixe o `python app.py` rodando no outro), rode:
   ```
   ngrok http 5000
   ```
5. O ngrok vai mostrar algo como:
   ```
   Forwarding    https://abcd-123-45-67.ngrok-free.app -> http://localhost:5000
   ```
   Copie essa URL `https://....ngrok-free.app`.

---

## PARTE 4 — Conectar o Twilio ao seu bot

1. No painel do Twilio, vá em **Messaging > Try it out > Send a WhatsApp message > Sandbox Settings**.
2. No campo **"When a message comes in"**, cole:
   ```
   https://abcd-123-45-67.ngrok-free.app/webhook
   ```
   (a URL do ngrok + `/webhook`)
3. Método: **HTTP POST**.
4. Salve.

---

## PARTE 5 — Testar!

No seu WhatsApp, mande "oi" para o número do Twilio Sandbox. O bot deve responder automaticamente com o menu de opções. Teste digitando "1", "2", "3" também.

Acompanhe o terminal onde o `app.py` está rodando: cada mensagem recebida aparece ali impressa (isso ajuda a depurar erros).

---

## PARTE 6 — Personalizando as respostas

Toda a "inteligência" do bot está na função `gerar_resposta()` dentro do `app.py`. Para mudar o comportamento, edite essa função — não precisa mexer em mais nada. Exemplos do que dá pra evoluir depois:
- Conectar a um banco de dados (SQLite, PostgreSQL) para guardar histórico de conversas.
- Conectar a uma IA (API da Anthropic/Claude, por exemplo) para respostas mais inteligentes em vez de palavras-chave fixas.
- Integrar com uma planilha ou CRM.

---

## PARTE 7 — Indo além: outros canais e o Bitrix24

A vantagem de ter feito com Flask é que essa mesma lógica de `gerar_resposta()` é reaproveitável:

- **Telegram:** trocar a parte do Twilio pela biblioteca `python-telegram-bot`, mas a função de resposta continua igual.
- **Bitrix24:** o Bitrix24 tem seu próprio recurso chamado **Open Channels** e também **Webhooks/REST API**, que permitem conectar canais externos (inclusive WhatsApp Business) à central de atendimento do CRM. Nesse caso, o "conector" muda (você usaria as chamadas REST do Bitrix24 em vez do Twilio), mas o raciocínio de "receber mensagem → decidir resposta → devolver mensagem" é o mesmo que você aprendeu aqui.
- Quando for integrar com o Bitrix24 especificamente, me avise — a configuração de Webhooks de entrada/saída do Bitrix24 tem particularidades próprias e posso te guiar passo a passo nessa parte também.

---

## PARTE 8 — Colocando em produção (resumo)

Para não depender do ngrok e do seu PC ligado o tempo todo:
1. Hospedar o `app.py` em um servidor real (ex: Render, Railway, PythonAnywhere, ou uma VPS).
2. Trocar a URL do ngrok pela URL fixa do servidor no painel do Twilio.
3. Solicitar um número de WhatsApp Business oficial dentro do Twilio (sai do modo Sandbox).

Isso já é um passo mais avançado — quando chegar nessa etapa, também posso te ajudar em detalhes.
