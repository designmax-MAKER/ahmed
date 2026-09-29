# ahmed

## تشغيل Claude Code في الترمنال

### 1. التثبيت

**على Mac أو Linux أو WSL:**
```bash
curl -fsSL https://claude.ai/install.sh | bash
```

**على Windows (من PowerShell):**
```powershell
irm https://claude.ai/install.ps1 | iex
```

**أو عن طريق npm** (لازم يكون عندك Node.js 18 أو أحدث):
```bash
npm install -g @anthropic-ai/claude-code
```

### 2. نزّل المشروع ده على جهازك
```bash
git clone https://github.com/designmax-MAKER/ahmed.git
cd ahmed
git checkout claude/confident-euler-p8x52p
```

### 3. افتحه في VS Code
```bash
code .
```
بعد كده افتح الترمنال جوه VS Code بـ `` Ctrl+` `` واكتب:
```bash
claude
```

أول مرة هيطلب منك تسجل دخول بحساب Claude أو بمفتاح API.

> ممكن كمان تنزّل إضافة **Claude Code** من الـ Extensions في VS Code
> عشان تشتغل معاه من جوه المحرر.

### أوامر مفيدة
| الأمر | وظيفته |
|---|---|
| `claude "سؤالك"` | يبدأ جلسة جديدة بسؤال على طول |
| `claude -c` | يكمّل آخر محادثة |
| `/help` | يعرض المساعدة |
| `/init` | يعمل ملف `CLAUDE.md` فيه وصف للمشروع |
| `/login` أو `/logout` | يغيّر الحساب اللي داخل بيه |
| `Ctrl+C` أو `/exit` | يقفل البرنامج |

**لو ظهرلك `command not found`:** اقفل الترمنال وافتحه تاني. ولو لسه مش شغال، اكتب `claude doctor` عشان يكشف المشكلة.
