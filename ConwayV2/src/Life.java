

public class Life{
    public int x;
    public int y;
    public boolean grid[][];
    public boolean running = true;
    
    private final boolean tempGrid[][];
    private final boolean backupGrid[][];
    private int ticks = 0;
    
    public Life(int x, int y){
        this.x = x;
        this.y = y;
        grid = new boolean[x][y];
        tempGrid = new boolean[x][y];
        backupGrid = new boolean [x][y];
        randomGen(.75);
    }
    
    public void tick(){
        if(running == true){
            ticks++;
            for (int X = 0; X < grid.length; X++) {
                System.arraycopy(grid[X], 0, tempGrid[X], 0, grid[0].length);
            }
            for (int X = 0; X < grid.length; X++) {
                for (int Y = 0; Y < grid[0].length; Y++) {
                    int neighbors = checkNeighbors(X,Y);
                    if(neighbors < 2)
                        tempGrid[X][Y] = false;

                    if(neighbors == 3)
                        tempGrid[X][Y] = true;

                    if(neighbors > 3)
                        tempGrid[X][Y] = false;
                }
            }

            for (int X = 0; X < grid.length; X++) {
                System.arraycopy(tempGrid[X], 0, grid[X], 0, grid[0].length);
            }
            if(ticks%50 == 0 && ticks%3 == 0){
                boolean similarity = true;
                 for (int X = 0; X < grid.length; X++) {
                    for (int Y = 0; Y < grid[0].length; Y++) {
                        if(backupGrid[X][Y] != grid[X][Y])
                            similarity = false;
                    }
                }
                if (similarity == true){
                    restartGrid();
                }
                for (int X = 0; X < grid.length; X++) {
                    for (int Y = 0; Y < grid[0].length; Y++) {
                        backupGrid[X][Y] = grid[X][Y];         
                    }
                }
            }
        }
    }
    private int checkNeighbors(int X, int Y){
        int neighbor = 0;

        if(X>0 && X<grid.length-1 && Y>0 && Y< grid[0].length-1){

            if(grid[X-1][Y-1]== true)
                neighbor++;
            if(grid[X-1][Y]== true)
                neighbor++;
            if(grid[X-1][Y+1]== true)
                neighbor++;        
            if(grid[X][Y-1]== true)
                neighbor++;
            if(grid[X][Y+1]== true)
                neighbor++;
            if(grid[X+1][Y-1]== true)
                neighbor++;
            if(grid[X+1][Y]== true)
                neighbor++;
            if(grid[X+1][Y+1]== true)
                neighbor++;
            
            
        }else if(Y == 0 && X > 0 && X < grid.length-1){
            if(grid[X-1][grid[0].length-1]== true)
                neighbor++;
            if(grid[X-1][Y]== true)
                neighbor++;
            if(grid[X-1][Y+1]== true)
                neighbor++;
            if(grid[X][grid[0].length-1]== true)
                neighbor++;
            if(grid[X][Y+1]== true)
                neighbor++;
            if(grid[X+1][grid[0].length-1]== true)
                neighbor++;
            if(grid[X+1][Y]== true)
                neighbor++;
            if(grid[X+1][Y+1]== true)
                neighbor++;
        }else if(Y == grid[0].length-1 && X > 0 && X < grid.length-1){
            if(grid[X-1][Y-1]== true)
                neighbor++;
            if(grid[X-1][Y]== true)
                neighbor++;
            if(grid[X-1][0]== true)
                neighbor++;
            if(grid[X][Y-1]== true)
                neighbor++;
            if(grid[X][0]== true)
                neighbor++;
            if(grid[X+1][Y-1]== true)
                neighbor++;
            if(grid[X+1][Y]== true)
                neighbor++;
            if(grid[X+1][0]== true)
                neighbor++;
        }else if(X == 0 && Y > 0 && Y < grid[0].length-1){
            if(grid[grid.length-1][Y-1]== true)
                neighbor++;
            if(grid[grid.length-1][Y]== true)
                neighbor++;
            if(grid[grid.length-1][Y+1]== true)
                neighbor++;
            if(grid[X][Y-1]== true)
                neighbor++;
            if(grid[X][Y+1]== true)
                neighbor++;
            if(grid[X+1][Y-1]== true)
                neighbor++;
            if(grid[X+1][Y]== true)
                neighbor++;
            if(grid[X+1][Y+1]== true)
                neighbor++;
        }else if(X == grid.length-1 && Y > 0 && Y < grid[0].length-1){
            if(grid[X-1][Y-1]== true)
                neighbor++;
            if(grid[X-1][Y]== true)
                neighbor++;
            if(grid[X-1][Y+1]== true)
                neighbor++;
            if(grid[X][Y-1]== true)
                neighbor++;
            if(grid[X][Y+1]== true)
                neighbor++;
            if(grid[0][Y-1]== true)
                neighbor++;
            if(grid[0][Y]== true)
                neighbor++;
            if(grid[0][Y+1]== true)
                neighbor++;
        } else if(X==0 && Y==0){
            if(grid[grid.length-1][grid[0].length-1]== true)
                neighbor++;
            if(grid[grid.length-1][Y]== true)
                neighbor++;
            if(grid[grid.length-1][Y+1]== true)
                neighbor++;        
            if(grid[X][grid[0].length-1]== true)
                neighbor++;
            if(grid[X][Y+1]== true)
                neighbor++;
            if(grid[X+1][grid[0].length-1]== true)
                neighbor++;
            if(grid[X+1][Y]== true)
                neighbor++;
            if(grid[X+1][Y+1]== true)
                neighbor++;
        }else if(X == grid.length-1 && Y == 0){
            if(grid[X-1][grid[0].length-1]== true)
                neighbor++;
            if(grid[X-1][Y]== true)
                neighbor++;
            if(grid[X-1][Y+1]== true)
                neighbor++;        
            if(grid[X][grid[0].length-1]== true)
                neighbor++;
            if(grid[X][Y+1]== true)
                neighbor++;
            if(grid[0][grid[0].length-1]== true)
                neighbor++;
            if(grid[0][Y]== true)
                neighbor++;
            if(grid[0][Y+1]== true)
                neighbor++;
        }else if(X == 0 && Y == grid[0].length-1){
            if(grid[grid.length-1][Y-1]== true)
                neighbor++;
            if(grid[grid.length-1][Y]== true)
                neighbor++;
            if(grid[grid.length-1][0]== true)
                neighbor++;        
            if(grid[X][Y-1]== true)
                neighbor++;
            if(grid[X][0]== true)
                neighbor++;
            if(grid[X+1][Y-1]== true)
                neighbor++;
            if(grid[X+1][Y]== true)
                neighbor++;
            if(grid[X+1][0]== true)
                neighbor++;
        }else if(X == grid.length-1 && Y == grid[0].length-1){
            if(grid[X-1][Y-1]== true)
                neighbor++;
            if(grid[X-1][Y]== true)
                neighbor++;
            if(grid[X-1][0]== true)
                neighbor++;        
            if(grid[X][Y-1]== true)
                neighbor++;
            if(grid[X][0]== true)
                neighbor++;
            if(grid[0][Y-1]== true)
                neighbor++;
            if(grid[0][Y]== true)
                neighbor++;
            if(grid[0][0]== true)
                neighbor++;
        }
        
        return neighbor;
    }
    private void randomGen(double percent){
        for (boolean[] grid1 : grid) {
            for (int j = 0; j < grid[0].length; j++) {
                if (Math.random()<percent) {
                    grid1[j] = true;
                }
            }
        }
    }
    private void restartGrid(){
        for (int X = 0; X < grid.length; X++) {
            for (int Y = 0; Y < grid[0].length; Y++) {
                grid[X][Y] = false;
            }
        }
        randomGen(.75);
        tick();
        tick();
    }
}