STABLECliPy

Lightweight CLI version of STABLESElectron2. CLI version for a snappier UX, and so that my nerd friends will actually use my software. Log parsing is optimized by performing substring searches line by line, and then if substring matches, then we check regex (string matching is much faster under the hood than regex'ing every line).
Contains a controller class for each database table, and a controller class for the CLI.
