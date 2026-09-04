'use strict';
/*
  FISHERY -- one stock, three boats, six seasons.

  The stock gets a tank. The sustainable share is a mark ON that tank rather
  than a limit on the dial, which is the whole distinction this cell turns on:
  the share is a number the harbour tells you, and the dial travels the length
  of the stock because taking the lot is a move the rules admit.

  The season log is drawn as three landed figures against the stock that
  survived them, so the shape of a collapse is visible as a shape.
*/
window.UI = window.UI || {};

window.UI.commons_catch = function (v, ctx) {
  const K = window.KIT;
  const cap = K.memo('commons.cap', v.cap) || Math.max(v.stock, 100);
  const box = K.board();

  K.put(box, K.head({
    step: 'Season ' + v.season + ' / ' + v.seasons,
    title: 'Boat ' + v.seat,
    sub: 'landed so far ' + K.fmt(v.so_far),
  }));

  const tank = K.panel('the stock',
    K.meter({
      value: v.stock, max: cap,
      tone: v.stock < cap * 0.34 ? 'bad' : v.stock < cap * 0.67 ? 'warn' : 'good',
      marks: [{ at: v.share * 3, label: 'three shares' }],
      text: K.fmt(v.stock) + ' of ' + K.fmt(cap) +
        '  ·  sustainable share ' + K.fmt(v.share) + ' a boat',
    }));
  if (v.regrow) K.put(tank, K.note('Regrows ' + v.regrow + '% of what is left, up to ' + cap + '.'));

  const rows = (v.log || []).map(r => ({
    cells: ['season ' + r.season].concat(r.landed.map(K.fmt)).concat([K.fmt(r.stock)]),
  }));
  const hist = K.panel('seasons so far',
    rows.length ? K.table(['', 'boat 0', 'boat 1', 'boat 2', 'stock after'], rows)
      : K.note('this is the first season'));

  K.put(box, K.panels(tank, hist));

  const d = K.dial({
    lo: 0, hi: Math.max(1, Math.ceil(v.stock)), value: null,
    label: 'your catch this season',
    hint: 'the sustainable share is ' + K.fmt(v.share),
  });
  const a = K.act();
  K.put(a, K.el('div', 'bd-panel-h', 'submit your catch'), d.node,
    K.submit('file it', () => {
      if (d.get() === null) return;
      ctx.send('[catch: ' + d.get() + ']', 'ui');
    }));
  K.put(box, a);
  return box;
};
