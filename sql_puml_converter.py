from collections import defaultdict

s = None
with open('file.txt', 'r') as file:
    s = file.read()
    print(s)

s = s.replace('\n(', ' (')
s = s.replace('\n', '')
s = s.replace('\t', '')
s = s.replace(');', ' ) ;')
s = s.replace(' ( ', ' ')
s = s.replace(' ) ', ' ')

left = None
right = None

for i in range(len(s)):
    if s[i] == '(':
        left = i
    if s[i] == ')':
        right = i
    if left is not None and right is not None:
        t1 = s[:left]
        t2 = s[left:right].replace(',', '|')
        t3 = s[right:]
        s = t1 + t2 + t3
        left = None
        right = None

s = s.replace('| ', '|')


s = s.split(';')


dct = {}

for item in s:
    item = ' '.join(item.split())
    item = item.replace(', ', ',').split(',')

    current = None

    for sub in item:
        if current is None and 'create table ' in sub:
            current = sub.split(' ', 3)[2]
            dct[current] = []
            dct[current].append(sub.split(' ', 3)[3])
            continue
        if current:
            sub = sub.replace('|', ',')
            dct[current].append(sub)

new_dct = {}

for key, value in dct.items():
    name = None
    _type = None
    color = None
    relations = None
    new_dct[key] = []
    tmp = False

    for item in value:
        item = item.split(' ')
        for sub in item:
            if name is None:
                name = sub
                continue
            if _type is None:
                _type = sub
                _type = _type.replace(',', ', ')
                continue
            if sub == 'primary':
                color = 0
            if sub == 'references':
                tmp = True
                color = 1
                continue
            if tmp:
                tmp = False
                relations = sub

        new_dct[key].append({'name': name, 'type': _type, 'color': color if color is not None else 2, 'relations': relations})
        name = None
        _type = None
        color = None
        relations = None

colors = {0: 'green', 1: 'orange', 2: 'gray'}

relations = defaultdict(list)
with open('temp.puml', 'w') as file:
    file.write('@startuml\n\n')
    file.write('header Новый проект\n\n')
    file.write(
        'title **Схема БД** \\n \\\n'
        '<size:14>Текущее состояние</size> \\n \\\n\n'
    )
    file.write(
        'legend\n'
        'Легенда:\n'
        '<color:green>первичные ключи\n'
        '<color:orange>внешние ключи\n'
        '<color:olive>первичные ключи, являющиеся внешними\n'
        '<color:gray>нужные для работы поля\n'
        '<color:red>поля, нуждающиеся в доработке или нормализации\n'
        '<color:blue>служебные поля\n'
        '<color:black>неточно идентифицированные поля, использование которых сомнительно\n'
        'end legend\n\n'
    )
    file.write('hide circle\n'
               'skinparam linetype ortho\n'
               'left to right direction\n'
               )
    for key, value in new_dct.items():
        value = sorted(value, key=lambda d: d['color'])
        file.write(f'\nentity {key}' + ' {\n')
        for item in value:
            if item.get('relations'):
                relations[key].append(item.get('relations'))
            file.write(
                f'    --\n'
                f'    * <color:{colors.get(item.get("color"))}>'
                f'**{item.get("name")}**: {item.get("type")}\n'
            )
        file.write('}\n')

    file.write('\n')

    for key, value in relations.items():
        if value:
            for item in value:
                file.write(key + ' }o--|| ' + item + '\n')
            file.write('\n')

    file.write('@enduml')
