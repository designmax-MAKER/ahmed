# فيديو SALYSS Commerce

فيديو إعلاني طولي (1080×1920، 42 ثانية، 30 fps) على نفس أسلوب إعلان Estavo:
جملة بالمصري فوق كل مشهد + شاشات بتتحرك تحت، بألوان موقع salyss.com.

- `salyss_commerce.mp4`: الفيديو النهائي
- `index.html`: كل المشاهد والحركة (بتتحكم فيها دالة `render(t)`)
- `render.js`: بيصوّر الصفحة فريم فريم ويطلّع الفيديو
- `music.py`: بيولّد المزيكا والمؤثرات الصوتية (موسيقى أصلية)
- `mark.png`: علامة اللوجو، مقصوصة من سكرين الموقع

## إعادة الإنتاج بعد أي تعديل
```bash
npm install
node render.js preview 5 20 40
node render.js video silent.mp4
python3 -m venv .venv && .venv/bin/pip install numpy scipy && .venv/bin/python music.py
ffmpeg -y -i silent.mp4 -i music.wav -c:v copy -c:a aac -b:a 192k -shortest -movflags +faststart salyss_commerce.mp4
```
`render.js` محتاج Playwright متثبّت (`npm i -D playwright && npx playwright install chromium`).
