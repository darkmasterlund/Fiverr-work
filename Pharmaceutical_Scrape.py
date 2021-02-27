# Import the functions urlopen and beautifulsoup to open and interact with web pages
from urllib.request import urlopen
from bs4 import BeautifulSoup as soup

# Function to revmove unencoded characters
def letters_only(word):
    # Takes in a string, or a list of strings
    # Outputs a strion or list of strings without any unencoded characters
    # Directories of letters numbers and dash, period
    letters = 'abcdefghijklmnopqrstuvwxyz .-'
    digits = '0123456789'
    upper_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    
    # If the word is a strin
    if type(word) == str:
        # For each letter in the word
        for ltr in word:
            # If it is not in the directories, replace it
            if ltr not in letters and ltr not in upper_letters and ltr not in digits:
                word = word.replace(ltr, '')
    
    # If the word is a list
    elif type(word) == list:
        # For each word in the list
        for wrd in range(len(word)):
            # For each letter in the list
            for ltr in word[wrd]:
                # If it's not in direc, replace
                if ltr not in letters and ltr not in upper_letters and ltr not in digits:
                    word[wrd] = word[wrd].replace(ltr, '')
    return word

# Create a csv file to store all the information
phrms = open('pharmaceuticals.csv', 'w')
phrms.write('NAME, PRICE, PERSCRIPTION, MANUFACTURER, INTRO, SALT COMP, HOW TO USE, HOW IT WORKS, IF YOU FORGET TO TAKE, USES, SIDE EFFECTS, SAFETY, TIPS, INTERACTION, QUESTION, ANSWER, ALTERNATES\n')

# List to store all the manufacturers
mnfctrs = []

print('Gathering Manufacturers')
# Gather the list of manufactuers from the various websites
for index in range(129):
    print(f'page {index}')
    # Open the page, read and close
    page = urlopen('https://www.1mg.com/manufacturers?api=true&pageNumber=' + str(index))
    mnfctr_page = page.read()
    page.close()
        
    # Turn into soup, and then string
    mnfctr_page = soup(mnfctr_page, 'html.parser')
    mnfctr_page = str(mnfctr_page)
    
    # For each letter in the page
    for i in range(len(mnfctr_page)):
        # If the letter is the start of the url mark, which is slug for some reason
        if mnfctr_page[i:i+4] == 'slug':
            # Get the url
            url = mnfctr_page[i+7:i+200]
            lim = url.find('"}')
            mnfctrs.append(url[:lim])
            
    print(len(mnfctrs))
    
print('Finished gathering')
# Convert the page into a soup object for easy manipulation
#mnfctr_page = soup(mnfctr_page, 'html.parser')

# Make a list of all the manufacturers
#mnfctrs = mnfctr_page.findAll('div', {'class':'col-sm-3 col-xs-6 mar-B15'})

# For each manufacturer open their page and get a list of their drugs
for mnf in mnfctrs:    
    # Store manufacturer for later writing
    manufacturer = mnf[13:-6]
    manufacturer = letters_only(manufacturer)
    print(manufacturer)
    
    # Open read and close page
    page2 = urlopen('https://www.1mg.com' + mnf)
    drug_page = page2.read()
    page2.close()
    # Convert to a soup object
    drug_page = soup(drug_page, 'html.parser')
    
    # Create a list of the drugs for the manufacturer
    drugs = drug_page.findAll('div', {'class':'col-sm-3 col-xs-6'})
    
    # For each drug on the page, gather the information for that drug
    for drg in drugs:
        # Open read and close page
        page3 = urlopen('https://www.1mg.com' + drg.a['href'])
        info_page = page3.read()
        page3.close()
        # Convert to soup object
        info_page = soup(info_page, 'html.parser')
        
        # Name
        try: name = info_page.find('h1', {'class':'col-6'}).text
        except: continue
        name = letters_only(name)
        print('    ' + name)
        
        # Price / Perscription required?
        price_persc = info_page.findAll('span', {'class', 'footerMedium'})
        if price_persc[1] == None:
            price = 'Not Available'
        else:
            price = price_persc[1].text + ' rupee'
            price = letters_only(price)
        
        if price_persc[0] == None:
            persc = 'Not Available'
        else:
            persc = price_persc[0].text
            persc = letters_only(persc)
        
        # Intro paragraph
        intro_1 = info_page.findAll('div', {'class':'pRegular'})
        if intro_1 == None:
            intro = 'Not Available'
        else:
            intro_1 = [x for x in intro_1 if x.div == None]
            intro_1 = [x.text for x in intro_1]
            intro = ''
            
            for i in intro_1:
                intro += i
                
            intro = letters_only(intro)
        
        # Salt Comp
        salt_comp = info_page.find('div', {'class':'FactBox__rowContent__JHFU7 FactBox__flexCenter__zYkHn col-3'})
        if salt_comp == None:
            salt_comp = 'Not Available'
        else:
            salt_comp = salt_comp.text
            salt_comp = letters_only(salt_comp)
        
        # Uses
        uses = info_page.find('ul', {'class':'marginTop-8'})
        if uses == None:
            uses = ['Not Available']
        else:
            uses = uses.findAll('li')
            uses = [x.text for x in uses]
            uses = letters_only(uses)
        
        # Side Effects
        side_effects = info_page.find('div', {'class':'GroupedAccordion__content__7S-xd GroupedAccordion__collapsed__1I3K2'})
        if side_effects == None:
            side_effects = ['Not Available']
        else:
            side_effects = side_effects.div.div.findAll('li')
            side_effects = [x.text for x in side_effects]
            side_effects = letters_only(side_effects)
        
        # Safety
        labels = info_page.findAll('div', {'class':'DrugContainer__container__2ZFXt'})
        labels = [x.text for x in labels]
        safety = ['Alcohhol: ' + labels[1], 'Pregnancy: ' + labels[2], 'Breastfeeding: ' + labels[3], 'Driving: ' + labels[4], 'Kidney: ' + labels[5], 'Liver: ' + labels[6]]
        safety = letters_only(safety)
        
        # How to Use
        hw_us = info_page.find('div', {'id':'how_to_take_0'}).find('p', {'class':'col-6'})
        if hw_us == None:
            hw_us = 'Not Available'
        else:
            hw_us = hw_us.text
            hw_us = letters_only(hw_us)
        
        # How it Works
        hw_wk = info_page.find('div', {'id':'how_it_works_0'}).find('p', {'class':'col-6'})
        if hw_wk == None:
            hw_wk = 'Not Available'
        else:
            hw_wk = hw_wk.text
            hw_wk = letters_only(hw_wk)
        
        # If you forget to take it
        try: forget = info_page.find('p', {'class':'col-6 marginTop-8'}).text
        except: forget = 'Not Available'
        forget = letters_only(forget)
        
        # Alternate Brands
        alternates = info_page.find('div', {'id':'alternate_brands'}).findAll('div', {'class':'DrugContainer__rowContent__374pc col-3'})
        if alternates == None:
            alt_names = ['Not Available']
        else:
            alt_names = [x.a.text for x in alternates if x.a != None]
            alt_names = letters_only(alt_names)
        
        # Tips
        tips = info_page.find('div', {'id':'expert_advice_0'})
        if tips == None:
            tips = ['Not Available']
        else:
            tips = tips.findAll('li')
            tips = [x.text for x in tips]
            tips = letters_only(tips)
        
        # Interaction
        interacts = info_page.findAll('div', {'class':'DrugContainer__interactionRow__3mIG1'})
        if interacts == []:
            int_names = ['Not Available']
            int_type = ['Not Available']
        else:
            int_names = [x.a.text for x in interacts if x.a != None]
            int_type = [x.findAll('span')[1].text for x in interacts]
            int_names = letters_only(int_names)
            int_type = letters_only(int_type)
        
        # FAQs
        faqs = info_page.findAll('div', {'class':'Accordion__accordion__3c_vu'})
        if faqs == []:
            faqs = ['Not Available']
        else:
            faqs = faqs[7:]
            faq_question = [x.input['id'] for x in faqs]
            faq_answer = faq_answers = [x.find('div', {'class':'Accordion__content__1hNch'}).p.text for x in faqs]
            faq_question = letters_only(faq_question)
            faq_answer = letters_only(faq_answer)
        
        # Write info to file
        phrms.write(f'{name}, {price}, {persc}, {manufacturer}, {intro}, {salt_comp}, {hw_us}, {hw_wk}, {forget}\n')
        
        # Write the uses, safety and side effects as a drop menu
        # For whichever list is longest
        for i in range(len(max(uses, side_effects, tips, int_names, safety, faq_question, alt_names))):
            # Find that value in the list and write it to the file
            # If the value doesn't exist, then use blank
            try: use = uses[i]
            except: use = ''
            
            try: side = side_effects[i]
            except: side = ''
                
            try: safe = safety[i]
            except: safe = ''
                
            try: tip = tips[i]
            except: tip = ''
                
            try: int_n, int_t = int_names[i], int_type[i]
            except: int_n, int_t = '', ''
                
            try: ques, answ = faq_question[i], faq_answers[i]
            except: ques, answ = '', ''
            
            try: alt_n = alt_names[i]
            except: alt_n = ''
                
            try: phrms.write(f',,,,,,,,, {use}, {side}, {safe}, {tip}, {int_n} : {int_t}, {ques}, {answ}, {alt_n}\n')
            except:
                print(f'''
                      {use}
                      {side}
                      {safe}
                      {tip}
                      {int_n}
                      {int_t}
                      {ques}
                      {answ}
                      {alt_n}
                      {alt_p}
                      
                      
                      ''')
                
phrms.close()
        