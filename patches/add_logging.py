import pathlib
Q = chr(34)
roots = [pathlib.Path("work/fallout1-ce"), pathlib.Path("work/fallout2-ce")]
for root in roots:
    if not root.exists():
        print("skip missing engine:", root)
        continue
    for mouse_path in sorted(root.rglob("mouse.cc")):
        text = mouse_path.read_text(encoding="utf-8", errors="ignore")
        if "kTap" not in text:
            continue
        if "touch.log" in text:
            print("already logged:", mouse_path)
            continue
        lines = text.splitlines()
        if not any("#include <cstdio>" in line for line in lines):
            for i, line in enumerate(lines):
                if line.startswith("#include"):
                    lines.insert(i + 1, "#include <cstdio>")
                    break
        if "gMouseCursorX" in text and "gMouseCursorY" in text:
            cur_x = "gMouseCursorX"
            cur_y = "gMouseCursorY"
        elif "mouse_x" in text and "mouse_y" in text:
            cur_x = "mouse_x"
            cur_y = "mouse_y"
        else:
            print("skip, cursor vars not found:", mouse_path)
            continue
        log_line = "        { FILE* _tl = fopen(" + Q + "touch.log" + Q + ", " + Q + "a" + Q + "); if (_tl) { fprintf(_tl, " + Q + "gesture type=%d state=%d touches=%d x=%d y=%d cursor=%d,%d" + Q + ", (int)gesture.type, (int)gesture.state, gesture.numberOfTouches, gesture.x, gesture.y, " + cur_x + ", " + cur_y + "); fputc(10, _tl); fclose(_tl); } }"
        for i, line in enumerate(lines):
            if "if (touch_get_gesture(&gesture)) {" in line:
                lines.insert(i + 1, log_line)
                break
        mouse_path.write_text(chr(10).join(lines) + chr(10), encoding="utf-8")
        print("patched gesture log:", mouse_path)
print("logging patch done")
