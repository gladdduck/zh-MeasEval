import os


# files = os.listdir('zh-brat')

# txt = [ file for file in files if file.endswith('.txt')]
# ann = [ file for file in files if file.endswith('.ann')]
# txt.sort()
# ann.sort()
# for i in range(len(txt)):
#     if txt[i].replace('.txt','') != ann[i].replace('.ann',''):
        
#         print('Error: ', txt[i], ann[i])
#         break

with open('brat/S0960896612001022-1223-1.ann', 'r', encoding='utf-8') as f:
    lines = f.readlines()

a = ['Quantity', '107', '113;125', '133']
b,*_ = a
trans_lines = []
for line in lines:
    line = line.strip('\n').strip().replace('\t\t','\t')
    text = line.split('\t')[-1]
    print(line)
    print(line.split('\t')[1].split(' '))
    if text!='' and len(line.split('\t'))==3 and not line.split('\t')[0].startswith('#'):
        try:
            t,start,end = line.split('\t')[1].split(' ')
        except:
            t,*_ = line.split('\t')[1].split(' ')
            start = -1
            end = -1
        print(t,start,end)
    else:
        print('else')