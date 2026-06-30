import json
import codecs

# Load JSON
with codecs.open('data/exercises.json', 'r', 'utf-8') as f:
    data = json.load(f)

targets = [
  'barbell bench press', 'dumbbell incline bench press', 'cable low fly', 'cable incline fly',
  'dumbbell seated shoulder press', 'dumbbell lateral raise',
  'cable overhead triceps extension (rope attachment)', 'cable triceps pushdown (v-bar)',
  'wheel rollerout', 'barbell full squat', 'barbell romanian deadlift',
  'barbell single leg split squat', 'lever seated leg curl', 'lever leg extension',
  'lever standing calf raise', 'cable kneeling crunch', 'hanging leg raise',
  'weighted pull-up', 'barbell bent over row', 'dumbbell incline row',
  'cable lat pulldown full range of motion', 'cable rear delt row (with rope)',
  'barbell curl', 'dumbbell incline curl', 'dumbbell hammer curl',
  'barbell glute bridge', 'walking lunge', 'lever seated calf raise',
  'lever back extension', 'cable twist'
]

sled_leg_press = next((x for x in data if 'sled 45' in x['name'] and 'leg press' in x['name'] and not any(p in x['name'] for p in ['one leg', 'back pov', 'side pov'])), None)

filtered = [x for x in data if x['name'] in targets]
if sled_leg_press:
    filtered.append(sled_leg_press)

json_str = json.dumps(filtered, ensure_ascii=False)

html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Gelişmiş Workout Planım</title>
    <style>
        :root {{
            --bg-color: #0f172a;
            --card-bg: #1e293b;
            --text-main: #f8fafc;
            --text-muted: #94a3b8;
            --accent: #3b82f6;
            --accent-hover: #2563eb;
            --danger: #ef4444;
        }}
        body {{
            font-family: 'Segoe UI', system-ui, sans-serif;
            background-color: var(--bg-color);
            color: var(--text-main);
            margin: 0;
            padding: 20px;
        }}
        h1 {{ text-align: center; color: var(--accent); }}
        
        /* Floating Button for Plan Image */
        .floating-btn {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background-color: var(--accent);
            color: white;
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            font-size: 24px;
            cursor: pointer;
            box-shadow: 0 4px 15px rgba(0,0,0,0.3);
            z-index: 100;
            transition: transform 0.2s;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        .floating-btn:hover {{
            transform: scale(1.1);
            background-color: var(--accent-hover);
        }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
            gap: 20px;
            max-width: 1200px;
            margin: 0 auto;
        }}
        .card {{
            background: var(--card-bg);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.2s;
            position: relative;
        }}
        .card:hover {{
            transform: translateY(-5px);
        }}
        .card-img-wrapper {{
            position: relative;
            width: 100%;
            padding-top: 100%; /* 1:1 Aspect Ratio */
            background: #fff;
            cursor: pointer;
        }}
        .card img {{
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: contain;
        }}
        .play-icon {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            background: rgba(0,0,0,0.6);
            color: white;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 24px;
            pointer-events: none;
            opacity: 0.8;
            transition: opacity 0.2s;
        }}
        .card-content {{
            padding: 15px;
            cursor: pointer;
        }}
        .card-title {{
            font-size: 1.1rem;
            font-weight: bold;
            margin: 0 0 10px 0;
            text-transform: capitalize;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        .info-icon {{
            color: var(--accent);
            font-size: 1.2rem;
        }}
        .badge-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }}
        .badge {{
            background: rgba(59, 130, 246, 0.2);
            color: #60a5fa;
            padding: 4px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            text-transform: capitalize;
        }}

        /* Modal Styles */
        .modal {{
            display: none;
            position: fixed;
            top: 0; left: 0; right: 0; bottom: 0;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }}
        .modal.active {{ display: flex; }}
        .modal-content {{
            background: var(--card-bg);
            border-radius: 12px;
            width: 100%;
            max-width: 600px;
            max-height: 90vh;
            overflow-y: auto;
            position: relative;
            padding: 20px;
        }}
        .modal-close {{
            position: absolute;
            top: 15px;
            right: 15px;
            background: none;
            border: none;
            color: var(--text-muted);
            font-size: 24px;
            cursor: pointer;
        }}
        .modal-close:hover {{ color: var(--text-main); }}
        .modal-img-container {{
            width: 100%;
            background: #fff;
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 20px;
            display: flex;
            justify-content: center;
        }}
        .modal-img-container img {{
            max-width: 100%;
            max-height: 300px;
            object-fit: contain;
        }}
        .plan-modal-img {{
            width: 100%;
            height: auto;
            border-radius: 8px;
        }}
    </style>
</head>
<body>
    <h1>Antrenman Programım</h1>
    
    <button class="floating-btn" onclick="openPlanModal()" title="Planı Göster">
        📅
    </button>

    <div class="grid" id="exercise-grid"></div>

    <!-- Exercise Modal -->
    <div class="modal" id="exercise-modal" onclick="if(event.target===this) closeModal()">
        <div class="modal-content">
            <button class="modal-close" onclick="closeModal()">×</button>
            <h2 id="modal-title" style="text-transform: capitalize; margin-top: 0;"></h2>
            <div class="modal-img-container">
                <img id="modal-img" src="" alt="Exercise">
            </div>
            <div id="modal-details"></div>
        </div>
    </div>

    <!-- Plan Modal -->
    <div class="modal" id="plan-modal" onclick="if(event.target===this) closePlanModal()">
        <div class="modal-content" style="max-width: 800px; text-align: center;">
            <button class="modal-close" onclick="closePlanModal()">×</button>
            <h2 style="margin-top:0;">Workout Planım</h2>
            <!-- Force reload by using absolute URL just in case, but keep relative as primary so it works on github pages -->
            <img src="./workout_new.png" class="plan-modal-img" alt="Workout Plan" onerror="this.onerror=null; this.src='https://raw.githubusercontent.com/emrullahxyz/exercises-dataset/main/workout_new.png';">
        </div>
    </div>

    <script>
        const exercises = {json_str};

        const grid = document.getElementById('exercise-grid');

        exercises.forEach((ex, index) => {{
            const card = document.createElement('div');
            card.className = 'card';
            
            const jpgUrl = 'https://raw.githubusercontent.com/emrullahxyz/exercises-dataset/main/data/exercises/' + ex.id + '/0.jpg';
            const gifUrl = 'https://raw.githubusercontent.com/emrullahxyz/exercises-dataset/main/data/exercises/' + ex.id + '/0.gif';
            
            const badges = [ex.target].concat(ex.secondaryMuscles || []).slice(0,3).map(m => `<span class="badge">${{m}}</span>`).join('');
            
            card.innerHTML = `
                <div class="card-img-wrapper" onclick="handleImgClick(event, ${{index}}, '${{jpgUrl}}', '${{gifUrl}}')">
                    <img id="img-${{index}}" src="${{jpgUrl}}" alt="${{ex.name}}" loading="lazy">
                    <div class="play-icon" id="play-${{index}}">▶</div>
                </div>
                <div class="card-content" onclick="openModal(${{index}})">
                    <h3 class="card-title">
                        ${{ex.name}}
                        <span class="info-icon">ℹ️</span>
                    </h3>
                    <div class="badge-container">
                        ${{badges}}
                    </div>
                </div>
            `;
            grid.appendChild(card);
        }});

        let playTimeouts = {{}};

        function handleImgClick(e, index, jpgUrl, gifUrl) {{
            e.stopPropagation();
            const imgEl = document.getElementById(`img-${{index}}`);
            const playIcon = document.getElementById(`play-${{index}}`);
            
            if (imgEl.src.includes('.gif')) return; // Already playing

            const timestamp = new Date().getTime();
            imgEl.src = `${{gifUrl}}?t=${{timestamp}}`;
            playIcon.style.opacity = '0';

            if (playTimeouts[index]) clearTimeout(playTimeouts[index]);

            // Play for ~4 seconds then stop
            playTimeouts[index] = setTimeout(() => {{
                imgEl.src = jpgUrl;
                playIcon.style.opacity = '0.8';
            }}, 4000);
        }}

        function openModal(index) {{
            const ex = exercises[index];
            document.getElementById('modal-title').textContent = ex.name;
            
            const gifUrl = 'https://raw.githubusercontent.com/emrullahxyz/exercises-dataset/main/data/exercises/' + ex.id + '/0.gif';
            document.getElementById('modal-img').src = gifUrl;
            
            let detailsHtml = '';
            
            if (ex.instructions && ex.instructions.tr) {{
                detailsHtml += '<h3>Nasıl Yapılır?</h3><ul>';
                ex.instructions.tr.forEach(step => {{
                    detailsHtml += `<li>${{step}}</li>`;
                }});
                detailsHtml += '</ul>';
            }} else if (ex.instructions) {{
                detailsHtml += '<h3>Instructions</h3><ul>';
                ex.instructions.forEach(step => {{
                    detailsHtml += `<li>${{step}}</li>`;
                }});
                detailsHtml += '</ul>';
            }}

            detailsHtml += `
                <p><strong>Hedef Kas:</strong> ${{ex.target}}</p>
                <p><strong>Ekipman:</strong> ${{ex.equipment}}</p>
            `;
            
            document.getElementById('modal-details').innerHTML = detailsHtml;
            document.getElementById('exercise-modal').classList.add('active');
        }}

        function closeModal() {{
            document.getElementById('exercise-modal').classList.remove('active');
            document.getElementById('modal-img').src = '';
        }}

        function openPlanModal() {{
            document.getElementById('plan-modal').classList.add('active');
        }}

        function closePlanModal() {{
            document.getElementById('plan-modal').classList.remove('active');
        }}
    </script>
</body>
</html>"""

with codecs.open('my_workout.html', 'w', 'utf-8') as f:
    f.write(html_content)
