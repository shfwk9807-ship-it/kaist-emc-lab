(() => {
  'use strict';
  const readDismissed = key => { try { return Number(localStorage.getItem(key) || 0); } catch { return 0; } };
  const writeDismissed = (key, until) => { try { localStorage.setItem(key, String(until)); } catch { /* The notice will reappear on the next page. */ } };
  function safeLink(value) {
    if (typeof value !== 'string' || !value.trim()) return null;
    try {
      const url = new URL(value, location.href);
      if (!['http:', 'https:'].includes(url.protocol)) return null;
      return url.href;
    } catch { return null; }
  }
  async function showAnnouncement() {
    let config;
    try {
      const response = await fetch('data/announcement.json');
      if (!response.ok) return;
      config = await response.json();
    } catch { return; }
    if (!config || config.enabled !== true || typeof config.title !== 'string' || !config.title.trim() || typeof config.message !== 'string' || !config.message.trim()) return;
    const id = typeof config.id === 'string' && config.id.trim() ? config.id.trim() : 'default';
    const key = 'emclab-notice:' + id;
    if (readDismissed(key) > Date.now()) return;
    const dialog = document.createElement('dialog');
    if (typeof dialog.showModal !== 'function') return;
    dialog.className = 'announcement';
    dialog.setAttribute('aria-labelledby', 'announcement-title');
    const heading = document.createElement('h2');
    heading.id = 'announcement-title';
    heading.textContent = config.title;
    const label = document.createElement('p');
    label.className = 'announcement-label';
    label.textContent = 'NOTICE / EMC LAB';
    const message = document.createElement('p');
    message.className = 'announcement-message';
    message.textContent = config.message;
    const close = document.createElement('button');
    close.className = 'announcement-close';
    close.type = 'button';
    close.setAttribute('aria-label', 'Close notice');
    close.textContent = '×';
    const actions = document.createElement('div');
    actions.className = 'announcement-actions';
    const link = safeLink(config.link_url);
    if (link && typeof config.link_text === 'string' && config.link_text.trim()) {
      const anchor = document.createElement('a');
      anchor.href = link;
      anchor.textContent = config.link_text;
      if (new URL(link).origin !== location.origin) { anchor.target = '_blank'; anchor.rel = 'noopener noreferrer'; }
      actions.append(anchor);
    }
    const later = document.createElement('button');
    later.type = 'button';
    const hours = Number(config.dismiss_hours);
    const validHours = Number.isFinite(hours) && hours > 0 && hours <= 720 ? hours : 24;
    later.textContent = `Do not show for ${validHours} hours`;
    actions.append(later);
    dialog.append(close, label, heading, message, actions);
    document.body.append(dialog);
    let previouslyFocused = document.activeElement;
    const dismiss = () => dialog.close();
    close.addEventListener('click', dismiss);
    later.addEventListener('click', () => { writeDismissed(key, Date.now() + validHours * 3600000); dismiss(); });
    dialog.addEventListener('click', event => { if (event.target === dialog) dismiss(); });
    dialog.addEventListener('close', () => { dialog.remove(); if (previouslyFocused instanceof HTMLElement) previouslyFocused.focus(); });
    dialog.showModal();
    close.focus();
  }
  showAnnouncement();
})();
