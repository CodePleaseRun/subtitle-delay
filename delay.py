import datetime


def get_sec(time_str):
    # Slightly edited from https://stackoverflow.com/a/6402859
    """Get seconds elapsed from time format hh:mm:ss"""
    h, m, s = time_str.split(':')
    return int(h) * 3600 + int(m) * 60 + float(s.replace(',', '.'))


def subs_delay(file_name, delay_time):
    '''
    Delay the subtitles of a given SubRip Subtitle file (SRT) by a given time.

            Parameteres:
                    file_name (str): directory to the SubRip Subtitle file
                    delay_time (float): seconds by which subtitles have to be delayed

            Returns:
                    0: if subtitles were delayed successfully
                    1: otherwise
    '''
    try:
        delay_time = float(delay_time)
    except ValueError as er:
        print(str(er))
        return 1

    t_stamps = []
    try:
        with open(file_name, 'r', encoding='UTF-8') as f:
            # getting a nested list of all occurance of time-stamps along with it's position index
            t_stamps = [list(i) for i in list(enumerate(f)) if ' --> ' in i[1]]
    except FileNotFoundError as er:
        print(str(er))
        return 1

    first_stamp = get_sec(t_stamps[0][1].split(' --> ')[0])
    if first_stamp + delay_time < 0:
        print(
            f'Requested delay_time is invalid. Delay should be > -{first_stamp}')
        return 1

    for each in t_stamps:
        ts = each[1].strip().split(' --> ')
        each[1] = [(get_sec(time_str=i) + delay_time) for i in ts]

        stamp_begin = str(datetime.timedelta(seconds=each[1][0]))
        stamp_end = str(datetime.timedelta(seconds=each[1][1]))

        if stamp_begin.rfind('.') == -1:
            stamp_begin += ',000000'
        if stamp_end.rfind('.') == -1:
            stamp_end += ',000000'

        # datetime.timedelta() return milliseconds with 6 digits precision. srt files only likes it till 3.
        string = f'0{stamp_begin[:-3]} --> 0{stamp_end[:-3]}\n'
        string = string.replace('.', ',')
        each[1] = string

    with open(file_name, 'r+', encoding='UTF-8') as f:
        lines = f.readlines()
        for line in t_stamps:
            lines[line[0]] = line[1]
        f.seek(0)
        f.writelines(lines)

    return 0
