// ============================================================
//  GFL2 Wiki — Data Entry Tool  (app.js)
//  Handles: character, weapon, and FAQ tabs
//  No external dependencies; runs in any modern browser.
// ============================================================

'use strict';

// ── Constants ─────────────────────────────────────────────────────────────
const CLASS_LIST = ['Bulwark', 'Vanguard', 'Support', 'Sentinel'];
const RARITY_LIST = ['Elite', 'Standard'];
const PHASE_LIST = ['Physical', 'Burn', 'Hydro', 'Electric', 'Freeze', 'Corrosion', 'Resonance'];
const WEAPON_TYPES = ['Assault Rifle', 'SMG', 'Shotgun', 'MG', 'Sniper Rifle', 'Handgun', 'Blade'];
const AMMO_TYPES = ['Light Ammo', 'Medium Ammo', 'Heavy Ammo', 'Shotgun Ammo', 'Melee'];
const SKILL_TAGS = ['Basic Attack', 'Active', 'Buff', 'Debuff', 'Targeted', 'AoE', 'Passive', 'Healing', 'Shield'];
const RARITY_W_LIST = ['SSR', 'SR', 'R'];

// Loaded from assets/effects.json at boot
let EFFECTS_DATA = {}; // { "Effect Name": "description…", … }

// ── Internationalization state & helpers ──────────────────────────────────
let currentLang = 'en';
try {
  const savedLang = localStorage.getItem('gfl2_lang');
  if (savedLang === 'vi' || savedLang === 'en') currentLang = savedLang;
} catch (e) {
  console.warn('localStorage not accessible:', e);
}
let VI_DATA = null;
let CHARACTERS_INDEX = [];
let loadedCharacterSlug = null;

// ── Utility ───────────────────────────────────────────────────────────────
const $ = id => document.getElementById(id);
const el = (tag, attrs = {}, ...children) => {
  const e = document.createElement(tag);
  Object.entries(attrs).forEach(([k, v]) => {
    if (k === 'cls') e.className = v;
    else if (k === 'html') e.innerHTML = v;
    else if (k.startsWith('on')) e.addEventListener(k.slice(2), v);
    else e.setAttribute(k, v);
  });
  children.forEach(c => c != null && e.append(typeof c === 'string' ? document.createTextNode(c) : c));
  return e;
};

function slugify(s) {
  return s.trim().toLowerCase()
    .normalize('NFD').replace(/[\u0300-\u036f]/g, '')
    .replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '');
}

function makeSelect(opts, value = '', placeholder = '— select —') {
  const s = el('select');
  s.append(el('option', { value: '' }, placeholder));
  opts.forEach(o => {
    const opt = el('option', { value: o }, o);
    if (o === value) opt.selected = true;
    s.append(opt);
  });
  return s;
}

function showToast(msg, type = 'ok', duration = 2800) {
  const t = $('toast');
  t.textContent = msg;
  t.className = `show ${type}`;
  setTimeout(() => { t.className = ''; }, duration);
}

// Strip null / '' / [] / {} from object recursively
function compact(obj) {
  if (Array.isArray(obj)) return obj.map(compact).filter(v => v != null);
  if (obj !== null && typeof obj === 'object') {
    const out = {};
    for (const [k, v] of Object.entries(obj)) {
      const cv = compact(v);
      if (cv !== null && cv !== '' && !(Array.isArray(cv) && cv.length === 0)) {
        out[k] = cv;
      }
    }
    return out;
  }
  return obj;
}

// Syntax-highlighted JSON
function syntaxHL(json) {
  return json
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)/g, m => {
      let cls = 'jv-num';
      if (/^"/.test(m)) cls = /:$/.test(m) ? 'jk' : 'jv-str';
      else if (/true|false/.test(m)) cls = 'jv-bool';
      else if (/null/.test(m)) cls = 'jv-null';
      return `<span class="${cls}">${m}</span>`;
    });
}

// Download a string as a file
function downloadFile(filename, content) {
  const a = document.createElement('a');
  a.href = URL.createObjectURL(new Blob([content], { type: 'application/json' }));
  a.download = filename;
  a.click();
}

// Ordered JSON serialise (schema key order)
const CHAR_KEY_ORDER = [
  'slug', 'name', 'class', 'rarity', 'phase', 'weapon_type', 'ammo_type',
  'signature_weapon', 'stats', 'skill_attribute', 'weakness', 'stability_gauge',
  'movement_speed', 'effects_glossary', 'skills', 'summons', 'fortification', 'neural_helix',
  'keys', 'images', 'source_notes'
];
function orderedStringify(obj, keyOrder = null) {
  function replacer(key, value) { return value; }
  if (!keyOrder) return JSON.stringify(obj, replacer, 2);
  // Reorder top-level keys
  const ordered = {};
  keyOrder.forEach(k => { if (k in obj) ordered[k] = obj[k]; });
  Object.keys(obj).forEach(k => { if (!(k in ordered)) ordered[k] = obj[k]; });
  return JSON.stringify(ordered, replacer, 2);
}

// ─────────────────────────────────────────────────────────────────────────
//  TAB SWITCHING
// ─────────────────────────────────────────────────────────────────────────
function initTabs() {
  document.querySelectorAll('.tab-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
      btn.classList.add('active');
      $(btn.dataset.tab).classList.add('active');
      refreshPreview();
    });
  });
}

// ─────────────────────────────────────────────────────────────────────────
//  LIVE PREVIEW
// ─────────────────────────────────────────────────────────────────────────
function refreshPreview() {
  const activeTab = document.querySelector('.tab-content.active');
  let data = {};
  if (activeTab?.id === 'tab-character') {
    data = currentLang === 'vi' ? gatherCharacterVi() : gatherCharacter();
  } else if (activeTab?.id === 'tab-weapon') {
    data = gatherWeapon();
  } else if (activeTab?.id === 'tab-faq') {
    data = gatherFaq();
  }
  const json = orderedStringify(compact(data), (activeTab?.id === 'tab-character' && currentLang === 'en') ? CHAR_KEY_ORDER : null);
  $('json-preview').innerHTML = syntaxHL(json);
}

// ─────────────────────────────────────────────────────────────────────────
//  ████  CHARACTER TAB  ████
// ─────────────────────────────────────────────────────────────────────────
let skillCounter = 0;
let summonCounter = 0;
let glossaryCounter = 0;
let fortCounter = 0;
let nhCounter = 0;
let keyCounter = 0;

function initCharacterTab() {
  // Load existing characters from search-index
  loadExistingCharacters();

  // Auto-slug from name
  $('c-name').addEventListener('input', () => {
    const slug = slugify($('c-name').value);
    $('c-slug').value = slug;
    refreshImagePaths(slug);
    refreshFortSkillDropdowns();
    refreshPreview();
  });
  $('c-slug').addEventListener('input', () => {
    refreshImagePaths($('c-slug').value);
    refreshPreview();
  });
  $('c-class').addEventListener('change', () => {
    refreshImagePaths($('c-slug').value);
  });

  // Wire all basic-info inputs to preview
  document.querySelectorAll('#tab-character input, #tab-character select, #tab-character textarea')
    .forEach(el => el.addEventListener('input', refreshPreview));

  // Glossary
  $('btn-add-glossary').addEventListener('click', addGlossaryRow);
  // Skills
  $('btn-add-skill').addEventListener('click', addSkillCard);
  // Summons
  $('btn-add-summon').addEventListener('click', () => addSummonCard());
  // Fortification (pre-populate 6 tiers)
  for (let i = 1; i <= 6; i++) addFortRow(i);
  // Neural Helix (pre-populate 6 nodes)
  for (let i = 1; i <= 6; i++) addNHRow(i);
  // Keys (pre-populate 9 slots)
  const KEY_NAMES = [
    'Fixed Key 1', 'Fixed Key 2', 'Fixed Key 3',
    'Fixed Key 4', 'Fixed Key 5', 'Fixed Key 6',
    'Affinity Key', 'Common Key', 'Expansion Key'
  ];
  KEY_NAMES.forEach((n, idx) => addKeyRow(n, idx < 6 ? '' : n === 'Affinity Key' ? 'Affinity Lvl 5' : ''));

  // Action buttons
  $('btn-save-char').addEventListener('click', saveToFileSystem);
  $('btn-download-char').addEventListener('click', downloadCharacter);
  $('btn-load-char').addEventListener('click', () => $('file-load-char').click());
  $('file-load-char').addEventListener('change', loadCharacter);
  $('btn-clear-char').addEventListener('click', clearCharacterForm);

  // Existing character selector
  $('btn-load-existing').addEventListener('click', () => {
    const slug = $('char-selector').value;
    if (!slug) { showToast('Select a character first', 'err'); return; }
    loadCharacterBySlug(slug);
  });
  $('char-selector').addEventListener('dblclick', () => {
    const slug = $('char-selector').value;
    if (slug) loadCharacterBySlug(slug);
  });

  // Image upload
  initImageUpload();
}

// ── Glossary ───────────────────────────────────────────────────────────
function addGlossaryRow(text = '') {
  glossaryCounter++;
  const id = `gloss-${glossaryCounter}`;
  const row = el('div', { cls: 'repeat-item', id });
  const header = el('div', { cls: 'item-header' });
  header.append(
    el('span', { cls: 'item-index' }, `Status Effect ${glossaryCounter}`),
    makeBtnRemove(id, 'glossary-list', refreshPreview)
  );
  const inp = el('input', { type: 'text', placeholder: 'e.g. Shelter: Gains Stability Protection…' });
  if (text) inp.value = text;
  inp.addEventListener('input', refreshPreview);
  row.append(header, inp);
  $('glossary-list').append(row);
  refreshPreview();
}

// ── Skills ─────────────────────────────────────────────────────────────
function addSkillCard(data = {}) {
  skillCounter++;
  const id = `skill-${skillCounter}`;
  const card = el('div', { cls: 'skill-card', id });

  // Header
  const hdr = el('div', { cls: 'skill-card-header' });
  const idxBadge = el('span', { cls: 'item-index' }, `${t('sec_skills_title', currentLang)} ${skillCounter}`);
  const nameInput = el('input', { type: 'text', placeholder: t('placeholder_skill_name', currentLang), style: 'flex:1;min-width:0' });
  if (data.name) nameInput.value = data.name;
  if (data.en_name) nameInput.dataset.enName = data.en_name;
  nameInput.addEventListener('input', () => { refreshFortSkillDropdowns(); refreshPreview(); });

  hdr.append(idxBadge, nameInput, makeBtnRemove(id, 'skills-list', () => { refreshFortSkillDropdowns(); refreshPreview(); }));

  // Body
  const body = el('div', { cls: 'skill-card-body' });

  // Tags
  const tagField = el('div', { cls: 'field' });
  tagField.append(el('label', { 'data-i18n': 'skill_tags' }, t('skill_tags', currentLang)));
  const tagGrid = el('div', { cls: 'tag-grid', id: `${id}-tags` });
  (window.TERMS ? window.TERMS.tags : []).forEach(item => {
    const label = currentLang === 'vi' ? item.vi : item.en;
    const pill = el('span', { cls: 'tag-pill' }, label);
    pill.dataset.tagEn = item.en;
    pill.dataset.tagVi = item.vi;
    const isSelected = data.tags?.some(tStr =>
      tStr.toLowerCase() === item.en.toLowerCase() ||
      tStr.toLowerCase() === item.vi.toLowerCase()
    );
    if (isSelected) pill.classList.add('selected');
    pill.addEventListener('click', () => { pill.classList.toggle('selected'); refreshPreview(); });
    tagGrid.append(pill);
  });
  tagField.append(tagGrid);

  // Row 1: ammo_type, stability_damage, cooldown, confectance_cost
  const row1 = el('div', { cls: 'field-row' });
  const currentAmmoVal = data.ammo_type ? mapTerm(data.ammo_type, 'ammo_types', currentLang) : '';
  const ammoSel = makeSelect(getTermList('ammo_types', currentLang), currentAmmoVal, t('placeholder_select', currentLang));
  ammoSel.addEventListener('change', refreshPreview);
  row1.append(
    wrapField(t('skill_ammo_type', currentLang), ammoSel, 'skill_ammo_type'),
    wrapField(t('skill_stab_dmg', currentLang), numInput(data.stability_damage, 'e.g. 4'), 'skill_stab_dmg'),
    wrapField(t('skill_cooldown', currentLang), textInput(data.cooldown, t('placeholder_skill_cd', currentLang)), 'skill_cooldown'),
    wrapField(t('skill_confectance', currentLang), numInput(data.confectance_cost, '0'), 'skill_confectance')
  );

  // Row 2: range, effect_area
  const row2 = el('div', { cls: 'field-row two' });
  row2.append(
    wrapField(t('skill_range', currentLang), numInput(data.range, t('placeholder_skill_range', currentLang)), 'skill_range'),
    wrapField(t('skill_effect_area', currentLang), textInput(data.effect_area, t('placeholder_skill_area', currentLang)), 'skill_effect_area')
  );

  // Description
  const descField = el('div', { cls: 'field full' });

  // Label row: "Description" + Insert Effect picker
  const descLabelRow = el('div', { cls: 'desc-label-row' });
  descLabelRow.append(el('label', { 'data-i18n': 'skill_desc' }, t('skill_desc', currentLang)));
  descLabelRow.append(makeEffectInserter(() => descTA));
  descField.append(descLabelRow);

  const descTA = el('textarea', { rows: 3, placeholder: t('placeholder_skill_desc', currentLang) });
  if (data.description) descTA.value = data.description;
  descTA.addEventListener('input', refreshPreview);
  descField.append(descTA);

  body.append(tagField, row1, row2, descField);
  card.append(hdr, body);
  $('skills-list').append(card);
  wireInputs(card, refreshPreview);
  refreshFortSkillDropdowns();
  refreshPreview();
}

// ── Summons ────────────────────────────────────────────────────────────
function addSummonCard(data = {}) {
  summonCounter++;
  const id = `summon-${summonCounter}`;
  const card = el('div', { cls: 'skill-card', id });

  // Header
  const hdr = el('div', { cls: 'skill-card-header' });
  const idxBadge = el('span', { cls: 'item-index' }, `Summon Unit ${summonCounter}`);
  const nameInput = el('input', { type: 'text', cls: 's-name-inp', placeholder: 'Summon unit name…', style: 'flex:1;min-width:0' });
  if (data.name) nameInput.value = data.name;
  nameInput.addEventListener('input', refreshPreview);
  
  hdr.append(idxBadge, nameInput, makeBtnRemove(id, 'summons-list', refreshPreview));

  // Body
  const body = el('div', { cls: 'skill-card-body' });

  // Stats row
  const statsRow = el('div', { cls: 'field-row three' });
  const hpInp = numInput(data.stats?.hp, 'HP'); hpInp.className = 's-hp-inp';
  const atkInp = numInput(data.stats?.atk, 'ATK'); atkInp.className = 's-atk-inp';
  const defInp = numInput(data.stats?.def, 'DEF'); defInp.className = 's-def-inp';
  statsRow.append(wrapField('HP', hpInp), wrapField('ATK', atkInp), wrapField('DEF', defInp));

  // Other stats row
  const otherStatsRow = el('div', { cls: 'field-row two' });
  const stabInp = textInput(data.stability_gauge, 'e.g. 12 points'); stabInp.className = 's-stab-inp';
  const moveInp = textInput(data.movement_speed, 'e.g. 6 tiles'); moveInp.className = 's-move-inp';
  otherStatsRow.append(wrapField('Stability Gauge', stabInp), wrapField('Movement Speed', moveInp));

  // Skills container
  const skillsContainer = el('div', { cls: 'field full', style: 'margin-top: 12px; border-top: 1px solid var(--border); padding-top: 12px;' });
  skillsContainer.append(el('label', {}, 'Summon Skills'));
  const skillsList = el('div', { cls: 'repeat-list', id: `${id}-skills-list` });
  const btnAddSkill = el('button', { cls: 'btn-add', type: 'button' }, '+ Add Summon Skill');
  skillsContainer.append(skillsList, btnAddSkill);

  let sSkillCounter = 0;
  const addSummonSkill = (skData = {}) => {
    sSkillCounter++;
    const skId = `${id}-skill-${sSkillCounter}`;
    const skRow = el('div', { cls: 'repeat-item', id: skId, style: 'background: var(--bg-alt)' });

    const skHdr = el('div', { cls: 'item-header' });
    const skName = el('input', { type: 'text', cls: 's-skill-name-inp', placeholder: 'Skill Name' });
    if (skData.name) skName.value = skData.name;
    skHdr.append(skName, makeBtnRemove(skId, `${id}-skills-list`, refreshPreview));

    const skDescLabelRow = el('div', { cls: 'desc-label-row' });
    skDescLabelRow.append(el('label', {}, 'Description'));
    skDescLabelRow.append(makeEffectInserter(() => skDesc));

    const skDesc = el('textarea', { rows: 2, placeholder: 'Skill description…' });
    if (skData.description) skDesc.value = skData.description;

    skRow.append(skHdr, skDescLabelRow, skDesc);
    skillsList.append(skRow);
    wireInputs(skRow, refreshPreview);
    refreshPreview();
  };

  btnAddSkill.addEventListener('click', () => addSummonSkill());
  if (data.skills?.length) {
    data.skills.forEach(sk => addSummonSkill(sk));
  } else {
    addSummonSkill();
  }

  body.append(statsRow, otherStatsRow, skillsContainer);
  card.append(hdr, body);
  $('summons-list').append(card);
  wireInputs(card, refreshPreview);
  refreshPreview();
}

// ── Fortification ──────────────────────────────────────────────────────
function addFortRow(tier = null, data = {}) {
  fortCounter++;
  const tNum = tier ?? fortCounter;
  const id = `fort-${tNum}`;
  const row = el('div', { cls: 'repeat-item', id });

  const header = el('div', { cls: 'item-header' });
  const canRemove = tier === null;
  header.append(el('span', { cls: 'item-index' }, `${t('tier_label', currentLang)} ${tNum}`));
  if (canRemove) header.append(makeBtnRemove(id, 'fort-list', refreshPreview));

  // Tier number (hidden / display)
  const tierInp = el('input', { type: 'number', style: 'display:none' });
  tierInp.value = tNum;

  const rowContent = el('div', { cls: 'field-row' });
  const skillSel = el('select');
  skillSel.append(el('option', { value: '' }, t('placeholder_select', currentLang)));
  skillSel.addEventListener('change', refreshPreview);
  if (data.skill) skillSel.dataset.pendingSkill = data.skill;

  const levelInp = el('input', { type: 'number', placeholder: 'e.g. 2', min: 1 });
  if (data.level != null) levelInp.value = data.level;
  levelInp.addEventListener('input', refreshPreview);

  rowContent.append(
    wrapField(t('target_skill_label', currentLang), skillSel, 'target_skill_label'),
    wrapField(t('req_level_label', currentLang), levelInp, 'req_level_label')
  );

  const effectField = el('div', { cls: 'field full' });
  effectField.append(el('label', { 'data-i18n': 'effect_label' }, t('effect_label', currentLang)));
  const effectTA = el('textarea', { rows: 2, placeholder: t('placeholder_fort_effect', currentLang) });
  if (data.effect) effectTA.value = data.effect;
  effectTA.addEventListener('input', refreshPreview);
  effectField.append(effectTA);

  row.append(header, tierInp, rowContent, effectField);
  $('fort-list').append(row);
  refreshFortSkillDropdowns();
}

function refreshFortSkillDropdowns() {
  const skillCards = [...document.querySelectorAll('#skills-list .skill-card')];
  const skillNames = skillCards.map(card => {
    const inp = card.querySelector('input[type="text"]');
    return inp ? inp.value.trim() : '';
  }).filter(Boolean);

  document.querySelectorAll('#fort-list select').forEach(sel => {
    const current = sel.value || sel.dataset.pendingSkill || '';
    sel.innerHTML = '';
    sel.append(el('option', { value: '' }, t('placeholder_select', currentLang)));
    skillNames.forEach(sn => {
      const opt = el('option', { value: sn }, sn);
      if (sn.toLowerCase() === current.toLowerCase()) opt.selected = true;
      sel.append(opt);
    });
    delete sel.dataset.pendingSkill;
  });
}

// ── Neural Helix ───────────────────────────────────────────────────────
function addNHRow(idx = null, data = {}) {
  nhCounter++;
  const i = idx ?? nhCounter;
  const id = `nh-${nhCounter}`;
  const row = el('div', { cls: 'repeat-item', id });

  const header = el('div', { cls: 'item-header' });
  const defaultNodeName = currentLang === 'vi' ? `Cường Hóa ${i}` : `Enhancement ${i}`;
  header.append(el('span', { cls: 'item-index' }, defaultNodeName));
  if (idx === null) header.append(makeBtnRemove(id, 'nh-list', refreshPreview));

  const rowContent = el('div', { cls: 'field-row three' });
  const nodeInp = textInput(data.node || (idx ? defaultNodeName : ''), t('node_name_label', currentLang));
  const levelInp = numInput(data.level, t('req_level_label', currentLang));
  const mats = textInput(data.materials, t('placeholder_nh_materials', currentLang));
  wireInput(nodeInp, refreshPreview);
  wireInput(levelInp, refreshPreview);
  wireInput(mats, refreshPreview);
  rowContent.append(
    wrapField(t('node_name_label', currentLang), nodeInp, 'node_name_label'),
    wrapField(t('req_level_label', currentLang), levelInp, 'req_level_label'),
    wrapField(currentLang === 'vi' ? 'Nguyên Liệu' : 'Materials', mats)
  );

  const effectField = el('div', { cls: 'field full' });
  effectField.append(el('label', { 'data-i18n': 'effect_label' }, t('effect_label', currentLang)));
  const effectTA = el('textarea', { rows: 1, placeholder: t('placeholder_nh_effect', currentLang) });
  if (data.effect) effectTA.value = data.effect;
  effectTA.addEventListener('input', refreshPreview);
  effectField.append(effectTA);

  row.append(header, rowContent, effectField);
  $('nh-list').append(row);
  refreshPreview();
}

// ── Keys ───────────────────────────────────────────────────────────────
function addKeyRow(name = '', defaultLevel = '', data = {}) {
  keyCounter++;
  const id = `key-${keyCounter}`;
  const row = el('div', { cls: 'repeat-item', id });

  const header = el('div', { cls: 'item-header' });
  header.append(
    el('span', { cls: 'item-index' }, `${t('key_name_label', currentLang)} ${keyCounter}`),
    makeBtnRemove(id, 'keys-list', refreshPreview)
  );

  const rowContent = el('div', { cls: 'field-row three' });
  const nameInp = textInput(data.name || name, t('key_name_label', currentLang));
  nameInp.addEventListener('input', () => { nameInp.dataset.userEdited = 'true'; refreshPreview(); });

  const levelInp = textInput(data.level != null ? String(data.level) : defaultLevel, t('req_level_label', currentLang));
  const matsInp = textInput(data.materials || '', t('placeholder_key_materials', currentLang));
  wireInput(nameInp, refreshPreview);
  wireInput(levelInp, refreshPreview);
  wireInput(matsInp, refreshPreview);
  rowContent.append(
    wrapField(t('key_name_label', currentLang), nameInp, 'key_name_label'),
    wrapField(t('req_level_label', currentLang), levelInp, 'req_level_label'),
    wrapField(currentLang === 'vi' ? 'Nguyên Liệu' : 'Materials', matsInp)
  );

  const effectField = el('div', { cls: 'field full' });
  effectField.append(el('label', { 'data-i18n': 'effect_label' }, t('effect_label', currentLang)));
  const effectTA = el('textarea', { rows: 2, placeholder: t('placeholder_key_effect', currentLang) });
  if (data.effect) effectTA.value = data.effect;
  effectTA.addEventListener('input', refreshPreview);
  effectField.append(effectTA);

  row.append(header, rowContent, effectField);
  $('keys-list').append(row);
  refreshPreview();
}

// ── Gather character data ──────────────────────────────────────────────
function gatherCharacter() {
  const stats = {
    hp: numVal('c-hp'),
    atk: numVal('c-atk'),
    def: numVal('c-def'),
  };
  const images = {
    portrait: $('c-img-portrait').value,
    class_icon: $('c-img-classicon').value,
  };
  const effects_glossary = [...document.querySelectorAll('#glossary-list .repeat-item input')]
    .map(i => i.value.trim()).filter(Boolean);

  const skills = [...document.querySelectorAll('#skills-list .skill-card')].map(card => {
    const inputs = [...card.querySelectorAll('input[type="text"]')];
    const numInputs = [...card.querySelectorAll('input[type="number"]')];
    const sel = card.querySelector('select');
    const tags = [...card.querySelectorAll('.tag-pill.selected')].map(p => p.textContent.trim());
    const textareas = [...card.querySelectorAll('textarea')];
    return {
      name: inputs[0]?.value?.trim() || '',
      tags,
      ammo_type: sel?.value || null,
      stability_damage: numInputs[0] ? (numInputs[0].value !== '' ? +numInputs[0].value : null) : null,
      cooldown: inputs[1]?.value?.trim() || null,
      confectance_cost: numInputs[1] ? (numInputs[1].value !== '' ? +numInputs[1].value : null) : null,
      range: numInputs[2] ? (numInputs[2].value !== '' ? +numInputs[2].value : null) : null,
      effect_area: inputs[2]?.value?.trim() || null,
      description: textareas[0]?.value?.trim() || '',
    };
  });

  const summons = [...document.querySelectorAll('#summons-list .skill-card')].map(card => {
    const name = card.querySelector('.s-name-inp')?.value?.trim() || '';
    const hpStr = card.querySelector('.s-hp-inp')?.value;
    const atkStr = card.querySelector('.s-atk-inp')?.value;
    const defStr = card.querySelector('.s-def-inp')?.value;
    const hp = hpStr !== '' && hpStr != null ? +hpStr : null;
    const atk = atkStr !== '' && atkStr != null ? +atkStr : null;
    const def = defStr !== '' && defStr != null ? +defStr : null;
    const stats = (hp != null || atk != null || def != null) ? { hp, atk, def } : null;

    const stability_gauge = card.querySelector('.s-stab-inp')?.value?.trim() || null;
    const movement_speed = card.querySelector('.s-move-inp')?.value?.trim() || null;

    const skills = [...card.querySelectorAll('.repeat-list .repeat-item')].map(row => {
      const sName = row.querySelector('.s-skill-name-inp')?.value?.trim() || '';
      const sDesc = row.querySelector('textarea')?.value?.trim() || '';
      return { name: sName, description: sDesc };
    });

    return { name, stats, stability_gauge, movement_speed, skills };
  });

  const fortification = [...document.querySelectorAll('#fort-list .repeat-item')].map((row, idx) => {
    const hiddenNum = row.querySelector('input[type="number"][style]');
    const tier = hiddenNum ? +hiddenNum.value : idx + 1;
    const sel = row.querySelector('select');
    const numInps = [...row.querySelectorAll('input[type="number"]:not([style])')];
    const ta = row.querySelector('textarea');
    return {
      tier,
      skill: sel?.value?.trim() || '',
      level: numInps[0] ? (numInps[0].value !== '' ? +numInps[0].value : null) : null,
      effect: ta?.value?.trim() || '',
    };
  });

  const neural_helix = [...document.querySelectorAll('#nh-list .repeat-item')].map(row => {
    const inps = [...row.querySelectorAll('input[type="text"]')];
    const numInp = row.querySelector('input[type="number"]');
    const ta = row.querySelector('textarea');
    return {
      node: inps[0]?.value?.trim() || '',
      level: numInp ? (numInp.value !== '' ? +numInp.value : null) : null,
      effect: ta?.value?.trim() || '',
      materials: inps[1]?.value?.trim() || '',
    };
  });

  const keys = [...document.querySelectorAll('#keys-list .repeat-item')].map(row => {
    const inps = [...row.querySelectorAll('input[type="text"]')];
    const ta = row.querySelector('textarea');
    return {
      name: inps[0]?.value?.trim() || '',
      level: inps[1]?.value?.trim() || '',
      materials: inps[2]?.value?.trim() || '',
      effect: ta?.value?.trim() || '',
    };
  });

  return {
    slug: $('c-slug').value.trim(),
    name: $('c-name').value.trim(),
    class: $('c-class').value,
    rarity: $('c-rarity').value,
    phase: $('c-phase').value,
    weapon_type: $('c-weapon-type').value,
    ammo_type: $('c-ammo-type').value,
    signature_weapon: $('c-sig-weapon').value.trim() || null,
    stats: (stats.hp || stats.atk || stats.def) ? stats : null,
    skill_attribute: $('c-skill-attr').value.trim() || null,
    weakness: $('c-weakness').value.trim() || null,
    stability_gauge: $('c-stab-gauge').value.trim() || null,
    movement_speed: $('c-move-speed').value.trim() || null,
    effects_glossary: effects_glossary.length ? effects_glossary : [],
    skills,
    summons: summons.length ? summons : undefined,
    fortification,
    neural_helix,
    keys,
    images,
    source_notes: $('c-source-notes').value.trim() || null,
  };
}

function gatherCharacterVi(slug = $('c-slug').value.trim()) {
  const skills = [...document.querySelectorAll('#skills-list .skill-card')].map(card => {
    const inputs = [...card.querySelectorAll('input[type="text"]')];
    const tags = [...card.querySelectorAll('.tag-pill.selected')].map(p => p.textContent.trim());
    const textareas = [...card.querySelectorAll('textarea')];
    const skillObj = {
      name: inputs[0]?.value?.trim() || '',
      description: textareas[0]?.value?.trim() || '',
      tags
    };
    const enName = inputs[0]?.dataset.enName;
    if (enName) skillObj.en_name = enName;
    return skillObj;
  });

  const fortification = [...document.querySelectorAll('#fort-list .repeat-item')].map((row, idx) => {
    const hiddenNum = row.querySelector('input[type="number"][style]');
    const tier = hiddenNum ? +hiddenNum.value : idx + 1;
    const sel = row.querySelector('select');
    const numInps = [...row.querySelectorAll('input[type="number"]:not([style])')];
    const ta = row.querySelector('textarea');
    return {
      tier,
      level: numInps[0] ? (numInps[0].value !== '' ? +numInps[0].value : 2) : 2,
      skill: sel?.value?.trim() || '',
      effect: ta?.value?.trim() || ''
    };
  });

  const neural_helix = [...document.querySelectorAll('#nh-list .repeat-item')].map(row => {
    const inps = [...row.querySelectorAll('input[type="text"]')];
    const numInp = row.querySelector('input[type="number"]');
    const ta = row.querySelector('textarea');
    return {
      node: inps[0]?.value?.trim() || '',
      level: numInp ? (numInp.value !== '' ? +numInp.value : null) : null,
      effect: ta?.value?.trim() || '',
      materials: inps[1]?.value?.trim() || ''
    };
  });

  const keys = [...document.querySelectorAll('#keys-list .repeat-item')].map(row => {
    const inps = [...row.querySelectorAll('input[type="text"]')];
    const ta = row.querySelector('textarea');
    return {
      name: inps[0]?.value?.trim() || '',
      level: inps[1]?.value?.trim() || '',
      effect: ta?.value?.trim() || '',
      materials: inps[2]?.value?.trim() || ''
    };
  });

  const summons = [...document.querySelectorAll('#summons-list .skill-card')].map(card => {
    const name = card.querySelector('.s-name-inp')?.value?.trim() || '';
    const hpStr = card.querySelector('.s-hp-inp')?.value;
    const atkStr = card.querySelector('.s-atk-inp')?.value;
    const defStr = card.querySelector('.s-def-inp')?.value;
    const hp = hpStr !== '' && hpStr != null ? +hpStr : null;
    const atk = atkStr !== '' && atkStr != null ? +atkStr : null;
    const def = defStr !== '' && defStr != null ? +defStr : null;
    const stats = (hp != null || atk != null || def != null) ? { hp, atk, def } : null;
    const stability_gauge = card.querySelector('.s-stab-inp')?.value?.trim() || null;
    const movement_speed = card.querySelector('.s-move-inp')?.value?.trim() || null;

    const sSkills = [...card.querySelectorAll('.repeat-list .repeat-item')].map(row => {
      const sName = row.querySelector('.s-skill-name-inp')?.value?.trim() || '';
      const sDesc = row.querySelector('textarea')?.value?.trim() || '';
      return { name: sName, description: sDesc };
    });

    return { name, stats, stability_gauge, movement_speed, skills: sSkills };
  });

  return {
    name: $('c-name').value.trim(),
    en_name: $('c-name').dataset.enName || $('c-name').value.trim(),
    class: $('c-class').value,
    phase: $('c-phase').value,
    rarity: $('c-rarity').value,
    weapon_type: $('c-weapon-type').value,
    ammo_type: $('c-ammo-type').value || null,
    signature_weapon: $('c-sig-weapon').value.trim() || null,
    weakness: $('c-weakness').value.trim() || null,
    skills,
    fortification,
    neural_helix,
    keys,
    summons: summons.length ? summons : [],
    server: $('c-source-notes').value.trim() || 'global'
  };
}

// ── Download / Load / Clear / Save to Disk ──────────────────────────────
function downloadCharacter() {
  const slug = $('c-slug').value.trim();
  const name = $('c-name').value.trim();
  if (!slug) { showToast(t('toast_slug_req', currentLang), 'err'); return; }
  if (!name) { showToast(t('toast_name_req', currentLang), 'err'); return; }

  if (currentLang === 'vi') {
    const data = gatherCharacterVi(slug);
    const json = JSON.stringify(compact(data), null, 2);
    downloadFile(`${slug}_vi.json`, json);
    showToast(`${t('toast_downloaded', 'vi')} ${slug}_vi.json`, 'ok');
  } else {
    const data = gatherCharacter();
    const json = orderedStringify(compact(data), CHAR_KEY_ORDER);
    downloadFile(`${slug}.json`, json);
    showToast(`${t('toast_downloaded', 'en')} ${slug}.json`, 'ok');
  }
}

async function saveToFileSystem() {
  const slug = $('c-slug').value.trim();
  const name = $('c-name').value.trim();
  if (!slug) { showToast(t('toast_slug_req', currentLang), 'err'); return; }
  if (!name) { showToast(t('toast_name_req', currentLang), 'err'); return; }
  if (!loadedCharacterSlug) {
    showToast(currentLang === 'vi' ? 'Hãy tải một nhân vật có sẵn trước khi cập nhật.' : 'Load an existing character before updating.', 'err', 4500);
    return;
  }
  if (slug !== loadedCharacterSlug) {
    showToast(currentLang === 'vi' ? 'Không thể đổi slug khi cập nhật file gốc.' : 'The slug cannot change while updating the source file.', 'err', 4500);
    return;
  }

  const data = compact(currentLang === 'vi' ? gatherCharacterVi(slug) : gatherCharacter());
  try {
    const response = await fetch(`/api/characters/${encodeURIComponent(loadedCharacterSlug)}?lang=${currentLang}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    const result = await response.json().catch(() => ({}));
    if (!response.ok) throw new Error(result.error || `HTTP ${response.status}`);
    if (currentLang === 'vi' && VI_DATA?.characters) {
      VI_DATA.characters[loadedCharacterSlug] = {
        ...(VI_DATA.characters[loadedCharacterSlug] || {}),
        ...data,
      };
    }
    showToast(`${t('toast_saved', currentLang)} ${result.path}`, 'ok', 4000);
  } catch (e) {
    showToast(`${currentLang === 'vi' ? 'Cập nhật thất bại' : 'Update failed'}: ${e.message}. ${currentLang === 'vi' ? 'Hãy chạy tools/data_entry_server.py.' : 'Run tools/data_entry_server.py.'}`, 'err', 6500);
  }
}

async function downloadFullI18nVi() {
  await ensureViDataLoaded();
  if (!VI_DATA) {
    showToast('i18n_vi.json could not be loaded', 'err');
    return;
  }
  const slug = $('c-slug').value.trim();
  if (slug) {
    const viChar = gatherCharacterVi(slug);
    if (!VI_DATA.characters) VI_DATA.characters = {};
    VI_DATA.characters[slug] = viChar;
  }
  const json = JSON.stringify(VI_DATA, null, 2);
  downloadFile('i18n_vi.json', json);
  showToast(currentLang === 'vi' ? 'Đã tải về tệp i18n_vi.json hoàn chỉnh' : 'Downloaded complete i18n_vi.json', 'ok');
}

// ── Load existing characters from search-index ─────────────────────────
async function loadExistingCharacters() {
  const sel = $('char-selector');
  if (!sel) return;
  try {
    const res = await fetch('../../dist/search-index.json');
    if (!res.ok) throw new Error('search-index not found — run build.py first');
    const index = await res.json();
    CHARACTERS_INDEX = index.filter(e => e.category === 'doll').sort((a, b) => a.name.localeCompare(b.name));
    renderCharSelectorOptions();
    ensureViDataLoaded().then(() => {
      if (currentLang === 'vi') renderCharSelectorOptions();
    });
  } catch (e) {
    console.warn('Could not load character list:', e.message);
    const opt = el('option', { value: '', style: 'color:#f87171' }, '⚠ Build site first to load character list');
    sel.append(opt);
  }
}

function renderCharSelectorOptions() {
  const sel = $('char-selector');
  if (!sel || !CHARACTERS_INDEX.length) return;
  const currentVal = sel.value;
  sel.innerHTML = '';
  sel.append(el('option', { value: '' }, t('select_char_placeholder', currentLang)));

  CHARACTERS_INDEX.forEach(c => {
    let displayName = c.name;
    let displayClass = c.class || '';
    let displayRarity = c.rarity || '';
    if (currentLang === 'vi') {
      const viChar = VI_DATA?.characters?.[c.slug];
      if (viChar?.name) displayName = viChar.name;
      displayClass = mapTerm(displayClass, 'classes', 'vi');
      displayRarity = mapTerm(displayRarity, 'rarities', 'vi');
    }
    const label = `${displayName} (${displayRarity} ${displayClass})`.trim();
    const opt = el('option', { value: c.slug }, label);
    if (c.slug === currentVal) opt.selected = true;
    sel.append(opt);
  });
}

async function loadCharacterBySlug(slug) {
  try {
    if (currentLang === 'vi') {
      await ensureViDataLoaded();
      const viChar = VI_DATA?.characters?.[slug];
      let enData = null;
      try {
        const enRes = await fetch(`../../data/characters/${slug}.json`);
        if (enRes.ok) enData = await enRes.json();
      } catch {}

      if (viChar) {
        populateCharacterFormVi(slug, viChar, enData);
        loadedCharacterSlug = slug;
        showToast(`${t('toast_loaded', 'vi')}: ${viChar.name || slug}`, 'ok');
        return;
      }
      if (enData) {
        populateCharacterForm(enData);
        loadedCharacterSlug = slug;
        showToast(`Chưa có bản dịch tiếng Việt cho ${enData.name || slug}, đã tải dữ liệu gốc để dịch.`, 'ok');
        return;
      }
    }

    const res = await fetch(`../../data/characters/${slug}.json`);
    if (!res.ok) throw new Error(`${slug}.json not found`);
    const data = await res.json();
    populateCharacterForm(data);
    loadedCharacterSlug = slug;
    showToast(`${t('toast_loaded', currentLang)}: ${data.name}`, 'ok');
  } catch (e) {
    showToast(`Could not load ${slug}: ${e.message}`, 'err');
  }
}

// ── Image Upload Slots ─────────────────────────────────────────────────
const IMG_SLOT_TYPES = [
  { key: 'portrait', label: 'Portrait', path: slug => `assets/images/characters/${slug}/portrait.png` },
  { key: 'portrait_webp', label: 'Portrait (WebP)', path: slug => `assets/images/characters/${slug}/portrait.webp` },
  { key: 'avatar', label: 'Avatar', path: slug => `assets/images/characters/${slug}/avatar.png` },
  { key: 'skill1_icon', label: 'Skill 1 Icon', path: slug => `assets/images/characters/${slug}/skill1-icon.png` },
  { key: 'skill1_range', label: 'Skill 1 Range', path: slug => `assets/images/characters/${slug}/skill1-range.png` },
  { key: 'skill2_icon', label: 'Skill 2 Icon', path: slug => `assets/images/characters/${slug}/skill2-icon.png` },
  { key: 'skill2_range', label: 'Skill 2 Range', path: slug => `assets/images/characters/${slug}/skill2-range.png` },
  { key: 'skill3_icon', label: 'Skill 3 Icon', path: slug => `assets/images/characters/${slug}/skill3-icon.png` },
  { key: 'skill3_range', label: 'Skill 3 Range', path: slug => `assets/images/characters/${slug}/skill3-range.png` },
  { key: 'custom', label: 'Custom', path: slug => `assets/images/characters/${slug}/` },
];

let imgSlotCounter = 0;

function initImageUpload() {
  const btn = $('btn-add-img-slot');
  if (btn) btn.addEventListener('click', addImageSlot);
  // Add a default portrait slot
  addImageSlot();
}

function addImageSlot(typeKey = 'portrait') {
  imgSlotCounter++;
  const id = `img-slot-${imgSlotCounter}`;
  const slot = el('div', { cls: 'img-upload-slot', id });

  // Type selector
  const typeSel = el('select', { cls: 'img-type-sel' });
  IMG_SLOT_TYPES.forEach(t => {
    const opt = el('option', { value: t.key }, t.label);
    if (t.key === typeKey) opt.selected = true;
    typeSel.append(opt);
  });

  // Path display
  const pathDisp = el('input', { type: 'text', cls: 'img-path-disp', readonly: true, placeholder: 'Path will appear here' });

  // File input (hidden)
  const fileInp = el('input', { type: 'file', accept: 'image/*', style: 'display:none', id: `${id}-file` });

  // Preview
  const preview = el('img', { cls: 'img-preview', alt: 'preview', style: 'display:none' });

  // Buttons
  const pickBtn = el('button', { cls: 'btn btn-secondary', type: 'button', style: 'font-size:0.75rem;padding:4px 10px' }, '📁 Choose File');
  const saveBtn = el('button', { cls: 'btn btn-primary', type: 'button', style: 'font-size:0.75rem;padding:4px 10px', disabled: true }, '💾 Save');
  const removeBtn = el('button', { cls: 'btn-remove', type: 'button' }, '✕');

  let selectedFile = null;

  function updatePath() {
    const slug = $('c-slug').value || '<slug>';
    const typeKey = typeSel.value;
    const typeDef = IMG_SLOT_TYPES.find(t => t.key === typeKey);
    pathDisp.value = typeDef ? typeDef.path(slug) : '';
  }
  updatePath();

  typeSel.addEventListener('change', updatePath);
  $('c-slug').addEventListener('input', updatePath);

  pickBtn.addEventListener('click', () => fileInp.click());

  fileInp.addEventListener('change', e => {
    const file = e.target.files[0];
    if (!file) return;
    selectedFile = file;
    const url = URL.createObjectURL(file);
    preview.src = url;
    preview.style.display = 'block';
    saveBtn.disabled = false;
    updatePath();
    // Auto-suggest file name in path
    if (typeSel.value === 'custom') {
      const slug = $('c-slug').value || '<slug>';
      pathDisp.value = `assets/images/characters/${slug}/${file.name}`;
    }
  });

  saveBtn.addEventListener('click', async () => {
    if (!selectedFile) return;
    const suggestedPath = pathDisp.value;
    const suggestedName = suggestedPath.split('/').pop();
    if ('showSaveFilePicker' in window) {
      try {
        const ext = suggestedName.split('.').pop().toLowerCase();
        const mimeMap = { png: 'image/png', webp: 'image/webp', jpg: 'image/jpeg', jpeg: 'image/jpeg', gif: 'image/gif' };
        const mime = mimeMap[ext] || 'image/*';
        const handle = await window.showSaveFilePicker({
          suggestedName,
          types: [{ description: 'Image file', accept: { [mime]: [`.${ext}`] } }],
          startIn: 'pictures',
        });
        const writable = await handle.createWritable();
        await writable.write(selectedFile);
        await writable.close();
        showToast(`Saved ${suggestedName}`, 'ok');
      } catch (e) {
        if (e.name !== 'AbortError') showToast(`Save failed: ${e.message}`, 'err');
      }
    } else {
      const a = document.createElement('a');
      a.href = URL.createObjectURL(selectedFile);
      a.download = suggestedName;
      a.click();
      showToast(`Downloaded ${suggestedName} (copy to ${pathDisp.value})`, 'ok', 4000);
    }
  });

  removeBtn.addEventListener('click', () => slot.remove());

  const row1 = el('div', { cls: 'img-slot-row' });
  row1.append(typeSel, pathDisp, pickBtn, saveBtn, removeBtn);
  slot.append(row1, fileInp, preview);
  $('img-upload-slots').append(slot);
}



function loadCharacter(e) {
  const file = e.target.files[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    try {
      const data = JSON.parse(ev.target.result);
      populateCharacterForm(data);
      loadedCharacterSlug = data.slug || null;
      showToast(`Loaded: ${data.name || file.name}`, 'ok');
    } catch {
      showToast('Invalid JSON file', 'err');
    }
    e.target.value = '';
  };
  reader.readAsText(file);
}

function clearCharacterForm() {
  if (!confirm('Clear all character data? This cannot be undone.')) return;
  resetCharacterForm();
  loadedCharacterSlug = null;
  showToast('Form cleared', 'ok');
}

function resetCharacterForm() {
  ['c-name', 'c-slug', 'c-sig-weapon', 'c-skill-attr', 'c-weakness',
    'c-stab-gauge', 'c-move-speed', 'c-source-notes'].forEach(id => { $(id).value = ''; });
  ['c-class', 'c-rarity', 'c-phase', 'c-weapon-type', 'c-ammo-type'].forEach(id => { $(id).value = ''; });
  ['c-hp', 'c-atk', 'c-def'].forEach(id => { $(id).value = ''; });
  $('glossary-list').innerHTML = '';
  $('skills-list').innerHTML = '';
  $('summons-list').innerHTML = '';
  $('fort-list').innerHTML = '';
  $('nh-list').innerHTML = '';
  $('keys-list').innerHTML = '';
  skillCounter = summonCounter = glossaryCounter = fortCounter = nhCounter = keyCounter = 0;
  for (let i = 1; i <= 6; i++) addFortRow(i);
  for (let i = 1; i <= 6; i++) addNHRow(i);
  const keyList = window.TERMS ? window.TERMS.keys : [];
  keyList.forEach((k, idx) => {
    const keyName = currentLang === 'vi' ? k.vi : k.en;
    const levelDef = idx < 6 ? '' : idx === 6 ? (currentLang === 'vi' ? 'Thân Thiết Lv 5' : 'Affinity Lvl 5') : '';
    addKeyRow(keyName, levelDef);
  });
  refreshImagePaths('');
  refreshPreview();
}

function populateCharacterForm(d) {
  resetCharacterForm();
  if (d.name) {
    $('c-name').value = d.name;
    $('c-name').dataset.enName = d.name;
  }
  if (d.slug) $('c-slug').value = d.slug;
  if (d.class) $('c-class').value = mapTerm(d.class, 'classes', currentLang);
  if (d.rarity) $('c-rarity').value = mapTerm(d.rarity, 'rarities', currentLang);
  if (d.phase) $('c-phase').value = mapTerm(d.phase, 'phases', currentLang);
  if (d.weapon_type) $('c-weapon-type').value = mapTerm(d.weapon_type, 'weapon_types', currentLang);
  if (d.ammo_type) $('c-ammo-type').value = mapTerm(d.ammo_type, 'ammo_types', currentLang);
  if (d.signature_weapon) $('c-sig-weapon').value = d.signature_weapon;
  if (d.stats) {
    if (d.stats.hp != null) $('c-hp').value = d.stats.hp;
    if (d.stats.atk != null) $('c-atk').value = d.stats.atk;
    if (d.stats.def != null) $('c-def').value = d.stats.def;
  }
  if (d.skill_attribute) $('c-skill-attr').value = mapTerm(d.skill_attribute, 'phases', currentLang);
  if (d.weakness) $('c-weakness').value = mapTerm(d.weakness, 'phases', currentLang);
  if (d.stability_gauge) $('c-stab-gauge').value = d.stability_gauge;
  if (d.movement_speed) $('c-move-speed').value = d.movement_speed;
  if (d.source_notes) $('c-source-notes').value = d.source_notes;
  (d.effects_glossary || []).forEach(t => addGlossaryRow(t));

  // Skills
  (d.skills || []).forEach(s => addSkillCard(s));

  // Summons
  (d.summons || []).forEach(s => addSummonCard(s));

  // Fortification — replace the 6 pre-populated rows
  $('fort-list').innerHTML = '';
  fortCounter = 0;
  if (d.fortification?.length) {
    d.fortification.forEach(f => addFortRow(f.tier, f));
  } else {
    for (let i = 1; i <= 6; i++) addFortRow(i);
  }

  // Neural Helix
  $('nh-list').innerHTML = '';
  nhCounter = 0;
  if (d.neural_helix?.length) {
    d.neural_helix.forEach((n, i) => addNHRow(i + 1, n));
  } else {
    for (let i = 1; i <= 6; i++) addNHRow(i);
  }

  // Keys
  $('keys-list').innerHTML = '';
  keyCounter = 0;
  if (d.keys?.length) {
    d.keys.forEach(k => addKeyRow(k.name, '', k));
  } else {
    const keyList = window.TERMS ? window.TERMS.keys : [];
    keyList.forEach((k, idx) => {
      const keyName = currentLang === 'vi' ? k.vi : k.en;
      const levelDef = idx < 6 ? '' : idx === 6 ? (currentLang === 'vi' ? 'Thân Thiết Lv 5' : 'Affinity Lvl 5') : '';
      addKeyRow(keyName, levelDef);
    });
  }

  refreshImagePaths(d.slug || '');
  refreshFortSkillDropdowns();
  refreshPreview();
}

function populateCharacterFormVi(slug, viChar, enData = null) {
  resetCharacterForm();
  if (viChar.name) {
    $('c-name').value = viChar.name;
    $('c-name').dataset.enName = viChar.en_name || enData?.name || viChar.name;
  }
  if (slug) $('c-slug').value = slug;
  if (viChar.class) $('c-class').value = mapTerm(viChar.class, 'classes', currentLang);
  if (viChar.rarity) $('c-rarity').value = mapTerm(viChar.rarity, 'rarities', currentLang);
  if (viChar.phase) $('c-phase').value = mapTerm(viChar.phase, 'phases', currentLang);
  if (viChar.weapon_type) $('c-weapon-type').value = mapTerm(viChar.weapon_type, 'weapon_types', currentLang);
  if (viChar.ammo_type) $('c-ammo-type').value = mapTerm(viChar.ammo_type, 'ammo_types', currentLang);
  if (viChar.signature_weapon) $('c-sig-weapon').value = viChar.signature_weapon;
  if (viChar.weakness) $('c-weakness').value = mapTerm(viChar.weakness, 'phases', currentLang);
  if (viChar.server) $('c-source-notes').value = viChar.server;

  // Stats from enData
  if (enData?.stats) {
    if (enData.stats.hp != null) $('c-hp').value = enData.stats.hp;
    if (enData.stats.atk != null) $('c-atk').value = enData.stats.atk;
    if (enData.stats.def != null) $('c-def').value = enData.stats.def;
  }
  if (enData?.stability_gauge) $('c-stab-gauge').value = enData.stability_gauge;
  if (enData?.movement_speed) $('c-move-speed').value = enData.movement_speed;
  if (enData?.skill_attribute) $('c-skill-attr').value = mapTerm(enData.skill_attribute, 'phases', currentLang);

  // Skills
  if (viChar.skills?.length) {
    $('skills-list').innerHTML = '';
    skillCounter = 0;
    viChar.skills.forEach((s, idx) => {
      const enSkill = enData?.skills?.[idx];
      addSkillCard({
        name: s.name,
        en_name: s.en_name || enSkill?.name || '',
        tags: s.tags,
        description: s.description,
        ammo_type: enSkill?.ammo_type || s.ammo_type,
        stability_damage: enSkill?.stability_damage != null ? enSkill.stability_damage : s.stability_damage,
        cooldown: enSkill?.cooldown || s.cooldown,
        confectance_cost: enSkill?.confectance_cost != null ? enSkill.confectance_cost : s.confectance_cost,
        range: enSkill?.range != null ? enSkill.range : s.range,
        effect_area: enSkill?.effect_area || s.effect_area
      });
    });
  }

  // Fortifications
  if (viChar.fortification?.length) {
    $('fort-list').innerHTML = '';
    fortCounter = 0;
    viChar.fortification.forEach(f => {
      addFortRow(f.tier || f.level, f);
    });
  }

  // Neural Helix
  if (viChar.neural_helix?.length) {
    $('nh-list').innerHTML = '';
    nhCounter = 0;
    viChar.neural_helix.forEach((n, i) => {
      addNHRow(i + 1, n);
    });
  }

  // Keys
  if (viChar.keys?.length) {
    $('keys-list').innerHTML = '';
    keyCounter = 0;
    viChar.keys.forEach(k => {
      addKeyRow(k.name, '', k);
    });
  }

  // Summons
  if (viChar.summons?.length) {
    $('summons-list').innerHTML = '';
    summonCounter = 0;
    viChar.summons.forEach(s => {
      addSummonCard(s);
    });
  }

  refreshImagePaths(slug || '');
  refreshFortSkillDropdowns();
  refreshPreview();
}

function refreshImagePaths(slug) {
  const base = slug ? `assets/images/characters/${slug}/` : 'assets/images/characters/<slug>/';
  const clsVal = $('c-class').value;
  const clsEn = mapTerm(clsVal, 'classes', 'en');
  const classFile = clsEn ? `${clsEn.toLowerCase()}.png` : '<class>.png';
  $('c-img-portrait').value = `${base}portrait.png`;
  $('c-img-classicon').value = `assets/images/class/${classFile}`;
}

// ─────────────────────────────────────────────────────────────────────────
//  ████  WEAPON TAB  ████
// ─────────────────────────────────────────────────────────────────────────
function initWeaponTab() {
  $('w-name').addEventListener('input', () => {
    $('w-slug').value = slugify($('w-name').value);
    refreshWeaponImagePath();
    refreshPreview();
  });
  $('w-slug').addEventListener('input', () => { refreshWeaponImagePath(); refreshPreview(); });
  document.querySelectorAll('#tab-weapon input, #tab-weapon select, #tab-weapon textarea')
    .forEach(e => e.addEventListener('input', refreshPreview));
  $('btn-download-weapon').addEventListener('click', downloadWeapon);
  $('btn-load-weapon').addEventListener('click', () => $('file-load-weapon').click());
  $('file-load-weapon').addEventListener('change', loadWeapon);
  $('btn-clear-weapon').addEventListener('click', clearWeaponForm);
}

function refreshWeaponImagePath() {
  const slug = $('w-slug').value || '<slug>';
  $('w-img-path').value = `assets/images/weapons/${slug}.png`;
}

function gatherWeapon() {
  return {
    slug: $('w-slug').value.trim(),
    name: $('w-name').value.trim(),
    weapon_type: $('w-weapon-type').value,
    rarity: $('w-rarity').value,
    images: { weapon: $('w-img-path').value },
  };
}
function downloadWeapon() {
  const data = gatherWeapon();
  if (!data.slug) { showToast('Slug required', 'err'); return; }
  downloadFile(`weapon-${data.slug}.json`, orderedStringify(compact(data)));
  showToast(`Downloaded weapon-${data.slug}.json`, 'ok');
}
function loadWeapon(e) {
  const file = e.target.files[0]; if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    try {
      const d = JSON.parse(ev.target.result);
      if (d.slug) $('w-slug').value = d.slug;
      if (d.name) $('w-name').value = d.name;
      if (d.weapon_type) $('w-weapon-type').value = d.weapon_type;
      if (d.rarity) $('w-rarity').value = d.rarity;
      refreshWeaponImagePath();
      refreshPreview();
      showToast(`Loaded ${file.name}`, 'ok');
    } catch { showToast('Invalid JSON', 'err'); }
    e.target.value = '';
  };
  reader.readAsText(file);
}
function clearWeaponForm() {
  ['w-name', 'w-slug'].forEach(id => $(id).value = '');
  ['w-weapon-type', 'w-rarity'].forEach(id => $(id).value = '');
  refreshWeaponImagePath(); refreshPreview();
}

// ─────────────────────────────────────────────────────────────────────────
//  ████  FAQ TAB  ████
// ─────────────────────────────────────────────────────────────────────────
let faqCounter = 0;
function initFaqTab() {
  $('btn-add-faq').addEventListener('click', () => addFaqRow());
  $('btn-download-faq').addEventListener('click', downloadFaq);
  $('btn-load-faq').addEventListener('click', () => $('file-load-faq').click());
  $('file-load-faq').addEventListener('change', loadFaq);
  $('btn-clear-faq').addEventListener('click', clearFaqForm);
  addFaqRow();
}
function addFaqRow(data = {}) {
  faqCounter++;
  const id = `faq-${faqCounter}`;
  const row = el('div', { cls: 'repeat-item', id });
  const header = el('div', { cls: 'item-header' });
  header.append(el('span', { cls: 'item-index' }, `Q&A ${faqCounter}`), makeBtnRemove(id, 'faq-list', refreshPreview));
  const qInp = el('input', { type: 'text', placeholder: 'Question…' });
  if (data.question) qInp.value = data.question;
  qInp.addEventListener('input', refreshPreview);
  const aTA = el('textarea', { rows: 3, placeholder: 'Answer…' });
  if (data.answer) aTA.value = data.answer;
  aTA.addEventListener('input', refreshPreview);
  row.append(header, wrapField('Question', qInp), wrapField('Answer', aTA));
  $('faq-list').append(row);
  refreshPreview();
}
function gatherFaq() {
  return [...document.querySelectorAll('#faq-list .repeat-item')].map(row => ({
    question: row.querySelector('input')?.value?.trim() || '',
    answer: row.querySelector('textarea')?.value?.trim() || '',
  })).filter(r => r.question);
}
function downloadFaq() {
  const data = gatherFaq();
  downloadFile('faq.json', JSON.stringify(data, null, 2));
  showToast('Downloaded faq.json', 'ok');
}
function loadFaq(e) {
  const file = e.target.files[0]; if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    try {
      const arr = JSON.parse(ev.target.result);
      $('faq-list').innerHTML = ''; faqCounter = 0;
      arr.forEach(item => addFaqRow(item));
      showToast(`Loaded ${arr.length} Q&A`, 'ok');
    } catch { showToast('Invalid JSON', 'err'); }
    e.target.value = '';
  };
  reader.readAsText(file);
}
function clearFaqForm() {
  $('faq-list').innerHTML = ''; faqCounter = 0; addFaqRow(); refreshPreview();
}

// ─────────────────────────────────────────────────────────────────────────
//  Helpers
// ─────────────────────────────────────────────────────────────────────────
function makeBtnRemove(itemId, listId, onRemove) {
  return el('button', {
    cls: 'btn-remove',
    onclick: () => { $(itemId)?.remove(); onRemove?.(); }
  }, '✕ Remove');
}

function wrapField(label, inputEl, i18nKey = null) {
  const f = el('div', { cls: 'field' });
  const lbl = el('label', {}, label);
  if (i18nKey) lbl.setAttribute('data-i18n', i18nKey);
  f.append(lbl, inputEl);
  return f;
}
function textInput(value = '', placeholder = '') {
  const i = el('input', { type: 'text', placeholder });
  if (value) i.value = value;
  return i;
}
function numInput(value = null, placeholder = '') {
  const i = el('input', { type: 'number', placeholder });
  if (value != null && value !== '') i.value = value;
  return i;
}
function numVal(id) {
  const v = $(id)?.value;
  return v !== '' && v != null ? +v : null;
}
function wireInput(inp, fn) { inp.addEventListener('input', fn); }
function wireInputs(container, fn) {
  container.querySelectorAll('input, select, textarea').forEach(e => e.addEventListener('input', fn));
}

// ─────────────────────────────────────────────────────────────────────────
//  EFFECTS INSERTER
// ─────────────────────────────────────────────────────────────────────────
/**
 * Creates a small inline row: [ search input ] [ dropdown ] [ Insert → ]
 * getTA: a function that returns the target textarea element at call-time.
 */
function makeEffectInserter(getTA) {
  const wrapper = el('div', { cls: 'effect-inserter' });

  // Search/filter input
  const searchInp = el('input', {
    type: 'text',
    placeholder: 'Filter effects…',
    cls: 'effect-search',
  });

  // Select dropdown
  const sel = el('select', { cls: 'effect-select' });
  sel.append(el('option', { value: '' }, '— Insert effect name —'));

  function rebuildOptions(filter = '') {
    // keep placeholder
    while (sel.options.length > 1) sel.remove(1);
    const lower = filter.toLowerCase();
    Object.keys(EFFECTS_DATA)
      .filter(name => !lower || name.toLowerCase().includes(lower))
      .sort()
      .forEach(name => {
        const opt = el('option', { value: name, title: EFFECTS_DATA[name] }, name);
        sel.append(opt);
      });
  }
  rebuildOptions();

  searchInp.addEventListener('input', () => rebuildOptions(searchInp.value));

  // Insert button
  const btn = el('button', { cls: 'btn-insert-effect', type: 'button' }, 'Insert →');
  btn.addEventListener('click', () => {
    const effectName = sel.value;
    if (!effectName) return;
    const ta = getTA();
    if (!ta) return;
    // Insert at cursor, or append
    const start = ta.selectionStart ?? ta.value.length;
    const end = ta.selectionEnd ?? ta.value.length;
    const before = ta.value.slice(0, start);
    const after = ta.value.slice(end);
    // Add a space before if needed
    const spaceBefore = before.length && !before.endsWith(' ') && !before.endsWith('\n') ? ' ' : '';
    const spaceAfter = after.length && !after.startsWith(' ') && !after.startsWith('\n') ? ' ' : '';
    const insertText = `[[${effectName}]]`;
    ta.value = before + spaceBefore + insertText + spaceAfter + after;
    // Move cursor after inserted text
    const newPos = start + spaceBefore.length + insertText.length;
    ta.setSelectionRange(newPos, newPos);
    ta.focus();
    ta.dispatchEvent(new Event('input'));
    // Reset select (keep search term so user can insert multiple quickly)
    sel.value = '';
  });

  wrapper.append(searchInp, sel, btn);
  return wrapper;
}

// ── Language Toggle & UI Translation ─────────────────────────────────────
async function ensureViDataLoaded() {
  if (VI_DATA) return VI_DATA;
  if (window.GFL2_I18N_VI) {
    VI_DATA = window.GFL2_I18N_VI;
    return VI_DATA;
  }
  try {
    const res = await fetch('../../data/i18n_vi.json');
    if (res.ok) {
      VI_DATA = await res.json();
    }
  } catch (e) {
    console.warn('Could not load i18n_vi.json via fetch:', e.message);
  }
  if (!VI_DATA && window.GFL2_I18N_VI) {
    VI_DATA = window.GFL2_I18N_VI;
  }
  return VI_DATA;
}

function updateLangButton(lang) {
  document.querySelectorAll('#lang-toggle-btn .lang-opt').forEach(opt => {
    if (opt.getAttribute('data-lang') === lang) {
      opt.classList.add('active');
    } else {
      opt.classList.remove('active');
    }
  });
  const btn = $('lang-toggle-btn');
  if (btn) {
    btn.title = t('switch_lang_title', lang);
  }
}

function populateFormSelects(lang = currentLang) {
  const configs = [
    { id: 'c-class', cat: 'classes' },
    { id: 'c-rarity', cat: 'rarities' },
    { id: 'c-phase', cat: 'phases' },
    { id: 'c-weapon-type', cat: 'weapon_types' },
    { id: 'c-ammo-type', cat: 'ammo_types' },
    { id: 'w-weapon-type', cat: 'weapon_types' },
    { id: 'w-rarity', cat: 'rarities_weapon' }
  ];

  configs.forEach(({ id, cat }) => {
    const sel = $(id);
    if (!sel) return;
    const oldVal = sel.value;
    sel.innerHTML = '';
    sel.append(el('option', { value: '' }, t('placeholder_select', lang)));
    getTermList(cat, lang).forEach(term => {
      sel.append(el('option', { value: term }, term));
    });
    if (oldVal) {
      sel.value = mapTerm(oldVal, cat, lang);
    }
  });
}

function initGlobalControls() {
  const langBtn = $('lang-toggle-btn');
  if (langBtn && !langBtn.dataset.bound) {
    langBtn.dataset.bound = 'true';
    langBtn.addEventListener('click', (e) => {
      if (e) e.preventDefault();
      toggleLanguage();
    });
  }
  const btnDownloadI18n = $('btn-download-i18n');
  if (btnDownloadI18n && !btnDownloadI18n.dataset.bound) {
    btnDownloadI18n.dataset.bound = 'true';
    btnDownloadI18n.addEventListener('click', downloadFullI18nVi);
  }
}

async function toggleLanguage() {
  const newLang = currentLang === 'en' ? 'vi' : 'en';
  try {
    localStorage.setItem('gfl2_lang', newLang);
  } catch (e) {
    console.warn('localStorage not accessible:', e);
  }
  await applyLanguage(newLang);
  showToast(t(newLang === 'vi' ? 'toast_switched_vi' : 'toast_switched_en', newLang), 'ok');
}
window.toggleLanguage = toggleLanguage;

async function applyLanguage(lang) {
  currentLang = lang;
  window.currentLang = lang;
  updateLangButton(lang);

  // 1. Static text elements with data-i18n
  document.querySelectorAll('[data-i18n]').forEach(el => {
    const key = el.getAttribute('data-i18n');
    const trans = t(key, lang);
    if (trans) {
      if (el.tagName === 'INPUT' && (el.type === 'button' || el.type === 'submit')) {
        el.value = trans;
      } else {
        el.textContent = trans;
      }
    }
  });

  // 2. Placeholder attributes with data-i18n-placeholder
  document.querySelectorAll('[data-i18n-placeholder]').forEach(el => {
    const key = el.getAttribute('data-i18n-placeholder');
    const trans = t(key, lang);
    if (trans) el.placeholder = trans;
  });

  // 3. Dropdown selects
  populateFormSelects(lang);

  // 4. Character selector options
  renderCharSelectorOptions();

  // 5. Download i18n button visibility
  const btnDownloadI18n = $('btn-download-i18n');
  if (btnDownloadI18n) {
    btnDownloadI18n.style.display = lang === 'vi' ? 'inline-block' : 'none';
  }

  // 6. Update skill cards tag pills and labels
  document.querySelectorAll('#skills-list .skill-card').forEach(card => {
    card.querySelectorAll('.tag-pill').forEach(pill => {
      const enTag = pill.dataset.tagEn || mapTerm(pill.textContent.trim(), 'tags', 'en');
      pill.dataset.tagEn = enTag;
      pill.textContent = mapTerm(enTag, 'tags', lang);
    });

    const ammoSel = card.querySelector('.field-row select');
    if (ammoSel) {
      const oldVal = ammoSel.value;
      ammoSel.innerHTML = '';
      ammoSel.append(el('option', { value: '' }, t('placeholder_select', lang)));
      getTermList('ammo_types', lang).forEach(a => {
        ammoSel.append(el('option', { value: a }, a));
      });
      if (oldVal) ammoSel.value = mapTerm(oldVal, 'ammo_types', lang);
    }
  });

  // 7. Update Fortification tier labels
  document.querySelectorAll('#fort-list .repeat-item').forEach((row, idx) => {
    const tierNum = idx + 1;
    const badge = row.querySelector('.item-index');
    if (badge) badge.textContent = `${t('tier_label', lang)} ${tierNum}`;
  });

  // 8. Update Neural Helix headers
  document.querySelectorAll('#nh-list .repeat-item').forEach((row, idx) => {
    const num = idx + 1;
    const badge = row.querySelector('.item-index');
    if (badge) badge.textContent = lang === 'vi' ? `Mắt Cường Hóa ${num}` : `Enhancement ${num}`;
  });

  // 9. Update Keys names
  document.querySelectorAll('#keys-list .repeat-item').forEach((row, idx) => {
    const nameInp = row.querySelector('input[type="text"]');
    if (nameInp && !nameInp.dataset.userEdited) {
      const keyList = window.TERMS ? window.TERMS.keys : [];
      if (keyList[idx]) {
        nameInp.value = lang === 'vi' ? keyList[idx].vi : keyList[idx].en;
      }
    }
  });

  // 10. Switch character data between English and Vietnamese if a character is currently loaded
  const currentSlug = $('c-slug').value.trim();
  if (currentSlug) {
    if (lang === 'vi') {
      await ensureViDataLoaded();
      const viChar = VI_DATA?.characters?.[currentSlug];
      let enData = null;
      try {
        const enRes = await fetch(`../../data/characters/${currentSlug}.json`);
        if (enRes.ok) enData = await enRes.json();
      } catch {}

      if (viChar) {
        populateCharacterFormVi(currentSlug, viChar, enData);
      }
    } else {
      try {
        const res = await fetch(`../../data/characters/${currentSlug}.json`);
        if (res.ok) {
          const enData = await res.json();
          populateCharacterForm(enData);
        }
      } catch (err) {
        console.warn('Could not reload EN data:', err);
      }
    }
  }

  refreshPreview();
}

// ─────────────────────────────────────────────────────────────────────────
//  BOOT
// ─────────────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', () => {
  // Load effects.json first, then initialise the UI
  fetch('../../assets/effects.json')
    .then(r => r.ok ? r.json() : Promise.reject(r.status))
    .then(data => { EFFECTS_DATA = data ?? {}; })
    .catch(() => {
      console.warn('Could not load assets/effects.json — Insert Effect will be empty.');
    })
    .finally(async () => {
      try {
        console.log('[Boot] Starting init sequence…');
        if (currentLang === 'vi') {
          console.log('[Boot] Loading VI data…');
          await ensureViDataLoaded();
        }

        console.log('[Boot] initGlobalControls…');
        initGlobalControls();

        console.log('[Boot] populateFormSelects…');
        populateFormSelects(currentLang);

        console.log('[Boot] initTabs…');
        initTabs();
        console.log('[Boot] initCharacterTab…');
        initCharacterTab();
        console.log('[Boot] initWeaponTab…');
        initWeaponTab();
        console.log('[Boot] initFaqTab…');
        initFaqTab();
        console.log('[Boot] initExcelAutofill…');
        initExcelAutofill();

        console.log('[Boot] applyLanguage…');
        await applyLanguage(currentLang);

        console.log('[Boot] refreshPreview…');
        refreshPreview();
        console.log('[Boot] ✅ Init complete.');
      } catch (err) {
        console.error('[Boot] ❌ Init failed:', err);
        // Show visible error so it's not a silent failure
        const banner = document.createElement('div');
        banner.style.cssText = 'position:fixed;top:0;left:0;right:0;z-index:99999;background:#7f1d1d;color:#fca5a5;padding:12px 16px;font-family:monospace;font-size:13px;white-space:pre-wrap;';
        banner.textContent = `⚠ Data Entry Tool boot error — open DevTools (F12) for details:\n${err.message}\n${err.stack}`;
        document.body.prepend(banner);
      }
    });
});

// ─────────────────────────────────────────────────────────────────────────
//  ████  EXCEL AUTO-FILL (Gemini API)  ████
// ─────────────────────────────────────────────────────────────────────────

const GEMINI_LS_KEY = 'gfl2_gemini_apikey';
const GEMINI_MODEL = 'gemini-3.6-flash';

// ── API-key modal helpers ─────────────────────────────────────────────────
function getStoredApiKey() { return localStorage.getItem(GEMINI_LS_KEY) || ''; }
function saveApiKey(k) { localStorage.setItem(GEMINI_LS_KEY, k.trim()); }

function openApiKeyModal(onSaved) {
  const overlay = $('apikey-overlay');
  const inp = $('apikey-input');
  inp.value = getStoredApiKey();
  overlay.style.display = 'flex';
  inp.focus();

  function close() { overlay.style.display = 'none'; cleanup(); }

  function save() {
    const k = inp.value.trim();
    if (!k) { showToast('Please enter an API key', 'err'); return; }
    saveApiKey(k);
    close();
    onSaved(k);
  }

  function cleanup() {
    $('btn-apikey-save').removeEventListener('click', save);
    $('btn-apikey-cancel').removeEventListener('click', close);
    $('btn-apikey-cancel2').removeEventListener('click', close);
    inp.removeEventListener('keydown', onEnter);
  }

  function onEnter(e) { if (e.key === 'Enter') save(); }

  $('btn-apikey-save').addEventListener('click', save);
  $('btn-apikey-cancel').addEventListener('click', close);
  $('btn-apikey-cancel2').addEventListener('click', close);
  inp.addEventListener('keydown', onEnter);
}

// ── Status bar helpers ────────────────────────────────────────────────────
function setAiStatus(msg) {
  const bar = $('ai-status-bar');
  $('ai-status-text').textContent = msg;
  bar.style.display = 'flex';
}
function hideAiStatus() { $('ai-status-bar').style.display = 'none'; }

// ── SheetJS → raw text snapshot ───────────────────────────────────────────
/**
 * Reads the first sheet of an xlsx file and returns a plain-text
 * representation that Gemini can parse robustly.
 * Each non-empty cell is output as:  [Row R, Col C (ColLetter)]: value
 */
function xlsxToText(arrayBuffer) {
  const wb = XLSX.read(arrayBuffer, { type: 'array', cellText: true, cellDates: false });
  const ws = wb.Sheets[wb.SheetNames[0]];
  const range = XLSX.utils.decode_range(ws['!ref'] || 'A1:A1');
  const lines = [];

  for (let r = range.s.r; r <= range.e.r; r++) {
    for (let c = range.s.c; c <= range.e.c; c++) {
      const addr = XLSX.utils.encode_cell({ r, c });
      const cell = ws[addr];
      if (!cell || cell.v == null || cell.v === '') continue;
      const colLetter = XLSX.utils.encode_col(c);
      // Normalise multi-line cell values: replace CRLF / LF with ↵
      const raw = String(cell.v).replace(/\r\n|\r/g, '\n');
      lines.push(`[Row ${r + 1}, Col ${colLetter}]: ${raw}`);
    }
  }
  return lines.join('\n');
}

// ── Build Gemini prompt ───────────────────────────────────────────────────
function buildPrompt(sheetText) {
  return `You are a structured-data extraction assistant for a GFL2 (Girls' Frontline 2: Exilium) wiki.

I will give you the raw cell-by-cell dump of an Excel character sheet. Your job is to extract the data and return ONLY a valid JSON object — no markdown, no commentary, no code fences — matching the schema below exactly.

═══════════════════════════════════════════════════════
TARGET JSON SCHEMA
═══════════════════════════════════════════════════════
{
  "name": "string — character display name",
  "slug": "string — kebab-case identifier derived from name",
  "class": "one of: Bulwark | Vanguard | Support | Sentinel",
  "rarity": "one of: Elite | Standard",
  "phase": "one of: Physical | Burn | Hydro | Electric | Freeze | Corrosion | Resonance",
  "weapon_type": "one of: Assault Rifle | SMG | Shotgun | MG | Sniper Rifle | Handgun | Blade",
  "ammo_type": "one of: Light Ammo | Medium Ammo | Heavy Ammo | Shotgun Ammo | Melee  (use the Skill Attribute column)",
  "stats": { "hp": number, "atk": number, "def": number },
  "skill_attribute": "string — ammo/element noted in Skill Attribute column, or null",
  "weakness": "string — phase name noted in Weakness column, or null",
  "stability_gauge": "string — e.g. '12 points'",
  "movement_speed": "string — e.g. '6 tiles'",
  "effects_glossary": ["string — 'EffectName: description' — one entry per named effect from the Effects cell"],
  "skills": [
    {
      "name": "string — skill display name (without the tag line)",
      "tags": ["array of applicable tags from: Basic Attack | Active | Buff | Debuff | Targeted | AoE | Passive | Healing | Shield | Ultimate | Defense | Summon"],
      "ammo_type": "string or null — from the ammo column beside the skill name",
      "stability_damage": "number or null — parse from 'Stability Damage: N'",
      "cooldown": "string or null — parse from 'Cooldown: N turns'",
      "confectance_cost": "number or null — parse from 'Confectance Cost: N'",
      "range": "string or number or null — parse from 'Range' row beside the skill",
      "effect_area": "string or null — parse from 'Eff. Area' row beside the skill",
      "description": "string — full skill description text"
    }
  ],
  "summons": [
    {
      "name": "string — name of the summoned unit (e.g. 'Auto-Turret')",
      "stats": { "hp": "number", "atk": "number", "def": "number" },
      "stability_gauge": "string or null",
      "movement_speed": "string or null",
      "skills": [
        {
          "name": "string — summon skill name",
          "description": "string"
        }
      ]
    }
  ],
  "fortification": [
    {
      "tier": "number 1–6",
      "skill": "string — name of the skill this tier upgrades",
      "effect": "string — the upgrade text from 'Vertebrae Upgrade N' rows"
    }
  ],
  "source_notes": "string or null — any explanation / tip text found in the sheet"
}

═══════════════════════════════════════════════════════
EXTRACTION RULES
═══════════════════════════════════════════════════════
1. The 'summons' array is OPTIONAL. Only include it if the character spawns a persistent unit (e.g. Auto-Turret, drone) that has its own stats or sub-skills described elsewhere in the sheet.
2. For each 'Vertebrae Upgrade N' row: N is the tier number, the adjacent cell (Col C) is the effect text, and 'skill' should be the name of the skill that the upgrade modifies (infer from context).
3. Parse the Effects cell (one big multi-line cell) into individual entries: split on blank lines. Each entry starts with 'EffectName:' — keep the whole 'EffectName: description' string as a single array element.
4. The 'phase' field refers to the character's elemental phase (Electric, Burn, etc.), NOT their weakness. Map from context; if unclear use 'Physical'.
5. If a field is absent or cannot be determined, use null (not an empty string, not 0).
6. Output ONLY the JSON object. No preamble, no explanation, no markdown fences.

═══════════════════════════════════════════════════════
RAW CELL DUMP
═══════════════════════════════════════════════════════
${sheetText}`;
}

// ── Gemini API call ───────────────────────────────────────────────────────
async function callGemini(apiKey, prompt) {
  const url = `https://generativelanguage.googleapis.com/v1beta/models/${GEMINI_MODEL}:generateContent?key=${encodeURIComponent(apiKey)}`;
  const body = {
    contents: [{ parts: [{ text: prompt }] }],
    generationConfig: {
      temperature: 0.1,
      responseMimeType: 'application/json',
    },
  };

  const res = await fetch(url, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  });

  if (!res.ok) {
    const errBody = await res.json().catch(() => ({}));
    const msg = errBody?.error?.message || `HTTP ${res.status}`;
    throw new Error(msg);
  }

  const json = await res.json();
  const raw = json?.candidates?.[0]?.content?.parts?.[0]?.text;
  if (!raw) throw new Error('Empty response from Gemini');

  // Strip any accidental markdown fences
  const cleaned = raw.replace(/^```(?:json)?\s*/i, '').replace(/\s*```\s*$/, '').trim();
  return JSON.parse(cleaned);
}

// ── Map extracted data → character form shape ─────────────────────────────
/**
 * Gemini may return slightly different key names or extra fields.
 * We normalise here before handing off to populateCharacterForm().
 */
function normaliseExtracted(d) {
  const skills = (d.skills || []).map(s => ({
    name: s.name || '',
    tags: Array.isArray(s.tags) ? s.tags : [],
    ammo_type: s.ammo_type || null,
    stability_damage: s.stability_damage != null ? +s.stability_damage : null,
    cooldown: s.cooldown || null,
    confectance_cost: s.confectance_cost != null ? +s.confectance_cost : null,
    range: s.range != null ? s.range : null,
    effect_area: s.effect_area || null,
    description: (s.description || '').trim(),
  }));

  const summons = (d.summons || []).map(s => ({
    name: s.name || '',
    stats: s.stats || null,
    stability_gauge: s.stability_gauge || null,
    movement_speed: s.movement_speed || null,
    skills: Array.isArray(s.skills) ? s.skills.map(sk => ({
      name: sk.name || '',
      description: sk.description || ''
    })) : []
  }));

  const fortification = (d.fortification || []).map((f, i) => ({
    tier: f.tier != null ? +f.tier : i + 1,
    skill: f.skill || '',
    level: null,
    effect: f.effect || '',
  }));

  // Ensure 6 fort tiers exist
  for (let t = 1; t <= 6; t++) {
    if (!fortification.find(f => f.tier === t)) {
      fortification.push({ tier: t, skill: '', level: null, effect: '' });
    }
  }
  fortification.sort((a, b) => a.tier - b.tier);

  return {
    name: d.name || '',
    slug: d.slug || slugify(d.name || ''),
    class: d.class || '',
    rarity: d.rarity || '',
    phase: d.phase || '',
    weapon_type: d.weapon_type || '',
    ammo_type: d.ammo_type || '',
    signature_weapon: d.signature_weapon || null,
    stats: d.stats || null,
    skill_attribute: d.skill_attribute || null,
    weakness: d.weakness || null,
    stability_gauge: d.stability_gauge || null,
    movement_speed: d.movement_speed || null,
    effects_glossary: Array.isArray(d.effects_glossary) ? d.effects_glossary : [],
    skills,
    summons: summons.length ? summons : undefined,
    fortification,
    neural_helix: d.neural_helix || [],
    keys: d.keys || [],
    source_notes: d.source_notes || null,
  };
}

// ── Core orchestration ────────────────────────────────────────────────────
async function processExcelFile(file) {
  const btn = $('btn-excel-autofill');
  btn.disabled = true;

  try {
    setAiStatus('Reading spreadsheet…');
    const buffer = await file.arrayBuffer();

    setAiStatus('Converting cells to text…');
    const sheetText = xlsxToText(buffer);
    if (!sheetText.trim()) throw new Error('The spreadsheet appears to be empty.');

    setAiStatus('Sending to Gemini AI… (this may take 5–15 s)');
    const apiKey = getStoredApiKey();
    const prompt = buildPrompt(sheetText);
    const extracted = await callGemini(apiKey, prompt);

    setAiStatus('Populating form…');
    const normalised = normaliseExtracted(extracted);
    populateCharacterForm(normalised);

    hideAiStatus();
    showToast(`✨ Auto-filled: ${normalised.name || file.name}`, 'ok', 4000);
  } catch (err) {
    hideAiStatus();
    console.error('[Excel Auto-fill]', err);
    showToast(`Auto-fill failed: ${err.message}`, 'err', 6000);
  } finally {
    btn.disabled = false;
    // Reset the file input so the same file can be re-selected
    $('file-load-excel').value = '';
  }
}

// ── Initialisation ────────────────────────────────────────────────────────
function initExcelAutofill() {
  const btn = $('btn-excel-autofill');
  const fileInput = $('file-load-excel');

  // Dismiss status bar manually
  $('btn-ai-status-close').addEventListener('click', hideAiStatus);

  btn.addEventListener('click', () => {
    const apiKey = getStoredApiKey();
    if (!apiKey) {
      // First time: ask for API key, then open file picker on save
      openApiKeyModal(() => fileInput.click());
    } else {
      fileInput.click();
    }
  });

  fileInput.addEventListener('change', e => {
    const file = e.target.files?.[0];
    if (!file) return;
    // Switch to character tab if not already active
    const charBtn = $('tab-btn-character');
    if (charBtn && !charBtn.classList.contains('active')) charBtn.click();
    processExcelFile(file);
  });
}

