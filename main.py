import os.path
import utils as u
import answers as a
import globals as g

file_exists: bool = os.path.exists(g.csv_file)

def main():
    '''Calls two functions'''
    '''1. Reads and manipulates data'''
    '''2. Answers questions and collates them into one output'''

    df = u.handler()
    a.collate_answers(df)

if __name__ == "__main__":
    main()