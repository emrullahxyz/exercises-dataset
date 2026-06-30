# Egzersiz Veritabanı ve Not Sistemi Geliştirme Bağlamı

## 1. Notes (Notlar) Özelliğinin Arayüze Eklenmesi
- `my_workout.html` dosyasına, her egzersizin kendi detay görünümüne (modal) "Notlar" bölümü eklendi.
- "Notlar" modülü iki ana kısımdan oluşmaktadır:
  1. **Serbest Not (Textarea):** Kullanıcının egzersizle ilgili ekstra notlar alabileceği genişletilebilir bir metin alanı.
  2. **Set/Kg/Tekrar Girişleri:** `exercises_data.json` dosyasındaki hedef set sayılarına göre (ör. "3x10-12") otomatik olarak satırları oluşturulan set girişleri.
- Set girişlerinde **Auto-expanding Input** tekniği kullanıldı. JavaScript (inline `style.width`) kullanılarak `kg` ve `tekrar` eklerinin yazılan sayıya dinamik olarak yapışması sağlandı. CSS Grid uyumsuzlukları JS yöntemi ile aşıldı.
- Debounce mantığı (1000ms gecikmeli otomatik kaydetme) entegre edildi. Formda herhangi bir "Kaydet" butonuna ihtiyaç duyulmadan, kullanıcının veri girmesinden 1 saniye sonra asenkron olarak arka plana veri gönderiliyor.

## 2. Oracle Cloud Backend API (Flask & SQLite)
- Emrullah'ın Oracle sunucusu (`92.5.42.0`) üzerinde `/home/emrullah/workout-api/` dizininde bir Python Flask API yazıldı.
- Veritabanı olarak **SQLite** (`workout_notes.db`) tercih edildi. Tabloda `exercise_id` (PRIMARY KEY) ve `data` (JSON) sütunları mevcut. "Upsert" işlemi (`ON CONFLICT DO UPDATE`) kullanılarak dinamik kayıt atılabiliyor.
- API `emrullah.xyz` ve `emrullahxyz.github.io` adreslerinden (CORS) gelecek istekleri kabul edecek şekilde ayarlandı.
- API'ın sunucuda 7/24 aralıksız ve stabil çalışabilmesi için `systemd` servisi (`workout-api.service`) oluşturuldu ve aktif edildi.

## 3. Nginx & YunoHost (SSOwat) Yapılandırması
- Sunucu YunoHost mimarisinde olduğu için, `https://emrullah.xyz/api/workout/*` istekleri SSOwat kimlik doğrulama duvarına takılıyordu (Frontend tarafında 401/302 yönlendirmesi oluyordu).
- Bu problemi aşmak adına `/etc/nginx/conf.d/emrullah.xyz.d/workout.conf` adında özel bir Nginx bloğu eklendi.
- `access_by_lua_block { return }` kuralı kullanılarak YunoHost'un SSO yönlendirmesi sadece `/api/workout` route'u için by-pass edildi.
- Böylece GitHub Pages üzerinde barınan statik (Frontend) site, dinamik olarak özel Oracle sunucusuna kimlik doğrulamasına takılmadan güvenle veri okuyup yazabilir hale getirildi.

## 4. GitHub Versiyon Kontrolü
- Yapılan değişiklikler GitHub `emrullahxyz/exercises-dataset` deposuna başarıyla senkronize edildi.
- Arka plan yetki kilitlenmeleri aşılarak GitHub CLI ile token-based remote push yöntemiyle kodlar commitlendi.
