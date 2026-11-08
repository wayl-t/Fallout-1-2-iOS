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
glyph_cases = [
"    case 66: return 0b110101110101110;",
"    case 70: return 0b111100110100100;",
"    case 71: return 0b011100101101011;",
"    case 74: return 0b001001001101010;",
"    case 81: return 0b010101101110011;",
"    case 87: return 0b101101101111101;",
"    case 88: return 0b101101010101101;",
"    case 89: return 0b101101010010010;",
"    case 90: return 0b111001010100111;",
"    case 42: return 0b010101111101010;",
"    case 63: return 0b110001010000010;",
"    case 48: return 0b011101101101111;",
"    case 49: return 0b010010010010111;",
"    case 50: return 0b110001010100111;",
"    case 51: return 0b110001010001110;",
"    case 52: return 0b101101111001001;",
"    case 53: return 0b111100110001110;",
"    case 54: return 0b011100110101010;",
"    case 55: return 0b111001010100100;",
"    case 56: return 0b010101010101010;",
"    case 57: return 0b010101011001110;",
]
tex_helper = [
"static void side_texture_overlay(SDL_Rect* r, int seed)",
"{",
"    unsigned int v = (unsigned int)(seed * 1103515245 + 12345);",
"    for (int i = 0; i < 56; i++) { v = v * 1103515245u + 12345u; int px = r->x + (int)((v >> 16) % (unsigned int)(r->w > 0 ? r->w : 1)); v = v * 1103515245u + 12345u; int py = r->y + (int)((v >> 16) % (unsigned int)(r->h > 0 ? r->h : 1)); if ((i % 2) == 0) { SDL_SetRenderDrawColor(gSdlRenderer, 255, 255, 255, 36); } else { SDL_SetRenderDrawColor(gSdlRenderer, 0, 0, 0, 64); } SDL_Rect s = { px, py, 2, 2 }; SDL_RenderFillRect(gSdlRenderer, &s); }",
"    SDL_SetRenderDrawColor(gSdlRenderer, 255, 255, 255, 72); SDL_RenderDrawLine(gSdlRenderer, r->x, r->y, r->x + r->w - 1, r->y); SDL_RenderDrawLine(gSdlRenderer, r->x, r->y, r->x, r->y + r->h - 1);",
"    SDL_SetRenderDrawColor(gSdlRenderer, 0, 0, 0, 130); SDL_RenderDrawLine(gSdlRenderer, r->x, r->y + r->h - 1, r->x + r->w - 1, r->y + r->h - 1); SDL_RenderDrawLine(gSdlRenderer, r->x + r->w - 1, r->y, r->x + r->w - 1, r->y + r->h - 1);",
"    SDL_SetRenderDrawColor(gSdlRenderer, 0, 0, 0, 150); SDL_Rect rv = { r->x + 5, r->y + 5, 3, 3 }; SDL_RenderFillRect(gSdlRenderer, &rv); rv.x = r->x + r->w - 8; SDL_RenderFillRect(gSdlRenderer, &rv); rv.y = r->y + r->h - 8; SDL_RenderFillRect(gSdlRenderer, &rv); rv.x = r->x + 5; SDL_RenderFillRect(gSdlRenderer, &rv);",
"}"
]
ll_old = "    SideButton dsb[8]; int dsbn = side_collect_buttons(dsb, 8); const char* ll[4] = { dsbn > 0 ? dsb[0].label : " + q + "INV" + q + ", dsbn > 1 ? dsb[1].label : " + q + "OPT" + q + ", dsbn > 2 ? dsb[2].label : " + q + "SKL" + q + ", dsbn > 3 ? dsb[3].label : " + q + "MAP" + q + " };"
rl_old = "    const char* rl[4] = { dsbn > 4 ? dsb[4].label : " + q + "PIP" + q + ", dsbn > 5 ? dsb[5].label : " + q + "CHA" + q + ", dsbn > 6 ? dsb[6].label : " + q + "TURN" + q + ", dsbn > 7 ? dsb[7].label : " + q + "END" + q + " };"
ll_new = [
"    SideButton dsb[8]; int dsbn = side_collect_buttons(dsb, 8);",
"    static char side_cache_label[8][8] = {" + q + "INV" + q + ", " + q + "OPT" + q + ", " + q + "SKL" + q + ", " + q + "MAP" + q + ", " + q + "PIP" + q + ", " + q + "CHA" + q + ", " + q + "TURN" + q + ", " + q + "END" + q + "};",
"    for (int ci = 0; ci < dsbn && ci < 8; ci++) { if (dsb[ci].label[0] != 0 && dsb[ci].label[0] != 42 && side_glyph(dsb[ci].label[0]) != 0) { side_cache_label[ci][0] = dsb[ci].label[0]; side_cache_label[ci][1] = 0; } }",
"    const char* ll[4] = { side_cache_label[0], side_cache_label[1], side_cache_label[2], side_cache_label[3] };"
]
rl_new = "    const char* rl[4] = { side_cache_label[4], side_cache_label[5], side_cache_label[6], side_cache_label[7] };"
for f in ["work/fallout1-ce/src/plib/gnw/svga.cc", "work/fallout2-ce/src/svga.cc"]:
    rep(f, "    default: return 0;", chr(10).join(glyph_cases) + chr(10) + "    default: return 0;", "glyph expansion " + f)
    ins(f, "SDL_RenderFillRect(gSdlRenderer, &r);", ["            side_texture_overlay(&r, x * 31 + y);"], "texture overlay call " + f)
    insb(f, "static void draw_side_buttons()", tex_helper, "texture helper " + f)
    rep(f, ll_old, chr(10).join(ll_new), "persistent labels left " + f)
    rep(f, rl_old, rl_new, "persistent labels right " + f)
if not ok:
    sys.exit("ERROR update_side_buttons_v3 did not fully apply")
print("update_side_buttons_v3 done")
