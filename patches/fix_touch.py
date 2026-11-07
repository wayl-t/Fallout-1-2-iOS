import pathlib, sys
roots = [pathlib.Path('work/fallout1-ce'), pathlib.Path('work/fallout2-ce')]
tap_fixed = []
for root in roots:
    if not root.exists():
        print('skip missing engine:', root)
        continue
    for touch_path in sorted(root.rglob('touch.cc')):
        text = touch_path.read_text(encoding='utf-8', errors='ignore')
        new = text.replace('PAN_MINIMUM_MOVEMENT 4', 'PAN_MINIMUM_MOVEMENT 16')
        if new != text:
            touch_path.write_text(new, encoding='utf-8')
            print('patched pan threshold:', touch_path)
    for mouse_path in sorted(root.rglob('mouse.cc')):
        text = mouse_path.read_text(encoding='utf-8', errors='ignore')
        if 'kTap' not in text:
            continue
        if '_mouse_simulate_input' in text:
            fn = '_mouse_simulate_input'
        elif 'mouse_simulate_input' in text:
            fn = 'mouse_simulate_input'
        elif 'mouseSimulateInput' in text:
            fn = 'mouseSimulateInput'
        else:
            fn = None
        if 'gMouseCursorX' in text and 'gMouseCursorY' in text:
            cur_x = 'gMouseCursorX'
            cur_y = 'gMouseCursorY'
        elif 'mouse_x' in text and 'mouse_y' in text:
            cur_x = 'mouse_x'
            cur_y = 'mouse_y'
        else:
            cur_x = None
            cur_y = None
        if fn is None or cur_x is None:
            print('skip, simulate fn or cursor vars not found:', mouse_path)
            continue
        new = text.replace(fn + '(0, 0, MOUSE_STATE_LEFT_BUTTON_DOWN)', fn + '(gesture.x - ' + cur_x + ', gesture.y - ' + cur_y + ', MOUSE_STATE_LEFT_BUTTON_DOWN)')
        new = new.replace(fn + '(0, 0, MOUSE_STATE_RIGHT_BUTTON_DOWN)', fn + '(gesture.x - ' + cur_x + ', gesture.y - ' + cur_y + ', MOUSE_STATE_RIGHT_BUTTON_DOWN)')
        lines = new.splitlines()
        out = []
        i = 0
        while i < len(lines):
            out.append(lines[i])
            if 'prevx = gesture.x;' in lines[i] and i + 1 < len(lines) and 'prevy = gesture.y;' in lines[i + 1]:
                out.append(lines[i + 1])
                indent = lines[i + 1][:len(lines[i + 1]) - len(lines[i + 1].lstrip())]
                out.append(indent + fn + '(gesture.x - ' + cur_x + ', gesture.y - ' + cur_y + ', 0);')
                i += 2
                continue
            i += 1
        new = chr(10).join(out) + chr(10)
        if new != text:
            mouse_path.write_text(new, encoding='utf-8')
            tap_fixed.append(str(mouse_path))
            print('patched absolute tap:', mouse_path)
print('tap fixed in:', tap_fixed)
if not any('fallout1-ce' in p for p in tap_fixed):
    sys.exit('ERROR: Fallout 1 tap fix did not apply')
if not any('fallout2-ce' in p for p in tap_fixed):
    sys.exit('ERROR: Fallout 2 tap fix did not apply')
