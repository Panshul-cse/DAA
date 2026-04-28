class LL{
	int data;
	LL next;

	LL(int data){
		this.data=data;
		this.next=null;
	}
}

class Stackk{
	LL head;

	Stackk(){
		head=null;
	}

	boolean isEmpty(){
		return head==null;
	}

	void push(int val){
		LL temp=new LL(val);
		temp.next=head;
		head=temp;
	}

	int pop(){
		if(head==null){
			System.out.println("Stack is empty");
			return -1;
		}
		int val=head.data;
		head=head.next;
		return val;
	}

	int peek(){
		if(head==null){
			System.out.println("Stack is empty");
			return -1;
		}
		return head.data;
	}

	int size(){
		int c=0;
		LL temp=head;
		while(temp!=null){
			c++;
			temp=temp.next;
		}
		return c;
	}
}

public class Stackbyll{
	public static void main(String[] args){
		Stackk s=new Stackk();
		System.out.println(s.isEmpty());
		s.push(10);
		s.push(20);
		s.push(30);
		System.out.println("Size: "+s.size());
		System.out.println(s.peek());
		System.out.println(s.pop());
		System.out.println(s.peek());
	}
}