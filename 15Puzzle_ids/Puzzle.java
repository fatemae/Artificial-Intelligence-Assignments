import java.util.Arrays;
import java.util.LinkedList;
import java.util.List;

/** Puzzle class defines a node in the tree */
public class Puzzle{
    public static final int size=4;
    int[][] state;
    Puzzle parent;
    int depth;
    char path;
    List<Puzzle> children=new LinkedList<>();

    public Puzzle(int[][] state,Puzzle parent,int depth,char path){
        this.state=state;
        this.parent=parent;
        this.depth=depth;
        this.path=path;
    }
    
    @Override
    public boolean equals(Object obj) {
        // TODO Auto-generated method stub
        Puzzle p=(Puzzle)obj;
        if (this.state == null) {
            return (p.state == null);
        }
        if (p.state == null) {  
            return false;
        }
        if (this.state.length != p.state.length) {
            return false;
        }
        for (int i = 0; i < this.state.length; i++) {
            if (!Arrays.equals(this.state[i], p.state[i])) {
                return false;
            }     
        }
             
        return true;
    }
}
