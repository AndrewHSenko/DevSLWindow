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
            for i in range(max(lensl, lenfl, lenel)):
                if not i >= lensl:
                    sl = start_lines[i].replace('(', '?').replace(')', '?')
                    if sl[0] == '+':
                        raw_str = sl[:-1].split('?')
                        time = raw_str[0].split()[-1]
                        name = raw_str[1]
                        qty = raw_str[2].split()[-1]
                        sl_checks[f'{time}'] = (time, name, qty)
                if not i >= lenfl:
                    fl = finish_lines[i].replace('(', '?').replace(')', '?')
                    if fl[0] == '+':
                        raw_str = fl[:-1].split('?')
                        time = raw_str[0].split()[-1]
                        name = raw_str[1]
                        qty = raw_str[2].split()[-1]
                        fl_checks[f'{time}'] = (time, name, qty)
                if not i >= lenel:
                    el = expo_lines[i].replace('(', '?').replace(')', '?')
                    if el[0] == '+':
                        raw_str = el[:-1].split('?')
                        time = raw_str[0].split()[-1]
                        name = raw_str[1]
                        qty = raw_str[2].split()[-1]
                        el_checks[f'{time}'] = (time, name, qty)
            with open('pv_checks.txt', 'w') as pv:
                for check in sl_checks:
                    pv.write(f'{str(sl_checks[check])}\n')
            with open('finish_checks.txt', 'w') as pv:
                for check in fl_checks:
                    pv.write(f'{str(fl_checks[check])}\n')
            with open('fpv_checks.txt', 'w') as pv:
                for check in el_checks:
                    pv.write(f'{str(el_checks[check])}\n')
            for el_check in el_checks:
                if el_check not in sl_checks and el_check not in fl_checks:
                    print(el_checks[el_check][1])
                    if el_check not in sl_checks:
                        print('Not in PV')
                    if el_check not in fl_checks:
                        print('Not in Finish')


            