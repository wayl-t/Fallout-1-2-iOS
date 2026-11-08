import pathlib, re, sys
ok = True
def do_patch(path, hover_re, hover_repl, old_block, new_block):
    global ok
    p = pathlib.Path(path)
    text = p.read_text(encoding='utf-8', errors='ignore')
    if 'return button->mask[width * y + x] != 0;' in text:
        text = text.replace('return button->mask[width * y + x] != 0;', 'return true;')
        print('mask removed:', path)
    else:
        print('ERROR mask line not found:', path); ok = False
    text2, n = re.subn(hover_re, hover_repl, text)
    if n == 1:
        text = text2; print('hover gate fixed:', path)
    else:
        print('ERROR hover gate count', n, path); ok = False
    if old_block in text:
        text = text.replace(old_block, new_block); print('hit area expanded:', path)
    else:
        print('ERROR hit block not found:', path); ok = False
    p.write_text(text, encoding='utf-8')
f1_old = 'rectCopy(&v58, &(button->rect));' + chr(10) + '                rectOffset(&v58, w->rect.ulx, w->rect.uly);' + chr(10) + '                if (button_under_mouse(button, &v58)) {'
f1_new = 'rectCopy(&v58, &(button->rect));' + chr(10) + '                rectOffset(&v58, w->rect.ulx, w->rect.uly);' + chr(10) + '                v58.ulx -= 20; v58.lrx += 170; v58.uly -= 6; v58.lry += 6;' + chr(10) + '                if (button_under_mouse(button, &v58)) {'
f1_re = r'if \(button != w->hoveredButton && button != w->clickedButton\) \{\s+break;\s+\}'
f1_repl = 'if (button != w->hoveredButton && button != w->clickedButton) { w->hoveredButton = button; }'
do_patch('work/fallout1-ce/src/plib/gnw/button.cc', f1_re, f1_repl, f1_old, f1_new)
f2_old = 'rectCopy(&v58, &(button->rect));' + chr(10) + '                rectOffset(&v58, window->rect.left, window->rect.top);' + chr(10) + '                if (_button_under_mouse(button, &v58)) {'
f2_new = 'rectCopy(&v58, &(button->rect));' + chr(10) + '                rectOffset(&v58, window->rect.left, window->rect.top);' + chr(10) + '                v58.left -= 20; v58.right += 170; v58.top -= 6; v58.bottom += 6;' + chr(10) + '                if (_button_under_mouse(button, &v58)) {'
f2_re = r'if \(button != window->hoveredButton && button != window->clickedButton\) \{\s+break;\s+\}'
f2_repl = 'if (button != window->hoveredButton && button != window->clickedButton) { window->hoveredButton = button; }'
do_patch('work/fallout2-ce/src/window_manager.cc', f2_re, f2_repl, f2_old, f2_new)
if not ok:
    sys.exit('ERROR: menu button patch did not fully apply')
print('menu button patch done')
