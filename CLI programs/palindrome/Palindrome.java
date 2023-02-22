import java.util.Scanner;
import java.util.Stack;

/**
 * @author Carl 
 * @version 1.0
 * Assignment 2.2
 */ 
public final class Palindrome
{
	private Stack<String> stack;
	private String original;
	
	/**
	 * Allocates both the Stack and String
	 */
	public Palindrome()
	{
		stack = new Stack<>();
		original = "";
	}//end empty-argument
	
	/**
	 * @param original, the String to be determined if it is a palindrome
	 */ 
	public Palindrome(String original)
	{
		this();
		scan(original);
	}//end constructor
	
	/**
	 * @param orginal, the String to scan
	 * the Scanner object ignores punctuation and spaces and the tokens returned are concatenated to a single String.
	 * Note: Scanner object is glitchy.
	 * Assertion: Scanner object delimit input String without any glitch. 
	 */
	private void scan(String word)
	{
		Scanner scan = new Scanner(word);
		scan.useDelimiter("\\W+");
		while (scan.hasNext())
			original += scan.next();
		scan.close();
	}//end Scan

	/**
	 * @return true if the String original is a palindrome
	 */ 
	private boolean solve()
	{
	    if (original.length() == 1)
	        return true;
	    if (original == "")
	    	return false;
		
		String substring;
		int end = original.length()-1;
		int start;
		int mid = original.length()/2;
		int character = 0;
		boolean result;
		
		if (original.length() % 2 == 0)
			start = mid;
		else
			start = mid+1;//need to start +1 of mid, since that character in exactly in the middle of the String and the substrings to the right and to the left are of the same length
		
		for (int i = start; i < end+1; i++)
		{
			substring = original.substring(start, start+1);
			stack.push(substring);
			start++;
		}
		do
		{
			substring = original.substring(character, character+1);
			result = stack.pop().equalsIgnoreCase(substring);
			character++;
		} 
		while (result && character < mid);
		return result;
	}//end solve
	
	/**
	 * @param word the String to check
	 * @return true if this word or sentence is a palindrome, this String can contain punctuation(s) and space(s)
	 */
	public boolean isPalindrome(String word)
	{
		original = "";
		scan(word);
		return solve();
	}//end isPalindrom(String)
		
	/**
	 * @return true if the String original is a palindrome
	 */ 
	public boolean isPalindrome()
	{
	    return solve();
	}//end isPalindrome
	
	/**
	 * main method where this program is executed, this program accept a palindrome from the user, check it using a stack, and return whether the String is a palindrome or not.
	 * Note: Scanner object is glitchy.
	 * Assertion: Scanner object delimit input String without any glitch.
	 * @param args
	 */
	public static void main(String[] args) 
	{
		Scanner user = new Scanner(System.in);
		Palindrome palindrome = new Palindrome();
		System.out.println("Would you like to solve a palindrome? (yes or no)");
		String sentinel = user.next();
		
		while (sentinel.equalsIgnoreCase("yes"))
		{
			System.out.println("Please type out the word or sentence in question:");
			sentinel = user.next();
			
			if (palindrome.isPalindrome(sentinel))
				System.out.println(sentinel+" is a palindrome.");
			else
				System.out.println(sentinel+" is not a palindrome.");
			
			System.out.println("Would you like to solve another palindrome?");
			sentinel = user.next();
		}
		user.close();
		System.out.println("Thanks for your input.");
	}//end main
}//end class