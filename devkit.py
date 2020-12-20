def set_env(sel_key):
	from os import path, getenv
	from dotenv import load_dotenv

	envs = {
		'd': 'development',
		'p': 'production',
	}

	basedir = path.abspath(path.dirname(__file__))
	load_dotenv(path.join(basedir, '.env'))
	e = getenv('FLASK_ENV')
	if e is None:
		with open(path.join(basedir, '.env'), 'a') as f:
			f.write('\nFLASK_ENV={envs[sel_key]}')
			return envs[sel_key]
	else:
		return e
	# overwrite the variable in dotenv file
	'''elif e != envs[sel_key]:
		with open(path.join(basedir, '.env'), 'r') as f:
			lines = f.readlines()
		with open(path.join(basedir, '.env'), 'w') as f:
			for line in lines:
				if 'FLASK_ENV=' in line:
					f.write('FLASK_ENV={envs[sel_key]}')
				else:
					f.write(line)
	return envs[sel_key]'''
