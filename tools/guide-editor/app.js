// ============================================================
//  GFL2 Wiki — Guide Editor (app.js)
//  Block-based guide editor with live preview
// ============================================================
'use strict';

// ── State ─────────────────────────────────────────────────────────────────
const state = {
  charSlug: '',
  title: '',
  blocks: [],    // array of block objects
  charData: {},  // slug -> character JSON
  charList: [],  // [{slug, name, rarity, class}]
  weaponList: [],// [{slug, name, rarity, weapon_type}]
};

let blockCounter = 0;

// ── Utils ──────────────────────────────────────────────────────────────────
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

function showToast(msg, type = 'ok', dur = 2800) {
  const t = $('toast');
  t.textContent = msg;
  t.className = `show ${type}`;
  setTimeout(() => { t.className = ''; }, dur);
}

function escHTML(s) {
  return String(s || '').replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');
}

// ── Data Loading ───────────────────────────────────────────────────────────
async function loadSearchIndex() {
  try {
    const res = await fetch('../../dist/search-index.json');
    if (!res.ok) throw new Error();
    const idx = await res.json();
    state.charList = idx.filter(e => e.category === 'doll').sort((a,b) => a.name.localeCompare(b.name));
    state.weaponList = idx.filter(e => e.category === 'weapon').sort((a,b) => a.name.localeCompare(b.name));
    populateAllSelectors();
  } catch {
    showToast('Could not load search index — run build.py first', 'err', 5000);
  }
}

async function loadCharData(slug) {
  if (!slug || state.charData[slug]) return state.charData[slug];
  try {
    const res = await fetch(`../../data/characters/${slug}.json`);
    if (!res.ok) throw new Error();
    const data = await res.json();
    state.charData[slug] = data;
    return data;
  } catch {
    return null;
  }
}

function populateAllSelectors() {
  // Main char selector in header
  const hdr = $('char-sel');
  hdr.innerHTML = '<option value="">— Character —</option>';
  state.charList.forEach(c => {
    hdr.append(el('option', {value: c.slug}, `${c.name} (${c.class || ''})`));
  });

  // Modal selectors
  ['modal-skill-char', 'modal-char-card-sel'].forEach(id => {
    const sel = $(id);
    sel.innerHTML = '<option value="">— Select character —</option>';
    state.charList.forEach(c => sel.append(el('option', {value: c.slug}, c.name)));
  });

  const wSel = $('modal-weapon-card-sel');
  wSel.innerHTML = '<option value="">— Select weapon —</option>';
  state.weaponList.forEach(w => wSel.append(el('option', {value: w.slug}, `${w.name} (${w.rarity || ''})`)));
}

// ── Block Management ──────────────────────────────────────────────────────
function addBlock(blockDef) {
  blockCounter++;
  const id = `block-${blockCounter}`;
  blockDef.id = id;
  state.blocks.push(blockDef);
  renderBlockItem(blockDef);
  updateEmptyState();
  renderPreview();
}

function removeBlock(id) {
  state.blocks = state.blocks.filter(b => b.id !== id);
  $(id)?.remove();
  updateEmptyState();
  renderPreview();
}

function moveBlock(id, dir) {
  const idx = state.blocks.findIndex(b => b.id === id);
  if (idx < 0) return;
  const newIdx = idx + dir;
  if (newIdx < 0 || newIdx >= state.blocks.length) return;
  [state.blocks[idx], state.blocks[newIdx]] = [state.blocks[newIdx], state.blocks[idx]];
  // Re-render list
  const list = $('blocks-list');
  list.innerHTML = '';
  state.blocks.forEach(b => renderBlockItem(b));
  renderPreview();
}

function updateEmptyState() {
  const empty = $('editor-empty');
  if (empty) empty.style.display = state.blocks.length === 0 ? 'block' : 'none';
}

function blockActions(id) {
  const row = el('div', {cls: 'block-actions'});
  row.append(
    el('button', {cls: 'block-action-btn', onclick: () => moveBlock(id, -1)}, '↑'),
    el('button', {cls: 'block-action-btn', onclick: () => moveBlock(id, 1)}, '↓'),
    el('button', {cls: 'block-action-btn danger', onclick: () => removeBlock(id)}, '✕')
  );
  return row;
}

function blockHandle() {
  const h = el('div', {cls: 'block-handle'});
  for (let i=0;i<3;i++) h.append(el('span'));
  return h;
}

// ── Block Renderers ────────────────────────────────────────────────────────
function renderBlockItem(b) {
  const list = $('blocks-list');
  let item;
  switch(b.type) {
    case 'heading': item = renderHeadingBlock(b); break;
    case 'paragraph': item = renderParagraphBlock(b); break;
    case 'char_card': item = renderCharCardBlock(b); break;
    case 'weapon_card': item = renderWeaponCardBlock(b); break;
    case 'skill_ref': item = renderSkillRefBlock(b); break;
    case 'summon_skill_ref': item = renderSummonSkillRefBlock(b); break;
    case 'table': item = renderTableBlock(b); break;
    case 'image': item = renderImageBlock(b); break;
    case 'link': item = renderLinkBlock(b); break;
    default: return;
  }
  item.id = b.id;
  list.append(item);
}

function wrapBlock(b, typeLabel, body) {
  const item = el('div', {cls: 'block-item'});
  item.append(blockHandle());
  const bodyEl = el('div', {cls: 'block-body'});
  bodyEl.append(el('div', {cls: 'block-type-badge'}, typeLabel));
  bodyEl.append(body);
  item.append(bodyEl);
  item.append(blockActions(b.id));
  return item;
}

function renderHeadingBlock(b) {
  const body = el('div', {cls: 'field-row', style: 'display:flex; gap:0.4rem; align-items:center;'});
  const lvlSel = el('select', {cls: 'block-heading-sel'});
  [2,3].forEach(l => {
    const o = el('option', {value: l}, `H${l}`);
    if (b.level == l) o.selected = true;
    lvlSel.append(o);
  });
  const inp = el('input', {type:'text', cls:'block-input', placeholder:'Heading text…'});
  if (b.text) inp.value = b.text;
  lvlSel.addEventListener('change', () => { b.level = +lvlSel.value; renderPreview(); });
  inp.addEventListener('input', () => { b.text = inp.value; renderPreview(); });
  body.append(lvlSel, inp);
  return wrapBlock(b, `H${b.level || 2} Heading`, body);
}

function renderParagraphBlock(b) {
  const ta = el('textarea', {cls:'block-input', placeholder:'Paragraph text… (HTML allowed: <strong>, <em>, <a>)'});
  if (b.html) ta.value = b.html;
  ta.addEventListener('input', () => { b.html = ta.value; renderPreview(); });
  return wrapBlock(b, '¶ Paragraph', ta);
}

function renderCharCardBlock(b) {
  const sel = el('select', {cls:'block-card-sel'});
  sel.append(el('option', {value:''}, '— Select character —'));
  state.charList.forEach(c => {
    const o = el('option', {value:c.slug}, `${c.name} (${c.class || ''})`);
    if (c.slug === b.slug) o.selected = true;
    sel.append(o);
  });
  sel.addEventListener('change', () => { b.slug = sel.value; renderPreview(); });
  return wrapBlock(b, '👤 Character Card', sel);
}

function renderWeaponCardBlock(b) {
  const sel = el('select', {cls:'block-card-sel'});
  sel.append(el('option', {value:''}, '— Select weapon —'));
  state.weaponList.forEach(w => {
    const o = el('option', {value:w.slug}, `${w.name} (${w.rarity || ''})`);
    if (w.slug === b.slug) o.selected = true;
    sel.append(o);
  });
  sel.addEventListener('change', () => { b.slug = sel.value; renderPreview(); });
  return wrapBlock(b, '🔫 Weapon Card', sel);
}

function renderSkillRefBlock(b) {
  const row = el('div', {cls:'skill-ref-row'});
  const charSel = el('select');
  charSel.append(el('option', {value:''}, '— Character —'));
  state.charList.forEach(c => {
    const o = el('option', {value:c.slug}, c.name);
    if (c.slug === b.char) o.selected = true;
    charSel.append(o);
  });

  const skillSel = el('select');
  skillSel.append(el('option', {value:''}, '— Skill —'));

  async function refreshSkills() {
    const slug = charSel.value;
    skillSel.innerHTML = '';
    skillSel.append(el('option', {value:''}, '— Skill —'));
    if (!slug) return;
    const data = await loadCharData(slug);
    if (!data?.skills) return;
    data.skills.forEach((sk, idx) => {
      const o = el('option', {value:idx}, `Skill ${idx+1}: ${sk.name}`);
      if (b.skill_idx == idx) o.selected = true;
      skillSel.append(o);
    });
  }

  charSel.addEventListener('change', () => { b.char = charSel.value; refreshSkills(); renderPreview(); });
  skillSel.addEventListener('change', () => { b.skill_idx = +skillSel.value; renderPreview(); });
  refreshSkills();
  row.append(charSel, skillSel);
  return wrapBlock(b, '⚡ Skill Reference', row);
}

function renderSummonSkillRefBlock(b) {
  const row = el('div', {cls:'skill-ref-row'});
  const charSel = el('select');
  charSel.append(el('option', {value:''}, '— Character —'));
  state.charList.forEach(c => {
    const o = el('option', {value:c.slug}, c.name);
    if (c.slug === b.char) o.selected = true;
    charSel.append(o);
  });

  const summonSel = el('select');
  summonSel.append(el('option', {value:''}, '— Summon —'));

  const skillSel = el('select');
  skillSel.append(el('option', {value:''}, '— Skill —'));

  async function refreshSummons() {
    const slug = charSel.value;
    summonSel.innerHTML = '';
    summonSel.append(el('option', {value:''}, '— Summon —'));
    skillSel.innerHTML = '';
    skillSel.append(el('option', {value:''}, '— Skill —'));
    if (!slug) return;
    const data = await loadCharData(slug);
    if (!data?.summons) return;
    data.summons.forEach((sm, idx) => {
      const o = el('option', {value:idx}, sm.name || `Summon ${idx+1}`);
      if (b.summon_idx == idx) o.selected = true;
      summonSel.append(o);
    });
    if (b.summon_idx != null) refreshSummonSkills();
  }

  async function refreshSummonSkills() {
    const slug = charSel.value;
    const sumIdx = +summonSel.value;
    skillSel.innerHTML = '';
    skillSel.append(el('option', {value:''}, '— Skill —'));
    if (!slug || summonSel.value === '') return;
    const data = await loadCharData(slug);
    const summon = data?.summons?.[sumIdx];
    if (!summon?.skills) return;
    summon.skills.forEach((sk, idx) => {
      const o = el('option', {value:idx}, sk.name || `Skill ${idx+1}`);
      if (b.skill_idx == idx) o.selected = true;
      skillSel.append(o);
    });
  }

  charSel.addEventListener('change', () => { b.char = charSel.value; refreshSummons(); renderPreview(); });
  summonSel.addEventListener('change', () => { b.summon_idx = +summonSel.value; refreshSummonSkills(); renderPreview(); });
  skillSel.addEventListener('change', () => { b.skill_idx = +skillSel.value; renderPreview(); });
  refreshSummons();
  row.append(charSel, summonSel, skillSel);
  return wrapBlock(b, '🤖 Summon Skill', row);
}

function renderTableBlock(b) {
  if (!b.headers?.length) { b.headers = ['Column 1']; b.rows = [['']]; }
  const wrapper = el('div', {cls:'table-editor'});

  function rebuildTable() {
    wrapper.innerHTML = '';
    const table = el('table');
    // Header row
    const thead = el('thead'); const trh = el('tr');
    b.headers.forEach((h, ci) => {
      const th = el('th');
      const inp = el('input', {type:'text', value:h, placeholder:`Col ${ci+1}`});
      inp.addEventListener('input', () => { b.headers[ci] = inp.value; renderPreview(); });
      th.append(inp); trh.append(th);
    });
    thead.append(trh); table.append(thead);
    // Data rows
    const tbody = el('tbody');
    b.rows.forEach((row, ri) => {
      const tr = el('tr');
      b.headers.forEach((_, ci) => {
        const td = el('td');
        const inp = el('input', {type:'text', value: row[ci] || '', placeholder:'…'});
        inp.addEventListener('input', () => { b.rows[ri][ci] = inp.value; renderPreview(); });
        td.append(inp); tr.append(td);
      });
      tbody.append(tr);
    });
    table.append(tbody);
    wrapper.append(table);

    const ctrl = el('div', {cls:'table-controls'});
    const btnAddCol = el('button', {cls:'btn btn-secondary', style:'font-size:0.72rem;padding:3px 8px', type:'button'}, '+ Col');
    btnAddCol.addEventListener('click', () => { b.headers.push(`Col ${b.headers.length+1}`); b.rows.forEach(r => r.push('')); rebuildTable(); renderPreview(); });
    const btnAddRow = el('button', {cls:'btn btn-secondary', style:'font-size:0.72rem;padding:3px 8px', type:'button'}, '+ Row');
    btnAddRow.addEventListener('click', () => { b.rows.push(b.headers.map(()=>'')); rebuildTable(); renderPreview(); });
    const btnDelCol = el('button', {cls:'btn btn-secondary', style:'font-size:0.72rem;padding:3px 8px', type:'button'}, '- Col');
    btnDelCol.addEventListener('click', () => { if(b.headers.length<=1) return; b.headers.pop(); b.rows.forEach(r=>r.pop()); rebuildTable(); renderPreview(); });
    const btnDelRow = el('button', {cls:'btn btn-secondary', style:'font-size:0.72rem;padding:3px 8px', type:'button'}, '- Row');
    btnDelRow.addEventListener('click', () => { if(b.rows.length<=1) return; b.rows.pop(); rebuildTable(); renderPreview(); });
    ctrl.append(btnAddCol, btnAddRow, btnDelCol, btnDelRow);
    wrapper.append(ctrl);
  }
  rebuildTable();
  return wrapBlock(b, '⊞ Table', wrapper);
}

function renderImageBlock(b) {
  const body = el('div');
  const inp = el('input', {type:'text', cls:'block-input', placeholder:'Image path or URL (assets/images/…)'});
  if (b.src) inp.value = b.src;
  const capInp = el('input', {type:'text', cls:'block-input', placeholder:'Caption (optional)', style:'margin-top:0.4rem'});
  if (b.caption) capInp.value = b.caption;

  const fileBtn = el('button', {cls:'btn btn-secondary', type:'button', style:'font-size:0.75rem;padding:4px 10px;margin-top:0.4rem'}, '📁 Choose File');
  const fileInp = el('input', {type:'file', accept:'image/*', style:'display:none'});
  const preview = el('img', {cls:'img-block-preview', alt:'preview', style: b.src ? '' : 'display:none'});
  if (b.src) preview.src = b.src;

  inp.addEventListener('input', () => { b.src = inp.value; preview.src = inp.value; preview.style.display = inp.value ? 'block' : 'none'; renderPreview(); });
  capInp.addEventListener('input', () => { b.caption = capInp.value; renderPreview(); });
  fileBtn.addEventListener('click', () => fileInp.click());
  fileInp.addEventListener('change', e => {
    const file = e.target.files[0]; if (!file) return;
    const url = URL.createObjectURL(file);
    preview.src = url; preview.style.display = 'block';
    inp.value = `assets/images/${file.name}`;
    b.src = inp.value; b._objectUrl = url;
    renderPreview();
  });

  body.append(inp, capInp, fileBtn, fileInp, preview);
  return wrapBlock(b, '🖼 Image', body);
}

function renderLinkBlock(b) {
  const body = el('div', {style:'display:flex;gap:0.4rem;flex-wrap:wrap'});
  const urlInp = el('input', {type:'url', cls:'block-input', placeholder:'https://…', style:'flex:2'});
  const txtInp = el('input', {type:'text', cls:'block-input', placeholder:'Display text…', style:'flex:1'});
  if (b.url) urlInp.value = b.url;
  if (b.text) txtInp.value = b.text;
  urlInp.addEventListener('input', () => { b.url = urlInp.value; renderPreview(); });
  txtInp.addEventListener('input', () => { b.text = txtInp.value; renderPreview(); });
  body.append(urlInp, txtInp);
  return wrapBlock(b, '🔗 Link', body);
}

// ── Preview Renderer ───────────────────────────────────────────────────────
function renderPreview() {
  const title = $('guide-title').value;
  const parts = [];

  if (title) parts.push(`<h1 style="font-size:1.5rem;font-weight:800;color:#e8ecf4;margin-bottom:1.25rem">${escHTML(title)}</h1>`);

  state.blocks.forEach(b => {
    parts.push(renderBlockPreview(b));
  });

  $('preview-content').innerHTML = parts.join('');
}

function renderBlockPreview(b) {
  switch(b.type) {
    case 'heading': {
      const tag = `h${b.level || 2}`;
      return `<${tag}>${escHTML(b.text || '')}</${tag}>`;
    }
    case 'paragraph':
      return `<p>${b.html || ''}</p>`;
    case 'char_card': {
      if (!b.slug) return '';
      const ch = state.charList.find(c => c.slug === b.slug);
      const name = ch?.name || b.slug;
      const imgSrc = `../../assets/images/characters/${b.slug}/avatar.png`;
      return `<a href="../../dist/characters/${b.slug}.html" class="preview-char-card" target="_blank">
        <img src="${escHTML(imgSrc)}" onerror="this.style.display='none'" alt="${escHTML(name)}" />
        ${escHTML(name)}
      </a><br>`;
    }
    case 'weapon_card': {
      if (!b.slug) return '';
      const wp = state.weaponList.find(w => w.slug === b.slug);
      const name = wp?.name || b.slug;
      const imgSrc = `../../assets/images/weapons/${b.slug}.png`;
      return `<div class="preview-weapon-card">
        <img src="${escHTML(imgSrc)}" onerror="this.style.display='none'" alt="${escHTML(name)}" />
        ${escHTML(name)}
      </div><br>`;
    }
    case 'skill_ref': {
      if (!b.char || b.skill_idx == null) return '';
      const data = state.charData[b.char];
      const sk = data?.skills?.[b.skill_idx];
      if (!sk) return `<span class="preview-skill-chip">⚡ Skill (loading…)</span>`;
      const icon = sk.icon ? `<img src="../../${escHTML(sk.icon)}" onerror="this.style.display='none'" />` : '';
      const tags = sk.tags?.join(', ') || '';
      const desc = escHTML(sk.description || '').slice(0, 200);
      return `<span class="preview-skill-chip">${icon}${escHTML(sk.name)}
        <span class="skill-popover-tip">
          <div class="skill-popover-tip-name">${escHTML(sk.name)}</div>
          <div class="skill-popover-tip-tags">${escHTML(tags)}</div>
          <div class="skill-popover-tip-desc">${desc}</div>
        </span>
      </span>`;
    }
    case 'summon_skill_ref': {
      if (!b.char || b.summon_idx == null || b.skill_idx == null) return '';
      const data = state.charData[b.char];
      const sk = data?.summons?.[b.summon_idx]?.skills?.[b.skill_idx];
      if (!sk) return `<span class="preview-skill-chip">🤖 Summon Skill (loading…)</span>`;
      const icon = sk.icon ? `<img src="../../${escHTML(sk.icon)}" />` : '';
      const desc = escHTML(sk.description || '').slice(0, 200);
      const summonName = data?.summons?.[b.summon_idx]?.name || '';
      return `<span class="preview-skill-chip">${icon}${escHTML(sk.name)} <small style="opacity:0.6">(${escHTML(summonName)})</small>
        <span class="skill-popover-tip">
          <div class="skill-popover-tip-name">${escHTML(sk.name)}</div>
          <div class="skill-popover-tip-tags">Summon: ${escHTML(summonName)}</div>
          <div class="skill-popover-tip-desc">${desc}</div>
        </span>
      </span>`;
    }
    case 'table': {
      if (!b.headers?.length) return '';
      const headers = b.headers.map(h => `<th>${escHTML(h)}</th>`).join('');
      const rows = (b.rows || []).map(r =>
        `<tr>${b.headers.map((_,i) => `<td>${escHTML(r[i]||'')}</td>`).join('')}</tr>`
      ).join('');
      return `<table class="preview-table"><thead><tr>${headers}</tr></thead><tbody>${rows}</tbody></table>`;
    }
    case 'image': {
      if (!b.src) return '';
      const src = b._objectUrl || `../../${b.src}`;
      const cap = b.caption ? `<p class="preview-img-caption">${escHTML(b.caption)}</p>` : '';
      return `<img class="preview-img" src="${escHTML(src)}" alt="${escHTML(b.caption||'')}"/>${cap}`;
    }
    case 'link':
      if (!b.url) return '';
      return `<p><a href="${escHTML(b.url)}" target="_blank" rel="noopener">${escHTML(b.text || b.url)}</a></p>`;
    default: return '';
  }
}

// ── Save / Load ────────────────────────────────────────────────────────────
function buildGuideData() {
  return {
    slug: ($('char-sel').value || 'unnamed') + '-guide',
    char_slug: $('char-sel').value || '',
    title: $('guide-title').value || 'Untitled Guide',
    last_updated: new Date().toISOString().slice(0,10),
    blocks: state.blocks.map(b => {
      const clean = {...b};
      delete clean._objectUrl; // strip blob URLs
      return clean;
    }),
  };
}

async function saveGuide() {
  const data = buildGuideData();
  const json = JSON.stringify(data, null, 2);
  const filename = `${data.slug}.json`;
  if ('showSaveFilePicker' in window) {
    try {
      const handle = await window.showSaveFilePicker({
        suggestedName: filename,
        types: [{ description: 'JSON', accept: {'application/json': ['.json']} }],
        startIn: 'documents',
      });
      const w = await handle.createWritable();
      await w.write(json);
      await w.close();
      showToast(`Saved ${filename}`, 'ok');
    } catch(e) {
      if (e.name !== 'AbortError') showToast(`Save failed: ${e.message}`, 'err');
    }
  } else {
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([json], {type:'application/json'}));
    a.download = filename;
    a.click();
    showToast(`Downloaded ${filename}`, 'ok');
  }
}

function loadGuide(e) {
  const file = e.target.files[0]; if (!file) return;
  const reader = new FileReader();
  reader.onload = ev => {
    try {
      const data = JSON.parse(ev.target.result);
      // Reset
      $('char-sel').value = data.char_slug || '';
      $('guide-title').value = data.title || '';
      state.blocks = [];
      blockCounter = 0;
      $('blocks-list').innerHTML = '';
      (data.blocks || []).forEach(b => {
        blockCounter++;
        b.id = `block-${blockCounter}`;
        state.blocks.push(b);
        renderBlockItem(b);
      });
      updateEmptyState();
      renderPreview();
      showToast(`Loaded: ${data.title || file.name}`, 'ok');
    } catch(err) {
      showToast('Invalid JSON guide file', 'err');
    }
    e.target.value = '';
  };
  reader.readAsText(file);
}

// ── Modal Helpers ──────────────────────────────────────────────────────────
function openModal(id) { $(id).style.display = 'flex'; }
function closeModal(id) { $(id).style.display = 'none'; }

function modalOk(modalId, onOk) {
  const id = `modal-${modalId}`;
  $(`modal-${modalId}-ok`)?.addEventListener('click', () => { closeModal(id); onOk(); });
  $(`modal-${modalId}-cancel`)?.addEventListener('click', () => closeModal(id));
}

// ── Toolbar Handlers ───────────────────────────────────────────────────────
function initToolbar() {
  $('tb-heading').addEventListener('click', () => {
    $('modal-heading-text').value = '';
    openModal('modal-heading');
    setTimeout(() => $('modal-heading-text').focus(), 50);
  });

  $('tb-paragraph').addEventListener('click', () => {
    addBlock({type:'paragraph', html:''});
  });

  $('tb-char-card').addEventListener('click', () => {
    openModal('modal-char-card');
  });

  $('tb-weapon-card').addEventListener('click', () => {
    openModal('modal-weapon-card');
  });

  $('tb-skill-ref').addEventListener('click', () => {
    $('modal-skill-title').textContent = '⚡ Insert Skill Reference';
    $('modal-skill-summon-field').style.display = 'none';
    $('modal-skill-label').textContent = 'Skill';
    $('modal-skill-char').value = '';
    $('modal-skill-pick').innerHTML = '<option value="">— Skill —</option>';
    openModal('modal-skill');
    // Wire char select to load skills
    const charSel = $('modal-skill-char');
    charSel.onchange = async () => {
      const skillSel = $('modal-skill-pick');
      skillSel.innerHTML = '<option value="">— Skill —</option>';
      const data = await loadCharData(charSel.value);
      (data?.skills || []).forEach((sk, i) => {
        skillSel.append(el('option', {value:i}, `${i+1}. ${sk.name}`));
      });
    };
  });

  $('tb-summon-ref').addEventListener('click', () => {
    $('modal-skill-title').textContent = '🤖 Insert Summon Skill';
    $('modal-skill-summon-field').style.display = 'block';
    $('modal-skill-label').textContent = 'Summon Skill';
    $('modal-skill-char').value = '';
    $('modal-skill-summon').innerHTML = '<option value="">— Summon —</option>';
    $('modal-skill-pick').innerHTML = '<option value="">— Skill —</option>';
    openModal('modal-skill');

    const charSel = $('modal-skill-char');
    const summonSel = $('modal-skill-summon');
    const skillSel = $('modal-skill-pick');

    charSel.onchange = async () => {
      summonSel.innerHTML = '<option value="">— Summon —</option>';
      skillSel.innerHTML = '<option value="">— Skill —</option>';
      const data = await loadCharData(charSel.value);
      (data?.summons || []).forEach((sm, i) => {
        summonSel.append(el('option', {value:i}, sm.name || `Summon ${i+1}`));
      });
    };
    summonSel.onchange = async () => {
      skillSel.innerHTML = '<option value="">— Skill —</option>';
      const data = await loadCharData(charSel.value);
      const summon = data?.summons?.[+summonSel.value];
      (summon?.skills || []).forEach((sk, i) => {
        skillSel.append(el('option', {value:i}, sk.name || `Skill ${i+1}`));
      });
    };
  });

  $('tb-table').addEventListener('click', () => {
    $('modal-table-cols').value = 3;
    $('modal-table-rows').value = 3;
    openModal('modal-table');
  });

  $('tb-image').addEventListener('click', () => {
    addBlock({type:'image', src:'', caption:''});
  });

  $('tb-link').addEventListener('click', () => {
    $('modal-link-url').value = '';
    $('modal-link-text').value = '';
    openModal('modal-link');
    setTimeout(() => $('modal-link-url').focus(), 50);
  });
}

function initModals() {
  // Heading modal
  $('modal-heading-ok').addEventListener('click', () => {
    const text = $('modal-heading-text').value.trim();
    const level = +$('modal-heading-level').value;
    if (!text) return;
    addBlock({type:'heading', level, text});
    closeModal('modal-heading');
  });
  $('modal-heading-cancel').addEventListener('click', () => closeModal('modal-heading'));
  $('modal-heading-text').addEventListener('keydown', e => { if (e.key==='Enter') $('modal-heading-ok').click(); });

  // Table modal
  $('modal-table-ok').addEventListener('click', () => {
    const cols = Math.max(1, Math.min(10, +$('modal-table-cols').value));
    const rows = Math.max(1, Math.min(20, +$('modal-table-rows').value));
    const headers = Array.from({length:cols}, (_,i) => `Column ${i+1}`);
    const rowData = Array.from({length:rows}, () => Array(cols).fill(''));
    addBlock({type:'table', headers, rows:rowData});
    closeModal('modal-table');
  });
  $('modal-table-cancel').addEventListener('click', () => closeModal('modal-table'));

  // Skill/summon modal
  $('modal-skill-ok').addEventListener('click', () => {
    const charSlug = $('modal-skill-char').value;
    const isSummon = $('modal-skill-summon-field').style.display !== 'none';
    if (!charSlug) return;
    if (isSummon) {
      const summonIdx = $('modal-skill-summon').value;
      const skillIdx = $('modal-skill-pick').value;
      if (summonIdx === '' || skillIdx === '') return;
      addBlock({type:'summon_skill_ref', char:charSlug, summon_idx:+summonIdx, skill_idx:+skillIdx});
    } else {
      const skillIdx = $('modal-skill-pick').value;
      if (skillIdx === '') return;
      addBlock({type:'skill_ref', char:charSlug, skill_idx:+skillIdx});
    }
    closeModal('modal-skill');
  });
  $('modal-skill-cancel').addEventListener('click', () => closeModal('modal-skill'));

  // Char card modal
  $('modal-char-card-ok').addEventListener('click', () => {
    const slug = $('modal-char-card-sel').value;
    if (!slug) return;
    addBlock({type:'char_card', slug});
    closeModal('modal-char-card');
  });
  $('modal-char-card-cancel').addEventListener('click', () => closeModal('modal-char-card'));

  // Weapon card modal
  $('modal-weapon-card-ok').addEventListener('click', () => {
    const slug = $('modal-weapon-card-sel').value;
    if (!slug) return;
    addBlock({type:'weapon_card', slug});
    closeModal('modal-weapon-card');
  });
  $('modal-weapon-card-cancel').addEventListener('click', () => closeModal('modal-weapon-card'));

  // Link modal
  $('modal-link-ok').addEventListener('click', () => {
    const url = $('modal-link-url').value.trim();
    const text = $('modal-link-text').value.trim();
    if (!url) return;
    addBlock({type:'link', url, text: text || url});
    closeModal('modal-link');
  });
  $('modal-link-cancel').addEventListener('click', () => closeModal('modal-link'));
  $('modal-link-url').addEventListener('keydown', e => { if (e.key==='Enter') $('modal-link-ok').click(); });
}

// ── Boot ───────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  await loadSearchIndex();
  initToolbar();
  initModals();

  $('btn-save-guide').addEventListener('click', saveGuide);
  $('btn-load-guide').addEventListener('click', () => $('file-load-guide').click());
  $('file-load-guide').addEventListener('change', loadGuide);
  $('guide-title').addEventListener('input', renderPreview);
  $('char-sel').addEventListener('change', () => {
    state.charSlug = $('char-sel').value;
    renderPreview();
  });

  updateEmptyState();
  renderPreview();
});