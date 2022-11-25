import cv2   # lib para ler o arquivo da imagem em matriz
import numpy as np   # para trabalhar com a matriz da imagem 
import matplotlib.pyplot as plt   # para plotar a imagem
import psutil as ps
import statistics as stt
from numpy import random
import requests as rq


content_img = rq.get('https://media.istockphoto.com/id/530045185/pt/foto/gal%C3%A1xia-andr%C3%B3meda.jpg?s=612x612&w=0&k=20&c=3QSr-rg65t_qB0s_8e37EdfT1monvMMt7rFclLt75OY=').content
with open('test.png','wb') as file:
  file.write(content_img)





# importando a imagem teste


img = cv2.imread('test.png') # importando a imagem original

img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) #deixando a imagem cinza (feia) para poder ser trabalhada melhor

fig, ax = plt.subplots(figsize=(16,9)) # configurando o painel de plotagem

plt.imshow(img,cmap='gray') # colocando a matriz da imagem para plotagem

plt.title('imagem original', fontweight='bold') # confiugrando o titulo da plotagem

#plt.savefig() # plotando a imagem 'virgem'




# criando funções importantes



''' plotagem em 16x9 '''
def plt_169(img,title):
    plt.cla()
    plt.clf()
    
    ax, fig = plt.subplots(figsize=(16,9))
    plt.imshow(img,cmap='gray')
    plt.title(title,fontweight='bold')
    plt.savefig(title.replace(' ','_')+'.png')
#    return plt





# função para adicionar o ruído (ruído gaussiano)

def ruido_gauss(img,taxa_ruido=.5):
#     ruido = np.random.normal(0,taxa_ruido,img.shape) # criando o ruido gaussiano (ruido da normal da matriz) da imagem
    
#     ruido = ruido.astype(np.uint8) # mudando o tipo da matriz para uint8 para que seja aceito na adição de imagem 
    
#     img_r = cv2.add(img,ruido) # adicionando o ruido na matriz da imagem

    mean = 0
    var = 10
    sigma = var*3
    gaussian = np.random.normal(mean, sigma, img.shape) #  np.zeros((224, 224), np.float32)

    noisy_image = np.zeros(img.shape, np.float32)
    
    noisy_image = img + gaussian

    return noisy_image

plt_169(img,'base')
def add_noise(img):
    img_n = img
    row , col = img_n.shape
    number_of_pixels = random.randint(300, 10000)
    for i in range(number_of_pixels):
        y_coord=random.randint(0, row - 1)
        x_coord=random.randint(0, col - 1)
        img_n[y_coord][x_coord] = 255

    number_of_pixels = random.randint(300 , 10000)
    for i in range(number_of_pixels):
        y_coord=random.randint(0, row - 1)
        x_coord=random.randint(0, col - 1)
        img_n[y_coord][x_coord] = 0
         
    return img_n.astype(np.uint8)

'''
def add_noise(image):
      row,col = image.shape
      s_vs_p = 0.5
      amount = 0.004
      out = np.copy(image)
      # Salt mode
      num_salt = np.ceil(amount * image.size * s_vs_p)
      coords = [np.random.randint(0, i - 1, int(num_salt))
              for i in image.shape]
      out[coords] = 1

      # Pepper mode
      num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
      coords = [np.random.randint(0, i - 1, int(num_pepper))
              for i in image.shape]
      out[coords] = 0
     
      return out
'''
img_r = add_noise(img)

fig,ax = plt.subplots(2)

plt_169(img,'original')
#plt.show()
plt_169(img_r,'imagem com ruído')

    


#diferenciando a imagem virgem da imagem com ruido

img_dff = img_r - img

plt_169(img_dff,'ruído gaussiano da imagem')
#plt.show()






pixel = [[36,78,34],
         [23,57,80],
         [30,58,39]]


#mediana caseira (feita por nós)
def mediana2D(arr):
    arr = list(arr)
    lista_n = []
    for l in arr:
        for p in l:
            lista_n.append(p)
    
    lista_n.sort()
    
    if not len(lista_n)%2:
        casa_n1 = len(lista_n)//2
        casa_n2 = casa_n1 + 1
        mediana = (lista_n[casa_n2]+lista_n[casa_n1])/2
        return mediana
    
    else:
        casa_n1 = len(lista_n)//2
        casa_n = casa_n1 
        mediana = lista_n[casa_n]
        return mediana
        
#desvio padrao
def desv_pixel(arr):
    arr = list(arr)
    lista_n = []
    for l in arr:
        for p in l:
            lista_n.append(p)
    
    lista_n.sort()
    desv = stt.stdev(lista_n)*10
#    mediana = mediana2D(arr)
#    n_arr = arr
#    for il,l in enumerate(arr):
#        for ip,p in enumerate(l):
#            #p = p-desv if p<mediana else p
#            n_arr[il][ip] = p+desv
#
    return desv


#mediana real
med_r = np.median(np.array(pixel))

#mediana caseira
med_c = mediana2D(pixel)

print(f'mediana real: {med_r} | mediana caseira: {med_c}')





def mediana2D_filtro(arr):
    nova_arr = arr
#    desv = desv_pixel(arr)
    mediana = mediana2D(arr)
    c = 0
    l = 0
    for lin in arr:
        for p in lin:
           # print(f'o q eh:{p} | oq tô pegando {arr[c][l]}')
            if p>mediana:
                p = mediana
                nova_arr[c][l] = p
            l = l+1
        c = c+1
        l = 0
    return nova_arr

mediana2D_filtro(pixel)



#função para retirar o ruído (pela mediana de cada pixel de matriz)
#from IPython.display import clear_output
import time
import os
np.seterr(all='ignore')

img_r_litle = img_r[10:2000]
plt.imshow(img_r_litle)
# plt.show()
# pixel = img[0][0]/np.median(img[0][0])
# pixel


def plt_(x,y,title):
	plt.cla()
	plt.clf()
	plt.plot(x,y)
	plt.title(title)
	plt.savefig(title.replace(' ','_')+'.png')



os.system('clear')
def mediana_normal(img):
    img_3D = img.reshape((img.shape[0]*img.shape[1])//9,3,3)
    nova_img = img_3D
    i = 0
    c = 0
    l = 0
    
    ping = 0
    ping_lst = []
    rest = 0
    size = len(img_3D)
    time_c = 0
    time_t = 0

    temp_ls = []
    c_ls = []
    cpu_ls = []

    time_curr = time.time()
    for pixel in img_3D:
        time_init = time.time()
        #clear_output(wait=True)
#        os.system('clear')
        curr_min = int(time_c//60)
        curr_s = int(time_c%60)
        
        rest_min = int(rest//60)
        rest_s = int(rest%60)

        time_t_min = int(time_t//60)
        time_t_s = int(time_t%60)
        
        
        temp = (ps.sensors_temperatures()['coretemp'][0].current+ps.sensors_temperatures()['coretemp'][1].current)/2
        cpu_perc = ps.cpu_percent()
        ram = ps.virtual_memory().percent
        #temp_ls.append(temp)
        #cpu_ls.append(cpu_perc)
        #c_ls.append(int(time_c))
	
        #temp,cpu_perc,ram
        
        time_prt = f'[ping: {(ping*1000):.2f}ms | curr: {curr_min}m:{curr_s}s | rest: {rest_min}m:{rest_s}s]'
        sys_info = f'[temp: {temp}°C | RAM:{ram}% | CPU:{cpu_perc}%]'
        
        print(f'indice: {i}/{size} ({(i*100/size):.2f}%) {time_prt}\n{sys_info}',flush=True)


       # median = (np.median(pixel))[
        #print(pixel)
        novo_pixel = mediana2D_filtro(pixel)
        #print(nova_img[c][l])
        nova_img[c] = novo_pixel


        c = c+1


        #nova_img.append(c)
        i+=1
        ping = time.time() - time_init
        ping_lst.append(ping)
        ping_m = (sum(ping_lst)/len(ping_lst))+stt.pstdev(ping_lst)
        rest = ping_m*(size - i)
        time_t = ping_m*size
        time_c = time.time() - time_curr
    
    print('então...')
    #plt_(c_ls,temp_ls,'temp cpu')
    #plt_(c_ls,cpu_ls,'cpu percent')
    nova_img = nova_img.reshape(*img.shape)
    print('foi... sheipado')
    return nova_img

img_denoise = mediana_normal(img_r)

plt_169(img_denoise,'denoise')

