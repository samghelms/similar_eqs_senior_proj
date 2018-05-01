from pipeline import pipeline

def test_pipeline():
	pipeline('eqs_100k.tsv', 'test_pipeline_out')
	assert len(open('test_pipeline_out').readlines()) == 3111