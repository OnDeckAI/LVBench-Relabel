"""Recompute every published count for the LVBench relabel from the two parquets.

A 'repair' is a change to the correct option's TEXT. Comparing text rather than
the option letter makes the measure invariant to option reordering; comparing
case/punctuation-normalized text makes it invariant to typography fixes.
"""
import sys, re, unicodedata, pandas as pd

OPT = re.compile(r'^\(([A-D])\)\s*(.*)$')
def split(q):
    L = q.split('\n'); return L[0].strip(), {m.group(1): m.group(2).strip()
        for ln in L[1:] if (m := OPT.match(ln.strip()))}
def norm(s):
    s = unicodedata.normalize('NFKC', s or '').lower()
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s)).strip()

def flags(new, old):
    assert (new.index == old.index).all(), "uid misalignment"
    out = {}
    for uid in new.index:
        ns, no_ = split(new.loc[uid, 'question']); os_, oo = split(old.loc[uid, 'question'])
        nl, ol = new.loc[uid, 'answer'], old.loc[uid, 'answer']
        nt, ot = norm(no_.get(nl)), norm(oo.get(ol))
        out[uid] = dict(
            key_changed = nt != ot,
            stem_changed = norm(ns) != norm(os_),
            distractors_changed = sorted(norm(v) for k, v in no_.items() if k != nl)
                               != sorted(norm(v) for k, v in oo.items() if k != ol),
            key_is_original_option = nt in {norm(v) for v in oo.values()},
        )
    return pd.DataFrame(out).T

if __name__ == '__main__':
    new = pd.read_parquet(sys.argv[1]).set_index('uid').sort_index()
    old = pd.read_parquet(sys.argv[2]).set_index('uid').sort_index()
    f = flags(new, old); N = len(f)
    print(f"items: {N}")
    for c in ['key_changed', 'stem_changed', 'distractors_changed']:
        print(f"  {c:22s} {int(f[c].sum()):5d}  ({f[c].mean():5.1%})")
    any_ = f[['key_changed','stem_changed','distractors_changed']].any(axis=1)
    print(f"  {'any of the three':22s} {int(any_.sum()):5d}  ({any_.mean():5.1%})")
    kc = f[f.key_changed]
    print(f"\n  of the {len(kc)} repairs: {int(kc.key_is_original_option.sum())} promoted an existing "
          f"option, {int((~kc.key_is_original_option).sum())} use rewritten text")
    agree = (new['repair_decision'] == f.key_changed.map({True:'repair', False:'keep'})).all()
    print(f"\n  repair_decision matches key_changed on every row: {agree}")
