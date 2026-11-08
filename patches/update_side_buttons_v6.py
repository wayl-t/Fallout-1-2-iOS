import pathlib, sys
ok = True
def fail(m):
    global ok
    print("ERROR " + m)
    ok = False
def load(p):
    return pathlib.Path(p).read_text(encoding="utf-8", errors="ignore")
def save(p, t):
    pathlib.Path(p).write_text(t, encoding="utf-8")
def rep(path, old, new, label):
    t = load(path)
    if old not in t:
        fail("not found " + label)
        return
    save(path, t.replace(old, new, 1))
    print("patched " + label)
for f in ["work/fallout1-ce/src/plib/gnw/gnw.cc", "work/fallout2-ce/src/window_manager.cc"]:
    rep(f, "if (kk == 517 || kk == 519 || kk == 520 || (kk >= 503 && kk <= 516) || kk >= 536) hasEd = 1;", "if (kk == 517 || kk == 519 || kk == 520) hasEd = 1;", "editor strict " + f)
    rep(f, "if (kk == 116 || kk == 109 || kk == 99) hasSel = 1;", "if (kk == 116) hasSel += 1; if (kk == 109) hasSel += 2; if (kk == 500 || kk == 501) hasSel += 4;", "selector strict " + f)
    rep(f, "else if (hasSel) ctx = 2;", "else if (hasSel >= 7) ctx = 2;", "selector ctx " + f)
    rep(f, "if (kk == 505 || kk == 506) hasLoad = 1;", "if (kk == 502) hasLoad += 1; if (kk == 505 || kk == 506) hasLoad += 2;", "load strict " + f)
    rep(f, "else if (hasPip && !hasLoad) ctx = 7;", "else if (hasPref) ctx = 9; else if (hasPip && hasLoad < 3) ctx = 7;", "pref priority " + f)
    rep(f, "else if (hasLoad) ctx = 5;", "else if (hasLoad >= 3) ctx = 5;", "load ctx " + f)
for f in ["work/fallout1-ce/src/plib/gnw/touch.cc", "work/fallout2-ce/src/touch.cc"]:
    rep(f, "if (idx >= sbn) idx = sbn - 1;", "if (idx >= sbn) return false;", "side no clamp " + f)
    rep(f, "if (dx < 12 && dy < 12) { touch->currentLocation.x = touch->sideX; touch->currentLocation.y = touch->sideY; }", "if (dx < 12 && dy < 12 && touch->currentTimestamp - touch->startTimestamp <= TAP_MAXIMUM_DURATION) { touch->currentLocation.x = touch->sideX; touch->currentLocation.y = touch->sideY; }", "side snap tap only " + f)
if not ok:
    sys.exit("ERROR update_side_buttons_v6 did not fully apply")
print("update_side_buttons_v6 done")
