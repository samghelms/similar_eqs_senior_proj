"""Main pipeline for creating the equations dataset"""
import argparse
from tok import tokenize, fix_macros, CouldNotFindError
from split import split
from filter_tokens import filter_tokens
from suitable import suitable
import json
import os

def pipeline(fpath, outfolderpath):
	os.mkdir(outfolderpath)
	outf = open('./' + outfolderpath+'/file_0.jsonlist', 'w+')
	error_ct = 0
	with open(fpath, 'rb') as f:
		for i, row in enumerate(f):
			# print(row)
			row = row.decode("unicode_escape").split('\t')
			rowid = row[0]
			row_val = row[1]
			tnized = None
			try:
				tnized = tokenize(row_val)
				# I added this step in to deal with the mysterious pmatrix command that was popping up
				# Maybe a macro that made it through demacro.py somehow?
				tnized_filt = filter_tokens(tnized, tokens_to_filter=['\\pmatrix, \\matrix'])
				fixed = fix_macros(tnized_filt)
			except CouldNotFindError:
				error_ct += 1
				continue

			spl = split(tnized)

			for expr in spl:
				# the split on equal sign expressions
				aligned = []
				for eq in expr:
					filt_expr = filter_tokens(eq)
					if suitable(filt_expr):
						aligned.append(filt_expr)

				if len(aligned) > 1:
					d = {}
					d['rowid'] = rowid
					d['aligned'] = aligned
					d['source_equation'] = row_val
					d['tokenized_equation'] = tnized
					d['tokenized_equation_filtered'] = filt_expr
					outf.write(json.dumps(d)+'\n')
			if i % 10000 == 0:
				print("{i} done".format(i=i))
			if i % 100000 == 0 and i > 0:
				outf.close()
				new_f_path = './' + outfolderpath + '/file_' + str(int(i / 1000)) + '.jsonlist'
				outf = open(new_f_path, 'w+')
	print("done. {error_ct} errors".format(error_ct=error_ct))


# python pipeline.py -f eqs_100k.tsv -o test_pipeline_out 
if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Process some integers.')
	parser.add_argument('-f', type=str, help='path to the file you want to get equations from')
	parser.add_argument('-o', type=str, help='path to the file you want to write to')

	args = parser.parse_args()

	pipeline(args.f, args.o)

