import core.adfisher as adfisher

site_file = 'substance.txt'
log_file = 'log.substance.txt'


## Set up treatments

treatment1 = adfisher.Treatment("substance")
treatment1.login2fb()
treatment1.opt_in()
treatment1.visitfb()
treatment1.visit_sites(site_file)

treatment2 = adfisher.Treatment("null")
treatment2.opt_in()

## Set up measurement

measurement = adfisher.Measurement()
measurement.get_ads(site='bbc', reloads=10, delay=5)

## Run Experiment

adfisher.run_experiment(treatments=[treatment1, treatment2], measurement=measurement, 
	agents=2, blocks=20, log_file=log_file, timeout=500)
	
## Analyze Data

adfisher.run_ml_analysis(log_file, verbose=True)
