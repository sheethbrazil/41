import os
import json
import time
import asyncio
from datetime import datetime, timedelta, timezone
from typing import Optional

import discord
from discord.ext import commands
from discord import app_commands

# =========================================================
# CONFIG
# =========================================================
TOKEN = os.getenv("DISCORD_TOKEN") or os.getenv("TOKEN") or ""
GUILD_ID = 1407568064987533473

# Colors
EMBED_COLOR = 0x8240B7
SUCCESS_COLOR = 0x22C55E
ERROR_COLOR = 0xEF4444
WAIT_COLOR = 0xF59E0B

# Channels
PANEL_CHANNEL_ID = 1471983685703176376
WELCOME_CHANNEL_ID = 1429240464720134288
CHAT_CHANNEL_ID = 1471529008100282519
RULES_CHANNEL_ID = 1429240462014943243
SUPPORT_CHANNEL_ID = 1468769718029779146
SUGGESTIONS_CHANNEL_ID = 1429240482583678998

TICKET_REQUEST_LOG_CHANNEL_ID = 1471981262351634474
TICKET_CLOSE_LOG_CHANNEL_ID = 1488204071616647258

LEVEL_ANNOUNCE_CHANNEL_ID = 1488978455776333895
JAIL_CHANNEL_ID = 1472845204666056774

STAFF_APPLY_CHANNEL_ID = 1490081954656288990
KICK_APPLY_CHANNEL_ID = 1490082219040178178

AUTO_THREAD_CHANNEL_IDS = {
    1487508885513179378,
    1104918419121385533,
}
AUTO_REACTION_EMOJIS = [
    1488247009847808162,
    1458216548899618898,
    1458212400678440992,
]

# Roles
SERVER_DEVELOPER_ROLE_ID = 1470864946811113647
FOUNDER_ROLE_ID = 1466102368356798801
ADMINISTRATOR_ROLE_ID = 1488194280710344776
HIGH_ADMIN_ROLE_ID = 1479205207689920625
MID_ADMIN_ROLE_ID = 1484221403711541432
MODERATOR_ROLE_ID = 1482227493909037076
JUNIOR_ADMIN_ROLE_ID = 1482227629720342670
SUPPORT_ROLE_ID = 1477411291856638044
GIRL_SUPPORT_ROLE_ID = 1488192711566561300
KICK_MOD_ROLE_ID = 1485896155144392814

GENERAL_ROLE_ID = 1427783336696217791
KICK_VISITORS_ROLE_ID = 1429240282729152524
SERVER_SUPPORTER_ROLE_ID = 1417912343626514522
VIP_ROLE_ID = 1482230783501537362

JAIL_ROLE_ID = 1473371387136577668
APPLICATION_ACCEPT_ROLE_ID = 1482227629720342670

OWNER_USER_ID = 1240321290410397717

EXTRA_TICKET_PERMISSION_ROLE_IDS = {
    1466102368356798801,
    1479205207689920625,
    1484221403711541432,
    1482227493909037076,
    1482227629720342670,
}

# Level roles
LEVEL_ROLE_MAP = [
    {"min": 1, "max": 49, "role_id": 1488950677672820976, "name": "🌱│Beginner"},
    {"min": 50, "max": 149, "role_id": 1488951219060867103, "name": "🔥│Active"},
    {"min": 150, "max": 299, "role_id": 1488951358005706913, "name": "⚡│Pro"},
    {"min": 300, "max": 499, "role_id": 1488952288038093100, "name": "💎│Elite"},
    {"min": 500, "max": 699, "role_id": 1488952584772522024, "name": "👑│Master"},
    {"min": 700, "max": 899, "role_id": 1488952786866540604, "name": "🗡️│Legend"},
    {"min": 900, "max": 1000, "role_id": 1488952921021223105, "name": "🧪│GOD"},
]

# Images
PANEL_IMAGE_URL = "https://i.postimg.cc/0Nw4BvMv/tsmym-bdwn-%CA%BFnwan.png"
RULES_IMAGE_URL = "https://i.postimg.cc/ZYcMgVRy/hl-ant-mtakd-mn-fth-altdhkrt.png"
SUCCESS_IMAGE_URL = "https://i.postimg.cc/GhvHd8WV/copyright-success.png"
WAIT_IMAGE_URL = "https://i.postimg.cc/ZqGGbntC/copyright-wait.png"
FAIL_IMAGE_URL = "https://i.postimg.cc/SRdN551G/copyright-fail.png"
INFO_IMAGE_URL = RULES_IMAGE_URL
APPLY_IMAGE_URL = "https://i.postimg.cc/02qv2GXh/altqdym.png"

# Social links
LINK_TIKTOK = "https://www.tiktok.com/@turkixg0?is_from_webapp=1&sender_device=pc"
LINK_WHATSAPP = "https://whatsapp.com/channel/0029VbBbXRz5fM5bQJk4fR2i"
LINK_INSTAGRAM = "https://www.instagram.com/turkixg1_b7?igsh=Y3ZlazN4a3B4eG40"
LINK_TWITTER = "https://x.com/turki_m18"
LINK_KICK = "https://kick.com/turkixg1-b7"

EMOJI_TIKTOK = "<:tiktok:1471977399083077672>"
EMOJI_INSTA = "<:instagram:1471977324059689062>"
EMOJI_TWIT = "<:twitter:1471977160884355145>"
EMOJI_WA = "<:whatsapp:1471977202642845726>"
EMOJI_KICK = "<:kick:1471977584433823934>"

# Files
DB_FILE = "data.json"
SUGG_STATE_FILE = "suggestions_state.json"
APPLICATION_STATE_FILE = "applications_state.json"

# =========================================================
# TEXT
# =========================================================
PANEL_TITLE = "Turki Community Panel"
PANEL_TEXT = (
    "مرحبًا بك 👋\n\n"
    "اختر من الأزرار بالأسفل لعرض القوانين، المعلومات، السوشال ميديا، "
    "الرتب، ورتب اللفلات، والتقديم.\n\n"
    "⚠️ ممنوع منشن تركي أو أي ستريمر/صانع محتوى."
)

SERVER_RULES_TEXT = (
    "**📜 قوانين السيرفر**\n\n"
    "احترام جميع الأعضاء والآراء\n"
    "يمنع النشر بأي شكل\n"
    "يمنع السب والتحريض على المشاكل\n"
    "يمنع مضايقة الآخرين حتى لو كان مزاحًا\n"
    "يمنع استخدام البلقين منعًا باتًا\n"
    "يمنع نشر التحذيرات أو محتوى تذاكر الدعم\n"
    "عدم إزعاج الإدارة إلا للضرورة\n"
    "يمنع المواضيع الخارجة عن حدود الآداب العامة\n"
    "يمنع طلب الرتب أو التلميح لذلك\n"
    "يمنع طلب المال أو أي شيء مماثل\n"
    "يمنع التطرق للسياسة أو الدين أو العنصرية\n"
    "يمنع وضع صورة أو اسم غير لائق\n"
    "يمنع الحرق إلا البثوث\n"
    "لكل شات وظيفة مخصصة\n"
    "يمنع إعطاء حسابك لأشخاص آخرين\n"
    "يمنع البيع والشراء والترويج بجميع أنواعه\n"
    "يمنع السبام بكل أشكاله\n\n"
    "إذا عندك مشكلة توجه للدعم الفني."
)

PUBLIC_CHAT_RULES_TEXT = (
    "**🗨️ قوانين الشات العام**\n\n"
    "الحد المسموح للإيموجيات 15 فقط\n"
    "الحد المسموح للمنشن 10 فقط\n"
    "الحد المسموح بالحروف 350\n"
    "ممنوع مواضيع الحب\n"
    "يمنع منشن الإدارة العليا\n"
    "مسموح العربية والإنجليزية فقط\n"
    "يمنع فتح مواضيع مشكوك فيها\n"
    "يمنع تشويه منظر الشات\n"
    "يمنع انتحال شغل الإدارة"
)

EVENT_CHAT_RULES_TEXT = (
    "**🎉 قوانين شات الفعاليات**\n\n"
    "عدم الاحتجاج أو المظاهرات\n"
    "عدم التحالف بجميع أشكاله\n"
    "يمنع الكراهية بجميع أشكالها\n"
    "يمنع الحقد الطويل"
)

NEW_TEXT = (
    "🍀 **New**\n\n"
    "هذا القسم يساعدك تبدأ بالسيرفر.\n\n"
    f"إذا عندك مشكلة أو استفسار توجه إلى <#{SUPPORT_CHANNEL_ID}>."
)

SOCIAL_TEXT = (
    "🌐 **وسائل التواصل الاجتماعي**\n\n"
    f"{EMOJI_KICK} **[Kick]({LINK_KICK})**\n"
    f"{EMOJI_TWIT} **[Twitter]({LINK_TWITTER})**\n"
    f"{EMOJI_INSTA} **[Instagram]({LINK_INSTAGRAM})**\n"
    f"{EMOJI_WA} **[WhatsApp]({LINK_WHATSAPP})**\n"
    f"{EMOJI_TIKTOK} **[TikTok]({LINK_TIKTOK})**"
)

INFO_FULL_TEXT = (
    "🌟 **دليل أقسام السيرفر** 🌟\n\n"
    f"👋 الترحيب: <#{WELCOME_CHANNEL_ID}>\n"
    f"💬 الشات العام: <#{CHAT_CHANNEL_ID}>\n"
    f"📜 القوانين: <#{RULES_CHANNEL_ID}>\n"
    f"💡 الاقتراحات: <#{SUGGESTIONS_CHANNEL_ID}>\n"
    f"🛠️ الدعم: <#{SUPPORT_CHANNEL_ID}>\n"
    f"⭐ اللفلات: <#{LEVEL_ANNOUNCE_CHANNEL_ID}>"
)

ROLES_INFO_TEXT = (
    "## 👑 Owner\n"
    f"<@{OWNER_USER_ID}>\n"
    "صاحب السيرفر وله التحكم الكامل في كل شيء\n\n"
    "## 🏆 High Management\n"
    f"<@&{SERVER_DEVELOPER_ROLE_ID}>\n"
    "مسؤول عن السيرفر كامل والبوتات وجميع أعضاء الإدارة\n\n"
    f"<@&{ADMINISTRATOR_ROLE_ID}>\n"
    "رتبة إدارية عليا مخصصة للإدارة الأساسية\n\n"
    f"<@&{FOUNDER_ROLE_ID}>\n"
    "أقوى رتبة إدارية ولديه جميع الصلاحيات\n\n"
    "## 👨‍💼 Staff Roles\n"
    f"<@&{HIGH_ADMIN_ROLE_ID}>\n"
    "إداري عالي ولديه صلاحيات قوية جدًا\n\n"
    f"<@&{MID_ADMIN_ROLE_ID}>\n"
    "إداري متوسط ولديه صلاحيات قوية\n\n"
    f"<@&{MODERATOR_ROLE_ID}>\n"
    "إداري ذو خبرة وصلاحيات متقدمة\n\n"
    f"<@&{JUNIOR_ADMIN_ROLE_ID}>\n"
    "إداري مبتدئ في بداية مسيرته\n\n"
    f"<@&{SUPPORT_ROLE_ID}>\n"
    "إدارة خاصة للرجال مسؤولة عن مساعدة الأعضاء\n\n"
    f"<@&{GIRL_SUPPORT_ROLE_ID}>\n"
    "إدارة خاصة للبنات مسؤولة عن المساعدة\n\n"
    f"<@&{KICK_MOD_ROLE_ID}>\n"
    "مود في بثوث كيك ومسؤول عن تنظيم الشات\n\n"
    "## 🧩 General Roles\n"
    f"<@&{GENERAL_ROLE_ID}>\n"
    "رتبة عامة تُعطى لجميع الأعضاء\n\n"
    f"<@&{KICK_VISITORS_ROLE_ID}>\n"
    "رتبة للأعضاء القادمين من بثوث كيك\n\n"
    f"<@&{SERVER_SUPPORTER_ROLE_ID}>\n"
    "رتبة لداعمي السيرفر بالبوست ولهم مزايا خاصة\n\n"
    f"<@&{VIP_ROLE_ID}>\n"
    "رتبة VIP لأشخاص مميزين أو من طرف تركي"
)

LEVEL_ROLES_INFO_TEXT = (
    f"🌱 <@&1488950677672820976>\n"
    "LVL │ 1 → 49\n"
    "بداية النشاط للأعضاء الجدد\n\n"
    f"🔥 <@&1488951219060867103>\n"
    "LVL │ 50 → 149\n"
    "ينضم إلى مجتمع المتميزين ويتضمن البوسترز، الاستريمرز، والأعضاء المميزين\n\n"
    f"⚡ <@&1488951358005706913>\n"
    "LVL │ 150 → 299\n"
    "عضو محترف ونشيط بشكل كبير\n\n"
    f"💎 <@&1488952288038093100>\n"
    "LVL │ 300 → 499\n"
    "نشاط عالي وتفاعل قوي داخل السيرفر\n\n"
    f"👑 <@&1488952584772522024>\n"
    "LVL │ 500 → 699\n"
    "عضو مميز وحضوره قوي جدًا\n\n"
    f"🗡️ <@&1488952786866540604>\n"
    "LVL │ 700 → 899\n"
    "من الأعضاء النادرين شديدي النشاط\n\n"
    f"🧪 <@&1488952921021223105>\n"
    "LVL │ 900 → 1000\n"
    "أعلى مستوى وأقوى نشاط في السيرفر 🔥"
)

STAFF_TERMS_TEXT = (
    "# الاستبيان\n\n"
    "**الاستبيان | التقديم على الإدارة**\n\n"
    "تفاعلك كتابياً وصوتياً بشكل جيد ، وتفاعلك المستمر في الشات\n"
    "سجلك خالي من المشاكل\n"
    "بعض الملاحظات\n"
    "في حال انقبلت بتجي لك الرتب الإدارية إلى أنت مقدم لها وفي حال رفضك ما بتجي الرتبة ولا يتم إخبارك\n"
    "يمنع طلب القبول من الإدارة المسؤولة في حال الطلب سوف تتعرض للعقوبات\n"
    "عدم قبولك في المرة الأولى لا يعني أنه لا تستطيع إعادة المحاولة\n"
    "تستطيع التقديم في أي وقت إذا كنت تستوفي الشروط\n"
    "في حال ما عندك خبرة بيتم تعليمك بشكل كامل\n"
    "التفاعل كتابياً يرفع من نسبة قبولك"
)

KICK_TERMS_TEXT = (
    "# الاستبيان\n\n"
    "**الاستبيان | التقديم على كيك ستاف**\n\n"
    "تفاعلك كتابياً بشكل جيد ، وتفاعلك المستمر في شات كيك\n"
    "سجلك خالي من المشاكل\n"
    "بعض الملاحظات\n"
    "في حال انقبلت بتجي لك الرتبة كيك ستاف إلى أنت مقدم لها وفي حال رفضك ما بتجي الرتبة ولا يتم إخبارك\n"
    "يمنع طلب القبول من الإدارة المسؤولة في حال الطلب سوف تتعرض للعقوبات\n"
    "عدم قبولك في المرة الأولى لا يعني أنه لا تستطيع إعادة المحاولة\n"
    "تستطيع التقديم في أي وقت إذا كنت تستوفي الشروط\n"
    "في حال ما عندك خبرة بيتم تعليمك بشكل كامل\n"
    "لفل 20 كتابياً يرفع من نسبة قبولك"
)

# =========================================================
# STORAGE
# =========================================================
def default_db() -> dict:
    return {
        "ticket_counter": 0,
        "tickets": {},
        "user_open_ticket": {},
        "message_counts": {},
        "support_message_counts": {},
        "warnings": {},
        "levels": {},
    }

def load_json_file(path: str, default):
    if not os.path.exists(path):
        return default
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default

def save_json_file(path: str, data) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

db = load_json_file(DB_FILE, default_db())
sugg_state = load_json_file(SUGG_STATE_FILE, {})
application_state = load_json_file(APPLICATION_STATE_FILE, {})
xp_cooldowns: dict[str, float] = {}

def save_db():
    save_json_file(DB_FILE, db)

def save_sugg_state():
    save_json_file(SUGG_STATE_FILE, sugg_state)

def save_application_state():
    save_json_file(APPLICATION_STATE_FILE, application_state)

# =========================================================
# HELPERS
# =========================================================
def make_embed(title: str, description: str = "", color: int = EMBED_COLOR) -> discord.Embed:
    return discord.Embed(title=title, description=description, color=color)

def now_utc() -> datetime:
    return datetime.now(timezone.utc)

def iso_now() -> str:
    return now_utc().isoformat()

def parse_iso(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        return datetime.fromisoformat(value)
    except Exception:
        return None

def fmt_dt(dt: Optional[datetime]) -> str:
    if not dt:
        return "Unknown"
    return discord.utils.format_dt(dt, style="F")

def user_has_any_role(member: discord.Member, role_ids: set[int]) -> bool:
    return any(role.id in role_ids for role in member.roles)

def sanitize_name(text: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in text)
    while "--" in cleaned:
        cleaned = cleaned.replace("--", "-")
    return cleaned.strip("-")[:40] or "user"

def ensure_guild_bucket(container: dict, guild_id: int) -> dict:
    key = str(guild_id)
    if key not in container:
        container[key] = {}
    return container[key]

def increment_message_count(guild_id: int, user_id: int, support: bool = False) -> None:
    bucket = ensure_guild_bucket(db["message_counts"], guild_id)
    uid = str(user_id)
    bucket[uid] = bucket.get(uid, 0) + 1
    if support:
        support_bucket = ensure_guild_bucket(db["support_message_counts"], guild_id)
        support_bucket[uid] = support_bucket.get(uid, 0) + 1
    save_db()

def top_member(guild_id: int, support: bool = False) -> Optional[tuple[int, int]]:
    source = db["support_message_counts"] if support else db["message_counts"]
    bucket = source.get(str(guild_id), {})
    if not bucket:
        return None
    uid, count = max(bucket.items(), key=lambda item: item[1])
    return int(uid), int(count)

def reset_counts(guild_id: int, support: bool = False) -> None:
    source = db["support_message_counts"] if support else db["message_counts"]
    source[str(guild_id)] = {}
    save_db()

def add_warning(guild_id: int, user_id: int) -> int:
    bucket = ensure_guild_bucket(db["warnings"], guild_id)
    uid = str(user_id)
    bucket[uid] = int(bucket.get(uid, 0)) + 1
    save_db()
    return bucket[uid]

def remove_warning(guild_id: int, user_id: int) -> int:
    bucket = ensure_guild_bucket(db["warnings"], guild_id)
    uid = str(user_id)
    current = int(bucket.get(uid, 0))
    if current > 0:
        bucket[uid] = current - 1
    save_db()
    return int(bucket.get(uid, 0))

def parse_duration(text: str) -> Optional[timedelta]:
    text = text.strip().lower()
    if not text:
        return None
    try:
        unit = text[-1]
        value = int(text[:-1])
    except Exception:
        return None
    if value <= 0:
        return None
    if unit == "s":
        return timedelta(seconds=value)
    if unit == "m":
        return timedelta(minutes=value)
    if unit == "h":
        return timedelta(hours=value)
    if unit == "d":
        return timedelta(days=value)
    return None

def get_required_roles_text(guild: discord.Guild) -> str:
    lines = []
    for role_id in EXTRA_TICKET_PERMISSION_ROLE_IDS:
        role = guild.get_role(role_id)
        lines.append(f"• {role.mention if role else f'<@&{role_id}>'}")
    return "\n".join(lines)

def support_command_allowed(member: discord.Member) -> bool:
    return user_has_any_role(member, {SUPPORT_ROLE_ID, GIRL_SUPPORT_ROLE_ID, ADMINISTRATOR_ROLE_ID})

def best_reset_allowed(member: discord.Member) -> bool:
    return user_has_any_role(member, {ADMINISTRATOR_ROLE_ID})

def say_allowed(member: discord.Member) -> bool:
    return user_has_any_role(member, {FOUNDER_ROLE_ID, ADMINISTRATOR_ROLE_ID})

def jail_allowed(member: discord.Member) -> bool:
    return user_has_any_role(
        member,
        {
            FOUNDER_ROLE_ID,
            ADMINISTRATOR_ROLE_ID,
            HIGH_ADMIN_ROLE_ID,
            MID_ADMIN_ROLE_ID,
            MODERATOR_ROLE_ID,
            JUNIOR_ADMIN_ROLE_ID,
            SUPPORT_ROLE_ID,
            GIRL_SUPPORT_ROLE_ID,
        },
    )

def application_review_allowed(member: discord.Member) -> bool:
    return jail_allowed(member)

def ticket_button_allowed(member: discord.Member, ticket_role_id: int) -> bool:
    allowed_roles = set(EXTRA_TICKET_PERMISSION_ROLE_IDS)
    allowed_roles.add(ticket_role_id)
    allowed_roles.add(ADMINISTRATOR_ROLE_ID)
    return user_has_any_role(member, allowed_roles)

def get_ticket_type_config(ticket_type: str) -> dict:
    return {
        "support": {"label": "Support Ticket", "role_id": SUPPORT_ROLE_ID, "prefix": "support"},
        "girl": {"label": "Girl Ticket", "role_id": GIRL_SUPPORT_ROLE_ID, "prefix": "girl"},
        "administrator": {"label": "Administrator Ticket", "role_id": ADMINISTRATOR_ROLE_ID, "prefix": "admin"},
    }[ticket_type]

def get_level_bucket(guild_id: int) -> dict:
    return ensure_guild_bucket(db["levels"], guild_id)

def get_user_level_data(guild_id: int, user_id: int) -> dict:
    bucket = get_level_bucket(guild_id)
    uid = str(user_id)
    if uid not in bucket:
        bucket[uid] = {"xp": 0, "level": 0}
    return bucket[uid]

def xp_needed_for_next_level(current_level: int) -> int:
    return 100 + (current_level * current_level * 5)

def get_level_role(level: int) -> Optional[dict]:
    for item in LEVEL_ROLE_MAP:
        if item["min"] <= level <= item["max"]:
            return item
    return None

async def update_level_role(member: discord.Member, old_level: int, new_level: int) -> Optional[int]:
    old_role_info = get_level_role(old_level)
    new_role_info = get_level_role(new_level)
    if not new_role_info:
        return None

    old_role_id = old_role_info["role_id"] if old_role_info else None
    new_role_id = new_role_info["role_id"]

    if old_role_id == new_role_id and any(r.id == new_role_id for r in member.roles):
        return None

    remove_roles = []
    for item in LEVEL_ROLE_MAP:
        role = member.guild.get_role(item["role_id"])
        if role and role in member.roles:
            remove_roles.append(role)

    new_role = member.guild.get_role(new_role_id)
    if not new_role:
        return None

    try:
        if remove_roles:
            await member.remove_roles(*remove_roles, reason="Level role update")
        await member.add_roles(new_role, reason="Level role update")
        return new_role_id
    except Exception:
        return None

async def process_leveling(message: discord.Message) -> None:
    if not message.guild or not isinstance(message.author, discord.Member):
        return
    if message.author.bot:
        return

    cooldown_key = f"{message.guild.id}:{message.author.id}"
    now_ts = time.time()
    if now_ts - xp_cooldowns.get(cooldown_key, 0) < 10:
        return
    xp_cooldowns[cooldown_key] = now_ts

    data = get_user_level_data(message.guild.id, message.author.id)
    old_level = int(data.get("level", 0))
    data["xp"] = int(data.get("xp", 0)) + 10

    leveled_up = False
    while data["xp"] >= xp_needed_for_next_level(int(data["level"])):
        data["level"] = int(data["level"]) + 1
        leveled_up = True

    save_db()

    new_level = int(data["level"])
    if not leveled_up or new_level <= old_level:
        return

    new_role_id = await update_level_role(message.author, old_level, new_level)

    announce_channel = message.guild.get_channel(LEVEL_ANNOUNCE_CHANNEL_ID)
    if isinstance(announce_channel, discord.TextChannel):
        text = (
            f"🥳 Congratulations, {message.author.mention}!\n"
            f"You climbed from level {old_level} to {new_level}. Keep it up!"
        )
        if new_role_id:
            text += f"\n\n🎖️ New Role: <@&{new_role_id}>"
        await announce_channel.send(text)

async def send_permission_error(interaction: discord.Interaction) -> None:
    if not interaction.guild:
        return
    embed = make_embed(
        "Permission System",
        "You do not have permission to use this command.\n\n"
        "• Required roles:\n"
        f"{get_required_roles_text(interaction.guild)}",
        ERROR_COLOR,
    )
    embed.set_image(url=FAIL_IMAGE_URL)
    if interaction.response.is_done():
        await interaction.followup.send(embed=embed, ephemeral=True)
    else:
        await interaction.response.send_message(embed=embed, ephemeral=True)

# =========================================================
# APPLY SYSTEM
# =========================================================
class ApplyStartView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="Staff Apply", style=discord.ButtonStyle.primary)
    async def staff_apply(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = make_embed("", STAFF_TERMS_TEXT, EMBED_COLOR)
        await interaction.response.edit_message(embed=embed, view=StaffTermsView())

    @discord.ui.button(label="Kick Apply", style=discord.ButtonStyle.secondary)
    async def kick_apply(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = make_embed("", KICK_TERMS_TEXT, EMBED_COLOR)
        await interaction.response.edit_message(embed=embed, view=KickTermsView())

class StaffTermsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="I have read and agree to the terms", style=discord.ButtonStyle.success)
    async def agree(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(StaffApplyModal())

    @discord.ui.button(label="Back", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=apply_start_embed(), view=ApplyStartView())

class KickTermsView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="I have read and agree to the terms", style=discord.ButtonStyle.success)
    async def agree(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_modal(KickApplyModal())

    @discord.ui.button(label="Back", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.edit_message(embed=apply_start_embed(), view=ApplyStartView())

class StaffApplyModal(discord.ui.Modal, title="Server Staff Application"):
    name = discord.ui.TextInput(label="الاسم", placeholder="اكتب اسمك", max_length=100)
    age = discord.ui.TextInput(label="العمر", placeholder="اكتب عمرك", max_length=10)
    activity = discord.ui.TextInput(label="مدة تفاعلك؟", placeholder="اكتب مدة تفاعلك", max_length=100)
    mic = discord.ui.TextInput(label="هل لديك تفاعل صوتي (مايك)؟", placeholder="نعم أو لا", max_length=20)
    experience = discord.ui.TextInput(label="اذكر سيرفرات كنت إداري فيها", placeholder="اكتب أسماء السيرفرات أو خبرتك", style=discord.TextStyle.paragraph, max_length=1000)

    async def on_submit(self, interaction: discord.Interaction):
        await interaction.response.send_modal(StaffApplyExtraModal(
            self.name.value,
            self.age.value,
            self.activity.value,
            self.mic.value,
            self.experience.value
        ))

class StaffApplyExtraModal(discord.ui.Modal, title="Server Staff Application"):
    why = discord.ui.TextInput(label="ليش نختارك للإدارة؟", placeholder="اقنعنا ليش أنت مناسب", style=discord.TextStyle.paragraph, max_length=1000)
    previous = discord.ui.TextInput(label="هل كنت إداري سابق معنا؟", placeholder="نعم / لا", max_length=10)

    def __init__(self, name: str, age: str, activity: str, mic: str, experience: str):
        super().__init__()
        self.name_value = name
        self.age_value = age
        self.activity_value = activity
        self.mic_value = mic
        self.experience_value = experience

    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.guild or not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("This can only be used in a server.", ephemeral=True)
            return

        channel = interaction.guild.get_channel(STAFF_APPLY_CHANNEL_ID)
        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message("روم التقديمات غير موجود.", ephemeral=True)
            return

        embed = make_embed("📋 طلب تقديم جديد", "", EMBED_COLOR)
        embed.add_field(name="👤 العضو", value=interaction.user.mention, inline=False)
        embed.add_field(name="📝 النوع", value="Staff Apply", inline=False)
        embed.add_field(name="الاسم", value=self.name_value, inline=True)
        embed.add_field(name="العمر", value=self.age_value, inline=True)
        embed.add_field(name="مدة التفاعل", value=self.activity_value, inline=False)
        embed.add_field(name="هل عنده مايك", value=self.mic_value, inline=True)
        embed.add_field(name="سيرفرات/خبرة", value=self.experience_value[:1024], inline=False)
        embed.add_field(name="ليش نختارك", value=self.why.value[:1024], inline=False)
        embed.add_field(name="هل كان إداري سابق معنا", value=self.previous.value, inline=False)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.timestamp = now_utc()

        sent = await channel.send(embed=embed, view=ApplicationActionView())
        application_state[str(sent.id)] = {
            "type": "staff",
            "user_id": interaction.user.id,
            "channel_id": channel.id,
            "status": "pending",
        }
        save_application_state()
        await interaction.response.send_message("✅ تم إرسال تقديمك بنجاح.", ephemeral=True)

class KickApplyModal(discord.ui.Modal, title="Kick Staff Application"):
    name_age = discord.ui.TextInput(label="الاسم والعمر؟", placeholder="أدخل اسمك وعمرك", max_length=100)
    know = discord.ui.TextInput(label="كيف تعرفت على تركي؟", placeholder="اكتب كيف تعرفت على تركي", max_length=300)
    watch = discord.ui.TextInput(label="ما مدى متابعتك للبثوث؟", placeholder="(نادراً = 1 | دائماً = 10)", max_length=50)
    activity = discord.ui.TextInput(label="مدة تفاعلك؟", placeholder="اكتب ساعات تفاعلك هنا", max_length=100)
    experience = discord.ui.TextInput(label="هل لديك خبرة في الإدارة؟", placeholder="اذكر خبرتك إن وجدت", style=discord.TextStyle.paragraph, max_length=1000)

    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.guild or not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("This can only be used in a server.", ephemeral=True)
            return

        channel = interaction.guild.get_channel(KICK_APPLY_CHANNEL_ID)
        if not isinstance(channel, discord.TextChannel):
            await interaction.response.send_message("روم تقديم كيك غير موجود.", ephemeral=True)
            return

        embed = make_embed("📋 طلب تقديم جديد", "", EMBED_COLOR)
        embed.add_field(name="👤 العضو", value=interaction.user.mention, inline=False)
        embed.add_field(name="📝 النوع", value="Kick Apply", inline=False)
        embed.add_field(name="الاسم والعمر", value=self.name_age.value, inline=False)
        embed.add_field(name="كيف تعرفت على تركي", value=self.know.value, inline=False)
        embed.add_field(name="مدى متابعتك للبثوث", value=self.watch.value, inline=False)
        embed.add_field(name="مدة تفاعلك", value=self.activity.value, inline=False)
        embed.add_field(name="هل لديك خبرة", value=self.experience.value[:1024], inline=False)
        embed.set_thumbnail(url=interaction.user.display_avatar.url)
        embed.timestamp = now_utc()

        sent = await channel.send(embed=embed, view=ApplicationActionView())
        application_state[str(sent.id)] = {
            "type": "kick",
            "user_id": interaction.user.id,
            "channel_id": channel.id,
            "status": "pending",
        }
        save_application_state()
        await interaction.response.send_message("✅ تم إرسال تقديمك بنجاح.", ephemeral=True)

class ApplicationActionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="قبول", style=discord.ButtonStyle.success, custom_id="application_accept")
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.message:
            return
        await handle_application_action(interaction, interaction.message.id, "accept")

    @discord.ui.button(label="رفض", style=discord.ButtonStyle.danger, custom_id="application_reject")
    async def reject(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.message:
            return
        await handle_application_action(interaction, interaction.message.id, "reject")

    @discord.ui.button(label="قبول بسبب", style=discord.ButtonStyle.primary, custom_id="application_accept_reason")
    async def accept_reason(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.message:
            return
        await interaction.response.send_modal(ApplicationReasonModal(interaction.message.id, "accept_reason"))

    @discord.ui.button(label="رفض بسبب", style=discord.ButtonStyle.secondary, custom_id="application_reject_reason")
    async def reject_reason(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.message:
            return
        await interaction.response.send_modal(ApplicationReasonModal(interaction.message.id, "reject_reason"))

class ApplicationReasonModal(discord.ui.Modal, title="سبب القرار"):
    reason = discord.ui.TextInput(label="السبب", placeholder="اكتب السبب", style=discord.TextStyle.paragraph, max_length=1000)

    def __init__(self, message_id: int, action: str):
        super().__init__()
        self.message_id = message_id
        self.action = action

    async def on_submit(self, interaction: discord.Interaction):
        await handle_application_action(interaction, self.message_id, self.action, self.reason.value)

async def handle_application_action(interaction: discord.Interaction, message_id: int, action: str, reason: Optional[str] = None):
    if not interaction.guild or not isinstance(interaction.user, discord.Member):
        return

    if not application_review_allowed(interaction.user):
        await interaction.response.send_message("❌ ما عندك صلاحية", ephemeral=True)
        return

    record = application_state.get(str(message_id))
    if not record:
        await interaction.response.send_message("❌ هذا التقديم غير موجود.", ephemeral=True)
        return

    if record.get("status") != "pending":
        await interaction.response.send_message("تم اتخاذ قرار مسبق على هذا التقديم.", ephemeral=True)
        return

    member = interaction.guild.get_member(int(record["user_id"]))
    if not member:
        await interaction.response.send_message("❌ العضو غير موجود بالسيرفر.", ephemeral=True)
        return

    accepted = action in {"accept", "accept_reason"}
    rejected = action in {"reject", "reject_reason"}

    if accepted:
        record["status"] = "accepted"
        try:
            role = interaction.guild.get_role(APPLICATION_ACCEPT_ROLE_ID)
            if role:
                await member.add_roles(role, reason=f"Application accepted by {interaction.user}")
        except Exception:
            pass

        dm_text = (
            "🎉 ألف مبروك!\n\n"
            "تم قبولك في الإدارة بنجاح 👑\n"
            "نبارك لك انضمامك لفريق العمل ونتمنى لك التوفيق والتميز معنا 🔥\n\n"
            "حافظ على نشاطك والتزامك وكن قد المسؤولية 💪"
        )
        if reason:
            dm_text = (
                "🎉 ألف مبروك!\n\n"
                "تم قبولك في الإدارة 👑\n"
                f"السبب: {reason}\n\n"
                "نتمنى لك التوفيق والنجاح معنا 🔥"
            )
        try:
            await member.send(dm_text)
        except Exception:
            pass

    if rejected:
        record["status"] = "rejected"
        dm_text = "تم رفض تقديمك."
        if reason:
            dm_text = f"تم رفض تقديمك.\nالسبب: {reason}"
        try:
            await member.send(dm_text)
        except Exception:
            pass

    save_application_state()

    try:
        if isinstance(interaction.channel, discord.TextChannel):
            message = await interaction.channel.fetch_message(message_id)
            if message.embeds:
                embed = discord.Embed.from_dict(message.embeds[0].to_dict())
                status_value = "✅ مقبول" if accepted else "❌ مرفوض"
                if reason:
                    status_value += f"\nالسبب: {reason}"
                embed.add_field(name="قرار الإدارة", value=status_value, inline=False)
                await message.edit(embed=embed, view=None)
    except Exception:
        pass

    if interaction.response.is_done():
        await interaction.followup.send("✅ تم تحديث حالة التقديم.", ephemeral=True)
    else:
        await interaction.response.send_message("✅ تم تحديث حالة التقديم.", ephemeral=True)

# =========================================================
# TICKET SYSTEM
# =========================================================
class FeedbackView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def send_rating(self, interaction: discord.Interaction, stars: int):
        embed = make_embed("Thank you", f"Your feedback has been received: {'⭐' * stars}", SUCCESS_COLOR)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="⭐", style=discord.ButtonStyle.secondary, custom_id="feedback_1")
    async def one(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_rating(interaction, 1)

    @discord.ui.button(label="⭐⭐", style=discord.ButtonStyle.secondary, custom_id="feedback_2")
    async def two(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_rating(interaction, 2)

    @discord.ui.button(label="⭐⭐⭐", style=discord.ButtonStyle.secondary, custom_id="feedback_3")
    async def three(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_rating(interaction, 3)

    @discord.ui.button(label="⭐⭐⭐⭐", style=discord.ButtonStyle.secondary, custom_id="feedback_4")
    async def four(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_rating(interaction, 4)

    @discord.ui.button(label="⭐⭐⭐⭐⭐", style=discord.ButtonStyle.secondary, custom_id="feedback_5")
    async def five(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.send_rating(interaction, 5)

class TicketActionView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Claim", style=discord.ButtonStyle.secondary, custom_id="ticket_claim_btn")
    async def claim_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild or not interaction.channel:
            return

        ticket = db["tickets"].get(str(interaction.channel.id))
        if not ticket:
            await interaction.response.send_message("This ticket record was not found.", ephemeral=True)
            return

        role_id = int(ticket["responsible_role_id"])
        if not isinstance(interaction.user, discord.Member) or not ticket_button_allowed(interaction.user, role_id):
            await send_permission_error(interaction)
            return

        if ticket.get("claimed_by"):
            member = interaction.guild.get_member(int(ticket["claimed_by"]))
            await interaction.response.send_message(
                f"This ticket is already claimed by {member.mention if member else 'someone'}.",
                ephemeral=True
            )
            return

        ticket["claimed_by"] = interaction.user.id
        ticket["claimed_at"] = iso_now()
        save_db()

        embed = make_embed("Ticket System", f"The ticket has been claimed by {interaction.user.mention}.", SUCCESS_COLOR)
        embed.set_image(url=SUCCESS_IMAGE_URL)
        await interaction.response.send_message(embed=embed)

    @discord.ui.button(label="Close", style=discord.ButtonStyle.secondary, custom_id="ticket_close_btn")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if not interaction.guild or not interaction.channel:
            return

        ticket = db["tickets"].get(str(interaction.channel.id))
        if not ticket:
            await interaction.response.send_message("This ticket record was not found.", ephemeral=True)
            return

        role_id = int(ticket["responsible_role_id"])
        if not isinstance(interaction.user, discord.Member) or not ticket_button_allowed(interaction.user, role_id):
            await send_permission_error(interaction)
            return

        guild = interaction.guild
        opener_id = int(ticket["opener_id"])
        opener = guild.get_member(opener_id)
        claimed_by = guild.get_member(int(ticket["claimed_by"])) if ticket.get("claimed_by") else None
        opened_at = parse_iso(ticket.get("opened_at"))
        closed_at = now_utc()
        reason = ticket.get("reason", "No reason")
        ticket_label = ticket.get("ticket_label", "Unknown Ticket")
        ticket_id = ticket.get("ticket_id", 0)

        if opener:
            try:
                summary = make_embed(
                    "Your ticket has been closed.",
                    (
                        f"**Opened By:** {opener.mention}\n"
                        f"**Claimed By:** {(claimed_by.mention if claimed_by else 'Not claimed')}\n"
                        f"**Reason:** {reason}\n"
                        f"**Closed By:** {interaction.user.mention}\n"
                        f"**Opened At:** {fmt_dt(opened_at)}\n"
                        f"**Closed At:** {fmt_dt(closed_at)}\n"
                        f"**Ticket ID:** {ticket_id}"
                    ),
                    EMBED_COLOR
                )
                await opener.send(embed=summary)

                feedback = make_embed("We value your feedback", "Please rate your experience:", EMBED_COLOR)
                await opener.send(embed=feedback, view=FeedbackView())
            except Exception:
                pass

        log_channel = guild.get_channel(TICKET_CLOSE_LOG_CHANNEL_ID)
        if isinstance(log_channel, discord.TextChannel):
            opener_mention = opener.mention if opener else f"<@{opener_id}>"
            claimed_mention = claimed_by.mention if claimed_by else "Not claimed"
            log_embed = make_embed(
                "Ticket Closed",
                (
                    f"**User:** {opener_mention}\n"
                    f"**Claimed By:** {claimed_mention}\n"
                    f"**Ticket Type:** {ticket_label}\n"
                    f"**Reason:** {reason}"
                ),
                EMBED_COLOR
            )
            await log_channel.send(embed=log_embed)

        db["user_open_ticket"].pop(str(opener_id), None)
        db["tickets"].pop(str(interaction.channel.id), None)
        save_db()

        await interaction.response.send_message("Closing ticket...", ephemeral=True)
        await asyncio.sleep(1)

        try:
            await interaction.channel.delete(reason=f"Ticket closed by {interaction.user}")
        except Exception:
            pass

class TicketReasonModal(discord.ui.Modal, title="Ticket System"):
    reason = discord.ui.TextInput(
        label="Reason",
        placeholder="Please provide all the details of the reason for opening the ticket.",
        style=discord.TextStyle.paragraph,
        required=True,
        max_length=1000,
    )

    def __init__(self, ticket_type_key: str):
        super().__init__()
        self.ticket_type_key = ticket_type_key

    async def on_submit(self, interaction: discord.Interaction):
        if not interaction.guild or not isinstance(interaction.user, discord.Member):
            await interaction.response.send_message("This can only be used in a server.", ephemeral=True)
            return

        user_id_key = str(interaction.user.id)
        existing_channel_id = db["user_open_ticket"].get(user_id_key)

        if existing_channel_id:
            ch = interaction.guild.get_channel(int(existing_channel_id))
            if ch:
                await interaction.response.send_message(f"You already have an open ticket: {ch.mention}", ephemeral=True)
                return
            db["user_open_ticket"].pop(user_id_key, None)
            save_db()

        cfg = get_ticket_type_config(self.ticket_type_key)
        responsible_role = interaction.guild.get_role(cfg["role_id"])

        db["ticket_counter"] += 1
        ticket_id = db["ticket_counter"]
        save_db()

        channel_name = f"{cfg['prefix']}-{sanitize_name(interaction.user.display_name)}-{ticket_id}"
        bot_member = interaction.guild.me or interaction.guild.get_member(bot.user.id)

        overwrites = {
            interaction.guild.default_role: discord.PermissionOverwrite(view_channel=False),
            interaction.user: discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                attach_files=True,
                embed_links=True,
            )
        }

        if bot_member:
            overwrites[bot_member] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                manage_channels=True,
                manage_messages=True,
            )

        if responsible_role:
            overwrites[responsible_role] = discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                manage_messages=True,
            )

        category = interaction.channel.category if isinstance(interaction.channel, discord.TextChannel) else None

        ticket_channel = await interaction.guild.create_text_channel(
            name=channel_name,
            category=category,
            overwrites=overwrites,
            reason=f"Ticket opened by {interaction.user}"
        )

        db["tickets"][str(ticket_channel.id)] = {
            "ticket_id": ticket_id,
            "ticket_label": cfg["label"],
            "ticket_type_key": self.ticket_type_key,
            "opener_id": interaction.user.id,
            "responsible_role_id": cfg["role_id"],
            "reason": str(self.reason),
            "opened_at": iso_now(),
            "claimed_by": None,
            "claimed_at": None,
        }
        db["user_open_ticket"][user_id_key] = ticket_channel.id
        save_db()

        request_log = interaction.guild.get_channel(TICKET_REQUEST_LOG_CHANNEL_ID)
        if isinstance(request_log, discord.TextChannel):
            mention_role = responsible_role.mention if responsible_role else f"<@&{cfg['role_id']}>"
            request_embed = make_embed(
                "Ticket Request",
                (
                    f"**User:** {interaction.user.mention}\n"
                    f"**Ticket Type:** {cfg['label']}\n"
                    f"**Reason:** {self.reason}\n"
                    f"**Responsible Role:** {mention_role}"
                ),
                EMBED_COLOR
            )
            await request_log.send(content=mention_role, embed=request_embed)

        responsible_mention = responsible_role.mention if responsible_role else f"<@&{cfg['role_id']}>"
        top_mentions = f"{interaction.user.mention} {responsible_mention}"

        wait_embed = make_embed(
            f"Ticket Created - {cfg['label']}",
            "Please wait for the staff to assist you, To save time, please write the full reason for opening the ticket.",
            WAIT_COLOR
        )
        wait_embed.set_image(url=WAIT_IMAGE_URL)

        reason_embed = make_embed("Ticket System - Reason", str(self.reason), WAIT_COLOR)

        await ticket_channel.send(content=top_mentions, allowed_mentions=discord.AllowedMentions(users=True, roles=True))
        await ticket_channel.send(embed=wait_embed)
        await ticket_channel.send(embed=reason_embed, view=TicketActionView())

        success_embed = make_embed(
            "Ticket Created",
            f"Your ticket has been created successfully in {ticket_channel.mention}.",
            SUCCESS_COLOR
        )
        success_embed.set_image(url=SUCCESS_IMAGE_URL)

        await interaction.response.send_message(
            embed=success_embed,
            view=GoToTicketView(ticket_channel),
            ephemeral=True
        )

class TicketTypeSelect(discord.ui.Select):
    def __init__(self):
        options = [
            discord.SelectOption(label="Support Ticket", description="Open a ticket for support.", value="support"),
            discord.SelectOption(label="Girl Ticket", description="Open a support ticket for girls only.", value="girl"),
            discord.SelectOption(label="Administrator Ticket", description="Open a ticket to speak to an administrator.", value="administrator"),
        ]
        super().__init__(
            placeholder="Please select a type to open a ticket.",
            min_values=1,
            max_values=1,
            options=options,
            custom_id="ticket_type_select"
        )

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_modal(TicketReasonModal(self.values[0]))

class TicketTypeView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)
        self.add_item(TicketTypeSelect())

class GoToTicketView(discord.ui.View):
    def __init__(self, channel: discord.TextChannel):
        super().__init__(timeout=300)
        self.add_item(discord.ui.Button(label="Go to Ticket", url=channel.jump_url))

class TicketPanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Open Ticket", style=discord.ButtonStyle.success, custom_id="open_ticket_btn")
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = make_embed(
            "Ticket System",
            "Welcome to the ticket system, here you can open a ticket and get help from the staff team.\n*Please read the rules before opening a ticket.*",
            EMBED_COLOR
        )
        embed.set_image(url=RULES_IMAGE_URL)
        await interaction.response.send_message(embed=embed, view=TicketTypeView(), ephemeral=True)

    @discord.ui.button(label="Some Information", style=discord.ButtonStyle.secondary, custom_id="ticket_info_btn")
    async def some_information(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = make_embed("Information", "", EMBED_COLOR)
        embed.set_image(url=INFO_IMAGE_URL)
        await interaction.response.send_message(embed=embed, ephemeral=True)

# =========================================================
# SUGGESTIONS
# =========================================================
def build_suggestion_embed(author: discord.Member, suggestion_text: str, yes_count: int, no_count: int, status: str) -> discord.Embed:
    status_text = "⏳ Pending Review"
    if status == "accepted":
        status_text = "✅ Accepted"
    elif status == "rejected":
        status_text = "❌ Rejected"

    embed = discord.Embed(title="📝 New Suggestion", color=EMBED_COLOR)
    embed.add_field(name="Suggestion:", value=suggestion_text[:1024], inline=False)
    embed.add_field(name="Status", value=status_text, inline=True)
    embed.add_field(name="Support", value=f"👍 {yes_count} | 👎 {no_count}", inline=True)
    embed.set_thumbnail(url=author.display_avatar.url)
    embed.set_footer(text=f"Suggested by {author.display_name}")
    embed.timestamp = now_utc()
    return embed

def build_suggestion_view(message_id: int, status: str) -> discord.ui.View:
    disabled = status in {"accepted", "rejected"}
    view = discord.ui.View(timeout=None)
    view.add_item(discord.ui.Button(label="Accept", style=discord.ButtonStyle.success, custom_id=f"sugg_admin_accept:{message_id}", disabled=disabled))
    view.add_item(discord.ui.Button(label="Reject", style=discord.ButtonStyle.danger, custom_id=f"sugg_admin_reject:{message_id}", disabled=disabled))
    view.add_item(discord.ui.Button(emoji="👍", style=discord.ButtonStyle.primary, custom_id=f"sugg_vote_yes:{message_id}", disabled=disabled))
    view.add_item(discord.ui.Button(emoji="👎", style=discord.ButtonStyle.primary, custom_id=f"sugg_vote_no:{message_id}", disabled=disabled))
    return view

def suggestion_staff_allowed(member: discord.Member) -> bool:
    return user_has_any_role(
        member,
        {
            SUPPORT_ROLE_ID,
            GIRL_SUPPORT_ROLE_ID,
            ADMINISTRATOR_ROLE_ID,
            FOUNDER_ROLE_ID,
            HIGH_ADMIN_ROLE_ID,
            MID_ADMIN_ROLE_ID,
            MODERATOR_ROLE_ID,
            JUNIOR_ADMIN_ROLE_ID,
        }
    )
# =========================================================
# PANEL SYSTEM
# =========================================================

class PanelView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="القوانين", style=discord.ButtonStyle.secondary, custom_id="panel_rules")
    async def rules(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = make_embed("📜 القوانين", SERVER_RULES_TEXT, EMBED_COLOR)
        embed.set_image(url=RULES_IMAGE_URL)
        await interaction.response.send_message(embed=embed, view=RulesSubView(), ephemeral=True)

    @discord.ui.button(label="المعلومات", style=discord.ButtonStyle.secondary, custom_id="panel_info")
    async def info(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = make_embed("📖 المعلومات", INFO_FULL_TEXT, EMBED_COLOR)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="السوشال", style=discord.ButtonStyle.secondary, custom_id="panel_social")
    async def social(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = make_embed("🌐 السوشال", SOCIAL_TEXT, EMBED_COLOR)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="الرتب", style=discord.ButtonStyle.secondary, custom_id="panel_roles")
    async def roles(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = make_embed("🎭 الرتب", ROLES_INFO_TEXT, EMBED_COLOR)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="لفلات", style=discord.ButtonStyle.secondary, custom_id="panel_levels")
    async def levels(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = make_embed("⭐ لفلات", LEVEL_ROLES_INFO_TEXT, EMBED_COLOR)
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="التقديم", style=discord.ButtonStyle.success, custom_id="panel_apply")
    async def apply(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.send_message(embed=apply_start_embed(), view=ApplyStartView(), ephemeral=True)


class RulesSubView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="الشات العام", style=discord.ButtonStyle.secondary)
    async def chat(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = make_embed("🗨️ قوانين الشات", PUBLIC_CHAT_RULES_TEXT, EMBED_COLOR)
        await interaction.response.edit_message(embed=embed, view=RulesBackView())

    @discord.ui.button(label="الفعاليات", style=discord.ButtonStyle.secondary)
    async def events(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = make_embed("🎉 قوانين الفعاليات", EVENT_CHAT_RULES_TEXT, EMBED_COLOR)
        await interaction.response.edit_message(embed=embed, view=RulesBackView())


class RulesBackView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=300)

    @discord.ui.button(label="رجوع", style=discord.ButtonStyle.secondary)
    async def back(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = make_embed("📜 القوانين", SERVER_RULES_TEXT, EMBED_COLOR)
        embed.set_image(url=RULES_IMAGE_URL)
        await interaction.response.edit_message(embed=embed, view=RulesSubView())


def apply_start_embed():
    embed = discord.Embed(
        description="# تقديم",
        color=EMBED_COLOR
    )
    embed.set_image(url=APPLY_IMAGE_URL)
    return embed
# =========================================================
# BOT CLASS
# =========================================================
class MyBot(commands.Bot):
    async def setup_hook(self):
        self.add_view(PanelView())
        self.add_view(RulesSubView())
        self.add_view(RulesBackView())
        self.add_view(TicketPanelView())
        self.add_view(TicketActionView())
        self.add_view(FeedbackView())
        self.add_view(ApplicationActionView())

        guild = discord.Object(id=GUILD_ID)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        print(f"Synced commands to guild {GUILD_ID}")

intents = discord.Intents.default()
intents.guilds = True
intents.members = True
intents.messages = True
intents.message_content = True

bot = MyBot(command_prefix="!", intents=intents)

# =========================================================
# EVENTS
# =========================================================
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user} ({bot.user.id})")
    await upsert_panel_message()

@bot.event
async def on_member_join(member: discord.Member):
    channel = member.guild.get_channel(WELCOME_CHANNEL_ID)
    if not isinstance(channel, discord.TextChannel):
        return

    embed = make_embed(
        "👋 Welcome!",
        (
            f"Welcome {member.mention}!\n\n"
            f"💬 Say Hi in: <#{CHAT_CHANNEL_ID}>\n"
            f"📜 Check Rules: <#{RULES_CHANNEL_ID}>\n"
            f"🛠️ Support in: <#{SUPPORT_CHANNEL_ID}>"
        ),
        EMBED_COLOR
    )
    embed.set_thumbnail(url=member.display_avatar.url)
    await channel.send(embed=embed)

@bot.event
async def on_message(message: discord.Message):
    if message.author.bot or not message.guild:
        return

    support_member = isinstance(message.author, discord.Member) and user_has_any_role(
        message.author,
        {SUPPORT_ROLE_ID, GIRL_SUPPORT_ROLE_ID}
    )
    increment_message_count(message.guild.id, message.author.id, support=support_member)
    await process_leveling(message)

    if message.channel.id in AUTO_THREAD_CHANNEL_IDS:
        for emoji_id in AUTO_REACTION_EMOJIS:
            emoji = bot.get_emoji(emoji_id)
            if emoji:
                try:
                    await message.add_reaction(emoji)
                except Exception:
                    pass
        try:
            if getattr(message, "thread", None) is None:
                await message.create_thread(name=f"Thread - {message.author.display_name}")
        except Exception:
            pass

    if message.channel.id == SUGGESTIONS_CHANNEL_ID:
        content = (message.content or "").strip()
        if content:
            author = message.author if isinstance(message.author, discord.Member) else None
            if author:
                try:
                    await message.delete()
                except Exception:
                    pass

                sent = await message.channel.send(
                    embed=build_suggestion_embed(author, content, 0, 0, "pending")
                )
                sugg_state[str(sent.id)] = {
                    "author_id": author.id,
                    "text": content,
                    "yes": 0,
                    "no": 0,
                    "votes": {},
                    "status": "pending",
                }
                save_sugg_state()
                await sent.edit(view=build_suggestion_view(sent.id, "pending"))
            return

    await bot.process_commands(message)

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.type != discord.InteractionType.component:
        return

    data = interaction.data or {}
    custom_id = data.get("custom_id")
    if not custom_id or ":" not in custom_id:
        return

    action, raw_id = custom_id.split(":", 1)
    if not raw_id.isdigit():
        return

    message_id = int(raw_id)
    state = sugg_state.get(str(message_id))
    if not state:
        return

    if state.get("status") in {"accepted", "rejected"}:
        if not interaction.response.is_done():
            await interaction.response.send_message("تم اتخاذ قرار نهائي لهذا الاقتراح.", ephemeral=True)
        return

    if not interaction.guild or not isinstance(interaction.channel, discord.TextChannel):
        return

    try:
        suggestion_message = await interaction.channel.fetch_message(message_id)
    except Exception:
        suggestion_message = None

    if action in {"sugg_vote_yes", "sugg_vote_no"}:
        user_id = str(interaction.user.id)
        if user_id in state["votes"]:
            await interaction.response.send_message("تصويتك مسجل مسبقًا.", ephemeral=True)
            return

        choice = "yes" if action == "sugg_vote_yes" else "no"
        state["votes"][user_id] = choice
        state[choice] += 1
        sugg_state[str(message_id)] = state
        save_sugg_state()

        author = interaction.guild.get_member(int(state["author_id"]))
        if suggestion_message and author:
            await suggestion_message.edit(
                embed=build_suggestion_embed(author, state["text"], state["yes"], state["no"], state["status"]),
                view=build_suggestion_view(message_id, state["status"])
            )

        await interaction.response.send_message("✅ تم تسجيل تصويتك.", ephemeral=True)
        return

    if action in {"sugg_admin_accept", "sugg_admin_reject"}:
        if not isinstance(interaction.user, discord.Member) or not suggestion_staff_allowed(interaction.user):
            await interaction.response.send_message("هذا الزر مخصص للإدارة فقط.", ephemeral=True)
            return

        state["status"] = "accepted" if action == "sugg_admin_accept" else "rejected"
        sugg_state[str(message_id)] = state
        save_sugg_state()

        author = interaction.guild.get_member(int(state["author_id"]))
        if suggestion_message and author:
            await suggestion_message.edit(
                embed=build_suggestion_embed(author, state["text"], state["yes"], state["no"], state["status"]),
                view=build_suggestion_view(message_id, state["status"])
            )

        await interaction.response.send_message("✅ تم تحديث حالة الاقتراح.", ephemeral=True)

# =========================================================
# CHECKS
# =========================================================
def support_check():
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.guild or not isinstance(interaction.user, discord.Member):
            return False
        if support_command_allowed(interaction.user):
            return True
        await send_permission_error(interaction)
        return False
    return app_commands.check(predicate)

def admin_reset_check():
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.guild or not isinstance(interaction.user, discord.Member):
            return False
        if best_reset_allowed(interaction.user):
            return True
        await send_permission_error(interaction)
        return False
    return app_commands.check(predicate)

def say_check():
    async def predicate(interaction: discord.Interaction) -> bool:
        if not interaction.guild or not isinstance(interaction.user, discord.Member):
            return False
        if say_allowed(interaction.user):
            return True
        await send_permission_error(interaction)
        return False
    return app_commands.check(predicate)

# =========================================================
# COMMANDS
# =========================================================
@bot.tree.command(name="send_ticket_panel", description="Send the ticket panel.")
@support_check()
async def send_ticket_panel(interaction: discord.Interaction):
    embed = make_embed(
        "Ticket System",
        "Welcome to the ticket system, here you can open a ticket and get help from the staff team.",
        EMBED_COLOR
    )
    embed.set_image(url=PANEL_IMAGE_URL)
    await interaction.channel.send(embed=embed, view=TicketPanelView())
    await interaction.response.send_message(embed=make_embed("Done", "The ticket panel has been sent.", SUCCESS_COLOR), ephemeral=True)

@bot.tree.command(name="best", description="Show the best member by messages.")
async def best(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
        return

    result = top_member(interaction.guild.id, support=False)
    if not result:
        await interaction.response.send_message(embed=make_embed("Best Member", "No data found yet."), ephemeral=True)
        return

    user_id, count = result
    member = interaction.guild.get_member(user_id)
    embed = make_embed("Best Member", f"🥇 **Member:** {member.mention if member else f'<@{user_id}>'}\n**Messages:** {count}", EMBED_COLOR)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="bestsupport", description="Show the best support member by messages.")
async def bestsupport(interaction: discord.Interaction):
    if not interaction.guild:
        await interaction.response.send_message("This command can only be used in a server.", ephemeral=True)
        return

    result = top_member(interaction.guild.id, support=True)
    if not result:
        await interaction.response.send_message(embed=make_embed("Best Support", "No data found yet."), ephemeral=True)
        return

    user_id, count = result
    member = interaction.guild.get_member(user_id)
    embed = make_embed("Best Support", f"🥇 **Member:** {member.mention if member else f'<@{user_id}>'}\n**Messages:** {count}", EMBED_COLOR)
    await interaction.response.send_message(embed=embed)

@bot.tree.command(name="bestsformat", description="Reset best member stats.")
@admin_reset_check()
async def bestsformat(interaction: discord.Interaction):
    reset_counts(interaction.guild.id, support=False)
    await interaction.response.send_message(embed=make_embed("Best Reset", "Best member statistics have been reset.", EMBED_COLOR), ephemeral=True)

@bot.tree.command(name="formatbestsupport", description="Reset best support stats.")
@admin_reset_check()
async def formatbestsupport(interaction: discord.Interaction):
    reset_counts(interaction.guild.id, support=True)
    await interaction.response.send_message(embed=make_embed("Best Support Reset", "Best support statistics have been reset.", EMBED_COLOR), ephemeral=True)

@bot.tree.command(name="kick", description="Kick a member.")
@support_check()
@app_commands.describe(member="Member to kick", reason="Reason")
async def kick(interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = "No reason provided"):
    if member.top_role >= interaction.user.top_role and interaction.guild.owner_id != interaction.user.id:
        await interaction.response.send_message("You cannot kick this member.", ephemeral=True)
        return
    try:
        await member.kick(reason=f"{interaction.user}: {reason}")
        await interaction.response.send_message(embed=make_embed("Kick", f"{member.mention} has been kicked.\n**Reason:** {reason}", EMBED_COLOR))
    except Exception as e:
        await interaction.response.send_message(f"Failed to kick member: {e}", ephemeral=True)

@bot.tree.command(name="ban", description="Ban a member.")
@support_check()
@app_commands.describe(member="Member to ban", reason="Reason")
async def ban(interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = "No reason provided"):
    if member.top_role >= interaction.user.top_role and interaction.guild.owner_id != interaction.user.id:
        await interaction.response.send_message("You cannot ban this member.", ephemeral=True)
        return
    try:
        await member.ban(reason=f"{interaction.user}: {reason}")
        await interaction.response.send_message(embed=make_embed("Ban", f"{member.mention} has been banned.\n**Reason:** {reason}", EMBED_COLOR))
    except Exception as e:
        await interaction.response.send_message(f"Failed to ban member: {e}", ephemeral=True)

@bot.tree.command(name="timeout", description="Timeout a member.")
@support_check()
@app_commands.describe(member="Member to timeout", duration="Like 10m, 1h, 1d", reason="Reason")
async def timeout_cmd(interaction: discord.Interaction, member: discord.Member, duration: str, reason: Optional[str] = "No reason provided"):
    td = parse_duration(duration)
    if td is None:
        await interaction.response.send_message("Invalid duration. Use examples like 10m, 1h, 1d.", ephemeral=True)
        return
    try:
        await member.timeout(td, reason=f"{interaction.user}: {reason}")
        await interaction.response.send_message(embed=make_embed("Timeout", f"{member.mention} has been timed out for **{duration}**.\n**Reason:** {reason}", EMBED_COLOR))
    except Exception as e:
        await interaction.response.send_message(f"Failed to timeout member: {e}", ephemeral=True)

@bot.tree.command(name="untimeout", description="Remove timeout from a member.")
@support_check()
@app_commands.describe(member="Member to remove timeout from", reason="Reason")
async def untimeout(interaction: discord.Interaction, member: discord.Member, reason: Optional[str] = "No reason provided"):
    try:
        await member.timeout(None, reason=f"{interaction.user}: {reason}")
        await interaction.response.send_message(embed=make_embed("Untimeout", f"Timeout removed from {member.mention}.\n**Reason:** {reason}", EMBED_COLOR))
    except Exception as e:
        await interaction.response.send_message(f"Failed to remove timeout: {e}", ephemeral=True)

@bot.tree.command(name="clear", description="Delete a number of messages.")
@support_check()
@app_commands.describe(amount="Number of messages to delete")
async def clear(interaction: discord.Interaction, amount: app_commands.Range[int, 1, 100]):
    if not isinstance(interaction.channel, discord.TextChannel):
        await interaction.response.send_message("This command must be used in a text channel.", ephemeral=True)
        return

    await interaction.response.defer(ephemeral=True)
    deleted = await interaction.channel.purge(limit=amount)
    await interaction.followup.send(embed=make_embed("Clear", f"Deleted **{len(deleted)}** messages.", EMBED_COLOR), ephemeral=True)

@bot.tree.command(name="lock", description="Lock the current channel.")
@support_check()
async def lock(interaction: discord.Interaction):
    if not isinstance(interaction.channel, discord.TextChannel):
        await interaction.response.send_message("This command must be used in a text channel.", ephemeral=True)
        return

    overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = False
    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    await interaction.response.send_message(embed=make_embed("Lock", "This channel has been locked.", EMBED_COLOR))

@bot.tree.command(name="unlock", description="Unlock the current channel.")
@support_check()
async def unlock(interaction: discord.Interaction):
    if not isinstance(interaction.channel, discord.TextChannel):
        await interaction.response.send_message("This command must be used in a text channel.", ephemeral=True)
        return

    overwrite = interaction.channel.overwrites_for(interaction.guild.default_role)
    overwrite.send_messages = None
    await interaction.channel.set_permissions(interaction.guild.default_role, overwrite=overwrite)
    await interaction.response.send_message(embed=make_embed("Unlock", "This channel has been unlocked.", EMBED_COLOR))

@bot.tree.command(name="warn", description="Warn a member.")
@support_check()
@app_commands.describe(member="Member to warn", reason="Reason for warning")
async def warn(interaction: discord.Interaction, member: discord.Member, reason: str):
    count = add_warning(interaction.guild.id, member.id)
    try:
        dm_embed = make_embed("Warning", f"You have received **1 warning**.\n\n**Reason:** {reason}", EMBED_COLOR)
        await member.send(embed=dm_embed)
    except Exception:
        pass

    await interaction.response.send_message(embed=make_embed("Warn", f"{member.mention} has been warned.\n**Total warnings:** {count}\n**Reason:** {reason}", EMBED_COLOR))

@bot.tree.command(name="unwarn", description="Remove one warning from a member.")
@support_check()
@app_commands.describe(member="Member to remove a warning from")
async def unwarn(interaction: discord.Interaction, member: discord.Member):
    count = remove_warning(interaction.guild.id, member.id)
    await interaction.response.send_message(embed=make_embed("Unwarn", f"One warning removed from {member.mention}.\n**Remaining warnings:** {count}", EMBED_COLOR))

@bot.tree.command(name="say", description="Send a message to a selected channel.")
@say_check()
@app_commands.describe(channel="The channel to send the message to", message="The message you want to send")
async def say(interaction: discord.Interaction, channel: discord.TextChannel, message: str):
    try:
        await channel.send(message)
        await interaction.response.send_message(embed=make_embed("Say", f"Message sent to {channel.mention}.", SUCCESS_COLOR), ephemeral=True)
    except Exception as e:
        await interaction.response.send_message(f"Failed to send message: {e}", ephemeral=True)

@bot.tree.command(name="jail", description="Jail a member")
@app_commands.describe(user="العضو", reason="السبب")
async def jail(interaction: discord.Interaction, user: discord.Member, reason: str):
    if not isinstance(interaction.user, discord.Member) or not jail_allowed(interaction.user):
        await interaction.response.send_message("❌ ما عندك صلاحية", ephemeral=True)
        return

    role = interaction.guild.get_role(JAIL_ROLE_ID) if interaction.guild else None
    channel = interaction.guild.get_channel(JAIL_CHANNEL_ID) if interaction.guild else None

    if not role or not isinstance(channel, discord.TextChannel):
        await interaction.response.send_message("❌ في مشكلة بالإعدادات", ephemeral=True)
        return

    roles_to_remove = [r for r in user.roles if r != interaction.guild.default_role and r.id != JAIL_ROLE_ID]
    try:
        if roles_to_remove:
            await user.remove_roles(*roles_to_remove, reason=f"Jailed by {interaction.user}")
        await user.add_roles(role, reason=f"Jailed by {interaction.user}")
    except Exception as e:
        await interaction.response.send_message(f"❌ فشل سجن العضو: {e}", ephemeral=True)
        return

    msg = (
        "⚖️ إعلان رسمي من إدارة السجن المركزي لسيرفر تركي ⚖️\n\n"
        f"تم القبض على المواطن {user.mention} بعد تحقيقات طويلة ومطاردات شرسة استمرت ٣ دقايق ونص 😤\n"
        f"الجرائم المنسوبة إليه تتضمن: {reason} 😂\n\n"
        "وعليه، تم تحويله إلى السجن الانفرادي حيث لا يوجد سوى روم واحد وصوت الصدى فقط...\n"
        "نرجو من الأصدقاء إرسال وجبات افتراضية ودعوات بالحرية .\n\n"
        "🔒 مدة الحكم: غير معروفة (يعتمد على مزاج الإدارة)\n"
        "🧃 حقوق السجين: ولا شي غير التفكير بأفعاله.\n"
        "https://tenor.com/view/dj-khaled-jailed-dj-khaled-dj-khaled-dancing-jail-jailed-gif-5775727153817439120"
    )

    await channel.send(msg)
    await interaction.response.send_message("✅ تم سجن العضو", ephemeral=True)

@bot.tree.command(name="unjail", description="Unjail a member")
@app_commands.describe(user="العضو")
async def unjail(interaction: discord.Interaction, user: discord.Member):
    if not isinstance(interaction.user, discord.Member) or not jail_allowed(interaction.user):
        await interaction.response.send_message("❌ ما عندك صلاحية", ephemeral=True)
        return

    role = interaction.guild.get_role(JAIL_ROLE_ID) if interaction.guild else None
    channel = interaction.guild.get_channel(JAIL_CHANNEL_ID) if interaction.guild else None

    if not role or not isinstance(channel, discord.TextChannel):
        await interaction.response.send_message("❌ في مشكلة بالإعدادات", ephemeral=True)
        return

    try:
        await user.remove_roles(role, reason=f"Unjailed by {interaction.user}")
    except Exception as e:
        await interaction.response.send_message(f"❌ فشل فك السجن: {e}", ephemeral=True)
        return

    msg = (
        f"🔓 تم فك سجن {user.mention} بنجاح! (تم تحديث السجل وإزالة الرتبة).\n"
        f"🔓 تم الإفراج عن {user.mention} رسميًا!\n"
        "عاد إلى المجتمع بعد فترة تأمل قصيرة في الزنزانة،\n"
        "نرجو منه يتعلم من تجربته... أو على الأقل ما يرجع بسرعة 😂\n"
        "https://tenor.com/view/jail-release-natev-gif-22733511"
    )

    await channel.send(msg)
    await interaction.response.send_message("✅ تم فك السجن", ephemeral=True)

# =========================================================
# RUN
# =========================================================
if __name__ == "__main__":
    if not TOKEN:
        raise RuntimeError("Please set DISCORD_TOKEN in Railway variables.")
    bot.run(TOKEN)