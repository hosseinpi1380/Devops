# راه‌اندازی پروژه با Docker

## پیش‌نیاز
نصب Docker Desktop (ویندوز/مک) یا Docker Engine + Docker Compose (لینوکس):
https://www.docker.com/products/docker-desktop/

بررسی نصب صحیح:
```bash
docker --version
docker compose version
```

---

## روش پیشنهادی (ساده و مطمئن روی همه سیستم‌عامل‌ها)

فقط **دیتابیس PostgreSQL** را با داکر بالا می‌آوریم؛ برنامه گرافیکی (Tkinter) را
مستقیم روی سیستم خودتان اجرا می‌کنید. این روش چون برنامه گرافیکی نیازی به
عبور دادن نمایشگر (X11) از داخل کانتینر ندارد، همیشه بدون مشکل کار می‌کند.

### مرحله ۱: بالا آوردن دیتابیس

```bash
cp .env.example .env
docker compose up -d db
```

با این دستور یک کانتینر PostgreSQL روی پورت `5432` سیستم شما بالا می‌آید و
داده‌هایش در یک Volume داکر (`hotel_db_data`) نگه‌داری می‌شود (با ری‌استارت
کردن کانتینر داده از بین نمی‌رود).

بررسی وضعیت:
```bash
docker compose ps
docker compose logs db
```

### مرحله ۲: اجرای برنامه پایتون روی سیستم خودتان

```bash
python -m venv venv
source venv/bin/activate        # ویندوز: venv\Scripts\activate
pip install -r requirements.txt

export HOTEL_DB_URL="postgresql+psycopg2://hotel_user:hotel_pass123@localhost:5432/hotel_db"
# ویندوز PowerShell:  $env:HOTEL_DB_URL="postgresql+psycopg2://hotel_user:hotel_pass123@localhost:5432/hotel_db"

python seed.py     # ساخت جداول + داده نمونه (فقط بار اول لازم است)
python main.py      # اجرای برنامه
```

اگر فایل `.env` را همانطور که در مرحله ۱ کپی کردید نگه دارید و پکیج
`python-dotenv` نصب باشد (در requirements.txt هست)، دیگر نیازی به `export`
دستی نیست؛ برنامه خودش مقدار `HOTEL_DB_URL` را از `.env` می‌خواند — کافیست
در همان فولدر پروژه اجرا کنید.

### توقف و پاک‌سازی

```bash
docker compose stop db        # فقط متوقف کردن (داده حفظ می‌شود)
docker compose down           # حذف کانتینر (داده در volume باقی می‌ماند)
docker compose down -v        # حذف کامل همراه با داده‌ها
```

---

## روش کامل (اجرای خود برنامه گرافیکی هم داخل داکر) — فقط لینوکس

اگر می‌خواهید **همه‌چیز** از جمله رابط گرافیکی هم داخل کانتینر اجرا شود
(مثلاً برای دمو روی سرور لینوکسی با دسکتاپ گرافیکی):

```bash
xhost +local:docker
cp .env.example .env
docker compose --profile gui up --build
```

توضیح:
- `docker/entrypoint.sh` داخل کانتینر منتظر آماده‌شدن دیتابیس می‌ماند، جداول را
  می‌سازد و برنامه را اجرا می‌کند.
- `network_mode: host` و mount کردن `/tmp/.X11-unix` باعث می‌شود پنجره Tkinter
  بتواند روی همان دسکتاپ لینوکس شما نمایش داده شود.
- بعد از پایان کار، برای بستن دسترسی X11:  `xhost -local:docker`

### ویندوز و مک (پیشرفته، اختیاری)

روی ویندوز و مک، داکر داخل یک ماشین مجازی اجرا می‌شود و دسترسی مستقیم به
نمایشگر ندارد، بنابراین باید یک X-Server جداگانه نصب کنید:

- **ویندوز**: نصب [VcXsrv](https://sourceforge.net/projects/vcxsrv/) و اجرای آن
  با گزینه «Disable access control»، سپس:
  ```powershell
  $env:DISPLAY="host.docker.internal:0.0"
  docker compose --profile gui up --build
  ```
- **مک**: نصب [XQuartz](https://www.xquartz.org/)، در تنظیمات آن
  "Allow connections from network clients" را فعال کنید، سپس:
  ```bash
  xhost + 127.0.0.1
  export DISPLAY=host.docker.internal:0
  docker compose --profile gui up --build
  ```

اگر پنجره باز نشد یا خطای اتصال به Display دیدید، از **روش پیشنهادی** بالا
(فقط دیتابیس در داکر) استفاده کنید — سریع‌تر و بدون دردسر است.

---

## اتصال به MySQL به‌جای PostgreSQL

اگر ترجیح می‌دهید از MySQL استفاده کنید، سرویس `db` در `docker-compose.yml`
را با این جایگزین کنید:

```yaml
  db:
    image: mysql:8
    container_name: hotel_db
    restart: unless-stopped
    environment:
      MYSQL_DATABASE: ${POSTGRES_DB:-hotel_db}
      MYSQL_USER: ${POSTGRES_USER:-hotel_user}
      MYSQL_PASSWORD: ${POSTGRES_PASSWORD:-hotel_pass123}
      MYSQL_ROOT_PASSWORD: root_pass123
    ports:
      - "3306:3306"
    volumes:
      - hotel_db_data:/var/lib/mysql
```

و در `requirements.txt` خط `pymysql` را از حالت کامنت خارج کنید، سپس
`HOTEL_DB_URL` را این‌طور تنظیم کنید:

```
HOTEL_DB_URL=mysql+pymysql://hotel_user:hotel_pass123@localhost:3306/hotel_db
```

---

## عیب‌یابی متداول

| مشکل | راه‌حل |
|---|---|
| `connection refused` هنگام اتصال به دیتابیس | چند ثانیه صبر کنید تا Postgres کامل بالا بیاید، یا `docker compose logs db` را بررسی کنید |
| پورت ۵۴۳۲ اشغال است | در `.env` مقدار `POSTGRES_PORT` را مثلاً به `5433` تغییر دهید و در `HOTEL_DB_URL` هم همان پورت را بگذارید |
| پنجره Tkinter داخل داکر باز نمی‌شود | از «روش پیشنهادی» (دیتابیس در داکر، برنامه روی سیستم) استفاده کنید |
| خطای `ModuleNotFoundError: psycopg2` | `pip install -r requirements.txt` را دوباره اجرا کنید |
