import pathlib, sys, re
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
def rep_opt(path, old, new, label):
    t = load(path)
    if old not in t:
        print("skip " + label)
        return
    save(path, t.replace(old, new, 1))
    print("patched " + label)
def rep_re(path, pat, new, label):
    t = load(path)
    nt, n = re.subn(pat, new, t, count=1)
    if n == 0:
        fail("not found " + label)
        return
    save(path, nt)
    print("patched " + label)
def replace_func(path, sig, new_lines, label):
    t = load(path)
    i = t.find(sig)
    if i < 0:
        fail("not found " + label)
        return
    j = t.find("{", i)
    if j < 0:
        fail("brace " + label)
        return
    depth = 0
    k = j
    while k < len(t):
        if t[k] == "{":
            depth += 1
        elif t[k] == "}":
            depth -= 1
            if depth == 0:
                break
        k += 1
    save(path, t[:i] + chr(10).join(new_lines) + chr(10) + t[k+1:])
    print("patched " + label)
q = chr(34)
G = {1040: "01110100011000111111100011000110001",
1041: "11110100001000011110100011000111110",
1042: "11110100011000111110100011000111110",
1043: "11111100001000010000100001000010000",
1044: "00100010100101001010100011111110001",
1045: "11111100001000011110100001000011111",
1025: "01010000001111110000111101000011111",
1046: "10101101010101011111010101010110101",
1047: "01110100010000100110000011000101110",
1048: "10001100111010111001100011000110001",
1049: "01010001001000110011101011100110001",
1050: "10001100101010011000101001001010001",
1051: "00110010100101001010100011000110001",
1052: "10001110111010110101100011000110001",
1053: "10001100011000111111100011000110001",
1054: "01110100011000110001100011000101110",
1055: "11111100011000110001100011000110001",
1056: "11110100011000111110100001000010000",
1057: "01110100011000010000100001000101110",
1058: "11111001000010000100001000010000100",
1059: "10001100011000101010001000010000100",
1060: "00100011101010110101011100010000100",
1061: "10001100010101000100010101000110001",
1062: "10001100011000110001100011111100001",
1063: "10001100011000101111000010000100001",
1064: "10001100011000110001100011000111111",
1065: "10001100011000110001101011111100001",
1066: "11000010000100001110010010100101110",
1067: "10010100101001011110100011000111110",
1068: "10000100001000011110100011000111110",
1069: "01110100010000100111000011000101110",
1070: "10110100011010111101101011000110010",
1071: "01111100011000101110001000100010000"}
for _i in range(32):
    G[1072 + _i] = G[1040 + _i]
G[1105] = G[1025]
G[65] = G[1040]
G[66] = G[1042]
G[67] = G[1057]
G[69] = G[1045]
G[70] = "11111100001000011110100001000010000"
G[72] = G[1053]
G[75] = G[1050]
G[77] = G[1052]
G[79] = G[1054]
G[80] = G[1056]
G[84] = G[1058]
G[88] = G[1061]
G[89] = G[1059]
G[68] = "11100100101000110001100011001011100"
G[71] = "01110100011000010111100011000101111"
G[73] = "11111001000010000100001000010011111"
G[74] = "00111000100001000010000101001001100"
G[76] = "10000100001000010000100001000011111"
G[78] = "10001110011010110011100011000110001"
G[81] = "01110100011000110001101011001001101"
G[82] = "11110100011000111110101001001010001"
G[83] = "01111100001000001110000010000111110"
G[85] = "10001100011000110001100011000101110"
G[86] = "10001100011000110001100010101000100"
G[87] = "10001100011000110101101011010101010"
G[90] = "11111000010001000100010001000011111"
G[46] = "00000000000000000000000000000000010"
G[45] = "00000000000000011111000000000000000"
G[43] = "00000001000010011111001000010000000"
G[42] = "00000101010111010101000000000000000"
G[63] = "01110100010000100110001000000000100"
for _cp, _b in G.items():
    if len(_b) != 35:
        fail("glyph len " + str(_cp) + " " + str(len(_b)))
ru = [
"static const char* side_ru_label(int key, int ctx)",
"{",
"    static char nb[16];"
"    if (key == 27) return " + q + "НАЗАД" + q + ";"
"    if (ctx == 3) {"
"        if (key == 500) return " + q + "ГОТОВО" + q + ";"
"        if (key == 501) return " + q + "ОПЦИИ" + q + ";"
"        if (key == 502) return " + q + "ОТМЕНА" + q + ";"
"        if (key >= 503 && key <= 509) return " + q + "+" + q + ";"
"        if (key >= 510 && key <= 516) return " + q + "-" + q + ";"
"        if (key == 517) return " + q + "ИМЯ" + q + ";"
"        if (key == 519) return " + q + "ВОЗРАСТ" + q + ";"
"        if (key == 520) return " + q + "ПОЛ" + q + ";"
"        if (key == 521 || key == 522) return " + q + "+" + q + ";"
"        if (key == 523 || key == 524) return " + q + "-" + q + ";"
"        if (key >= 525 && key < 535) return " + q + "ИНФО" + q + ";"
"        if (key == 535) return " + q + "ПАПКА" + q + ";"
"        if (key >= 536 && key < 554) return " + q + "НАВЫК" + q + ";"
"        if (key >= 555 && key < 600) return " + q + "ЧЕРТА" + q + ";"
"        return " + q + "ДЕЙСТВ." + q + ";"
"    }"
"    if (ctx == 2) {"
"        if (key == 500) return " + q + "ПРЕД." + q + ";"
"        if (key == 501) return " + q + "СЛЕД." + q + ";"
"        if (key == 116 || key == 84) return " + q + "ВЗЯТЬ" + q + ";"
"        if (key == 109 || key == 77) return " + q + "ИЗМЕН." + q + ";"
"        if (key == 99 || key == 67) return " + q + "СОЗДАТЬ" + q + ";"
"        return " + q + "МЕНЮ" + q + ";"
"    }"
"    if (ctx == 1) {"
"        if (key == 105 || key == 73) return " + q + "ВСТУПЛ." + q + ";"
"        if (key == 110 || key == 78) return " + q + "НОВАЯ" + q + ";"
"        if (key == 108 || key == 76) return " + q + "ЗАГРУЗ." + q + ";"
"        if (key == 111 || key == 79) return " + q + "НАСТР." + q + ";"
"        if (key == 99 || key == 67) return " + q + "ТИТРЫ" + q + ";"
"        if (key == 101 || key == 69) return " + q + "ВЫХОД" + q + ";"
"        return " + q + "МЕНЮ" + q + ";"
"    }"
"    if (ctx == 4) {"
"        if (key == 500) return " + q + "СЛОЖН." + q + ";"
"        if (key == 501) return " + q + "НАСИЛИЕ" + q + ";"
"        if (key == 502) return " + q + "ЦЕЛЬ" + q + ";"
"        if (key == 503) return " + q + "БОЙ" + q + ";"
"        if (key == 504) return " + q + "ТЕКСТ" + q + ";"
"        if (key == 505) return " + q + "СУБТИТ." + q + ";"
"        if (key == 506) return " + q + "ЗВУК" + q + ";"
"        if (key == 507) return " + q + "МУЗЫКА" + q + ";"
"        if (key == 508) return " + q + "ЯРКОСТЬ" + q + ";"
"        if (key == 509) return " + q + "ПРОКРУТ." + q + ";"
"        return " + q + "НАСТР." + q + ";"
"    }"
"    if (ctx == 5) {"
"        if (key == 500) return " + q + "ГОТОВО" + q + ";"
"        if (key == 501) return " + q + "ОТМЕНА" + q + ";"
"        if (key == 502) return " + q + "СЛОТ" + q + ";"
"        if (key == 503 || key == 504) return " + q + "ВНИЗ" + q + ";"
"        if (key == 505 || key == 506) return " + q + "ВВЕРХ" + q + ";"
"        return " + q + "ФАЙЛ" + q + ";"
"    }"
"    if (ctx == 7) {"
"        if (key == 500) return " + q + "СТАТУС" + q + ";"
"        if (key == 501) return " + q + "КАРТА" + q + ";"
"        if (key == 502) return " + q + "ВИДЕО" + q + ";"
"        if (key == 503 || key == 504) return " + q + "БУДИЛЬН." + q + ";"
"        if (key >= 505 && key <= 527) return " + q + "ЗАПИСЬ" + q + ";"
"        if (key == 528) return " + q + "НАЗАД" + q + ";"
"        return " + q + "ПИП-БОЙ" + q + ";"
"    }"
"    if (ctx == 8) {"
"        if (key == 115 || key == 83) return " + q + "СКАНЕР" + q + ";"
"        if (key == 104 || key == 72 || key == 108 || key == 76) return " + q + "ВИД" + q + ";"
"        return " + q + "КАРТА" + q + ";"
"    }"
"    if (ctx == 9) {"
"        if (key == 504) return " + q + "ГОТОВО" + q + ";"
"        if (key == 527) return " + q + "СБРОС" + q + ";"
"        if (key == 528) return " + q + "ОТМЕНА" + q + ";"
"        if (key >= 505 && key <= 524) { snprintf(nb, sizeof(nb), " + q + "НАСТР.%d" + q + ", key - 504); return nb; }"
"        return " + q + "НАСТР." + q + ";"
"    }"
"    if (key == 105 || key == 73) return " + q + "ВЕЩИ" + q + ";"
"    if (key == 111 || key == 79) return " + q + "НАСТР." + q + ";"
"    if (key == 115 || key == 83) return " + q + "НАВЫКИ" + q + ";"
"    if (key == 9) return " + q + "КАРТА" + q + ";"
"    if (key == 112 || key == 80) return " + q + "ПИП-БОЙ" + q + ";"
"    if (key == 99 || key == 67) return " + q + "ПЕРСОН." + q + ";"
"    if (key == 98 || key == 66) return " + q + "РУКИ" + q + ";"
"    if (key == 97 || key == 65) return " + q + "АТАКА" + q + ";"
"    if (key == 32) return " + q + "ХОД" + q + ";"
"    if (key == 13) return " + q + "ГОТОВО" + q + ";"
"    return " + q + "ДЕЙСТВ." + q + ";"
"}"]
collect_head = [
"int side_collect_buttons(SideButton* out, int max)",
"{",
"    if (out == NULL || max <= 0) return 0;",
"    SideButton tmp[64]; int tn = 0;",
"    int ctx = 0; int hasEd = 0; int hasSel = 0; int hasPip = 0; int hasLoad = 0; int hasPref = 0; int has115 = 0; int has27 = 0;",
"    int sc[64]; int n = 0; int seenPlus = 0; int seenMinus = 0; int seenTag = 0; int seenTrait = 0;"]
collect_tail = [
"        if (tn == 0) continue;",
"        for (int k = 0; k < tn; k++) { int kk = tmp[k].key; if (kk == 517 || kk == 519 || kk == 520 || (kk >= 503 && kk <= 516) || kk >= 536) hasEd = 1; if (kk == 116 || kk == 109 || kk == 99) hasSel = 1; if (kk == 504) hasPip = 1; if (kk == 505 || kk == 506) hasLoad = 1; if (kk == 527 || kk == 528) hasPref = 1; if (kk == 115) has115 = 1; if (kk == 27) has27 = 1; }"
"        if (hasEd) ctx = 3;",
"        else if (hasSel) ctx = 2;",
"        else if (hasPip && !hasLoad) ctx = 7;",
"        else if (hasLoad) ctx = 5;",
"        else if (hasPref) ctx = 9;",
"        else { int cont = tn >= 6; for (int k = 0; k < tn; k++) if (tmp[k].key < 500 || tmp[k].key > 509) cont = 0; if (cont) ctx = 4; }"
"        if (ctx == 0) { int hasI = 0, hasN = 0, hasL = 0; for (int k = 0; k < tn; k++) { if (tmp[k].key == 105 || tmp[k].key == 73) hasI = 1; if (tmp[k].key == 110 || tmp[k].key == 78) hasN = 1; if (tmp[k].key == 108 || tmp[k].key == 76) hasL = 1; } if (hasI && hasN && hasL) ctx = 1; }"
"        if (ctx == 0 && has115 && has27) ctx = 8;",
"        for (int k = 0; k < tn; k++) { int kk = tmp[k].key; int s = 50; if (ctx == 3) { if (kk == 500 || kk == 501 || kk == 502) s = 100; else if (kk == 517 || kk == 519 || kk == 520) s = 90; else if ((kk >= 503 && kk <= 516) || kk == 521 || kk == 522 || kk == 523 || kk == 524) s = 80; else if (kk >= 536 && kk < 554) s = 30; else if (kk >= 555) s = 30; else s = 20; } else if (ctx == 5) { if (kk == 500) s = 100; else if (kk == 501) s = 90; else if (kk == 503 || kk == 505) s = 70; else if (kk == 502) s = 10; } else if (ctx == 7) { if (kk >= 500 && kk <= 504) s = 90; else s = 20; } else if (ctx == 9) { if (kk == 504) s = 100; else if (kk == 527) s = 90; else s = 40; } sc[k] = s; }"
"        for (int i = 0; i < tn; i++) { for (int j = i + 1; j < tn; j++) { if (sc[j] > sc[i] || (sc[j] == sc[i] && (tmp[j].y < tmp[i].y || (tmp[j].y == tmp[i].y && tmp[j].x < tmp[i].x)))) { SideButton t = tmp[i]; tmp[i] = tmp[j]; tmp[j] = t; int ts = sc[i]; sc[i] = sc[j]; sc[j] = ts; } } }"
"        n = 0; seenPlus = 0; seenMinus = 0; seenTag = 0; seenTrait = 0;",
"        for (int k = 0; k < tn && n < max; k++) { int kk = tmp[k].key; int isPlus = (kk >= 503 && kk <= 509) || kk == 521 || kk == 522; int isMinus = (kk >= 510 && kk <= 516) || kk == 523 || kk == 524; int isTag = kk >= 536 && kk < 554; int isTrait = kk >= 555 && kk < 600; if (isPlus && seenPlus) continue; if (isMinus && seenMinus) continue; if (isTag && seenTag) continue; if (isTrait && seenTrait) continue; if (isPlus) seenPlus = 1; if (isMinus) seenMinus = 1; if (isTag) seenTag = 1; if (isTrait) seenTrait = 1; out[n] = tmp[k]; n++; }"
"        for (int i = 0; i < n; i++) { for (int j = i + 1; j < n; j++) { if (out[j].y < out[i].y || (out[j].y == out[i].y && out[j].x < out[i].x)) { SideButton t = out[i]; out[i] = out[j]; out[j] = t; } } }"
"        for (int k = 0; k < n; k++) { const char* s = side_ru_label(out[k].key, ctx); int qi = 0; while (s[qi] != 0 && qi < 23) { out[k].label[qi] = s[qi]; qi++; } out[k].label[qi] = 0; }"
"        if (n > 0) return n;",
"    }",
"    return 0;",
"}"]
f1_mid = [
"    for (int wi = num_windows - 1; wi >= 1; wi--) {",
"        Window* w = window[wi];",
"        if (w == NULL) continue;",
"        if ((w->flags & WINDOW_HIDDEN) != 0) continue;",
"        if (w->buttonListHead == NULL) continue;",
"        tn = 0;",
"        for (Button* b = w->buttonListHead; b != NULL && tn < 64; b = b->next) {",
"            if ((b->flags & BUTTON_FLAG_DISABLED) != 0) continue;",
"            int k = b->leftMouseUpEventCode;",
"            if (k == -1) continue;",
"            int bw = b->rect.lrx - b->rect.ulx; int bh = b->rect.lry - b->rect.uly;",
"            if (bw <= 0 || bh <= 0) continue;",
"            tmp[tn].x = w->rect.ulx + b->rect.ulx + bw / 2;",
"            tmp[tn].y = w->rect.uly + b->rect.uly + bh / 2;",
"            tmp[tn].w = bw; tmp[tn].h = bh; tmp[tn].key = k; tmp[tn].label[0] = 0; tn++;",
"        }"]
f2_mid = [
"    for (int wi = gWindowsLength - 1; wi >= 1; wi--) {",
"        Window* w = gWindows[wi];",
"        if (w == NULL) continue;",
"        if ((w->flags & WINDOW_HIDDEN) != 0) continue;",
"        if (w->buttonListHead == NULL) continue;",
"        tn = 0;",
"        for (Button* b = w->buttonListHead; b != NULL && tn < 64; b = b->next) {",
"            if ((b->flags & BUTTON_FLAG_DISABLED) != 0) continue;",
"            int k = b->leftMouseUpEventCode;",
"            if (k == -1) continue;",
"            int bw = b->rect.right - b->rect.left; int bh = b->rect.bottom - b->rect.top;",
"            if (bw <= 0 || bh <= 0) continue;",
"            tmp[tn].x = w->rect.left + b->rect.left + bw / 2;",
"            tmp[tn].y = w->rect.top + b->rect.top + bh / 2;",
"            tmp[tn].w = bw; tmp[tn].h = bh; tmp[tn].key = k; tmp[tn].label[0] = 0; tn++;",
"        }"]
f1_collect = collect_head + f1_mid + collect_tail
f2_collect = collect_head + f2_mid + collect_tail
glyph_new = ["static unsigned long long side_glyph(int c)", "{", "    switch (c) {"]
for _cp in sorted(G.keys()):
    glyph_new.append("    case " + str(_cp) + ": return (unsigned long long)0b" + G[_cp] + ";")
glyph_new += ["    default: return 0;", "    }", "}"]
label_new = [
"static void draw_side_label(const char* s, int cx, int cy, int px)",
"{",
"    int n = side_utf8_len(s);",
"    int w = n * 6 * px - px;",
"    int x0 = cx - w / 2;",
"    int y0 = cy - 7 * px / 2;",
"    SDL_SetRenderDrawColor(gSdlRenderer, 230, 190, 90, 255);",
"    for (int i = 0, bi = 0; i < n; i++) {",
"        unsigned long long g = side_glyph(side_utf8_next(s, &bi));",
"        for (int b = 0; b < 35; b++) {",
"            if ((g & (1ULL << (34 - b))) != 0) {",
"                SDL_Rect r = { x0 + i * 6 * px + (b % 5) * px, y0 + (b / 5) * px, px, px };",
"                SDL_RenderFillRect(gSdlRenderer, &r);",
"            }",
"        }",
"    }",
"}"]
replace_func("work/fallout1-ce/src/plib/gnw/gnw.cc", "static const char* side_ru_label(int key, int ctx)", ru, "ru v5 f1")
replace_func("work/fallout2-ce/src/window_manager.cc", "static const char* side_ru_label(int key, int ctx)", ru, "ru v5 f2")
replace_func("work/fallout1-ce/src/plib/gnw/gnw.cc", "int side_collect_buttons(SideButton* out, int max)", f1_collect, "collect v5 f1")
replace_func("work/fallout2-ce/src/window_manager.cc", "int side_collect_buttons(SideButton* out, int max)", f2_collect, "collect v5 f2")
rep_re("work/fallout1-ce/src/plib/gnw/gnw.h", "typedef struct SideButton.*SideButton;", "typedef struct SideButton { int x; int y; int w; int h; int key; char label[24]; } SideButton;", "struct v5 f1")
rep_re("work/fallout2-ce/src/window_manager.h", "typedef struct SideButton.*SideButton;", "typedef struct SideButton { int x; int y; int w; int h; int key; char label[24]; } SideButton;", "struct v5 f2")
for f in ["work/fallout1-ce/src/plib/gnw/svga.cc", "work/fallout2-ce/src/svga.cc"]:
    replace_func(f, "static unsigned short side_glyph(int c)", glyph_new, "glyph 5x7 " + f)
    replace_func(f, "static void draw_side_label(const char* s, int cx, int cy, int px)", label_new, "label 5x7 " + f)
    rep(f, "    int px = bw / 36;", "    int px = bw / 36; { int ml = 0; for (int ci = 0; ci < 4; ci++) { int l1 = side_utf8_len(ll[ci]); if (l1 > ml) ml = l1; int l2 = side_utf8_len(rl[ci]); if (l2 > ml) ml = l2; } if (ml > 6) px = bw / (ml * 6 + 6); if (px < 2) px = 2; if (px > 4) px = 4; }", "px adaptive " + f)
    rep_re(f, "side_cache_label\[8\]\[\d+\]", "side_cache_label[8][24]", "cache 24 " + f)
    rep_opt(f, "kk < 15", "kk < 23", "cache copy " + f)
if not ok:
    sys.exit("ERROR update_side_buttons_v5 did not fully apply")
print("update_side_buttons_v5 done")
