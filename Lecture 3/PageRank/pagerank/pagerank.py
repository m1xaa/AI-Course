import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    links = corpus[page]
    probability_dictionary = {}

    for page_name in corpus:
        initial_probability = (1 - damping_factor) / len(corpus)

        if page_name in links:
            initial_probability += damping_factor / len(links)
        probability_dictionary[page_name] = initial_probability
    
    return probability_dictionary

def get_first_page(corpus):
    names = [name for name in corpus.keys()]
    initial_probability = 1/len(names)
    probabilities = [initial_probability for _ in names]
    first_page = random.choices(names, probabilities)[0]
    return first_page


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    histogram = {name: 0 for name in corpus.keys()}
    page = get_first_page(corpus)

    for i in range(n):
        probability_dict = transition_model(corpus, page, damping_factor)
        names = [name for name in probability_dict.keys()]
        probabilities = [probability_dict[name] for name in probability_dict.keys()]
        page = random.choices(names, probabilities)[0]
        histogram[page] += 1
    
    for page in histogram:
        histogram[page] = histogram[page] / n 

    return histogram

def find_links_to_current(corpus, current):
    links = []
    for page in corpus:
        if current in corpus[page]:
            links.append(page)
    return links


def iterate_pagerank(corpus: dict, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    probability_dicitonary = {name: 1/len(corpus) for name in corpus.keys()}
    new_dictionary = {}

    while True:
        should_stop = {name: False for name in corpus.keys()}
        for page in corpus:
            links = find_links_to_current(corpus, page)
            new_rank = (1 - damping_factor) / len(corpus) + damping_factor*sum(probability_dicitonary[name]/len(corpus[name]) for name in links)
            if abs(probability_dicitonary[page] - new_rank) < 0.001:
                should_stop[page] = True
            else:
                should_stop[page] = False
            new_dictionary[page] = new_rank
        difference = max([abs(new_dictionary[x] - probability_dicitonary[x]) for x in probability_dicitonary])
        if difference < 0.001:
            break
        else:
            probability_dicitonary = new_dictionary.copy()
    return probability_dicitonary
        


if __name__ == "__main__":
    main()
