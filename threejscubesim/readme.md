Three.js project for making some floating cubes.
I originally planned to use this to represent a simple neural network as a visualizer. 
Nodes represented by cubes, brightness represented activation, weights represented by lines.
Came to realize a minst problem requires, 
28x28=784 cubes
2000*5 cubes for hidden and output layers.

Current setup drops to around 30 fps rendering alone with that many cubes.

Some points to revise:
rendering calculation may be incorrect since I am calculating 3*n sine functions per frame. May actually perform better with network. Since calculations could be done throughout the animation.
look into how to export / import dense network. (Network already made with ~96% acc. on mnist.
Minimize per-frame computations for more efficient rendering.