"""Durable process-safe budget reservations; ambiguous charges remain reserved."""
import json
import sqlite3
import uuid
from pathlib import Path

class BudgetExceeded(RuntimeError):
    pass

class Ledger:
    def __init__(self, path, ceiling=500.0):
        self.path = str(path)
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        with self.connect() as db:
            db.execute('CREATE TABLE IF NOT EXISTS settings (id INTEGER PRIMARY KEY CHECK(id=1), ceiling REAL)')
            db.execute('INSERT OR IGNORE INTO settings VALUES (1,?)', (ceiling,))
            if db.execute('SELECT ceiling FROM settings').fetchone()[0] != ceiling:
                raise ValueError('Existing budget ceiling differs')
            db.execute('CREATE TABLE IF NOT EXISTS calls (id TEXT PRIMARY KEY, model TEXT, reserved REAL, charged REAL, status TEXT, detail TEXT)')

    def connect(self):
        return sqlite3.connect(self.path, timeout=60)

    def reserve(self, model, amount):
        if amount < 0: raise ValueError('Negative reservation')
        ident = uuid.uuid4().hex
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            ceiling = db.execute('SELECT ceiling FROM settings').fetchone()[0]
            used = db.execute('SELECT COALESCE(SUM(COALESCE(charged,reserved)),0) FROM calls').fetchone()[0]
            if used + amount > ceiling:
                raise BudgetExceeded(f'Budget unavailable: committed ${used:.4f}, request ${amount:.4f}, ceiling ${ceiling:.2f}')
            db.execute('INSERT INTO calls VALUES (?,?,?,?,?,?)', (ident,model,amount,None,'reserved',''))
        return ident

    def settle(self, ident, charged, detail=''):
        if charged is not None and charged < 0: raise ValueError('Negative cost')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row = db.execute('SELECT reserved,status FROM calls WHERE id=?',(ident,)).fetchone()
            if row is None or row[1] != 'reserved': raise ValueError('Unknown or settled reservation')
            # Missing billing data keeps the full upper-bound reservation.
            db.execute('UPDATE calls SET charged=?,status=?,detail=? WHERE id=?',
                       (charged,'settled' if charged is not None else 'unknown',detail,ident))
            if charged is not None and charged > row[0]:
                # Fail closed for subsequent requests if a provider violates our bound.
                db.execute('UPDATE settings SET ceiling=0')

    def summary(self):
        with self.connect() as db:
            ceiling=db.execute('SELECT ceiling FROM settings').fetchone()[0]
            rows=db.execute('SELECT status,COUNT(*),SUM(COALESCE(charged,reserved)),SUM(COALESCE(charged,0)) FROM calls GROUP BY status').fetchall()
        return dict(ceiling_usd=ceiling,committed_usd=sum(r[2] for r in rows),reported_usd=sum(r[3] for r in rows),states={r[0]:dict(calls=r[1],committed_usd=r[2]) for r in rows})
