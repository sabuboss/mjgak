# 모든 jobs 의 답변 구조 도식(structure-*.png)만 다시 그린다. 캡처·썸네일은 건드리지 않는다.
# python regen_structures.py
import sys, importlib, inspect
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))
import promo_style

done = []
def noop(*a, **k):
    pass

MODULES = ["promo_style", "jobs_urgent", "jobs_pharm", "jobs_ee", "jobs_batch4", "jobs_b5_A", "jobs_b5_B", "jobs_b5_C", "jobs_b5_D",
           "jobs_ssu", "jobs_kw", "jobs_dongduk", "jobs_inha", "jobs_voc", "jobs_jc", "jobs_dodream", "jobs_hufs_int",
           "jobs_ajou_ace", "jobs_sm_talent", "jobs_uos", "jobs_seoultech", "jobs_mju", "jobs_konkuk"]
for name in MODULES:
    try:
        m = importlib.import_module(name)
    except ModuleNotFoundError:
        continue
    m.make_capture = noop
    m.make_thumb = noop
    real = promo_style.make_structure
    def rec(out, *a, _real=real, **k):
        _real(out, *a, **k); done.append(Path(out).name)
    m.make_structure = rec
    for fn_name, fn in inspect.getmembers(m, inspect.isfunction):
        if fn_name.startswith("jobs_") and fn.__module__ == m.__name__ and fn_name != "jobs_restyle_previous":
            try:
                fn()
            except Exception as e:
                print("FAIL", name, fn_name, repr(e)[:120])
print(len(done), "structures:", " ".join(sorted(set(done))))
