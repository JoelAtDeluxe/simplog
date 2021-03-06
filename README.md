# Simplog

A simple, functional, opinionated logger for python

## Motivation

I generally only need to implement simple logging in my services. For the most part, I don't need anything especially fancy,
but I do need to stick to a consistent format, to help log analyzers do their job.

## Requirements

Currently this requires python 3 to run (developed against 3.6, but should compile under most recent versions)

## Usage

There are 3 main steps:

1. Generate a loging function:
   `log = logger.make_logger(print)`
2. Provide some input into logging function:
   `log("The program is exploding", level='error', why='Value Error')`
3. Observe the results:
    `2018-12-02T22:44:17.269137 level=error why="Value Error" msg="The program is exploding"`

Note that only level and message are requird. Level, in addition, has a default value of `info`. All other values
to be logged can be provided as keyword arguments (see above), which will be logged in `key=value` format. The current
system time is always provided as well, to help order the events.
In addition, there are some configuration possible that will make themselves useful in certain situations.

### Basic

Typically, all I need is a print that goes to standard out. You can accomplish this via this approach:

```python
from logger import make_logger, refine_logger
from uuid import uuid4

# Generate a logger function
main_logger = make_logger()

main_logger("This is happening on the mainline")
# prints to standard out: 'dt level=info msg="This is happening on the mainline"'

ctx_logger = refine_logger(main_logger, context=uuid4())
ctx_logger("A configured logger")
# prints to standard out: 'dt level=info context="ff088e2c-b127-4d8a-ba1d-347de59d302e" msg="A configured logger"'
```

### Advanced

If you need something more robust, then there are some configuration opportunities.

#### Preconfigre log values

If you want to ensure that consistent values are always provided with the logger, you can refine the logger via the
`refine_logger` method. This will return a new logger that always have the supplied arugments when called. Note that
under the hood, this is just a call to functool's `partial`

```python
log = make_logger()
rlog = refine_logger(log, confidence_level="100%")
rlog("Things are going well")
# Outputs: 2018-12-02T23:23:43.524875 level=info confidence_level=100% msg="Things are going well"

# These values is overwritable as well:
rlog("Things aren't looking so great", confidence_level="25%")
# Outputs: 2018-12-02T23:24:07.786726 level=info confidence_level=25% msg="Things aren't looking so great"
```

#### Output to somewhere else

This project is meant to log to the console, but will accept any function that accepts a string as input.

```python
# Completely untested, but in theory this would work
import os

def make_filewriter_function(output_path):
    writer = open(output_path, 'a', 0)  # Writing in unhuffered mode
    def write_fn(s):
      writer.write(s)

    def close_fn():
      os.close(writer)

    return write_fn, close_fn

write_fn, close_fn = make_filewriter_function('/var/log/my-script-log.log')
log = logger.make_logger(write_fn)
# ...
close_fn()
```

#### Change default labels

If you don't like `msg` and `level` you can easily switch these when making the logger
If you want to add a label for the time, you can do that too

```python
custom_log = logger.make_logger(print, message_label='message', level_label='logLevel', time_label='app_time')
custom_log("Look at that!")
# outputs: app_time=2018-12-02T23:06:59.566174 logLevel=info message="Look at that!"
```

#### Forcing quoting

By default, any value that does not have a space in it will be left unquoted, while any string that does have a space will be double-quoted
(i.e. `"Expect values like this"`)
If you always make to make sure your values are quoted, you can do that by supplying `force_quote=True` in the make_logger constructor.

#### Serialize non-standard values

If you have some class you want to log, you'll need to supply your own serializer. Once you have that, you can pass the serialize func
using the `to_string_func` parameter.

## Development

This project uses pipenv to aid development. See https://pipenv.readthedocs.io/en/latest/ for usage.

### Running tests

This project utilizes pytest for running unit tests. They can be run via:

```sh
pipenv shell
cd simplog
python -m pytest
```

## TODOs

1. Test & Optimize performance
2. Suport custom character escapes?
3. Add in support for mypy