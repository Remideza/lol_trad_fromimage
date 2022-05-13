# League of Legends ingame traductor

Traduce the League of legends ingame chat by capturing the ingame window

## Requirements

- TesseractOCR with the language packages you plan on using (https://tesseract-ocr.github.io/tessdoc/Data-Files-in-different-versions.html)
- Mentionned python packages at the start of the 

## Config

- WINDOWPOS : Position and size of the chatbox window
- LINESIZE  : Textline size on the current chatbox, there is a debug preview of thoses line to check if your values are correct, run with DEBUG_IMAGE = True to have an example
- LANG_FROM_TESS  : Language pack to use for image to text recognition (see previous link)
- LANG_FROM_GTRAD : Name of the language in the google trad api (https://www.labnol.org/code/19899-google-translate-languages#google-translate-languages)
- LANG_TO_GRAD    : Name of the language to traduce to
- DEBUG_WINDOW    : Show lines during the runtime
- DEBUG_IMAGE     : Run from a saved screenshot of a game to debug window position and tweek the code
