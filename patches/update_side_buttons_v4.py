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
ru_bits = [
"010101111101101",
"111100110100111",
"110101110101110",
"111100100100100",
"010101101111101",
"111100111100111",
"101101111101101",
"111001011001111",
"101111101101101",
"010111101101101",
"101110100110101",
"001101101101111",
"101111111101101",
"101101111101101",
"010101101101010",
"111101101101101",
"110101110100100",
"011100100100011",
"111010010010010",
"101101010010010",
"010111101111010",
"101101010101101",
"101101101111110",
"101101111001001",
"101101101101111",
"101101101101110",
"110100110101111",
"101101110101111",
"100100110101110",
"011100011100011",
"110101111101101",
"110101011001111",
]
glyph_cases = []
for i, b in enumerate(ru_bits):
    glyph_cases.append("    case " + str(1040 + i) + ": return 0b" + b + ";")
    glyph_cases.append("    case " + str(1072 + i) + ": return 0b" + b + ";")
glyph_cases.append("    case 1025: return 0b010111111101111;")
glyph_cases.append("    case 1105: return 0b010111111101111;")
glyph_cases.append("    case 46: return 0b000000000000010;")
glyph_cases.append("    case 45: return 0b000000111000000;")
utf8_helpers = [
"static int side_utf8_next(const char* s, int* idx)",
"{",
"    unsigned char b = (unsigned char)s[*idx];",
"    if (b == 0) return 0;",
"    if (b < 0x80) { (*idx)++; return b; }",
"    if ((b & 0xE0) == 0xC0 && s[*idx + 1] != 0) { int cp = ((b & 0x1F) << 6) | ((unsigned char)s[*idx + 1] & 0x3F); *idx += 2; return cp; }",
"    (*idx)++;",
"    return 63;",
"}",
"static int side_utf8_len(const char* s)",
"{",
"    int n = 0; int i = 0; while (s[i] != 0) { side_utf8_next(s, &i); n++; } return n;",
"}",
]
ru_helper = [
"static const char* side_ru_label(int key, int ctx)",
"{",
"    if (ctx == 2) {",
"        if (key == 500) return " + q + "ПРЕД." + q + ";",
"        if (key == 501) return " + q + "СЛЕД." + q + ";",
"        if (key == 116 || key == 84) return " + q + "ВЗЯТЬ" + q + ";",
"        if (key == 109 || key == 77) return " + q + "ИЗМЕН." + q + ";",
"        if (key == 99 || key == 67) return " + q + "СОЗДАТЬ" + q + ";",
"        if (key == 27) return " + q + "НАЗАД" + q + ";",
"        return " + q + "ВЫБОР" + q + ";",
"    }",
"    if (ctx == 1) {",
"        if (key == 105 || key == 73) return " + q + "ВСТУПЛ." + q + ";",
"        if (key == 110 || key == 78) return " + q + "НОВАЯ" + q + ";",
"        if (key == 108 || key == 76) return " + q + "ЗАГРУЗ." + q + ";",
"        if (key == 111 || key == 79) return " + q + "НАСТР." + q + ";",
"        if (key == 99 || key == 67) return " + q + "ТИТРЫ" + q + ";",
"        if (key == 101 || key == 69) return " + q + "ВЫХОД" + q + ";",
"        return " + q + "МЕНЮ" + q + ";",
"    }",
"    if (key == 105 || key == 73) return " + q + "ВЕЩИ" + q + ";",
"    if (key == 111 || key == 79) return " + q + "НАСТР." + q + ";",
"    if (key == 115 || key == 83) return " + q + "НАВЫКИ" + q + ";",
"    if (key == 9) return " + q + "КАРТА" + q + ";",
"    if (key == 112 || key == 80) return " + q + "ПИП-БОЙ" + q + ";",
"    if (key == 99 || key == 67) return " + q + "ПЕРСОН." + q + ";",
"    if (key == 98 || key == 66) return " + q + "РУКИ" + q + ";",
"    if (key == -20) return " + q + "АТАКА" + q + ";",
"    if (key == 32) return " + q + "ХОД" + q + ";",
"    if (key == 13) return " + q + "БОЙ" + q + ";",
"    if (key == 27) return " + q + "НАЗАД" + q + ";",
"    if (key == 500) return " + q + "ПРЕД." + q + ";",
"    if (key == 501) return " + q + "СЛЕД." + q + ";",
"    if (key >= 500 && key < 600) return " + q + "ВЫБОР" + q + ";",
"    return " + q + "ДЕЙСТВ." + q + ";",
"}",
]
ctx_block = [
"        int ctx = 0;",
"        for (int k = 0; k < n; k++) { if (out[k].key == 500 || out[k].key == 501) ctx = 2; }",
"        if (ctx == 0) { int hasI = 0, hasN = 0, hasL = 0; for (int k = 0; k < n; k++) { if (out[k].key == 105 || out[k].key == 73) hasI = 1; if (out[k].key == 110 || out[k].key == 78) hasN = 1; if (out[k].key == 108 || out[k].key == 76) hasL = 1; } if (hasI && hasN && hasL && n <= 6) ctx = 1; }",
"        for (int k = 0; k < n; k++) { const char* s = side_ru_label(out[k].key, ctx); int qi = 0; while (s[qi] != 0 && qi < 15) { out[k].label[qi] = s[qi]; qi++; } out[k].label[qi] = 0; }",
]
for f in ["work/fallout1-ce/src/plib/gnw/gnw.h", "work/fallout2-ce/src/window_manager.h"]:
    rep(f, "char label[8];", "char label[16];", "label size " + f)
for f in ["work/fallout1-ce/src/plib/gnw/gnw.cc", "work/fallout2-ce/src/window_manager.cc"]:
    insb(f, "int side_collect_buttons", ru_helper, "ru helper " + f)
    rep(f, "            if (c >= 32 && c < 127) { out[n].label[0] = (char)c; out[n].label[1] = 0; } else { out[n].label[0] = 42; out[n].label[1] = 0; }", "            (void)c; out[n].label[0] = 0;", "label placeholder " + f)
    insb(f, "        if (n > 0) return n;", ctx_block, "ru context " + f)
for f in ["work/fallout1-ce/src/plib/gnw/svga.cc", "work/fallout2-ce/src/svga.cc"]:
    rep(f, "    case 57: return 0b010101011001110;" + chr(10) + "    default: return 0;", "    case 57: return 0b010101011001110;" + chr(10) + chr(10).join(glyph_cases) + chr(10) + "    default: return 0;", "glyph ru " + f)
    insb(f, "static void draw_side_label", utf8_helpers, "utf8 helpers " + f)
    rep(f, "    int n = 0;" + chr(10) + "    while (s[n] != 0) n++;", "    int n = side_utf8_len(s);" + chr(10) + "    // utf8 length counted above", "utf8 len " + f)
    rep(f, "    for (int i = 0; i < n; i++) {", "    for (int i = 0, bi = 0; i < n; i++) {", "utf8 loop " + f)
    rep(f, "        unsigned short g = side_glyph((int)s[i]);", "        unsigned short g = side_glyph(side_utf8_next(s, &bi));", "utf8 glyph " + f)
    rep(f, "    int px = bw / 30;", "    int px = bw / 36;", "px ru " + f)
    rep(f, "side_cache_label[8][8]", "side_cache_label[8][16]", "cache size " + f)
    rep(f, q + "INV" + q, q + "ВЕЩИ" + q, "fallback inv " + f)
    rep(f, q + "OPT" + q, q + "НАСТР." + q, "fallback opt " + f)
    rep(f, q + "SKL" + q, q + "НАВЫКИ" + q, "fallback skl " + f)
    rep(f, q + "MAP" + q, q + "КАРТА" + q, "fallback map " + f)
    rep(f, q + "PIP" + q, q + "ПИП-БОЙ" + q, "fallback pip " + f)
    rep(f, q + "CHA" + q, q + "ПЕРСОН." + q, "fallback cha " + f)
    rep(f, q + "TURN" + q, q + "ХОД" + q, "fallback turn " + f)
    rep(f, q + "END" + q, q + "БОЙ" + q, "fallback end " + f)
    rep(f, "    for (int ci = 0; ci < dsbn && ci < 8; ci++) { if (dsb[ci].label[0] != 0 && dsb[ci].label[0] != 42 && side_glyph(dsb[ci].label[0]) != 0) { side_cache_label[ci][0] = dsb[ci].label[0]; side_cache_label[ci][1] = 0; } }", "    for (int ci = 0; ci < dsbn && ci < 8; ci++) { if (dsb[ci].label[0] != 0) { int kk = 0; while (dsb[ci].label[kk] != 0 && kk < 15) { side_cache_label[ci][kk] = dsb[ci].label[kk]; kk++; } side_cache_label[ci][kk] = 0; } }", "cache copy ru " + f)
if not ok:
    sys.exit("ERROR update_side_buttons_v4 did not fully apply")
print("update_side_buttons_v4 done")
