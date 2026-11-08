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
q = chr(34)
def clog(text, args):
    tail = ", " + args if args else ""
    return "    { FILE* _c = fopen(" + q + "crash.log" + q + ", " + q + "a" + q + "); if (_c) { fprintf(_c, " + q + text + chr(92) + "n" + q + tail + "); fclose(_c); } }"
def insert_after_brace(path, signature, block, label):
    lines = load(path).splitlines()
    for i, line in enumerate(lines):
        if signature in line:
            for j in range(i + 1, min(i + 6, len(lines))):
                if lines[j].strip() == "{":
                    lines[j + 1:j + 1] = block
                    save(path, chr(10).join(lines) + chr(10))
                    print("patched " + label)
                    return
    fail("brace not found " + label)
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
f = "work/fallout1-ce/src/game/combatai.cc"
insert_after_brace(f, "bool combatai_want_to_join(Object* a1)", ["    if (a1 == NULL || obj_dude == NULL) {", "        return false;", "    }", clog("want_to_join pid=%d sid=%d tile=%d", "a1->pid, a1->sid, a1->tile")], "want_to_join guard and log")
insert_before(f, "scr_set_objs(a1->sid, NULL, NULL);", [clog("want_to_join script sid=%d", "a1->sid")], "want_to_join script log")
insert_before(f, "if (ai_danger_source(a1) == NULL)", [clog("want_to_join danger check", "")], "want_to_join danger log")
insert_after_brace(f, "Object* ai_danger_source(Object* critter)", ["    if (critter == NULL) {", "        return NULL;", "    }"], "danger source guard")
replace_line(f, "Object* targets[4];", "    Object* targets[4] = { NULL, NULL, NULL, NULL };", "targets init")
replace_line(f, "if (*a4 != NULL)", "    if (a4 != NULL) {", "a4 null check fix")
insert_after_brace(f, "static Object* ai_find_nearest_team", ["    if (critter == NULL || curr_crit_list == NULL) {", "        return NULL;", "    }"], "nearest team guard")
insert_after_brace(f, "static int ai_find_attackers", ["    if (critter == NULL || curr_crit_list == NULL) {", "        return 0;", "    }"], "find attackers guard")
replace_line(f, "candidate = curr_crit_list[index];", "        candidate = curr_crit_list[index];" + chr(10) + "        if (candidate == NULL) {" + chr(10) + "            continue;" + chr(10) + "        }", "nearest team candidate guard")
replace_line(f, "Object* candidate = curr_crit_list[index];", "        Object* candidate = curr_crit_list[index];" + chr(10) + "        if (candidate == NULL) {" + chr(10) + "            continue;" + chr(10) + "        }", "find attackers candidate guard")
insert_after_brace(f, "bool is_within_perception(Object* critter1, Object* critter2)", ["    if (critter1 == NULL || critter2 == NULL) {", "        return false;", "    }"], "perception guard")
if not ok:
    sys.exit("ERROR fix_combat_crash did not fully apply")
print("fix_combat_crash done")
