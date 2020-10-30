import numpy as np
import pygame

 
class Display(object):
    
    def __init__(self, sizeBrX,sizeBrY, win):
        self.sizeBr = [sizeBrX, sizeBrY]
        self.brd = np.array([28,28])  
        self.brd = np.zeros(self.brd) 
        self.board_shape = np.shape(self.brd)[0]
        self.sizeX = sizeBrX // self.board_shape
        self.sizeY = sizeBrY // self.board_shape
        self.win = win
        
        self.myfont = pygame.font.SysFont('Comic Sans MS', 30)   
         
    def draw_on_screen(self):  
        """ drawing picture on window """
        pygame.draw.rect(self.win,(0, 0, 0),(0, 0, 1200, 840 ) )
        for i in range(0, np.shape(self.brd)[0]): 
            for j in range(0, np.shape(self.brd)[1]):    
                if self.brd[i][j] == 0 :
                    pygame.draw.rect(self.win,(22, 22, 22),(i*self.sizeX, j*self.sizeY, self.sizeX-5, self.sizeY-5)) 
                else:
                    pygame.draw.rect(self.win,(self.brd[i][j] * 255,self.brd[i][j] * 255,self.brd[i][j] * 255),(i*self.sizeX, j*self.sizeY, self.sizeX-5, self.sizeY-5))                     


    def new_value(self, pos, val):
        """ setting drawed values to board list """
        if pos[0] < self.sizeBr[0] and pos[1] < self.sizeBr[1]:      # границы поля для рисования
            self.brd[pos[0]//self.sizeX][pos[1]//self.sizeY] = val
            if pos[0]//self.sizeX+1 < self.board_shape:  # проверка на выход за границы массива снизу
                if self.brd[pos[0]//self.sizeX+1][pos[1]//self.sizeY] != 1:
                    self.brd[pos[0]//self.sizeX+1][pos[1]//self.sizeY] = val * 0.5     
            if pos[1]//self.sizeY+1 < self.board_shape:  # проверка на выход за границы массива справа
                if self.brd[pos[0]//self.sizeX][pos[1]//self.sizeY+1] != 1:
                    self.brd[pos[0]//self.sizeX][pos[1]//self.sizeY+1] = val * 0.5  
            if not pos[1]//self.sizeY+1 == 1:  # проверка на выход за границы массива сверху
                if self.brd[pos[0]//self.sizeX][pos[1]//self.sizeY-1] != 1:
                    self.brd[pos[0]//self.sizeX][pos[1]//self.sizeY-1] = val * 0.5
            if not pos[0]//self.sizeX+1 == 1:  # проверка на выход за границы массива слева
                if self.brd[pos[0]//self.sizeX-1][pos[1]//self.sizeY] != 1:
                    self.brd[pos[0]//self.sizeX-1][pos[1]//self.sizeY] = val * 0.5

    def draw_prediction(self, predictions):
        """  prints prediction for each number on right side of window"""
        for i in range(0,len(predictions[0])):
            numbers = self.myfont.render((f'{chr(48+i)} = {  predictions[0][i] }'  ), True, (200, 200, 200)) # string for predictions   
            self.win.blit(numbers,( self.sizeBr[0] + 10, 30 * (i + 1)))
        max = np.argmax(predictions[0])
        best_value = self.myfont.render((f'{chr(48+max)} = {  predictions[0][max] }'  ), True, (80, 80, 220)) # highlighting best value
        self.win.blit(best_value,( self.sizeBr[0] + 10, 30 * (max + 1)))

    def return_value(self):
        return np.reshape(self.brd, (1, 28, 28, 1))
