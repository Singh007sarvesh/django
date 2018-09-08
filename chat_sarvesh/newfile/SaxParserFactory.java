import java.util.ArrayList;
import java.util.List;
import javax.xml.parsers.SAXParser;
import javax.xml.parsers.SAXParserFactory;
import org.xml.sax.Attributes;
import org.xml.sax.SAXException;
import org.xml.sax.helpers.DefaultHandler;
import java.io.File;
 
public class SaxParserFactory 
{
  SaxHandler handler = new SaxHandler(); 
  public List<Employee> readSaxParserFactory(File file)
  {
    try
    {
      SAXParserFactory parserFactor = SAXParserFactory.newInstance();
      SAXParser parser = parserFactor.newSAXParser();
      parser.parse(file,handler);
      return handler.empList;
    }
    catch(Exception e)
    {
      System.out.println(e);
    }
    return handler.empList;
  }
}

 
