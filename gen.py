import json
import os
import glob
import sys
import argparse

from page_contents import PageContents

# Load command line args
def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)
parser = argparse.ArgumentParser(
    prog='Website generator', 
    description='Generates the quinnjam.es website from markdown articles'
)
parser.add_argument('-v', '--verbose', 
    action='store_true', 
    help='Output additional information during build'
)
parser.add_argument('-e', '--erase',
    action='store_true',
    help='Erase the contents of the output directory before build'
)
parser.add_argument('-o', '--output-directory',
    help='The directory where output webpages are saved (default:\'%(default)s\')',
    default='./output',
    type=dir_path,
    required=False
)
parser.add_argument('-a', '--article-directory',
    help='The directory from which to load articles (default:\'%(default)s\')',
    default='./articles',
    type=dir_path,
    required=False
)

# Parse args
args = parser.parse_args()
if args.verbose:
    print(f'Using args: {args}')

# Load page content
pages = []
if args.verbose:
    print(f'Loading articles from {args.article_directory}', end='')
article_files = glob.glob(f'{args.article_directory}/*')
if args.verbose:
    print(f' ({len(article_files)} files)')
for f in article_files:
    if args.verbose:
        print(f'    {f}', end='')
    with open(f, 'r') as o:
        # Parse article contents
        pages.append(PageContents(o, f))
    if args.verbose:
        print(f' ... {pages[-1].title} ({pages[-1].get_line_count()} lines)')

# Clear the existing output
if args.erase:
    if args.verbose:
        print(f'Erasing contents of {args.output_directory}', end='')
    output_files = glob.glob(f'{args.output_directory}/*')
    if args.verbose:
        print(f' ({len(output_files)} files)')
    for f in output_files:
        if args.verbose:
            print(f'    {f}')
        os.remove(f)

# Generate new pages
for page in pages:
    