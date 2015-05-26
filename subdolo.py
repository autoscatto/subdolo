#!/usr/bin/env python3
import re
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='DvdSubtitle to .srt converter')
    parser.add_argument('--out', dest='outf', nargs=1, help='converted file name (overwrite if exist)')
    parser.add_argument('-n', dest='stdo', action="store_true", help='write converted to stdoutput')
    parser.add_argument('inputf', action="store", type=str, help=".sub file to convert")
    results = parser.parse_args()

    time_regex = re.compile('\{T (\d\d:\d\d:\d\d:\d\d)\n([^\}]+)\}\n{T (\d\d:\d\d:\d\d:\d\d)')
    head_regex = re.compile('\{HEAD[\s\S]+LICENSE=[\s]\}')


    def formattime(t):
        return t[:-3]+','+t[-2:]+'0'

    try:
        with open(results.inputf, 'r') as infile:
            txt = infile.read()
            txt = re.sub('\r', "", txt)
            textnoh = re.sub(head_regex, "", txt)
            tlist = re.findall(time_regex, textnoh)

            outlines = ["%d\n%s --> %s\n%s\n" % (i, formattime(x[0]), formattime(x[2]), x[1])
                        for i, x in enumerate(tlist)]
            if results.stdo:
                print(''.join(outlines))
            else:
                outf = results.outf
                if outf is None:
                    outf = results.inputf[:-3]+'srt'

                if not outlines or len(outlines) == 0:
                    raise ValueError('Invalid DvdSubtitle format')

                with open(outf, 'w') as outfile:
                    outfile.writelines(outlines)

    except IOError as e:
        print("%s: invalid file or invalid permission!" % e.filename)

    except ValueError as e:
        print(e)

    except Exception as e:
        print("DRAMA!\nPlease submit a issue to https://github.com/autoscatto/subdolo/issues")

    finally:
        print(u"Conversion complete! \u2665")
