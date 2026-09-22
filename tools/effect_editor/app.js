import { setupServerGate, requestJson } from '../shared/editor-api.js';

(() => {
  'use strict';

  const $ = (id) => document.getElementById(id);
  const state = {
    effects: [],
    selected: null,
    selectedSubEffects: [],
    dirty: false,
  };

  function toast(message, error = false) {
    const node = $('toast');
    node.textContent = message;
    node.className = error ? 'show error' : 'show';
    clearTimeout(toast.timer);
    toast.timer = setTimeout(() => {
      node.className = '';
    }, 3200);
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
        .toLocaleLowerCase('vi')
        .includes(query)
    );
  }

  function renderList() {
    const effects = filteredEffects();
    $('count').textContent = `${effects.length}/${state.effects.length} hiệu ứng`;
    const list = $('effect-list');
    list.replaceChildren(
      ...effects.map((effect) => {
        const button = document.createElement('button');
        button.type = 'button';
        button.className = effect.id === state.selected?.id ? 'effect-row active' : 'effect-row';
        button.innerHTML = `<strong></strong><span></span>`;
        button.querySelector('strong').textContent = effect.name_en;
        button.querySelector('span').textContent = effect.name;
        button.addEventListener('click', () => selectEffect(effect));
        return button;
      })
    );
  }

  function renderSubEffectChips() {
    const root = $('sub-effects');
    root.replaceChildren();

    if (!state.selectedSubEffects.length) {
      const empty = document.createElement('span');
      empty.className = 'muted';
      empty.textContent = 'Không có hiệu ứng con';
      root.append(empty);
      return;
    }

    state.selectedSubEffects.forEach((subId) => {
      const target = state.effects.find((e) => e.id === subId);
      const chip = document.createElement('span');
      chip.className = 'chip';

      const label = document.createElement('span');
      label.className = 'chip-label';
      label.textContent = target ? `${target.name} · ${target.name_en}` : subId;
      label.title = 'Xem hiệu ứng này';
      label.addEventListener('click', () => {
        if (target) selectEffect(target);
      });

      const removeBtn = document.createElement('button');
      removeBtn.type = 'button';
      removeBtn.className = 'chip-remove';
      removeBtn.innerHTML = '&times;';
      removeBtn.title = 'Gỡ bỏ hiệu ứng con này';
      removeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        state.selectedSubEffects = state.selectedSubEffects.filter((id) => id !== subId);
        renderSubEffectChips();
        setDirty(true);
      });

      chip.append(label, removeBtn);
      root.append(chip);
    });
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
    state.selectedSubEffects = [...(effect.sub_effect_ids || [])];

    $('name-en').value = effect.name_en;
    $('desc-en').value = effect.desc_en || '';
    $('name-vi').value = effect.name || '';
    $('desc-vi').value = effect.desc || '';
    $('effect-type').value = effect.type || 'effect';

    renderSubEffectChips();
    renderChips('referenced-by', effect.referenced_by || [], 'Không có');
    $('workspace').hidden = false;
    $('empty-state').hidden = true;
    setDirty(false);
    renderList();
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  // --- Sub-effect Picker Dialog ---

  function openSubEffectPicker() {
    if (!state.selected) return;
    $('picker-search').value = '';
    renderPickerList();
    $('sub-effect-picker').hidden = false;
    $('picker-search').focus();
  }

  function closeSubEffectPicker() {
    $('sub-effect-picker').hidden = true;
  }

  function renderPickerList() {
    const query = $('picker-search').value.trim().toLocaleLowerCase('vi');
    const container = $('picker-list');
    container.replaceChildren();

    const candidates = state.effects.filter(
      (effect) =>
        effect.id !== state.selected?.id &&
        !state.selectedSubEffects.includes(effect.id) &&
        (!query ||
          `${effect.name_en} ${effect.name}`.toLocaleLowerCase('vi').includes(query))
    );

    if (!candidates.length) {
      const empty = document.createElement('div');
      empty.className = 'muted';
      empty.style.padding = '12px';
      empty.textContent = 'Không tìm thấy hiệu ứng phù hợp.';
      container.append(empty);
      return;
    }

    candidates.forEach((effect) => {
      const item = document.createElement('button');
      item.type = 'button';
      item.className = 'picker-item';
      item.innerHTML = `<strong></strong><span></span>`;
      item.querySelector('strong').textContent = effect.name_en;
      item.querySelector('span').textContent = `${effect.name} (${effect.type || 'effect'})`;

      item.addEventListener('click', () => {
        if (!state.selectedSubEffects.includes(effect.id)) {
          state.selectedSubEffects.push(effect.id);
          renderSubEffectChips();
          setDirty(true);
        }
        closeSubEffectPicker();
      });

      container.append(item);
    });
  }

  // --- New Effect Modal Dialog ---

  function openNewEffectModal() {
    if (state.dirty && !window.confirm('Có thay đổi chưa lưu trong hiệu ứng hiện tại. Tiếp tục tạo mới?')) {
      return;
    }
    $('new-name-en').value = '';
    $('new-name-vi').value = '';
    $('new-desc-en').value = '';
    $('new-desc-vi').value = '';
    $('new-effect-type').value = 'effect';
    $('new-effect-modal').hidden = false;
    $('new-name-en').focus();
  }

  function closeNewEffectModal() {
    $('new-effect-modal').hidden = true;
  }

  async function handleCreateEffect(event) {
    event.preventDefault();
    const name_en = $('new-name-en').value.trim();
    const name_vi = $('new-name-vi').value.trim();
    const desc_en = $('new-desc-en').value.trim();
    const desc_vi = $('new-desc-vi').value.trim();
    const type = $('new-effect-type').value;

    if (!name_en || !name_vi || !desc_vi) {
      toast('Vui lòng điền đủ các trường bắt buộc (*)', true);
      return;
    }

    const submitBtn = $('submit-new-effect-btn');
    submitBtn.disabled = true;
    submitBtn.textContent = 'Đang tạo…';

    try {
      const payload = await requestJson('/api/effects', {
        method: 'POST',
        body: JSON.stringify({
          name_en,
          name: name_vi,
          desc_en,
          desc: desc_vi,
          type,
        }),
      });

      closeNewEffectModal();
      const newEffect = payload.effect;
      toast(`Đã tạo thành công hiệu ứng: ${newEffect?.name || name_vi}`);
      await loadEffects(newEffect?.id);
    } catch (error) {
      toast(error.message, true);
    } finally {
      submitBtn.disabled = false;
      submitBtn.textContent = 'Tạo hiệu ứng';
    }
  }

  // --- Data Loading & Save ---

  async function loadEffects(selectId = null) {
    const payload = await requestJson('/api/effects');
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
      const payload = await requestJson(
        `/api/effects/${encodeURIComponent(state.selected.id)}`,
        {
          method: 'PUT',
          body: JSON.stringify({
            name: $('name-vi').value,
            desc: $('desc-vi').value,
            type: $('effect-type').value,
            sub_effect_ids: state.selectedSubEffects,
          }),
        }
      );

      const effectId = state.selected.id;
      await loadEffects(effectId);
      toast('Đã lưu thành công và đồng bộ hóa đa tệp.');
    } catch (error) {
      setDirty(true);
      toast(error.message, true);
    }
  }

  // --- Event Bindings ---

  ['name-vi', 'desc-vi', 'effect-type'].forEach((id) => {
    $(id).addEventListener('input', () => setDirty(true));
    $(id).addEventListener('change', () => setDirty(true));
  });

  $('search').addEventListener('input', renderList);
  $('save').addEventListener('click', save);

  // New effect button & modal events
  $('btn-new-effect').addEventListener('click', openNewEffectModal);
  $('close-new-modal-btn').addEventListener('click', closeNewEffectModal);
  $('cancel-new-effect-btn').addEventListener('click', closeNewEffectModal);
  $('new-effect-form').addEventListener('submit', handleCreateEffect);

  // Sub-effect picker events
  $('add-sub-effect-btn').addEventListener('click', openSubEffectPicker);
  $('close-picker-btn').addEventListener('click', closeSubEffectPicker);
  $('picker-search').addEventListener('input', renderPickerList);

  document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
      if (!$('new-effect-modal').hidden) {
        closeNewEffectModal();
        return;
      }
      if (!$('sub-effect-picker').hidden) {
        closeSubEffectPicker();
        return;
      }
    }
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

  // --- Initialization with Server Gate ---

  async function init() {
    const isOk = await setupServerGate('server-gate-banner', 'effects', [
      'save',
      'add-sub-effect-btn',
      'btn-new-effect',
    ]);
    if (isOk) {
      loadEffects().catch((error) => toast(error.message, true));
    }
  }

  init();
})();
