ACCL
====
Phase 1: Simply use python nltk to find the similarity between words for highlighting. 

Phase 2: Use Wikipedia based, nltk assisted similarity look up mechanism for highlighting keywords.

Functionality: Accelerate read speed by converting input text to html page with keywords highlighted.

Why using it: This tool will help you to better skim through a long article/paper/essay using automatic keyword highlighting mechanisms.

How to use it:

  In Phase 2: First, currently with not perfect UI, clone this repository, have Python 2.7, 
              download nltk (www.nltk.org) and wikipedia (https://github.com/goldsmith/Wikipedia) module,
              Then substitute file_env to the keywords you know are key words a before reading. (1 line style)
              Then substitute file_in to the paragraph you want to highlight.
              Then in command line/ terminal, type: python acc_Learn_wiki.py
              Then you can open the output file file_out.html in browser.

Demo:

  Get the oxygen page on wikipedia and put its first 3 paragraphs in my file_in.txt.
  
  Then put word "oxygen" in my file_env,
  
  Then my keyword highlighting mechanism think the phrases ["Chemical element","ozone layer","Earth's crust","Ultraviolet radiation","Cellular respiration","oxygen","periodic table","Great oxygenation event","Billion years","Earth's atmosphere","Electrolysis of water","Atomic number","Fractional distillation","Life on Earth","Earth","Life Support System","Billion years ago","Low earth orbit"]
  
  Then render html with those words highlighted red!
  
Current Constraints and further TODOs:
1.Constraint 1:Currently only accept English. For example: greek will break it.
2.Constraint 2 && TODO1 :Bad UI, not that easy to use.
3.TODO2: Change input format from txt to more common formats such as pdf.
  
  

