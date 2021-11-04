import os
import re
from nltk.tokenize import sent_tokenize
import InsertIntoDb


folder = r'C:\Users\andre\Desktop\final\dataset-2'


def solution_definer(sents):
    solution = ''
    x = re.compile(r'отменено')
    y = re.compile(r'(?=передаче)[\w\s]*отказано')
    a = re.compile(r'части\w*')
    b = re.compile(r'удовлетвор\w+[\w\s]*отказ\w*')
    c = re.compile(r'удовлетвор\w+')
    
    s = re.compile(r'решение:[\s\w\)\;]*(?=[.,])')
    for sent in sents:
        if s.search(sent):
            
            if x.search(sent):
                if solution == 'Не удовлетворено':
                    solution = 'Удовлетворено'
                elif solution == 'Удовлетворено' or solution == 'Частично удовлетворено':
                    solution = 'Не удовлетворено'
                return solution
        
            if y.search(sent):
                solution = '='
                return solution
                
            if a.search(sent):
                solution = 'Частично удовлетворено'
                return solution
                
            if b.search(sent):
                solution = 'Не удовлетворено'
                return solution
                
            if c.search(sent):
                solution = 'Удовлетворено'
                return solution
        
    for sent in sents:
        
        if x.search(sent):
            if solution == 'Не удовлетворено':
                solution = 'Удовлетворено'
            elif solution == 'Удовлетворено' or solution == 'Частично удовлетворено':
                solution = 'Не удовлетворено'
            break
        
        if y.search(sent):
            solution = '='
            break
                
        if a.search(sent):
            solution = 'Частично удовлетворено'
            break
                
        if b.search(sent):
            solution = 'Не удовлетворено'
            break
                
        if c.search(sent):
            solution = 'Удовлетворено'
            break
         
    return solution


def category1_definer(sent):
    patterns = [
        r'(егрюл|юридическ\w+ адрес\w*|государственн\w+ регистрац\w+|регистрац.*запи\w+)',
        r'(прав.*собственнос\w+|истребован\w+|прав.*собственн.*|негаторн.*|владен.*|пользован.*)',
        r'(ликвид\w+|акци\w+|обществ\w|убытк\w+|сдел\w+|директор\w+|общ.*собран\w+)',
    ]
    cats = [
        ('Споры о государственной регистрации', 4),
        ('Споры, связанные с защитой вещных прав', 2),
        ('Корпоративные споры', 1),    
    ]
    
    for i in range(len(patterns)):
        r = re.compile(patterns[i])
        if r.search(sent):
            return cats[i]
        
    return ('Не определено', 0)
    

def category2_definer(sent, cat):
    patterns = []
    cats = []
    if cat == 4:
        patterns = [
            r'(егрюл|смен\w+ юридическ\w+ адрес\w*)',
            r'(кадастр\w*|регистрац.*запис\w+)',
            r'отказ.*государств.*регистрац\w+'
        ]
        cats = [
            ('Споры о государственной регистрации юридического лица и ИП', 41),
            ('Споры о государственной регистрации прав на недвижимое имущество и сделок с ним', 42),
            ('Споры об обжаловании отказа в государственной регистрации прав на недвижимое имущество и сделок с ним', 43)
        ]
    
    elif cat == 2:
        patterns = [
            r'признани.*прав.*собственн.*',
            r'истребован.*имуществ.*',
            r'устранени.*(владен.*|пользован.*|проезд.*)' 
        ]
        cats = [
           ('Споры о признании права собственности', 21),
           ('Споры об истребовании имущества из чужого незаконного владения (виндикация)', 22),
           ('Споры об устранении нарушений прав собственника, не связанных с лишением права (споры по негаторным исками)', 23)
        ]  
    elif cat == 1: 
        patterns = [
           r'(ликвидаци\w.*общества|ликвидаци\w.*лица|ликвид\w*)',
           r'(исклю.*|дол\w+|действит.*акц\w+|перех.*акц\w+|выкуп.*акц\w+.*капита.*)',
           r'(взыскани\w.*(директор\w+|учредител\w+)|причинени\w.*вреда.*хозяйственному|взыск.*директ.*убытк.*)',
           r'(недействитель.*сдел\w+.*(уст.*капит.*|купл.*|общест.*)|недействит.*реш.*(собран.*|совет.*)|недейств.*протокол.*(собр.*|совет.*))',
           r'(прав.*акци\w*|эмитент.*|выкуп.*акци\w)',
           #r'(недействительн.*(собран.*|совета директоров|протокол\w+|назначени\w нового генерального директора))'
        ]    
        cats = [
            ('Споры, связанные с ликвидацией юридических лиц', 11),
            ('Споры, связанные с принадлежностью акций и долей участия, установлением их обременений и реализацией вытекающих из них убытков', 12),
            ('Споры по искам участников юридического лица о возмещении убытков, причиненных юридическому лицу', 13),
            ('Споры о признании недействительными сделок или решений, связанных с юридическим лицом', 14),
            ('Споры, связанные с эмиссией ценных бумаг', 16),
            #('Споры об обжаловании решений органов управления юридического лица', 18)
        ]

    
    for i in range(len(patterns)):
        r = re.compile(patterns[i])
        if r.search(sent):
            return cats[i]    
    
    return ('Не определено', 0)


def demand_definer(sent, cat2):
    patterns = []
    cats = []
    
    if cat2 == 41:
        patterns = [
            r'призн.*недейств.*егрюл',
            r'обязан.*осуществ.*регистрирующ.*орган.*'
        ]
        cats = [
            'О признании недействительными решений, связанных с юридическим адресом',
            'Об обязании осуществить действия по обращению в регистрирующий орган'
        ]
    elif cat2 == 42:
        patterns = [
            r'погашен.*регистр.*запис\w+',
            r'(признан.*незаконн.*службы.*кадастра|признан.*службы.*кадастра.*незаконн.*)'
        ]
        cats = [
            'О погашении регистрационных записей',
            'О признании незаконными решений Федеральной службы государственной регистрации, кадастра и картографии'
        ]
    elif cat2 == 43:
        patterns = [
            r'отказ.*'    
        ]
        cats = [
            'О признании незаконными решений об отказе в государственной регистрации'    
        ]
    
    elif cat2 == 21:
        patterns = [
            r'отсутствующ.*',
            r'собственн\w+'
        ]
        cats = [
            'О признании права собственности отсутствующим',
            'О признании права собственности'
        ]
    elif cat2 == 22:
        patterns =[
            r'чужого.*',
            r'истре.*'
            
        ]
        cats = [
            'Об истребовании имущества из чужого незаконного владения',
            'Об истребовании имущества'
        ]
    elif cat2 == 23:
        patterns = [
            r'не связанных.*лишением',
            r'устранении.*препятствий.*пользов.*',
            r'устранении.*препятствий.*проезд.*'
        ]
        cats = [
            'Об устранении нарушений права, не связанных с лишением владения',
            'Об устранении препятствий в пользовании (своим) имуществом',
            'Об устранении препятствий в проезде по служащему земельному участку'
        ]
    elif cat2 == 11:
        patterns = [
            r'(срок.*ликвидац\w+|ликвидаци\w.*(обществ\w+|лиц\w+))', 
            r'действи\w+.*ликвидатор\w+'
        ]
        cats = [
            'О ликвидации общества',
            'О признании (не)законными действий ликвидатора'
        ]
    elif cat2 == 12:
        patterns = [
            r'стоимост\w.*(акци\w|дол\w+)',
            r'исключени\w.*(участник\w*|акционер\w*)',
            r'выкупит.*(акци\w|дол\w+)'
        ]
        cats =[
            'О взыскании действительной стоимости',
            'Об исключении из общества',
            'Об обязании выкупить акции'
        ]
    elif cat2 == 13:
        patterns = [
            r'убытк.*директор\w*',
            #r'убытк.*(участник\w|учредител\w+)*'
        ]
        cats = [
            'О взыскании убытков с генерального директора',
            #'О взыскании убытков с участников'
        ]
    elif cat2 == 14:
        patterns = [
            r'недейств.*реш.*',
            r'недействит.*сделк\w+'
        ]
        cats = [
            'О признании решения недействительным',
            'О признании сделки недействительной'
        ]
    elif cat2 == 16:
        patterns = [
            r'перево.*акци\w',
            r'обяза\w+договор',
            r'выкупит.*акци\w'
        ]
        cats = [
            'О переводе прав покупателей акций',
            'Об обязании исполнить договор купли-продажи',
            'Об обязании выкупить акции'
        ]
    elif cat2 == 17:
        patterns = [
            r'собрани\w',
            r'передать.*директор\w+'
        ]
        cats = [
            'Об обязании провести общее собрание',
            'Об обязании передать директору оригиналы протокола'
        ]
        
    
    for i in range(len(patterns)):
        r = re.compile(patterns[i])
        if r.search(sent):
            return cats[i]
    
    return 'Не определено'
    
    
d = re.compile(r'(?=(требовани.*:|процессуальн.*вопросы\s?:))[.\)]*(т\.ч\.)?.*\.')
n = re.compile(r'n\s[/\w-]*')
acts = [x[0] for x in os.walk(folder)]
records = []
for i in range(1, len(acts)):
    
    general_category1 = 'Не определено'
    general_category2 = 'Не определено'
    general_demand = 'Не определено'
    general_number = 'Не определено'
    general_solution = 'Не определено'
    general_text = ''

    # walk through files of each act    
    files = [f for f in os.listdir(acts[i])]
    count_inst = 0
    
    for f in files:
        if not f.endswith('themes.txt') and not f.endswith('results.txt'):
            count_inst += 1
            file_path = os.path.join(acts[i], f)
            text = open(file_path, 'r', encoding='utf-8').read()
            general_text += text + '\n'
            sents = sent_tokenize(text.lower())
            
            solution = solution_definer(sents)
            if solution == '':
                general_solution = 'Не определено'
            elif solution != '=':
                general_solution = solution
            
            for sent in sents: 
                if d.search(sent): 
                    
                    if general_category1 == 'Не определено':
                        general_category1 = category1_definer(sent)
                    if general_category1 != 'Не определено' and general_category2 == 'Не определено':
                        general_category2 = category2_definer(sent, general_category1[1])
                    if general_category1 != 'Не определено' and general_category2 != 'Не определено' and general_demand == 'Не определено':
                        general_demand = demand_definer(sent, general_category2[1])
                
                if n.search(sent):
                    number = n.search(sent).group().upper()
                    
                    if general_number == 'Не определено':
                        general_number = number
                        
            if general_number != 'Не определено' and general_demand != 'Не определено':
                break
                    
                    
    records.append((general_number, general_demand, general_solution,
    general_category1[0], general_category2[0], general_text, count_inst))
    print((general_number, general_demand, general_category2, general_category1))
            
InsertIntoDb.DbInsert(records)