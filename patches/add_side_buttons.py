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
def patch(path, anchor, block, label, after=False):
    lines = load(path).splitlines()
    for i, line in enumerate(lines):
        if anchor in line:
            if after:
                lines[i + 1:i + 1] = block
            else:
                lines[i:i + 1] = block
            save(path, chr(10).join(lines) + chr(10))
            print("patched " + label)
            return
    fail("anchor not found " + label)
side_helper = [
    "static bool touch_side_target(float nx, float ny, int* tx, int* ty)",
    "{",
    "    if (gSdlWindow == NULL) return false;",
    "    int winW = 0; int winH = 0;",
    "    SDL_GetWindowSize(gSdlWindow, &winW, &winH);",
    "    if (winW <= 0 || winH <= 0) return false;",
    "    float wa = (float)winW / (float)winH;",
    "    float ga = 640.0f / 480.0f;",
    "    if (wa <= ga) return false;",
    "    float bar = (1.0f - ga / wa) / 2.0f;",
    "    int side = -1;",
    "    if (nx < bar) side = 0; else if (nx > 1.0f - bar) side = 1; else return false;",
    "    int slot = (int)(ny * 4.0f);",
    "    if (slot < 0) slot = 0;",
    "    if (slot > 3) slot = 3;",
    "    static const int tg[2][4][2] = {{{227, 451}, {227, 459}, {534, 398}, {547, 430}}, {{547, 468}, {547, 449}, {609, 434}, {609, 456}}};",
    "    *tx = tg[side][slot][0];",
    "    *ty = tg[side][slot][1];",
    "    return true;",
    "}",
    "void touch_handle_start(SDL_TouchFingerEvent* event)"
]
for f in ["work/fallout1-ce/src/plib/gnw/touch.cc", "work/fallout2-ce/src/touch.cc"]:
    patch(f, "int phase;", ["    int phase;", "    bool sideButton;", "    int sideX;", "    int sideY;"], "touch struct " + f)
    patch(f, "void touch_handle_start", side_helper, "side target helper " + f)
    patch(f, "touch->phase = TOUCH_PHASE_BEGAN;", ["        touch->phase = TOUCH_PHASE_BEGAN;", "        touch->sideButton = touch_side_target(event->x, event->y, &(touch->sideX), &(touch->sideY));", "        if (touch->sideButton) { touch->startLocation.x = touch->sideX; touch->startLocation.y = touch->sideY; touch->currentLocation = touch->startLocation; }"], "side tap start " + f)
    patch(f, "touch->phase = TOUCH_PHASE_MOVED;", ["        touch->phase = TOUCH_PHASE_MOVED;", "        if (touch->sideButton) { touch->currentLocation.x = touch->sideX; touch->currentLocation.y = touch->sideY; }"], "side tap move " + f)
    patch(f, "touch->phase = TOUCH_PHASE_ENDED;", ["        touch->phase = TOUCH_PHASE_ENDED;", "        if (touch->sideButton) { touch->currentLocation.x = touch->sideX; touch->currentLocation.y = touch->sideY; }"], "side tap end " + f)
draw_helper = [
    "static unsigned short side_glyph(int c)",
    "{",
    "    switch (c) {",
    "    case 65: return 0b010101111101101;",
    "    case 67: return 0b011100100100011;",
    "    case 68: return 0b110101101101110;",
    "    case 69: return 0b111100110100111;",
    "    case 72: return 0b101101111101101;",
    "    case 73: return 0b111010010010111;",
    "    case 75: return 0b101100110100101;",
    "    case 76: return 0b100100100100111;",
    "    case 77: return 0b101111111101101;",
    "    case 78: return 0b101111101101101;",
    "    case 79: return 0b010101101101010;",
    "    case 80: return 0b110101110100100;",
    "    case 82: return 0b110101110101101;",
    "    case 83: return 0b011100010001110;",
    "    case 84: return 0b111010010010010;",
    "    case 85: return 0b101101101101111;",
    "    case 86: return 0b101101101101010;",
    "    default: return 0;",
    "    }",
    "}",
    "static void draw_side_label(const char* s, int cx, int cy, int px)",
    "{",
    "    int n = 0;",
    "    while (s[n] != 0) n++;",
    "    int w = n * 4 * px - px;",
    "    int x0 = cx - w / 2;",
    "    int y0 = cy - 5 * px / 2;",
    "    SDL_SetRenderDrawColor(gSdlRenderer, 230, 190, 90, 255);",
    "    for (int i = 0; i < n; i++) {",
    "        unsigned short g = side_glyph((int)s[i]);",
    "        for (int b = 0; b < 15; b++) {",
    "            if ((g & (1 << (14 - b))) != 0) {",
    "                SDL_Rect r = { x0 + i * 4 * px + (b % 3) * px, y0 + (b / 3) * px, px, px };",
    "                SDL_RenderFillRect(gSdlRenderer, &r);",
    "            }",
    "        }",
    "    }",
    "}",
    "static void draw_side_buttons()",
    "{",
    "    if (gSdlRenderer == NULL) return;",
    "    int ow = 0; int oh = 0;",
    "    if (SDL_GetRendererOutputSize(gSdlRenderer, &ow, &oh) != 0) return;",
    "    if (ow * 480 <= oh * 640) return;",
    "    int vw = oh * 640 / 480;",
    "    int bw = (ow - vw) / 2;",
    "    if (bw < 40) return;",
    "    SDL_Rect vp;",
    "    SDL_RenderGetViewport(gSdlRenderer, &vp);",
    "    SDL_RenderSetViewport(gSdlRenderer, NULL);",
    "    SDL_RenderSetLogicalSize(gSdlRenderer, ow, oh);",
    "    SDL_SetRenderDrawBlendMode(gSdlRenderer, SDL_BLENDMODE_BLEND);",
    '    static const char* ll[4] = {"INV", "OPT", "SKL", "MAP"};',
    '    static const char* rl[4] = {"PIP", "CHA", "TURN", "END"};',
    "    int px = bw / 30;",
    "    if (px < 2) px = 2;",
    "    for (int side = 0; side < 2; side++) {",
    "        for (int slot = 0; slot < 4; slot++) {",
    "            int x = side == 0 ? 6 : ow - bw + 6;",
    "            int y = slot * oh / 4 + 6;",
    "            int w = bw - 12;",
    "            int h = oh / 4 - 12;",
    "            SDL_Rect r = { x, y, w, h };",
    "            SDL_SetRenderDrawColor(gSdlRenderer, 35, 28, 16, 200);",
    "            SDL_RenderFillRect(gSdlRenderer, &r);",
    "            SDL_SetRenderDrawColor(gSdlRenderer, 190, 130, 40, 255);",
    "            SDL_RenderDrawRect(gSdlRenderer, &r);",
    "            draw_side_label(side == 0 ? ll[slot] : rl[slot], x + w / 2, y + h / 2, px);",
    "        }",
    "    }",
    "    SDL_RenderSetLogicalSize(gSdlRenderer, screenGetWidth(), screenGetHeight());",
    "    SDL_RenderSetViewport(gSdlRenderer, &vp);",
    "}",
    "void renderPresent()"
]
for f in ["work/fallout1-ce/src/plib/gnw/svga.cc", "work/fallout2-ce/src/svga.cc"]:
    patch(f, "void renderPresent()", draw_helper, "draw side buttons " + f)
    patch(f, "SDL_RenderPresent(gSdlRenderer);", ["    draw_side_buttons();", "    SDL_RenderPresent(gSdlRenderer);"], "present hook " + f)
if not ok:
    sys.exit("ERROR add_side_buttons did not fully apply")
print("add_side_buttons done")
