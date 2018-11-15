# =============================================================================
# Pretvori
# =====================================================================@018267=
# 1. podnaloga
# Naslednji program naj bi seštel dva kota, podana v stopinjah, minutah in sekundah
# 
#      print('Prvi kot\n=========')
#      stopinje1 = int(input('stopinje: '))
#      minute1 = int(input('minute: '))
#      sekunde1 = int(input('sekunde: '))
#      print('Drugi kot\n=========')
#      stopinje2 = int(input('stopinje: '))
#      minute2 = int(input('minute: '))
#      sekunde2 = int(input('sekunde: '))
#      stopinje = stopinje1 + stopinje2
#      minute = minute1 + minute2
#      sekunde = sekunde1 + sekunde2
#      minute = minute + sekunde // 60
#      minute = minute % 60
#      print('Vsota kotov je', stopinje, 'stopinj,', minute, 'minut in', sekunde, 'sekund.')
# 
# Žal ne dela pravilno. Popravi ga!
# =============================================================================

# =====================================================================@018268=
# 2. podnaloga
# Spodaj je napisan program, ki kot v radianih (realno število) pretvori in izpiše
# v stopinjah in minutah (kot celi števili; za minute naj program ne uporabi
# zaokroženja ampak naj samo odreže decimalna mesta). 
# 
# Primer: Za 
# 
#     kot = 2.185
# 
# naj program izpiše
# 
#     2.185 radianov je 125 stopinj in 11 minut.
# 
# Žal ne deluje povsem pravilno. Popravi ga!
# 
#      import math # Število π je shranjeno v math.pi
#      
#      kot = input('Kot: ')
#      stopinje = kot * 360 / math.pi
#      minute = 60 * stopinje
#      stopinje = int(stopinje)
#      print('{:.6}'.format(kot), 'radianov je', stopinje, 'stopinj in', minute, 'minut
# =============================================================================

# =====================================================================@018269=
# 3. podnaloga
# Program
# 
# 
#      ura = int(input('Ur: '))
#      minuta = int(input('Minut: '))
#      alfa = 60 * (3 * minuta) # Kot minutnega kazalca v kotnih minutah.
#      beta = 60 * (ura + minuta) # Kot urnega kazalca v kotnih minutah.
#      minute = abs(alfa - beta)
#      minute = min(minute, 360 * 60 - minute) # Vzamemo manjšega od obeh kotov.
#      minute = minute - int(minute) # Odrežemo decimalni del.
#      stopinje = minute // 60
#      print('Kot med urnim in minutnim kazalcem je', stopinje, 'stopinj in', minute, 'minut.')
# 
# naj bi izračunal manjšega izmed kotov med urnim in
# minutnim kazalcem ob danem času. Čas je podan z uro in minutami.
# Upoštevajte, da se vsako minuto tudi urni kazalec malo prestavi.
# Trenutno uro in minuto imate podano v spremenljivkah z imenoma `ura`
# in `minuta`. Kot naj bo izpisan v obliki
#  
#     Kot med urnim in minutnim kazalcem je x stopinj in y minut.
# 
# kjer sta `x` in `y` celi števili (minut ne zaokrožuj, ampak samo odreži
# decimalni del).
# 
# Primer: za vrednosti
# 
#     ura = 17
#     minuta = 47
# 
# naj program izpiše
# 
#     Kot med urnim in minutnim kazalcem je 108 stopinj in 30 minut.
# =============================================================================





































































































# ============================================================================@

'Če vam Python sporoča, da je v tej vrstici sintaktična napaka,'
'se napaka v resnici skriva v zadnjih vrsticah vaše kode.'

'Kode od tu naprej NE SPREMINJAJTE!'


















































import json, os, re, sys, shutil, traceback, urllib.error, urllib.request


import io, sys
from contextlib import contextmanager

class VisibleStringIO(io.StringIO):
    def read(self, size=None):
        x = io.StringIO.read(self, size)
        print(x, end='')
        return x

    def readline(self, size=None):
        line = io.StringIO.readline(self, size)
        print(line, end='')
        return line

class Check:
    @staticmethod
    def has_solution(part):
        return part['solution'].strip() != ''

    @staticmethod
    def initialize(parts):
        Check.parts = parts
        for part in Check.parts:
            part['valid'] = True
            part['feedback'] = []
            part['secret'] = []
        Check.current_part = None
        Check.part_counter = None

    @staticmethod
    def part():
        if Check.part_counter is None:
            Check.part_counter = 0
        else:
            Check.part_counter += 1
        Check.current_part = Check.parts[Check.part_counter]
        return Check.has_solution(Check.current_part)

    @staticmethod
    def feedback(message, *args, **kwargs):
        Check.current_part['feedback'].append(message.format(*args, **kwargs))

    @staticmethod
    def error(message, *args, **kwargs):
        Check.current_part['valid'] = False
        Check.feedback(message, *args, **kwargs)

    @staticmethod
    def clean(x, digits=6, typed=False):
        t = type(x)
        if t is float:
            x = round(x, digits)
            # Since -0.0 differs from 0.0 even after rounding,
            # we change it to 0.0 abusing the fact it behaves as False.
            v = x if x else 0.0
        elif t is complex:
            v = complex(Check.clean(x.real, digits, typed), Check.clean(x.imag, digits, typed))
        elif t is list:
            v = list([Check.clean(y, digits, typed) for y in x])
        elif t is tuple:
            v = tuple([Check.clean(y, digits, typed) for y in x])
        elif t is dict:
            v = sorted([(Check.clean(k, digits, typed), Check.clean(v, digits, typed)) for (k, v) in x.items()])
        elif t is set:
            v = sorted([Check.clean(y, digits, typed) for y in x])
        else:
            v = x
        return (t, v) if typed else v

    @staticmethod
    def secret(x, hint=None, clean=None):
        clean = Check.get('clean', clean)
        Check.current_part['secret'].append((str(clean(x)), hint))

    @staticmethod
    def equal(expression, expected_result, clean=None, env=None, update_env=None):
        global_env = Check.init_environment(env=env, update_env=update_env)
        clean = Check.get('clean', clean)
        actual_result = eval(expression, global_env)
        if clean(actual_result) != clean(expected_result):
            Check.error('Izraz {0} vrne {1!r} namesto {2!r}.',
                        expression, actual_result, expected_result)
            return False
        else:
            return True

    @staticmethod
    def run(statements, expected_state, clean=None, env=None, update_env=None):
        code = "\n".join(statements)
        statements = "  >>> " + "\n  >>> ".join(statements)
        global_env = Check.init_environment(env=env, update_env=update_env)
        clean = Check.get('clean', clean)
        exec(code, global_env)
        errors = []
        for (x, v) in expected_state.items():
            if x not in global_env:
                errors.append('morajo nastaviti spremenljivko {0}, vendar je ne'.format(x))
            elif clean(global_env[x]) != clean(v):
                errors.append('nastavijo {0} na {1!r} namesto na {2!r}'.format(x, s[x], v))
        if errors:
            Check.error('Ukazi\n{0}\n{1}.', statements,  ";\n".join(errors))
            return False
        else:
            return True

    @staticmethod
    @contextmanager
    def in_file(filename, content, encoding=None):
        encoding = Check.get('encoding', encoding)
        with open(filename, 'w', encoding=encoding) as f:
            for line in content:
                print(line, file=f)
        old_feedback = Check.current_part['feedback'][:]
        yield
        new_feedback = Check.current_part['feedback'][len(old_feedback):]
        Check.current_part['feedback'] = old_feedback
        if new_feedback:
            new_feedback = ['\n    '.join(error.split('\n')) for error in new_feedback]
            Check.error('Pri vhodni datoteki {0} z vsebino\n  {1}\nso se pojavile naslednje napake:\n- {2}', filename, '\n  '.join(content), '\n- '.join(new_feedback))

    @staticmethod
    @contextmanager
    def input(content, visible=None):
        old_stdin = sys.stdin
        old_feedback = Check.current_part['feedback'][:]
        try:
            with Check.set_stringio(visible):
                sys.stdin = Check.get('stringio')('\n'.join(content) + '\n')
                yield
        finally:
            sys.stdin = old_stdin
        new_feedback = Check.current_part['feedback'][len(old_feedback):]
        Check.current_part['feedback'] = old_feedback
        if new_feedback:
            new_feedback = ['\n  '.join(error.split('\n')) for error in new_feedback]
            Check.error('Pri vhodu\n  {0}\nso se pojavile naslednje napake:\n- {1}', '\n  '.join(content), '\n- '.join(new_feedback))

    @staticmethod
    def out_file(filename, content, encoding=None):
        encoding = Check.get('encoding', encoding)
        with open(filename, encoding=encoding) as f:
            out_lines = f.readlines()
        equal, diff, line_width = Check.difflines(out_lines, content)
        if equal:
            return True
        else:
            Check.error('Izhodna datoteka {0}\n  je enaka{1}  namesto:\n  {2}', filename, (line_width - 7) * ' ', '\n  '.join(diff))
            return False

    @staticmethod
    def output(expression, content, env=None, update_env=None):
        global_env = Check.init_environment(env=env, update_env=update_env)
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            exec(expression, global_env)
        finally:
            output = sys.stdout.getvalue().strip().splitlines()
            sys.stdout = old_stdout
        equal, diff, line_width = Check.difflines(output, content)
        if equal:
            return True
        else:
            Check.error('Program izpiše{0}  namesto:\n  {1}', (line_width - 13) * ' ', '\n  '.join(diff))
            return False

    @staticmethod
    def difflines(actual_lines, expected_lines):
        actual_len, expected_len = len(actual_lines), len(expected_lines)
        if actual_len < expected_len:
            actual_lines += (expected_len - actual_len) * ['\n']
        else:
            expected_lines += (actual_len - expected_len) * ['\n']
        equal = True
        line_width = max(len(actual_line.rstrip()) for actual_line in actual_lines + ['Program izpiše'])
        diff = []
        for out, given in zip(actual_lines, expected_lines):
            out, given = out.rstrip(), given.rstrip()
            if out != given:
                equal = False
            diff.append('{0} {1} {2}'.format(out.ljust(line_width), '|' if out == given else '*', given))
        return equal, diff, line_width

    @staticmethod
    def init_environment(env=None, update_env=None):
        global_env = globals()
        if not Check.get('update_env', update_env):
            global_env = dict(global_env)
        global_env.update(Check.get('env', env))
        return global_env

    @staticmethod
    def generator(expression, expected_values, should_stop=None, further_iter=None, clean=None, env=None, update_env=None):
        from types import GeneratorType
        global_env = Check.init_environment(env=env, update_env=update_env)
        clean = Check.get('clean', clean)
        gen = eval(expression, global_env)
        if not isinstance(gen, GeneratorType):
            Check.error("Izraz {0} ni generator.", expression)
            return False

        try:
            for iteration, expected_value in enumerate(expected_values):
                actual_value = next(gen)
                if clean(actual_value) != clean(expected_value):
                    Check.error("Vrednost #{0}, ki jo vrne generator {1} je {2!r} namesto {3!r}.",
                                iteration, expression, actual_value, expected_value)
                    return False
            for _ in range(Check.get('further_iter', further_iter)):
                next(gen)  # we will not validate it
        except StopIteration:
            Check.error("Generator {0} se prehitro izteče.", expression)
            return False
        
        if Check.get('should_stop', should_stop):
            try:
                next(gen)
                Check.error("Generator {0} se ne izteče (dovolj zgodaj).", expression)
            except StopIteration:
                pass  # this is fine
        return True

    @staticmethod
    def summarize():
        for i, part in enumerate(Check.parts):
            if not Check.has_solution(part):
                print('{0}. podnaloga je brez rešitve.'.format(i + 1))
            elif not part['valid']:
                print('{0}. podnaloga nima veljavne rešitve.'.format(i + 1))
            else:
                print('{0}. podnaloga ima veljavno rešitev.'.format(i + 1))
            for message in part['feedback']:
                print('  - {0}'.format('\n    '.join(message.splitlines())))

    settings_stack = [{
        'clean': clean.__func__,
        'encoding': None,
        'env': {},
        'further_iter': 0,
        'should_stop': False,
        'stringio': VisibleStringIO,
        'update_env': False,
    }]

    @staticmethod
    def get(key, value=None):
        if value is None:
            return Check.settings_stack[-1][key]
        return value

    @staticmethod
    @contextmanager
    def set(**kwargs):
        settings = dict(Check.settings_stack[-1])
        settings.update(kwargs)
        Check.settings_stack.append(settings)
        try:
            yield
        finally:
            Check.settings_stack.pop()

    @staticmethod
    @contextmanager
    def set_clean(clean=None, **kwargs):
        clean = clean or Check.clean
        with Check.set(clean=(lambda x: clean(x, **kwargs))
                             if kwargs else clean):
            yield

    @staticmethod
    @contextmanager
    def set_environment(**kwargs):
        env = dict(Check.get('env'))
        env.update(kwargs)
        with Check.set(env=env):
            yield

    @staticmethod
    @contextmanager
    def set_stringio(stringio):
        if stringio is True:
            stringio = VisibleStringIO
        elif stringio is False:
            stringio = io.StringIO
        if stringio is None or stringio is Check.get('stringio'):
            yield
        else:
            with Check.set(stringio=stringio):
                yield


def _validate_current_file():
    def extract_parts(filename):
        with open(filename, encoding='utf-8') as f:
            source = f.read()
        part_regex = re.compile(
            r'# =+@(?P<part>\d+)=\s*\n' # beginning of header
            r'(\s*#( [^\n]*)?\n)+?'     # description
            r'\s*# =+\s*?\n'            # end of header
            r'(?P<solution>.*?)'        # solution
            r'(?=\n\s*# =+@)',          # beginning of next part
            flags=re.DOTALL | re.MULTILINE
        )
        parts = [{
            'part': int(match.group('part')),
            'solution': match.group('solution')
        } for match in part_regex.finditer(source)]
        # The last solution extends all the way to the validation code,
        # so we strip any trailing whitespace from it.
        parts[-1]['solution'] = parts[-1]['solution'].rstrip()
        return parts

    def backup(filename):
        backup_filename = None
        suffix = 1
        while not backup_filename or os.path.exists(backup_filename):
            backup_filename = '{0}.{1}'.format(filename, suffix)
            suffix += 1
        shutil.copy(filename, backup_filename)
        return backup_filename

    def submit_parts(parts, url, token):
        submitted_parts = []
        for part in parts:
            if Check.has_solution(part):
                submitted_part = {
                    'part': part['part'],
                    'solution': part['solution'],
                    'valid': part['valid'],
                    'secret': [x for (x, _) in part['secret']],
                    'feedback': json.dumps(part['feedback']),
                }
                if 'token' in part:
                    submitted_part['token'] = part['token']
                submitted_parts.append(submitted_part)
        data = json.dumps(submitted_parts).encode('utf-8')
        headers = {
            'Authorization': token,
            'content-type': 'application/json'
        }
        request = urllib.request.Request(url, data=data, headers=headers)
        response = urllib.request.urlopen(request)
        return json.loads(response.read().decode('utf-8'))

    def update_attempts(old_parts, response):
        updates = {}
        for part in response['attempts']:
            part['feedback'] = json.loads(part['feedback'])
            updates[part['part']] = part
        for part in old_parts:
            valid_before = part['valid']
            part.update(updates.get(part['part'], {}))
            valid_after = part['valid']
            if valid_before and not valid_after:
                wrong_index = response['wrong_indices'].get(str(part['part']))
                if wrong_index is not None:
                    hint = part['secret'][wrong_index][1]
                    if hint:
                        part['feedback'].append('Namig: {}'.format(hint))


    filename = os.path.abspath(sys.argv[0])
    file_parts = extract_parts(filename)
    Check.initialize(file_parts)

    if Check.part():
        Check.current_part['token'] = 'eyJ1c2VyIjozMzA3LCJwYXJ0IjoxODI2N30:1gDZGX:SpmM-pRn5Ijn7V-g2KQflGteZFI'
        try:
            with Check.input(['12', '34', '56', '65', '43', '21']):
                Check.output(Check.current_part['solution'], [
                    'Prvi kot',
                    '=========',
                    'stopinje: 12',
                    'minute: 34',
                    'sekunde: 56',
                    'Drugi kot',
                    '=========',
                    'stopinje: 65',
                    'minute: 43',
                    'sekunde: 21',
                    'Vsota kotov je 78 stopinj, 18 minut in 17 sekund.',
            ])
            with Check.input(['1', '1', '1', '1', '1', '1']):
                Check.output(Check.current_part['solution'], [
                    'Prvi kot',
                    '=========',
                    'stopinje: 1',
                    'minute: 1',
                    'sekunde: 1',
                    'Drugi kot',
                    '=========',
                    'stopinje: 1',
                    'minute: 1',
                    'sekunde: 1',
                    'Vsota kotov je 2 stopinj, 2 minut in 2 sekund.',
            ])
            
            with Check.input(['12', '34', '3', '32', '34', '59']):
                Check.output(Check.current_part['solution'], [
                    'Prvi kot',
                    '=========',
                    'stopinje: 12',
                    'minute: 34',
                    'sekunde: 3',
                    'Drugi kot',
                    '=========',
                    'stopinje: 32',
                    'minute: 34',
                    'sekunde: 59',
                    'Vsota kotov je 45 stopinj, 9 minut in 2 sekund.',
            ])
            
            with Check.input(['10', '30', '30', '15', '29', '35']):
                Check.output(Check.current_part['solution'], [
                    'Prvi kot',
                    '=========',
                    'stopinje: 10',
                    'minute: 30',
                    'sekunde: 30',
                    'Drugi kot',
                    '=========',
                    'stopinje: 15',
                    'minute: 29',
                    'sekunde: 35',
                    'Vsota kotov je 26 stopinj, 0 minut in 5 sekund.',
            ])
        except:
            Check.error("Testi sprožijo izjemo\n  {0}",
                        "\n  ".join(traceback.format_exc().split("\n"))[:-2])

    if Check.part():
        Check.current_part['token'] = 'eyJ1c2VyIjozMzA3LCJwYXJ0IjoxODI2OH0:1gDZGX:sIdpD_-yjkTJ7Svu13E9DHyjZ74'
        try:
            vhodni = ['1.23456']
            izhodni = ['70', '44']
            with Check.input(vhodni):
                Check.output(Check.current_part['solution'], [
                    'Vnesi kot: ' + vhodni[0],
                    vhodni[0] + ' radianov je ' + izhodni[0] + ' stopinj in ' + izhodni[1] + ' minut.',
            ])
            
            vhodni = ['0.5']
            izhodni = ['28', '38']
            with Check.input(vhodni):
                Check.output(Check.current_part['solution'], [
                    'Vnesi kot: ' + vhodni[0],
                    vhodni[0] + ' radianov je ' + izhodni[0] + ' stopinj in ' + izhodni[1] + ' minut.',
            ])
                
            vhodni = ['1.0']
            izhodni = ['57', '17']
            with Check.input(vhodni):
                Check.output(Check.current_part['solution'], [
                    'Vnesi kot: ' + vhodni[0],
                    vhodni[0] + ' radianov je ' + izhodni[0] + ' stopinj in ' + izhodni[1] + ' minut.',
            ])
        except:
            Check.error("Testi sprožijo izjemo\n  {0}",
                        "\n  ".join(traceback.format_exc().split("\n"))[:-2])

    if Check.part():
        Check.current_part['token'] = 'eyJ1c2VyIjozMzA3LCJwYXJ0IjoxODI2OX0:1gDZGX:QEFTsDZ74HBbaxemO655Suz_l4c'
        try:
            vh = ['14', '35']
            izh = ['132', '30']
            with Check.input(vh):
                Check.output(Check.current_part['solution'], [
                    'Ur: ' + vh[0],
                    'Minut: ' + vh[1],
                    'Kot med urnim in minutnim kazalcem je ' + izh[0] + ' stopinj in ' + izh[1] + ' minut.',
            ])
            
            vh = ['12', '0']
            izh = ['0', '0']
            with Check.input(vh):
                Check.output(Check.current_part['solution'], [
                    'Ur: ' + vh[0],
                    'Minut: ' + vh[1],
                    'Kot med urnim in minutnim kazalcem je ' + izh[0] + ' stopinj in ' + izh[1] + ' minut.',
            ])
            
            vh = ['11', '11']
            izh = ['90', '30']
            with Check.input(vh):
                Check.output(Check.current_part['solution'], [
                    'Ur: ' + vh[0],
                    'Minut: ' + vh[1],
                    'Kot med urnim in minutnim kazalcem je ' + izh[0] + ' stopinj in ' + izh[1] + ' minut.',
            ])
                
            # tudi spodnje teste bi bilo smisleno prepisati kot zgornjega!
            with Check.input(['13', '57']):
                Check.output(Check.current_part['solution'], [
                    'Ur: 13',
                    'Minut: 57',
                    'Kot med urnim in minutnim kazalcem je 76 stopinj in 30 minut.',
            ])
            
            with Check.input(['1', '57']):
                Check.output(Check.current_part['solution'], [
                    'Ur: 1',
                    'Minut: 57',
                    'Kot med urnim in minutnim kazalcem je 76 stopinj in 30 minut.',
            ])
            
            with Check.input(['2', '35']):
                Check.output(Check.current_part['solution'], [
                    'Ur: 2',
                    'Minut: 35',
                    'Kot med urnim in minutnim kazalcem je 132 stopinj in 30 minut.',
            ])
        except:
            Check.error("Testi sprožijo izjemo\n  {0}",
                        "\n  ".join(traceback.format_exc().split("\n"))[:-2])

    print('Shranjujem rešitve na strežnik... ', end="")
    try:
        url = 'https://www.projekt-tomo.si/api/attempts/submit/'
        token = 'Token b47eb18147c843f4468f2cfeab73059790682aa8'
        response = submit_parts(Check.parts, url, token)
    except urllib.error.URLError:
        print('PRI SHRANJEVANJU JE PRIŠLO DO NAPAKE! Poskusite znova.')
    else:
        print('Rešitve so shranjene.')
        update_attempts(Check.parts, response)
        if 'update' in response:
            print('Updating file... ', end="")
            backup_filename = backup(filename)
            with open(__file__, 'w', encoding='utf-8') as f:
                f.write(response['update'])
            print('Previous file has been renamed to {0}.'.format(backup_filename))
            print('If the file did not refresh in your editor, close and reopen it.')
    Check.summarize()

if __name__ == '__main__':
    _validate_current_file()
