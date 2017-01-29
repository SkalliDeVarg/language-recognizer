# language-recognizer
Neuron based AI which learns languages, recognizes their specific patterns and determines the language of a given word.
It trains on the enclosed wordbooks, is able to test itself spitting out success percentages and you can ask it your own words.

This program is fully modular, takes as much languages as you want (and your RAM is able to manage), 
has stacked patterns for 1 to ∞ letter constructions which are specific on the location etc.

It works like that:

    Letters
    |   Neuron Layers
    |   1   2   3   4    ...
    E - E   |   |   |
            EX  |   |
    X - X       EXA |
            XA      EXAM
    A - A       XAM
            AM      XAMP
    M - M       AMP
            MP      AMPL
    P - P       MPL
            PL      MPLE
    L - L       PLE  |
            LE   |   |
    E - E    |   |   |
        |    |   |   |
        sum+sum+sum+sum=chance
   
It can convert all words to a standard A-Z format to make the task a little more difficult for the apllication, but suprisingly
it doesn't make that much of a difference.

The application detects wordends by marking them with a "[". Also words split by "-", get marked that way when being converted.

The language files provided are from http://www.winedt.org/dict.html and I converted them to plain .txt files in utf_8.
They should work out of the box.

How to start?:

Simply run language_recognition.py with python3 and everything should be quite self explanatory.
If you want to import your own language files, make them .txt and utf_8 format and then test them for "strange" characters with
wordbooks.py . It will return a list of the letters which you should add in the converse1 and converse2 dicts in wordbooks.py .

The chances per pattern are raised when seen, so keep an eye on your RAM while training the program, your computer might lock
up when the RAM overfloods.

Additional functions:
- prompt for sentence or text detection (but please spare the .,!? etc.)
- learning steps changeable inside program
- choosable minimum and maximum length of words
- choosable maximum pattern length
- chances of individual patterns are callable
