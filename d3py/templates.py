d3py_template = '''<html>
<head>
	<script type="text/javascript" src="http://mbostock.github.com/d3/d3.js"></script>
	<script type="text/javascript" src="http://{{ host }}:{{ port }}/{{ name }}.js"></script>
	<link type="text/css" rel="stylesheet" href="http://{{ host }}:{{ port }}/{{ name }}.css">
    <link href='http://fonts.googleapis.com/css?family={{ font }}' rel='stylesheet' type='text/css'>
    
	<title>d3py: {{ name }}</title>
</head>

<body>
	<div id="chart"></div>
	<script>
		d3.json("http://{{ host }}:{{ port }}/{{ name }}.json", draw);
	</script>
</body>

</html>
'''
