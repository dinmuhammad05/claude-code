"""Claude Code ruxsat qoidalarining o'quv simulyatori (Manual rejim).

Rasmiy hujjatdagi (code.claude.com/docs/en/permissions) hujjatlashtirilgan
qoidalarni soddalashtirilgan holda takrorlaydi:

  - tartib: deny -> ask -> allow; birinchi moslik qaror qiladi, aniqlik
    (specificity) tartibni o'zgartirmaydi;
  - Bash: `*` istalgan matn; `Bash(ls *)` -> `ls` va `ls -la`, `lsof` emas;
    `Bash(ls:*)` = `Bash(ls *)`; murakkab buyruq qismlarga bo'linadi
    (&&, ||, ;, |, &) va har qism alohida tekshiriladi;
  - o'ramlar (timeout, nohup, ...) moslashdan oldin olib tashlanadi;
  - o'qish uchun o'rnatilgan buyruqlar (ls, cat, grep, git status...) so'rovsiz;
  - Read/Edit: gitignore uslubidagi yo'llar; Read deny Edit/Write ni ham bloklaydi
    va `cat`, `head`, `tail` argumentlariga ham amal qiladi;
  - WebFetch(domain:...).

Bu haqiqiy Claude Code EMAS: chekka holatlarda farq bo'lishi mumkin.
Haqiqiy xulqni `/permissions` va sessiyaning o'zida tekshiring.

Sinash:  python ruxsat.py Bash "git push origin main"
         python ruxsat.py Read .env
         python ruxsat.py WebFetch https://docs.python.org/3/
"""

import json
import os
import re
import sys
from urllib.parse import urlparse

LOYIHA = "/loyiha"          # simulyatsiyadagi loyiha ildizi
UY = "/home/siz"            # simulyatsiyadagi uy papkasi

SEPARATORS = re.compile(r"\|&|&&|\|\||;|\||&|\n")
WRAPPERS = {"timeout", "time", "nice", "nohup", "stdbuf", "command", "builtin", "noglob"}
SAFE_ENV = {"NODE_ENV"}
READ_ONLY = {"ls", "cat", "echo", "pwd", "head", "tail", "grep", "find", "wc",
             "which", "diff", "stat", "du", "cd"}
READ_ONLY_GIT = {"status", "diff", "log", "show"}
FILE_READERS = {"cat", "head", "tail"}


# ---------- yordamchilar ----------

def parse_rule(rule):
    """'Bash(npm test *)' -> ('Bash', 'npm test *'); 'Bash' -> ('Bash', None)."""
    m = re.fullmatch(r"\s*([A-Za-z_]\w*)\s*(?:\((.*)\))?\s*", rule)
    if not m:
        return None, None
    return m.group(1), m.group(2)


def bash_rule_match(spec, cmd):
    if spec is None:
        return True
    spec = spec.strip()
    if spec.endswith(":*"):
        spec = spec[:-2] + " *"
    rx = ".*".join(re.escape(p) for p in spec.split("*"))
    if re.fullmatch(rx, cmd, flags=re.S):
        return True
    # oxirgi " *" yagona yulduzcha bo'lsa — yalang'och buyruq ham mos
    if spec.endswith(" *") and spec.count("*") == 1 and cmd == spec[:-2]:
        return True
    return False


def strip_wrappers(words):
    while words:
        w = words[0]
        if w in WRAPPERS:
            words = words[1:]
            # o'ram argumentlari: timeout 30, nice -n 10, stdbuf -oL
            while words and (words[0].startswith("-") or re.fullmatch(r"[\d.]+[smhd]?", words[0])):
                words = words[1:]
        elif w == "xargs" and len(words) > 1 and not words[1].startswith("-"):
            words = words[1:]
        else:
            break
    return words


def normalize(sub, for_allow):
    words = sub.split()
    while words and re.fullmatch(r"[A-Za-z_]\w*=\S*", words[0]):
        if for_allow and words[0].split("=")[0] not in SAFE_ENV:
            return None          # allow noma'lum o'zgaruvchidan o'tib moslashmaydi
        words = words[1:]
    words = strip_wrappers(words)
    return " ".join(words)


def is_read_only(cmd):
    words = cmd.split()
    if not words or any(w in (">", ">>") or w.startswith((">", ">>")) for w in words):
        return False
    if words[0] == "git":
        rest = words[1:]
        if rest and rest[0] in READ_ONLY_GIT:
            return True
        return False
    if words[0] == "find" and any(w in ("-exec", "-execdir", "-delete") for w in words):
        return False
    return words[0] in READ_ONLY


def resolve(path):
    """Fayl yo'lini simulyatsiyadagi mutlaq yo'lga aylantiradi."""
    if path.startswith("~/"):
        return UY + path[1:]
    if path.startswith("/"):
        return os.path.normpath(path)
    return os.path.normpath(os.path.join(LOYIHA, path))


def glob_rx(pattern):
    out, i = "", 0
    while i < len(pattern):
        if pattern.startswith("**/", i):
            out += "(?:.*/)?"
            i += 3
        elif pattern.startswith("**", i):
            out += ".*"
            i += 2
        elif pattern[i] == "*":
            out += "[^/]*"
            i += 1
        elif pattern[i] == "?":
            out += "[^/]"
            i += 1
        else:
            out += re.escape(pattern[i])
            i += 1
    return out


def path_rule_match(spec, path):
    """gitignore uslubi: '//' mutlaq, '~/' uy, '/' loyiha, './' yoki yalang'och — joriy papka (loyiha)."""
    if spec is None:
        return True
    p = spec.strip()
    if p.startswith("//"):
        base, p, anchored = "", p[1:], True
    elif p.startswith("~/"):
        base, p, anchored = UY, p[1:], True
    elif p.startswith("/"):
        base, anchored = LOYIHA, True
    else:
        if p.startswith("./"):
            p = p[2:]
        base = LOYIHA
        # gitignore: o'rtada '/' bo'lmasa — istalgan chuqurlikda
        anchored = "/" in p.rstrip("/")
        p = "/" + p
    if p.endswith("/"):
        p += "**"
    full = resolve(path)
    if anchored:
        return re.fullmatch(re.escape(base) + glob_rx(p), full) is not None
    return re.fullmatch(re.escape(base) + "(?:/.*)?" + glob_rx(p), full) is not None


def domain_match(spec, url):
    if spec is None:
        return True
    if not spec.startswith("domain:"):
        return False
    pat = spec[len("domain:"):].lower().rstrip(".")
    host = (urlparse(url).hostname or url).lower().rstrip(".")
    if pat == "*":
        return True
    if pat.startswith("*."):
        return host.endswith(pat[1:])
    if pat.endswith(".*"):
        return re.fullmatch(re.escape(pat[:-2]) + r"\.[^.]+", host) is not None
    return host == pat


# ---------- asosiy qaror ----------

class Qoidalar:
    def __init__(self, settings):
        perm = settings.get("permissions", {}) if isinstance(settings, dict) else {}
        self.r = {k: [parse_rule(x) for x in perm.get(k, []) if isinstance(x, str)]
                  for k in ("deny", "ask", "allow")}

    def rules(self, kind, tools):
        return [spec for tool, spec in self.r[kind] if tool in tools]

    def bash(self, command):
        subs = [s.strip() for s in SEPARATORS.split(command) if s.strip()]
        if not subs:
            return "ask"
        verdicts = []
        for sub in subs:
            da = normalize(sub, for_allow=False)
            al = normalize(sub, for_allow=True)
            if any(bash_rule_match(s, da) for s in self.rules("deny", {"Bash"})):
                return "deny"
            words = da.split()
            # Read deny cat/head/tail argumentlariga; Edit deny yo'naltirish nishoniga
            if words and words[0] in FILE_READERS:
                for a in words[1:]:
                    if not a.startswith("-") and self.read(a) == "deny":
                        return "deny"
            for i, w in enumerate(words):
                if w in (">", ">>") and i + 1 < len(words) and self.edit(words[i + 1]) == "deny":
                    return "deny"
            if any(bash_rule_match(s, da) for s in self.rules("ask", {"Bash"})):
                verdicts.append("ask")
            elif al is not None and any(bash_rule_match(s, al) for s in self.rules("allow", {"Bash"})):
                verdicts.append("allow")
            elif is_read_only(da):
                verdicts.append("allow")
            else:
                verdicts.append("ask")
        return "allow" if all(v == "allow" for v in verdicts) else "ask"

    def read(self, path):
        if any(path_rule_match(s, path) for s in self.rules("deny", {"Read"})):
            return "deny"
        if any(path_rule_match(s, path) for s in self.rules("ask", {"Read"})):
            return "ask"
        if any(path_rule_match(s, path) for s in self.rules("allow", {"Read"})):
            return "allow"
        return "allow" if resolve(path).startswith(LOYIHA + "/") else "ask"

    def edit(self, path):
        if any(path_rule_match(s, path) for s in self.rules("deny", {"Edit", "Read"})):
            return "deny"
        if any(path_rule_match(s, path) for s in self.rules("ask", {"Edit"})):
            return "ask"
        if any(path_rule_match(s, path) for s in self.rules("allow", {"Edit"})):
            return "allow"
        return "ask"

    def webfetch(self, url):
        for kind in ("deny", "ask", "allow"):
            if any(domain_match(s, url) for s in self.rules(kind, {"WebFetch"})):
                return kind
        return "ask"

    def qaror(self, tool, arg):
        tool = {"Write": "Edit"}.get(tool, tool)
        return {"Bash": self.bash, "Read": self.read, "Edit": self.edit,
                "WebFetch": self.webfetch}[tool](arg)


def yukla(yol=None):
    yol = yol or os.path.join(os.path.dirname(os.path.abspath(__file__)), ".claude", "settings.json")
    with open(yol, encoding="utf-8") as f:
        return json.load(f)


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(__doc__)
        sys.exit(2)
    q = Qoidalar(yukla())
    belgi = {"allow": "ruxsat (so'rovsiz)", "ask": "so'raladi", "deny": "taqiqlangan"}
    print(belgi[q.qaror(sys.argv[1], sys.argv[2])])
