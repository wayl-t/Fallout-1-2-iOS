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
bt = "    if (c) { fprintf(c, " + q + "crash signal=%d" + chr(92) + "n" + q + ", sig); void* fr[32]; int nf = backtrace(fr, 32); backtrace_symbols_fd(fr, nf, fileno(c)); fclose(c); }"
replace_line(f1, "#include <csignal>", "#include <csignal>" + chr(10) + "#include <execinfo.h>", "f1 execinfo include")
replace_line(f2, "#include <csignal>", "#include <csignal>" + chr(10) + "#include <execinfo.h>", "f2 execinfo include")
replace_line(f1, "crash signal=%d", bt, "f1 backtrace in handler")
replace_line(f2, "crash signal=%d", bt, "f2 backtrace in handler")
if not ok:
    sys.exit("ERROR add_crash_backtrace did not fully apply")
print("add_crash_backtrace done")
