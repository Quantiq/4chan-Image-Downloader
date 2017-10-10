# Chanimg
Chanimg is a simple commandline script written in python that retrieves images from a given 4chan thread.

## Usage
<code>python3 chanimg.py url [optional arguments]</code>

Chanimg will save images to a folder under /Output as "(board id) - (thread number) - (thread title)".

## Optional Arguments

<code>-h, --help</code> Show the help message and exit

<code>-m, --monitor</code> Monitors a thread.

<code>-u, --update TIME</code> Specifies the amount of time in seconds to update a thread (Default: 60). Higher values are recommended for slow boards.

<code>-o, --original</code> Saves images as original filenames.

<code>-f, --foldername "NAME"</code> Save images to a custom folder name.

<code>-v, --verbose </code> Increase output verbosity.