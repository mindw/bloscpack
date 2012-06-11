# ∴ bloscpack

Command line interface to Blosc via python-blosc

## ∴ Description

This script provides a command line interface to
[Blosc](http://blosc.pytables.org/trac), a high performance, multi-threaded,
blocking and shuffeling compressor. The interface is realized by using the
[argparse](http://docs.python.org/dev/library/argparse.html) library
and [python-blosc](https://github.com/FrancescAlted/python-blosc) bindings.

## ∴ Website

Repository is at: https://github.com/esc/bloscpack

## ∴ Dependencies

* Python 2.7
* [python-blosc](https://github.com/FrancescAlted/python-blosc) (provides Blosc)

## ∴ Installation

Add the ``blpk`` file to your ``$PATH`` somehow. For example by copying using
dereferencing (``-L``), since ``blpk`` is a sym-link to ``bloscpack.py``:

    zsh» cp -L blpk ~/bin

Or, of course, use the standard ``setup.py``:

    zsh» python setup.py install

... which may require superuser privileges.

## ∴ Usage

Bloscpack has a number of global options and two subcommands: ``[c |
compress]`` and ``[d | decompress]`` which each have their own options.


Help for global options and subcommands:

    zsh» ./blpk --help
    [...]

Help for each one of the subcommands:

    zsh» ./blpk compress --help
    [...]
    zsh» ./blpk decompress --help
    [...]

## ∴ Examples

Basic compression:

    zsh» ./blpk c data.dat

... will compress the file ``data.dat`` to ``data.dat.blp``

Basic decompression:

    zsh» ./blpk d data.dat.blp data.dcmp

... will decompress the file ``data.dat.blp`` to the file ``data.dcmp``. If you
leave out the ``[<out_file>]`` argument, bloscpack will complain that the file
``data.dat`` exists already and refuse to overwrite it:

    zsh» ./blpk d data.dat.blp
    blpk: error: output file 'data.dat' exists!

If you know what you are doing, you can use the global option ``[-f |
--force]`` to override the overwrite checks:

    zsh» ./blpk -f d data.dat.blp

Incidentally this works for compression too:

    zsh» ./blpk c data.dat
    blpk: error: output file 'data.dat.blp' exists!
    zsh» ./blpk -f c data.dat

By default, the number of threads that Blosc uses is determined by the number
of cores detected on your system. You can change this using the ``[-n |
--nthreads]`` option:

    zsh» ./blpk -n 1 c data.dat

There are some useful additional options for compression, that are passed
directly to Blosc:

* ``[-t | --typesize]``
  Typesize used by Blosc (default: 4):
  ``zsh» ./blpk c -t 8 data.dat``
* ``[-l | --level]``
  Compression level (default: 7):
  ``zsh» ./blpk c -l 3 data.dat``
* ``[-s | --no-shuffle]``
  Deactivate shuffle:
  ``zsh» ./blpk c -s data.dat``

In addition, there are two mutually exclusive options for bloscpack itself,
that govern how the file is split into chunks:

* ``[-z | --chunk-size]``
  Desired approximate size of the chunks, where you can use human readable
  strings like ``8M`` or ``128K`` (default: ``4MB``):
  ``zsh» ./blpk -d c -z 128K data.dat``
* ``[-c | --nchunks]``
  Desired number of chunks:
  ``zsh» ./blpk -d c -c 2 data.dat``

Lastly there are two options to control how much output is produced,

The first causes basic info to be printed, ``[-v | --verbose]``:

    zsh» ./blpk -v c data.dat
    blpk: getting ready for compression
    blpk: input file is: data.dat
    blpk: output file is: data.dat.blp
    blpk: using 8 threads
    blpk: input file size: 1.49G
    blpk: nchunks: 382
    blpk: chunk_size: 4.0M
    blpk: output file size: 688.07M
    blpk: compression ratio: 0.450935
    blpk: done

... and ``[-d | --debug]`` prints a detailed account of what is going on:

    zsh» ./blpk -d c -z 0.5G data.dat
    blpk: command line argument parsing complete
    blpk: command line arguments are:
    blpk:   nchunks: None
    blpk:   force: False
    blpk:   verbose: False
    blpk:   out_file: None
    blpk:   subcommand: c
    blpk:   in_file: data.dat
    blpk:   chunk_size: 536870912
    blpk:   debug: True
    blpk:   shuffle: True
    blpk:   typesize: 4
    blpk:   clevel: 7
    blpk:   nthreads: 8
    blpk: getting ready for compression
    blpk: blosc args are:
    blpk:   typesize: 4
    blpk:   shuffle: True
    blpk:   clevel: 7
    blpk: input file is: data.dat
    blpk: output file is: data.dat.blp
    blpk: using 8 threads
    blpk: input file size: 1.49G
    blpk: 'chunk_size' proposed
    blpk: nchunks: 3
    blpk: chunk_size: 512.0M
    blpk: last_chunk_size: 501.88M
    blpk: bloscpack_header: 'blpk\x03\x00\x00\x00'
    blpk: chunk '0' written, in: 512.0M out: 235.14M
    blpk: chunk '1' written, in: 512.0M out: 229.74M
    blpk: chunk '2' (last) written, in: 501.88M out: 223.19M
    blpk: output file size: 688.07M
    blpk: compression ratio: 0.450932
    blpk: done


## ∴ Testing

Basic tests, runs quickly:

    zsh» nosetests
    [...]

Extended tests:

    zsh» nosetests test_bloscpack.py:pack_unpack_extended
    [...]

## ∴ Benchmark

Using the provided ``bench/blpk_vs_gzip.py`` script on a ``Intel(R) Core(TM) i7
CPU 960  @ 3.20GHz`` cpu with 4 cores and active hyperthreading yields the
following results:

    zsh» PYTHONPATH=. bench/blpk_vs_gzip.py
    create the test data..........
    Input file size: 1.49G
    Will now run bloscpack...
    Time: 6.69 seconds
    Output file size: 557.93M
    Ratio: 0.37
    Will now run gzip...
    Time: 141.38 seconds
    Output file size: 924.05M
    Ratio: 0.61

As was expected from previous benchmarks of Blosc using the python-blosc
bindings, Blosc is both much faster and has a better compression ratio for this
kind of structured data.

## ∴ Implementation Details

The input is split into chunks since a) we wish to put less stress on main
memory and b) because Blosc has a buffer limit of 2GB (May 2012). By default
the chunk-size is a moderate ``4MB`` which should be fine, even for less
powerful machines. The last chunk always contains the remainder and has thus
size either equal too or less than the rest of the chunks.

Bloscpack adds an 8 byte header to a compressed file, which consists of a 4
byte magic string, ``blpk``, and a 4 byte little-endian unsigned integer which
designates how many chunks there are.  Effectively, this limits the number of
chunks to ``2**32-1 = 4294967295``, but this should not be relevant in
practice. In terms of overhead, this means that for a given file bloscpack
will add a total of 8 bytes for itself and 16 bytes for each chunk compressed
by Blosc.

## ∴ TODO

* possibly provide a BloscPackFile abstraction, like GzipFile
* document library usage
* --equal-size argument to create large chunks of equal size
* --max-size to create the largest possible chunks, regardless of input size
* Use the special token -1 and a singned 64 int to denote the number of chunks
* subcommand e or estimate to estimate the size of the uncompressed dtaa.
* ... this allows it to be used as a filter, since the data size needs not be
  known in advance
* then add --raw-input and --raw-output switches to allow stuff like:
  cat file | blpk --raw-input --raw-output compress > file.blp
* fix the typesize default argument, possibly make it platform dependent
* since we now have potentially small chunks, the progressbar becomes relevant
  again

## ∴ Changelog

### ● v0.1.0-rc2 - Sat Jun 09 2012

* Default chunk-size now ``4MB``
* Human readable chunk-size argument
* Last chunk now contains remainder
* Pure python benchmark to compare against gzip
* Benchmark to measure the effect of chunk-size
* Various minor fixes and enhancements

### ● v0.1.0-rc1 - Sun May 27 2012

* Initial version
* Compression/decompression
* Command line argument parser
* README, setup.py, tests and benchmark

## ∴ Thanks

* Fracesc Alted for writing Blosc in the first place and for providing
  code-review and feedback on bloscpack

## ∴ Author, Copyright and License

(C) 2012 Valentin Haenel <valentin.haenel@gmx.de>

bloscpack is licensed under the terms of the MIT License.

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
