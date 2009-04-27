import java.io.*;
import java.net.*;

public class gqservExample{

    // Use the functions readns and writens in your own programs

    public static void writens(Socket sock,String command){
	//given a socket and a command, write the command to
	//the socket in netstring format
	try{
	    PrintWriter to_server = new PrintWriter(sock.getOutputStream());
	    //send command to the server in netstring format
	    //dont forget to flush
	    to_server.print(command.length()+":"+command+",");
	    to_server.flush();
	}

	catch(Exception e){
	    System.err.println(e);
	}
    }

    public static String readns(Socket sock) throws IOException{
	
	//read and and decode a netstring from a socket
	String ret = "";
	try{    
	    InputStream from_server = sock.getInputStream();
	    OutputStream to_file = System.out;

	    //read the message size returned by the server
	    int bytes_read;
	    String size = "";
	    byte[] b = new byte[1];
	    String tmp = "";
	    while(!tmp.equals(":")){
		bytes_read = from_server.read(b);
		tmp=new String(b);
		if(!tmp.equals(":"))
		    size = size + new String(b);
		else if(bytes_read==0)
		    throw new IOException("Missing : seperator");
	    }	    
	    int sz = Integer.parseInt(size);
	    

	    byte[] b2 = new byte[sz];
	    while(sz!=0){
		bytes_read=from_server.read(b2,0,sz);
		if(bytes_read==0)
		    throw new IOException("Short netstring read");
		sz-=bytes_read;
	    }
	    bytes_read=from_server.read(b);
	    tmp = new String(b,0,1);
	    if(!tmp.equals(","))
		throw new IOException("Missing netstring terminator");
	    if(bytes_read==0)
		throw new IOException("Short netstring read");

	    ret = ret + new String(b2);
	    
	}

	catch(Exception e){
	    System.err.println(e);
	}	
	return ret;
    }
    
    public static void main(String args[]){
	try{
	    String host = "smi.ucd.ie";
	    int port = 8081;
	    String command1,command2;
	    String response;

	    //open a connection to the socket
	    Socket sock = new Socket(host,port);
	    
	    command1 = "add_query hello java world";
	    command2 = "queue_contents";

	    //send some commands and ger the results
	    writens(sock,command1);
	    response = readns(sock);
	    System.out.println(response);
	    writens(sock,command2);
	    response = readns(sock);
	    System.out.println(response);

	    //send BYE message when finished
	    writens(sock,"BYE");
	  
	    //close the connection
	    sock.close();

	}
	catch(Exception e){
	    System.err.println(e);
	}
    }
}
