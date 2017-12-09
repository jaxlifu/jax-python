import re
#''.replace(r'\\|/|:|*|?|<|>|\|', '')
title = 'ParaText: 以2.5GB每秒的速度处理CSV文件?'
title = re.sub(r'\\|\/|\:|\*|\?|\<|\>|\|', '', title)
print(title)
