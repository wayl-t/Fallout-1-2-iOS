import pathlib, sys
ok = True
def fail(m):
    global ok
    print('ERROR ' + m)
    ok = False
def load(p):
    return pathlib.Path(p).read_text(encoding='utf-8', errors='ignore')
def save(p, t):
    pathlib.Path(p).write_text(t, encoding='utf-8')
def rep(path, old, new, label):
    t = load(path)
    if old not in t:
        fail('not found ' + label)
        return
    save(path, t.replace(old, new, 1))
    print('patched ' + label)
rep('work/fallout1-ce/src/plib/gnw/svga.cc', '    SDL_RenderCopy(gSdlRenderer, gSdlTexture, NULL, NULL);', '    int _ow = 0; int _oh = 0; SDL_GetRendererOutputSize(gSdlRenderer, &_ow, &_oh); if (_ow > 0 && _oh > 0) { SDL_RenderSetViewport(gSdlRenderer, NULL); SDL_RenderSetLogicalSize(gSdlRenderer, 0, 0); SDL_Rect _dest = { 0, 0, _ow, _oh }; SDL_RenderCopy(gSdlRenderer, gSdlTexture, NULL, &_dest); } else { SDL_RenderCopy(gSdlRenderer, gSdlTexture, NULL, NULL); }', 'fullscreen f1')
rep('work/fallout2-ce/src/svga.cc', '    SDL_RenderCopy(gSdlRenderer, gSdlTexture, nullptr, nullptr);', '    int _ow = 0; int _oh = 0; SDL_GetRendererOutputSize(gSdlRenderer, &_ow, &_oh); if (_ow > 0 && _oh > 0) { SDL_RenderSetViewport(gSdlRenderer, nullptr); SDL_RenderSetLogicalSize(gSdlRenderer, 0, 0); SDL_Rect _dest = { 0, 0, _ow, _oh }; SDL_RenderCopy(gSdlRenderer, gSdlTexture, nullptr, &_dest); } else { SDL_RenderCopy(gSdlRenderer, gSdlTexture, nullptr, nullptr); }', 'fullscreen f2')
if not ok:
    sys.exit('ERROR fullscreen patch did not fully apply')
print('fullscreen_no_side done')
