import argparse
import random
import json
import os

def get_parser():
	parser = argparse.ArgumentParser(description='Simple sequence generator')
	parser.add_argument('-d','--dest', action="store",default="output", help="Destination folder")
	parser.add_argument('config', action="store", help="JSON config file")

	return parser


				

def mutate(nucl, error_prob,supstitution_only):
	is_error = error_prob>random.uniform(0.0,1.0)
	if is_error:
		def substitution(nucl):
				short_nucls = nucls[:]
				short_nucls.remove(nucl)
				return short_nucls[random.randint(0, len(short_nucls)-1)]

		if supstitution_only:
			nucl = substitution(nucl)
		else:
			def deletion(nucl):
				return ""
			def addition(nucl):
				side = random.randint(0, 1)
				if side==0:
					return nucls[random.randint(0, len(nucls)-1)] + nucl 
				else:
					return nucl + nucls[random.randint(0, len(nucls)-1)]

			options =[deletion, addition, substitution]
			nucl = options[random.randint(0, len(options)-1)](nucl)
			

	return nucl
def main():
	args=get_parser().parse_args()
	config = None
	
	with open(args.config) as json_file:
		config = json.load(json_file)
 

	if not os.path.isdir(args.dest):
		os.mkdir(args.dest)	
	"""
	Stvaranje baznih sekvenci 
	"""
	for lenght in config['lenghts']:
		
		lenght_dir = "%s/len_%d"%(args.dest, lenght)
		if not os.path.isdir(lenght_dir):
			os.mkdir(lenght_dir)	

		with open("%s/base"%lenght_dir, 'w') as fout:
			for i in xrange(lenght):
				nucl = nucls[random.randint(0, len(nucls)-1)]
				fout.write(nucl)
	

	"""
	Stvaranje mutiranih sekvenci
	"""

	for lenght in config['lenghts']: 
		lenght_dir = "%s/len_%d"%(args.dest, lenght)
		for error_prob_index, seq_count in enumerate(config["seq_counts"]):
			error_prob = config["error_probs"][error_prob_index]

			error_prob_dir = ("%s/len_%d/err_%f"%(args.dest, lenght,error_prob)).rstrip('0').rstrip('.')
			if not os.path.isdir(error_prob_dir):
				os.mkdir(error_prob_dir)	

			for i in xrange(seq_count):
				with open("%s/base"%lenght_dir, 'r') as fin:
					with open("%s/%d"%(error_prob_dir, i+1), 'w') as fout:
						for j in xrange(lenght):
							nucl = fin.read(1)
							new_nucl=mutate(nucl,error_prob, config["substitution_only"])
							fout.write(new_nucl)


if __name__ == '__main__':
	nucls = ['A', 'C', 'G', 'T']
	main()

