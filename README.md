# vocabulary_expander
Vocabulary Expander is a program useful in case if you want to learn a lot of foreign words in a short time.

How to use it:
1) download this directory
2) Create your own dictionary in the directory of program under the name 'dict.txt'.
   Write there, strictly adhering to the template of each line (and use only utf-8 encoding):
   <foreign_wod> -- <native_lang_word>
   or
   <foreign_wod> -- <native_lang_word> // <number_of_rehearsals>, <time_of_the_latest_rehearsal (integer)>
3) start main.py via Python interpreter in command line.
   In Windows, for example, you can do it this way:
   1. Add python into PATH, if you have not managed it yet. If you don't know how, google it
   2. start cmd
   3. write: python <main.py location>
4) Enjoy it

System requirement:
1) Installed Python v.3.5 or larger
2) Installed re, random and time modules
