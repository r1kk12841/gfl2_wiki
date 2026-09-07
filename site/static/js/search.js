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

  // Search input handler
  function initSearchInput() {
    const input = document.getElementById('global-search-input');
    const dropdown = document.getElementById('search-dropdown');
    if (!input || !dropdown) return;

    input.addEventListener('input', () => {
      const q = input.value.trim().toLowerCase();
      if (!q || q.length < 1) {
        dropdown.innerHTML = '';
        dropdown.classList.remove('open');
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
        dropdown.innerHTML = `<div class="search-result-item" style="color:var(--text-muted);font-size:0.85rem">${emptyMsg}</div>`;
        dropdown.classList.add('open');
        return;
      }

      dropdown.innerHTML = '';
      results.forEach(r => {
        const a = document.createElement('a');
        a.className = 'search-result-item';
        a.href = r.url.startsWith('/') ? `${rootPath}${r.url.substring(1)}` : `${rootPath}${r.url}`;

        const thumb = document.createElement('img');
        thumb.className = 'search-thumb';
        thumb.src = r.image ? (r.image.startsWith('/') ? `${rootPath}${r.image.substring(1)}` : `${rootPath}${r.image}`) : `${rootPath}assets/images/characters/groza/portrait.png`;
        thumb.alt = r.name;

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
        subtitle.textContent = `${r.category === 'doll' ? 'Doll' : 'Weapon'} • ${r.rarity || ''} • ${r.class || r.weapon_type || ''}`;

        info.append(title, subtitle);
        a.append(thumb, info);
        dropdown.append(a);
      });
      dropdown.classList.add('open');
    });

    document.addEventListener('click', (e) => {
      if (!input.contains(e.target) && !dropdown.contains(e.target)) {
        dropdown.classList.remove('open');
      }
    });
  }

  // Filter logic for Character Index & Weapons Index
  function initFilters() {
    const activeFilters = {
      class: 'all',
      rarity: 'all',
      phase: 'all',
      weapon_type: 'all',
      server: 'all'
    };

    const chips = document.querySelectorAll('.chip[data-filter]');
    const cards = document.querySelectorAll('[data-card-item]');

    if (chips.length === 0 || cards.length === 0) return;

    chips.forEach(chip => {
      chip.addEventListener('click', () => {
        const filterType = chip.dataset.filter;
        const filterVal = chip.dataset.value;

        // Toggle within same group
        const groupChips = document.querySelectorAll(`.chip[data-filter="${filterType}"]`);
        groupChips.forEach(c => c.classList.remove('active'));
        chip.classList.add('active');

        activeFilters[filterType] = filterVal;

        // Filter cards
        let visibleCount = 0;
        cards.forEach(card => {
          let match = true;
          for (let [fKey, fVal] of Object.entries(activeFilters)) {
            if (fVal && fVal !== 'all') {
              const cardVal = card.dataset[fKey];
              if (cardVal !== fVal) {
                match = false;
                break;
              }
            }
          }
          if (match) {
            card.style.display = '';
            visibleCount++;
          } else {
            card.style.display = 'none';
          }
        });

        const countEl = document.getElementById('filter-count');
        if (countEl) {
          const isVi = (window.GFL2_I18N && window.GFL2_I18N.current === 'vi') || document.documentElement.lang === 'vi';
          if (isVi) {
            countEl.textContent = `${visibleCount} mục`;
          } else {
            countEl.textContent = `${visibleCount} item${visibleCount === 1 ? '' : 's'}`;
          }
        }
      });
    });

  }

  // FAQ Accordion
  function initFaq() {
    document.querySelectorAll('.faq-question').forEach(q => {
      q.addEventListener('click', () => {
        const answer = q.nextElementSibling;
        if (!answer) return;
        const isHidden = answer.style.display === 'none';
        answer.style.display = isHidden ? 'block' : 'none';
        const arrow = q.querySelector('.faq-arrow');
        if (arrow) {
          arrow.textContent = isHidden ? '▲' : '▼';
        }
      });
    });
  }

  // Status Effect Interactive Popover Controller
  function initEffectPopovers() {
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

    function formatDescHTML(desc, subEffects) {
      if (!desc) return '';
      let text = escapeHTML(desc);

      // 1. Highlight referenced sub-effects in text
      if (subEffects && subEffects.length > 0) {
        subEffects.forEach(subName => {
          const subData = (window.GFL2_EFFECTS && window.GFL2_EFFECTS[subName]) || {};
          const sType = subData.type || 'effect';
          const escapedSub = escapeHTML(subName);
          const regex = new RegExp('\\b' + escapeRegex(escapedSub) + '\\b', 'g');
          text = text.replace(regex, `<span class="popover-subeffect-mention sub-${sType}">${escapedSub}</span>`);
        });
      }

      // 2. Damage types (Dandegate colors - English & Vietnamese)
      text = text.replace(/\b(Freeze\s+[Dd]amage|ST\s+Băng(?:\s+Kết)?|Sát\s+[Tt]hương\s+Băng(?:\s+Kết)?)\b/g, '<span class="dmg-freeze">$1</span>');
      text = text.replace(/\b(Burn\s+[Dd]amage|ST\s+Thiêu\s+Đốt|Sát\s+[Tt]hương\s+Thiêu\s+Đốt)\b/g, '<span class="dmg-burn">$1</span>');
      text = text.replace(/\b(Corrosion\s+[Dd]amage|ST\s+Ăn\s+Mòn|Sát\s+[Tt]hương\s+Ăn\s+Mòn)\b/g, '<span class="dmg-corrosion">$1</span>');
      text = text.replace(/\b(Hydro\s+[Dd]amage|ST\s+Hóa\s+Lỏng|Sát\s+[Tt]hương\s+Hóa\s+Lỏng)\b/g, '<span class="dmg-hydro">$1</span>');
      text = text.replace(/\b(Electric\s+[Dd]amage|ST\s+Dẫn\s+Điện|Sát\s+[Tt]hương\s+Dẫn\s+Điện)\b/g, '<span class="dmg-electric">$1</span>');
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

    function showPopover(trigger) {
      clearTimeout(hideTimer);
      activeTrigger = trigger;
      const pop = getPopoverEl();

      const isVi = (localStorage.getItem('gfl2_lang') || 'en') === 'vi';
      const name = trigger.getAttribute('data-effect') || '';
      let desc = trigger.getAttribute('data-desc') || '';
      let type = trigger.getAttribute('data-type') || 'effect';

      const effectObj = (window.GFL2_EFFECTS && window.GFL2_EFFECTS[name]) ? window.GFL2_EFFECTS[name] : null;
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
      const subEffects = effectObj ? (isVi && effectObj.sub_effects_vi && effectObj.sub_effects_vi.length > 0 ? effectObj.sub_effects_vi : (effectObj.sub_effects || [])) : [];
      let subEffectsHTML = '';

      if (subEffects.length > 0 && window.GFL2_EFFECTS) {
        const cards = [];
        subEffects.forEach(subName => {
          const subData = window.GFL2_EFFECTS[subName];
          if (subData) {
            const sType = subData.type || 'effect';
            const sTitle = isVi ? (subData.name || subName) : (subData.name_en || subName);
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
      const trigger = e.target.closest('.effect-trigger');
      if (trigger) {
        showPopover(trigger);
      }
    });

    document.addEventListener('mouseout', (e) => {
      const trigger = e.target.closest('.effect-trigger');
      if (trigger) {
        hidePopover();
      }
    });

    document.addEventListener('click', (e) => {
      const trigger = e.target.closest('.effect-trigger');
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
      const trigger = e.target.closest('.effect-trigger');
      if (trigger) {
        showPopover(trigger);
      }
    });

    document.addEventListener('focusout', (e) => {
      const trigger = e.target.closest('.effect-trigger');
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

  // Boot
  document.addEventListener('DOMContentLoaded', () => {
    initRootPath();
    loadSearchIndex();
    initSearchInput();
    initFilters();
    initFaq();
    initEffectPopovers();
  });
})();

