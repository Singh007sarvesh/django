import java.util.regex.Matcher;
import java.util.regex.Pattern;

class EmailValidate
{
	public static boolean isEmailValid(String email) throws Exception
  	{
    	String emailRegex = "^[a-zA-Z0-9_+&*-]+(?:\\."+"[a-zA-Z0-9_+&*-]+)*@" +"(?:[a-zA-Z0-9-]+\\.)+[a-z" +"A-Z]{2,7}$";                     
    	Pattern pat = Pattern.compile(emailRegex);
    	if (email == null)
        	return false;
        return pat.matcher(email).matches();
  	}    
}