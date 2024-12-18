cat <<EOF
<html>
<head>
	<title>TCB Change Log</title>
	<style>
		body {
			font-family: 'Courier New', Courier, monospace;
			background-color: #000;
			color: #0f0;
			margin: 0;
			padding: 20px;
			line-height: 1.5;
		}
		h1, h2 {
			color: #ff00ff;
			text-shadow: 2px 2px 0 #00ffff;
		}
		pre {
			background-color: #111;
			border: 1px solid #0f0;
			padding: 10px;
			overflow: auto;
			white-space: pre-wrap; /* Wrap long lines */
		}
		ul {
			list-style-type: none; /* Remove default bullets */
			padding-left: 0; /* Remove default padding */
		}
		li {
			margin-bottom: 10px;
			padding: 5px;
			border: 1px dashed #0f0;
			background-color: rgba(0, 255, 0, 0.1);
		}
		li:hover {
			background-color: rgba(0, 255, 0, 0.3);
		}
	</style>
</head>
<body>
EOF

ls -rt diffs/* | xargs cat 2>/dev/null

cat <<EOF
</body>
</html>
EOF
