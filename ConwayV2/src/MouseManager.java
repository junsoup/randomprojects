

import java.awt.event.MouseEvent;
import java.awt.event.MouseListener;

public class MouseManager implements MouseListener{

    public int lastClicked[];
    public boolean clicked;
    
    public MouseManager(){
        lastClicked = new int[]{0,0};
    }
    
    @Override
    public void mousePressed(MouseEvent e) {
        lastClicked[0] = e.getX();
        lastClicked[1] = e.getY();
        clicked = true;
    }
    
    @Override
    public void mouseClicked(MouseEvent e) {
        
    }
    @Override
    public void mouseReleased(MouseEvent e) {

    }
    @Override
    public void mouseEntered(MouseEvent e) {
        
    }
    @Override
    public void mouseExited(MouseEvent e) {
        
    }
    
}
