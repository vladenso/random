import java.util.*;

public class test {
	public static void main(String[] args) {
		System.out.println(time(1, 8, 3, 2, 6, 4));
	}
	
	public static String time(int A, int B, int C, int D, int E, int F) {
    // write your code in Java SE 8
	// Given 6 integers, find the largest legal time.
	// return in format hh:mm:ss
	// if not possible, return "NOT POSSIBLE"
        PriorityQueue<Integer> queue = new PriorityQueue<Integer>(6, Collections.reverseOrder());
        queue.add(A);
        queue.add(B);
        queue.add(C);
        queue.add(D);
        queue.add(E);
        queue.add(F);
        
        F = queue.poll();
        if (F > 9) {
            return "NOT POSSIBLE";
        }
        
        E = queue.poll();
        ArrayList<Integer> arr = new ArrayList<Integer>();
        while (E > 5) {
            arr.add(E);
            if (queue.size() == 0) {
                return "NOT POSSIBLE";
            }
            E = queue.poll();
        }
        for (int i: arr) {
            queue.add(i);
        }
        String s = String.valueOf(E) + String.valueOf(F);
        System.out.println(s);
        
        D = queue.poll();
        C = queue.poll();
        arr = new ArrayList<Integer>();
        while (C > 5) {
            arr.add(C);
            if (queue.size() == 0) {
                return "NOT POSSIBLE";
            }
            C = queue.poll();
        }
        for (int i: arr) {
            queue.add(i);
        }
        String m = String.valueOf(A) + String.valueOf(B);
        System.out.println(m);

        B = queue.poll();
        A = queue.poll();
        String h = String.valueOf(A) + String.valueOf(B);
        if (Integer.valueOf(h) > 24) {
            return "NOT POSSIBLE";
        }
        return h + ':' + m + ':' + s;
	}

}
