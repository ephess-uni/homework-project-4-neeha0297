# hp_4.py
#
from datetime import datetime, timedelta
from csv import DictReader, DictWriter
from collections import defaultdict


def reformat_dates(old_dates):
    """Accepts a list of date strings in format yyyy-mm-dd, re-formats each
    element to a format dd mmm yyyy--01 Jan 2001."""
    formatted_result = [datetime.strptime(each_old_date, "%Y-%m-%d").strftime('%d %b %Y') for each_old_date in old_dates]    
    return formatted_result

def date_range(start, n):
    """For input date string `start`, with format 'yyyy-mm-dd', returns
    a list of of `n` datetime objects starting at `start` where each
    element in the list is one day after the previous."""
    if not isinstance(start, str) or not isinstance(n, int):
        raise TypeError()
    date_range_list = []
    for x in range(n):
        date_range_list.append(datetime.strptime(start, '%Y-%m-%d') + timedelta(days=x))
    return date_range_list


def add_date_range(values, start_date):
    """Adds a daily date range to the list `values` beginning with
    `start_date`.  The date, value pairs are returned as tuples
    in the returned list."""
    pair_of_date_valeu = date_range(start_date, len(values))
    zip_list = list(zip(pair_of_date_valeu, values))
    return zip_list


def fees_report(infile, outfile):
    """Calculates late fees per patron id and writes a summary report to
    outfile."""
    headers = ("book_uid,isbn_13,patron_id,date_checkout,date_due,date_returned".
              split(','))
    dict_for_late_fees = defaultdict(float)
    with open(infile, 'r') as fl:
        linesData = DictReader(fl, fieldnames=headers)
        rows = [row for row in linesData]
    rows.pop(0)
    for book in rows:
        patronID = book['patron_id']
        original_date_due = datetime.strptime(book['date_due'], "%m/%d/%Y")
        returned_date = datetime.strptime(book['date_returned'], "%m/%d/%Y")
        dsdrf = (returned_date - original_date_due).days
        
        dict_for_late_fees[patronID]+= 0.25 * dsdrf if dsdrf > 0 else 0.0
            
    output_format = [
        {'patron_id': pn, 'late_fees': f'{fs:0.2f}'} for pn, fs in dict_for_late_fees.items()
    ]
    with open(outfile, 'w') as fl:
        id_fee = DictWriter(fl,['patron_id', 'late_fees'])
        id_fee.writeheader()
        id_fee.writerows(output_format)


# The following main selection block will only run when you choose
# "Run -> Module" in IDLE.  Use this section to run test code.  The
# template code below tests the fees_report function.
#
# Use the get_data_file_path function to get the full path of any file
# under the data directory.

if __name__ == '__main__':
    
    try:
        from src.util import get_data_file_path
    except ImportError:
        from util import get_data_file_path

    # BOOK_RETURNS_PATH = get_data_file_path('book_returns.csv')
    BOOK_RETURNS_PATH = get_data_file_path('book_returns_short.csv')

    OUTFILE = 'book_fees.csv'

    fees_report(BOOK_RETURNS_PATH, OUTFILE)

    # Print the data written to the outfile
    with open(OUTFILE) as f:
        print(f.read())
