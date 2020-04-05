import java.util.*;

public class RDP{

    static TreeMap<Character,List<String>> grammar = new TreeMap(Collections.reverseOrder());
    static Vector<String> rules = new Vector();
    static String inputString = "";
    static Scanner s = new Scanner(System.in);
    static int iptr = 0, rulesCount = 0;
    static int valCheck = 0, flag = 0;

    public static boolean parser(Character nt, List<String> exps){
    	try{
	    	// If input ptr has reached end of string.... means the string is parsed....
	    	// Hence return true 
	        if(iptr == inputString.length())
	            return true;

	        for(String ele: exps){
	            int tempptr = iptr;
	            int flag = 0;
	            for(int i=0; i<ele.length(); i++){
	                if(ele.charAt(i) == inputString.charAt(iptr)){
	                	rules.add(0,Character.toString(nt) + " -> " + ele);
	                    System.out.println("Matched characters: "+ele.charAt(i)+" : "+inputString.charAt(iptr));
	                    iptr++;
	                }
	                else{
	                    if(grammar.containsKey(ele.charAt(i))){
	                        exps = grammar.get(ele.charAt(i));
	                        if(!parser(ele.charAt(i), exps))
	                            flag = 1;
	                       	else
	                       		continue;
	                    }
	                    else {
	                        iptr = tempptr;
	                        flag = 1;
	                    }
	                }
	                if(flag == 1)
	                    break;
	            }
	            if(iptr == inputString.length() || flag == 0){
	                valCheck = iptr;
	                return true;
	            }  
	        }
	        return false;
    	}catch (Exception e) {
    		System.out.println("--------- The input string cannot be parsed -----------");
    		System.exit(0);
    	}
    	return false;
    }

    public static void initialiseData(){
        // Store the grammar rules
        List<String> ll1 = new ArrayList<>();
        ll1.add("Aa");
        grammar.put('S',ll1);

        List<String> ll2= new ArrayList<>();
        ll2.add("bB");
        ll2.add("c");
        grammar.put('A',ll2);
        
        List<String> ll3 = new ArrayList<>();
        ll3.add("a");
        ll3.add("b");
        grammar.put('B',ll3);

        System.out.println("---- The given grammar is : ----");
        for(Map.Entry<Character,List<String>> entry: grammar.entrySet()){
        	System.out.printf(entry.getKey()+" -> ");
        	List<String> list = entry.getValue();
        	for(int i=0; i<list.size(); i++){
        		if(i!=list.size()-1)
        			System.out.printf(list.get(i)+" | ");
        		else
        			System.out.printf(list.get(i));
        	}
        	System.out.println();
        }

        // Input the string to be parsed ...
        System.out.printf("Enter the input string to be parsed : ");
        inputString = s.next();
        
        for(Map.Entry<Character,List<String>> entry: grammar.entrySet()){
            iptr = 0;
            boolean val = parser(entry.getKey(), entry.getValue());
            if(val == true && iptr == inputString.length()){
                System.out.println("----------------------------------------------");
                System.out.println("The input string '"+inputString+"' is successfully parsed.");
                System.out.println("Rules used in parsing were: ");
                int i=1;
                for(String r : rules)
                	System.out.println((i++)+". "+r);
                flag = 1;
                break;
            }
        }
        if(flag == 0){
        	System.out.println("----------------------------------------------");
        	System.out.println("The input string '"+inputString+"' cannot be parsed.");
        }
    }

    public static void main(String args[]){
        initialiseData();
    }
}