from bs4 import BeautifulSoup
import re
import os
import json

path='C:\\Alessandro\\Python\\Master - Gigli\\ikea_ok'

products={}
filelist=[x for x in os.listdir(path) if '.htm' in x]
for filename in filelist: 
        #print('filename: ',filename)
        file_html=open(filename, encoding="utf8")
        soup = BeautifulSoup(file_html, 'html.parser')
        #all_things=soup.find_all()
        res=soup.find_all('div', class_ = 'productDetails')
        title=soup.find('title').text
        #print('TITLE')
        #print(title)
        if title not in products:
            products[title]=[]
        #print(res)
        for tag in res:
              t=False
              dt={}
              dt['productTitle']='Not Available'
              dt['productDesp']='Not Available'
              dt['price']='Not Available'
              dt['previousPrice']='Not Available'
              dt['ratingsCount']='Not Available'
              #print('+++++++++++++++++++++')
              productTitle=tag.find('span', class_ = 'productTitle floatLeft')
              if productTitle is not None: 
               t=True       
               dt['productTitle']=productTitle.text
               #print(productTitle.text)

              productDesp=tag.find('span', class_ = 'productDesp')
              if productDesp is not None:
               t=True
               dt['productDesp']=productDesp.text
               #print(productDesp.text)

              regularPrice=tag.find('span', class_ = 'price regularPrice')
              redPrice=tag.find(class_ = 'redPrice')
              previousPrice=tag.find('span', class_ = 'previousPrice')
              
              if redPrice is not None or regularPrice is not None:
                 if redPrice is not None:
                   #print(filename)      
                   #print('redPrice.text')   
                   #print(redPrice.text)
                   price=redPrice.text.replace('.','')
                   price=price[0:15]
                   if previousPrice is not None:
                    previousPrice=previousPrice.text.replace('.','')
                    #previousPrice=previousPrice[0:15]
                    #print('redPrice: ',redPrice)
                    previousPrice=re.sub('[^0-9,]', "", previousPrice)
                    previousPrice=previousPrice.replace(',','.')
                    dt['previousPrice']=round(float(previousPrice),2)
                    #print('previousPrice: ',previousPrice)
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
                 #print('price: ',price)
                 dt['price']=float(price)

              #rating=tag.find('a', class_ = 'ratingsCount')
              rating=tag.find('div', class_ = 'ratingStarsOnLarge') #'ratingStarsOffLarge') #
              if rating is not None:
               t=True
               #ratingperc=tag.find('div', class_ = 'ratingStarsOnLarge')
               #width=re.sub('[^0-9.]', "", ratingperc.get('style'))
               width=re.sub('[^0-9.]', "", rating.get('style'))
               dt['ratingsCount']=round((float(len(rating.text))*float(width))/100,2)
               #print('dt[''ratingsCount'']: ',dt['ratingsCount'])
              if t:           
               products[title].append(dt)
                                 
print('*********************************************')
'''
for item in products:
    print('-----------------------')
    print(item)
    for it in products[item]:
     print(it)
'''
with open('products.json', 'w', encoding="utf-8", newline='\r\n') as fp:
    json.dump(products, fp, indent=3, ensure_ascii=False)
fp.close()
print('Fine.')
           
        
