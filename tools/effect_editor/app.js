(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const state = { effects: [], selected: null, dirty: false };

  function toast(message, error = false) {
    const node = $('toast');
    node.textContent = message;
    node.className = error ? 'show error' : 'show';
    clearTimeout(toast.timer);
    toast.timer = setTimeout(() => { node.className = ''; }, 3200);
  }

  function setDirty(dirty) {
    state.dirty = dirty;
    $('save').disabled = !dirty || !state.selected;
    $('save-state').textContent = dirty ? 'Có thay đổi chưa lưu' : 'Đã đồng bộ';
    $('save-state').classList.toggle('dirty', dirty);
  }

  function filteredEffects() {
    const query = $('search').value.trim().toLocaleLowerCase('vi');
    if (!query) return state.effects;
    return state.effects.filter((effect) =>
      `${effect.name_en} ${effect.name} ${effect.desc} ${effect.desc_en}`
        .toLocaleLowerCase('vi').includes(query)
    );
  }

  function renderList() {
    const effects = filteredEffects();
    $('count').textContent = `${effects.length}/${state.effects.length} hiệu ứng`;
    const list = $('effect-list');
    list.replaceChildren(...effects.map((effect) => {
      const button = document.createElement('button');
      button.type = 'button';
      button.className = effect.id === state.selected?.id ? 'effect-row active' : 'effect-row';
      button.innerHTML = `<strong></strong><span></span>`;
      button.querySelector('strong').textContent = effect.name_en;
      button.querySelector('span').textContent = effect.name;
      button.addEventListener('click', () => selectEffect(effect));
      return button;
    }));
  }

  function renderChips(id, items, emptyText) {
    const root = $(id);
    root.replaceChildren();
    if (!items.length) {
      const empty = document.createElement('span');
      empty.className = 'muted';
      empty.textContent = emptyText;
      root.append(empty);
      return;
    }
    items.forEach((item) => {
      const chip = document.createElement('button');
      chip.type = 'button';
      chip.className = 'chip';
      const targetId = typeof item === 'string' ? item : item.id;
      const target = state.effects.find((effect) => effect.id === targetId);
      const fallback = typeof item === 'string' ? item : item.name_en;
      chip.textContent = target ? `${target.name} · ${target.name_en}` : fallback;
      chip.addEventListener('click', () => target && selectEffect(target));
      root.append(chip);
    });
  }

  function selectEffect(effect) {
    if (state.dirty && !window.confirm('Bỏ thay đổi chưa lưu?')) return;
    state.selected = effect;
    $('name-en').value = effect.name_en;
    $('desc-en').value = effect.desc_en || '';
    $('name-vi').value = effect.name || '';
    $('desc-vi').value = effect.desc || '';
    $('effect-type').value = effect.type || 'effect';
    renderChips('sub-effects', effect.sub_effect_ids || [], 'Không có');
    renderChips('referenced-by', effect.referenced_by || [], 'Không có');
    $('workspace').hidden = false;
    $('empty-state').hidden = true;
    setDirty(false);
    renderList();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  async function loadEffects(selectId = null) {
    const response = await fetch('/api/effects', { cache: 'no-store' });
    const payload = await response.json();
    if (!response.ok) throw new Error(payload.error || 'Không thể tải dữ liệu.');
    state.effects = payload.effects;
    renderList();
    if (selectId) {
      const selected = state.effects.find((effect) => effect.id === selectId);
      if (selected) selectEffect(selected);
    }
  }

  async function save() {
    if (!state.selected || !state.dirty) return;
    $('save').disabled = true;
    $('save-state').textContent = 'Đang lưu…';
    try {
      const response = await fetch(`/api/effects/${encodeURIComponent(state.selected.id)}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: $('name-vi').value,
          desc: $('desc-vi').value,
          type: $('effect-type').value,
        }),
      });
      const payload = await response.json();
      if (!response.ok) throw new Error(payload.error || 'Không thể lưu dữ liệu.');
      const effectId = state.selected.id;
      await loadEffects(effectId);
      toast(`Đã lưu. Bảo toàn ${payload.preserved_references} chỉ mục liên quan bằng ID.`);
    } catch (error) {
      setDirty(true);
      toast(error.message, true);
    }
  }

  ['name-vi', 'desc-vi', 'effect-type'].forEach((id) => {
    $(id).addEventListener('input', () => setDirty(true));
    $(id).addEventListener('change', () => setDirty(true));
  });
  $('search').addEventListener('input', renderList);
  $('save').addEventListener('click', save);
  document.addEventListener('keydown', (event) => {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 's') {
      event.preventDefault();
      save();
    }
  });
  window.addEventListener('beforeunload', (event) => {
    if (!state.dirty) return;
    event.preventDefault();
    event.returnValue = '';
  });

  loadEffects().catch((error) => toast(error.message, true));
})();
