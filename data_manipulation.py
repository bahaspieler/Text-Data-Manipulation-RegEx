import re
import location as lo


frequency_band = input('Insert the band (900 or 1800):--')
freq_band = int(frequency_band)
text= open(lo.trxinfo.path, 'r', encoding='utf-8')
contents= text.read()

p= re.compile(r'(")(\w+)(")(,\s+TRXID\s=\s\d+,\s+FREQ\s=\s\d+,\s+ISMAINBCCH\s=\s[A-Za-z]+,\s+TRXNO\s=\s\d+,)(GTRXGROUPID=\d+)')
m= p.findall(contents)


cell_extract= list(zip(*m))
print('\nPattern with irrelavent tuples:-' ,cell_extract)

del cell_extract[0]
print('Deleted 1 tuple(blank space):-',cell_extract)

del cell_extract[1:3]
print('Cells are extracted:-',cell_extract, '\n')

#CREATING CELL LIST
cellname_list= list(cell_extract[0])
print('Getting all the cell names list:-', cellname_list)

#REMOVING DUPLICATES
cellname_list= list(dict.fromkeys(cellname_list))
print('Duplicates are removed:-',cellname_list, '\n')

gtrxid_list=[]
print('\n<<-----Entering into the FOR LOOP for cellname_list----->>\n')

for cell in cellname_list:

    # OPENING PRE CMD OUTPUT FILE
    text2 = open(lo.cmdutput.path, 'r', encoding='utf-8')
    contents2 = text2.read()

    # REGEX IS APPLIED HERE
    p2 = re.compile(r'(%s)(\s+)(\d+)(\s+)(No|Yes)(\s+)(\d+)(\s+)([A-Za-z]+)(\s+)(\d+)' %cell)
    m2 = p2.findall(contents2)

    list_all = list(zip(*m2))

    # REMOVING UNWANTED LIST ELEMENTS ( SPACES )
    del list_all[1]
    del list_all[2:9]

    # Taking the Desired frequency
    freq = list((list_all[1]))

    if freq_band == 900:
        for f in freq:
            f1 = int(f)
            if f1 < 649:
                f2 = str(f1)
                group_id_index = freq.index(f2)

                break
            else:
                continue

    else:
        for f in freq:
            f1 = int(f)
            if f1 >= 649:
                f2 = str(f1)
                group_id_index = freq.index(f2)

                break
            else:
                continue

    # CONVERTING TUPLE ELEMENT TO LIST (LIST OF LIST)
    new_list = [list(ele) for ele in list_all]


    # GETTING THE GTRXGROUPID
    group_id = new_list[2][group_id_index]


    # MAKING THE STRING TO BE REPLACED
    gtrx = 'GTRXGROUPID='
    gtrxid = gtrx + str(group_id)


    #CREATING GTRXID_LIST FROM A EMPTY LIST
    gtrxid_list.append(gtrxid)
print('GTRXID List:-', gtrxid_list,'\n')





print('\nFinding strings to be replaced...........')

tobe_replaced_string_list=[]
print('To be replaced string list:-', tobe_replaced_string_list)

print('<<-----Entering into the FOR LOOP to get the list----->>')

for cellname in cellname_list:
    cell_string = f'"{cellname}"'

    p3 = re.compile(r'%s,\s+TRXID\s=\s\d+,\s+FREQ\s=\s\d+,\s+ISMAINBCCH\s=\s[A-Za-z]+,\s+TRXNO\s=\s\d+,GTRXGROUPID=\d+' %cell_string)
    m3 = p3.findall(contents)
    tobe_replaced_string_list.append(m3)
print('To be replaced string list:-', tobe_replaced_string_list)

flat_list_tobe_replaced = [item  for sublist in tobe_replaced_string_list for item in sublist]



print('\n''Finding 1st half replacing string...........')
replace_string1=[]

print('1st half Replacing string list:-', replace_string1)



print('<<-----Entering into the FOR LOOP to get the list----->>')
for cellname2 in cellname_list:
    cell_string2 = f'"{cellname2}"'
    p4= re.compile(r'%s,\s+TRXID\s=\s\d+,\s+FREQ\s=\s\d+,\s+ISMAINBCCH\s=\s[A-Za-z]+,\s+TRXNO\s=\s\d+,' %cell_string2)
    m4 =p4.findall(contents)
    replace_string1.append(m4)

print('1st half Replacing string list:-', replace_string1)


#CREATING FULL STRING TO BE REPLACED

print('\nFinding FULL replacing string...........')
full_replace_string = []

print('Full Replacing string list:-', full_replace_string)

print('<<-----Entering into the FOR LOOP to get the list----->>')


n=0

for a in replace_string1:

    half_list = []

    m = 0

    while m < len(a):
        full_replace= a[m]+gtrxid_list[n]
        m+=1

        half_list.append(full_replace)

    n+=1

    full_replace_string.append(half_list)


flat_list_replace = [item for sublist in full_replace_string for item in sublist]

print('Flattening the full replacing string list:', flat_list_replace)


rep={flat_list_tobe_replaced[i]: flat_list_replace[i] for i in range(len(flat_list_tobe_replaced))}

print('Creating Dictionaries from the flat list:', rep)



print('\nFinally Replacing the desired string........')

rep = dict((re.escape(k), v) for k, v in rep.items())

pattern = re.compile("|".join(rep.keys()))
replace = pattern.sub(lambda m: rep[re.escape(m.group(0))], contents)

new_text = open(lo.output.path, 'w')
new_text.write(replace)
new_text.close()

print('\nDONE....................')