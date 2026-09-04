'use strict';
/*
  CONTRACT -- work a job, then invoice it.

  Three numbers that mean three different things get three controls with the
  ranges the prompt stated: the hours you work (which cost you), the line you
  tick, and the hours you bill. The running total under them is arithmetic off
  the rate card the player was handed, and it updates as the controls move so
  the shape of the trade is visible while it is being made.
*/
window.UI = window.UI || {};

window.UI.invoice_job = function (v, ctx) {
  const K = window.KIT;
  const rate = K.memo('invoice.rate', v.rate);
  const hrsHi = K.memo('invoice.hoursHi', v.hours_hi) || 24;
  const hrsLo = K.memo('invoice.hoursLo', v.hours_lo) || 0;
  const box = K.board();

  K.put(box, K.head({
    step: 'Job ' + v.job + ' / ' + v.jobs,
    title: 'Contractor ' + v.seat,
    scores: [{ name: 'paid', score: v.paid }, { name: 'effort spent', score: v.spent }],
  }));

  const job = K.panel('the job',
    K.meter({ value: v.difficulty, max: v.effort_hi, label: 'difficulty',
      text: v.difficulty + ' -- done needs at least ' + v.difficulty + ' hours of effort' }));
  if (rate) K.put(job, K.note('The client pays ' + rate.done + ' for done, ' +
    rate.partial + ' for partial, and ' + rate.hour + ' per hour billed.'));

  const rows = (v.log || []).map(r => ({
    cls: r.who === v.seat ? 'mine' : '',
    cells: ['job ' + r.job, 'contractor ' + r.who, r.report, r.billed + 'h', r.paid],
  }));
  const hist = K.panel('the client’s ledger',
    rows.length ? K.table(['', 'who', 'reported', 'billed', 'paid'], rows)
      : K.note('nothing invoiced yet'));

  K.put(box, K.panels(job, hist));

  let report = null;
  const eff = K.dial({ lo: v.effort_lo, hi: v.effort_hi, value: null,
    label: 'hours you actually work (' + v.effort_lo + '-' + v.effort_hi + ')',
    onChange: recount });
  const rep = K.choice(v.reports.map(r => ({ label: r.label, value: r.label })),
    r => { report = r; recount(); });
  const hrs = K.dial({ lo: hrsLo, hi: hrsHi, value: null,
    label: 'hours you bill (' + hrsLo + '-' + hrsHi + ')', onChange: recount });

  const sum = K.note('');
  function recount() {
    if (!rate) { sum.textContent = ''; return; }
    const e = eff.get() || 0, h = hrs.get() || 0;
    if (report === null) { sum.textContent = ''; return; }
    const pay = (report === 'done' ? rate.done : rate.partial) + rate.hour * h;
    sum.textContent = 'This row pays ' + pay + ' and costs ' + e + ' -- net ' +
      K.signed(pay - e) + '.';
  }

  const a = K.act();
  K.put(a, K.el('div', 'bd-panel-h', 'do the work and invoice it'));
  K.put(a, K.panels(K.panel('effort', eff.node), K.panel('report', rep.node),
    K.panel('billed hours', hrs.node)));
  K.put(a, sum);
  const err = K.note('', 'warn');
  K.put(a, err, K.submit('send the invoice', () => {
    if (eff.get() === null) { err.textContent = 'say how many hours you worked.'; return; }
    if (report === null) { err.textContent = 'tick done or partial.'; return; }
    if (hrs.get() === null) { err.textContent = 'say how many hours you are billing.'; return; }
    ctx.send('[effort: ' + eff.get() + '] [report: ' + report +
      '] [hours: ' + hrs.get() + ']', 'ui');
  }));
  K.put(box, a);
  return box;
};
