def set_env(sel_key):
	from os import path, getenv
	from dotenv import load_dotenv

	envs = {
		'd': 'development'
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
