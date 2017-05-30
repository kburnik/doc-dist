# Document distance

This project showcases a simple document distance computation implemented in
Python. The method used for evaluating similarity (distance) is the popular SSD
(Sum of Squares Distance) algorithm, however the Cosine Distance method is
available as well.

Stop words are always excluded as defined by the stop-word-list.txt

## Installation

```sh
virtualenv venv -p python2.7
. venv/Scripts/activate # Git bash in Windows
pip install -r requirements.txt
```

## Running the tool

```sh
# Compare inline text.
./dist.py -i "First sentence." "Second sentence" ... "Nth sentence."

# Compare files
./dist.py -f file1 file2 ... fileN
```

### Options

* to use cosine distance, use the `-m cos` option
* to output the computed vectors, use the `-v` option for verbosity
* to specify different stop-words file, use the `-s path_to_file` option


## Sample run

```sh
./dist.py \
    --method cos \
    --verbose \
    --inline \
    "Today is a nice day!" \
    "Tomorrow will also be a nice day..." \
    "This sentence has nothing in common with the other two."
```

Sample output

```
Comparing documents 1 and 2. cos distance = 0.3333
Comparing documents 1 and 3. cos distance = 1.0000
Comparing documents 2 and 3. cos distance = 1.0000
sentence      day   common tomorrow    today     nice
       0        1        0        0        1        1
       0        1        0        1        0        1
       1        0        1        0        0        0
```

## Testing and Evaluation

You can test the program on email spam messages. An example file
spam_samples.txt is provided. Also you can use the provided examples a.txt
b.txt and c.txt.

--

The problem author is
[Dr.sc. Marko Horvat, dipl. ing.](http://marko-horvat.name/site/)
