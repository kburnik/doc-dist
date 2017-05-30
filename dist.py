#!/usr/bin/env python
import argparse
import numpy as  np
import os
import re
import string


def ssd_dist(a, b):
  """Computes the sum of squares distance between two vectors."""
  return np.sum((a - b) ** 2)


def cosine_dist(a, b):
  """Computes the cosine distance between two vectors.
     as defined here: https://en.wikipedia.org/wiki/Cosine_similarity"""
  similarity = float(np.sum(a * b)) / (np.linalg.norm(a) * np.linalg.norm(b))
  distance = 1.0 - similarity
  return distance


DISTANCE_METHODS = {'ssd': ssd_dist, 'cos': cosine_dist}
"""Mapping of selected distance method and implementation."""


DEFAULT_DISTANCE_METHOD = 'ssd'
"""Default distance method."""


def extract_words(document):
  """Computes the list of normalized words for the given document."""
  # Make all words lowercase and remove surrounding spaces.
  text = document.lower().strip()
  # Remove double spaces and replace tabs and newlines with single spaces.
  text = re.sub(r'\s+', ' ', text)
  # Remove punctuation.
  text = text.translate(None, string.punctuation)
  # Remove punctuation.
  text = re.sub('[' + re.escape('.,') + ']', '', text)
  # Break into list of words.
  words = text.split(' ')
  return words


def remove_stop_words(word_list, stop_word_set):
  """Removes all ocurrences of words in the stop_word_set from the word_list."""
  return [word for word in word_list if not word in stop_word_set]


def compare_documents(documents, stop_words=[], method=DEFAULT_DISTANCE_METHOD,
                      verbose=False):
  """Compares two or more in memory documents. The stop words are first removed
     from the document text and the distance is computed using the provided
     method."""
  dist = DISTANCE_METHODS[method]
  """The distance method used for comparing the document vectors."""

  stop_word_set = set(stop_words)
  """The set of stop words to exclude from the document vectors."""

  freq_map = dict()
  """The map of word frequences for each document. Key is the word and
     value is the vector for the word frequency in each document."""

  # Parse the documents and extract vectors via the frequency map.
  for i, document in enumerate(documents):
    # Sanitize and break up the document.
    words = extract_words(document)
    words = remove_stop_words(words, stop_words)

    # Build up the frequency map.
    for word in words:
      if not word in freq_map:
        freq_map[word] = [0] * len(documents)
      freq_map[word][i] += 1

  distinct_words = freq_map.keys()
  """Distinct words as ordered in the vectors."""

  vectors = np.transpose(freq_map.values())
  """The word frequency vectors. Suitable for comparison."""

  # Make all comparisons.
  for i in range(len(vectors) - 1):
    for j in range(i + 1, len(vectors)):
      d = dist(vectors[i], vectors[j])
      yield (i, j, d)

  if verbose:
    max_word_length = max([len(word) for word in distinct_words])
    output_format_str = "%" + str(max_word_length) + "s"
    output_format_int = "%" + str(max_word_length) + "d"
    for word in distinct_words:
      print output_format_str % word,
    print ""
    for vector in vectors:
      for value in vector:
        print output_format_int % value,
      print ""



if __name__ == "__main__":
  ap = argparse.ArgumentParser()
  ap.add_argument("-f", "--file",
                  type=str,
                  nargs='*',
                  default=None,
                  help="Two or more files to compare.")
  ap.add_argument("-i", "--inline",
                  type=str,
                  nargs='*',
                  default=None,
                  metavar="TEXT",
                  help="Two or more inline sentences to compare.")
  ap.add_argument("-m", "--method",
                  type=str,
                  choices=DISTANCE_METHODS.keys(),
                  default=DEFAULT_DISTANCE_METHOD,
                  help="Method for distance computation.")
  ap.add_argument("-s", "--stop_word_file",
                  type=str,
                  default="stop-word-list.txt",
                  help="Path to the stop word list file.")
  ap.add_argument("-v", "--verbose",
                  default=False,
                  action="store_true",
                  help="Display the word vectors when done.")
  args = ap.parse_args()

  if args.file is not None and len(args.file) < 2:
    ap.error("Must specify at least 2 files with -f/--file option.")

  if args.inline is not None and len(args.inline) < 2:
    ap.error("Must specify at least 2 values with -i/--inline option.")

  documents = None

  if args.file:
    documents = []
    for file in args.file:
      if not os.path.exists(file):
        raise Exception("File does not exist: %s" % file)

      with open(file, "r") as f:
        documents.append(f.read().strip())
  elif args.inline:
    documents = args.inline

  if not os.path.exists(args.stop_word_file):
    raise Exception("Stop word file does not exist: %s" % args.stop_word_file)

  with open(args.stop_word_file, "r") as f:
    stop_words = [word.rstrip() for word in f]

  if documents is None:
    ap.print_help()
    ap.exit(1)

  results = compare_documents(documents, stop_words, args.method, args.verbose)

  for i, j, d in results:
    print "Comparing documents %d and %d. %s distance = %.4lf" % \
        (i + 1, j + 1, args.method, d)





