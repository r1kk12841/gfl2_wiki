(function exposeGuideRichText(root) {
  'use strict';

  const ALLOWED_TAGS = new Set([
    'b', 'strong', 'i', 'em', 'u', 'span', 'code', 'br', 'a',
    'p', 'ul', 'ol', 'li', 'img',
  ]);
  const DROP_CONTENT_TAGS = new Set(['script', 'style', 'iframe', 'object', 'embed', 'svg', 'math']);
  const ALLOWED_CLASSES = new Set([
    'guide-text-red', 'guide-text-orange', 'guide-text-blue', 'guide-text-green',
    'guide-text-burn', 'guide-text-electric', 'guide-text-hydro', 'guide-text-corrosion',
    'guide-text-physical', 'guide-text-freeze', 'guide-text-resonance',
    'guide-highlight-yellow', 'guide-highlight-green', 'guide-highlight-blue', 'guide-highlight-pink',
    'guide-font-small', 'guide-font-large', 'guide-font-xlarge',
    'guide-align-left', 'guide-align-center', 'guide-align-right',
    'guide-inline-ref', 'guide-inline-character', 'guide-inline-weapon',
    'guide-inline-skill', 'guide-inline-effect', 'guide-inline-icon',
    'guide-ref-popover', 'guide-weapon-popover', 'guide-weapon-popover-image',
    'guide-weapon-popover-name', 'guide-weapon-popover-desc',
    'guide-skill-popover', 'guide-skill-popover-name', 'guide-skill-popover-desc',
    'effect-trigger', 'effect-buff', 'effect-debuff', 'effect-effect',
  ]);
  const SAFE_EFFECT_ATTRIBUTES = new Set([
    'data-effect-id', 'data-effect', 'data-effect-en', 'data-text-en',
    'data-type', 'data-desc', 'data-desc-en', 'tabindex',
  ]);

  function isSafeHref(value) {
    const href = String(value || '').trim();
    return /^(https?:|mailto:|\/|\.\/|\.\.\/|#)/i.test(href);
  }

  function isSafeImageSrc(value) {
    const src = String(value || '').trim();
    return /^(?:(?:\.\.\/)+|\.\/|\/)?assets\/images\/[^<>]+$/i.test(src);
  }

  function sanitizeRichHTML(input) {
    if (typeof document === 'undefined') return String(input || '');
    const source = document.createElement('template');
    source.innerHTML = String(input || '');
    const output = document.createElement('template');

    function cleanNode(node) {
      if (node.nodeType === Node.TEXT_NODE) return document.createTextNode(node.textContent || '');
      if (node.nodeType !== Node.ELEMENT_NODE) return document.createDocumentFragment();

      const tag = node.tagName.toLowerCase();
      if (DROP_CONTENT_TAGS.has(tag)) return document.createDocumentFragment();
      // Chromium commonly emits <div> when Enter is pressed in contenteditable.
      // Normalize it to a supported paragraph instead of flattening line breaks.
      const normalizedTag = tag === 'div' ? 'p' : tag;

      const fragment = document.createDocumentFragment();
      Array.from(node.childNodes).forEach(child => fragment.append(cleanNode(child)));
      if (!ALLOWED_TAGS.has(normalizedTag)) return fragment;

      const clean = document.createElement(normalizedTag);
      const classes = Array.from(node.classList || []).filter(name => ALLOWED_CLASSES.has(name));
      if (classes.length) clean.className = classes.join(' ');
      const title = node.getAttribute('title');
      if (title) clean.setAttribute('title', title);
      if (normalizedTag === 'span') {
        SAFE_EFFECT_ATTRIBUTES.forEach(attribute => {
          if (!node.hasAttribute(attribute)) return;
          clean.setAttribute(attribute, attribute === 'tabindex' ? '0' : node.getAttribute(attribute));
        });
      }
      if (normalizedTag === 'a') {
        const href = node.getAttribute('href');
        if (isSafeHref(href)) {
          clean.setAttribute('href', href.trim());
          clean.setAttribute('target', '_blank');
          clean.setAttribute('rel', 'noopener');
        }
      }
      if (normalizedTag === 'img') {
        const src = node.getAttribute('src');
        if (isSafeImageSrc(src)) clean.setAttribute('src', src.trim());
        const alt = node.getAttribute('alt');
        if (alt) clean.setAttribute('alt', alt);
        clean.setAttribute('loading', 'lazy');
      }
      clean.append(fragment);
      return clean;
    }

    Array.from(source.content.childNodes).forEach(node => output.content.append(cleanNode(node)));
    return output.innerHTML
      .replace(/(?:<br>\s*){3,}/gi, '<br><br>')
      .replace(/^(?:\s|&nbsp;)+|(?:\s|&nbsp;)+$/gi, '');
  }

  function textToHTML(text) {
    const holder = document.createElement('div');
    holder.textContent = String(text || '');
    return holder.innerHTML.replace(/\r?\n/g, '<br>');
  }

  const api = { ALLOWED_CLASSES, sanitizeRichHTML, textToHTML, isSafeHref, isSafeImageSrc };
  root.GuideRichText = api;
  if (typeof module !== 'undefined' && module.exports) module.exports = api;
})(typeof globalThis !== 'undefined' ? globalThis : window);
