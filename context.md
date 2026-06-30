# Egzersiz Veritabanı ve Not Sistemi Bağlamı (Context)

Bu dosya, projenin frontend (GitHub Pages) ve backend (Oracle Cloud) altyapısının detaylı bir haritasını çıkarmak, mevcut mimariyi özetlemek ve projede çalışacak olan diğer Yapay Zeka / LLM sistemleri için eksiksiz bir rehber sunmak amacıyla hazırlanmıştır.

## 1. Mimari ve Veri Akışı
- **Frontend:** Statik HTML, CSS ve JavaScript kullanılarak oluşturulmuş, GitHub Pages üzerinde barınan bir web uygulamasıdır (`my_workout.html`).
- **Backend:** `92.5.42.0` (Oracle Cloud ARM) IP adresinde barınan, Python Flask tabanlı, hafif bir REST API servisidir. Nginx ters vekil sunucusu (Reverse Proxy) aracılığıyla dışarıya açılmıştır.
- **Veritabanı:** Backend tarafında `workout_notes.db` adlı yerel bir SQLite veritabanı kullanılmaktadır.

**Veri Akışı:** Kullanıcı GitHub Pages'teki frontend'e girip bir egzersize tıkladığında, `my_workout.html` içindeki JS kodu `https://emrullah.xyz/api/workout/notes/{exercise_id}` adresine bir `GET` isteği atar. Veri geldiğinde form doldurulur. Kullanıcı formda herhangi bir değişiklik yaptığında ise 1000ms gecikmeli (debounce) olarak aynı adrese `POST` isteği ile veriler güncellenir.

---

## 2. Frontend Detayları (`my_workout.html`)

### Arayüz Elementleri ve Notlar Modülü
- Her egzersiz için modal (popup) ekranında bir "Notlar" bölümü yer alır.
- **Serbest Not Alanı:** Kullanıcının egzersiz hakkında uzun notlar alabileceği gizlenip açılabilen bir `<textarea>` alanıdır.
- **Set/Kg/Tekrar Girişleri:** `exercises_data.json` içerisindeki "3x10-12" gibi dinamik set yapılarını algılayıp, o set sayısına göre otomatik input satırları (Row) oluşturur.

### JavaScript Fonksiyonları (Core Logic)
- `fetchNotes(exercise_id, setsString)`: Egzersiz modal'ı açıldığında çağrılır. `exercise_id` parametresi ile backend'den verileri getirir. **Race Condition** koruması mevcuttur (Eğer istek yanıtlanmadan kullanıcı başka bir egzersize tıklarsa, eski yanıt yoksayılır: `if (currentExerciseId !== exercise_id) return;`).
- `scheduleSave()`: Her input (klavye) hareketinde veya buton tıklamasında tetiklenen, gereksiz API trafiğini önlemek için `setTimeout` (1 saniye - debounce) kullanan otomatik kaydetme mekanizması.

### UI ve CSS Optimizasyonları (Önemli!)
- **Auto-expanding (Otomatik Esneyen) Inputlar:** Girdi kutuları (`<input type="number">`) sabit bir genişliğe sahip olmak yerine, JavaScript yardımıyla (inline style: `width: ${text.length + 0.5}ch`) içerisindeki metne göre genişler veya daralır.
- **Sarmalayıcı (Wrapper) CSS Yapısı:**
  ```html
  <div class="input-wrap has-val">
    <input type="number" class="set-input" style="width: 2.5ch" />
    <span class="input-suffix">kg</span>
  </div>
  ```
- CSS tarafında `.input-wrap` sınıfı asıl kutucuğun görsel çerçevesini (`border`, `background`) oluşturur. `.set-input` arka planı şeffaftır (`transparent`). Girdi yapıldığında (JS ile `has-val` eklendiğinde) veya kutucuğa tıklandığında (CSS `:focus-within`), `kg` ve `tekrar` gibi küçük ibareler (suffix) yumuşak bir animasyonla sağdan kayarak görünür.

---

## 3. Backend Detayları (Oracle Cloud)

### Flask API (`app.py`)
- Dizin: `/home/emrullah/workout-api/app.py`
- Sadece `emrullahxyz.github.io` ve `emrullah.github.io` adreslerinden gelen isteklere (CORS) izin verilmiştir.
- Sadece iki route mevcuttur:
  - `GET /api/workout/notes/<exercise_id>`: Veriyi döner.
  - `POST /api/workout/notes/<exercise_id>`: Veriyi yazar veya günceller (Upsert).

### SQLite Veritabanı Şeması
Dosya: `/home/emrullah/workout-api/workout_notes.db`
```sql
CREATE TABLE notes (
    exercise_id TEXT PRIMARY KEY,
    data TEXT
)
```
- `data` sütunu içerisinde JSON formatında `{ "note": "...", "sets": [ {"kg": "20", "reps": "10"}, ... ] }` verisi saklanmaktadır. `ON CONFLICT DO UPDATE` kullanılarak aynı id geldiğinde JSON doğrudan ezilir.

### Sunucu ve Servis Yapılandırması
- **Systemd Servisi:** API sunucusunun arka planda 5000 portunda daemon olarak çalışması için `/etc/systemd/system/workout-api.service` tanımlanmıştır. Servis `emrullah` kullanıcısı ile çalışır.
- **Nginx Reverse Proxy & SSOwat Bypass:**
  - Sunucu panel olarak **YunoHost** kullanmaktadır. YunoHost varsayılan olarak her siteye SSO (Single Sign-On) duvarı örer (SSOwat).
  - Statik sayfalarımız dışarıdan API'a erişirken bu SSOwat duvarına çarpıp 401 Unauthorized/302 Redirect hataları alıyordu.
  - **Çözüm:** `/etc/nginx/conf.d/emrullah.xyz.d/workout.conf` içine şu kural eklenmiştir:
    ```nginx
    location /api/workout/ {
        access_by_lua_block { return } # YunoHost SSO duvarını delmek için kritik Lua kuralı
        proxy_pass http://127.0.0.1:5000;
        ...
    }
    ```
  - Bu sayede API güzergahı kimlik doğrulamasından muaf tutularak açık hale getirilmiştir.

---

## 4. Dikkat Edilmesi Gereken Geliştirici (LLM) Notları
1. **GitHub Deploy ve Cache:** Projenin frontend kodları GitHub sayfalarında barındığı için `git push` yapıldığında yayınlanması 1-2 dakikayı bulabilir ve tarayıcıda `10 dakika` cache kalabilir. Tasarım değişikliklerinden sonra kullanıcıya `?v=2` gibi Cache-Buster taktikleri sunulmalıdır.
2. **Kimlik Yöneticisi Hatası:** LLM arka planda terminali kullanırken `git push` yaptığında Windows Credential Manager onay bekleyebilir ve işlemi dondurabilir (Özellikle bilgisayar yeniden başlatıldıysa). Sorun yaşanırsa LLM'in `gh auth token` komutunu kullanarak, doğrudan `https://username:token@github.com/...` şeklinde push etmesi en güvenli yöntemdir.
3. **Kapsüllenmiş DOM Müdahalesi:** `my_workout.html` dosyasında set inputlarının CSS seçicilerine müdahale ederken `grid` yapıları cihazdan cihaza ve yazı tipine (font) göre tutarsız davrandığı için bilinçli olarak JavaScript tabanlı (inline width = x + ch) çözüme geçilmiştir. Yeni özellik ekleneceğinde bu esnek (auto-expanding) yapı bozulmamalıdır.
4. **Git Sync Protokolü:** `app.py` veya `nginx/workout.conf` gibi kritik sunucu altyapısı güncellendiğinde, bu dosyalar Emrullah'ın kuralları gereği mutlaka yereldeki (bilgisayarındaki) `/oracle-infrastructure/` (eğer varsa) veya ilgili backup depolarına senkronize edilmelidir.
