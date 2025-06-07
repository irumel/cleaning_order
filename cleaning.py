from datetime import datetime
from zoneinfo import ZoneInfo

info_path = 'info.txt'
log_path = 'log.txt'
info_log_path = 'info_log/info_log_'
history_path = 'history.txt'

log_dic_list = [{0: '\t', 1: 'exception: ', 2: 'enter today\'s implementer: ', 3: 'activate person: ', 4: 'deactivate person: ', 5: 'add person: ', 6: 'save info log:'},
                {0: '', 1: 'read infofile', 2: 'write infofile', 3: 'write historyfile', 4: 'write ideal infofile'},
                {0: '', 1: 'Nothing entered', 2: 'Wrong input', 3: 'Already activated', 4: 'Already deactivated', 5: 'Not in the list', 6: 'Nothing inputted'}]

def log(log_info):
  now_korea = datetime.now(ZoneInfo("Asia/Seoul"))
  formatted_time = now_korea.strftime("%Y/%m/%d (%a) %H:%M:%S")

  # log_info[0]: log type code
  # (0: tap, 1: exception, 2: enter today's implementer, 3: activate person, 4: deactivate person, 5: add person)
  # log_info[1]: function
  # (0: N/A, 1: read infofile, 2: write infofile, 3: write historyfile, 4: write ideal infofile)
  # log_info[2]: detailed information
  # (0: N/A, 1: Nothing entered, 2: Wrong input, 3: Already activated, 4: Already deactivated, 5: Not in the list, 6: Nothing inputted)
  # log_info[3]: additional information

  f = open(log_path, 'a')
  f.writelines(f'{formatted_time}\t{log_dic_list[0][log_info[0]]}{log_dic_list[1][log_info[1]]}{log_dic_list[2][log_info[2]]}{log_info[3]}\n')
  f.close()

def read_infofile():
  log([0, 1, 0, ''])
  info = []
  f = open(info_path, 'r')
  while True:
    line = f.readline()
    if line == '': break

    person_info = line.split()
    for i in range(1, len(person_info)):
      person_info[i] = int(person_info[i])
    info.append(person_info)
  f.close()
  return info

def write_infofile(info, implementer):
  log([0, 2, 0, f': for implementer ({implementer})' if implementer else ': for update'])
  f = open(info_path, 'w')
  if implementer:
    for i in info:
      if (i[0] in implementer) and i[5]:
        i[2] += 1
        i[4] = i[2] - i[3]
        f.writelines(f'{i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]}\n')
      else:
        f.writelines(f'{i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]}\n')
  else:
    for i in info:
      i[4] = i[2] - i[3]
      f.writelines(f'{i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]}\n')
  f.close()

def info_log():
  info = read_infofile()
  now_korea = datetime.now(ZoneInfo("Asia/Seoul"))
  formatted_time = now_korea.strftime("%Y%m%d_%H%M%S")
  f = open(info_log_path + formatted_time + '.txt', 'w')
  for i in info:
    f.writelines(f'{i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]}\n')
  f.close()
  log([6, 0, 0, f' {formatted_time}'])

def write_ideal_infofile(info, top2_implementer):
  log([0, 4, 0, f': {top2_implementer}'])
  f = open(info_path, 'w')
  for i in info:
    if i[0] in top2_implementer:
      i[3] += 1
      i[4] = i[2] - i[3]
      f.writelines(f'{i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]}\n')
    else:
      i[4] = i[2] - i[3]
      f.writelines(f'{i[0]} {i[1]} {i[2]} {i[3]} {i[4]} {i[5]}\n')
  f.close()

def check_list(name, info):
  result = False
  for i in info:
    if name == i[0] and i[5] == 1:
      result = True
      break
  return result

def write_implementer(info):
  implementer = input('\n청소 한 사람 (쉼표로 구분): ').replace(' ','').split(',')
  if implementer == ['']:
    print('아무것도 입력되지 않음')
    log([1, 0, 1, '']);
    return

  for i in implementer:
    check = check_list(i, info)
    if not check:
      answer = input(f'"{i}"는 현재 명단에 없습니다. 계속합니까? [Y/N]')
      if answer in ['Y', 'y', 'Yes', 'YES', 'yes']: pass
      elif answer in ['N', 'n', 'No', 'NO', 'no']: print('입력을 취소합니다.'); log([1, 0, 0, ' cancelled']); return
      else: print('잘못된 입력입니다. 입력을 취소합니다.'); log([1, 0, 2, '']); return

  write_infofile(info, implementer)
  print('입력되었습니다.')

  return implementer

def write_historyfile(implementer):
  if not implementer: log([1, 0, 6, '']); return

  log([0, 3, 0, ''])
  now_korea = datetime.now(ZoneInfo("Asia/Seoul"))
  formatted_time = now_korea.strftime("%Y/%m/%d (%a) %H:%M:%S")

  f = open(history_path, 'a')
  f.writelines(f"\n{formatted_time}\t{' '.join(implementer)}\n")
  f.close()

def find_activate_person_and_minimum(info, index):
  active_index = []
  for ind, i in enumerate(info):
    if i[5]: active_index.append(ind)

  smaller = [x for x in active_index if x < index]
  larger = [x for x in active_index if x > index]

  result = []

  if smaller:
      result.append(max(smaller))
  if larger:
      result.append(min(larger))

  minimum = 10000
  for i in result:
    if info[i][3] < minimum: minimum = info[i][3]

  return minimum

def enter_todays_implementer():
  log([2, 0, 0, ''])
  info = read_infofile()
  sorted_info = sorted(info, key=lambda x: (x[2], x[1]))
  ideal_sorted_info = sorted(info, key=lambda x: (-x[5], x[3]))
  top2_implementer = [ideal_sorted_info[0][0], ideal_sorted_info[1][0]]

  print('<우선순위>')
  num = 1
  for data in sorted_info:
    if data[5]: print(f'{num}: {data[0]}'); num += 1

  implementer = write_implementer(info)
  if not implementer: return
  write_historyfile(implementer)
  write_ideal_infofile(info, top2_implementer)
  info_log()

def activate_person():
  log([3, 0, 0, ''])
  info = read_infofile()

  name = input('활성화할 사람의 이름: ').replace(' ', '')
  if not name:
    print('아무것도 입력되지 않음')
    log([1, 0, 1, '']);
    return
  log([0, 0, 0, f'entered: {name}'])
  info = sorted(info, key=lambda x:  x[1])
  flag = 0
  for i in range(len(info)):
    if info[i][0] == name:
      flag = 1
      if info[i][5] == 1: print('이미 활성화되었습니다.'); log([1, 0, 3, f' ({name})']); return
      info[i][5] = 1
      info[i][3] = find_activate_person_and_minimum(info, i)
      info[i][2] = info[i][4] + info[i][3]
      break

  if not flag:
    print(f'{name}은 명단에 없습니다.'); log([1, 0, 5, f' ({name})']); return

  print(f'활성화되었습니다: {name}')
  write_infofile(info, None)
  info_log()

def deactivate_person():
  log([4, 0, 0, ''])
  info = read_infofile()

  name = input('비활성화할 사람의 이름: ').replace(' ', '')
  if not name:
    print('아무것도 입력되지 않음')
    log([1, 0, 1, '']);
    return
  log([0, 0, 0, f'entered: {name}'])
  flag = 0
  for i in range(len(info)):
    if info[i][0] == name:
      flag = 1
      if info[i][5] == 0: print('이미 비활성화되었습니다.'); log([1, 0, 4, f' ({name})']); return
      info[i][5] = 0
      break

  if not flag:
    print(f'{name}은 명단에 없습니다.'); log([1, 0, 5, f' ({name})']); return

  print(f'비활성화되었습니다: {name}')
  write_infofile(info, None)
  info_log()

def add_person():
  log([5, 0, 0, ''])
  info = read_infofile()

  name = input('추가할 사람의 이름: ').replace(' ', '')
  if not name:
    print('아무것도 입력되지 않음')
    log([1, 0, 1, '']);
    return
  try: number = int(input('구역 (정수): '))
  except: print('잘못된 입력. 추가를 취소합니다.'); log([1, 0, 2, '']); return
  log([0, 0, 0, f'entered: {name}, {number}'])

  info = sorted(info, key=lambda x: x[1])
  index_max = 0
  clean_num_min = 10000
  for i in range(len(info)):
    if info[i][1] == number:
      index_max = i
      if info[i][3] < clean_num_min: clean_num_min = info[i][3]

  info.insert(index_max + 1, [name, number, clean_num_min, clean_num_min, 0, 1])

  write_infofile(info, None)
  info_log()
