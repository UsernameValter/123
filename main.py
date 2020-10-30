import draw 
import pygame 
import os

import tensorflow as tf  

 
def interface(model):
    pygame.init()
    pygame.font.init()
    pygame.display.set_caption("drawing")
    clock = pygame.time.Clock()
    run = True 
         
    win = pygame.display.set_mode((1200, 840))

    DP = draw.Display(840, 840, win)  
    DP.draw_on_screen() 

    while(run): 
        clock.tick(80) 

        if pygame.mouse.get_pressed()[0]: # drawing with left click
            DP.draw_on_screen() 
            DP.new_value(pygame.mouse.get_pos(), 1)   
 
            prediction_drawed =  DP.return_value()

            prediction = model.predict(prediction_drawed)  
            DP.draw_prediction(prediction)   

        if pygame.mouse.get_pressed()[2]:   # erasing with right click
            DP.draw_on_screen() 
            DP.new_value(pygame.mouse.get_pos(), 0) 
 
            prediction_drawed =  DP.return_value()

            prediction = model.predict(prediction_drawed)  
            DP.draw_prediction(prediction) 
            
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
    model = tf.keras.models.load_model(path)
    model.summary()

    interface(model)