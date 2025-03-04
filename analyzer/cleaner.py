#!/usr/bin/env python3

import numpy as np
import pandas as pd
import sys


def count_tags(df):
    tags = df['tags']
    tags = pd.concat([tags[col] for col in tags])
    tags = pd.DataFrame({'tag': tags, 'count': np.ones(len(tags))})
    return tags.groupby('tag').sum().sort_values('count', ascending=False)


def empty_tag(t):
    if len(t) > 0:
        return t
    else:
        return "unknown"


def clean_df(df):
    df['tags'].fillna("", inplace=True)
    df['date'] = pd.to_datetime(df['date'])
    df['tags'] = df['tags'].apply(lambda x: str(x).lower().split('\x1E'))
    df['tags'] = df['tags'].apply(empty_tag)


def load_playlist(fname):
    df = pd.read_csv(fname, names=['date', 'track', 'artist', 'tags'],
                     sep='\x1F')
    return df


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage:", sys.argv[0], "<infile> <outfile>")
        sys.exit(1)

    print("Cleaning and extracting tag ranking from", sys.argv[1])
    df = load_playlist(sys.argv[1])
    clean_df(df)
    tag_pop = count_tags(df)
    print("Done! Writing csv to", sys.argv[2])
    tag_pop.to_csv(sys.argv[2], sep='\x1F')
