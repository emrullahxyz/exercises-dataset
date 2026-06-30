import codecs
import json
import re

with codecs.open('template_dump.html', 'r', 'utf-8') as f:
    template = f.read()

with codecs.open('workout_exercises_data.json', 'r', 'utf-8') as f:
    json_data = f.read()

# Replace JSON placeholder
html = template.replace('__EXERCISES_JSON__', json_data)

# Fix github raw links
html = html.replace('hasaneyldrm', 'emrullahxyz')

# Find the renderSession innerHTML and event listeners part
old_card_code = """    card.innerHTML = `
      <span class="ex-num">${i + 1}</span>
      <div class="ex-img-wrap">
        <img src="https://raw.githubusercontent.com/emrullahxyz/exercises-dataset/main/${data.image}" alt="${data.name}" loading="lazy" />
        <div class="ex-play">
          <div class="ex-play-icon">
            <svg viewBox="0 0 16 16"><path d="M4 2l10 6-10 6V2z"/></svg>
          </div>
        </div>
      </div>
      <div class="ex-info">
        <div class="ex-name">${data.name}</div>
        <div class="ex-tags">
          <span class="ex-tag ex-tag-target">${data.target}</span>
          <span class="ex-tag ex-tag-equip">${data.equipment}</span>
        </div>
        <div class="ex-sets">${ex.sets}</div>
      </div>
    `;

    card.addEventListener('click', () => openModal(data, ex));
    card.addEventListener('keydown', e => { if (e.key === 'Enter') openModal(data, ex); });
    grid.appendChild(card);"""

new_card_code = """    card.innerHTML = `
      <span class="ex-num">${i + 1}</span>
      <div class="ex-img-wrap" id="img-wrap-${i}-${dayKey}">
        <img src="https://raw.githubusercontent.com/emrullahxyz/exercises-dataset/main/${data.image}" id="img-${i}-${dayKey}" alt="${data.name}" loading="lazy" />
        <div class="ex-play" id="play-${i}-${dayKey}">
          <div class="ex-play-icon">
            <svg viewBox="0 0 16 16"><path d="M4 2l10 6-10 6V2z"/></svg>
          </div>
        </div>
      </div>
      <div class="ex-info" id="info-${i}-${dayKey}" style="cursor: pointer;">
        <div class="ex-name" style="display:flex; justify-content:space-between; align-items:center;">
          <span>${data.name}</span>
          <span style="opacity:0.5; font-size:1.2em;" title="Detayları Gör">ℹ️</span>
        </div>
        <div class="ex-tags">
          <span class="ex-tag ex-tag-target">${data.target}</span>
          <span class="ex-tag ex-tag-equip">${data.equipment}</span>
        </div>
        <div class="ex-sets">${ex.sets}</div>
      </div>
    `;

    grid.appendChild(card);

    const imgWrap = card.querySelector('#img-wrap-' + i + '-' + dayKey);
    const infoWrap = card.querySelector('#info-' + i + '-' + dayKey);
    const imgEl = card.querySelector('#img-' + i + '-' + dayKey);
    const playEl = card.querySelector('#play-' + i + '-' + dayKey);

    imgWrap.addEventListener('click', (e) => {
      e.stopPropagation();
      if (imgEl.src.includes('.gif')) return;
      const t = new Date().getTime();
      imgEl.src = "https://raw.githubusercontent.com/emrullahxyz/exercises-dataset/main/" + data.gif_url + "?t=" + t;
      playEl.style.opacity = '0';
      setTimeout(() => {
        imgEl.src = "https://raw.githubusercontent.com/emrullahxyz/exercises-dataset/main/" + data.image;
        playEl.style.opacity = '';
      }, 4000);
    });

    infoWrap.addEventListener('click', () => openModal(data, ex));
    card.addEventListener('keydown', e => { if (e.key === 'Enter') openModal(data, ex); });"""

html = html.replace(old_card_code, new_card_code)

with codecs.open('my_workout.html', 'w', 'utf-8') as f:
    f.write(html)

print("Generated my_workout.html successfully.")
