from atproto import client_utils

def format(item):
    usage = item['details']['Reikšmė ir vartosena']

    text = client_utils.TextBuilder()\
        .text('✒️ ')\
        .link(item['header'], f'https://ekalba.lt/naujazodziai/a?i={item['uuid']}')\
        .text(f' – {usage['Apibrėžtis']}')
    
    sritys = usage.get('Vartojimo sritys', '')
    if sritys:
        tags = [part.strip() for part in sritys.split(',')]
        text = text.text('\n')
        text = text.tag(f'#{tags[0]}', tags[0])
        for tag in tags[1:]:
            text = text.text(' ')
            text = text.tag(f'#{tag}', tag)
    
    return text