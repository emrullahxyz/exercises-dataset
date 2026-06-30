import codecs
import re

with codecs.open('my_workout.html', 'r', 'utf-8') as f:
    content = f.read()

# 1. Day Tabs
old_tabs = '''  <div class="day-tabs" id="dayTabs">
    <button class="day-tab active" data-day="upperA">🔵 Upper A — İtme</button>
    <button class="day-tab" data-day="lowerFull">🟢 Lower — Tam Bacak</button>
    <button class="day-tab" data-day="upperB">🔴 Upper B — Çekiş</button>
    <button class="day-tab" data-day="lowerA">🟢 Lower A — Quad</button>
    <button class="day-tab" data-day="lowerB">🟠 Lower B — Posterior</button>
  </div>'''

new_tabs = '''  <div class="day-tabs" id="dayTabs">
    <button class="day-tab active" data-day="upperA">🔵 Upper A (Push)</button>
    <button class="day-tab" data-day="lowerA">🟢 Lower A (Quad)</button>
    <button class="day-tab" data-day="upperB">🔴 Upper B (Pull)</button>
    <button class="day-tab" data-day="lowerB">🟠 Lower B (Posterior)</button>
  </div>'''
content = content.replace(old_tabs, new_tabs)

# 2. Header Buttons
old_header = '''  <div class="header-meta">
    <button class="btn-plan" id="btnShowPlan">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
        <circle cx="8.5" cy="8.5" r="1.5"></circle>
        <polyline points="21 15 16 10 5 21"></polyline>
      </svg>
      Özet Görseli
    </button>
  </div>'''

new_header = '''  <div class="header-meta">
    <button class="btn-plan" id="btnShowRules" style="background: rgba(255,255,255,0.05); color: var(--text2);">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <circle cx="12" cy="12" r="10"></circle>
        <line x1="12" y1="16" x2="12" y2="12"></line>
        <line x1="12" y1="8" x2="12.01" y2="8"></line>
      </svg>
      Kurallar
    </button>
    <button class="btn-plan" id="btnShowPlan">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
        <rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect>
        <circle cx="8.5" cy="8.5" r="1.5"></circle>
        <polyline points="21 15 16 10 5 21"></polyline>
      </svg>
      Özet Görseli
    </button>
  </div>'''
content = content.replace(old_header, new_header)

# 3. PLAN object
plan_pattern = re.compile(r'const PLAN = \{.*?\n\};\n', re.DOTALL)
new_plan = '''const PLAN = {
  upperA: {
    title: '🔵 Upper A — İtme (Push)',
    sub: 'Göğüs · Omuz · Triceps',
    stats: [{ v: '8', l: 'Egzersiz' }, { v: '27', l: 'Set' }, { v: '~75', l: 'Dk' }],
    exercises: [
      { name: 'barbell bench press',                              sets: '4×5–6',   label: 'Ana İtiş Gücü' },
      { name: 'dumbbell incline bench press',                     sets: '3×8–10',  label: 'Üst Göğüs' },
      { name: 'dumbbell seated shoulder press',                   sets: '4×8–10',  label: 'Omuz Hacmi' },
      { name: 'cable low fly',                                    sets: '3×12–15', label: 'İç Göğüs İzolasyon' },
      { name: 'dumbbell lateral raise',                           sets: '4×15–20', label: 'Yan Omuz (Genişlik)' },
      { name: 'cable standing overhead triceps extension',        sets: '3×12–15', label: 'Triceps Uzun Baş' },
      { name: 'cable triceps pushdown',                           sets: '3×12–15', label: 'Triceps Hacim' },
      { name: 'wheel rollerout',                                  sets: '3×8-10',  label: 'Core / Karın' },
      { name: 'cable standing shoulder external rotation',        sets: '2×15–20', label: 'Rotator Cuff (Prehab)' }
    ]
  },
  lowerA: {
    title: '🟢 Lower A — Quad Dominant',
    sub: 'Ön Bacak Odaklı',
    stats: [{ v: '7', l: 'Egzersiz' }, { v: '23', l: 'Set' }, { v: '~75', l: 'Dk' }],
    exercises: [
      { name: 'barbell full squat',              sets: '4×5–6',             label: 'Ana Güç Hareketi' },
      { name: 'sled 45° leg press (side pov)',   sets: '3×12–15',           label: 'Quad Hacmi' },
      { name: 'barbell single leg split squat',  sets: '3×8–10',            label: 'Bulgarian Split Squat' },
      { name: 'lever leg extension',             sets: '3×15–20',           label: 'Quad İzolasyon' },
      { name: 'lever standing calf raise',       sets: '4×15–20',           label: 'Baldır Hacmi' },
      { name: 'hanging leg raise',               sets: '3×10–15',           label: 'Core (Alt Karın)' },
      { name: 'cable kneeling crunch',           sets: '3×15–20',           label: 'Rectus Abdominis' }
    ]
  },
  upperB: {
    title: '🔴 Upper B — Çekiş (Pull)',
    sub: 'Sırt · Biceps · Arka Omuz',
    stats: [{ v: '8', l: 'Egzersiz' }, { v: '26', l: 'Set' }, { v: '~75', l: 'Dk' }],
    exercises: [
      { name: 'weighted pull-up',                            sets: '4×4–6',   label: 'Sırt Güç Tabanı' },
      { name: 'barbell bent over row',                       sets: '4×6–8',   label: 'Sırt Kalınlığı' },
      { name: 'dumbbell incline row',                        sets: '3×10–12', label: 'Chest Supported Row' },
      { name: 'cable lat pulldown full range of motion',     sets: '3×10–12', label: 'Sırt Genişliği (Wide Grip)' },
      { name: 'cable rear delt row (with rope)',             sets: '3×15–20', label: 'Face Pull Alternatifi' },
      { name: 'barbell curl',                                sets: '3×8–10',  label: 'Biceps Güç' },
      { name: 'dumbbell incline curl',                       sets: '3×10–12', label: 'Biceps Uzun Baş' },
      { name: 'dumbbell hammer curl',                        sets: '2×12–15', label: 'Brachialis & Ön Kol' }
    ]
  },
  lowerB: {
    title: '🟠 Lower B — Posterior Chain',
    sub: 'Arka Bacak · Glute · Hamstring',
    stats: [{ v: '7', l: 'Egzersiz' }, { v: '25', l: 'Set' }, { v: '~75', l: 'Dk' }],
    exercises: [
      { name: 'barbell romanian deadlift', sets: '4×6–8',            label: 'Arka Bacak + Kalça Güç' },
      { name: 'barbell glute bridge',      sets: '4×10–12',           label: 'Hip Thrust (Glute)' },
      { name: 'lever seated leg curl',     sets: '4×10–12',           label: 'Hamstring İzolasyon' },
      { name: 'walking lunge',             sets: '3×12 Adım',         label: 'Bacak Bütünü + Denge' },
      { name: 'lever back extension',      sets: '3×12–15',           label: 'Alt Sırt (Reverse Hyper alt.)' },
      { name: 'lever seated calf raise',   sets: '4×15–20',           label: 'Soleus (İç Baldır)' },
      { name: 'cable twist',               sets: '3×15',              label: 'Obliques' }
    ]
  }
};
'''
content = plan_pattern.sub(new_plan, content)


# 4. GIF loop count from 3 to 2
content = content.replace('const totalLoops = 3;', 'const totalLoops = 2;')


# 5. Modals & JS
old_modal_html = '</div>\n</div>\n\n<script>'
new_modal_html = '''</div>\n</div>\n\n<!-- ── RULES MODAL ── -->
<div class="modal-overlay" id="rulesOverlay">
  <div class="modal-panel" style="width: min(700px, 100%);">
    <div class="modal-header">
      <h2 class="modal-title">Program Kuralları</h2>
      <button class="modal-close" id="rulesClose">✕</button>
    </div>
    <div style="padding: 24px; color: var(--text2); line-height: 1.7; font-size: 14px; max-height: 70vh; overflow-y: auto;">
      <h3 style="color: var(--text1); margin-bottom: 8px;">🔄 Progressive Overload (Double Progression)</h3>
      <p>Örneğin Bench Press (4x5–6):</p>
      <ul style="margin-bottom: 16px; margin-left: 20px;">
        <li>Hafta 1: 80 kg → 6, 5, 5, 5</li>
        <li>Hafta 2: 80 kg → 6, 6, 6, 5</li>
        <li>Hafta 3: 80 kg → 6, 6, 6, 6 (Üst sınıra ulaşıldı!)</li>
        <li>Hafta 4: 82.5 kg → Tekrar 5-6 aralığında başla.</li>
      </ul>
      <p style="margin-bottom: 24px;"><strong>Kural:</strong> Tekrar aralığının üst sınırına tüm setlerde ulaştığında ağırlığı artır.</p>

      <h3 style="color: var(--text1); margin-bottom: 8px;">🔋 Deload Protokolü (Her 4-6 Haftada Bir)</h3>
      <ul style="margin-bottom: 24px; margin-left: 20px;">
        <li>Ağırlıkları %60’a düşür.</li>
        <li>Set sayılarını %30-40 azalt (Örn: 4 set yerine 2-3 set yap).</li>
        <li>Asla tükenişe (failure) gitme. Amaç CNS ve tendonların toparlanmasıdır.</li>
      </ul>

      <h3 style="color: var(--text1); margin-bottom: 8px;">📅 Version A (Yoğun Haftalar İçin)</h3>
      <p style="margin-bottom: 16px;">Sadece 3 gün spora gidebildiğin haftalarda <strong>Pazartesi (Upper A), Çarşamba (Lower A) ve Cumartesi (Upper B)</strong> günlerini uygula. Hacim kaybını engellemek için şu egzersizlere <strong>+1 Set</strong> ekle:</p>
      <ul style="margin-bottom: 24px; margin-left: 20px;">
        <li><strong>Upper A:</strong> Cable Fly, Lateral Raise, Triceps Pushdown</li>
        <li><strong>Lower A:</strong> Leg Extension, Calf Raise</li>
        <li><strong>Upper B:</strong> Lat Pulldown, Face Pull, Hammer Curl</li>
      </ul>

      <h3 style="color: var(--text1); margin-bottom: 8px;">⚠️ Dikkat Edilecekler</h3>
      <ul style="margin-bottom: 16px; margin-left: 20px;">
        <li>Omuz sağlığı için <strong>External Rotation</strong> egzersizini Upper A gününün sonunda (2x15-20) yapabilirsin.</li>
        <li>Cuma günleri <strong>Squash</strong> oynamaya devam et (Aktif toparlanma). Core bölgesi Squash'ta çok çalıştığı için karın hareketlerinde tükenişe gitme (2-3 tekrar rezerv bırak).</li>
        <li>Sürekli program değiştirme, uzun süre bu sisteme sadık kal ve ağırlık loglarını tut.</li>
      </ul>
    </div>
  </div>
</div>

<script>'''
content = content.replace(old_modal_html, new_modal_html)

# Append Rules modal JS
old_js = '''function closePlanModal() {
  planOverlay.classList.remove('open');
  document.body.style.overflow = '';
}

planClose.addEventListener('click', closePlanModal);
planOverlay.addEventListener('click', e => {
  if (e.target === e.currentTarget) closePlanModal();
});'''

new_js = '''function closePlanModal() {
  planOverlay.classList.remove('open');
  document.body.style.overflow = '';
}
function closeRulesModal() {
  rulesOverlay.classList.remove('open');
  document.body.style.overflow = '';
}

planClose.addEventListener('click', closePlanModal);
planOverlay.addEventListener('click', e => {
  if (e.target === e.currentTarget) closePlanModal();
});

const rulesOverlay = document.getElementById('rulesOverlay');
const rulesClose = document.getElementById('rulesClose');
document.getElementById('btnShowRules').addEventListener('click', () => {
  rulesOverlay.classList.add('open');
  document.body.style.overflow = 'hidden';
});
rulesClose.addEventListener('click', closeRulesModal);
rulesOverlay.addEventListener('click', e => {
  if (e.target === e.currentTarget) closeRulesModal();
});'''
content = content.replace(old_js, new_js)

# Fix Escape handler
old_esc = '''document.addEventListener('keydown', e => { 
  if (e.key === 'Escape') {
    closeModal();
    closePlanModal();
  }
});'''
new_esc = '''document.addEventListener('keydown', e => { 
  if (e.key === 'Escape') {
    closeModal();
    closePlanModal();
    if(typeof closeRulesModal === 'function') closeRulesModal();
  }
});'''
content = content.replace(old_esc, new_esc)

with codecs.open('my_workout.html', 'w', 'utf-8') as f:
    f.write(content)

print('Success')
