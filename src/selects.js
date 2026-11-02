// Select-only comboboxes: one focusable trigger, keyboard navigation and native values.
const selectWidgets = [...document.querySelectorAll('[data-select]')].map(root => ({
  root, select: $(root.dataset.select), trigger: $(root.dataset.select + 'Trigger'),
  menu: $(root.dataset.select + 'Options'), value: $(root.dataset.select + 'Value'), active: 0
}));
let openSelect = null;

function paintSelect(widget) {
  const {select, trigger, menu, value} = widget;
  const selected = [...select.options].findIndex(option => option.value === select.value);
  value.textContent = select.options[selected]?.textContent || '';
  menu.innerHTML = [...select.options].map((option, index) =>
    `<div class="select-option${index === widget.active ? ' is-active' : ''}" id="${select.id}Option${index}" role="option" aria-selected="${index === selected}" data-option="${index}"><span>${esc(option.textContent)}</span><span class="option-check" aria-hidden="true">${index === selected ? '✓' : ''}</span></div>`).join('');
  if (openSelect === widget) trigger.setAttribute('aria-activedescendant', `${select.id}Option${widget.active}`);
}

function closeSelect() {
  if (!openSelect) return;
  openSelect.menu.hidden = true;
  openSelect.trigger.setAttribute('aria-expanded', 'false');
  openSelect.trigger.removeAttribute('aria-activedescendant');
  openSelect = null;
}

function showSelect(widget, index) {
  closeSelect();
  widget.active = index ?? widget.select.selectedIndex;
  openSelect = widget;
  paintSelect(widget);
  widget.menu.hidden = false;
  widget.trigger.setAttribute('aria-expanded', 'true');
}

function chooseSelect(widget, index) {
  widget.select.selectedIndex = index;
  closeSelect();
  paintSelect(widget);
  widget.trigger.focus({preventScroll: true});
  widget.select.dispatchEvent(new Event('change', {bubbles: true}));
}

function syncSelects() {
  for (const widget of selectWidgets) {
    if (openSelect !== widget) widget.active = widget.select.selectedIndex;
    paintSelect(widget);
  }
}

for (const widget of selectWidgets) {
  widget.trigger.addEventListener('click', () => openSelect === widget ? closeSelect() : showSelect(widget));
  widget.menu.addEventListener('click', event => {
    const option = event.target.closest('[data-option]');
    if (option) chooseSelect(widget, Number(option.dataset.option));
  });
  widget.menu.addEventListener('pointermove', event => {
    const option = event.target.closest('[data-option]');
    if (!option || openSelect !== widget) return;
    widget.active = Number(option.dataset.option);
    widget.menu.querySelectorAll('.select-option').forEach(el => el.classList.toggle('is-active', el === option));
    widget.trigger.setAttribute('aria-activedescendant', option.id);
  });
  widget.trigger.addEventListener('keydown', event => {
    const {key} = event;
    const count = widget.select.options.length;
    if (key === 'Tab') return closeSelect();
    if (key === 'Escape') { closeSelect(); event.preventDefault(); return; }
    if (!['ArrowDown', 'ArrowUp', 'Home', 'End', 'Enter', ' '].includes(key)) return;
    event.preventDefault();
    if (key === 'Enter' || key === ' ') {
      return openSelect === widget ? chooseSelect(widget, widget.active) : showSelect(widget);
    }
    if (openSelect !== widget) {
      showSelect(widget, key === 'Home' ? 0 : key === 'End' ? count - 1 : undefined);
    } else {
      widget.active = key === 'Home' ? 0 : key === 'End' ? count - 1 :
        Math.max(0, Math.min(count - 1, widget.active + (key === 'ArrowDown' ? 1 : -1)));
      paintSelect(widget);
    }
    $(widget.select.id + 'Option' + widget.active)?.scrollIntoView({block: 'nearest'});
  });
}
document.addEventListener('click', event => {
  if (openSelect && !openSelect.root.contains(event.target)) closeSelect();
});
window.addEventListener('resize', closeSelect);

document.addEventListener("focusin", event => {
  if (openSelect && !openSelect.root.contains(event.target)) closeSelect();
});
