'use strict';
// V4 board: the same observation the referee sends, laid out around the one
// decision this stage asks for. Everything drawn here comes from `v.present`,
// which the server derives from the public observation alone. The full rules,
// as the referee stated them, stay in the drawer below the board.
window.UI = window.UI || {};

window.V4 = window.V4 || {};
window.V4.historyTable = function (history) {
  const K = window.KIT;
  if (!history || !history.rows || !history.rows.length) return K.note('No completed round yet.');
  return K.table(history.columns, history.rows.map(r => r.map(c => c === null || c === undefined ? '' : String(c))));
};

window.UI.v4_move = function (v, ctx) {
  const K = window.KIT;
  const P = v.present;
  const box = K.board();
  box.classList.add('v4');

  // ── where you are ──────────────────────────────────────────────
  let scores = [];
  try {
    const raw = JSON.parse(v.scores);
    scores = raw.map((s, i) => ({ name: (P.seats && P.seats[i]) || ('Seat ' + i), score: s }));
    if (P.seats && P.seats.length === 1 && raw.length > 1) scores = [{ name: 'Team', score: raw[0] }];
  } catch (e) { scores = []; }
  K.put(box, K.head({ step: 'Round ' + v.round + ' of ' + v.rounds, title: v.title, scores, me: 'You' }));

  const strip = K.el('div', 'v4-stages');
  (P.stages || []).forEach((s, i) => {
    const step = K.el('div', 'v4-stage' + (s.id === P.stage ? ' now' : '') + (s.you_act ? ' you' : ''));
    K.put(step, K.el('span', 'n', String(i + 1)), K.el('span', 'lab', s.label), K.el('span', 'who', s.who));
    K.put(strip, step);
  });
  K.put(box, strip);

  // ── this round ─────────────────────────────────────────────────
  const top = K.el('div', 'v4-top');
  if (P.state && P.state.length) {
    const grid = K.el('div', 'v4-kv');
    P.state.forEach(([label, value]) => {
      K.put(grid, K.el('div', 'k', label), K.el('div', 'v', value));
    });
    K.put(top, K.panel('This round', grid));
  }
  if (P.messages && P.messages.length) {
    const msgs = K.panel('Messages this round');
    P.messages.forEach(m => {
      const q = K.quote(m.from_seat + ' · ' + m.kind, m.text);
      K.put(msgs, q);
    });
    K.put(top, msgs);
  }
  if (P.narrated) {
    K.put(top, K.panel('Last round', K.note(P.narrated)));
  } else if (v.round === 1) {
    K.put(top, K.panel('Last round', K.note('No completed round yet.')));
  }
  K.put(box, top);

  // ── your decision ──────────────────────────────────────────────
  const focus = P.focus || {};
  const decide = K.el('div', 'v4-decide');
  K.put(decide, K.el('div', 'v4-question', focus.question || 'Choose your action.'));
  if (focus.rules && focus.rules.length) {
    const list = K.el('ul', 'v4-rules');
    focus.rules.forEach(n => {
      const text = P.rules && P.rules[n - 1];
      if (text) K.put(list, K.el('li', null, 'Rule ' + n + ': ' + text));
    });
    K.put(decide, list);
  }
  if (focus.next) K.put(decide, K.note('Next: ' + focus.next, 'v4-next'));
  K.put(decide, renderForm(v, P, ctx));
  K.put(box, K.panel('Your decision', decide));

  // ── completed rounds ───────────────────────────────────────────
  if (P.history && P.history.rows && P.history.rows.length) {
    K.put(box, K.panel('Completed rounds', window.V4.historyTable(P.history)));
  }

  // ── all the rules ──────────────────────────────────────────────
  const all = K.el('details', 'v4-allrules');
  K.put(all, K.el('summary', null, 'All rules, numbered, with a worked example'));
  const ol = K.el('ol', 'v4-rules');
  (P.rules || []).forEach(r => K.put(ol, K.el('li', null, r)));
  K.put(all, ol);
  if (P.matrix) {
    K.put(all, K.matrix({ rows: P.matrix.rows, cols: P.matrix.cols, cell: (i, j) => P.matrix.cells[i][j] }));
    if (P.matrix.caption) K.put(all, K.note(P.matrix.caption));
  }
  if (P.example) K.put(all, K.note(P.example, 'v4-example'));
  K.put(box, all);
  return box;

  function renderForm(view, present, context) {
    const wrap = K.el('div', 'v4-form');
    const action = view.actions[0];
    if (!action) return wrap;
    const readers = {};
    const previews = present.previews && present.previews.cells ? present.previews : null;
    const previewBox = K.note('', 'v4-preview');
    const row = K.el('div', 'v4-fields');
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
          const option = K.el('option', '', (f.option_labels && f.option_labels[value]) || value);
          option.value = value;
          K.put(input, option);
        });
        input.addEventListener('change', updatePreview);
      } else {
        input = K.el('input');
        input.type = f.text ? 'text' : 'number';
        input.autocomplete = 'off';
        if (f.text) input.maxLength = 300;
        if (!f.text) {
          input.step = '1';
          if (f.minimum !== null && f.minimum !== undefined) input.min = f.minimum;
          if (f.maximum !== null && f.maximum !== undefined) input.max = f.maximum;
        }
      }
      input.setAttribute('aria-label', f.label);
      input.dataset.field = f.name;
      readers[f.name] = input;
      K.put(label, input);
      if (f.help) K.put(label, K.note(f.help));
      K.put(row, label);
    });
    K.put(wrap, row);
    if (previews) {
      K.put(wrap, previewBox);
      updatePreview();
    }
    const error = K.note('', 'warn');
    error.setAttribute('role', 'alert');
    K.put(wrap, error, K.submit(present.action_label || action.label, () => {
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
          tokens.push(context.fill(f.token, Object.assign({}, values, { value: values[f.name] })));
        }
      });
      context.send(tokens.join(' '), 'ui');
    }));
    return wrap;

    function updatePreview() {
      if (!previews) return;
      const key = previews.fields.map(name => (readers[name] && readers[name].value) || '').join('|');
      if (previews.fields.some(name => !readers[name] || !readers[name].value)) {
        previewBox.textContent = 'Pick an option to see what it pays under the stated rules.';
        previewBox.classList.remove('live');
        return;
      }
      const text = previews.cells[key];
      previewBox.textContent = text || '';
      previewBox.classList.toggle('live', !!text);
    }
  }
};
