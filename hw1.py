# Copyright 2021 Mario Graff Guerrero

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re
from typing import Tuple, List
from collections import Counter


def start_project(txt: str) -> Tuple[int, int]:
    """Use regular expressions to find 
    the start and end point of the line *** START OF THE PROJECT ... *** ...
    The ... indicates any text except the carriage return. 
    Usage: 

    >>> start_project("*** START OF THE PROJECT GUTENBERG EBOOK THE ILIAD ***")
    (0, 54)
    >>> start_project("Hi! *** START OF THE PROJECT GUTENBERG EBOOK WAR AND PEACE *** Excellent book")
    (4, 77)

    This function will be tested on two of the 
    25 most downloaded books from https://www.gutenberg.org. 
    The format used is txt and the file is read using open(fname).read()"""
    return (re.search(r'\*\*\* START OF THE PROJECT GUTENBERG EBOOK(.*) \*\*\*', txt)).span() #match the start of the book with the regex, then find its indexes

def entity_identification(txt: str) -> Counter:
    """Count the number of appearances of each entity using 
    the simple heuristic of identifying as an entity 
    each word starting with a capital letter or an abbreviation.
    Usage:
    
    >>> entity_identification("America is a continent.")
    Counter({'America': 1})
    >>> entity_identification("The United States is in America")
    Counter({'The': 1, 'United': 1, 'States': 1, 'America': 1})
    >>> entity_identification("U.S.A. is in America and Mexico is in America")
    Counter({'America': 2, 'U.S.A.': 1, 'Mexico': 1})
    >>> entity_identification("USA. U.S.A America.")
    Counter({'USA.': 1, 'U.S.A': 1, 'America.': 1})
    """
    return Counter(re.findall(r'[A-Z][a-zA-Z\.]*', txt)) #find all instances of an entity, and add to their value in a counter


def replace_user(txt: str) -> str:
    """Replace the appearance of a username (e.g. @mario) with the tag @user
    Usage:

    >>> replace_user("Hi @mgraffg!")
    'Hi @user!'
    >>> replace_user("@_mgraffg @mgraffg_ @mgraffg_2 @mgraffg?")
    '@user @user @user @user?'
    """
    return re.sub(r'@[a-zA-Z0-9_]+', '@user', txt) #substitute any instances of @ followed immediately by text with @user


def sentence_accuracy(y: List[str], hy: List[str]) -> float:
    """Computes the accuracy of a sentece tokenizer.
    Usage:
    
    >>> sentence_accuracy(['a', 'b'], ['b', 'a'])
    1.0
    >>> sentence_accuracy(['a', 'a'], ['a'])
    0.5
    >>> sentence_accuracy(['a', 'b', 'b', 'a'], ['b', 'a', 'a'])
    0.75
    """
    #punkt - does not modify inputs
    count = 0 # to count the number of strings from the 'gold' list found in the tokenized list
    tokenized = hy[:]
    for currStr in y:   #iterate through 'gold' set of sentences, if sentence in tokenized set remove it and add 1 to count
        if (currStr in tokenized):
            count += 1
            tokenized.remove(currStr)
    return count / len(y) 
