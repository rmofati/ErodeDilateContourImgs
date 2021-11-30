# Resolução do Exercício 1 - Visão Computacional.
# Aluno: Rafael Mofati Campos

import numpy as np
import cv2
import PIL
from PIL import Image
from matplotlib import pyplot as plt

def erosao(img):
    img_erodida = img.copy()
    for x in range(img.shape[0]):               # For Altura da imagem
        for y in range(img.shape[1]):           # For Largura da imagem
            try:
                if img[x][y + 1] == 255 and img[x - 1][y] == 255 and img[x][y] == 255 and img[x+1][y] == 255 and img[x][y-1] == 255:
                    img_erodida[x][y] = 255
                else:
                    img_erodida[x][y] = 0
            except:
                continue
    return img_erodida

def dilatacao(img):
    img_dilatada = img.copy()
    for x in range(img.shape[0]):               # For Altura da imagem
        for y in range(img.shape[1]):           # For Largura da imagem
            try:
                if img[x][y + 1] == 255 or img[x - 1][y] == 255 or img[x][y] == 255 or img[x+1][y] == 255 or img[x][y-1] == 255:
                    img_dilatada[x][y] = 255
                else:
                    img_dilatada[x][y] = 0
            except:
                continue
    return img_dilatada

def dilatacao_separacao(img, img_dilatada):

    for x in range(img.shape[0]):               # For Altura da imagem
        for y in range(img.shape[1]):           # For Largura da imagem
            try:
                if img[x-1][y + 1] == 255 or img[x][y + 1] == 255 or img[x+1][y + 1] == 255 or img[x - 1][y] == 255 or img[x][y] == 255 or img[x+1][y] == 255 or img[x-1][y - 1] == 255 or img[x][y-1] == 255 or img[x+1][y-1] == 255:
                    img_dilatada[x][y] = 255
                else:
                    img_dilatada[x][y] = 0
            except:
                continue
    
    return img, img_dilatada

def contorno(img_dilatada, img_erodida):
    img_contorno = np.zeros_like(img_dilatada)
    for x in range(img_contorno.shape[0]):      # For Altura da imagem
        for y in range(img_contorno.shape[1]):  # For Largura da imagem
            try:
                img_contorno[x][y] = img_dilatada[x][y] - img_erodida[x][y]
            except:
                continue
    return img_contorno

def extracao(img):

    path = "D:\Develop\VC\ExAula1\imgRegioesParaSeparar.png"
    
    img = cv2.imread(path, 0)
    img_zero = cv2.imread(path, 0)
    img_dilatada = cv2.imread(path, 0)
    img_aux = cv2.imread(path, 0)

    for x in range(img.shape[0]):
        for y in range(img.shape[1]):              
                img_zero[x][y] = 0
                img_dilatada[x][y] = 0
                img_aux[x][y] = 0
        
    n = 0
    n_fig = 1

    for x in range(img.shape[0]):
        for y in range(img.shape[1]):               
            if img[x][y] == 255 and n < 1:
                img_aux[x][y] = 255
                print("Aguarde... Separando as formas da imagem. Este processo pode levar até 1min")
                n += 1                    
                dif = 1
                num_pixels_anterior = 0
                while (dif != 0):
                    img_aux, img_dilatada = dilatacao_separacao(img_aux, img_dilatada) 
                    for x in range(img_dilatada.shape[0]):
                        for y in range(img_dilatada.shape[1]): 
                            if img[x][y] == 255 and img_dilatada[x][y] == 255:
                                img_zero[x][y] = 255
                            img_aux[x][y] = img_dilatada[x][y]
                                     
                    num_pixels_atual = np.sum(img_zero)
                    dif = num_pixels_atual - num_pixels_anterior 
                    num_pixels_anterior = num_pixels_atual 
                    
                cv2.imshow(("Imagem Separada " + str(n_fig)),img_zero)
                cv2.imwrite(("D:\Develop\VC\ExAula1\img_separada" + '%d' %n_fig + '.jpg'), img_zero)
    
                for x in range(img_aux.shape[0]):
                    for y in range(img_aux.shape[1]):
                        img[x][y] = img[x][y] - img_zero[x][y]
                        img_zero[x][y] = 0
                        img_dilatada[x][y] = 0
                        img_aux[x][y] = 0                                       

                n = 0
                n_fig += 1

gray_img = cv2.imread('imgRegioesParaErodir.png', 0)
extr_img = cv2.imread('imgRegioesParaSeparar.png', 0)
#(thresh, img) = cv2.threshold(grayImg, 127, 255, cv2.THRESH_BINARY)        # SOMENTE PARA IMAGENS COLORIDA

img_erodida = erosao(gray_img)
img_dilatada = dilatacao(gray_img)
img_contorno = contorno(img_dilatada, img_erodida)

cv2.imshow('Original', gray_img)
cv2.imshow('Erosao', img_erodida)
cv2.imshow('Dilatacao', img_dilatada)
cv2.imshow('Contorno', img_contorno)

cv2.imwrite('imgRegioesParaErodir_Erodida.jpg', img_erodida)
cv2.imwrite('imgRegioesParaErodir_Dilatada.jpg', img_dilatada)
cv2.imwrite('imgRegioesParaErodir_Contorno.jpg', img_contorno)

extracao(extr_img)


cv2.waitKey(0)
cv2.destroyAllWindows()