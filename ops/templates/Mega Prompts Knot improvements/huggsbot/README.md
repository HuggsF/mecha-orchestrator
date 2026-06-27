# HuggsBot — Mendas Studio · Central de Chamados (Telegram)

Bot conversacional que abre chamados de comunicação seguindo o SLA do **PR.COM.001**:
categorias de esforço (2/3/5/10/15 dias úteis), corte das 16h, protocolo, briefing mínimo e fluxo de urgência.

---

## ⚠️ Antes de tudo: troque o token
Você compartilhou o token em chat, então ele está exposto. No **@BotFather**:
1. `/revoke` → escolha o **HuggsBot** → copie o **novo** token.
2. Cole esse novo token no arquivo `.env` (passo abaixo). Nunca suba o `.env` para o Git.

---

## ▶️ Rodar e testar em 2 minutos (modo polling — sem hospedar nada)

Pré-requisito: **Python 3.10+** instalado.

```bash
cd huggsbot
python -m venv .venv && source .venv/bin/activate     # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env          # Windows: copy .env.example .env
#   edite .env e cole o NOVO token em TELEGRAM_TOKEN

python huggsbot.py
```

Deve aparecer `HuggsBot online — polling…`. Agora abra o Telegram, procure **@Huggies_bbot** e envie **/start**.

### Comandos
| Comando | O que faz |
|---|---|
| `/start`  | Apresentação + menu |
| `/novo`   | Abre um chamado (categoria → concessão → canal → título → briefing → urgência) |
| `/sla`    | Mostra as categorias de esforço e prazos |
| `/status` | Lista seus chamados abertos |
| `/cancel` | Cancela o fluxo atual |

---

## ☁️ Deixar o bot no ar 24/7 (opcional)
O modo polling acima só roda enquanto seu terminal está aberto. Para deixar online:

- **Railway / Render / Fly.io** (grátis para começar): suba esta pasta, defina a variável de ambiente `TELEGRAM_TOKEN` e use o `Procfile` (`worker: python huggsbot.py`).
- **VPS / Raspberry**: rode com `systemd` ou `screen`/`tmux`.

Nenhuma porta/HTTP é necessária — o polling fala direto com a API do Telegram.

---

## 🖥 Mini App (o mesmo front dentro do Telegram) — opcional
O painel visual (`Mendas Studio Chamados Telegram — MiniApp.html`) já vem com o SDK do Telegram.
Para plugá-lo:
1. Hospede esse arquivo em qualquer HTTPS estático (GitHub Pages, Netlify drop, Vercel).
2. No `.env`, defina `MINIAPP_URL=https://sua-url/arquivo.html` → o `/start` ganha o botão **Abrir painel**.
3. (Opcional) No @BotFather: `/newapp` ou *Bot Settings → Menu Button → Web App* apontando para a mesma URL.

---

## 🔌 Próxima fase (persistência real)
Hoje os chamados ficam em memória (somem ao reiniciar). Para produção, troque o dicionário `TICKETS`
por: Microsoft Planner (esteira), Microsoft Lists (calendário editorial) e os 8 hooks via Power Automate —
exatamente o desenho do deck *Como Configurar*.
