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
def fix(path):
    lines = load(path).splitlines()
    label_i = -1
    tex_i = -1
    btn_i = -1
    for i, line in enumerate(lines):
        if "static void draw_side_label" in line: label_i = i
        if "static void side_texture_overlay" in line and tex_i == -1: tex_i = i
        if "static void draw_side_buttons" in line: btn_i = i
    if label_i == -1 or tex_i == -1 or btn_i == -1:
        fail("sections not found " + path)
        return
    removed = 0
    out = []
    for i, line in enumerate(lines):
        if label_i < i < tex_i and "side_texture_overlay(&r, x * 31 + y);" in line:
            removed += 1
            continue
        out.append(line)
    if removed != 1:
        fail("misplaced call not removed " + path + " " + str(removed))
        return
    lines = out
    btn_i = -1
    for i, line in enumerate(lines):
        if "static void draw_side_buttons" in line: btn_i = i
    done = False
    for i in range(btn_i, len(lines)):
        if "SDL_RenderFillRect(gSdlRenderer, &r);" in lines[i]:
            lines[i + 1:i + 1] = ["            side_texture_overlay(&r, x * 31 + y);"]
            done = True
            break
    if not done:
        fail("button fill not found " + path)
        return
    save(path, chr(10).join(lines) + chr(10))
    print("patched texture placement " + path)
fix("work/fallout1-ce/src/plib/gnw/svga.cc")
fix("work/fallout2-ce/src/svga.cc")
if not ok:
    sys.exit("ERROR fix_side_texture did not fully apply")
print("fix_side_texture done")
