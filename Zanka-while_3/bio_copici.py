# =============================================================================
# Bio čopiči
#
# S tekmovanja RTK 2014
# =====================================================================@018947=
# 1. podnaloga
# V Ajdovščini tovarna Wlahna d. o. o. proizvaja krasne veganske bio čopiče, v celoti
# narejene iz lesa. Leseni ročaji so tako ali tako nekaj običajnega, v tej tovarni pa
# celó konico čopiča izdelajo iz lesa iste vrste, ki ga zmeljejo in predelajo v celulozna
# vlakna.
# V skladišču podjetja imajo lesene palčke enake debeline, a različnih dolžin, iz
# katerih želijo izdelati same enake čopiče. Za posamezen ročaj potrebujejo $dol_rocaj$ centimetrov
# lesa v enem kosu. Za konico čopiča pa potrebujejo toliko zmletega lesa, kot
# ga nastane iz $dol_konica$ centimetrov ene ali več palčk.
# 
# #### Naloga
# Napiši funkcijo `koliko_copicev(dol_rocaj, dol_konica, dol_palic)`, ki vrne število čopičev, ki jih podjetje
# s trenutno zalogo lesa lahko proizvede.
# 
# #### Vhodni podatki
# 
#     dol_rocaj....dolžina palčke potrebne za en ročaj
#     dol_konica...dolžina palčke potrebna za eno konico
#     dol_palic....tabela dolžin palčk na zalogi v cm
# 
# #### Izhodni podatki
# 
# Zaokroženo naravno število, ki predstavlja največje število čopičev, ki jih podjetje lahko proizvede.
# 
# #### Primer
# 
#     >>> koliko_copicev(4, 20, [423, 116, 235, 13, 119, 60])
#     40
# =============================================================================
def koliko_copicev(dol_rocaj, dol_konica, dol_palic):
    """
    fun vrne št čopičev, ki jih lahko podjetje
    s trenutno zalogo proizvede.
    
    """




































































































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
                errors.append('nastavijo {0} na {1!r} namesto na {2!r}'.format(x, global_env[x], v))
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
        Check.current_part['token'] = 'eyJ1c2VyIjozMzA3LCJwYXJ0IjoxODk0N30:1gNcDR:-yfjZ6C4gm50iu320x_C7JAphfg'
        try:
            L0 = [423, 116, 235, 13, 119, 60]
            L1 = [423, 116, 235, 13, 119, 60, 336, 154, 322, 56, 86, 57, 201, 369, 420, 196, 348, 379, 450, 37, 346, 258, 213, 158,
                  379, 445, 322, 200, 435, 319, 371, 13, 152, 409, 164, 320, 436, 272, 371, 453, 96, 191, 349, 287, 164, 265, 251,
                  218, 422, 123, 370, 290, 82, 442, 498, 175, 386, 26, 440, 187, 215, 16, 212, 398, 171, 371, 89, 269, 251, 233, 40,
                  231, 367, 482, 329, 364, 353, 275, 15, 342, 21, 41, 2, 67, 22, 224, 306, 464, 454, 376, 156, 101, 139, 284, 207,
                  91, 323, 494, 424, 306, 99]
            L2 = [51, 365, 54, 500, 381, 453, 59, 207, 459, 460, 18, 435, 500, 352, 301, 454, 497, 26, 167, 266, 500, 492, 218, 108,
                  234, 250, 324, 451, 329, 116, 161, 340, 388, 334, 104, 314, 263, 332, 276, 356, 239, 249, 193, 213, 417, 287, 120,
                  167, 353, 172, 100, 155, 333, 369, 24, 434, 266, 11, 126, 377, 150, 117, 209, 104, 248, 461, 140, 245, 36, 175,
                  200, 107, 135, 82, 343, 300, 218, 153, 314, 78, 129, 440, 351, 18, 257, 94, 159, 384, 37, 247, 179, 347, 391, 340,
                  157, 290, 289, 115, 19, 294, 74]
            L3 = [121, 216, 203, 467, 284, 253, 494, 329, 157, 267, 35, 443, 375, 259, 498, 267, 482, 462, 361, 243, 8, 233, 76,
                  311, 485, 452, 259, 190, 418, 66, 103, 191, 214, 269, 458, 348, 99, 155, 271, 268, 458, 247, 352, 34, 390, 192,
                  78, 152, 436, 86, 112, 116, 112, 335, 95, 42, 250, 277, 162, 201, 194, 359, 495, 121, 428, 273, 429, 470, 416,
                  179, 343, 79, 475, 128, 325, 477, 64, 490, 61, 12, 277, 268, 378, 110, 43, 107, 411, 192, 426, 153, 296, 495, 237,
                  19, 337, 470, 43, 420, 305, 69, 296]
            L4 = [227, 451, 334, 286, 212, 13, 222, 396, 245, 197, 3, 305, 183, 416, 19, 182, 225, 56, 409, 414, 283, 17, 284, 342,
                  25, 102, 321, 426, 30, 433, 225, 221, 401, 84, 384, 324, 244, 383, 442, 293, 475, 488, 258, 481, 6, 186, 261, 351,
                  432, 403, 87, 237, 153, 189, 430, 421, 32, 168, 181, 467, 496, 86, 178, 17, 20, 434, 181, 178, 5, 186, 496, 136,
                  147, 426, 476, 201, 493, 124, 228, 495, 214, 466, 338, 39, 208, 496, 216, 270, 355, 140, 215, 319, 217, 78, 239,
                  274, 330, 61, 239, 464, 210]
            L5 = [433, 410, 82, 30, 301, 37, 215, 30, 325, 305, 196, 384, 15, 262, 374, 349, 449, 433, 115, 351, 54, 77, 1, 160,
                  135, 212, 110, 13, 165, 258, 214, 16, 53, 281, 99, 446, 446, 362, 184, 314, 149, 63, 83, 289, 40, 463, 150, 311,
                  112, 139, 25, 410, 100, 86, 407, 258, 335, 478, 230, 302, 32, 211, 263, 236, 168, 420, 214, 298, 310, 445, 208,
                  84, 492, 277, 424, 498, 196, 281, 276, 305, 172, 349, 387, 49, 481, 486, 187, 297, 83, 471, 483, 223, 381, 300,
                  121, 127, 46, 186, 187, 40, 118]
            L6 = [253, 120, 136, 171, 438, 375, 286, 330, 356, 230, 459, 192, 81, 79, 139, 22, 451, 335, 99, 272, 97, 310, 361, 159,
                  53, 303, 153, 356, 109, 25, 308, 307, 151, 48, 62, 407, 474, 396, 289, 221, 282, 428, 159, 397, 407, 240, 150,
                  337, 225, 246, 68, 141, 14, 153, 240, 246, 372, 264, 116, 425, 70, 305, 55, 43, 372, 86, 192, 333, 455, 28, 260,
                  239, 8, 274, 450, 92, 201, 150, 292, 390, 15, 371, 83, 15, 149, 25, 139, 32, 113, 185, 19, 144, 174, 351, 489,
                  341, 327, 140, 292, 195, 136]
            
            
            Check.equal('koliko_copicev(4, 20, {0})'.format(L0), 40)
            Check.equal('koliko_copicev(4, 20, {0})'.format(L1), 1054)
            Check.equal('koliko_copicev(1, 5, {0})'.format(L2), 4154)
            Check.equal('koliko_copicev(3, 35, {0})'.format(L3), 694)
            Check.equal('koliko_copicev(30, 200, {0})'.format(L4), 113)
            Check.equal('koliko_copicev(4, 20, {0})'.format(L5), 997)
            Check.equal('koliko_copicev(4, 20, {0})'.format(L6), 931)
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
            print('Posodabljam datoteko... ', end="")
            backup_filename = backup(filename)
            with open(__file__, 'w', encoding='utf-8') as f:
                f.write(response['update'])
            print('Stara datoteka je bila preimenovana v {0}.'.format(backup_filename))
            print('Če se datoteka v urejevalniku ni osvežila, jo zaprite ter ponovno odprite.')
    Check.summarize()

if __name__ == '__main__':
    _validate_current_file()
