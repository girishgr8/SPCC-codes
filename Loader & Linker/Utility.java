import java.util.*;
import java.io.*; 

class Utility { 
	// declaring native method for division 
	private native void divide();

	public static void main(String[] args) { 
	Scanner sc = new Scanner(System.in); 
	System.out.println("\n\t****Called Multiply Module from JAVA language****\n");
	System.out.println("Enter the numbers to be multiplied: ");
	int a = sc.nextInt(); 
	int b = sc.nextInt(); 
	int answer = a*b;
	System.out.println("Multiplication of "+a+" and "+b+" is: "+answer);
	// invoking native method of C 
	new Utility().divide(); 
	} 
	static { 
		//loading library which contains implementation of division 
		System.loadLibrary("Divide"); 
	} 
}