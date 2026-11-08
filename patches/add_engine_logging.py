import pathlib, sys
ok = True
def rep(path, old, new, label):
    global ok
    p = pathlib.Path(path)
    t = p.read_text(encoding='utf-8', errors='ignore')
    if old in t:
        p.write_text(t.replace(old, new), encoding='utf-8')
        print('patched', label, path)
    else:
        print('ERROR anchor not found', label, path)
        ok = False
rep('work/fallout2-ce/src/dfile.cc', 'dbase->path = compat_strdup(filePath);', 'dbase->path = compat_strdup(filePath); { FILE* _l = fopen("db.log", "a"); if (_l) { fprintf(_l, "dbaseOpen ok path=%s entries=%d", filePath, dbase->entriesLength); fputc(10, _l); fclose(_l); } }', 'f2 dbase log')
rep('work/fallout2-ce/src/text_font.cc', 'File* stream = fileOpen(path, "rb");', 'File* stream = fileOpen(path, "rb"); { FILE* _l = fopen("font.log", "a"); if (_l) { fprintf(_l, "textFontLoad %s open=%d", path, stream != nullptr ? 1 : 0); fputc(10, _l); fclose(_l); } }', 'f2 font log')
rep('work/fallout2-ce/src/game.cc', 'int master_db_handle = dbOpen(main_file_name, 0, patch_file_name, 1);', 'int master_db_handle = dbOpen(main_file_name, 0, patch_file_name, 1); { FILE* _l = fopen("font.log", "a"); if (_l) { fprintf(_l, "gameDbInit master handle=%d", master_db_handle); fputc(10, _l); fclose(_l); } }', 'f2 dbinit log')
rep('work/fallout1-ce/src/plib/gnw/text.cc', 'DB_FILE* stream = db_fopen(path, "rb");', 'DB_FILE* stream = db_fopen(path, "rb"); { FILE* _l = fopen("font.log", "a"); if (_l) { fprintf(_l, "f1 load_font %s open=%d", path, stream != NULL ? 1 : 0); fputc(10, _l); fclose(_l); } }', 'f1 font log')
rep('launcher/main.cc', '#include <sys/stat.h>', '#include <sys/stat.h>' + chr(10) + '#include <dirent.h>', 'launcher includes')
rep('launcher/main.cc', 'int choice = pickGame();', '{ const char* _dirs[2] = { dir1.c_str(), dir2.c_str() }; for (int _i = 0; _i < 2; _i++) { DIR* _d = opendir(_dirs[_i]); if (!_d) { launcherLog("list opendir failed %s", _dirs[_i]); continue; } struct dirent* _e; while ((_e = readdir(_d)) != nullptr) { std::string _p = std::string(_dirs[_i]) + "/" + _e->d_name; struct stat _st; if (stat(_p.c_str(), &_st) == 0) launcherLog("file %s size=%lld", _p.c_str(), (long long)_st.st_size); } closedir(_d); } }' + chr(10) + '  int choice = pickGame();', 'launcher file listing')
if not ok:
    sys.exit('ERROR engine logging patch did not fully apply')
print('engine logging patch done')
