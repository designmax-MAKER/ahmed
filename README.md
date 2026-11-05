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

## تثبيت أدوات المونتاج

السكريبتات دي بتثبّت:

| الأداة | وظيفتها |
|---|---|
| **FFmpeg** | مونتاج من الترمنال: قص، دمج، تحويل صيغ، ترجمة (Claude Code يقدر يستخدمه مباشرة) |
| **Kdenlive** | برنامج مونتاج كامل ومجاني |
| **Shotcut** | برنامج مونتاج خفيف ومجاني |
| **Audacity** | تعديل الصوت |

**على Mac أو Linux:**
```bash
./scripts/install-montage-tools.sh
```

**على Windows (من PowerShell):**
```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\install-montage-tools.ps1
```

### أمثلة FFmpeg سريعة
```bash
# قص من الثانية 10 لحد الثانية 40
ffmpeg -i input.mp4 -ss 00:00:10 -to 00:00:40 -c copy cut.mp4

# دمج كذا فيديو (اكتب أسماءهم في list.txt بالشكل: file 'a.mp4')
ffmpeg -f concat -safe 0 -i list.txt -c copy merged.mp4

# تحويل لـ 1080p وتصغير الحجم
ffmpeg -i input.mp4 -vf scale=-2:1080 -c:v libx264 -crf 23 -c:a aac output.mp4

# استخراج الصوت
ffmpeg -i input.mp4 -vn -c:a libmp3lame -q:a 2 audio.mp3
```

> **ملحوظة:** DaVinci Resolve برنامج مونتاج احترافي مجاني برضه، بس لازم يتنزل يدوي من موقع Blackmagic Design.
