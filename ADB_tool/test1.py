file1 = r"C:\Users\lida\Desktop\123.txt"  # 存放图以所示文本的.txt
file2 = r"C:\Users\lida\Desktop\1234.txt"

# file1 = "/home/qtxu/semeval_data/1.txt"


#检验是否含有中文字符
def isContainChinese(s):
     for c in s:
         if ('\u4e00' <= c <= '\u9fa5'):
                return True
         return False


lists = []
# 从bert_pt_top10_*.txt中筛选出所有的英文单词
with open(file2, 'w') as fp:
    fp.write('')
with open(file1, "r",encoding='utf-8') as fr:
    lines = fr.readlines()
    # print(lines)
    for line in lines:
        a = ''.join(line.split(' ')[0].split())
        # print(a)
        lists.append(a)

print(lists)

for a in lists:
    if a.strip().isalpha() and not isContainChinese(a) and len(a) != 1:
        print(a)
        with open(file2, 'a+', encoding='gbk') as fp:
             fp.write(a + '\n')
print('文件已写完！')

with open(file1, 'w') as fp:
    fp.write('')

import win32api

win32api.ShellExecute(0, 'open',file2, '', '', 1)


