#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
HuggsBot — Mendas Studio · Central de Chamados (Telegram)
Bot conversacional que abre chamados de comunicação seguindo o SLA do PR.COM.001.

Comandos:
  /start    apresentação + menu
  /novo     abrir um chamado (fluxo guiado)
  /sla      ver as categorias de esforço e prazos
  /status   ver seus chamados abertos
  /cancel   cancelar o fluxo atual

Requer: python-telegram-bot==21.6  (pip install -r requirements.txt)
Rode:   TELEGRAM_TOKEN="seu_token" python huggsbot.py   (ou use o .env)
"""

import os
import logging
import datetime as dt

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

from telegram import (
    Update, InlineKeyboardButton, InlineKeyboardMarkup,
    ReplyKeyboardRemove, WebAppInfo,
)
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, ConversationHandler, ContextTypes, filters,
)

# Integração opcional com o FreeScout (persistência real dos chamados)
try:
    import freescout_client as fs
except Exception:
    fs = None

# ──────────────────────────────────────────────────────────────────────
# Config
# ──────────────────────────────────────────────────────────────────────
TOKEN = os.environ.get("TELEGRAM_TOKEN", "").strip()
MINIAPP_URL = os.environ.get("MINIAPP_URL", "").strip()  # opcional: URL HTTPS do front (Mini App)

logging.basicConfig(
    format="%(asctime)s · %(name)s · %(levelname)s · %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("huggsbot")

# Matriz de SLA (categoria de esforço → (nome, dias úteis, exemplos))
CATS = {
    "2":  ("Operacional / Distribuição", 2,
           "Fotos/vídeos prontos, comunicados em texto, vagas, republicação."),
    "3":  ("Comunicação simples / Informativa", 3,
           "Peça única p/ redes, ajuste em arte existente, release, pós-evento."),
    "5":  ("Criação e Design", 5,
           "Banners, cartazes, design p/ redes, marca em brindes/frota."),
    "10": ("Produção AV e Identidade estruturada", 10,
           "Marcas de programas, produção de vídeos (roteiro + aprovação + pós)."),
    "15": ("Projetos e campanhas integradas", 15,
           "Campanhas anuais (Maio Amarelo, SIPAT, GPTW), pacote multicanal."),
}
CAT_ORDER = ["2", "3", "5", "10", "15"]

CONCESSOES = ["Monte Rodovias", "Bahia Norte", "Litoral Norte",
              "Rota do Atlântico", "Rota dos Coqueiros"]
CANAIS = ["Redes Sociais", "E-mail", "TV Corporativa",
          "Somos Monte", "LinkedIn", "Imprensa"]

# Estados da conversa
CAT, CONC, CANAL, TITULO, BRIEF, URG = range(6)

# Armazenamento em memória (troque por DB/Planner numa próxima fase)
TICKETS = {}          # chat_id -> [ticket, ...]
SEQ = {"n": 7}        # contador de protocolo

# ──────────────────────────────────────────────────────────────────────
# SLA helpers (dias úteis + corte 16h)
# ──────────────────────────────────────────────────────────────────────
def add_business_days(start: dt.datetime, n: int) -> dt.datetime:
    d, added = start, 0
    while added < n:
        d += dt.timedelta(days=1)
        if d.weekday() < 5:   # 0-4 = seg-sex
            added += 1
    return d


def make_deadline(cat_days: int):
    now = dt.datetime.now()
    after16 = now.hour >= 16
    start = add_business_days(now, 1) if after16 else now
    return add_business_days(start, cat_days), after16


def fmt(d: dt.datetime) -> str:
    return d.strftime("%d/%m/%Y")


def customer_identity(update: Update):
    """Deriva um cliente estável do FreeScout a partir do usuário do Telegram.
    E-mail sintético tg<chat_id>@telegram.local permite reencontrar os chamados depois."""
    chat = update.effective_chat
    user = update.effective_user
    first = (user.first_name if user and user.first_name else "Telegram")
    last = (user.last_name if user and user.last_name else (f"@{user.username}" if user and user.username else "User"))
    email = f"tg{chat.id}@telegram.local"
    return email, first, last


def freescout_on() -> bool:
    return bool(fs and fs.enabled())

# ──────────────────────────────────────────────────────────────────────
# Teclados
# ──────────────────────────────────────────────────────────────────────
def kb_categorias():
    rows = []
    for cid in CAT_ORDER:
        nome, dias, _ = CATS[cid]
        rows.append([InlineKeyboardButton(f"🗂 {dias}d · {nome}", callback_data=f"cat:{cid}")])
    rows.append([InlineKeyboardButton("✖ Cancelar", callback_data="cancel")])
    return InlineKeyboardMarkup(rows)


def kb_grid(prefix, items, per_row=2):
    rows, row = [], []
    for i, it in enumerate(items):
        row.append(InlineKeyboardButton(it, callback_data=f"{prefix}:{i}"))
        if len(row) == per_row:
            rows.append(row); row = []
    if row:
        rows.append(row)
    rows.append([InlineKeyboardButton("✖ Cancelar", callback_data="cancel")])
    return InlineKeyboardMarkup(rows)


def kb_urg():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Normal", callback_data="urg:0"),
         InlineKeyboardButton("⚡ Urgente", callback_data="urg:1")],
        [InlineKeyboardButton("✖ Cancelar", callback_data="cancel")],
    ])

# ──────────────────────────────────────────────────────────────────────
# /start, /sla, /status
# ──────────────────────────────────────────────────────────────────────
async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    btns = [[InlineKeyboardButton("📝 Abrir chamado (/novo)", callback_data="go_novo")],
            [InlineKeyboardButton("📊 Ver SLA (/sla)", callback_data="go_sla")]]
    if MINIAPP_URL:
        btns.insert(0, [InlineKeyboardButton("🖥 Abrir painel", web_app=WebAppInfo(url=MINIAPP_URL))])
    txt = (
        "👋 *Mendas Studio · Central de Chamados*\n\n"
        "Sou o *HuggsBot*. Abro chamados de comunicação e inicio o SLA conforme "
        "a *categoria de esforço* (PR.COM.001).\n\n"
        "Este é o *canal oficial* — pedidos por e-mail ou conversa solta não iniciam SLA.\n\n"
        "Toque em *Abrir chamado* ou envie /novo."
    )
    await update.effective_message.reply_markdown(txt, reply_markup=InlineKeyboardMarkup(btns))


async def sla_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    linhas = ["📊 *Matriz de SLA — dias úteis*\n"]
    for cid in CAT_ORDER:
        nome, dias, ex = CATS[cid]
        linhas.append(f"*{dias}d · {nome}*\n_{ex}_\n")
    linhas.append("⏰ *Corte 16h:* chamados abertos após as 16h iniciam o SLA no próximo dia útil.")
    await update.effective_message.reply_markdown("\n".join(linhas))


async def status_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    # Fonte da verdade: FreeScout, se configurado; senão, memória.
    if freescout_on():
        email, _, _ = customer_identity(update)
        convs = fs.list_conversations(email, limit=10)
        if not convs:
            await update.effective_message.reply_text("Você ainda não tem chamados. Envie /novo para abrir.")
            return
        linhas = ["📋 *Seus chamados* (FreeScout)\n"]
        for c in convs:
            linhas.append(f"`#{c['number']}` — {c['subject']}\n_status: {c['status']}_\n")
        await update.effective_message.reply_markdown("\n".join(linhas))
        return

    chamados = TICKETS.get(update.effective_chat.id, [])
    if not chamados:
        await update.effective_message.reply_text("Você ainda não tem chamados. Envie /novo para abrir.")
        return
    linhas = ["📋 *Seus chamados*\n"]
    for t in chamados[-10:]:
        flag = " ⚡" if t["urgente"] else ""
        linhas.append(f"`{t['protocolo']}`{flag} — {t['titulo']}\n"
                      f"{t['cat_dias']}d · {t['concessao']} · prazo {t['deadline']}\n")
    await update.effective_message.reply_markdown("\n".join(linhas))

# ──────────────────────────────────────────────────────────────────────
# Fluxo /novo
# ──────────────────────────────────────────────────────────────────────
async def novo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["draft"] = {}
    msg = ("📝 *Novo chamado* — passo 1/6\n\nEscolha a *categoria de esforço* "
           "(ela define o prazo):")
    if update.callback_query:
        await update.callback_query.answer()
        await update.callback_query.message.reply_markdown(msg, reply_markup=kb_categorias())
    else:
        await update.effective_message.reply_markdown(msg, reply_markup=kb_categorias())
    return CAT


async def pick_cat(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    cid = q.data.split(":")[1]
    ctx.user_data["draft"]["cat"] = cid
    nome, dias, _ = CATS[cid]
    await q.edit_message_text(f"✅ Categoria: *{dias}d · {nome}*", parse_mode="Markdown")
    await q.message.reply_markdown("📝 Passo 2/6 — *Concessão / unidade*:",
                                   reply_markup=kb_grid("conc", CONCESSOES))
    return CONC


async def pick_conc(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    ctx.user_data["draft"]["concessao"] = CONCESSOES[int(q.data.split(":")[1])]
    await q.edit_message_text(f"✅ Concessão: *{ctx.user_data['draft']['concessao']}*", parse_mode="Markdown")
    await q.message.reply_markdown("📝 Passo 3/6 — *Canal de veiculação*:",
                                   reply_markup=kb_grid("canal", CANAIS))
    return CANAL


async def pick_canal(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    ctx.user_data["draft"]["canal"] = CANAIS[int(q.data.split(":")[1])]
    await q.edit_message_text(f"✅ Canal: *{ctx.user_data['draft']['canal']}*", parse_mode="Markdown")
    await q.message.reply_markdown("📝 Passo 4/6 — *Título da demanda*\n"
                                   "Envie em uma mensagem (ex: _Campanha Maio Amarelo — pacote de artes_):")
    return TITULO


async def set_titulo(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    ctx.user_data["draft"]["titulo"] = update.message.text.strip()
    await update.message.reply_markdown(
        "📝 Passo 5/6 — *Briefing*\nDescreva objetivo, mensagem-chave, formato e referências "
        "(mín. 12 caracteres):")
    return BRIEF


async def set_brief(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    txt = update.message.text.strip()
    if len(txt) < 12:
        # hook:triagem — briefing insuficiente, SLA não inicia
        await update.message.reply_text("⚠️ Briefing muito curto (mín. 12 caracteres). "
                                        "Descreva um pouco mais — o SLA não inicia sem briefing válido.")
        return BRIEF
    ctx.user_data["draft"]["briefing"] = txt
    await update.message.reply_markdown("📝 Passo 6/6 — A demanda é *urgente*?",
                                        reply_markup=kb_urg())
    return URG


async def set_urg(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    urgente = q.data.split(":")[1] == "1"
    d = ctx.user_data["draft"]
    d["urgente"] = urgente

    # ── hooks: intake → register (+ urgent) ──
    SEQ["n"] += 1
    protocolo = f"MEND-26-{SEQ['n']:03d}"
    nome, dias, _ = CATS[d["cat"]]
    deadline_dt, after16 = make_deadline(dias)
    ticket = {
        "protocolo": protocolo, "titulo": d["titulo"], "cat_dias": dias,
        "cat_nome": nome, "concessao": d["concessao"], "canal": d["canal"],
        "briefing": d["briefing"], "urgente": urgente,
        "deadline": fmt(deadline_dt), "stage": "Triagem",
    }

    # ── Persistência: FreeScout (canal oficial) com fallback em memória ──
    destino = "memória"
    fs_url = None
    if freescout_on():
        email, first, last = customer_identity(update)
        body_html = (
            f"<b>Categoria de esforço:</b> {dias}d · {nome}<br>"
            f"<b>Concessão:</b> {d['concessao']}<br>"
            f"<b>Canal:</b> {d['canal']}<br>"
            f"<b>Prazo (SLA):</b> {ticket['deadline']}"
            f"{' (após 16h — inicia no próximo dia útil)' if after16 else ''}<br>"
            f"<b>Urgente:</b> {'Sim ⚡' if urgente else 'Não'}<br><br>"
            f"<b>Briefing:</b><br>{d['briefing']}"
        )
        tags = [f"{dias}d", d["concessao"], d["canal"], "mendas-studio"]
        if urgente:
            tags.append("urgente")
        conv = fs.create_conversation(
            subject=f"[{dias}d] {d['titulo']}",
            body_html=body_html, customer_email=email,
            customer_first=first, customer_last=last,
            tags=tags, urgent=urgente,
        )
        if conv and conv.get("number"):
            protocolo = f"#{conv['number']}"
            ticket["protocolo"] = protocolo
            ticket["fs_id"] = conv.get("id")
            fs_url = fs.conversation_url(conv.get("id"))
            destino = "FreeScout"
        else:
            log.warning("FreeScout indisponível — usando fallback em memória para %s", protocolo)

    if destino == "memória":
        TICKETS.setdefault(update.effective_chat.id, []).append(ticket)

    log.info("hook:intake  %s recebido (%s)", protocolo, destino)
    log.info("hook:register %s · %dd · %s", protocolo, dias, d["concessao"])
    if urgente:
        log.info("hook:urgent %s repriorizado", protocolo)

    corte = ("\n⏰ Aberto após as 16h — SLA inicia no próximo dia útil." if after16 else "")
    flag = "\n⚡ *URGENTE* — valide com a equipe via Telegram." if urgente else ""
    link = f"\n🔗 [Abrir no FreeScout]({fs_url})" if fs_url else ""
    await q.edit_message_text(
        f"✅ *Chamado registrado* — `{protocolo}`\n\n"
        f"*{ticket['titulo']}*\n"
        f"🗂 {dias}d · {nome}\n"
        f"🏢 {d['concessao']}  ·  📡 {d['canal']}\n"
        f"📅 Prazo: *{ticket['deadline']}*{corte}{flag}{link}\n\n"
        f"_Em Triagem — o SLA começa a contar quando o briefing for validado._\n"
        f"Use /status para acompanhar.",
        parse_mode="Markdown", disable_web_page_preview=True)
    ctx.user_data.pop("draft", None)
    return ConversationHandler.END


async def cancel_cb(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query; await q.answer()
    await q.edit_message_text("❌ Fluxo cancelado. Envie /novo para recomeçar.")
    ctx.user_data.pop("draft", None)
    return ConversationHandler.END


async def cancel_cmd(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Cancelado. Envie /novo para recomeçar.",
                                    reply_markup=ReplyKeyboardRemove())
    ctx.user_data.pop("draft", None)
    return ConversationHandler.END

# ──────────────────────────────────────────────────────────────────────
# Bootstrap
# ──────────────────────────────────────────────────────────────────────
def main():
    if not TOKEN:
        raise SystemExit(
            "❌ TELEGRAM_TOKEN não definido.\n"
            "   Defina no arquivo .env (veja .env.example) ou exporte na shell:\n"
            '   TELEGRAM_TOKEN="seu_token" python huggsbot.py')

    app = Application.builder().token(TOKEN).build()

    conv = ConversationHandler(
        entry_points=[CommandHandler("novo", novo),
                      CallbackQueryHandler(novo, pattern="^go_novo$")],
        states={
            CAT:    [CallbackQueryHandler(pick_cat, pattern="^cat:")],
            CONC:   [CallbackQueryHandler(pick_conc, pattern="^conc:")],
            CANAL:  [CallbackQueryHandler(pick_canal, pattern="^canal:")],
            TITULO: [MessageHandler(filters.TEXT & ~filters.COMMAND, set_titulo)],
            BRIEF:  [MessageHandler(filters.TEXT & ~filters.COMMAND, set_brief)],
            URG:    [CallbackQueryHandler(set_urg, pattern="^urg:")],
        },
        fallbacks=[CommandHandler("cancel", cancel_cmd),
                   CallbackQueryHandler(cancel_cb, pattern="^cancel$")],
        allow_reentry=True,
    )

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sla", sla_cmd))
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(CallbackQueryHandler(sla_cmd, pattern="^go_sla$"))
    app.add_handler(conv)

    if freescout_on():
        log.info("Persistência: FreeScout em %s (mailbox %s)", fs.URL, fs.MAILBOX_ID)
    else:
        log.info("Persistência: memória (FreeScout não configurado — veja .env)")

    log.info("HuggsBot online — polling…")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
