// ============================================================
//  GFL2: Exilium Wiki — Search & Filter Logic (search.js)
// ============================================================

(function() {
  'use strict';

  let SEARCH_INDEX = [];
  let rootPath = '';

  // Determine root path based on current location
  function initRootPath() {
    const scripts = document.getElementsByTagName('script');
    for (let s of scripts) {
      if (s.src && s.src.includes('search.js')) {
        // e.g. "http://localhost/static/js/search.js" -> root is "/" or relative
        const url = new URL(s.src, window.location.href);
        const idx = url.pathname.indexOf('/static/js/search.js');
        if (idx !== -1) {
          rootPath = url.pathname.substring(0, idx + 1);
        }
        break;
      }
    }
    if (!rootPath) rootPath = './';
    if (!rootPath.endsWith('/')) rootPath += '/';
  }

  // Load search-index.json
  async function loadSearchIndex() {
    try {
      const resp = await fetch(`${rootPath}search-index.json`);
      if (resp.ok) {
        SEARCH_INDEX = await resp.json();
      }
    } catch (e) {
      console.warn('Search index load skipped:', e);
    }
  }

  // Search input handler with accessibility & keyboard navigation
  function initSearchInput() {
    const input = document.getElementById('global-search-input');
    const dropdown = document.getElementById('search-dropdown');
    if (!input || !dropdown) return;

    let selectedIndex = -1;

    function closeDropdown() {
      dropdown.innerHTML = '';
      dropdown.classList.remove('open');
      input.setAttribute('aria-expanded', 'false');
      input.removeAttribute('aria-activedescendant');
      selectedIndex = -1;
    }

    function updateActiveDescendant(items) {
      items.forEach((item, idx) => {
        if (idx === selectedIndex) {
          item.classList.add('selected');
          item.setAttribute('aria-selected', 'true');
          input.setAttribute('aria-activedescendant', item.id);
          item.scrollIntoView({ block: 'nearest' });
        } else {
          item.classList.remove('selected');
          item.setAttribute('aria-selected', 'false');
        }
      });
      if (selectedIndex === -1) {
        input.removeAttribute('aria-activedescendant');
      }
    }

    input.addEventListener('input', () => {
      const q = input.value.trim().toLowerCase();
      if (!q || q.length < 1) {
        closeDropdown();
        return;
      }

      const bundle = window.GFL2_I18N_VI;
      const isVi = (window.GFL2_I18N && window.GFL2_I18N.current === 'vi') || document.documentElement.lang === 'vi';

      const results = SEARCH_INDEX.filter(item => {
        const name = (item.name || '').toLowerCase();
        const type = (item.type || item.class || '').toLowerCase();
        const slug = (item.slug || '').toLowerCase();
        let viName = '';
        let viType = '';
        if (bundle) {
          if (item.category === 'weapon' && bundle.weapons && bundle.weapons[item.slug]) {
            viName = (bundle.weapons[item.slug].name || '').toLowerCase();
            viType = (bundle.weapons[item.slug].weapon_type || '').toLowerCase();
          } else if (item.category === 'doll' && bundle.characters && bundle.characters[item.slug]) {
            viName = (bundle.characters[item.slug].name || '').toLowerCase();
            viType = (bundle.characters[item.slug].class || '').toLowerCase();
          }
        }
        return name.includes(q) || type.includes(q) || slug.includes(q) || viName.includes(q) || viType.includes(q);
      }).slice(0, 8);

      if (results.length === 0) {
        const emptyMsg = isVi ? 'Không tìm thấy nhân vật hoặc vũ khí phù hợp' : 'No matching dolls or weapons found';
        dropdown.innerHTML = `<div class="search-result-item search-empty" role="status" aria-live="polite" style="color:var(--text-muted);font-size:0.85rem">${emptyMsg}</div>`;
        dropdown.classList.add('open');
        input.setAttribute('aria-expanded', 'true');
        selectedIndex = -1;
        return;
      }

      dropdown.innerHTML = '';
      selectedIndex = -1;
      results.forEach((r, idx) => {
        const a = document.createElement('a');
        a.className = 'search-result-item';
        a.id = `search-result-${idx}`;
        a.setAttribute('role', 'option');
        a.setAttribute('aria-selected', 'false');
        a.href = r.url.startsWith('/') ? `${rootPath}${r.url.substring(1)}` : `${rootPath}${r.url}`;

        const thumb = document.createElement('img');
        thumb.className = 'search-thumb';
        thumb.src = r.image ? (r.image.startsWith('/') ? `${rootPath}${r.image.substring(1)}` : `${rootPath}${r.image}`) : `${rootPath}assets/images/characters/groza/portrait.png`;
        thumb.alt = '';
        thumb.setAttribute('aria-hidden', 'true');

        const info = document.createElement('div');
        info.className = 'search-info';

        const title = document.createElement('div');
        title.className = 'search-title';
        let displayName = r.name;
        if (isVi && bundle) {
          if (r.category === 'weapon' && bundle.weapons && bundle.weapons[r.slug]) {
            displayName = bundle.weapons[r.slug].name || r.name;
          } else if (r.category === 'doll' && bundle.characters && bundle.characters[r.slug]) {
            displayName = bundle.characters[r.slug].name || r.name;
          }
        }
        title.textContent = displayName;

        const subtitle = document.createElement('div');
        subtitle.className = 'search-subtitle';
        const category = r.category === 'doll' ? (isVi ? 'Nhân vật' : 'Doll') : r.category === 'guide' ? (isVi ? 'Hướng dẫn' : 'Guide') : (isVi ? 'Vũ khí' : 'Weapon');
        subtitle.textContent = [category, r.rarity, r.class || r.weapon_type].filter(Boolean).join(' • ');

        info.append(title, subtitle);
        a.append(thumb, info);
        dropdown.append(a);
      });
      dropdown.classList.add('open');
      input.setAttribute('aria-expanded', 'true');
    });

    input.addEventListener('keydown', (e) => {
      if (!dropdown.classList.contains('open')) return;
      const items = [...dropdown.querySelectorAll('a.search-result-item')];
      if (!items.length) {
        if (e.key === 'Escape') {
          closeDropdown();
          e.preventDefault();
        }
        return;
      }

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        selectedIndex = (selectedIndex + 1) % items.length;
        updateActiveDescendant(items);
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        selectedIndex = (selectedIndex - 1 + items.length) % items.length;
        updateActiveDescendant(items);
      } else if (e.key === 'Enter') {
        if (selectedIndex >= 0 && items[selectedIndex]) {
          e.preventDefault();
          items[selectedIndex].click();
        }
      } else if (e.key === 'Escape') {
        e.preventDefault();
        closeDropdown();
      }
    });

    document.addEventListener('click', (e) => {
      if (!input.contains(e.target) && !dropdown.contains(e.target)) {
        closeDropdown();
      }
    });
  }

  // Filter logic for Character Index & Weapons Index
  function initFilters() {
    const panel = document.getElementById('catalog-filters');
    const toolbar = document.querySelector('.filter-toolbar');
    const cards = [...document.querySelectorAll('[data-card-item]')];
    if (!panel || !toolbar || !cards.length) return;
    const chips = [...panel.querySelectorAll('[data-filter]')];
    const active = { class: 'all', rarity: 'all', phase: 'all', weapon_type: 'all', ammo_type: 'all', server: 'all' };
    const toggle = toolbar.querySelector('.filter-toggle');
    const reset = toolbar.querySelector('.filter-reset');
    const count = document.getElementById('filter-count');
    const params = new URLSearchParams(location.search);
    const mobile = matchMedia('(max-width: 768px)');
    toolbar.hidden = false;
    panel.classList.add('filters-enhanced');
    if (document.getElementById('dolls-container')) {
      panel.querySelectorAll('.filter-group').forEach(group => {
        const key = group.querySelector('[data-filter]')?.dataset.filter;
        if (['rarity', 'weapon_type', 'ammo_type'].includes(key)) group.classList.add('filter-extra');
      });
    } else {
      panel.querySelector('[data-filter="server"]')?.closest('.filter-group').classList.add('filter-extra');
    }
    const empty = document.createElement('p');
    empty.className = 'catalog-empty';
    empty.setAttribute('role', 'status');
    panel.after(empty);
    function setOpen(open) {
      panel.classList.toggle('filters-open', open);
      toggle.setAttribute('aria-expanded', String(open));
    }
    toggle.addEventListener('click', () => setOpen(toggle.getAttribute('aria-expanded') !== 'true'));
    function render(writeUrl = false) {
      let visible = 0;
      cards.forEach(card => {
        const match = Object.entries(active).every(([key, value]) => value === 'all' || card.dataset[key] === value);
        card.style.display = match ? '' : 'none';
        if (match) visible++;
      });
      chips.forEach(chip => {
        const selected = (active[chip.dataset.filter] || 'all') === chip.dataset.value;
        chip.classList.toggle('active', selected);
        chip.setAttribute('aria-pressed', String(selected));
      });
      const total = Object.values(active).filter(value => value !== 'all').length;
      toolbar.querySelector('[data-filter-total]').textContent = String(total);
      reset.disabled = total === 0;
      const vi = document.documentElement.lang === 'vi';
      if (count) { count.textContent = vi ? `${visible} mục` : `${visible} items`; count.setAttribute('role', 'status'); }
      empty.hidden = visible !== 0;
      empty.textContent = vi ? 'Không có kết quả. Hãy xóa hoặc thay đổi bộ lọc.' : 'No results. Clear or change the filters.';
      if (writeUrl) {
        const url = new URL(location.href);
        Object.entries(active).forEach(([key, value]) => value === 'all' ? url.searchParams.delete(key) : url.searchParams.set(key, value));
        history.replaceState(null, '', url);
      }
    }
    chips.forEach(chip => {
      const key = chip.dataset.filter;
      if (!(key in active)) active[key] = 'all';
      if (params.get(key) === chip.dataset.value) active[key] = chip.dataset.value;
      chip.addEventListener('click', () => { active[key] = chip.dataset.value; render(true); });
    });
    reset.addEventListener('click', () => { Object.keys(active).forEach(key => { active[key] = 'all'; }); render(true); });
    // Reflect translated counts without coupling to the language switcher's internals.
    new MutationObserver(() => render()).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
    mobile.addEventListener('change', () => setOpen(false));
    const view = toolbar.querySelector('.view-toggle');
    if (view) view.addEventListener('click', () => {
      const compact = view.getAttribute('aria-pressed') !== 'true';
      view.setAttribute('aria-pressed', String(compact));
      document.getElementById('weapons-container').classList.toggle('is-list', compact);
    });
    render();
  }

  // FAQ Accordion with semantic HTML & ARIA
  function initFaq() {
    document.querySelectorAll('.faq-question').forEach(q => {
      q.addEventListener('click', () => {
        const answerId = q.getAttribute('aria-controls');
        const answer = answerId ? document.getElementById(answerId) : q.nextElementSibling;
        if (!answer) return;
        const isExpanded = q.getAttribute('aria-expanded') === 'true';
        q.setAttribute('aria-expanded', String(!isExpanded));
        answer.hidden = isExpanded;
        const arrow = q.querySelector('.faq-arrow');
        if (arrow) {
          arrow.textContent = isExpanded ? '▼' : '▲';
        }
      });
    });
  }

  // Mobile menu toggle
  function initMobileMenu() {
    const btn = document.getElementById('mobile-menu-btn');
    const navLinks = document.getElementById('nav-links');
    if (!btn || !navLinks) return;
    btn.addEventListener('click', () => {
      const isOpen = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!isOpen));
      navLinks.classList.toggle('open', !isOpen);
    });
  }

  // Status Effect Interactive Popover Controller
  function initEffectPopovers() {
    if (document.documentElement.dataset.effectPopoversReady === 'true') return;
    document.documentElement.dataset.effectPopoversReady = 'true';
    let popover = null;
    let activeTrigger = null;
    let hideTimer = null;

    function getPopoverEl() {
      if (!popover) {
        popover = document.createElement('div');
        popover.id = 'effect-popover';
        popover.setAttribute('role', 'tooltip');
        popover.setAttribute('aria-hidden', 'true');
        document.body.appendChild(popover);

        popover.addEventListener('mouseenter', () => {
          clearTimeout(hideTimer);
        });
        popover.addEventListener('mouseleave', () => {
          hidePopover();
        });
      }
      return popover;
    }

    function escapeHTML(str) {
      if (!str) return '';
      return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
    }

    function escapeRegex(str) {
      return String(str).replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
    }

    function currentLanguage() {
      try {
        return localStorage.getItem('gfl2_lang') || 'en';
      } catch (_) {
        return document.documentElement.lang === 'vi' ? 'vi' : 'en';
      }
    }

    function formatDescHTML(desc, subEffects) {
      if (!desc) return '';
      let text = escapeHTML(desc);

      // 1. Highlight referenced sub-effects in text
      if (subEffects && subEffects.length > 0) {
        subEffects.forEach(subId => {
          const subData = getEffectData('', subId) || {};
          const sType = subData.type || 'effect';
          const subName = currentLanguage() === 'vi'
            ? (subData.name || subData.name_en || '')
            : (subData.name_en || subData.name || '');
          if (!subName) return;
          const escapedSub = escapeHTML(subName);
          const regex = new RegExp(`(?<=^|[\\s,.:;!?'"\\(\\[\\{“‘])(${escapeRegex(escapedSub)})(?=[\\s,.:;!?'"\\)\\]\\}”’]|$)`, 'gi');
          text = text.replace(regex, `<span class="popover-subeffect-mention sub-${sType}">$1</span>`);
        });
      }

      // 2. Damage types (Dandegate colors - English & Vietnamese)
      text = text.replace(/\b(Freeze\s+[Dd]amage|ST\s+Băng(?:\s+Kết)?|Sát\s+[Tt]hương\s+Băng(?:\s+Kết)?)\b/g, '<span class="dmg-freeze">$1</span>');
      text = text.replace(/\b(Burn\s+[Dd]amage|ST\s+Thiêu\s+Đốt|Sát\s+[Tt]hương\s+Thiêu\s+Đốt)\b/g, '<span class="dmg-burn">$1</span>');
      text = text.replace(/\b(Corrosion\s+[Dd]amage|ST\s+Ăn\s+Mòn|Sát\s+[Tt]hương\s+Ăn\s+Mòn)\b/g, '<span class="dmg-corrosion">$1</span>');
      text = text.replace(/\b(Hydro\s+[Dd]amage|ST\s+Hóa\s+Lỏng|Sát\s+[Tt]hương\s+Hóa\s+Lỏng)\b/g, '<span class="dmg-hydro">$1</span>');
      text = text.replace(/\b(Electric\s+[Dd]amage|ST\s+Dẫn\s+Điện|Sát\s+[Tt]hương\s+Dẫn\s+Điện|ST\s+Điện\s+Từ|ST\s+Điện)\b/g, '<span class="dmg-electric">$1</span>');
      text = text.replace(/\b(Physical\s+[Dd]amage|ST\s+Vật\s+Lý|Sát\s+[Tt]hương\s+Vật\s+Lý)\b/g, '<span class="dmg-physical">$1</span>');
      text = text.replace(/\b([Ff]ixed\s+[Dd]amage|[Rr]eal\s+[Dd]amage|ST\s+cố\s+định|ST\s+Chuẩn|Sát\s+[Tt]hương\s+cố\s+định|Sát\s+[Tt]hương\s+Chuẩn)\b/g, '<span class="dmg-fixed">$1</span>');
      text = text.replace(/\b([Ss]tability\s+[Dd]amage|ST\s+Ổn\s+Định|Sát\s+[Tt]hương\s+Ổn\s+Định|Chỉ\s+Số\s+Ổn\s+Định|Độ\s+Ổn\s+Định)\b/g, '<span class="dmg-stability">$1</span>');

      // 3. Percentages (Dandegate orange rgb(243, 109, 28))
      text = text.replace(/\b(?:\d+(?:\.\d+)?%(?:\s*\/\s*)?)+/g, '<span class="val-highlight">$&</span>');

      // 4. Tiles (Dandegate orange rgb(243, 109, 28) - English & Vietnamese)
      text = text.replace(/\b(?:\d+(?:\.\d+)?(?:\s*(?:[\/to-]|to)\s*|\s*,\s*))*\d+(?:\.\d+)?\s*-?\s*tiles?(?:\s+(?:radius|wide))?\b/gi, '<span class="val-highlight">$&</span>');
      text = text.replace(/\b(?:\d+(?:\.\d+)?(?:\s*(?:[\/đến-]|đến)\s*|\s*,\s*))*\d+(?:\.\d+)?\s*ô(?:\s+(?:xung\s+quanh|bán\s+kính|rộng))?\b/gi, '<span class="val-highlight">$&</span>');
      text = text.replace(/\b\d+x\d+\s*ô\b/gi, '<span class="val-highlight">$&</span>');

      return text;
    }

    function positionPopover(trigger, pop) {
      const rect = trigger.getBoundingClientRect();
      const popRect = pop.getBoundingClientRect();
      const gap = 8;
      const margin = 10;

      // Vertical position: prefer above
      let top = rect.top - popRect.height - gap;
      if (top < margin) {
        // Not enough room above, place below
        top = rect.bottom + gap;
      }
      // Viewport bottom clamp
      if (top + popRect.height > window.innerHeight - margin) {
        top = window.innerHeight - margin - popRect.height;
      }
      if (top < margin) top = margin;

      // Horizontal position: center with trigger
      let left = rect.left + (rect.width / 2) - (popRect.width / 2);
      if (left < margin) {
        left = margin;
      } else if (left + popRect.width > window.innerWidth - margin) {
        left = window.innerWidth - margin - popRect.width;
      }

      pop.style.top = `${Math.round(top)}px`;
      pop.style.left = `${Math.round(left)}px`;
    }

    function getEffectData(name, id = '') {
      if (!window.GFL2_EFFECTS) return null;
      const byId = window.GFL2_EFFECTS.byId || window.GFL2_EFFECTS;
      if (id && byId[id]) return byId[id];
      if (!name) return null;
      const trimmed = String(name).trim();
      const index = window.GFL2_EFFECTS.nameIndex;
      const ids = index && index[trimmed.toLocaleLowerCase()];
      if (ids && ids.length) return byId[ids[0]] || null;
      const lower = trimmed.toLocaleLowerCase();
      for (const entry of Object.values(byId)) {
        if (!entry || typeof entry !== 'object') continue;
        if (String(entry.name_en || '').toLocaleLowerCase() === lower || String(entry.name || '').toLocaleLowerCase() === lower) return entry;
      }
      return null;
    }

    function showPopover(trigger) {
      clearTimeout(hideTimer);
      activeTrigger = trigger;
      const pop = getPopoverEl();

      const isVi = currentLanguage() === 'vi';
      const name = trigger.getAttribute('data-effect') || '';
      const effectId = trigger.getAttribute('data-effect-id') || '';
      let desc = trigger.getAttribute('data-desc') || '';
      let type = trigger.getAttribute('data-type') || 'effect';

      const effectObj = getEffectData(name, effectId);
      let displayTitle = name;
      if (effectObj) {
        if (isVi) {
          displayTitle = effectObj.name || name;
          desc = effectObj.desc || desc;
        } else {
          displayTitle = effectObj.name_en || name;
          desc = effectObj.desc_en || desc;
        }
        if (effectObj.type) type = effectObj.type;
      }
      const typeLabel = isVi
        ? (type === 'buff' ? 'Buff' : (type === 'debuff' ? 'Debuff' : 'Hiệu Ứng'))
        : (type === 'buff' ? 'Buff' : (type === 'debuff' ? 'Debuff' : 'Status Effect'));

      // Resolve referenced sub-effects
      const subEffects = effectObj ? (effectObj.sub_effect_ids || []) : [];
      let subEffectsHTML = '';

      if (subEffects.length > 0 && window.GFL2_EFFECTS) {
        const cards = [];
        subEffects.forEach(subId => {
          const subData = getEffectData('', subId);
          if (subData) {
            const sType = subData.type || 'effect';
            const sTitle = isVi ? (subData.name || subData.name_en) : (subData.name_en || subData.name);
            const sLabel = isVi
              ? (sType === 'buff' ? 'Buff' : (sType === 'debuff' ? 'Debuff' : 'Hiệu Ứng'))
              : (sType === 'buff' ? 'Buff' : (sType === 'debuff' ? 'Debuff' : 'Status Effect'));
            const sDesc = isVi ? (subData.desc || '') : (subData.desc_en || subData.desc || '');
            cards.push(`
              <div class="popover-subeffect-card subcard-${sType}">
                <div class="popover-subeffect-head">
                  <span class="popover-subeffect-title">${escapeHTML(sTitle)}</span>
                  <span class="popover-badge popover-badge-${sType}">${sLabel}</span>
                </div>
                <p class="popover-subeffect-desc">${formatDescHTML(sDesc)}</p>
              </div>
            `);
          }
        });
        if (cards.length > 0) {
          subEffectsHTML = `
            <div class="popover-subeffects">
              <div class="popover-subeffects-header">
                <span class="subeffects-icon">◈</span> ${isVi ? 'Hiệu Ứng Liên Quan' : 'Referenced Effects'}
              </div>
              <div class="popover-subeffects-list">
                ${cards.join('')}
              </div>
            </div>
          `;
        }
      }

      pop.className = `visible popover-${type}`;
      pop.setAttribute('aria-hidden', 'false');
      pop.innerHTML = `
        <div class="popover-header">
          <span class="popover-title">${escapeHTML(displayTitle)}</span>
          <span class="popover-badge popover-badge-${type}">${typeLabel}</span>
        </div>
        <p class="popover-desc">${formatDescHTML(desc, subEffects)}</p>
        ${subEffectsHTML}
      `;

      positionPopover(trigger, pop);
    }

    function hidePopover() {
      clearTimeout(hideTimer);
      hideTimer = setTimeout(() => {
        if (popover) {
          popover.className = '';
          popover.setAttribute('aria-hidden', 'true');
        }
        activeTrigger = null;
      }, 120);
    }

    // Event Delegation
    document.addEventListener('mouseover', (e) => {
      const trigger = e.target instanceof Element ? e.target.closest('.effect-trigger') : null;
      if (trigger) {
        showPopover(trigger);
      }
    });

    document.addEventListener('mouseout', (e) => {
      const trigger = e.target instanceof Element ? e.target.closest('.effect-trigger') : null;
      if (trigger) {
        hidePopover();
      }
    });

    document.addEventListener('click', (e) => {
      const trigger = e.target instanceof Element ? e.target.closest('.effect-trigger') : null;
      if (trigger) {
        if (activeTrigger === trigger && popover && popover.classList.contains('visible')) {
          hidePopover();
        } else {
          showPopover(trigger);
        }
      } else if (popover && !popover.contains(e.target)) {
        hidePopover();
      }
    });

    document.addEventListener('focusin', (e) => {
      const trigger = e.target instanceof Element ? e.target.closest('.effect-trigger') : null;
      if (trigger) {
        showPopover(trigger);
      }
    });

    document.addEventListener('focusout', (e) => {
      const trigger = e.target instanceof Element ? e.target.closest('.effect-trigger') : null;
      if (trigger) {
        hidePopover();
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && popover && popover.classList.contains('visible')) {
        hidePopover();
      }
    });

    window.addEventListener('scroll', () => {
      if (activeTrigger && popover && popover.classList.contains('visible')) {
        positionPopover(activeTrigger, popover);
      }
    }, { passive: true });

    window.addEventListener('resize', () => {
      if (activeTrigger && popover && popover.classList.contains('visible')) {
        positionPopover(activeTrigger, popover);
      }
    }, { passive: true });
  }

  function initMobileMenu() {
    const btn = document.getElementById('mobile-menu-btn');
    const navLinks = document.getElementById('nav-links');
    if (!btn || !navLinks) return;

    btn.addEventListener('click', () => {
      const expanded = btn.getAttribute('aria-expanded') === 'true';
      btn.setAttribute('aria-expanded', String(!expanded));
      navLinks.classList.toggle('open', !expanded);
    });

    document.addEventListener('click', (e) => {
      if (!btn.contains(e.target) && !navLinks.contains(e.target) && navLinks.classList.contains('open')) {
        btn.setAttribute('aria-expanded', 'false');
        navLinks.classList.remove('open');
      }
    });

    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && navLinks.classList.contains('open')) {
        btn.setAttribute('aria-expanded', 'false');
        navLinks.classList.remove('open');
        btn.focus();
      }
    });
  }

  function stripGuideGameMarkup(value) {
    return String(value || '')
      .replace(/<\/?color(?:=[^>]+)?>/gi, '')
      .replace(/\r\n?/g, '\n')
      .trim();
  }

  function ensureLegacySkillPopover(trigger) {
    if (!trigger.classList.contains('guide-inline-skill') || trigger.querySelector('.guide-skill-popover')) return;
    const legacyTitle = stripGuideGameMarkup(trigger.getAttribute('title') || '');
    if (!legacyTitle) return;
    const separator = legacyTitle.indexOf(':');
    const name = separator >= 0 ? legacyTitle.slice(0, separator).trim() : trigger.textContent.trim();
    const description = separator >= 0 ? legacyTitle.slice(separator + 1).trim() : legacyTitle;
    const popover = document.createElement('span');
    popover.className = 'guide-ref-popover guide-skill-popover';
    const nameEl = document.createElement('span');
    nameEl.className = 'guide-skill-popover-name';
    nameEl.textContent = name;
    const descEl = document.createElement('span');
    descEl.className = 'guide-skill-popover-desc';
    descEl.textContent = description;
    popover.append(nameEl, descEl);
    trigger.append(popover);
    trigger.removeAttribute('title');
    if (!trigger.hasAttribute('tabindex')) trigger.setAttribute('tabindex', '0');
  }

  function positionGuideReferencePopover(trigger) {
    const popover = trigger.querySelector(':scope > .guide-ref-popover');
    if (!popover) return;
    const viewportPadding = 12;
    popover.classList.add('is-open');
    popover.style.left = `${viewportPadding}px`;
    popover.style.top = `${viewportPadding}px`;
    const triggerRect = trigger.getBoundingClientRect();
    const popoverRect = popover.getBoundingClientRect();
    const preferredLeft = triggerRect.left + (triggerRect.width - popoverRect.width) / 2;
    const left = Math.max(viewportPadding, Math.min(preferredLeft, window.innerWidth - popoverRect.width - viewportPadding));
    const preferredTop = triggerRect.top - popoverRect.height - 8;
    const belowTop = triggerRect.bottom + 8;
    const unclampedTop = preferredTop >= viewportPadding ? preferredTop : belowTop;
    const top = Math.max(viewportPadding, Math.min(unclampedTop, window.innerHeight - popoverRect.height - viewportPadding));
    popover.style.left = `${Math.round(left)}px`;
    popover.style.top = `${Math.round(top)}px`;
  }

  function hideGuideReferencePopover(trigger) {
    const popover = trigger.querySelector(':scope > .guide-ref-popover');
    if (!popover) return;
    popover.classList.remove('is-open');
    popover.style.removeProperty('left');
    popover.style.removeProperty('top');
  }

  function initGuideReferencePopovers() {
    const triggers = document.querySelectorAll('.guide-inline-weapon, .guide-inline-skill');
    triggers.forEach((trigger) => {
      ensureLegacySkillPopover(trigger);
      const existingPopover = trigger.querySelector(':scope > .guide-weapon-popover, :scope > .guide-skill-popover');
      if (existingPopover) existingPopover.classList.add('guide-ref-popover');
      trigger.addEventListener('pointerenter', () => positionGuideReferencePopover(trigger));
      trigger.addEventListener('pointerleave', () => hideGuideReferencePopover(trigger));
      trigger.addEventListener('focusin', () => positionGuideReferencePopover(trigger));
      trigger.addEventListener('focusout', (event) => {
        if (!trigger.contains(event.relatedTarget)) hideGuideReferencePopover(trigger);
      });
    });
    let repositionFrame = 0;
    function repositionVisibleGuideReferencePopovers() {
      repositionFrame = 0;
      triggers.forEach((trigger) => {
        const isActive = trigger.matches(':hover') || trigger.contains(document.activeElement);
        if (isActive) positionGuideReferencePopover(trigger);
        else hideGuideReferencePopover(trigger);
      });
    }
    function scheduleGuideReferenceReposition() {
      if (repositionFrame) return;
      repositionFrame = window.requestAnimationFrame(repositionVisibleGuideReferencePopovers);
    }
    window.addEventListener('resize', scheduleGuideReferenceReposition);
    window.addEventListener('scroll', scheduleGuideReferenceReposition, { passive: true });
  }

  // Boot
  function boot() {
    if (matchMedia('(max-width: 900px)').matches) {
      document.querySelectorAll('.guide-toc').forEach(toc => { toc.open = false; });
    }
    // Keep popovers independent from failures in search/filter initialization.
    initEffectPopovers();
    try { initRootPath(); } catch (error) { console.warn('[search] initRootPath:', error); }
    try { loadSearchIndex(); } catch (error) { console.warn('[search] loadSearchIndex:', error); }
    try { initSearchInput(); } catch (error) { console.warn('[search] initSearchInput:', error); }
    try { initFilters(); } catch (error) { console.warn('[search] initFilters:', error); }
    try { initFaq(); } catch (error) { console.warn('[search] initFaq:', error); }
    try { initMobileMenu(); } catch (error) { console.warn('[search] initMobileMenu:', error); }
    try { initGuideReferencePopovers(); } catch (error) { console.warn('[search] initGuideReferencePopovers:', error); }
  }

  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', boot, { once: true });
  else boot();
})();
