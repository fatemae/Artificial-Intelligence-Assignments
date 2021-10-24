import java.util.Scanner;
import java.util.Stack;


public class DFSPuzzle {
    static int s=4;
    int nodesExpanded=0;
    Puzzle solution;

    /** Goal state of the puzzle */
    int[][] solvedPuzzle = {{1,2,3,4},{5,6,7,8},{9,10,11,12},{13,14,15,0}};
    // int[][] solvedPuzzle = {{1,2},{3,0}};

    /** Possible moves at a particular state */
    char[] move = {'L','R','U','D'};
    
    /**variable to store the Time and Memory, before and after the BFS */
    static long startTime,stopTime,memoryBefore,memoryAfter;


    int x,y;
    static int[][] puzzle;

    public static void main(String[] args) throws Exception {
        DFSPuzzle p =new DFSPuzzle();
        
        puzzle = new int[s][s];
        
        //Input the current state of puzzle; 
        Scanner sc= new Scanner(System.in);
        for(int i=0;i<s;i++){
            for(int j=0;j<s;j++){
                puzzle[i][j] = sc.nextInt();
            }
        }
        sc.close();
        Puzzle root=new Puzzle(puzzle, null, 0, '\0');
        //getting the memory and time before bfs
        memoryBefore = Runtime.getRuntime().totalMemory()-Runtime.getRuntime().freeMemory();
        startTime = System.nanoTime();

        //calling iterative deepening depth first search 
        p.ids(root);

        //getting the memory and time after bfs
        stopTime = System.nanoTime();
        memoryAfter = Runtime.getRuntime().totalMemory()-Runtime.getRuntime().freeMemory();

        p.print();
        
    }

    public void print(){
        System.out.println("Moves : "+tracePath(solution));
        System.out.println("No of Nodes expanded : "+nodesExpanded);
        System.out.println("Time Taken : "+(stopTime-startTime)/1000000.0+" ms");
        System.out.println("Memory Used : "+(memoryAfter-memoryBefore)/1024+" kb");
    }

    /** finding the co-ordinates for 0 block */
    public void findEmptyBlock(int[][] puzzle){
        for(int i=0;i<s;i++){
            for(int j=0;j<s;j++){
                if(puzzle[i][j]==0){
                    x=i;
                    y=j;
                    return;
                }
            }
        }
    }

    /** Creating a copy of an object/state */
    public int[][] createNewObject(int[][] oldObj){
        int[][] newObj=new int[s][s];
        for(int i=0;i<s;i++){
            for(int j=0;j<s;j++){
                newObj[i][j]=oldObj[i][j];
            }
        }
        return newObj;
    }


    /** implementation of iterative deepening */
    public void ids(Puzzle root) {
        boolean goal = false;
        for(int depth=0; !goal; depth++) {
            goal = dfs(root,depth);
        }
    }
    
    /**implementation of depth first search */
    public boolean dfs(Puzzle root, int limit) {
        nodesExpanded=0;
        Stack<Puzzle> frontier = new Stack<>();
        frontier.add(root); 
        boolean goal = false;
        while(!frontier.isEmpty() && !goal) {
            Puzzle temp = frontier.pop();
            // expended.add(temp);
            if(!isGoal(temp.state)) {
                if(temp.depth>=limit){
                    goal=false;
                }else if(!check_cycle(temp)){
                    nodesExpanded++;
                    for(int i=0;i<move.length;i++){
                        int[][] c= new int[s][s];
                        c=createNewObject(temp.state);    
                        findEmptyBlock(c);
                        switch(move[i]){
                            case 'L': 
                                if(y!=0){
                                    c[x][y]=c[x][y-1];
                                    c[x][y-1]=0;
                                    frontier.add(new Puzzle(c,temp,temp.depth+1,'L'));
                                }
                                break;
                            case 'R': 
                                if(y!=s-1){
                                    c[x][y]=c[x][y+1];
                                    c[x][y+1]=0;
                                    frontier.add(new Puzzle(c,temp,temp.depth+1,'R'));
                                }
                                break;
                            case 'U': 
                                if(x!=0){
                                    c[x][y]=c[x-1][y];
                                    c[x-1][y]=0;
                                    frontier.add(new Puzzle(c,temp,temp.depth+1,'U'));
                                }
                                break;
                            case 'D': 
                                if(x!=s-1){
                                    c[x][y]=c[x+1][y];
                                    c[x+1][y]=0;
                                    frontier.add(new Puzzle(c,temp,temp.depth+1,'D'));
                                }
                                break;                                      
                        }
                    }
                }
            } else {
                solution=temp;
                return true;
            }
        }
        return goal;
    }

    /** Method to find path */
    public String tracePath(Puzzle node){
        StringBuilder sBuilder = new StringBuilder();
        while(node!=null){
            sBuilder.append(node.path);
            node = node.parent;
        }

        return sBuilder.reverse().toString();
    }

    /** Method to check cycles */
    private boolean check_cycle(Puzzle temp) {
        Puzzle parent=temp.parent;
        while(parent!=null){
            if(parent.equals(temp))
                return true;
            parent=parent.parent;
        }
        return false;
    }

    // /** Function to check if the state of puzzle matches the Goal state */
    public boolean isGoal(int[][] puzzle){
        for(int i=0;i<s;i++){
            for(int j=0;j<s;j++){
                if(puzzle[i][j]!=solvedPuzzle[i][j])
                    return false;
            }
        }
        return true;
    }

}
