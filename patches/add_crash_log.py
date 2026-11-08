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
def insert_after(path, anchor, block, label):
    lines = load(path).splitlines()
    for i, line in enumerate(lines):
        if anchor in line:
            lines[i + 1:i + 1] = block
            save(path, chr(10).join(lines) + chr(10))
            print("patched " + label)
            return
    fail("anchor not found " + label)
def insert_before(path, anchor, block, label):
    lines = load(path).splitlines()
    for i, line in enumerate(lines):
        if anchor in line:
            lines[i:i] = block
            save(path, chr(10).join(lines) + chr(10))
            print("patched " + label)
            return
    fail("anchor not found " + label)
def replace_line(path, anchor, new, label):
    lines = load(path).splitlines()
    for i, line in enumerate(lines):
        if anchor in line:
            lines[i] = new
            save(path, chr(10).join(lines) + chr(10))
            print("patched " + label)
            return
    fail("line not found " + label)
f1 = "work/fallout1-ce/src/plib/gnw/debug.cc"
f2 = "work/fallout2-ce/src/debug.cc"
q = chr(34)
replace_line(f1, "#include <stdlib.h>", "#include <stdlib.h>" + chr(10) + "#include <csignal>", "f1 csignal")
replace_line(f2, "#include <stdlib.h>", "#include <stdlib.h>" + chr(10) + "#include <csignal>", "f2 csignal")
insert_before(f1, "void GNW_debug_init()", ["static void crash_handler(int sig) {", "    if (fd != NULL) { fflush(fd); }", "    FILE* c = fopen(" + q + "crash.log" + q + ", " + q + "a" + q + ");", "    if (c) { fprintf(c, " + q + "crash signal=%d" + chr(92) + "n" + q + ", sig); fclose(c); }", "    signal(sig, SIG_DFL);", "    raise(sig);", "}", ""], "f1 handler")
insert_before(f2, "void _GNW_debug_init()", ["static void crash_handler(int sig) {", "    if (_fd != nullptr) { fflush(_fd); }", "    FILE* c = fopen(" + q + "crash.log" + q + ", " + q + "a" + q + ");", "    if (c) { fprintf(c, " + q + "crash signal=%d" + chr(92) + "n" + q + ", sig); fclose(c); }", "    signal(sig, SIG_DFL);", "    raise(sig);", "}", ""], "f2 handler")
insert_after(f1, "atexit(debug_exit);", ["    signal(SIGSEGV, crash_handler);", "    signal(SIGABRT, crash_handler);", "    signal(SIGBUS, crash_handler);", "    signal(SIGILL, crash_handler);"], "f1 install")
insert_after(f2, "atexit(_debug_exit);", ["    signal(SIGSEGV, crash_handler);", "    signal(SIGABRT, crash_handler);", "    signal(SIGBUS, crash_handler);", "    signal(SIGILL, crash_handler);"], "f2 install")
insert_after(f1, "fd = compat_fopen(fileName, mode);", ["    setvbuf(fd, NULL, _IONBF, 0);"], "f1 unbuffered")
insert_after(f2, "_fd = compat_fopen(fileName, mode);", ["    setvbuf(_fd, nullptr, _IONBF, 0);"], "f2 unbuffered")
insert_after("work/fallout1-ce/src/game/map.cc", "    compat_strupr(file_name);", ["    { FILE* _c = fopen(" + q + "crash.log" + q + ", " + q + "a" + q + "); if (_c) { fprintf(_c, " + q + "map_load %s" + chr(92) + "n" + q + ", file_name); fclose(_c); } }"], "f1 map log")
insert_after("work/fallout2-ce/src/map.cc", "    compat_strupr(fileName);", ["    { FILE* _c = fopen(" + q + "crash.log" + q + ", " + q + "a" + q + "); if (_c) { fprintf(_c, " + q + "map_load %s" + chr(92) + "n" + q + ", fileName); fclose(_c); } }"], "f2 map log")
if not ok:
    sys.exit("ERROR add_crash_log did not fully apply")
print("add_crash_log done")

