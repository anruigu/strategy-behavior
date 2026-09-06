'use strict';
// V2 uses the frozen benchmark's action menu. All forms have equal weight;
// optional fields remain blank until selected, and clue text stays editable.
window.UI = window.UI || {};

window.UI.benchmark_move = function (v, ctx) {
  const K = window.KIT;
  const box = K.board();
  K.put(box, K.head({ step: 'Round ' + v.round + ' / ' + v.rounds,
    title: v.title || 'V2 · September 6', scores: [] }));
  if (v.table) {
    const t = v.table;
    K.put(box, K.note('One team · ' + t.score + ' / 6 points · ' + t.tokens + ' clue tokens'));
    const piles = K.el('div', 'human-hanabi-piles');
    ['R', 'B'].forEach(colour => {
      const n = t.piles[colour];
      K.put(piles, K.panel(colour === 'R' ? 'Red pile' : 'Blue pile',
        K.note(n ? 'Built: ' + Array.from({length: n}, (_, i) => i + 1).join(' → ') : 'Empty'),
        K.note(n === 3 ? 'Complete' : 'Next needed: ' + (n + 1))));
    });
    K.put(box, piles, K.note('Goal: build both colours 1 → 2 → 3 in eight turns. No replacement draws.'));
    function hand(title, cards, mine) {
      const row = K.el('div', 'human-hanabi-hand');
      cards.forEach(c => {
        const colour = c.colour === 'R' ? 'Red' : c.colour === 'B' ? 'Blue' : '? colour';
        const card = K.el('div', 'human-hanabi-card ' + (c.colour || 'unknown'));
        K.put(card, K.el('strong', '', colour + ' ' + (c.rank || '?')),
          K.el('span', '', 'Slot ' + c.slot));
        K.put(row, card);
      });
      const p = K.panel(title, cards.length ? row : K.note('No cards left.'));
      if (mine) K.put(p, K.note('Your cards are hidden from you. Teammate clues fill in what you know; ? means unknown. Slots run left to right and shift after a play.'));
      return p;
    }
    K.put(box, hand('Your hand · clue marks', t.own, true), K.note(t.teammate_clue));
    const others = K.el('div', 'human-hanabi-piles');
    t.others.forEach(p => K.put(others, hand('Player ' + p.player + ' · visible hand', p.cards, false)));
    K.put(box, others, K.note('Choose one action below. Give a clue to make a teammate play, or play a card from your own hand.'));
    if (t.discarded.length) K.put(box, K.note('Discarded: ' + t.discarded.map(c => c.join('')).join(', ')));
  } else {
    K.put(box, K.panel('At the table', K.note('Scores: ' + v.scores), K.note(v.state)));
  }
  K.put(box, K.panel('Last resolution', K.note(v.feedback)));

  const forms = K.el('div', 'benchmark-actions');
  v.actions.forEach(action => {
    const panel = K.panel(action.label);
    if (action.help) K.put(panel, K.note(action.help));
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

window.UI.hanabi_human = function (v, ctx) {
  return window.UI.benchmark_move(v, ctx);
};
