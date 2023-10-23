

import java.awt.event.KeyEvent;
import java.awt.event.KeyListener;


public class KeyManager implements KeyListener{
    
    public boolean[] keys;
    
    public KeyManager(){
        keys = new boolean[256];
    }
    
    @Override
    public void keyPressed(KeyEvent e) {  
        keys[e.getKeyCode()] = true;
    }
    
    @Override
    public void keyReleased(KeyEvent e) {
        if(!(e.getKeyCode() == 32 ||
            e.getKeyCode() == 91 ||
            e.getKeyCode() == 93 ||
            e.getKeyCode() == 45 ||
            e.getKeyCode() == 61 ||
            e.getKeyCode() == 10)){
            keys[e.getKeyCode()] = false;
        }        
    }
    
    @Override
    public void keyTyped(KeyEvent e) {  
    }
}
