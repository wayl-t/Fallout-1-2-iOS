import pathlib, sys
ok = True
def fail(msg):
    global ok
    print("ERROR " + msg)
    ok = False
def load(path):
    return pathlib.Path(path).read_text(encoding="utf-8", errors="ignore")
def save(path, text):
    pathlib.Path(path).write_text(text, encoding="utf-8")
def insert_after(path, anchor, block, label, occurrence=1):
    lines = load(path).splitlines()
    seen = 0
    for i, line in enumerate(lines):
        if anchor in line:
            seen += 1
            if seen == occurrence:
                lines[i + 1:i + 1] = block
                save(path, chr(10).join(lines) + chr(10))
                print("patched " + label)
                return
    fail("insert anchor not found " + label)
def replace_line(path, anchor, new_line, label):
    lines = load(path).splitlines()
    for i, line in enumerate(lines):
        if anchor in line:
            lines[i] = new_line
            save(path, chr(10).join(lines) + chr(10))
            print("patched " + label)
            return
    fail("line anchor not found " + label)
q = chr(39)
f1dbg = "work/fallout1-ce/src/plib/gnw/debug.cc"
cond = "    if ((mode[0] == " + q + "w" + q + " || mode[0] == " + q + "a" + q + ") && mode[1] == " + q + "t" + q + ") {"
replace_line(f1dbg, "mode[0] ==", cond, "f1 debug condition")
cpp1 = "    debug_register_log(" + chr(34) + "debug.log" + chr(34) + ", " + chr(34) + "wt" + chr(34) + ");"
insert_after(f1dbg, "atexit(debug_exit);", [cpp1], "f1 debug log on init")
cpp2 = "    _debug_register_log(" + chr(34) + "debug.log" + chr(34) + ", " + chr(34) + "wt" + chr(34) + ");"
insert_after("work/fallout2-ce/src/debug.cc", "atexit(_debug_exit);", [cpp2], "f2 debug log on init")
replace_line("work/fallout1-ce/src/plib/gnw/button.cc", "v58.ulx -= 20;", "                        if (button->rect.lrx - button->rect.ulx <= 27 && button->rect.lry - button->rect.uly <= 27) { v58.ulx -= 20; v58.lrx += 170; v58.uly -= 6; v58.lry += 6; } else { v58.ulx -= 6; v58.lrx += 6; v58.uly -= 6; v58.lry += 6; }", "f1 adaptive hit area")
replace_line("work/fallout2-ce/src/window_manager.cc", "v58.left -= 20;", "                if (button->rect.right - button->rect.left <= 27 && button->rect.bottom - button->rect.top <= 27) { v58.left -= 20; v58.right += 170; v58.top -= 6; v58.bottom += 6; } else { v58.left -= 6; v58.right += 6; v58.top -= 6; v58.bottom += 6; }", "f2 adaptive hit area")
f1stick = [
"        static bool camStick = false;",
"        static int stickCx = 0;",
"        static int stickCy = 0;",
"        static int savedX = 0;",
"        static int savedY = 0;",
"        if (gesture.type == kPan && gesture.numberOfTouches == 1) {",
"            if (!camStick && gesture.state == kBegan && gesture.x < 140 && gesture.y > scr_size.lry - 140) {",
"                camStick = true; stickCx = gesture.x; stickCy = gesture.y; savedX = mouse_x; savedY = mouse_y;",
"            }",
"            if (camStick) {",
"                if (gesture.state == kEnded) {",
"                    camStick = false; mouse_set_position(savedX, savedY);",
"                } else {",
"                    int dx = gesture.x - stickCx; int dy = gesture.y - stickCy; int tx = savedX; int ty = savedY;",
"                    if (dx < -10) tx = scr_size.ulx; if (dx > 10) tx = scr_size.lrx;",
"                    if (dy < -10) ty = scr_size.uly; if (dy > 10) ty = scr_size.lry;",
"                    mouse_set_position(tx, ty);",
"                }",
"                gesture.type = kUnrecognized;",
"            }",
"        }",
]
insert_after("work/fallout1-ce/src/plib/gnw/mouse.cc", "static int prevy;", f1stick, "f1 camera stick")
f1nudge = [
"            if (gesture.type == kPan && gesture.state == kEnded) {",
"                int nx = mouse_x; int ny = mouse_y;",
"                if (nx <= scr_size.ulx + 2) nx = scr_size.ulx + 24;",
"                if (nx >= scr_size.lrx - 2) nx = scr_size.lrx - 24;",
"                if (ny <= scr_size.uly + 2) ny = scr_size.uly + 24;",
"                if (ny >= scr_size.lry - 2) ny = scr_size.lry - 24;",
"                if (nx != mouse_x || ny != mouse_y) mouse_set_position(nx, ny);",
"            }",
]
insert_after("work/fallout1-ce/src/plib/gnw/mouse.cc", "prevy = gesture.y;", f1nudge, "f1 edge release", 2)
f2stick = [
"        static bool camStick = false;",
"        static int stickCx = 0;",
"        static int stickCy = 0;",
"        static int savedX = 0;",
"        static int savedY = 0;",
"        if (gesture.type == kPan && gesture.numberOfTouches == 1) {",
"            if (!camStick && gesture.state == kBegan && gesture.x < 140 && gesture.y > _scr_size.bottom - 140) {",
"                camStick = true; stickCx = gesture.x; stickCy = gesture.y; savedX = gMouseCursorX; savedY = gMouseCursorY;",
"            }",
"            if (camStick) {",
"                if (gesture.state == kEnded) {",
"                    camStick = false; _mouse_set_position(savedX, savedY);",
"                } else {",
"                    int dx = gesture.x - stickCx; int dy = gesture.y - stickCy; int tx = savedX; int ty = savedY;",
"                    if (dx < -10) tx = _scr_size.left; if (dx > 10) tx = _scr_size.right;",
"                    if (dy < -10) ty = _scr_size.top; if (dy > 10) ty = _scr_size.bottom;",
"                    _mouse_set_position(tx, ty);",
"                }",
"                gesture.type = kUnrecognized;",
"            }",
"        }",
]
insert_after("work/fallout2-ce/src/mouse.cc", "static int prevy;", f2stick, "f2 camera stick")
f2nudge = [
"            if (gesture.type == kPan && gesture.state == kEnded) {",
"                int nx = gMouseCursorX; int ny = gMouseCursorY;",
"                if (nx <= _scr_size.left + 2) nx = _scr_size.left + 24;",
"                if (nx >= _scr_size.right - 2) nx = _scr_size.right - 24;",
"                if (ny <= _scr_size.top + 2) ny = _scr_size.top + 24;",
"                if (ny >= _scr_size.bottom - 2) ny = _scr_size.bottom - 24;",
"                if (nx != gMouseCursorX || ny != gMouseCursorY) _mouse_set_position(nx, ny);",
"            }",
]
insert_after("work/fallout2-ce/src/mouse.cc", "prevy = gesture.y;", f2nudge, "f2 edge release", 2)
if not ok:
    sys.exit("ERROR fix_controls did not fully apply")
print("fix_controls done")
