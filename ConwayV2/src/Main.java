import java.util.Scanner;

public class Main {
    public static void main(String[] args) {
        Scanner in = new Scanner(System.in);

        double defaultWindowSize = 600;
        System.out.println("");
        System.out.println("How large would you like the simulation? (preferably between 10 ~ 600. 200 is good for demonstration)");

        int x = in.nextInt();

        if(x%10==0){
            if(x>defaultWindowSize){
                defaultWindowSize = x;
            }
        }else{
            while(!((defaultWindowSize/x)%1==0)){
                defaultWindowSize++;
            }
            System.out.println(x);
            System.out.println(defaultWindowSize);
        }

        Simulation simulation = new Simulation("Conway's Game of Life by Junsu Lee", (int)defaultWindowSize, (int)defaultWindowSize, x, x); //optimal startup is 600x600
        simulation.start();
    }
}