import draw 
import pygame 
import os
 
def interface(model_path):
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("drawing")
    clock = pygame.time.Clock()
    run = True 
         
    win = pygame.display.set_mode((1200, 840))

    DP = draw.Display(model_path, win)  
    DP.draw_on_screen() 

    while(run): 
        clock.tick(80) 

        if pygame.mouse.get_pressed()[0]:   # обработка левого нажатия мыши
            if DP.write_new_value(pygame.mouse.get_pos(), 1):
                DP.draw_on_screen()  
                DP.draw_prediction()   

        if pygame.mouse.get_pressed()[2]:   # обработка правого нажатия мыши (ластик)
            if DP.write_new_value(pygame.mouse.get_pos(), 0):
                DP.draw_on_screen()    
                DP.draw_prediction() 
            
        if pygame.key.get_pressed()[pygame.K_ESCAPE]: 
            run = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False   

        pygame.display.update()
    pygame.display.quit()
    pygame.quit()

if __name__ == "__main__":    
    path = os.path.join(os.getcwd(), 'model/my_model.h5')
    path = 'C:/Users/Valter/Desktop/tests/Keras/Digits_rework/model/my_model.h5'
    if os.path.exists(path):
        interface(path)
    else:
        print("Check file existense or change path variable")