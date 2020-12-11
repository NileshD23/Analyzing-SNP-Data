# Lab 5
## Write functions to check if a string is valid for each of the following cases. 
#  Assume that the function would be used in the following context, where wed like 
#  to check if a string has a particular pattern, and if so, execute a set of statements: 

# =================================== Part I ==================================

## a. Check to see if a string contains a valid Homo sapiens locus, e.g. 6p21.3, 11q1.4,
#  22p11.2. (Hint: a Human locus name consists of a number between 1 and 23 or an X or
#  Y, p (short) or q (long) denoting a chromosomal arm, a band number, a period, and a
#  sub-band number). Function name: is_valid_humanlocus

def is_valid_humanlocus(input_str):
    # 1. Look for p or q, and '.'
    if (input_str.find('p') == -1 or input_str.find('q') == -1) and input_str.find('.') == -1:
        return False
    else:
    # 2. Split by '.' and see if the sub-band is a number
        # Using the maxsplit operator = 1
        [first_part, sub_band] = input_str.split('.', 1)
        # print(first_part, ' ', sub_band) # Debug
        # Check if sub_band is a number
        if not sub_band.isdigit(): # not False = True
            return False
        
    # 3. Split by 'p' or 'q' and check validity of both chr_num and band_num
        # Split by either p or q (We already know there's either 'p' or 'q')
        if input_str.find('p') > 0:
            splitby = 'p'
        else: splitby = 'q'
        [chr_str, band_num] = first_part.split(splitby, 1)
        
        # print(chr_str, ' ', band_num) # Debug
    
        if not chr_str.isdigit():
            if not (chr_str == 'X' or chr_str == 'Y'):
                return False
        if not band_num.isdigit():
            return False
        
    # If none of these happens, return True
    return True

# 1: assert on: '6p21.3', '11q1.4', and '22p11.2'
assert(is_valid_humanlocus('6p21.3'))
assert(is_valid_humanlocus('11q1.4'))
assert(is_valid_humanlocus('22p11.2'))

assert(is_valid_humanlocus('Xp11.2'))

# 2: assert on: 'chr1:1000', 'nonsense', and '2a11p'
assert(is_valid_humanlocus('chr1:1000') == False) # So that it doesn't give an assertion error
assert(is_valid_humanlocus('nonsense') == False)
assert(is_valid_humanlocus('2a11p') == False)


# 3: Write two additional assertion statements that should check invalid examples and
# explain why you chose them (e.g. is an element out of range, did you expect a
# number here?, etc)

assert(is_valid_humanlocus('Xp11.1p') == False)
assert(is_valid_humanlocus('24p11.1p') == False)



# =================================== Part II =================================

## For this problem you will analyze data from sets of single nucleotide polymorphisms (SNPs) that
#  commonly vary in the human population. There are two datasets, extracted from
#  http://23andme.com, one from the fictitious male, Greg Mendel, and the other from his wife, Lilly
#  Mendel

## a. The data in these files are poorly formatted; you will need a set of Python string
#  expressions to properly extract all of the information. Parse out the SNP id,chromosome, 
#  position and SNPs for each row. For example the first row,
#  rs3094315chr1-742429(A,G) 
#  could be parsed to:
#  id  Chr  Position  SNP1  SNP2
#  rs3094315  1  742429  A  G

# Parsing the string
poor_str = 'rs3094315chr1-742429(A,G)'
[rsid, second] = poor_str.split('chr')
[chr_str, second] = second.split('-')
[pos_str, second] = second.split('(')
first_base = second[0]
second_base = second[2]

print('\t'.join([rsid, chr_str, pos_str, first_base, second_base]))


# Hint: a dictionary for each person, each one containing 4 parallel lists (e.g. key  Chr  is
# associated with a list with the chromosome values, key  Position  is associated with a list
# of the position values) is a reasonable data structure for this type of data

# Read from a file, parse each line and put everything inside a dictionary

if 0: # This block won't execute, the purpose is to show the thought process
    filename = 'GregMendel_SNPs.txt'
    file_ptr = open(filename, 'r')
    
    Person_dict = {'rsid':[],
                   'chr_num':[],
                   'position':[],
                   'bases':[]
                   }
    
    for poor_str in file_ptr:
        poor_str = poor_str.rstrip()
        [rsid, second] = poor_str.split('chr')
        
        # There maybe more than one '-'
        [chr_str, second] = second.split('-', 1)
        [pos_str, second] = second.split('(')
        bases = second[0] + second[2]
        
        Person_dict['rsid'].append(rsid)
        if chr_str.isdigit():
            Person_dict['chr_num'].append(int(chr_str))
        
        if pos_str.isdigit():
            Person_dict['position'].append(int(pos_str))
        
        Person_dict['bases'].append(bases)
    
    file_ptr.close()

## b. Once you ve finished part (a), use your code to define a function called
#  read_SNP_file, which you then call from your main script to process both Greg and
#  Lilly s data. The function should accept a string with the file name as an argument and
#  return a data structure with all of the individual s SNP information. Also, add an assert
#  statement inside this function to guarantee that the chromosome number is valid (we ve
#  only given you the data from the autosomes, so all SNPs should be on chromosomes 1-22)

def read_SNP_file(filename):
    file_ptr = open(filename, 'r')
    
    Person_dict = {'rsid':[],
               'chr_num':[],
               'position':[],
               'bases':[]
               }

    for poor_str in file_ptr:
        poor_str = poor_str.rstrip()
        [rsid, second] = poor_str.split('chr')
        [chr_str, second] = second.split('-',1)
        [pos_str, second] = second.split('(')
        bases = second[0] + second[2]
        
        Person_dict['rsid'].append(rsid)
        if chr_str.isdigit():
            # Checking valid chromosome number
            assert(1 <= int(chr_str) <= 22)
            Person_dict['chr_num'].append(int(chr_str))
        
        if pos_str.isdigit():
            Person_dict['position'].append(int(pos_str))
        
        Person_dict['bases'].append(bases)
 
    file_ptr.close()
    return Person_dict


Greg_dict = read_SNP_file('GregMendel_SNPs.txt')
Lilly_dict = read_SNP_file('LillyMendel_SNPs.txt')

## c. On Chromosome 10, find the largest region of shared SNPs between Lilly and Greg. The
#answer will be in the form of a pair of genomic coordinates (Position1, Position2). Below
#is an example of a region of shared SNPs (in bold). In this case, report the shared
#region as (31123, 31625).
#Chromosome Position Lilly Greg
#10 31,000 AA AT
#10 31,123 TT TT
#10 31,319 AT AT
#10 31,625 CC CC
#10 31,779 GA CC

# Hint: if you ve left your SNPs in genome position order in your lists, you can iterate
# through the list to find stretches of SNPs that are identical

# Getting indices of all the chromosome 10
indices = [i for i in range(len(Greg_dict['chr_num'])) if Greg_dict['chr_num'][i] == 10]

# Global (max) information
max_length = -5
max_start_ind = -10
max_end_ind = -10

# Local information (for each region)
start_ind = -5
end_ind = -5
curr_length = 0

for i in indices:
    # Start of a region
    if (Greg_dict['bases'][i] == Lilly_dict['bases'][i]):
        if curr_length == 0:
            curr_length = curr_length + 1
            start_ind = Greg_dict['position'][i]
        else:
            curr_length = curr_length + 1
    # We have passed the region of match and over by 1
    else:
        end_ind = Greg_dict['position'][i-1]
        
        # If we have a got a region, see if its bigger than what we already have so far
        if curr_length != 0:
            if max_length < curr_length:
                max_length = curr_length
                max_start_ind = start_ind
                max_end_ind = end_ind
        
        # reset local information variables
        curr_length = 0
        start_ind = -5
        end_ind = -5

# max_start -> 341235; max_end -> 341348
        
# max_start_ind -> 73515890; max_end_ind -> 74789905
        

# The data is sorted by chromosome number and within the same chromosome number, 
# by positions. And so we don't actually need to do any sorting. But if we had to
# do that, following are some ideas.

if 0:
    # Check if the positions are already sorted
    all(Greg_dict['position'][i] <= Greg_dict['position'][i+1] for i in indices[0:-1])
    
    # Sort positions and get indices too (so that it can be applied to other lists too)
    # sorted(range(len(myList)),key=lambda x:myList[x])
    # sorted_list = sorted(range(len(indices)), key=Greg_dict['position'].__getitem__)
    sorted_list = sorted((e,i) for i,e in enumerate(Greg_dict['position'][indices[0]:]))

## d. The SNP_Definitions.txt file contains information about the effects of various
#  SNPs. Load the SNP definitions into a data structure so that you can lookup a
#  description given a SNP id and the bases. (HINT: use a dictionary with the SNP id as the
#  key)
    
SNP_file = 'SNP_definitions.txt'
SNP_fp = open(SNP_file, 'r')

SNP_dict = {}

header= SNP_fp.readline()
for line in SNP_fp:
    line = line.rstrip()
    
    [rsid, genotype, info] = line.split('\t')
    key = '_'.join([rsid, genotype])
    SNP_dict[key] = info
    
SNP_fp.close()

## e. Use the information you read in from SNP_Definitions.txt to identify what the
#  region between 22070000 and 22106000 on chromosome 9 suggest about Greg's
#  chance of a heart attack. What about Lilly's chance of a heart attack? (Hint: find the
#  SNPs from this region, and use the information from the  Description  column to guide
#  your reasoning)
#  (If you feel bold, the use of a list comprehension would be very cool here)

def find_heart_disease_risk(Person_dict, SNP_dict, Name):
    rsid_list = Person_dict['rsid']
    chr_num_list = Person_dict['chr_num']
    bases_list = Person_dict['bases']
    position_list = Person_dict['position']

    start_pos = 22070000
    end_pos = 22106000
    
    print('\n', Name, "'s Risk of heart disease: ")
    for i in range(len(chr_num_list)) :
        if (chr_num_list[i] == 9) and (start_pos <= position_list[i] <= end_pos):
            key = '_'.join([rsid_list[i], bases_list[i]])
            if key in SNP_dict.keys():
                print(key, ':', SNP_dict[key])

    # Use of list comprehension to do the same thing
    # [ print(key, ':', SNP_dict[key]) for key in ['_'.join([rsid_list[i], bases_list[i]]) for i in range(len(chr_num_list)) 
    # if (chr_num_list[i] == 9) and (22070000 <= position_list[i] <= 22106000)] if key in SNP_dict.keys()]
    
    # [print(key, ':',SNP_dict['_'.join([rsid_list[i], bases_list[i]])]) 
    # for i in range(len(chr_num_list)) 
    # if (chr_num_list[i] == 9) and 
    # (22070000 <= position_list[i] <= 22106000) and 
    # ('_'.join([rsid_list[i], bases_list[i]]) in SNP_dict.keys())]                

find_heart_disease_risk(Greg_dict, SNP_dict, 'Greg')
find_heart_disease_risk(Lilly_dict, SNP_dict, 'Lilly')


## f. Find a SNP locus that interests you at SNPedia.com. Describe what is known about the
#  locus. Also, check what the SNP status is in both Lilly and Greg. What does the SNP
#  suggest about their possible health?

