import numpy as np
import pygame
import tensorflow as tf  
 
class Display(object):
    
    def __init__(self, model_path, win):
        self.img_size = [win.get_height(), win.get_height()]  
        self.img = np.zeros((28, 28)) 
        self.board_shape = np.shape(self.img)[0]
        self.sizeX = win.get_height() // self.board_shape
        self.sizeY = win.get_height() // self.board_shape
        self.win = win
        self.model = tf.keras.models.load_model(model_path)         
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)
         
    def draw_on_screen(self):  
        """ Вывод рисунка на экран """
        pygame.draw.rect(self.win, (0, 0, 0),(0, 0, self.win.get_width(), self.win.get_height()))
        for i in range(0, np.shape(self.img)[0]): 
            for j in range(0, np.shape(self.img)[1]):    
                if self.img[i][j] == 0 :
                    pygame.draw.rect(self.win, (22, 22, 22), (i * self.sizeX, j * self.sizeY, self.sizeX - 5, self.sizeY - 5)) 
                else:
                    pygame.draw.rect(self.win, (self.img[i][j] * 255,self.img[i][j] * 255,self.img[i][j] * 255), (i * self.sizeX, j * self.sizeY, self.sizeX - 5, self.sizeY - 5))                     
 
    def write_new_value(self, pos, val):
        """ Добавление пикселя в рисунок курсором """
        if pos[0] < self.img_size[0] and pos[1] < self.img_size[1]:      # границы поля для рисования

            if self.img[pos[0]//self.sizeX][pos[1]//self.sizeY] != val:     
                self.img[pos[0]//self.sizeX][pos[1]//self.sizeY] = val
                if pos[0]//self.sizeX+1 < self.board_shape:  # проверка на выход за границы массива снизу
                    if self.img[pos[0]//self.sizeX + 1][pos[1]//self.sizeY] != 1:
                        self.img[pos[0]//self.sizeX + 1][pos[1]//self.sizeY] = val * 0.5 

                if pos[1]//self.sizeY+1 < self.board_shape:  # проверка на выход за границы массива справа
                    if self.img[pos[0]//self.sizeX][pos[1]//self.sizeY + 1] != 1:
                        self.img[pos[0]//self.sizeX][pos[1]//self.sizeY + 1] = val * 0.5  

                if not pos[1]//self.sizeY+1 == 1:  # проверка на выход за границы массива сверху
                    if self.img[pos[0]//self.sizeX][pos[1]//self.sizeY - 1] != 1:
                        self.img[pos[0]//self.sizeX][pos[1]//self.sizeY - 1] = val * 0.5

                if not pos[0]//self.sizeX+1 == 1:  # проверка на выход за границы массива слева
                    if self.img[pos[0]//self.sizeX - 1][pos[1]//self.sizeY] != 1:
                        self.img[pos[0]//self.sizeX - 1][pos[1]//self.sizeY] = val * 0.5
                return True 
        return False

    def draw_prediction(self):
        """ Вывод предсказания для рисунка на экран """
        predictions = self.get_prediction()
        sum = np.sum(predictions)
        for i in range(0, len(predictions[0])):
            numbers = self.myfont.render((f'{chr(48+i)} = {predictions[0][i] / sum}'), True, (200, 200, 200)) # строка для предсказаний  
            self.win.blit(numbers, (self.img_size[0] + 10, 30 * (i + 1)))
        max = np.argmax(predictions[0])
        best_value = self.myfont.render((f'{chr(48 + max)} = {predictions[0][max] / sum}'), True, (80, 80, 220)) # выделение лучшего значения
        self.win.blit(best_value, (self.img_size[0] + 10, 30 * (max + 1)))

    def get_prediction(self):
        input = self.get_img_values()
        return self.model.predict(input)

    def get_img_values(self):
        return np.reshape(self.img, (1, 28, 28, 1)).T
