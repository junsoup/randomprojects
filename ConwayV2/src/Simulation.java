import java.awt.Color;
import java.awt.Graphics;
import java.awt.event.KeyEvent;
import java.awt.image.BufferStrategy;
import java.lang.Thread;

public class Simulation implements Runnable{
    
    private Display display;
    public String title;
    public int width, height;
    private boolean running = false;
    private Thread thread;
    private final KeyManager keyManager = new KeyManager();
    private final MouseManager mouseManager = new MouseManager();
    
    private int xOffset, yOffset, tickCounter = 0;

    private Life life;
    
    public Simulation(String title, int width, int height, int xSize, int ySize){
        this.width = width;
        this.height = height;
        this.title = title;
        life = new Life(xSize,ySize);
    }
    private void init(){
        display = new Display(title, width, height);
        display.getCanvas().addKeyListener(keyManager);
        display.getCanvas().addMouseListener(mouseManager);
        display.getFrame().toFront();
        display.getFrame().setAlwaysOnTop(true);
        display.getFrame().requestFocus();
        
    }
    private void tick(){
//        if(tickCounter > 10){
            checkKeyPress();
//            tickCounter = 0;
//        }
        tickCounter++;
        life.tick();
    }
    private void render(){
        BufferStrategy bs = display.getCanvas().getBufferStrategy();
        if(bs == null){
            display.getCanvas().createBufferStrategy(3);
            return;
        }
        Graphics g = bs.getDrawGraphics();
        
        g.setColor(Color.BLACK);
        g.fillRect(0,0,width,height);
        
        g.setColor(Color.WHITE);
        
        for (int X = 0; X < life.grid.length; X++) {
            for (int Y = 0; Y < life.grid[0].length; Y++) {
                if (life.grid[X][Y]) {
                    if(xOffset > 0)
                        xOffset -= life.x;
                    if(yOffset > 0)
                        yOffset -= life.y;
                    g.fillRect((X-xOffset)*(height / life.x)%height,(Y-yOffset)*(width/ life.y)%width,(height / life.x),(width / life.y));
                }
            }
        }
        bs.show();
        g.dispose();
    }
    @Override
    public void run() {
        init();
        double fps;
        int frameCount = 0;
        long startTime = System.nanoTime();

        while(running){
//            try {
//                Thread.sleep(17);
//            } catch (InterruptedException e) {
//                throw new RuntimeException(e);
//            }
            tick();
            render();
            frameCount++;
            long now = System.nanoTime();
            // has it been more than 1 second (1bn nanos)?
            long wallclock = now - startTime;
            if(wallclock > 1000000000) {
                fps = frameCount / (wallclock/1000000000);
                startTime = now;
                frameCount = 0;
                System.out.println("FPS: " + fps);
            }
        }
        stop();
    }
    public synchronized void start(){
        if(running){
            return;
        }
        running = true;
        thread = new Thread(this);
        thread.start();
    }
    public synchronized void stop(){
        if(!running){
            return;
        }
        running = false;
        try{
            thread.join();
        } catch (InterruptedException e){
            System.out.println("Error while stopping!");
        }   
    }
    private void checkKeyPress() {
        if(keyManager.keys[KeyEvent.VK_UP]){
            yOffset--;
        } 
        if(keyManager.keys[KeyEvent.VK_RIGHT]){
            xOffset++;
        }
        if(keyManager.keys[KeyEvent.VK_DOWN]){
            yOffset++;
        }
        if(keyManager.keys[KeyEvent.VK_LEFT]){
            xOffset--;
        }
        if(keyManager.keys[KeyEvent.VK_SPACE]){
            if(life.running){
                life.running = false;
            }else{
                life.running = true;
            }
            keyManager.keys[KeyEvent.VK_SPACE] = false;
        }

        if(keyManager.keys[KeyEvent.VK_ENTER]){
           if(!life.running){
               life.running = true;
               life.tick();
               life.running = false;
           }else{
               life.tick();
           }
           keyManager.keys[KeyEvent.VK_ENTER] = false;
        }
        if(keyManager.keys[KeyEvent.VK_ESCAPE]){
            display.getFrame().dispose();
            System.exit(0);
        }

        if(mouseManager.clicked){

//            while(((mouseManager.lastClicked[0]/ zoomFactor/(width/life.x))+xOffset-(life.x/(zoomFactor+1))+life.x/2)+zoomOffset < 0){
//                xOffset = xOffset + life.x;
//            }
//            while(((mouseManager.lastClicked[0]/ zoomFactor/(width/life.x))+xOffset-(life.x/(zoomFactor+1))+life.x/2)+zoomOffset >= life.x){
//                xOffset = xOffset - life.x;
//            }
//            while(((mouseManager.lastClicked[1]/zoomFactor/(height/life.y))+yOffset-(life.y/(zoomFactor+1))+life.y/2)+zoomOffset < 0){
//                yOffset = yOffset + life.y;
//            }
//            while(((mouseManager.lastClicked[1]/zoomFactor/(height/life.y))+yOffset-(life.y/(zoomFactor+1))+life.y/2)+zoomOffset >= life.y){
//                yOffset = yOffset - life.y;
//            }
            int screenX = (mouseManager.lastClicked[0]-xOffset)%height/ life.x;
            int screenY = (mouseManager.lastClicked[1]-yOffset)%width/ life.y;
            
            if(life.grid[screenX][screenY]){
                life.grid[screenX][screenY] = false;
            }else{
                life.grid[screenX][screenY] = true;
            }
            mouseManager.clicked = false;
        }
    }
}
