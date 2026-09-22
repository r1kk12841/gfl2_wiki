// ============================================================
//  GFL2 Wiki — Guide Editor (app.js)
//  Block-based guide editor with live preview
// ============================================================
'use strict';

// ── State ─────────────────────────────────────────────────────────────────
const state = {
  charSlug: '',
  title: '',
  author: 'Community',
  lastUpdated: '',
  blocks: [],    // array of block objects
  charData: {},  // slug -> character JSON
  charList: [],  // [{slug, name, rarity, class}]
  weaponList: [],// [{slug, name, rarity, weapon_type}]
  canonicalWeaponList: [],
  viCharacters: {},
  viWeapons: {},
  effects: {},
};

let blockCounter = 0;
let editableSelection = null;
let draggedBlockId = null;

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

function toEditorHTML(html) {
  return String(html || '')
    .replace(/src="\.\.\/assets\//g, 'src="../../assets/')
    .replace(/href="\.\.\/(characters|weapons)\//g, 'href="../../dist/$1/');
}

function toStoredHTML(html) {
  return String(html || '')
    .replace(/src="\.\.\/\.\.\/assets\//g, 'src="../assets/')
    .replace(/href="\.\.\/\.\.\/dist\/(characters|weapons)\//g, 'href="../$1/');
}

function sanitizeStoredHTML(html) {
  return window.GuideRichText.sanitizeRichHTML(toStoredHTML(html));
}

function characterInlineHTML(slug) {
  const character = state.charList.find(item => item.slug === slug);
  const name = character?.name || slug;
  return `<a class="guide-inline-ref guide-inline-character" href="../characters/${escHTML(slug)}.html" title="${escHTML(name)}"><img class="guide-inline-icon" src="../assets/images/characters/${escHTML(slug)}/avatar.png" alt="${escHTML(name)}">${escHTML(name)}</a>`;
}

function weaponInlineHTML(slug) {
  const wp = state.weaponList.find(item => item.slug === slug);
  const localized = localizedWeapon(slug);
  const name = localized.name || wp?.name || slug;
  const imagePath = wp?.image || `assets/images/weapons/${wp?.name || slug}.png`;
  const description = localized.effect || localized.trait || name;
  return `<a class="guide-inline-ref guide-inline-weapon" href="../weapons/${escHTML(slug)}.html"><img class="guide-inline-icon" src="../${escHTML(imagePath)}" alt="${escHTML(name)}">${escHTML(name)}<span class="guide-ref-popover guide-weapon-popover"><img class="guide-weapon-popover-image" src="../${escHTML(imagePath)}" alt=""><span class="guide-weapon-popover-name">${escHTML(name)}</span><span class="guide-weapon-popover-desc">${escHTML(description)}</span></span></a>`;
}

function stripGameMarkup(value) {
  return String(value || '')
    .replace(/<\/?color(?:=[^>]+)?>/gi, '')
    .replace(/\r\n?/g, '\n')
    .trim();
}

function skillInlineHTML(charSlug, skillIdx, summonIdx = null) {
  const skill = localizedSkill(charSlug, skillIdx, summonIdx);
  if (!skill) return '';
  const icon = skill.icon
    ? `<img class="guide-inline-icon" src="../${escHTML(skill.icon)}" alt="${escHTML(skill.name)}">`
    : '';
  const description = stripGameMarkup(skill.description || '');
  return `<span class="guide-inline-ref guide-inline-skill" tabindex="0">${icon}${escHTML(skill.name)}<span class="guide-ref-popover guide-skill-popover"><span class="guide-skill-popover-name">${escHTML(skill.name)}</span><span class="guide-skill-popover-desc">${escHTML(description)}</span></span></span>`;
}

function localizedWeapon(slug) {
  return state.viWeapons[slug] || state.weaponList.find(item => item.slug === slug) || {};
}

function localizedSkill(charSlug, skillIdx, summonIdx = null) {
  const source = state.charData[charSlug];
  const localized = state.viCharacters[charSlug];
  const sourceSkill = summonIdx == null
    ? source?.skills?.[skillIdx]
    : source?.summons?.[summonIdx]?.skills?.[skillIdx];
  const localizedSkillData = summonIdx == null
    ? localized?.skills?.[skillIdx]
    : localized?.summons?.[summonIdx]?.skills?.[skillIdx];
  if (!sourceSkill && !localizedSkillData) return null;
  return {
    ...(sourceSkill || {}),
    ...(localizedSkillData || {}),
    icon: sourceSkill?.icon || localizedSkillData?.icon || '',
  };
}

function normalizeReferenceText(value) {
  return ` ${String(value || '').normalize('NFKC').toLocaleLowerCase('vi').replace(/[^\p{L}\p{N}]+/gu, ' ').trim()} `;
}

function normalizeSearchText(value) {
  return String(value || '')
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .replace(/đ/g, 'd')
    .replace(/Đ/g, 'D')
    .toLocaleLowerCase('vi')
    .trim();
}

function filterSelectOptions(input, select) {
  const options = select._guideSearchOptions || [];
  const query = normalizeSearchText(input.value);
  const current = select.value;
  select.innerHTML = '';
  options
    .filter((option, index) => index === 0 || !query || normalizeSearchText(option.text).includes(query))
    .forEach(option => select.append(el('option', { value: option.value }, option.text)));
  if ([...select.options].some(option => option.value === current)) select.value = current;
}

function cacheSelectOptions(selectOrId) {
  const select = typeof selectOrId === 'string' ? $(selectOrId) : selectOrId;
  if (!select) return;
  select._guideSearchOptions = [...select.options].map(option => ({
    value: option.value,
    text: option.textContent,
  }));
  const input = document.querySelector(`[data-search-select="${select.id}"]`);
  if (input) filterSelectOptions(input, select);
}

function bindSelectSearch(inputId, selectId) {
  const input = $(inputId);
  const select = $(selectId);
  if (!input || !select) return;
  input.dataset.searchSelect = selectId;
  input.addEventListener('input', () => filterSelectOptions(input, select));
  cacheSelectOptions(select);
}

function resetSelectSearch(inputId, selectId) {
  const input = $(inputId);
  const select = $(selectId);
  if (input) input.value = '';
  if (input && select) filterSelectOptions(input, select);
}

function relatedEffectsForCharacter(charSlug) {
  const documents = [state.charData[charSlug], state.viCharacters[charSlug]].filter(Boolean);
  const serialized = normalizeReferenceText(JSON.stringify(documents));
  const explicitIds = new Set();
  const collectIds = value => {
    if (typeof value === 'string') {
      if (state.effects[value]) explicitIds.add(value);
      return;
    }
    if (Array.isArray(value)) return value.forEach(collectIds);
    if (value && typeof value === 'object') Object.values(value).forEach(collectIds);
  };
  documents.forEach(collectIds);
  return Object.entries(state.effects)
    .filter(([id, effect]) => {
      if (explicitIds.has(id)) return true;
      return [effect.name, effect.name_en]
        .filter(Boolean)
        .some(name => serialized.includes(normalizeReferenceText(name)));
    })
    .map(([id, effect]) => ({ id, ...effect }))
    .sort((a, b) => (a.name || a.name_en || '').localeCompare(b.name || b.name_en || '', 'vi'));
}

function effectInlineHTML(effectId) {
  const effect = state.effects[effectId];
  if (!effect) return '';
  const name = effect.name || effect.name_en || effectId;
  const description = effect.desc || effect.desc_en || '';
  const title = description ? `${name}: ${description}` : name;
  const type = effect.type || 'effect';
  return `<span class="guide-inline-ref guide-inline-effect effect-trigger effect-${escHTML(type)}" data-effect-id="${escHTML(effectId)}" data-effect="${escHTML(name)}" data-effect-en="${escHTML(effect.name_en || name)}" data-text-en="${escHTML(effect.name_en || name)}" data-type="${escHTML(type)}" data-desc="${escHTML(description)}" data-desc-en="${escHTML(effect.desc_en || description)}" title="${escHTML(title)}" tabindex="0">${escHTML(name)}</span>`;
}

function insertInlineReference(storedHTML) {
  if (!storedHTML) return;
  let target = editableSelection?.target?.isConnected ? editableSelection.target : null;
  if (!target) {
    addBlock({type:'paragraph', html:''});
    const editors = document.querySelectorAll('#blocks-list .rich-editor');
    target = editors[editors.length - 1];
    if (!target) return;
    const range = document.createRange();
    range.selectNodeContents(target);
    range.collapse(false);
    editableSelection = {target, range};
    restoreEditableSelection();
  }
  const template = document.createElement('template');
  template.innerHTML = `${toEditorHTML(window.GuideRichText.sanitizeRichHTML(storedHTML))}&nbsp;`;
  const fragment = template.content;
  const lastInsertedNode = fragment.lastChild;
  let range = editableSelection?.range?.cloneRange();
  if (!range || !target.contains(range.commonAncestorContainer)) {
    range = document.createRange();
    range.selectNodeContents(target);
    range.collapse(false);
  }
  range.deleteContents();
  range.insertNode(fragment);
  range.setStartAfter(lastInsertedNode);
  range.collapse(true);
  const selection = window.getSelection();
  selection.removeAllRanges();
  selection.addRange(range);
  editableSelection = {target, range: range.cloneRange()};
  syncRichEditor(target);
}

function rememberEditableSelection(event) {
  const rawTarget = event?.target || document.activeElement;
  const selection = window.getSelection();
  const anchorElement = selection?.anchorNode?.nodeType === Node.ELEMENT_NODE
    ? selection.anchorNode
    : selection?.anchorNode?.parentElement;
  const target = rawTarget?.closest?.('.rich-editor') || anchorElement?.closest?.('.rich-editor');
  if (!target || !selection?.rangeCount || !target.contains(selection.anchorNode)) return;
  editableSelection = { target, range: selection.getRangeAt(0).cloneRange() };
}

function restoreEditableSelection() {
  const selection = editableSelection;
  if (!selection?.target?.isConnected) {
    showToast('Hãy đặt con trỏ trong Paragraph hoặc ô Table.', 'err');
    return null;
  }
  selection.target.focus();
  const browserSelection = window.getSelection();
  browserSelection.removeAllRanges();
  browserSelection.addRange(selection.range);
  return selection.target;
}

function syncRichEditor(target) {
  target.dispatchEvent(new Event('input', { bubbles: true }));
  rememberEditableSelection({ target });
}

function applyRichTextCommand(command, value = null) {
  const target = restoreEditableSelection();
  if (!target) return;
  document.execCommand(command, false, value);
  syncRichEditor(target);
}

function applyClassFormat(className) {
  const target = restoreEditableSelection();
  if (!target) return;
  const selection = window.getSelection();
  if (!selection.rangeCount || selection.isCollapsed) {
    showToast('Hãy chọn văn bản cần định dạng.', 'err');
    return;
  }
  const range = selection.getRangeAt(0);
  const span = document.createElement('span');
  span.className = className;
  span.append(range.extractContents());
  range.insertNode(span);
  range.selectNodeContents(span);
  selection.removeAllRanges();
  selection.addRange(range);
  editableSelection = { target, range: range.cloneRange() };
  syncRichEditor(target);
}

function applyQuickFormat(prefix) {
  const commands = { '<b>': 'bold', '<i>': 'italic', '<u>': 'underline' };
  applyRichTextCommand(commands[prefix] || prefix);
}

function handleRichPaste(event) {
  event.preventDefault();
  const clipboard = event.clipboardData;
  const rich = clipboard?.getData('text/html');
  const html = rich
    ? window.GuideRichText.sanitizeRichHTML(rich)
    : window.GuideRichText.textToHTML(clipboard?.getData('text/plain') || '');
  document.execCommand('insertHTML', false, html);
  syncRichEditor(event.currentTarget);
}

function createRichEditor(initialHTML, onChange, extraClass = '') {
  const editor = el('div', {
    cls: `block-input rich-editor ${extraClass}`.trim(),
    contenteditable: 'true',
    role: 'textbox',
    'aria-multiline': 'true',
    'data-placeholder': 'Nhập và định dạng nội dung như Word…',
  });
  editor.innerHTML = toEditorHTML(window.GuideRichText.sanitizeRichHTML(initialHTML || ''));
  editor.addEventListener('input', () => {
    onChange(sanitizeStoredHTML(editor.innerHTML));
    requestAnimationFrame(() => rememberEditableSelection({ target: editor }));
  });
  editor.addEventListener('paste', handleRichPaste);
  editor.addEventListener('cut', () => {
    requestAnimationFrame(() => rememberEditableSelection({ target: editor }));
  });
  editor.addEventListener('blur', () => {
    const stored = sanitizeStoredHTML(editor.innerHTML);
    onChange(stored);
  });
  return editor;
}

function initQuickFormat() {
  const pane = $('editor-pane');
  ['focusin', 'select', 'keyup', 'mouseup', 'input'].forEach(eventName => {
    pane.addEventListener(eventName, rememberEditableSelection);
  });
  document.addEventListener('selectionchange', rememberEditableSelection);

  const preserveSelection = element => element.addEventListener('mousedown', event => event.preventDefault());
  const bindTagButton = (id, openTag) => {
    const button = $(id);
    preserveSelection(button);
    button.addEventListener('click', () => applyQuickFormat(openTag));
  };
  bindTagButton('fmt-bold', '<b>');
  bindTagButton('fmt-italic', '<i>');
  bindTagButton('fmt-underline', '<u>');

  const bindClassSelect = id => {
    const select = $(id);
    select.addEventListener('mousedown', () => rememberEditableSelection());
    select.addEventListener('change', () => {
      const className = select.value;
      if (className) applyClassFormat(className);
      select.value = '';
    });
  };
  bindClassSelect('fmt-font-size');
  bindClassSelect('fmt-text-color');
  bindClassSelect('fmt-highlight');

  const commandButtons = {
    'fmt-undo': 'undo',
    'fmt-redo': 'redo',
    'fmt-ul': 'insertUnorderedList',
    'fmt-ol': 'insertOrderedList',
    'fmt-clear': 'removeFormat',
  };
  Object.entries(commandButtons).forEach(([id, command]) => {
    preserveSelection($(id));
    $(id).addEventListener('click', () => applyRichTextCommand(command));
  });

  const alignButtons = {
    'fmt-align-left': 'guide-align-left',
    'fmt-align-center': 'guide-align-center',
    'fmt-align-right': 'guide-align-right',
  };
  Object.entries(alignButtons).forEach(([id, className]) => {
    preserveSelection($(id));
    $(id).addEventListener('click', () => applyClassFormat(className));
  });

  preserveSelection($('fmt-link'));
  $('fmt-link').addEventListener('click', () => {
    const target = restoreEditableSelection();
    if (!target || window.getSelection().isCollapsed) return;
    const href = window.prompt('Nhập URL liên kết:', 'https://');
    if (!href) return;
    if (!window.GuideRichText.isSafeHref(href)) {
      showToast('URL không an toàn hoặc không hợp lệ.', 'err');
      return;
    }
    applyRichTextCommand('createLink', href);
  });

  pane.addEventListener('keydown', event => {
    if (!event.ctrlKey || event.altKey || event.metaKey) return;
    const commands = {
      b: 'bold',
      i: 'italic',
      u: 'underline',
      z: event.shiftKey ? 'redo' : 'undo',
      y: 'redo',
    }[event.key.toLowerCase()];
    if (!commands) return;
    rememberEditableSelection(event);
    event.preventDefault();
    applyRichTextCommand(commands);
  });
}

// ── Data Loading ───────────────────────────────────────────────────────────
async function loadSearchIndex() {
  try {
    const res = await fetch('../../dist/search-index.json');
    if (!res.ok) throw new Error();
    const idx = await res.json();
    state.charList = idx.filter(e => e.category === 'doll').sort((a,b) => a.name.localeCompare(b.name));
    state.weaponList = idx.filter(e => e.category === 'weapon').sort((a,b) => a.name.localeCompare(b.name));
  } catch {
    showToast('Could not load search index — run build.py first', 'err', 5000);
  }
}

async function loadWeaponData() {
  try {
    const response = await fetch('../../data/weapons.json', { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    state.canonicalWeaponList = (Array.isArray(data) ? data : []).map(weapon => ({
      ...weapon,
      image: weapon.images?.weapon || weapon.image || '',
    }));
  } catch (error) {
    state.canonicalWeaponList = [];
    showToast(`Không tải được dữ liệu vũ khí gốc: ${error.message}`, 'err', 5000);
  }
}

function mergeCanonicalWeaponData() {
  const bySlug = new Map(state.weaponList.map(weapon => [weapon.slug, weapon]));
  state.canonicalWeaponList.forEach(weapon => {
    bySlug.set(weapon.slug, { ...(bySlug.get(weapon.slug) || {}), ...weapon });
  });
  state.weaponList = [...bySlug.values()].sort((a, b) => a.name.localeCompare(b.name));
}

async function loadVietnameseData() {
  try {
    const response = await fetch('../../data/i18n_vi.json', { cache: 'no-store' });
    if (!response.ok) throw new Error(`HTTP ${response.status}`);
    const data = await response.json();
    state.viCharacters = data.characters || {};
    state.viWeapons = data.weapons || {};
    state.effects = data.effects || {};
  } catch (error) {
    state.viCharacters = {};
    state.viWeapons = {};
    state.effects = {};
    showToast(`Không tải được dữ liệu tiếng Việt: ${error.message}`, 'err', 5000);
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

  populateWeaponPicker();
  ['modal-skill-char', 'modal-char-card-sel'].forEach(cacheSelectOptions);
}

function signatureWeaponForCharacter(charSlug) {
  if (!charSlug) return null;
  const source = state.charData[charSlug] || {};
  const localizedCharacter = state.viCharacters[charSlug] || {};
  const expectedNames = [source.signature_weapon, localizedCharacter.signature_weapon]
    .filter(Boolean)
    .map(normalizeSearchText);
  return state.weaponList.find(weapon => {
    const localized = localizedWeapon(weapon.slug);
    return [weapon.name, localized.name, localized.en_name]
      .filter(Boolean)
      .some(name => expectedNames.includes(normalizeSearchText(name)));
  }) || null;
}

function populateWeaponPicker(charSlug = state.charSlug || $('char-sel')?.value) {
  const wSel = $('modal-weapon-card-sel');
  wSel.innerHTML = '<option value="">— Select weapon —</option>';
  const signature = signatureWeaponForCharacter(charSlug);
  const weapons = signature
    ? [signature, ...state.weaponList.filter(weapon => weapon.slug !== signature.slug)]
    : state.weaponList;
  weapons.forEach(w => {
    const localized = localizedWeapon(w.slug);
    const aliases = localized.en_name && localized.en_name !== localized.name ? ` / ${localized.en_name}` : '';
    const badge = signature?.slug === w.slug ? '★ Vũ khí đặc trưng — ' : '';
    wSel.append(el('option', {value: w.slug}, `${badge}${localized.name || w.name}${aliases} (${w.rarity || ''})`));
  });
  cacheSelectOptions(wSel);
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

function duplicateBlock(id) {
  const idx = state.blocks.findIndex(b => b.id === id);
  if (idx < 0) return;
  const copy = JSON.parse(JSON.stringify(state.blocks[idx]));
  copy.id = `block-${++blockCounter}`;
  state.blocks.splice(idx + 1, 0, copy);
  const list = $('blocks-list');
  list.innerHTML = '';
  state.blocks.forEach(b => renderBlockItem(b));
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

function reorderBlock(sourceId, targetId, placeAfter = false) {
  if (!sourceId || sourceId === targetId) return;
  const sourceIndex = state.blocks.findIndex(block => block.id === sourceId);
  const targetIndex = state.blocks.findIndex(block => block.id === targetId);
  if (sourceIndex < 0 || targetIndex < 0) return;
  const [block] = state.blocks.splice(sourceIndex, 1);
  let insertIndex = state.blocks.findIndex(candidate => candidate.id === targetId);
  if (placeAfter) insertIndex += 1;
  state.blocks.splice(insertIndex, 0, block);
  const list = $('blocks-list');
  list.innerHTML = '';
  state.blocks.forEach(item => renderBlockItem(item));
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
    el('button', {cls: 'block-action-btn', title: 'Nhân đôi khối', onclick: () => duplicateBlock(id)}, '⧉'),
    el('button', {cls: 'block-action-btn danger', onclick: () => removeBlock(id)}, '✕')
  );
  return row;
}

function blockHandle() {
  const h = el('div', {cls: 'block-handle', draggable: 'true', title: 'Kéo để đổi vị trí khối'});
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
  const handle = blockHandle();
  handle.addEventListener('dragstart', event => {
    draggedBlockId = b.id;
    item.classList.add('is-dragging');
    event.dataTransfer.effectAllowed = 'move';
    event.dataTransfer.setData('text/plain', b.id);
  });
  handle.addEventListener('dragend', () => {
    draggedBlockId = null;
    document.querySelectorAll('.block-item').forEach(block => block.classList.remove('is-dragging', 'drag-before', 'drag-after'));
  });
  item.addEventListener('dragover', event => {
    if (!draggedBlockId || draggedBlockId === b.id) return;
    event.preventDefault();
    const after = event.clientY > item.getBoundingClientRect().top + item.offsetHeight / 2;
    item.classList.toggle('drag-before', !after);
    item.classList.toggle('drag-after', after);
  });
  item.addEventListener('dragleave', () => item.classList.remove('drag-before', 'drag-after'));
  item.addEventListener('drop', event => {
    event.preventDefault();
    const sourceId = draggedBlockId || event.dataTransfer.getData('text/plain');
    const after = event.clientY > item.getBoundingClientRect().top + item.offsetHeight / 2;
    item.classList.remove('drag-before', 'drag-after');
    reorderBlock(sourceId, b.id, after);
  });
  item.append(handle);
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
  const editor = createRichEditor(b.html, html => { b.html = html; renderPreview(); });
  return wrapBlock(b, '¶ Paragraph', editor);
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
      const localized = localizedSkill(slug, idx);
      const o = el('option', {value:idx}, `Kỹ năng ${idx+1}: ${localized?.name || sk.name}`);
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
      const localizedSummon = state.viCharacters[slug]?.summons?.[idx];
      const o = el('option', {value:idx}, localizedSummon?.name || sm.name || `Triệu hồi ${idx+1}`);
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
      const localized = localizedSkill(slug, idx, sumIdx);
      const o = el('option', {value:idx}, localized?.name || sk.name || `Kỹ năng ${idx+1}`);
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

function normalizeTableColumnWidths(block) {
  const source = Array.isArray(block.column_widths) ? block.column_widths : [];
  block.column_widths = block.headers.map((_, index) => {
    const width = Number(source[index]);
    return Number.isFinite(width) ? Math.max(80, Math.min(1200, Math.round(width))) : 180;
  });
  return block.column_widths;
}

function renderTableBlock(b) {
  if (!b.headers?.length) { b.headers = ['Column 1']; b.rows = [['']]; }
  normalizeTableColumnWidths(b);
  const wrapper = el('div', {cls:'table-editor'});

  function rebuildTable() {
    wrapper.innerHTML = '';
    const table = el('table');
    const widths = normalizeTableColumnWidths(b);
    const colgroup = el('colgroup');
    widths.forEach(width => colgroup.append(el('col', {style:`width:${width}px`})));
    table.style.width = `${widths.reduce((sum, width) => sum + width, 0)}px`;
    table.append(colgroup);
    // Header row
    const thead = el('thead'); const trh = el('tr');
    b.headers.forEach((h, ci) => {
      const th = el('th');
      const inp = el('input', {type:'text', value:h, placeholder:`Col ${ci+1}`});
      inp.addEventListener('input', () => { b.headers[ci] = inp.value; renderPreview(); });
      const resizeHandle = el('span', {
        cls:'table-column-resize-handle',
        title:'Kéo để chỉnh chiều rộng cột',
        role:'separator',
        'aria-orientation':'vertical',
      });
      resizeHandle.addEventListener('pointerdown', event => {
        event.preventDefault();
        event.stopPropagation();
        const startX = event.clientX;
        const startWidth = b.column_widths[ci];
        resizeHandle.setPointerCapture?.(event.pointerId);
        resizeHandle.classList.add('is-resizing');
        const updateWidth = moveEvent => {
          const width = Math.max(80, Math.min(1200, Math.round(startWidth + moveEvent.clientX - startX)));
          b.column_widths[ci] = width;
          colgroup.children[ci].style.width = `${width}px`;
          table.style.width = `${b.column_widths.reduce((sum, value) => sum + value, 0)}px`;
          renderPreview();
        };
        const finishResize = () => {
          resizeHandle.classList.remove('is-resizing');
          resizeHandle.removeEventListener('pointermove', updateWidth);
          resizeHandle.removeEventListener('pointerup', finishResize);
          resizeHandle.removeEventListener('pointercancel', finishResize);
        };
        resizeHandle.addEventListener('pointermove', updateWidth);
        resizeHandle.addEventListener('pointerup', finishResize);
        resizeHandle.addEventListener('pointercancel', finishResize);
      });
      th.append(inp, resizeHandle); trh.append(th);
    });
    thead.append(trh); table.append(thead);
    // Data rows
    const tbody = el('tbody');
    b.rows.forEach((row, ri) => {
      const tr = el('tr');
      b.headers.forEach((_, ci) => {
        const td = el('td');
        const editor = createRichEditor(row[ci] || '', html => {
          b.rows[ri][ci] = html;
          renderPreview();
        }, 'table-cell-editor');
        td.append(editor); tr.append(td);
      });
      tbody.append(tr);
    });
    table.append(tbody);
    wrapper.append(table);

    const ctrl = el('div', {cls:'table-controls'});
    const btnAddCol = el('button', {cls:'btn btn-secondary', style:'font-size:0.72rem;padding:3px 8px', type:'button'}, '+ Col');
    btnAddCol.addEventListener('click', () => { b.headers.push(`Col ${b.headers.length+1}`); b.column_widths.push(180); b.rows.forEach(r => r.push('')); rebuildTable(); renderPreview(); });
    const btnAddRow = el('button', {cls:'btn btn-secondary', style:'font-size:0.72rem;padding:3px 8px', type:'button'}, '+ Row');
    btnAddRow.addEventListener('click', () => { b.rows.push(b.headers.map(()=>'')); rebuildTable(); renderPreview(); });
    const btnDelCol = el('button', {cls:'btn btn-secondary', style:'font-size:0.72rem;padding:3px 8px', type:'button'}, '- Col');
    btnDelCol.addEventListener('click', () => { if(b.headers.length<=1) return; b.headers.pop(); b.column_widths.pop(); b.rows.forEach(r=>r.pop()); rebuildTable(); renderPreview(); });
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
      return `<div class="guide-paragraph">${toEditorHTML(window.GuideRichText.sanitizeRichHTML(b.html || ''))}</div>`;
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
      const imgSrc = wp?.image ? `../../${wp.image}` : `../../assets/images/weapons/${name}.png`;
      return `<div class="preview-weapon-card">
        <img src="${escHTML(imgSrc)}" onerror="this.style.display='none'" alt="${escHTML(name)}" />
        ${escHTML(name)}
      </div><br>`;
    }
    case 'skill_ref': {
      if (!b.char || b.skill_idx == null) return '';
      const sk = localizedSkill(b.char, b.skill_idx);
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
      const sk = localizedSkill(b.char, b.skill_idx, b.summon_idx);
      if (!sk) return `<span class="preview-skill-chip">🤖 Summon Skill (loading…)</span>`;
      const icon = sk.icon ? `<img src="../../${escHTML(sk.icon)}" />` : '';
      const desc = escHTML(sk.description || '').slice(0, 200);
      const summonName = state.viCharacters[b.char]?.summons?.[b.summon_idx]?.name
        || state.charData[b.char]?.summons?.[b.summon_idx]?.name || '';
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
      const widths = normalizeTableColumnWidths(b);
      const tableWidth = widths.reduce((sum, width) => sum + width, 0);
      const colgroup = `<colgroup>${widths.map(width => `<col style="width:${width}px">`).join('')}</colgroup>`;
      const headers = b.headers.map(h => `<th>${escHTML(h)}</th>`).join('');
      const rows = (b.rows || []).map(r =>
        `<tr>${b.headers.map((_,i) => `<td>${toEditorHTML(window.GuideRichText.sanitizeRichHTML(r[i] || ''))}</td>`).join('')}</tr>`
      ).join('');
      return `<div class="guide-table-scroll"><table class="preview-table" style="width:${tableWidth}px;min-width:100%;table-layout:fixed">${colgroup}<thead><tr>${headers}</tr></thead><tbody>${rows}</tbody></table></div>`;
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
// ── Modal Helpers ──────────────────────────────────────────────────────────
function openModal(id) { $(id).style.display = 'flex'; }
function closeModal(id) { $(id).style.display = 'none'; }

function modalOk(modalId, onOk) {
  const id = `modal-${modalId}`;
  $(`modal-${modalId}-ok`)?.addEventListener('click', () => { closeModal(id); onOk(); });
  $(`modal-${modalId}-cancel`)?.addEventListener('click', () => closeModal(id));
}

// ── Toolbar Handlers ───────────────────────────────────────────────────────
function preserveInlineSelection(event) {
  rememberEditableSelection();
  event.preventDefault();
}

function initToolbar() {
  ['tb-char-card', 'tb-weapon-card', 'tb-skill-ref', 'tb-summon-ref', 'tb-effect-ref'].forEach(id => {
    $(id).addEventListener('mousedown', preserveInlineSelection);
  });

  $('tb-heading').addEventListener('click', () => {
    $('modal-heading-text').value = '';
    openModal('modal-heading');
    setTimeout(() => $('modal-heading-text').focus(), 50);
  });

  $('tb-paragraph').addEventListener('click', () => {
    addBlock({type:'paragraph', html:''});
  });

  $('tb-char-card').addEventListener('click', () => {
    resetSelectSearch('modal-char-card-search', 'modal-char-card-sel');
    openModal('modal-char-card');
  });

  $('tb-weapon-card').addEventListener('click', async () => {
    const charSlug = state.charSlug || $('char-sel').value;
    if (charSlug) await loadCharData(charSlug);
    populateWeaponPicker(charSlug);
    resetSelectSearch('modal-weapon-card-search', 'modal-weapon-card-sel');
    openModal('modal-weapon-card');
  });

  $('tb-skill-ref').addEventListener('click', async () => {
    $('modal-skill-title').textContent = '⚡ Chèn kỹ năng tiếng Việt';
    $('modal-skill-summon-field').style.display = 'none';
    $('modal-skill-label').textContent = 'Kỹ năng';
    const defaultSlug = state.charSlug || $('char-sel').value;
    resetSelectSearch('modal-skill-char-search', 'modal-skill-char');
    resetSelectSearch('modal-skill-pick-search', 'modal-skill-pick');
    $('modal-skill-char').value = defaultSlug;
    $('modal-skill-pick').innerHTML = '<option value="">— Kỹ năng —</option>';
    openModal('modal-skill');
    const charSel = $('modal-skill-char');
    const refreshSkills = async () => {
      const skillSel = $('modal-skill-pick');
      skillSel.innerHTML = '<option value="">— Kỹ năng —</option>';
      const data = await loadCharData(charSel.value);
      (data?.skills || []).forEach((sk, i) => {
        const localized = localizedSkill(charSel.value, i);
        skillSel.append(el('option', {value:i}, `${i+1}. ${localized?.name || sk.name}`));
      });
      cacheSelectOptions(skillSel);
    };
    charSel.onchange = refreshSkills;
    await refreshSkills();
  });

  $('tb-summon-ref').addEventListener('click', () => {
    $('modal-skill-title').textContent = '🤖 Chèn kỹ năng triệu hồi tiếng Việt';
    $('modal-skill-summon-field').style.display = 'block';
    $('modal-skill-label').textContent = 'Summon Skill';
    $('modal-skill-char').value = '';
    $('modal-skill-summon').innerHTML = '<option value="">— Summon —</option>';
    $('modal-skill-pick').innerHTML = '<option value="">— Skill —</option>';
    resetSelectSearch('modal-skill-char-search', 'modal-skill-char');
    resetSelectSearch('modal-skill-summon-search', 'modal-skill-summon');
    resetSelectSearch('modal-skill-pick-search', 'modal-skill-pick');
    openModal('modal-skill');

    const charSel = $('modal-skill-char');
    const summonSel = $('modal-skill-summon');
    const skillSel = $('modal-skill-pick');

    charSel.onchange = async () => {
      summonSel.innerHTML = '<option value="">— Summon —</option>';
      skillSel.innerHTML = '<option value="">— Skill —</option>';
      const data = await loadCharData(charSel.value);
      (data?.summons || []).forEach((sm, i) => {
        const localizedSummon = state.viCharacters[charSel.value]?.summons?.[i];
        summonSel.append(el('option', {value:i}, localizedSummon?.name || sm.name || `Triệu hồi ${i+1}`));
      });
      cacheSelectOptions(summonSel);
      cacheSelectOptions(skillSel);
    };
    summonSel.onchange = async () => {
      skillSel.innerHTML = '<option value="">— Skill —</option>';
      const data = await loadCharData(charSel.value);
      const summon = data?.summons?.[+summonSel.value];
      (summon?.skills || []).forEach((sk, i) => {
        const localized = localizedSkill(charSel.value, i, +summonSel.value);
        skillSel.append(el('option', {value:i}, localized?.name || sk.name || `Kỹ năng ${i+1}`));
      });
      cacheSelectOptions(skillSel);
    };
  });

  $('tb-effect-ref').addEventListener('click', async () => {
    const charSlug = state.charSlug || $('char-sel').value;
    if (!charSlug) {
      showToast('Hãy chọn nhân vật đang làm guide trước.', 'err');
      return;
    }
    await loadCharData(charSlug);
    const effects = relatedEffectsForCharacter(charSlug);
    const picker = $('modal-effect-pick');
    picker.innerHTML = '<option value="">— Chọn hiệu ứng liên quan —</option>';
    effects.forEach(effect => {
      picker.append(el('option', {value: effect.id}, `${effect.name || effect.name_en} (${effect.type || 'effect'})`));
    });
    const character = state.viCharacters[charSlug] || state.charList.find(item => item.slug === charSlug);
    $('modal-effect-title').textContent = `✦ Hiệu ứng liên quan: ${character?.name || charSlug}`;
    if (!effects.length) {
      picker.innerHTML = '<option value="">Không tìm thấy hiệu ứng liên quan</option>';
    }
    cacheSelectOptions(picker);
    resetSelectSearch('modal-effect-search', 'modal-effect-pick');
    openModal('modal-effect');
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
      insertInlineReference(skillInlineHTML(charSlug, +skillIdx, +summonIdx));
    } else {
      const skillIdx = $('modal-skill-pick').value;
      if (skillIdx === '') return;
      insertInlineReference(skillInlineHTML(charSlug, +skillIdx));
    }
    closeModal('modal-skill');
  });
  $('modal-skill-cancel').addEventListener('click', () => closeModal('modal-skill'));

  $('modal-effect-ok').addEventListener('click', () => {
    const effectId = $('modal-effect-pick').value;
    if (!effectId) return;
    insertInlineReference(effectInlineHTML(effectId));
    closeModal('modal-effect');
  });
  $('modal-effect-cancel').addEventListener('click', () => closeModal('modal-effect'));

  // Char card modal
  $('modal-char-card-ok').addEventListener('click', () => {
    const slug = $('modal-char-card-sel').value;
    if (!slug) return;
    insertInlineReference(characterInlineHTML(slug));
    closeModal('modal-char-card');
  });
  $('modal-char-card-cancel').addEventListener('click', () => closeModal('modal-char-card'));

  // Weapon card modal
  $('modal-weapon-card-ok').addEventListener('click', () => {
    const slug = $('modal-weapon-card-sel').value;
    if (!slug) return;
    insertInlineReference(weaponInlineHTML(slug));
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

// ── Guide File Operations & Server Sync ─────────────────────────────────────
function exportGuideObject() {
  const slug = state.charSlug || $('char-sel').value.trim();
  const title = $('guide-title').value.trim();
  const cleanBlocks = state.blocks.map(({ id, _objectUrl, ...rest }) => rest);
  cleanBlocks.forEach(block => {
    if (block.type === 'paragraph') {
      block.html = window.GuideRichText.sanitizeRichHTML(block.html || '');
    } else if (block.type === 'table') {
      block.rows = (block.rows || []).map(row =>
        row.map(cell => window.GuideRichText.sanitizeRichHTML(cell || ''))
      );
    }
  });
  return {
    slug,
    char_slug: slug,
    title: title || (slug ? `${slug} Guide` : 'Guide'),
    last_updated: $('guide-date').value || new Date().toISOString().slice(0, 10),
    author: $('guide-author').value.trim() || 'Community',
    blocks: cleanBlocks,
  };
}

async function loadExistingGuide() {
  const slug = $('char-sel').value.trim();
  if (!slug) {
    showToast('Hãy chọn nhân vật trước khi mở guide.', 'err');
    return;
  }
  const btn = $('btn-load-existing');
  btn.disabled = true;
  btn.textContent = 'Đang mở…';
  try {
    const resp = await fetch(`/api/guides/${encodeURIComponent(slug)}`, { cache: 'no-store' });
    const data = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      throw new Error(resp.status === 404 ? 'Nhân vật chưa có guide.' : (data.error || `HTTP ${resp.status}`));
    }
    applyLoadedGuide(data);
    showToast(`Đã mở guide ${slug}.`, 'ok');
  } catch (err) {
    showToast(`Không thể mở guide: ${err.message}`, 'err', 4500);
  } finally {
    btn.disabled = false;
    btn.textContent = 'Mở guide nhân vật';
  }
}

function useLoreleyTemplate() {
  const slug = $('char-sel').value.trim();
  if (!slug) {
    showToast('Hãy chọn nhân vật trước khi tạo mẫu.', 'err');
    return;
  }
  if (!window.GuideTemplate?.createLoreleyStyleGuide) {
    showToast('Không tải được mẫu Loreley.', 'err');
    return;
  }
  if (state.blocks.length && !window.confirm('Thay toàn bộ nội dung hiện tại bằng mẫu Loreley?')) return;
  const character = state.charList.find(item => item.slug === slug);
  const guide = window.GuideTemplate.createLoreleyStyleGuide({
    slug,
    name: character?.name || slug,
    date: $('guide-date').value || new Date().toISOString().slice(0, 10),
    author: $('guide-author').value.trim() || 'Community',
  });
  applyLoadedGuide(guide);
  showToast(`Đã tạo mẫu guide cho ${character?.name || slug}.`, 'ok');
}

function downloadGuide() {
  const guide = exportGuideObject();
  if (!guide.slug) {
    showToast('Hãy chọn một nhân vật trước khi tải tệp JSON.', 'err');
    return;
  }
  const json = JSON.stringify(guide, null, 2);
  const blob = new Blob([json], { type: 'application/json;charset=utf-8' });
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = `${guide.slug}.json`;
  a.click();
  URL.revokeObjectURL(url);
  showToast(`Đã tải về tệp ${guide.slug}.json`, 'ok');
}

async function saveGuide() {
  const guide = exportGuideObject();
  if (!guide.slug) {
    showToast('Hãy chọn một nhân vật cho guide trước khi lưu.', 'err');
    return;
  }
  const btn = $('btn-save-guide');
  btn.disabled = true;
  btn.textContent = 'Đang lưu…';

  try {
    let resp = await fetch(`/api/guides/${encodeURIComponent(guide.slug)}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(guide),
    });

    if (resp.status === 404) {
      // Guide chưa tồn tại, gọi POST /api/guides để tạo mới
      resp = await fetch('/api/guides', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(guide),
      });
    }

    const result = await resp.json().catch(() => ({}));
    if (!resp.ok) {
      throw new Error(result.error || `HTTP ${resp.status}`);
    }
    showToast(`Đã cập nhật JSON gốc: data/guides/${guide.slug}.json`, 'ok', 4000);
  } catch (err) {
    showToast(`Lưu guide thất bại: ${err.message}`, 'err', 5000);
  } finally {
    btn.disabled = false;
    btn.textContent = '💾 Cập nhật JSON gốc';
  }
}

function loadGuide(e) {
  const file = e.target.files?.[0];
  if (!file) return;
  const reader = new FileReader();
  reader.onload = () => {
    try {
      const data = JSON.parse(reader.result);
      applyLoadedGuide(data);
      showToast(`Đã nạp guide từ tệp ${file.name}`, 'ok');
    } catch (err) {
      showToast(`Tệp JSON không hợp lệ: ${err.message}`, 'err');
    } finally {
      $('file-load-guide').value = '';
    }
  };
  reader.readAsText(file);
}

function applyLoadedGuide(data) {
  if (!data || typeof data !== 'object') return;
  const charSlug = data.char_slug || data.slug || '';
  if (charSlug) {
    state.charSlug = charSlug;
    $('char-sel').value = charSlug;
  }
  if (data.title) {
    state.title = data.title;
    $('guide-title').value = data.title;
  }
  state.author = data.author || 'Community';
  state.lastUpdated = data.last_updated || new Date().toISOString().slice(0, 10);
  $('guide-author').value = state.author;
  $('guide-date').value = state.lastUpdated;
  state.blocks = [];
  blockCounter = 0;
  if (Array.isArray(data.blocks)) {
    data.blocks.forEach((b) => {
      blockCounter++;
      state.blocks.push({ ...b, id: `block-${blockCounter}` });
    });
  }
  const list = $('blocks-list');
  list.innerHTML = '';
  state.blocks.forEach((b) => renderBlockItem(b));
  updateEmptyState();
  renderPreview();
}

async function checkGuideEditorServerGate() {
  const banner = $('server-gate-banner');
  const btnSave = $('btn-save-guide');
  try {
    const resp = await fetch('/api/health', { cache: 'no-store' });
    const contentType = resp.headers.get('Content-Type') || '';
    if (!resp.ok || !contentType.includes('application/json')) {
      throw new Error('Not editor server');
    }
    const data = await resp.json();
    if (data.service !== 'gfl2-editor-server' || !data.capabilities?.includes('guides')) {
      throw new Error('Server thiếu capability guides');
    }
    if (banner) banner.style.display = 'none';
    if (btnSave) btnSave.disabled = false;
  } catch (err) {
    if (banner) {
      banner.style.display = 'block';
      banner.innerHTML = `
        <div style="background: rgba(248, 81, 73, 0.15); border: 1px solid #f85149; color: #ff7b72; padding: 12px 16px; border-radius: 8px; margin: 12px 1.5rem 0; font-size: 14px; line-height: 1.5;">
          <strong>⚠️ Cảnh báo kết nối:</strong> Không thể kết nối tới Editor Server (có thể đang mở từ static server).<br>
          Nút "Cập nhật JSON gốc" đã bị khóa. Bạn vẫn có thể dùng nút "Tải tệp JSON" để lưu về máy. Để kích hoạt cập nhật trực tiếp, hãy chạy lệnh:
          <div style="margin-top: 6px;"><code style="background: rgba(0,0,0,0.5); padding: 3px 6px; border-radius: 4px; font-family: monospace;">.venv\\Scripts\\python.exe tools\\start_editors.py</code></div>
        </div>
      `;
    }
    if (btnSave) {
      btnSave.disabled = true;
      btnSave.title = 'Vui lòng chạy tools/start_editors.py để cập nhật JSON gốc.';
    }
  }
}

// ── Boot ───────────────────────────────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async () => {
  await Promise.all([loadSearchIndex(), loadVietnameseData(), loadWeaponData()]);
  mergeCanonicalWeaponData();
  populateAllSelectors();
  [
    ['modal-char-card-search', 'modal-char-card-sel'],
    ['modal-weapon-card-search', 'modal-weapon-card-sel'],
    ['modal-skill-char-search', 'modal-skill-char'],
    ['modal-skill-summon-search', 'modal-skill-summon'],
    ['modal-skill-pick-search', 'modal-skill-pick'],
    ['modal-effect-search', 'modal-effect-pick'],
  ].forEach(([inputId, selectId]) => bindSelectSearch(inputId, selectId));
  initToolbar();
  initModals();
  initQuickFormat();

  $('btn-save-guide').addEventListener('click', saveGuide);
  $('btn-load-existing').addEventListener('click', loadExistingGuide);
  $('btn-use-template').addEventListener('click', useLoreleyTemplate);
  $('btn-download-guide').addEventListener('click', downloadGuide);
  $('btn-load-guide').addEventListener('click', () => $('file-load-guide').click());
  $('file-load-guide').addEventListener('change', loadGuide);
  $('guide-title').addEventListener('input', renderPreview);
  $('guide-author').value = state.author;
  $('guide-date').value = new Date().toISOString().slice(0, 10);
  $('char-sel').addEventListener('change', async () => {
    state.charSlug = $('char-sel').value;
    if (state.charSlug) await loadCharData(state.charSlug);
    populateWeaponPicker(state.charSlug);
    renderPreview();
  });

  updateEmptyState();
  renderPreview();
  checkGuideEditorServerGate();
});
