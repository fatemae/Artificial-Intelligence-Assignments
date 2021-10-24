import java.util.LinkedList;
import java.util.List;
import java.util.Queue;
import java.util.Scanner;
import java.util.stream.Collectors;

public class Puzzle15 {
    /** Queues to store frontier and its corresponding moves(moveList) */
    Queue<int[][]> frontier = new LinkedList<>();
    Queue<String> moveList = new LinkedList<>();
    
    /**Queue for storing the already traversed state of puzzle */
    Queue<int[][]> reached = new LinkedList<>();

    /** Goal state of the puzzle */
    int[][] solvedPuzzle = {{1,2,3,4},{5,6,7,8},{9,10,11,12},{13,14,15,0}};

    /** Possible moves at a particular state */
    char[] move = {'L','R','U','D'};
    
    /**variable to store the Time and Memory, before and after the BFS */
    static long startTime,stopTime,memoryBefore,memoryAfter;


    int x,y;
    String m = "";
    static int[][] puzzle;

    public static void main(String[] args) throws Exception {
        Puzzle15 p =new Puzzle15();
        puzzle = new int[4][4];
        
        //Input the current state of puzzle; 
        Scanner sc= new Scanner(System.in);
        for(int i=0;i<4;i++){
            for(int j=0;j<4;j++){
                puzzle[i][j] = sc.nextInt();
            }
        }
        
        //getting the memory and time before bfs
        memoryBefore = Runtime.getRuntime().totalMemory()-Runtime.getRuntime().freeMemory();
        startTime = System.nanoTime();

        //calling breadth first search 
        puzzle=p.bfs(puzzle);

        //getting the memory and time after bfs
        stopTime = System.nanoTime();
        memoryAfter = Runtime.getRuntime().totalMemory()-Runtime.getRuntime().freeMemory();

        /** Null check of the state recieved from bfs, because if it is null 
        it means that there was no possible way to reach the goal
        */
        if(puzzle!=null){
            p.print();
        }else
            System.out.println("The Goal cannot be reached from this state");
        sc.close();
    }

    public void print(){
        System.out.println("Moves : "+m);
        System.out.println("No of Nodes expanded : "+reached.size());
        System.out.println("Time Taken : "+(stopTime-startTime)/1000000.0+" ms");
        System.out.println("Memory Used : "+(memoryAfter-memoryBefore)/1024+" kb");
    }

    /** finding the co-ordinates for 0 block */
    public void findEmptyBlock(int[][] puzzle){
        for(int i=0;i<4;i++){
            for(int j=0;j<4;j++){
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
        int[][] newObj=new int[4][4];
        for(int i=0;i<4;i++){
            for(int j=0;j<4;j++){
                newObj[i][j]=oldObj[i][j];
            }
        }
        return newObj;
    }

    /** BFS implementation */
    public int[][] bfs(int[][] puzzle) {
        String m1="";
        int[][] node = new int[4][4];
        node=createNewObject(puzzle);
        
        /** Finding if the puzzle is already in its goal */
        if(!isGoal(node)){
            frontier.add(node);
            moveList.add(m);
            reached.add(puzzle);

            while(!frontier.isEmpty()){
                node=frontier.poll();
                m1=moveList.poll();

                for(int i=0;i<move.length;i++){
                    int[][] c= new int[4][4];
                    m=new String(m1);
                    c=createNewObject(node);    
                    findEmptyBlock(node);

                    /** for each move operation, check if possible, 
                     * if it is possible, change co-ordinate of 0 to get child node
                     * add move in m string
                     * check if the child is the goal state, if true returns child
                     * if child state has not previously reached, push it in reached,frontier and m in moveList
                     */
                    switch(move[i]){
                        case 'L': 
                            if(y!=0){
                                c[x][y]=c[x][y-1];
                                c[x][y-1]=0;
                                m+='L';
                                if(goalCheckAndPushOperations(c))
                                    return c;
                            }
                            break;
                        case 'R': 
                            if(y!=3){
                                c[x][y]=c[x][y+1];
                                c[x][y+1]=0;
                                m+='R';
                                if(goalCheckAndPushOperations(c))
                                    return c;
                            }
                            break;
                        case 'U': 
                            if(x!=0){
                                c[x][y]=c[x-1][y];
                                c[x-1][y]=0;
                                m+='U';
                                if(goalCheckAndPushOperations(c))
                                    return c;
                            }
                            break;
                        case 'D': 
                            if(x!=3){
                                c[x][y]=c[x+1][y];
                                c[x+1][y]=0;
                                m+='D';
                                if(goalCheckAndPushOperations(c))
                                    return c;
                            }
                            break;
                                                           
                    }
                    
                }
            }
            
        }else
            return puzzle;/** return the original puzzle if it is in the goal state */
            
        return null;/** returns null when the goal state cannot be achieved after exploring all possible nodes */

    }

    /** If the child node is the goal node, it returns true else false.
     * Checks for child node in reached and does push operations accordingly*/
    boolean goalCheckAndPushOperations(int[][] c){
        if(!isInReached(c)){
            reached.add(c);
            frontier.add(c);
            moveList.add(m);
        }
        if(isGoal(c)){
            return true;
        }
        return false;
    }

    /** Function to check if the state of puzzle matches the Goal state */
    public boolean isGoal(int[][] puzzle){
        for(int i=0;i<4;i++){
            for(int j=0;j<4;j++){
                if(puzzle[i][j]!=solvedPuzzle[i][j])
                    return false;
            }
        }
        return true;
    }

    /** Function to check whether puzzle is in the reached list, 
     * which also denotes that the puzzle state has already been reached */
    public boolean isInReached(int[][] puzzle){
        List<int[][]> collector = reached.stream().filter(o-> o[0][0]==puzzle[0][0]&&o[1][0]==puzzle[1][0]&&o[2][0]==puzzle[2][0]&&
            o[3][0]==puzzle[3][0]&&o[0][1]==puzzle[0][1]&&o[1][1]==puzzle[1][1]&&o[2][1]==puzzle[2][1]&&
            o[3][1]==puzzle[3][1]&&o[0][2]==puzzle[0][2]&&o[1][2]==puzzle[1][2]&&o[2][2]==puzzle[2][2]&&
            o[3][2]==puzzle[3][2]&&o[0][3]==puzzle[0][3]&&o[1][3]==puzzle[1][3]&&o[2][3]==puzzle[2][3]&&
            o[3][3]==puzzle[3][3]).collect(Collectors.toList());
        if(collector.size()==0){
            return false;
        }else{
            return true;
        }
    }
}
