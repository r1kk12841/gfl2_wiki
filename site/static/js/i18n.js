// ============================================================
//  GFL2: Exilium Wiki — Internationalization Engine (i18n.js)
// ============================================================

(function () {
  'use strict';

  const STORAGE_KEY = 'gfl2_lang';
  let currentLang = 'en';

  // Helper: Damage types regex mapping to CSS classes in Vietnamese and English
  const DMG_REGEXES = [
    { regex: /\b(Freeze\s+[Dd]amage|ST\s+Băng\s+Kết|ST\s+Băng)\b/g, cls: 'dmg-freeze' },
    { regex: /\b(Burn\s+[Dd]amage|ST\s+Thiêu\s+Đốt)\b/g, cls: 'dmg-burn' },
    { regex: /\b(Corrosion\s+[Dd]amage|ST\s+Ăn\s+Mòn)\b/g, cls: 'dmg-corrosion' },
    { regex: /\b(Hydro\s+[Dd]amage|ST\s+Hóa\s+Lỏng)\b/g, cls: 'dmg-hydro' },
    { regex: /\b(Electric\s+[Dd]amage|ST\s+Dẫn\s+Điện|ST\s+Điện)\b/g, cls: 'dmg-electric' },
    { regex: /\b(Physical\s+[Dd]amage|ST\s+Vật\s+Lý)\b/g, cls: 'dmg-physical' },
    { regex: /\b([Ff]ixed\s+[Dd]amage|[Rr]eal\s+[Dd]amage|ST\s+cố\s+định|ST\s+Chuẩn\s+Xác)\b/g, cls: 'dmg-fixed' },
    { regex: /\b([Ss]tability\s+[Dd]amage|ST\s+Ổn\s+Định)\b/g, cls: 'dmg-stability' }
  ];

  const PERCENT_REGEX = /\b(?:\d+(?:\.\d+)?%(?:\s*\/\s*)?)+/g;
  const TILE_REGEX = /\b(?:\d+(?:\.\d+)?(?:\s*(?:[/to-]|to)\s*|\s*,\s*))*\d+(?:\.\d+)?\s*-?\s*(?:tiles?(?:\s+(?:radius|wide))?|ô(?:\s+(?:xung\s+quanh|bán\s+kính|trống))?)\b/gi;

  function escapeAttr(str) {
    if (!str) return '';
    return String(str).replace(/&/g, '&amp;').replace(/"/g, '&quot;').replace(/'/g, '&#39;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  }

  function escapeRegExp(str) {
    return str.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  }

  let VI_EFFECT_REGEX = null;
  function getViEffectRegex() {
    if (VI_EFFECT_REGEX) return VI_EFFECT_REGEX;
    if (!window.GFL2_EFFECTS) return null;
    const names = Object.keys(window.GFL2_EFFECTS).filter(k => k.length > 1);
    names.sort((a, b) => b.length - a.length);
    if (names.length === 0) return null;
    VI_EFFECT_REGEX = new RegExp(`(?<=^|[\\s,.:;!?'"\\(\\[\\{“‘])(${names.map(escapeRegExp).join('|')})(?=[\\s,.:;!?'"\\)\\]\\}”’]|$)`, 'g');
    return VI_EFFECT_REGEX;
  }

  function formatRichText(htmlStr) {
    if (!htmlStr) return '';

    // Convert Unity color tags (<color=#...>...</color>) to HTML span tags
    htmlStr = htmlStr.replace(/<color=([^>]+)>(.*?)<\/color>/gi, (match, colorHex, innerText) => {
      const trimmed = innerText.trim();
      // Check if innerText is a status effect
      if (window.GFL2_EFFECTS && window.GFL2_EFFECTS[trimmed]) {
        const eff = window.GFL2_EFFECTS[trimmed];
        const effType = eff.type || 'effect';
        const effName = currentLang === 'vi' ? (eff.name || trimmed) : (eff.name_en || trimmed);
        const effDesc = currentLang === 'vi' ? (eff.desc || '') : (eff.desc_en || eff.desc || '');
        return `<span class="effect-trigger effect-${effType}" data-effect="${escapeAttr(effName)}" data-type="${effType}" data-desc="${escapeAttr(effDesc)}" tabindex="0">${innerText}</span>`;
      }
      // Check if innerText is a damage type
      for (const d of DMG_REGEXES) {
        if (d.regex.test(innerText)) {
          return innerText.replace(d.regex, `<span class="${d.cls}">$1</span>`);
        }
      }
      if (/^\d+(?:\.\d+)?%?$/.test(trimmed)) {
        return `<span class="val-highlight">${innerText}</span>`;
      }
      return `<span style="color:${colorHex}; font-weight:600;">${innerText}</span>`;
    });

    // Preserve HTML tags
    const parts = htmlStr.split(/(<[^>]+>)/);
    const effRe = getViEffectRegex();
    for (let i = 0; i < parts.length; i += 2) {
      if (!parts[i]) continue;
      let s = parts[i];
      for (const d of DMG_REGEXES) {
        s = s.replace(d.regex, `<span class="${d.cls}">$1</span>`);
      }
      s = s.replace(PERCENT_REGEX, '<span class="val-highlight">$&</span>');
      s = s.replace(TILE_REGEX, '<span class="val-highlight">$&</span>');

      // Wrap status effect mentions in plain text
      if (effRe && currentLang === 'vi') {
        s = s.replace(effRe, (match, effName) => {
          const eff = window.GFL2_EFFECTS[effName];
          if (eff) {
            const effType = eff.type || 'effect';
            const effTitle = eff.name || effName;
            const effDesc = eff.desc || '';
            return `<span class="effect-trigger effect-${effType}" data-effect="${escapeAttr(effTitle)}" data-type="${effType}" data-desc="${escapeAttr(effDesc)}" tabindex="0">${effName}</span>`;
          }
          return match;
        });
      }
      parts[i] = s;
    }
    return parts.join('');
  }

  function getI18nBundle() {
    return window.GFL2_I18N_VI || null;
  }

  function translateStaticUI(bundle, lang) {
    if (!bundle || !bundle.ui) return;
    const ui = bundle.ui;

    // Elements with data-i18n
    document.querySelectorAll('[data-i18n]').forEach((el) => {
      const key = el.getAttribute('data-i18n');
      if (!el.dataset.i18nEn) {
        el.dataset.i18nEn = el.tagName === 'INPUT' ? el.placeholder : el.textContent.trim();
      }

      if (lang === 'vi') {
        const viVal = ui[key];
        if (viVal) {
          if (el.tagName === 'INPUT') el.placeholder = viVal;
          else el.textContent = viVal;
        }
      } else {
        if (el.tagName === 'INPUT') el.placeholder = el.dataset.i18nEn;
        else el.textContent = el.dataset.i18nEn;
      }
    });

    // Translate Global Search Placeholder
    const searchInput = document.getElementById('global-search-input');
    if (searchInput) {
      if (!searchInput.dataset.i18nEn) {
        searchInput.dataset.i18nEn = searchInput.placeholder || 'Search dolls, weapons…';
      }
      searchInput.placeholder = lang === 'vi' ? (ui.search_placeholder || 'Tìm kiếm nhân vật, vũ khí…') : searchInput.dataset.i18nEn;
    }

    // Dynamic counts
    const filterCount = document.getElementById('filter-count');
    if (filterCount) {
      const txt = filterCount.textContent.trim();
      const numMatch = txt.match(/\d+/);
      if (numMatch) {
        const num = numMatch[0];
        if (window.location.pathname.includes('weapon') || document.getElementById('weapons-container')) {
          filterCount.textContent = lang === 'vi' ? `${num} ${ui.weapon_filter_count_suffix || 'vũ khí'}` : `${num} weapons`;
        } else {
          filterCount.textContent = lang === 'vi' ? `${num} ${ui.filter_count_suffix || 'nhân vật'}` : `${num} dolls`;
        }
      }
    }
  }

  function translateClassAndPhaseBadges(bundle, lang) {
    if (!bundle || !bundle.ui) return;
    const ui = bundle.ui;

    // 1. Classes on badges & detail labels
    document.querySelectorAll('[data-doll-class]').forEach((el) => {
      if (el.classList.contains('doll-card') || el.classList.contains('weapon-card')) return;
      const clsKey = el.getAttribute('data-doll-class');
      if (!clsKey) return;
      const targetSpan = el.querySelector('span') || el;
      if (!el.dataset.origEn) el.dataset.origEn = targetSpan.textContent.trim();
      targetSpan.textContent = lang === 'vi' ? (ui.classes[clsKey] || clsKey) : el.dataset.origEn;
    });

    // Classes on filter chips
    document.querySelectorAll('.filter-chip[data-cls]').forEach((el) => {
      const clsKey = el.getAttribute('data-cls');
      if (!clsKey) return;
      const targetSpan = el.querySelector('span') || el;
      if (!el.dataset.origEn) el.dataset.origEn = targetSpan.textContent.trim();
      targetSpan.textContent = lang === 'vi' ? (ui.classes[clsKey] || clsKey) : el.dataset.origEn;
    });

    // 2. Phases on badges & detail labels
    document.querySelectorAll('[data-doll-phase]').forEach((el) => {
      if (el.classList.contains('doll-card') || el.classList.contains('weapon-card')) return;
      const phKey = el.getAttribute('data-doll-phase');
      if (!phKey) return;
      const targetSpan = el.querySelector('span') || el;
      if (!el.dataset.origEn) el.dataset.origEn = targetSpan.textContent.trim();
      targetSpan.textContent = lang === 'vi' ? (ui.phases[phKey] || phKey) : el.dataset.origEn;
    });

    // Phases on filter chips
    document.querySelectorAll('.filter-chip[data-phase]').forEach((el) => {
      const phKey = el.getAttribute('data-phase');
      if (!phKey) return;
      const targetSpan = el.querySelector('span') || el;
      if (!el.dataset.origEn) el.dataset.origEn = targetSpan.textContent.trim();
      targetSpan.textContent = lang === 'vi' ? (ui.phases[phKey] || phKey) : el.dataset.origEn;
    });

    // 3. Rarities on card badges and header badges
    document.querySelectorAll('[data-doll-rarity], [data-weapon-rarity]').forEach((el) => {
      if (el.classList.contains('doll-card') || el.classList.contains('weapon-card')) return;
      const rKey = el.getAttribute('data-doll-rarity') || el.getAttribute('data-weapon-rarity');
      if (!rKey) return;
      const targetSpan = el.querySelector('span') || el;
      if (!el.dataset.origEn) el.dataset.origEn = targetSpan.textContent.trim();
      targetSpan.textContent = lang === 'vi' ? (ui.rarities[rKey] || rKey) : el.dataset.origEn;
    });

    // Rarities on filter chips
    document.querySelectorAll('.filter-chip[data-rarity]').forEach((el) => {
      const rKey = el.getAttribute('data-rarity');
      if (!rKey) return;
      const targetSpan = el.querySelector('span') || el;
      if (!el.dataset.origEn) el.dataset.origEn = targetSpan.textContent.trim();
      const filterMap = ui.rarities_filter || ui.rarities;
      targetSpan.textContent = lang === 'vi' ? (filterMap[rKey] || ui.rarities[rKey] || rKey) : el.dataset.origEn;
    });

    // 4. Weapon Types on badges & detail labels
    document.querySelectorAll('[data-doll-weapontype], [data-weapon-type]').forEach((el) => {
      if (el.classList.contains('doll-card') || el.classList.contains('weapon-card')) return;
      const wtKey = el.getAttribute('data-doll-weapontype') || el.getAttribute('data-weapon-type');
      if (!wtKey) return;
      const targetSpan = el.querySelector('span') || el;
      if (!el.dataset.origEn) el.dataset.origEn = targetSpan.textContent.trim();
      targetSpan.textContent = lang === 'vi' ? (ui.weapon_types[wtKey] || wtKey) : el.dataset.origEn;
    });

    // Weapon Types on filter chips
    document.querySelectorAll('.filter-chip[data-weapontype]').forEach((el) => {
      const wtKey = el.getAttribute('data-weapontype');
      if (!wtKey) return;
      const targetSpan = el.querySelector('span') || el;
      if (!el.dataset.origEn) el.dataset.origEn = targetSpan.textContent.trim();
      targetSpan.textContent = lang === 'vi' ? (ui.weapon_types[wtKey] || wtKey) : el.dataset.origEn;
    });

    // 5. Ammo Types
    document.querySelectorAll('[data-doll-ammotype]').forEach((el) => {
      if (el.classList.contains('doll-card') || el.classList.contains('weapon-card')) return;
      const atKey = el.getAttribute('data-doll-ammotype');
      if (!atKey) return;
      const targetSpan = el.querySelector('span') || el;
      if (!el.dataset.origEn) el.dataset.origEn = targetSpan.textContent.trim();
      targetSpan.textContent = lang === 'vi' ? (ui.ammo_types[atKey] || atKey) : el.dataset.origEn;
    });

    // 6. Skill Tags
    document.querySelectorAll('[data-tag]').forEach((el) => {
      const tagKey = el.getAttribute('data-tag');
      if (!tagKey) return;
      if (!el.dataset.origEn) el.dataset.origEn = el.textContent.trim();
      el.textContent = lang === 'vi' ? (ui.tags[tagKey] || tagKey) : el.dataset.origEn;
    });

    // 7. Servers on badges & detail labels
    document.querySelectorAll('[data-doll-server], [data-weapon-server]').forEach((el) => {
      if (el.classList.contains('doll-card') || el.classList.contains('weapon-card')) return;
      const sKey = (el.getAttribute('data-doll-server') || el.getAttribute('data-weapon-server') || '').toLowerCase();
      if (!sKey) return;
      const targetSpan = el.querySelector('span') || el;
      if (!el.dataset.origEn) el.dataset.origEn = targetSpan.textContent.trim();
      if (ui.servers && ui.servers[sKey]) {
        targetSpan.textContent = lang === 'vi' ? ui.servers[sKey] : el.dataset.origEn;
      }
    });

    // Servers on filter chips
    document.querySelectorAll('.filter-chip[data-server]').forEach((el) => {
      const sKey = (el.getAttribute('data-server') || '').toLowerCase();
      if (!sKey) return;
      const targetSpan = el.querySelector('span') || el;
      if (!el.dataset.origEn) el.dataset.origEn = targetSpan.textContent.trim();
      if (ui.servers && ui.servers[sKey]) {
        targetSpan.textContent = lang === 'vi' ? ui.servers[sKey] : el.dataset.origEn;
      }
    });
  }


  function translateCharacterDetail(bundle, lang) {
    const charHeader = document.querySelector('[data-char-slug]');
    if (!charHeader || !bundle || !bundle.characters) return;
    const slug = charHeader.getAttribute('data-char-slug');
    const cdata = bundle.characters[slug];
    if (!cdata) return;

    // Weakness
    const weaknessEl = document.querySelector('[data-doll-weakness]');
    if (weaknessEl) {
      const wVal = weaknessEl.getAttribute('data-doll-weakness');
      if (!weaknessEl.dataset.origEn) weaknessEl.dataset.origEn = weaknessEl.textContent.trim();
      weaknessEl.textContent = lang === 'vi' ? (bundle.ui.phases[wVal] || wVal) : weaknessEl.dataset.origEn;
    }

    // Signature Weapon name
    const sigEl = document.querySelector('[data-doll-sigweapon]');
    if (sigEl) {
      if (!sigEl.dataset.origEn) sigEl.dataset.origEn = sigEl.textContent.trim();
      sigEl.textContent = lang === 'vi' ? (cdata.signature_weapon || sigEl.dataset.origEn) : sigEl.dataset.origEn;
    }

    // Skills
    if (cdata.skills) {
      document.querySelectorAll('.skill-card[data-skill-idx]').forEach((card) => {
        const idx = parseInt(card.getAttribute('data-skill-idx'), 10);
        const sdata = cdata.skills[idx];
        if (!sdata) return;

        // Skill Name
        const nameEl = card.querySelector('.skill-name');
        if (nameEl) {
          if (!nameEl.dataset.origEn) nameEl.dataset.origEn = nameEl.textContent.trim();
          nameEl.textContent = lang === 'vi' ? (sdata.name || nameEl.dataset.origEn) : nameEl.dataset.origEn;
        }

        // Skill Description
        const descEl = card.querySelector('.skill-desc');
        if (descEl) {
          if (!descEl.dataset.origEnHtml) descEl.dataset.origEnHtml = descEl.innerHTML;
          if (lang === 'vi') {
            descEl.innerHTML = formatRichText(sdata.description || descEl.dataset.origEnHtml);
          } else {
            descEl.innerHTML = descEl.dataset.origEnHtml;
          }
        }
      });
    }

    // Fortifications
    if (cdata.fortification && cdata.fortification.length > 0) {
      document.querySelectorAll('tr[data-fort-tier]').forEach((tr) => {
        const tier = parseInt(tr.getAttribute('data-fort-tier'), 10);
        const fdata = cdata.fortification.find((f) => f.tier === tier || f.level === tier);
        if (!fdata) return;

        // Target skill name
        const skillEl = tr.querySelector('[data-fort-skill]');
        if (skillEl) {
          if (!skillEl.dataset.origEn) skillEl.dataset.origEn = skillEl.textContent.trim();
          // Check if skill has translated name
          const matchedSkill = cdata.skills.find((s) => s.en_name === fdata.skill || s.name === fdata.skill);
          if (matchedSkill && lang === 'vi') {
            skillEl.textContent = matchedSkill.name || skillEl.dataset.origEn;
          } else {
            skillEl.textContent = skillEl.dataset.origEn;
          }
        }

        // Effect description
        const effectTd = tr.querySelector('[data-fort-effect]') || tr.querySelector('td:last-child');
        if (effectTd) {
          if (!effectTd.dataset.origEnHtml) effectTd.dataset.origEnHtml = effectTd.innerHTML;
          if (lang === 'vi') {
            effectTd.innerHTML = formatRichText(fdata.effect || effectTd.dataset.origEnHtml);
          } else {
            effectTd.innerHTML = effectTd.dataset.origEnHtml;
          }
        }
      });
    }

    // Neural Helix
    if (cdata.neural_helix && cdata.neural_helix.length > 0) {
      document.querySelectorAll('tr[data-helix-idx]').forEach((tr) => {
        const idx = parseInt(tr.getAttribute('data-helix-idx'), 10);
        const hdata = cdata.neural_helix[idx];
        if (!hdata) return;

        const nodeEl = tr.querySelector('[data-helix-node]');
        if (nodeEl) {
          if (!nodeEl.dataset.origEn) nodeEl.dataset.origEn = nodeEl.textContent.trim();
          nodeEl.textContent = lang === 'vi' ? (hdata.node || nodeEl.dataset.origEn) : nodeEl.dataset.origEn;
        }

        const effEl = tr.querySelector('[data-helix-effect]');
        if (effEl) {
          if (!effEl.dataset.origEnHtml) effEl.dataset.origEnHtml = effEl.innerHTML;
          if (lang === 'vi') {
            effEl.innerHTML = formatRichText(hdata.effect || effEl.dataset.origEnHtml);
          } else {
            effEl.innerHTML = effEl.dataset.origEnHtml;
          }
        }
      });
    }

    // Keys
    if (cdata.keys && cdata.keys.length > 0) {
      document.querySelectorAll('tr[data-key-idx]').forEach((tr) => {
        const idx = parseInt(tr.getAttribute('data-key-idx'), 10);
        const kdata = cdata.keys[idx];
        if (!kdata) return;

        const nameEl = tr.querySelector('[data-key-name]');
        if (nameEl) {
          if (!nameEl.dataset.origEn) nameEl.dataset.origEn = nameEl.textContent.trim();
          nameEl.textContent = lang === 'vi' ? (kdata.name || nameEl.dataset.origEn) : nameEl.dataset.origEn;
        }

        const effEl = tr.querySelector('[data-key-effect]');
        if (effEl) {
          if (!effEl.dataset.origEnHtml) effEl.dataset.origEnHtml = effEl.innerHTML;
          if (lang === 'vi') {
            effEl.innerHTML = formatRichText(kdata.effect || effEl.dataset.origEnHtml);
          } else {
            effEl.innerHTML = effEl.dataset.origEnHtml;
          }
        }

        const matEl = tr.querySelector('[data-key-materials]');
        if (matEl && kdata.materials) {
          if (!matEl.dataset.origEn) matEl.dataset.origEn = matEl.textContent.trim();
          matEl.textContent = lang === 'vi' ? kdata.materials : matEl.dataset.origEn;
        }
      });
    }

    // Summons
    if (cdata.summons && cdata.summons.length > 0) {
      document.querySelectorAll('[data-summon-card]').forEach((card) => {
        const sIdx = parseInt(card.getAttribute('data-summon-card'), 10);
        const smData = cdata.summons[sIdx];
        if (!smData) return;

        // Name
        const nameEl = card.querySelector('[data-summon-name]');
        if (nameEl) {
          if (!nameEl.dataset.origEn) nameEl.dataset.origEn = nameEl.textContent.trim();
          nameEl.textContent = lang === 'vi' ? (smData.name || nameEl.dataset.origEn) : nameEl.dataset.origEn;
        }

        // Desc
        const descEl = card.querySelector('[data-summon-desc]');
        if (descEl) {
          if (!descEl.dataset.origEnHtml) descEl.dataset.origEnHtml = descEl.innerHTML;
          if (lang === 'vi') {
            descEl.innerHTML = formatRichText(smData.description || descEl.dataset.origEnHtml);
          } else {
            descEl.innerHTML = descEl.dataset.origEnHtml;
          }
        }

        // Stats
        if (smData.stats) {
          card.querySelectorAll('[data-summon-stat]').forEach((stEl) => {
            const statKey = stEl.getAttribute('data-summon-stat');
            if (smData.stats[statKey]) {
              if (!stEl.dataset.origEnHtml) stEl.dataset.origEnHtml = stEl.innerHTML;
              if (lang === 'vi') {
                stEl.innerHTML = formatRichText(smData.stats[statKey]);
              } else {
                stEl.innerHTML = stEl.dataset.origEnHtml;
              }
            }
          });
        }

        // Summon Skills
        if (smData.skills && smData.skills.length > 0) {
          card.querySelectorAll('[data-summon-skill-idx]').forEach((skEl) => {
            const skIdx = parseInt(skEl.getAttribute('data-summon-skill-idx'), 10);
            const skData = smData.skills[skIdx];
            if (!skData) return;

            const skNameEl = skEl.querySelector('[data-summon-skill-name]');
            if (skNameEl) {
              if (!skNameEl.dataset.origEn) skNameEl.dataset.origEn = skNameEl.textContent.trim();
              skNameEl.textContent = lang === 'vi' ? (skData.name || skNameEl.dataset.origEn) : skNameEl.dataset.origEn;
            }

            const skDescEl = skEl.querySelector('[data-summon-skill-desc]');
            if (skDescEl) {
              if (!skDescEl.dataset.origEnHtml) skDescEl.dataset.origEnHtml = skDescEl.innerHTML;
              if (lang === 'vi') {
                skDescEl.innerHTML = formatRichText(skData.description || skDescEl.dataset.origEnHtml);
              } else {
                skDescEl.innerHTML = skDescEl.dataset.origEnHtml;
              }
            }
          });
        }
      });
    }
  }

  function translateWeaponDetail(bundle, lang) {
    const weaponHeader = document.querySelector('[data-weapon-slug]');
    if (!weaponHeader || !bundle || !bundle.weapons) return;
    const slug = weaponHeader.getAttribute('data-weapon-slug');
    const wdata = bundle.weapons[slug];
    if (!wdata) return;

    // Weapon Name in Header & Breadcrumb
    document.querySelectorAll(`[data-weapon-name]`).forEach((el) => {
      if (!el.dataset.origEn) el.dataset.origEn = el.textContent.trim();
      el.textContent = lang === 'vi' ? (wdata.name || el.dataset.origEn) : el.dataset.origEn;
    });

    // Weapon Stats
    const statsEl = document.querySelector('[data-weapon-stats]');
    if (statsEl) {
      if (!statsEl.dataset.origEn) statsEl.dataset.origEn = statsEl.textContent.trim();
      statsEl.textContent = lang === 'vi' ? (wdata.stats || statsEl.dataset.origEn) : statsEl.dataset.origEn;
    }

    // Weapon Trait
    const traitEl = document.querySelector('.weapon-trait-desc');
    if (traitEl && wdata.trait) {
      if (!traitEl.dataset.origEnHtml) traitEl.dataset.origEnHtml = traitEl.innerHTML;
      if (lang === 'vi') {
        traitEl.innerHTML = formatRichText(wdata.trait);
      } else {
        traitEl.innerHTML = traitEl.dataset.origEnHtml;
      }
    }

    // Weapon Effect
    const effectEl = document.querySelector('.weapon-effect-desc');
    if (effectEl && wdata.effect) {
      if (!effectEl.dataset.origEnHtml) effectEl.dataset.origEnHtml = effectEl.innerHTML;
      if (lang === 'vi') {
        effectEl.innerHTML = formatRichText(wdata.effect);
      } else {
        effectEl.innerHTML = effectEl.dataset.origEnHtml;
      }
    }
  }

  function translateWeaponCards(bundle, lang) {
    if (!bundle || !bundle.weapons) return;
    document.querySelectorAll('.weapon-card[data-slug]').forEach((card) => {
      const slug = card.getAttribute('data-slug');
      const wdata = bundle.weapons[slug];
      if (!wdata) return;

      const nameEl = card.querySelector('.weapon-name');
      if (nameEl) {
        if (!nameEl.dataset.origEn) nameEl.dataset.origEn = nameEl.textContent.trim();
        nameEl.textContent = lang === 'vi' ? (wdata.name || nameEl.dataset.origEn) : nameEl.dataset.origEn;
      }

      const statsEl = card.querySelector('.weapon-stats-text');
      if (statsEl && wdata.stats) {
        if (!statsEl.dataset.origEn) statsEl.dataset.origEn = statsEl.textContent.trim();
        statsEl.textContent = lang === 'vi' ? wdata.stats : statsEl.dataset.origEn;
      }

      const traitBody = card.querySelector('[data-weapon-card-trait]') || card.querySelector('.weapon-trait-body');
      const traitContainer = card.querySelector('.weapon-trait-text');
      if (traitBody && wdata.trait) {
        if (!traitBody.dataset.origEnHtml) traitBody.dataset.origEnHtml = traitBody.innerHTML;
        if (traitContainer && !traitContainer.dataset.origTitle) {
          traitContainer.dataset.origTitle = traitContainer.title || '';
        }
        if (lang === 'vi') {
          traitBody.innerHTML = formatRichText(wdata.trait);
          if (traitContainer) traitContainer.title = wdata.trait.replace(/<[^>]+>/g, '');
        } else {
          traitBody.innerHTML = traitBody.dataset.origEnHtml;
          if (traitContainer && traitContainer.dataset.origTitle) {
            traitContainer.title = traitContainer.dataset.origTitle;
          }
        }
      }
    });
  }

  function translateEffectTriggers(lang) {
    if (!window.GFL2_EFFECTS) return;
    document.querySelectorAll('.effect-trigger').forEach((el) => {
      const effectKey = el.dataset.effectEn || el.getAttribute('data-effect') || el.textContent.trim();
      if (!el.dataset.effectEn) el.dataset.effectEn = effectKey;
      if (!el.dataset.textEn) el.dataset.textEn = el.textContent.trim();
      if (!el.dataset.descEn) el.dataset.descEn = el.getAttribute('data-desc') || '';

      const eff = window.GFL2_EFFECTS[el.dataset.effectEn] || window.GFL2_EFFECTS[el.textContent.trim()];
      if (!eff) return;

      if (lang === 'vi') {
        const viName = eff.name || el.dataset.effectEn;
        const viDesc = eff.desc || el.dataset.descEn;
        el.setAttribute('data-effect', viName);
        el.setAttribute('data-desc', viDesc);
        if (eff.type) {
          el.className = el.className.replace(/effect-(buff|debuff|effect)/g, `effect-${eff.type}`);
          el.setAttribute('data-type', eff.type);
        }
        el.textContent = viName;
      } else {
        el.setAttribute('data-effect', el.dataset.effectEn);
        el.setAttribute('data-desc', el.dataset.descEn);
        el.textContent = el.dataset.textEn;
      }
    });
  }

  function updateSwitcherUI(lang) {
    document.querySelectorAll('.lang-opt').forEach((opt) => {
      if (opt.getAttribute('data-lang') === lang) {
        opt.classList.add('active');
      } else {
        opt.classList.remove('active');
      }
    });
  }

  function applyLanguage(lang) {
    currentLang = lang;
    document.documentElement.lang = lang;
    updateSwitcherUI(lang);

    const bundle = getI18nBundle();
    if (!bundle) return;

    translateStaticUI(bundle, lang);
    translateClassAndPhaseBadges(bundle, lang);
    translateCharacterDetail(bundle, lang);
    translateWeaponDetail(bundle, lang);
    translateWeaponCards(bundle, lang);
    translateEffectTriggers(lang);

    // Broadcast change event
    window.dispatchEvent(new CustomEvent('gfl2-lang-changed', { detail: { lang } }));
  }

  function toggleLanguage() {
    const nextLang = currentLang === 'en' ? 'vi' : 'en';
    localStorage.setItem(STORAGE_KEY, nextLang);
    applyLanguage(nextLang);
  }

  // Public API
  window.GFL2_I18N = {
    get current() {
      return currentLang;
    },
    setLanguage: function (lang) {
      if (lang === 'vi' || lang === 'en') {
        localStorage.setItem(STORAGE_KEY, lang);
        applyLanguage(lang);
      }
    },
    toggle: toggleLanguage
  };

  // Init on DOM ready
  function init() {
    const saved = localStorage.getItem(STORAGE_KEY);
    if (saved === 'vi' || saved === 'en') {
      currentLang = saved;
    } else {
      currentLang = 'en';
    }

    const toggleBtn = document.getElementById('lang-toggle-btn');
    if (toggleBtn) {
      toggleBtn.addEventListener('click', toggleLanguage);
    }

    applyLanguage(currentLang);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
