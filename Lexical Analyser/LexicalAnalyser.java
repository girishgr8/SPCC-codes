import java.util.*;
import java.io.*;

interface Global{
    String keywords[] = new String[]{"include","int","float","char","double","bool","void","extern","unsigned","goto","static","class","struct","for","if","else","return","register","long","while"};
    String predeffuncs[] = new String[]{"main","scanf","printf","puts","gets","getchar","putchar"};
    String headers[] = new String[]{"stdio.h","conio.h","iostream.h"};
    String operators[] = new String[]{"+","-","*","/","%","^","=","<",">","&","|","!"};
    String spcsym[] = new String[]{"(",")","{","}","[","]",",",";","#"};
}

public class LexicalAnalyser implements Global{
	static Vector<String> variables = new Vector();
	static Vector<String> literals = new Vector();
	static Vector<String> userdeffuncs = new Vector();
	static Vector<String> errors = new Vector();

    public static void main(String[] args) throws Exception {
        Scanner sc = new Scanner(System.in);
        File file = new File("lexical_input.cpp"); 
	  	BufferedReader br = new BufferedReader(new FileReader(file));
	  	String line;
	  	int l = 0;
	  	while ((line = br.readLine()) != null){
	  		l++;
	  		System.out.println("\n"+line);
	  		String lexems[] = line.split(" ");
	  		// System.out.println(Arrays.toString(lexems));
	  		for(String s: lexems){
	  			String tillNow = "";
	  			for(int i=0;i<s.length();i++){
	  				tillNow+=s.charAt(i);
	  				// System.out.println("tillNow is: "+tillNow);
	  				if(!Character.isDigit(s.charAt(i)) && !Character.isLetter(s.charAt(i))){
	  					// System.out.println("tillNow from if is: "+tillNow);
	  					if(check(spcsym, tillNow)!=-1){
	  						System.out.printf("special symbol #"+check(spcsym, tillNow)+"\t");
	  						tillNow="";
	  					}
	  					else if(tillNow.contains("=") && !String.valueOf(s.charAt(i+1)).equals("=")){
	  						int index = tillNow.indexOf("=");
  							String v = tillNow.substring(0,index);
  							// System.out.println("v = "+v);
  							if(!variables.contains(v)){
  								if(!Character.isDigit(v.charAt(0))){
  									variables.add(v);	
  									System.out.printf("variable #"+variables.indexOf(v)+"\t");
  								}
  								else
  									errors.add("Error on line: "+l+" at "+v);
  							}
  							else
  								System.out.printf("variable #"+variables.indexOf(v)+"\t");

  							tillNow = tillNow.substring(index,tillNow.length());
  							System.out.printf("operator #"+check(operators, "=")+"\t");
							tillNow = "";
							int cm = s.indexOf(',',i);
							int sm = s.indexOf(';',i);
							// System.out.println("i is "+i+" and cm is "+cm);
							// System.out.println("i is "+i+" and sm is "+sm);
							if(cm!=-1){
								String str = s.substring(i+1,cm);
								// System.out.println("str = "+str);
								if(variables.contains(str))
									System.out.printf("variable #"+variables.indexOf(str)+"\t");
								
								else if(literals.contains(str))
									System.out.printf("literal #"+literals.indexOf(str)+"\t");
								else if(!literals.contains(str)){
									literals.add(str);
									System.out.printf("literal #"+literals.indexOf(str)+"\t");
								}
								i = cm;
								System.out.printf("special symbol #"+check(spcsym, ",")+"\t");
							}
	  						else if(sm!=-1){
								String str = s.substring(i+1,sm);
								if(variables.contains(str))
									System.out.printf("variable #"+variables.indexOf(str)+"\t");

								else if(literals.contains(str))
									System.out.printf("literal #"+literals.indexOf(str)+"\t");
								else{
									literals.add(str);
									System.out.printf("literal #"+literals.indexOf(str)+"\t");
								}
								i = sm;
								System.out.printf("special symbol #"+check(spcsym, ";")+"\t");
	  						}
  						}

  						else if(tillNow.contains(">") || tillNow.contains("<") || tillNow.contains("&") || tillNow.contains("|")){
  							int index = Math.max(tillNow.indexOf("|"),Math.max(tillNow.indexOf("&"),Math.max(tillNow.indexOf("<"),tillNow.indexOf(">"))));
  							String v = tillNow.substring(0,index);
  							if(variables.contains(v))
  								System.out.printf("variable #"+variables.indexOf(v)+"\t");
  							
  							String tl = String.valueOf(tillNow.charAt(tillNow.length()-1));

  							System.out.printf("special symbol #"+check(operators, tl)+"\t");

  							tl = s.substring(s.indexOf(tl),s.indexOf(")"));
  							if(variables.contains(tl))
  								System.out.printf("variable #"+variables.indexOf(tl)+"\t");
  							else if(literals.contains(tl))
  								System.out.printf("literal #"+literals.indexOf(v)+"\t");
  							tillNow = "";
  							i = s.indexOf(")")-1;
  						}

  						else if(check(operators, tillNow)!=-1){
	  						System.out.printf("operator #"+check(operators, tillNow)+"\t");
	  						tillNow="";
  						}
	  				}
  					else{
	  					// System.out.println("tillNow else is: "+tillNow);
	  					if(check(keywords,tillNow)!=-1){
	  						System.out.printf("keyword #"+check(keywords, tillNow)+"\t");
	  						tillNow="";
	  					}
	  					else if(check(spcsym, tillNow)!=-1){
	  						System.out.printf("special symbol #"+check(spcsym, tillNow)+"\t");
	  						tillNow="";
	  					}
	  					else if(check(predeffuncs,tillNow)!=-1){
	  						System.out.printf("predeffunc #"+check(predeffuncs, tillNow)+"\t");
	  						tillNow="";
	  					}
	  					else if(check(headers,tillNow)!=-1){
	  						System.out.printf("header #"+check(headers, tillNow)+"\t");
	  						tillNow="";
	  					}
	  					else if(check(operators,tillNow)!=-1){
	  						System.out.printf("operator #"+check(operators, tillNow)+"\t");
	  						tillNow="";
	  					}
	  				}
	  			}		
	  		}
  			System.out.println();
	  	}
	  	System.out.println();
	  	printTables(keywords,"Keywords ");
		printTables(predeffuncs,"Pre-defined functions");
		printTables(operators, "Operators");
		printTables(spcsym, "Special Symbols");
		printDynamicTables(variables,"User-defined variables");
		printDynamicTables(literals,"Literals");
		printDynamicTables(userdeffuncs,"User-defined Functions");
		printDynamicTables(errors,"Errors");
    }

    public static int check(String arr[], String item){
    	return Arrays.asList(arr).indexOf(item);
    }

    public static void printTables(String arr[], String name){
    	System.out.println(name+"\n");
    	for(int i=0;i<arr.length;i++)
	  		System.out.println(i+")  "+arr[i]);
	  	System.out.println();
    }
    public static void printDynamicTables(Vector<String> v, String name){
    	System.out.println(name+"\n");
		for(int i=0;i<v.size();i++)
			System.out.println(i+")  "+v.get(i));
		System.out.println();
    }
}
