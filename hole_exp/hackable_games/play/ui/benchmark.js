'use strict';
// V2 uses the frozen benchmark's action menu. All forms have equal weight;
// optional fields remain blank until selected, and clue text stays editable.
window.UI = window.UI || {};

window.UI.benchmark_move = function (v, ctx) {
  const K = window.KIT;
  const box = K.board();
  K.put(box, K.head({ step: 'Round ' + v.round + ' / ' + v.rounds,
    title: 'V2 · September 6', scores: [] }));
  K.put(box, K.panel('At the table', K.note('Scores: ' + v.scores),
    K.note(v.state)), K.panel('Last resolution', K.note(v.feedback)));

  const forms = K.el('div', 'benchmark-actions');
  v.actions.forEach(action => {
    const panel = K.panel(action.label);
    const readers = {};
    action.fields.forEach(f => {
      const label = K.el('label', 'benchmark-field');
      K.put(label, K.el('span', 'lab', f.label));
      let input;
      if (f.options) {
        input = K.el('select');
        const empty = K.el('option', '', f.optional ? 'None' : 'Choose…');
        empty.value = '';
        K.put(input, empty);
        f.options.forEach(value => {
          const option = K.el('option', '', value);
          option.value = value;
          K.put(input, option);
        });
      } else {
        input = K.el('input');
        input.type = f.text ? 'text' : 'number';
        input.autocomplete = 'off';
        if (!f.text) {
          input.step = '1';
          if (f.minimum !== null) input.min = f.minimum;
          if (f.maximum !== null) input.max = f.maximum;
        }
      }
      input.setAttribute('aria-label', f.label);
      input.dataset.field = f.name;
      readers[f.name] = input;
      K.put(label, input);
      K.put(panel, label);
    });
    const error = K.note('', 'warn');
    error.setAttribute('role', 'alert');
    K.put(panel, error, K.submit(action.label, () => {
      const values = {};
      for (const f of action.fields) {
        const input = readers[f.name];
        const value = input.value.trim();
        if (!value && !f.optional) {
          error.textContent = 'Choose ' + f.label.toLowerCase() + '.';
          input.focus();
          return;
        }
        if (value && !input.checkValidity()) {
          input.reportValidity();
          return;
        }
        values[f.name] = value;
      }
      const tokens = action.token ? [action.token] : [];
      action.fields.forEach(f => {
        if (values[f.name] && f.token) {
          tokens.push(ctx.fill(f.token, Object.assign({}, values, { value: values[f.name] })));
        }
      });
      ctx.send(tokens.join(' '), 'ui');
    }));
    K.put(forms, panel);
  });
  K.put(box, forms);
  return box;
};
