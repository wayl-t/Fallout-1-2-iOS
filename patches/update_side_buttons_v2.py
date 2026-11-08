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
def ins(path, anchor, block, label):
    lines = load(path).splitlines()
    for i, line in enumerate(lines):
        if anchor in line:
            lines[i + 1:i + 1] = block
            save(path, chr(10).join(lines) + chr(10))
            print("patched " + label)
            return
    fail("anchor not found " + label)
def insb(path, anchor, block, label):
    lines = load(path).splitlines()
    for i, line in enumerate(lines):
        if anchor in line:
            lines[i:i] = block
            save(path, chr(10).join(lines) + chr(10))
            print("patched " + label)
            return
    fail("anchor not found " + label)
q = chr(34)
f1_collect = [
"int side_collect_buttons(SideButton* out, int max)",
"{",
"    if (out == NULL || max <= 0) return 0;",
"    for (int wi = num_windows - 1; wi >= 1; wi--) {",
"        Window* w = window[wi];",
"        if (w == NULL) continue;",
"        if ((w->flags & WINDOW_HIDDEN) != 0) continue;",
"        if (w->buttonListHead == NULL) continue;",
"        int n = 0;",
"        for (Button* b = w->buttonListHead; b != NULL && n < max; b = b->next) {",
"            if ((b->flags & BUTTON_FLAG_DISABLED) != 0) continue;",
"            out[n].x = w->rect.ulx + b->rect.ulx + (b->rect.lrx - b->rect.ulx) / 2;",
"            out[n].y = w->rect.uly + b->rect.uly + (b->rect.lry - b->rect.uly) / 2;",
"            out[n].key = b->leftMouseUpEventCode;",
"            int c = out[n].key;",
"            if (c >= 97 && c <= 122) c = c - 32;",
"            if (c >= 32 && c < 127) { out[n].label[0] = (char)c; out[n].label[1] = 0; } else { out[n].label[0] = 42; out[n].label[1] = 0; }",
"            n++;",
"        }",
"        for (int i = 0; i < n; i++) { for (int j = i + 1; j < n; j++) { if (out[j].y < out[i].y || (out[j].y == out[i].y && out[j].x < out[i].x)) { SideButton t = out[i]; out[i] = out[j]; out[j] = t; } } }",
"        if (n > 0) return n;",
"    }",
"    return 0;",
"}"
]
f2_collect = [
"int side_collect_buttons(SideButton* out, int max)",
"{",
"    if (out == NULL || max <= 0) return 0;",
"    for (int wi = gWindowsLength - 1; wi >= 1; wi--) {",
"        Window* w = gWindows[wi];",
"        if (w == NULL) continue;",
"        if ((w->flags & WINDOW_HIDDEN) != 0) continue;",
"        if (w->buttonListHead == NULL) continue;",
"        int n = 0;",
"        for (Button* b = w->buttonListHead; b != NULL && n < max; b = b->next) {",
"            if ((b->flags & BUTTON_FLAG_DISABLED) != 0) continue;",
"            out[n].x = w->rect.left + b->rect.left + (b->rect.right - b->rect.left) / 2;",
"            out[n].y = w->rect.top + b->rect.top + (b->rect.bottom - b->rect.top) / 2;",
"            out[n].key = b->leftMouseUpEventCode;",
"            int c = out[n].key;",
"            if (c >= 97 && c <= 122) c = c - 32;",
"            if (c >= 32 && c < 127) { out[n].label[0] = (char)c; out[n].label[1] = 0; } else { out[n].label[0] = 42; out[n].label[1] = 0; }",
"            n++;",
"        }",
"        for (int i = 0; i < n; i++) { for (int j = i + 1; j < n; j++) { if (out[j].y < out[i].y || (out[j].y == out[i].y && out[j].x < out[i].x)) { SideButton t = out[i]; out[i] = out[j]; out[j] = t; } } }",
"        if (n > 0) return n;",
"    }",
"    return 0;",
"}"
]
for f in ["work/fallout1-ce/src/plib/gnw/touch.cc", "work/fallout2-ce/src/touch.cc"]:
    rep(f, "        if (touch->sideButton) { touch->startLocation.x = touch->sideX; touch->startLocation.y = touch->sideY; touch->currentLocation = touch->startLocation; }", "        // side target kept for tap end, cursor follows real finger", "touch start fix " + f)
    rep(f, "        if (touch->sideButton) { touch->currentLocation.x = touch->sideX; touch->currentLocation.y = touch->sideY; }", "        // keep real position during pan", "touch move fix " + f)
    rep(f, "        if (touch->sideButton) { touch->currentLocation.x = touch->sideX; touch->currentLocation.y = touch->sideY; }", "        if (touch->sideButton) { int dx = touch->currentLocation.x - touch->startLocation.x; if (dx < 0) dx = -dx; int dy = touch->currentLocation.y - touch->startLocation.y; if (dy < 0) dy = -dy; if (dx < 12 && dy < 12) { touch->currentLocation.x = touch->sideX; touch->currentLocation.y = touch->sideY; } }", "touch end tap only " + f)
    rep(f, "    static const int tg[2][4][2] = {{{227, 451}, {227, 459}, {534, 398}, {547, 430}}, {{547, 468}, {547, 449}, {609, 434}, {609, 456}}};", "    SideButton sb[8]; int sbn = side_collect_buttons(sb, 8); if (sbn > 0) { int idx = side * 4 + slot; if (idx >= sbn) idx = sbn - 1; *tx = sb[idx].x; *ty = sb[idx].y; return true; } static const int tg[2][4][2] = {{{227, 451}, {227, 459}, {534, 398}, {547, 430}}, {{547, 468}, {547, 449}, {609, 434}, {609, 456}}};", "touch dynamic target " + f)
insb("work/fallout1-ce/src/plib/gnw/gnw.h", "int win_check_all_buttons();", ["typedef struct SideButton { int x; int y; int key; char label[8]; } SideButton;", "int side_collect_buttons(SideButton* out, int max);"], "f1 side header")
insb("work/fallout2-ce/src/window_manager.h", "int _win_check_all_buttons();", ["typedef struct SideButton { int x; int y; int key; char label[8]; } SideButton;", "int side_collect_buttons(SideButton* out, int max);"], "f2 side header")
insb("work/fallout1-ce/src/plib/gnw/gnw.cc", "int win_check_all_buttons()", f1_collect, "f1 side collect")
insb("work/fallout2-ce/src/window_manager.cc", "int _win_check_all_buttons()", f2_collect, "f2 side collect")
rep("work/fallout2-ce/src/svga.cc", "    SDL_SetRenderDrawColor(gSdlRenderer, 35, 28, 16, 200);", "    SDL_SetRenderDrawColor(gSdlRenderer, 18, 30, 38, 200);", "f2 theme bg")
rep("work/fallout2-ce/src/svga.cc", "    SDL_SetRenderDrawColor(gSdlRenderer, 190, 130, 40, 255);", "    SDL_SetRenderDrawColor(gSdlRenderer, 80, 170, 190, 255);", "f2 theme border")
rep("work/fallout2-ce/src/svga.cc", "    SDL_SetRenderDrawColor(gSdlRenderer, 230, 190, 90, 255);", "    SDL_SetRenderDrawColor(gSdlRenderer, 140, 220, 230, 255);", "f2 theme text")
for f in ["work/fallout1-ce/src/plib/gnw/svga.cc", "work/fallout2-ce/src/svga.cc"]:
    ins(f, "    SDL_Rect vp;", ["    int lw = 0; int lh = 0; SDL_RenderGetLogicalSize(gSdlRenderer, &lw, &lh);", "    float sx = 1.0f; float sy = 1.0f; SDL_RenderGetScale(gSdlRenderer, &sx, &sy);"], "save logical " + f)
    rep(f, "    SDL_RenderSetLogicalSize(gSdlRenderer, screenGetWidth(), screenGetHeight());", "    SDL_RenderSetLogicalSize(gSdlRenderer, lw, lh); SDL_RenderSetScale(gSdlRenderer, sx, sy);", "restore logical " + f)
ll_old = "    static const char* ll[4] = {" + q + "INV" + q + ", " + q + "OPT" + q + ", " + q + "SKL" + q + ", " + q + "MAP" + q + "};"
rl_old = "    static const char* rl[4] = {" + q + "PIP" + q + ", " + q + "CHA" + q + ", " + q + "TURN" + q + ", " + q + "END" + q + "};"
ll_new = "    SideButton dsb[8]; int dsbn = side_collect_buttons(dsb, 8); const char* ll[4] = { dsbn > 0 ? dsb[0].label : " + q + "INV" + q + ", dsbn > 1 ? dsb[1].label : " + q + "OPT" + q + ", dsbn > 2 ? dsb[2].label : " + q + "SKL" + q + ", dsbn > 3 ? dsb[3].label : " + q + "MAP" + q + " };"
rl_new = "    const char* rl[4] = { dsbn > 4 ? dsb[4].label : " + q + "PIP" + q + ", dsbn > 5 ? dsb[5].label : " + q + "CHA" + q + ", dsbn > 6 ? dsb[6].label : " + q + "TURN" + q + ", dsbn > 7 ? dsb[7].label : " + q + "END" + q + " };"
for f in ["work/fallout1-ce/src/plib/gnw/svga.cc", "work/fallout2-ce/src/svga.cc"]:
    rep(f, ll_old, ll_new, "draw dynamic left " + f)
    rep(f, rl_old, rl_new, "draw dynamic right " + f)
if not ok:
    sys.exit("ERROR update_side_buttons_v2 did not fully apply")
print("update_side_buttons_v2 done")
