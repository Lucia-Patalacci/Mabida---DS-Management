from bs4 import BeautifulSoup
import re
import os
import json
from urllib.error import HTTPError
from urllib.request import urlretrieve

path='C:\\Alessandro\\Python\\Master - Gigli\\ikea_ok'
repo='image_ikea\\'
products={}
filelist=[x for x in os.listdir(path) if '.htm' in x]
#print(len(filelist))
nfile=len(filelist)
for filename in filelist:
       nfile-=1
       print('Remaining: ',nfile)
       #print('filename: ',filename)
       file_html=open(filename, encoding="utf8")
       soup = BeautifulSoup(file_html, 'html.parser')
       title=soup.find('title').text
       title = re.sub('[^0-9a-zA-Z]+', '_',title)
       res=soup.find_all('div', class_ = 'threeColumn product ')
       for tag in res:
        images=tag.find('img')                
        if images is not None:
         src=images.get('src')
         productDesp=tag.find('span', class_ = 'productDesp')
         Desc = re.sub('[^0-9a-zA-Z]+', '_', productDesp.text)
         regularPrice=tag.find('span', class_ = 'price regularPrice')
         redPrice=tag.find(class_ = 'redPrice')
         price='NA'
         if redPrice is not None or regularPrice is not None:
                 if redPrice is not None:     
                   #print('redPrice.text')   
                   #print(redPrice.text)
                   price=redPrice.text.replace('.','')
                   price=price[0:15]
                 else:
                   #print(regularPrice.text)      
                   price=regularPrice.text.replace('.','')
                   price=price[0:15]

                 t=True 
                 if price.find('/')>=0:
                   price=regularPrice.text[0:price.find('/')]
                   price=re.sub('[^0-9,]', "", price)
                 else: 
                  price=re.sub('[^0-9,]', "", price)
                 price=price.replace(',','.')

         rating=tag.find('div', class_ = 'ratingStarsOnLarge') #'ratingStarsOffLarge') #
         ratingsCount='NA'
         if rating is not None:
            width=re.sub('[^0-9.]', "", rating.get('style'))
            ratingsCount=str((float(len(rating.text))*float(width))/100)

         filename='https://www.ikea.com'+src
         if 'jpg' in filename[len(filename)-4:len(filename)].lower():
             try:
              imagename=src.replace('/','')           
              urlretrieve(filename,repo+title+'--'+Desc+'__'+'Price_'+price+'__Rating_'+ratingsCount+'__'+imagename.replace('PIAimages',''))
             except FileNotFoundError as err:
              print(err)   # something wrong with local path
             except HTTPError as err:
              print(err)  # something wrong with url
print('End.')
        #images = [img for img in soup.findAll('img')]
        #images = [img for img in res.find('img')]
        #image_links = [each.get('src') for each in images]

        #title=soup.find('title').text
        #print('TITLE')
        #print(title)
'''
        c=0
        for each in image_links:     
            c+=1
            filename='https://www.ikea.com'+each
            print(filename)
            if 'jpg' in filename[len(filename)-4:len(filename)].lower():
             try:
              nm='image'
              if 'PIAimages' in each:
                      nm='PIAimages'
                      
              urlretrieve(filename,nm+str(c)+'.jpg')
             except FileNotFoundError as err:
              print(err)   # something wrong with local path
             except HTTPError as err:
              print(err)  # something wrong with url
                                 
print('*********************************************')

for item in products:
    print('-----------------------')
    print(item)
    for it in products[item]:
     print(it)

with open('products.json', 'w', encoding="utf-8", newline='\r\n') as fp:
    json.dump(products, fp, indent=3, ensure_ascii=False)
fp.close()
'''
           
        
