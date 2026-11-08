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
def add_include(path, anchor, inc, label):
    lines = load(path).splitlines()
    for i, line in enumerate(lines):
        if anchor in line:
            lines.insert(i + 1, inc)
            save(path, chr(10).join(lines) + chr(10))
            print("patched " + label)
            return
    fail("anchor not found " + label)
add_include("work/fallout1-ce/src/plib/gnw/touch.cc", "svga.h", "#include " + chr(34) + "plib/gnw/gnw.h" + chr(34), "f1 touch gnw include")
add_include("work/fallout2-ce/src/touch.cc", "svga.h", "#include " + chr(34) + "window_manager.h" + chr(34), "f2 touch window_manager include")
if not ok:
    sys.exit("ERROR fix_side_include did not fully apply")
print("fix_side_include done")
