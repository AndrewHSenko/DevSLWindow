with open('start_10.txt', 'r') as start:
    start_lines = start.readlines()
    with open('finish_10.txt', 'r') as finish:
        finish_lines = finish.readlines()
        with open('expo_10.txt', 'r') as expo:
            expo_lines = expo.readlines()
            lensl, lenfl, lenel = len(start_lines), len(finish_lines), len(expo_lines)
            sl_checks = {}
            fl_checks = {}
            el_checks = {}
            bad_checks = {}
            for i in range(max(lensl, lenfl, lenel)):
                if not i >= lensl:
                    sl = start_lines[i].replace('(', '?').replace(')', '?')
                    if sl[0] == '+':
                        raw_str = sl[:-1].split('?')
                        time = raw_str[0].split()[-1]
                        name = raw_str[1]
                        qty = raw_str[2].split()[-1]
                        sl_checks[name] = (time, qty)
                if not i >= lenfl:
                    fl = finish_lines[i].replace('(', '?').replace(')', '?')
                    if fl[0] == '+':
                        raw_str = fl[:-1].split('?')
                        time = raw_str[0].split()[-1]
                        name = raw_str[1]
                        qty = raw_str[2].split()[-1]
                        fl_checks[name] = (time, qty)
                if not i >= lenel:
                    el = expo_lines[i].replace('(', '?').replace(')', '?')
                    if el[0] == '+':
                        raw_str = el[:-1].split('?')
                        time = raw_str[0].split()[-1]
                        name = raw_str[1]
                        qty = raw_str[2].split()[-1]
                        el_checks[name] = (time, qty)
            for check in sl_checks:
                if check not in fl_checks:
                    if check not in el_checks:
                        bad_checks[check] = (sl_checks[check], 'finish', 'expo')
                    else:
                        bad_checks[check] = (sl_checks[check], 'finish')
                elif check not in el_checks:
                    bad_checks[check] = (sl_checks[check], 'expo')
            for check, info in bad_checks.items():
                print(f'{check} : {str(info)}')
            print('---')
            bad_checks = {}
            for check in fl_checks:
                if check not in sl_checks:
                    if check not in el_checks:
                        bad_checks[check] = (fl_checks[check], 'start', 'expo')
                    else:
                        bad_checks[check] = (fl_checks[check], 'start')
                elif check not in el_checks:
                    bad_checks[check] = (fl_checks[check], 'expo')
            for check, info in bad_checks.items():
                print(f'{check} : {str(info)}')
            # Check lists are now all filled


            