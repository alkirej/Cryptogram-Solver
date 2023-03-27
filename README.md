# Cryptogram-Solver
Utility written in Python 3 that will attempt to solve a cyrptogram in a minute or two.

**What is a Cryptogram?**
A Cryptogram starts as with English sentence, phrase, etc.
Each letter in the the original phrase is changed out for a different letter.  
The letters are changed out in the same way for the entire document.

Here is an example:

    ORIGINAL: Today is Sunday.

    CRYPTOGRAM: Isloe tn Nxrloe.

    This is not unique.  The same phrase could become Mylcb ah Hwvlcb.

**Rules used in this program:**
- Case will be consistent between the original phrase and the cryptogram.
    - This means if s becomes n, then S will become N
- Spaces and punctuation are not changed.


The program was written and tested on Ubuntu Linux, so the usage syntax is given
for Ubuntu.

# Command Line Usage:
python cryptogram.py "Cryptogram text here."

The utility will attempt to solve the cryptogram you provide.

# Alternate Usage:
python cryptogram.py

The utility will select from a set of cryptograms it knows and attempt to solve it.

# Solutions:
An example solution looks like this:

    A serious and good philosophical wor[km] could [fmbq]e written consisting entirely o[6] [fmj]o[km]es.
    
As you can see, most text is translated correctly.  This it typical in my experience though not guaranteed.  Difficult cryptograms may not be solvable by this utility.

For letters the solver could not determine completely, the options are given in square brackets [].
- wor[km] indicates the word could be work or worm.  The solver does not have enough information to determine which.  Us humans understand context and can tell the answer would be work.
- o[6] means there are 6 possible letters possible here such as **of** or **ok**.  **on** is not possible since it already knows what letter is converted to n (see writte**n**)

# Final Notes
- The code includes a routine to generate a cryptogram if you would like to create your own. A little update to the code could easily have this utility convert your English text into a cryptogram.
- This solver only converts English phrases as it is provided an English dictionary and makes no attempt to handle not-English characters.
